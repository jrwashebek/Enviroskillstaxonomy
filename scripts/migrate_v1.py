#!/usr/bin/env python3
"""Migrate EMST v1 into v2 seed records (WP-02; ADR-0011; P-DE-01…13).

Inputs (hash-pinned): data/v1_baseline/ (copyB extract + source_text/), docs/decisions/v1_disposition.csv,
docs/decisions/candidate_disposition.csv, legacy/v1/docs/ working records (D7 lens table, Task 10 register).

Outputs (all deterministic):
  data/v2/{core,modules/<ns>}/competencies/seed-v1-<code>.yaml   222 competency seeds (validationStatus seed-v1)
  data/v2/{core,modules/<ns>}/tasks/seed-v1-<code>-T<n>.yaml     666 task seeds
  data/v2/assessments/emst-v1-*/copyB.jsonl, working-records.jsonl   v1 tags as prior evidence (raterType v1-analyst)
  data/v2/crosswalks/emst-v1/emst-v1_to_v2.sssom.tsv (+ .yml)    X1, generated from v1_disposition.csv + records
  data/v2/migration/v1_targets.csv                               every disposition target with its seed key
  data/v2/migration/restoration_sample.csv                       10% verbatim check of restored text
  data/v2/migration/MIGRATION_INFO.json                          input hashes and generated counts

Rules: content comes from the source text where the database lost it (D5 Knowledge/Application, 2,104 truncated
indicators, 19 title/description splits); v1 tags migrate as prior evidence only (rater v1-analyst-01, low
confidence, misalignment flags); stored summaries (modal fields, counts, Zero-Core, FPP, stability tier, reform
count) are not migrated; held Tribal content is flagged (ADR-0007 §D); v1-derived text carries
LicenseRef-EMSTv1-PendingDedication (ADR-0013, Q2 pending).

Authoring safety: an existing seed file is NEVER overwritten once it has left validationStatus seed-v1 or moved;
use --force only on a clean checkout. Assessment batches, X1, and migration/ files are regenerated.

Usage:
  python scripts/migrate_v1.py             # create missing seeds, regenerate tags, X1 and migration files
  python scripts/migrate_v1.py --x1-only   # regenerate X1 (and v1_targets.csv) from the current records
  python scripts/migrate_v1.py --check     # exit 1 if any generated file (or an untouched seed) differs
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emstlib as L  # noqa: E402

VERSION = "1.0.0"
AGENT = f"emstagent:migrate_v1@{VERSION}"
REVIEW_AGENT = "emstagent:de-a1@wp-02"
MIGRATION_TS = "2026-10-23T12:00:00Z"      # fixed so reruns are byte-identical
MIGRATION_DATE = "2026-10-23"
ASSESSED_AT = "2026-02-23"                 # date of the copyB workbook; original session dates were not recorded
REVIEW_BY_EMERGING = "2028-10-23"          # +24 months (vocab/lifecycle_states.yaml emerging)
V1_LICENSE = "LicenseRef-EMSTv1-PendingDedication"
LEVELS = [("foundational", "L1"), ("intermediate", "L2"), ("advanced", "L3"), ("expert", "L4")]
SECTORS = ["public_agencies", "private_sector", "ngos", "consulting", "academia"]
SOURCE_TEXT = L.ROOT / "legacy" / "v1" / "docs" / "20251202_SkillsTaxonomy_Core_V2 (1).txt"
D7_RECORD = L.ROOT / "legacy" / "v1" / "docs" / "domain7_task14_tagging_record.txt"
TASK10_RECORD = L.ROOT / "legacy" / "v1" / "docs" / "taxonomy_task10_working_record.md"
CAND_RE = re.compile(r"^(DC-CAND-\d{2}|IA-CC-\d{2}|LC-C-\d{2}|CC-CM-\d{2}|C-LM-\d{2}|[A-Z]{2}-C\d{2})\b")
REL_LIVE = ("carried", "rewritten", "split-from", "merged-from", "recovered")
HELD_FLAGS = {"indigenousDataFlag": True, "approvalStatus": "pending-tribal-review", "aiUsePermitted": False}
# XR-05 (vocab/exposure_instrument_v2.yaml): tasks handling confidential Tribal information or Indigenous knowledge
XR05_TASKS = {"v1:6.5.1:T3", "v1:5.3.2:T3", "v1:5.3.3:T2"}
EXPOSURE_FLAG_SOURCES = {"d6": "reconciled_d6_2026_03", "pre15a": "pre15a_hybrid", "d7_record": "normative_h"}


def _tribal_triggers():
    gov = L.load_yaml(L.LINT_DIR / "governed_content.yaml")
    out = []
    for p in gov["tribal_hold"]["triggers"]:
        out.append(re.compile(p["pattern"]) if isinstance(p, dict) and p.get("cs") else re.compile(p["pattern"] if isinstance(p, dict) else p, re.I))
    return out


TRIBAL_TRIGGERS = _tribal_triggers()


def tribal_text(*texts) -> bool:
    """Conservative hold trigger (ADR-0007 §D: default is withhold; TN may release on review)."""
    return any(rx.search(t or "") for t in texts for rx in TRIBAL_TRIGGERS)


def slug(s: str) -> str:
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s[:48].strip("-")


# ---------------------------------------------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------------------------------------------


class Inputs:
    def __init__(self, root: Path = L.ROOT):
        b = root / "data" / "v1_baseline"
        self.base = b
        R = L.read_csv
        self.comps = {r["code"]: r for r in R(b / "competencies.csv")}
        self.tasks = R(b / "tasks.csv")
        self.prof = {r["key"]: r for r in R(b / "proficiency.csv")}
        self.inds = R(b / "indicators.csv")
        self.csr = {r["code"]: r for r in R(b / "craft_stage_reform.csv")}
        self.fams = R(b / "family_assignments.csv")
        self.lenses = R(b / "ethical_lenses.csv")
        self.expsum = {r["code"]: r for r in R(b / "exposure_summary.csv")}
        self.expsrc = R(b / "exposure_sources.csv")
        self.sectors = R(b / "sector_applications.csv")
        st = b / "source_text"
        self.st_comp = {r["code"]: r for r in R(st / "competencies.csv")}
        self.st_prof = {r["key"]: r for r in R(st / "proficiency.csv")}
        self.st_inds = R(st / "indicators.csv")
        self.st_tasks = {r["key"]: r for r in R(st / "tasks.csv")}
        info = json.loads((b / "BUILD_INFO.json").read_text(encoding="utf-8"))
        self.copyb = next(i["sha256"] for i in info["inputs"] if i["role"] == "baseline")
        self.disp = {r["v1_code"]: r for r in R(L.DISPOSITION)}
        self.cands = {r["cand_id"]: r for r in R(L.CANDIDATES)}
        self.source_lines = SOURCE_TEXT.read_text(encoding="utf-8").splitlines() if SOURCE_TEXT.exists() else []

    def code_key(self, code):
        return f"v1:{code}"


def sort_code(code: str):
    return tuple(int(x) if x.isdigit() else x for x in re.split(r"[.-]", code))


# ---------------------------------------------------------------------------------------------------------------
# Disposition targets
# ---------------------------------------------------------------------------------------------------------------


def module_ns(text: str) -> str | None:
    m = re.search(r"\bMOD-\d{2}[ab]?\s+([a-z]+)", text)
    return m.group(1) if m else None


def cand_area(cid: str, cands: dict) -> tuple[str, str]:
    """(area, decision) of a candidate; follows merge-into chains."""
    seen = set()
    while cid in cands and cid not in seen:
        seen.add(cid)
        c = cands[cid]
        if c["decision"] == "merge-into":
            nxt = c["target"].split("|")[0].strip()
            if nxt.startswith("v1:"):
                return "v1:" + nxt[3:], "merge-into"
            cid = nxt
            continue
        t = c["target"]
        if c["decision"] == "module-v2.0":
            return (module_ns(t) or "core"), c["decision"]
        return "core", c["decision"]
    return "core", "unknown"


def parse_targets(inp: Inputs, code: str) -> list[dict]:
    d = inp.disp[code]
    dec, raw = d["decision"], d["target"].strip()
    out = []
    if dec in ("carry", "rewrite", "move-to-module"):
        return [{"raw": raw, "key": f"seed:v1-{code}", "kind": "v1-seed", "area": None}]
    if dec == "retire":
        return [{"raw": raw, "key": "sssom:NoTermFound", "kind": "retire", "area": None}]
    letters = iter("ABCDEFGH")
    for item in [x.strip() for x in raw.split("|") if x.strip()]:
        t = {"raw": item}
        m = re.match(r"^v1:(\d\.\d{1,2}\.\d{1,2})(-([A-Z]))?\b", item)
        cm = CAND_RE.match(item)
        if m and m.group(3):
            t.update(key=f"seed:v1-{m.group(1)}-{m.group(3)}", kind="split-new", area="core")
        elif m:
            t.update(key=f"seed:v1-{m.group(1)}", kind="v1-seed", area=None)
        elif cm and cm.group(1) in inp.cands:
            cid = cm.group(1)
            area, cdec = cand_area(cid, inp.cands)
            t.update(key=f"seed:{cid}", kind="candidate", area=area, candidate_decision=cdec)
        elif item.startswith("L4 "):
            t.update(key=f"seed:tool-{slug(item[3:])}", kind="tool", area="tools")
        elif item.lower().startswith("credential:"):
            t.update(key=f"seed:crd-{slug(item.split(':', 1)[1])}", kind="credential", area="registers")
        elif item.startswith("SC enactment of") or " enactment of " in item:
            t.update(key=f"seed:v1-{code}-{next(letters)}", kind="enactment", area="core")
        elif re.match(r"^MOD-\d{2}[ab]?\s+[a-z]+:", item):
            t.update(key=f"seed:v1-{code}-{next(letters)}", kind="split-new", area=module_ns(item))
        else:   # "core practice: …", "TX-C safety culture (transversal)", other free text
            t.update(key=f"seed:v1-{code}-{next(letters)}", kind="split-new", area="core")
        out.append(t)
    return out


def resolve_v1_target(inp: Inputs, code: str, depth=0) -> str:
    """Follow v1 merge chains (a merge into a v1 code that itself merges) to the surviving key."""
    d = inp.disp.get(code)
    if d and d["decision"] == "merge" and depth < 5:
        t = d["target"].strip()
        if t.startswith("v1:") and not re.match(r"^v1:\d\.\d+\.\d+-[A-Z]", t):
            return resolve_v1_target(inp, t[3:].split()[0], depth + 1)
        cm = CAND_RE.match(t)
        if cm:
            return f"seed:{cm.group(1)}"
    return f"seed:v1-{code}"


class Plan:
    """Per-competency migration plan derived from the dispositions."""

    def __init__(self, inp: Inputs):
        self.inp = inp
        self.targets = {c: parse_targets(inp, c) for c in inp.disp}
        self.area = {}
        for code, d in inp.disp.items():
            self.area[code] = (module_ns(d["target"]) or "core") if d["decision"] == "move-to-module" else "core"
        # fill v1-seed target areas and candidate chains that end in v1 codes
        for code, ts in self.targets.items():
            for t in ts:
                if t["kind"] == "v1-seed":
                    tc = t["key"][len("seed:v1-"):]
                    t["key"] = resolve_v1_target(inp, tc) if t["key"] != f"seed:v1-{code}" else t["key"]
                    tc2 = t["key"][len("seed:v1-"):] if t["key"].startswith("seed:v1-") else None
                    t["area"] = self.area.get(tc2, "core") if tc2 else "core"
                elif t["kind"] == "candidate" and t["area"].startswith("v1:"):
                    t["key"] = f"seed:v1-{t['area'][3:]}"
                    t["kind"] = "v1-seed"
                    t["area"] = self.area.get(t["area"][3:], "core")
        self.held = {c for c, d in inp.disp.items() if d["decision"] == "hold-for-tribal-review"}
        self.held_tasks: set[str] = set()     # filled while task seeds are built

    def decision(self, code):
        return self.inp.disp[code]["decision"]

    def status(self, code):
        dec = self.decision(code)
        if dec in ("carry", "rewrite", "move-to-module"):
            return "draft"
        if dec == "retire":
            return "withdrawn"
        return "superseded"

    def replaced_by(self, code):
        if self.status(code) != "superseded":
            return None
        ts = self.targets[code]
        keys = [t["key"] for t in ts if t["kind"] != "tool"] + [t["key"] for t in ts if t["kind"] == "tool"]
        return list(dict.fromkeys(keys))

    def task_target(self, code):
        """(supports key, area) for the tasks of v1 competency `code`."""
        dec = self.decision(code)
        if dec == "merge":
            t = self.targets[code][0]
            return t["key"], (t["area"] if t["area"] not in (None, "tools", "registers") else "core")
        return f"seed:v1-{code}", self.area[code]


# ---------------------------------------------------------------------------------------------------------------
# Record builders
# ---------------------------------------------------------------------------------------------------------------


def lang(s):
    return {"en": L.normalize_text(s)}


def held_fields(rec):
    rec.update(HELD_FLAGS)
    rec["sensitivity"] = "restricted-governed"


def competency_type_from(target: str):
    t = target.lower()
    if "knowledge-area" in t or "knowledge area" in t:
        return "knowledge-area"
    if "transversal" in t:
        return "transversal"
    if "practice" in t:
        return "practice"
    return None


def build_competency(inp: Inputs, plan: Plan, code: str) -> tuple[Path, dict]:
    c = inp.comps[code]
    d = inp.disp[code]
    dec = d["decision"]
    st = inp.st_comp.get(code)
    split = bool(c["suggested_title"])
    title = c["suggested_title"] if split else c["title"]
    desc = c["suggested_description"] if split else c["description"]
    rid = f"seed:v1-{code}"
    area = plan.area[code]
    rec = {"id": rid, "type": "Competency", "prefLabel": lang(title), "statement": lang(desc)}
    if dec in ("carry", "rewrite", "move-to-module"):
        ctype = competency_type_from(d["target"])
        if ctype:
            rec["competencyType"] = ctype
        m = re.search(r"\bTX-[A-F]\b", d["target"])
        if ctype == "transversal" and m:
            rec["transversalCluster"] = m.group(0)
    rec["notation"] = [{"scheme": "EMSTv1", "value": code}]
    rec["layer"] = "L1"
    rec["module"] = area
    rec["homeModule"] = area
    rec["status"] = plan.status(code)
    rb = plan.replaced_by(code)
    if rb:
        rec["replacedBy"] = rb
    if "lifecycle emerging" in d["target"]:
        rec["lifecycleState"] = "emerging"
        rec["reviewBy"] = REVIEW_BY_EMERGING
    rec["useTier"] = "exploratory"
    rec["validationStatus"] = "seed-v1"
    rec["v1Domain"] = {"code": c["domain_num"], "label": c["domain_name"]}
    rec["v1SkillArea"] = {"code": c["skill_area_code"], "label": c["skill_area_name"].title() if c["skill_area_name"].isupper() else c["skill_area_name"]}
    note = (f"v1 disposition (ADR-0011; docs/decisions/v1_disposition.csv): {dec} → {d['target']}. "
            f"Rationale: {d['rationale']} Role verdicts considered: {d['role_verdicts_considered']}.")
    if split:
        note += " Title and description were merged in the v1 database and are split here from the source text."
    rec["editorialNote"] = {"en": L.normalize_text(note)}
    rec["license"] = V1_LICENSE
    rec["sensitivity"] = "public"
    if code in plan.held:
        held_fields(rec)
    dfrom = [{"v1Key": f"v1:{code}", "v1Code": code, "v1Table": "competencies", "v1Sheet": c["source_sheet"],
              "v1Row": int(c["source_row"]), "v1Fields": ["title", "description"], "workbookSha256": inp.copyb,
              "relation": "carried"}]
    if st:
        dfrom.append({"v1Key": f"v1:{code}", "v1Code": code, "v1Table": "source_text/competencies",
                      "sourceTextLine": int(st["source_line"]), "relation": "recovered",
                      "note": "v1Seed levels and indicators taken from the source competency text (ADR-0011 rule 2)"
                              + ("; title/description split" if split else "")})
    # merged-from / split-from lineage onto v1-seed targets is added by add_lineage()
    rec["provenance"] = {"method": "v1-migration", "agent": [AGENT], "generatedAt": MIGRATION_TS, "derivedFrom": dfrom,
                         "evidenceLabel": "J", "reviewStatus": "unreviewed", "adr": ["ADR-0011", "ADR-0010"]}
    rec["v1Seed"] = build_v1_seed(inp, code, c, split)
    base = L.DATA_V2 / ("core" if area == "core" else f"modules/{area}")
    return base / "competencies" / f"{L.id_to_stem(rid)}.yaml", rec


def build_v1_seed(inp: Inputs, code: str, c: dict, split: bool) -> dict:
    seed = {"v1Title": c["title"], "v1Description": c["description"]}
    if split:
        seed["titleDescriptionSplit"] = True
    levels = []
    st_inds = defaultdict(list)
    for r in inp.st_inds:
        if r["code"] == code:
            st_inds[r["level"]].append(r)
    db_inds = defaultdict(list)
    for r in inp.inds:
        if r["code"] == code and not r["qa_flag"]:
            db_inds[r["level"]].append(r)
    for v1lvl, v2lvl in LEVELS:
        key = f"v1:{code}:{v1lvl}"
        p = inp.prof.get(key, {})
        sp = inp.st_prof.get(key)
        lv = {"v1Level": v1lvl, "mapsTo": v2lvl, "v1Key": key}
        if sp:
            k, a = sp["source_knowledge"], sp["source_application"]
            restored = not (p.get("knowledge") or p.get("application"))
        else:
            k, a, restored = p.get("knowledge", ""), p.get("application", ""), False
        if k:
            lv["knowledge"] = L.normalize_text(k)
        if a:
            lv["application"] = L.normalize_text(a)
        if k or a:
            lv["knowledgeApplicationOrigin"] = "restored-from-source-text" if restored else "database"
        items = []
        if st_inds.get(v1lvl):
            for r in sorted(st_inds[v1lvl], key=lambda r: int(r["indicator_n"])):
                items.append({"v1Key": r["key"], "n": int(r["indicator_n"]), "text": L.normalize_text(r["text"]),
                              "origin": "database" if r["in_db_any_position"] == "true" else "restored-from-source-text"})
        else:
            for r in sorted(db_inds.get(v1lvl, []), key=lambda r: int(r["indicator_n"])):
                items.append({"v1Key": r["key"], "n": int(r["indicator_n"]), "text": L.normalize_text(r["text"]),
                              "origin": "database"})
        if items:
            lv["indicators"] = items
        levels.append(lv)
    seed["levels"] = levels
    secs = {r["sector"]: r for r in inp.sectors if r["code"] == code}
    seed["sectorApplications"] = [{"sector": s, "v1Key": secs[s]["key"], "text": L.normalize_text(secs[s]["text"])}
                                  for s in SECTORS if s in secs and secs[s]["text"]]
    seed["note"] = ("Reference-only v1 material (ADR-0011): v1 levels map to L1–L4 as four-level drafts (SPEC §8.3); "
                    "indicators are draft seeds to rewrite to IO's rules, never v2 indicators. Stripped from releases.")
    return seed


def build_task(inp: Inputs, plan: Plan, t: dict) -> tuple[Path, dict]:
    code, n = t["code"], int(t["task_n"])
    rid = f"seed:v1-{code}-T{n}"
    c = inp.comps[code]
    dec = plan.decision(code)
    sup, area = plan.task_target(code)
    text = L.normalize_text(t["text"])
    rec = {"id": rid, "type": "Task", "prefLabel": {"en": text}, "statement": {"en": text},
           "textSha256": L.text_sha256(text), "supports": [{"competency": sup, "strength": "primary"}],
           "notation": [{"scheme": "EMSTv1", "value": f"{code}:T{n}"}], "layer": "L2", "module": area,
           "homeModule": area, "status": "withdrawn" if dec == "retire" else "draft", "useTier": "exploratory",
           "validationStatus": "seed-v1", "v1Tier": f"T{n}",
           "v1Domain": {"code": c["domain_num"], "label": c["domain_name"]},
           "v1SkillArea": {"code": c["skill_area_code"], "label": c["skill_area_name"].title() if c["skill_area_name"].isupper() else c["skill_area_name"]}}
    notes = []
    if dec == "merge":
        notes.append(f"Supports re-pointed from v1 competency {code} to {sup} by the merge disposition (ADR-0011).")
    elif dec in ("split", "move-to-tools"):
        notes.append(f"v1 competency {code} is {dec}: reassign this task to one of {plan.replaced_by(code)} or retire it as tool fluency.")
    elif dec == "retire":
        notes.append(f"v1 competency {code} is retired without successor; this task is withdrawn with it.")
    elif dec == "hold-for-tribal-review":
        notes.append("Held under ADR-0007 §D with its competency.")
    notes.append("v1 task order (T1 foundational … T3 advanced) is kept as v1Tier for provenance only (ADR-0003 G-2).")
    rec["editorialNote"] = {"en": " ".join(notes)}
    rec["license"] = V1_LICENSE
    rec["sensitivity"] = "public"
    key = f"v1:{code}:T{n}"
    if code in plan.held or key in XR05_TASKS or tribal_text(text):
        held_fields(rec)
        plan.held_tasks.add(key)
    if key in XR05_TASKS:
        rec["governedData"] = "tribal"
    rec["provenance"] = {"method": "v1-migration", "agent": [AGENT], "generatedAt": MIGRATION_TS,
                         "derivedFrom": [{"v1Key": key, "v1Code": code, "v1Table": "tasks", "v1Sheet": "Competencies",
                                          "v1Row": int(t["source_row_text"]), "v1Fields": ["Job Tasks"],
                                          "workbookSha256": inp.copyb, "relation": "carried"}],
                         "evidenceLabel": "J", "reviewStatus": "unreviewed", "adr": ["ADR-0011"]}
    base = L.DATA_V2 / ("core" if area == "core" else f"modules/{area}")
    return base / "tasks" / f"{L.id_to_stem(rid)}.yaml", rec


def add_lineage(plan: Plan, comp_recs: dict[str, dict]):
    """Put merged-from / split-from / move-to-tools lineage onto the v1-seed records that absorb other v1 items."""
    for code in sorted(plan.targets, key=sort_code):
        dec = plan.decision(code)
        rel = {"merge": "merged-from", "split": "split-from", "move-to-tools": "merged-from"}.get(dec)
        if not rel:
            continue
        for t in plan.targets[code]:
            if t["kind"] != "v1-seed":
                continue
            tc = t["key"][len("seed:v1-"):]
            target = comp_recs.get(tc)
            if target is None:
                continue
            target["provenance"]["derivedFrom"].append(
                {"v1Key": f"v1:{code}", "v1Code": code, "relation": rel,
                 "note": f"v1 {code} ({dec}) → {t['key']} per v1_disposition.csv"})


# ---------------------------------------------------------------------------------------------------------------
# v1 tags as prior evidence (ADR-0008 §5; ADR-0011 rule 4)
# ---------------------------------------------------------------------------------------------------------------

MODE_MAP = {"A": ("assisted", False), "Ac": ("compressive", False), "H": ("human-executes", False),
            "V": ("compressive", True), "S": ("compressive", True)}
TACIT_MAP = {"Hi": "Hi", "Med": "Med", "Lo": "Lo"}


def _rating_base(rid, typ, label, held):
    rec = {"id": rid, "type": typ, "prefLabel": {"en": label}, "layer": "L5", "module": "core", "status": "draft",
           "license": V1_LICENSE, "sensitivity": "public"}
    if held:
        held_fields(rec)
    return rec


def _rater(method, instrument, codebook):
    return {"raterType": "v1-analyst", "raterId": "v1-analyst-01", "assessedAt": ASSESSED_AT, "method": method,
            "confidence": "low", "instrument": instrument, "codebookVersion": codebook, "evidenceLabel": "J", "sources": []}


def _prov(derived):
    return {"method": "v1-migration", "agent": [AGENT], "generatedAt": MIGRATION_TS, "derivedFrom": derived,
            "evidenceLabel": "J", "confidence": "low", "reviewStatus": "unreviewed", "adr": ["ADR-0008", "ADR-0011"]}


def exposure_records(inp: Inputs, plan: Plan):
    db, wr = [], []
    src_by_task = defaultdict(list)
    for r in inp.expsrc:
        src_by_task[r["task_key"]].append(r)
    for t in inp.tasks:
        code, n, key = t["code"], int(t["task_n"]), t["key"]
        dom = code.split(".")[0]
        held = key in plan.held_tasks
        flags = []
        recs = src_by_task.get(key, [])
        if dom in ("1", "3") and any(float(r["task_text_similarity"] or 1) < 0.8 for r in recs if r["source"] in ("d1_record", "d3_record")):
            flags.append("text_misaligned")
        if t["exposure_provenance"] == "reconstructed_d2":
            flags.append("reconstructed_d2")
            if any(r["source"] == "d2_record" and r["matches_baseline"] == "false" for r in recs):
                flags.append("d2_divergent")
        if t["exposure_provenance"] == "d6_exposure_file_reconciled_2026_03":
            flags.append("reconciled_d6_2026_03")
        if t["exposure_provenance"] == "pre_task_15a_d6_ac_retrospective":
            flags.append("pre15a_hybrid")
        if dom == "7" and t["auto_type"] == "H":
            flags.append("normative_h")
        rid = f"seed:v1asm/{code}-T{n}/copyB"
        rec = _rating_base(rid, "ExposureAssessment", f"v1 exposure codes for {key} (copyB database)", held)
        rec.update({"task": f"seed:v1-{code}-T{n}", "taskTextSha256": L.text_sha256(t["text"])})
        rec.update(_rater("v1 database copyB, per-task Task 12/13 dimensions", "emst-v1-task13", "v1 (Task 12/13 instrument)"))
        rec["v1Flags"] = flags
        rec["v1Values"] = {"auto_type": t["auto_type"], "tacit_density": t["tacit_density"],
                           "career_ladder": t["career_ladder"], "vector": t["vector"], "horizon": t["horizon"],
                           "exposure_provenance": t["exposure_provenance"]}
        _map_v2(rec, t["auto_type"], t["tacit_density"])
        rec["provenance"] = _prov([{"v1Key": key, "v1Code": code, "v1Table": "tasks", "v1Sheet": "Dimension Tags",
                                    "v1Row": int(t["source_row_exposure"]), "v1Fields": ["auto_type", "tacit_density", "career_ladder", "vector", "horizon"],
                                    "workbookSha256": inp.copyb, "v1ProvenanceCode": t["exposure_provenance"], "relation": "prior-evidence"}])
        db.append(rec)
    for r in sorted(inp.expsrc, key=lambda r: (sort_code(r["task_key"][3:].split(":")[0]), r["task_key"], r["key"])):
        key = r["task_key"]
        code, tn = key[3:].split(":")
        held = key in plan.held_tasks or tribal_text(r["rationale"], r["source_task_text"])
        flags = []
        sim = float(r["task_text_similarity"] or 1)
        if sim < 0.8:
            flags.append("text_misaligned")
        if r["source"] == "d2_record" and r["matches_baseline"] == "false":
            flags.append("d2_divergent")
        if r["source"] in EXPOSURE_FLAG_SOURCES and not (r["source"] == "d7_record" and r["auto_type"] != "H"):
            flags.append(EXPOSURE_FLAG_SOURCES[r["source"]])
        suffix = r["key"].split("#", 1)[1] if "#" in r["key"] else ""
        rid = f"seed:v1asm/{code}-{tn}/{r['source']}" + (f"-{suffix}" if suffix else "")
        rec = _rating_base(rid, "ExposureAssessment", f"v1 exposure codes for {key} ({r['source']})", held)
        rec.update({"task": f"seed:v1-{code}-{tn}", "taskTextSha256": L.text_sha256(r["source_task_text"])})
        rec.update(_rater(f"v1 working record {r['source_file']}", "emst-v1-task13", "v1 (Task 12/13 instrument)"))
        if r["rationale"]:
            rec["rationale"] = {"en": L.normalize_text(r["rationale"])}
        rec["v1Flags"] = sorted(set(flags), key=flags.index)
        vals = {k: r[k] for k in ("auto_type", "tacit_density", "career_ladder", "vector", "horizon", "prev_auto_type",
                                  "cld_flag", "cld_severity", "delphi_flag", "confidence", "source_inferred",
                                  "matches_baseline", "task_text_similarity") if r.get(k) not in (None, "")}
        vals["source_task_text"] = L.normalize_text(r["source_task_text"])
        rec["v1Values"] = vals
        _map_v2(rec, r["auto_type"], r["tacit_density"])
        d = {"v1Key": r["key"], "v1Code": code, "v1Table": "exposure_sources", "v1ProvenanceCode": r["source"],
             "relation": "prior-evidence", "note": r["source_file"]}
        if r["source_row"].isdigit():
            d["v1Row" if r["source_file"].endswith(".xlsx") else "sourceTextLine"] = int(r["source_row"])
        rec["provenance"] = _prov([d])
        wr.append(rec)
    return db, wr


def _map_v2(rec, auto, tacit):
    mode, swatch = MODE_MAP.get(auto, (None, False))
    if mode:
        rec["deploymentMode"] = mode
        if swatch:
            rec["sWatch"] = True
        rec["mappingRule"] = "vocab/exposure_instrument_v2.yaml#v1_migration_mapping (XR-04 for V and S)"
    if tacit in TACIT_MAP:
        rec["tacitExperienceRequirement"] = TACIT_MAP[tacit]


def _comp_hash(inp, code):
    c = inp.comps[code]
    split = bool(c["suggested_title"])
    return L.competency_text_sha256(c["suggested_title"] if split else c["title"], c["suggested_description"] if split else c["description"])


def tag_records(inp: Inputs, plan: Plan):
    out = defaultdict(list)
    dual = _dual_primary()
    lens_rec = _d7_lenses()
    for code in sorted(inp.comps, key=sort_code):
        c, k = inp.csr[code], f"v1:{code}"
        held = code in plan.held
        row = int(c["source_row"])
        h = _comp_hash(inp, code)
        # craft primary/secondary
        rec = _rating_base(f"seed:v1craft/{code}", "CraftRating", f"v1 craft tags for {k}", held)
        rec.update({"competency": f"seed:v1-{code}", "competencyTextSha256": h})
        rec.update(_rater("v1 Dimension Tags craft primary/secondary (irreducibility test)", "emst-v1-craft", "v1 craft_assignment_criteria.md"))
        rec["v1Flags"] = []
        rec["v1Values"] = {"craft_primary": c["craft_primary"], "craft_secondary": c["craft_secondary"] or None}
        rec["provenance"] = _prov([{"v1Key": k, "v1Code": code, "v1Table": "craft_stage_reform", "v1Sheet": "Dimension Tags",
                                    "v1Row": row, "v1Fields": ["craft_primary", "craft_secondary"], "workbookSha256": inp.copyb,
                                    "relation": "prior-evidence"}])
        out["emst-v1-craft"].append(rec)
        # workflow stages (+ recovered dual-primary second stage)
        rec = _rating_base(f"seed:v1stage/{code}", "FunctionRating", f"v1 workflow-stage tags for {k}", held)
        rec.update({"competency": f"seed:v1-{code}", "competencyTextSha256": h})
        rec.update(_rater("v1 Dimension Tags workflow stage S1–S6", "emst-v1-workflow-stage", "v1 workflow_stage_definitions.md"))
        rec["v1Flags"] = []
        vals = {"stage_primary_1": c["stage_primary_1"] or None, "stage_primary_2": c["stage_primary_2"] or None,
                "stage_secondary_1": c["stage_secondary_1"] or None, "dual_primary_exception": c["dual_primary_exception"] == "true"}
        derived = [{"v1Key": k, "v1Code": code, "v1Table": "craft_stage_reform", "v1Sheet": "Dimension Tags", "v1Row": row,
                    "v1Fields": ["stage_primary_1", "stage_primary_2", "stage_secondary_1", "dual_primary_exception"],
                    "workbookSha256": inp.copyb, "relation": "prior-evidence"}]
        if code in dual:
            stages, line = dual[code]
            vals["stage_primary_2"] = stages[1]
            vals["dual_primary_exception"] = True
            vals["recovered_from"] = "taxonomy_task10_working_record.md, Dual-Primary Exception Register"
            derived.append({"v1Key": k, "v1Code": code, "relation": "recovered", "sourceTextLine": line,
                            "note": "legacy/v1/docs/taxonomy_task10_working_record.md (P-DE-12)"})
        rec["v1Values"] = vals
        rec["provenance"] = _prov(derived)
        out["emst-v1-workflow-stage"].append(rec)
        # reform flags (the count and the stability tier are stored summaries: not migrated, ADR-0011 rule 5)
        rec = _rating_base(f"seed:v1reform/{code}", "RelevanceRating", f"v1 reform-sensitivity flags for {k}", held)
        rec.update({"subject": f"seed:v1-{code}", "subjectTextSha256": h, "object": "EMSTv1:reform-flags", "objectScheme": "v1-reform-flags"})
        rec.update(_rater("v1 Dimension Tags reform flags", "emst-v1-reform", "v1 (six reform flags)"))
        rec["v1Flags"] = []
        names = ["reform_nepa_timeline", "reform_digital_permitting", "reform_catex_scope", "reform_consultation",
                 "reform_one_federal_decision", "reform_s2_s3_boundary"]
        rec["v1Values"] = {n_: c[n_] == "true" for n_ in names}
        rec["provenance"] = _prov([{"v1Key": k, "v1Code": code, "v1Table": "craft_stage_reform", "v1Sheet": "Dimension Tags",
                                    "v1Row": row, "v1Fields": names, "workbookSha256": inp.copyb, "relation": "prior-evidence"}])
        out["emst-v1-reform"].append(rec)
        # CLD flag, severity (R9 overlay prior) and S-trajectory
        e = inp.expsum[code]
        rec = _rating_base(f"seed:v1cld/{code}", "RelevanceRating", f"v1 career-ladder (CLD) tags for {k}", held)
        rec.update({"subject": f"seed:v1-{code}", "subjectTextSha256": h, "object": "EMSTv1:cld", "objectScheme": "v1-cld"})
        rec.update(_rater("v1 Dimension Tags CLD flag, R9 severity and S-trajectory", "emst-v1-cld", "v1 (Task 13 CLD rubric R9)"))
        rec["v1Flags"] = []
        rec["v1Values"] = {"cld_flag": e["cld_flag"] == "true", "cld_severity": e["cld_severity"] or None,
                           "s_trajectory_flag": e["s_trajectory_flag"] == "true"}
        rec["provenance"] = _prov([{"v1Key": k, "v1Code": code, "v1Table": "exposure_summary", "v1Sheet": "Dimension Tags",
                                    "v1Row": int(e["source_row"]), "v1Fields": ["cld_flag", "cld_severity", "s_trajectory_flag"],
                                    "workbookSha256": inp.copyb, "relation": "prior-evidence"}])
        out["emst-v1-cld"].append(rec)
    for f in sorted(inp.fams, key=lambda r: (sort_code(r["code"]), int(r["family_code"][1:]))):
        code = f["code"]
        rec = _rating_base(f"seed:v1fam/{code}/{f['family_code']}", "RelevanceRating",
                           f"v1 profession-family relevance of v1:{code} to {f['family_code']}", code in plan.held)
        rec.update({"subject": f"seed:v1-{code}", "subjectTextSha256": _comp_hash(inp, code),
                    "object": f"EMSTv1:family/{f['family_code']}", "objectScheme": "v1-family"})
        rec.update(_rater("v1 Profession Family View (Core/Supporting)", "emst-v1-family", "v1 profession_family_definitions.md"))
        rec["v1Flags"] = []
        rec["v1Values"] = {"family_code": f["family_code"], "family_name": f["family_name"], "assignment": f["assignment"]}
        rec["provenance"] = _prov([{"v1Key": f["key"], "v1Code": code, "v1Table": "family_assignments", "v1Sheet": "Dimension Tags",
                                    "v1Row": int(f["source_row"]), "workbookSha256": inp.copyb, "relation": "prior-evidence"}])
        out["emst-v1-family"].append(rec)
    lens_rows = [(r["code"], r["lens_code"], r["lens_name"], r["value"], {"v1Key": r["key"], "v1Code": r["code"], "v1Table": "ethical_lenses",
                  "v1Sheet": "Dimension Tags", "v1Row": int(r["source_row"]), "workbookSha256": inp.copyb, "relation": "prior-evidence"})
                 for r in inp.lenses]
    names = {r["lens_code"]: r["lens_name"] for r in inp.lenses}
    for code, lvals, line in lens_rec:
        for i, v in enumerate(lvals, 1):
            lc = f"L{i}"
            lens_rows.append((code, lc, names.get(lc, lc), v, {"v1Key": f"v1:{code}:{lc}", "v1Code": code, "relation": "recovered",
                              "sourceTextLine": line, "note": "legacy/v1/docs/domain7_task14_tagging_record.txt Ethical Lens Summary (P-DE-12)"}))
    for code, lc, lname, v, d in sorted(lens_rows, key=lambda x: (sort_code(x[0]), x[1])):
        held = code in plan.held or lc == "L2"
        rec = _rating_base(f"seed:v1lens/{code}/{lc}", "RelevanceRating", f"v1 ethical-lens value of v1:{code} for {lc}", held)
        rec.update({"subject": f"seed:v1-{code}", "subjectTextSha256": _comp_hash(inp, code),
                    "object": f"EMSTv1:lens/{lc}", "objectScheme": "v1-ethical-lens"})
        rec.update(_rater("v1 ethical lens (E/I/A; R10 for 7.1)", "emst-v1-lens", "v1 ethical_lens_framework.md"))
        rec["v1Flags"] = []
        rec["v1Values"] = {"lens_code": lc, "lens_name": lname, "value": v}
        rec["provenance"] = _prov([d])
        out["emst-v1-lens"].append(rec)
    return out


def _dual_primary():
    """Dual-primary second stages from the Task 10 register (audit C13)."""
    out = {}
    if not TASK10_RECORD.exists():
        return out
    lines = TASK10_RECORD.read_text(encoding="utf-8").splitlines()
    start = next((i for i, ln in enumerate(lines) if "Dual-Primary Exception Register" in ln), None)
    if start is None:
        return out
    for i in range(start, min(start + 40, len(lines))):
        m = re.match(r"^\|\s*(\d\.\d+\.\d+)\s*\|[^|]*\|\s*(S\d)\+(S\d)\s*\|", lines[i])
        if m:
            out[m.group(1)] = ((m.group(2), m.group(3)), i + 1)
    return out


def _d7_lenses():
    """7.2.1–7.2.3 lens values from the D7 record's summary table (audit §1.4; CL-008)."""
    out = []
    if not D7_RECORD.exists():
        return out
    for i, ln in enumerate(D7_RECORD.read_text(encoding="utf-8").splitlines(), 1):
        m = re.match(r"^(7\.2\.\d)\s*\|\s*([EIA])\s*\|\s*([EIA])\s*\|\s*([EIA])\s*\|\s*([EIA])\s*\|\s*([EIA])\s*\|", ln)
        if m:
            out.append((m.group(1), [m.group(j) for j in range(2, 7)], i))
    return out


# ---------------------------------------------------------------------------------------------------------------
# X1 crosswalk (ADR-0022 X1; P-DE-08) and the target worklist
# ---------------------------------------------------------------------------------------------------------------

X1_COLUMNS = ["subject_id", "predicate_id", "object_id", "mapping_justification", "author_id", "mapping_date", "mapping_tool", "comment"]


def current_records(data_root: Path):
    recs = {}
    for loc, rec in L.iter_records(data_root):
        if isinstance(rec, dict) and isinstance(rec.get("id"), str):
            recs.setdefault(rec["id"], rec)
    return recs


def _actual(recs, v1key):
    out = []
    for rid, rec in recs.items():
        if rec.get("status") in ("superseded", "withdrawn") or rec.get("type") in L.RATING_TYPES:
            continue
        for d in (rec.get("provenance") or {}).get("derivedFrom") or []:
            if d.get("v1Key") == v1key and d.get("relation") in ("carried", "rewritten", "split-from", "merged-from"):
                out.append((rid, rec.get("type")))
                break
    return sorted(set(out))


def build_x1(inp: Inputs, plan: Plan, recs: dict) -> list[dict]:
    rows = []
    author = "emstagent:ca-v1-dispositions"
    for code in sorted(inp.disp, key=sort_code):
        d = inp.disp[code]
        dec = d["decision"]
        subj = f"EMSTv1:{code}"
        planned = plan.targets[code]
        actual = _actual(recs, f"v1:{code}")
        comment = f"decision={dec}; target={d['target']}; ADR-0011"
        objs: list[tuple[str, str]] = []
        if dec == "retire":
            objs = [("emst:retiredWithoutReplacement", "sssom:NoTermFound")]
        elif dec in ("carry", "rewrite", "move-to-module"):
            objs = [("emst:replacedBy", rid) for rid, _ in actual] or [("emst:replacedBy", planned[0]["key"])]
        else:
            keys = [rid for rid, _ in actual]
            types = dict(actual)
            if len(keys) < len(planned):
                keys += [t["key"] for t in planned if t["key"] not in recs and t["key"] not in keys]
            kinds = {t["key"]: t["kind"] for t in planned}
            pred = {"merge": "emst:mergedInto", "split": "emst:splitInto", "hold-for-tribal-review": "emst:replacedBy",
                    "move-to-tools": "emst:replacedBy"}[dec]
            for k in keys:
                p = "emst:movedToTools" if (kinds.get(k) == "tool" or types.get(k) == "Tool") else pred
                objs.append((p, k))
        for p, o in objs:
            rows.append({"subject_id": subj, "predicate_id": p, "object_id": o, "mapping_justification": "semapv:ManualMappingCuration",
                         "author_id": author, "mapping_date": MIGRATION_DATE, "mapping_tool": f"scripts/migrate_v1.py@{VERSION}",
                         "comment": comment})
        for n in (1, 2, 3):
            tkey = f"v1:{code}:T{n}"
            tsubj = f"EMSTv1:{code}:T{n}"
            tdec = "retire" if dec == "retire" else ("hold-for-tribal-review" if dec == "hold-for-tribal-review" else "carry")
            tcomment = f"decision={tdec}; parent=v1:{code} ({dec}); task text carried as seed (ADR-0011, ADR-0020)"
            if tdec == "retire":
                trows = [("emst:retiredWithoutReplacement", "sssom:NoTermFound")]
            else:
                act = [rid for rid, _ in _actual(recs, tkey)]
                if not act:
                    act = [f"seed:v1-{code}-T{n}"]
                trows = [("emst:splitInto" if len(act) > 1 else "emst:replacedBy", a) for a in act]
            for p, o in trows:
                rows.append({"subject_id": tsubj, "predicate_id": p, "object_id": o, "mapping_justification": "semapv:ManualMappingCuration",
                             "author_id": author, "mapping_date": MIGRATION_DATE, "mapping_tool": f"scripts/migrate_v1.py@{VERSION}",
                             "comment": tcomment})
    return rows


def x1_metadata(inp: Inputs) -> dict:
    return {
        "mapping_set_id": "https://w3id.org/emst/crosswalks/emst-v1/emst-v1_to_v2",
        "mapping_set_version": "0.1.0",
        "mapping_set_title": "EMST v1 to v2 (X1): every v1 competency and task with its recorded decision",
        "mapping_set_description": ("Generated by scripts/migrate_v1.py from docs/decisions/v1_disposition.csv and the "
                                    "current v2 records. Objects are seed: keys until IDs are minted. IDs only (ADR-0013)."),
        "license": "https://creativecommons.org/publicdomain/zero/1.0/",
        "subject_source": "https://w3id.org/emst/v1/",
        "subject_source_version": f"copyB sha256:{inp.copyb}",
        "object_source": "https://w3id.org/emst/",
        "object_source_version": "2.0.0-draft",
        "mapping_date": MIGRATION_DATE,
        "mapping_tool": f"scripts/migrate_v1.py@{VERSION}",
        "curie_map": {"EMSTv1": "https://w3id.org/emst/v1/", "emst": "https://w3id.org/emst/", "seed": "https://w3id.org/emst/seed/",
                      "sssom": "https://w3id.org/sssom/", "semapv": "https://w3id.org/semapv/vocab/",
                      "skos": "http://www.w3.org/2004/02/skos/core#", "emstagent": "https://w3id.org/emst/agent/"},
        "extension_definitions": [],
        "comment": "Decision vocabulary: ADR-0011 (carry, rewrite, split, merge, retire, move-to-tools, move-to-module, hold-for-tribal-review). "
                   "Held successors appear as keys only; build_release.py redacts them in release artifacts (ADR-0007 §D).",
    }


def x1_text(rows):
    return L.csv_text(X1_COLUMNS, rows, delimiter="\t")


TARGET_COLUMNS = ["v1_code", "decision", "position", "target_raw", "target_key", "target_kind", "area", "candidate_decision", "held"]


def targets_rows(inp: Inputs, plan: Plan, hold_keys: set[str]) -> list[dict]:
    rows = []
    for code in sorted(inp.disp, key=sort_code):
        for i, t in enumerate(plan.targets[code], 1):
            area = t["area"] if t["area"] is not None else plan.area.get(code, "core")
            rows.append({"v1_code": code, "decision": plan.decision(code), "position": i, "target_raw": t["raw"],
                         "target_key": t["key"] if t["kind"] != "retire" else "", "target_kind": t["kind"],
                         "area": area, "candidate_decision": t.get("candidate_decision", ""),
                         "held": "true" if (t["key"] in hold_keys or code in plan.held) else "false"})
    return rows


# ---------------------------------------------------------------------------------------------------------------
# Restoration sample (WP-02 acceptance: restored text reviewed on a 10% sample)
# ---------------------------------------------------------------------------------------------------------------

SAMPLE_COLUMNS = ["sample_key", "kind", "v1_domain", "restored_text", "db_text", "source_text_line", "verbatim_in_source",
                  "reviewer", "reviewed_on", "result", "note"]


def restoration_sample(inp: Inputs) -> list[dict]:
    norm_lines = [L.normalize_text(x) for x in inp.source_lines]

    def find(text):
        t = L.normalize_text(text)
        for i, ln in enumerate(norm_lines, 1):
            if t and t in ln:
                return i
        return None

    pop = defaultdict(list)
    for r in inp.st_inds:
        if r["in_db_any_position"] != "true":
            pop["indicator-truncated" if not r["code"].startswith("5.") else "indicator-d5"].append((r["key"], r["text"], r["db_text_same_position"]))
    for k, r in inp.st_prof.items():
        if r["code"].startswith("5.") and not inp.prof.get(k, {}).get("knowledge"):
            pop["d5-knowledge"].append((k + ":knowledge", r["source_knowledge"], ""))
            pop["d5-application"].append((k + ":application", r["source_application"], ""))
    for code, c in inp.comps.items():
        if c["suggested_title"]:
            pop["title-description-split"].append((f"v1:{code}", c["suggested_title"] + " || " + c["suggested_description"], c["title"]))
    rows = []
    for kind in sorted(pop):
        items = sorted(pop[kind], key=lambda x: hashlib.sha256(("emst-wp02-sample:" + x[0]).encode()).hexdigest())
        n = max(1, math.ceil(len(items) * 0.10))
        for key, text, db in sorted(items[:n], key=lambda x: x[0]):
            parts = text.split(" || ") if kind == "title-description-split" else [text]
            lines = [find(p) for p in parts]
            ok = all(x is not None for x in lines)
            rows.append({"sample_key": key, "kind": kind, "v1_domain": key[3], "restored_text": L.normalize_text(text),
                         "db_text": L.normalize_text(db), "source_text_line": "|".join(str(x) for x in lines if x),
                         "verbatim_in_source": "true" if ok else "false", "reviewer": REVIEW_AGENT,
                         "reviewed_on": MIGRATION_DATE, "result": "pass" if ok else "fail",
                         "note": f"population {len(items)}; sample {n}; agent verbatim check against legacy/v1/docs source text; "
                                 "human spot review pending (not validation)"})
    return rows


# ---------------------------------------------------------------------------------------------------------------
# Writing
# ---------------------------------------------------------------------------------------------------------------


def generate(inp: Inputs):
    plan = Plan(inp)
    comps, tasks = {}, {}
    for code in sorted(inp.comps, key=sort_code):
        path, rec = build_competency(inp, plan, code)
        comps[code] = (path, rec)
    add_lineage(plan, {c: r for c, (p, r) in comps.items()})
    for t in sorted(inp.tasks, key=lambda t: (sort_code(t["code"]), int(t["task_n"]))):
        path, rec = build_task(inp, plan, t)
        tasks[t["key"]] = (path, rec)
    db, wr = exposure_records(inp, plan)
    tags = tag_records(inp, plan)
    batches = {L.DATA_V2 / "assessments" / "emst-v1-task13" / "copyB.jsonl": db,
               L.DATA_V2 / "assessments" / "emst-v1-task13" / "working-records.jsonl": wr}
    for inst, recs in tags.items():
        batches[L.DATA_V2 / "assessments" / inst / "copyB.jsonl"] = recs
    return plan, comps, tasks, batches


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--x1-only", action="store_true")
    ap.add_argument("--force", action="store_true", help="overwrite seed files even if authors changed them")
    args = ap.parse_args(argv)
    inp = Inputs()
    plan, comps, tasks, batches = generate(inp)
    hold = L.load_yaml(L.GOVERNANCE / "tribal_hold.yaml") if (L.GOVERNANCE / "tribal_hold.yaml").exists() else {}
    hold_keys = set(hold.get("heldSeedKeys") or [])
    outputs: dict[Path, str] = {}
    skipped, drift = [], []
    existing = {}
    if not args.x1_only:
        for loc, rec in L.iter_records(L.DATA_V2):
            if isinstance(rec, dict) and isinstance(rec.get("id"), str) and loc.line is None:
                existing[rec["id"]] = (loc.path, rec)
        for path, rec in list(comps.values()) + list(tasks.values()):
            have = existing.get(rec["id"])
            if have is None or args.force:
                outputs[path] = L.dump_yaml(rec)
            elif have[0] != path or have[1].get("validationStatus") != "seed-v1":
                skipped.append(rec["id"])            # authored or moved: never overwritten
            elif L.dump_yaml(have[1]) != L.dump_yaml(rec):
                drift.append(str(path.relative_to(L.ROOT)))
                if not args.check:
                    outputs[path] = L.dump_yaml(rec)
            else:
                outputs[path] = L.dump_yaml(rec)
        for path, recs in batches.items():
            outputs[path] = "".join(L.jsonl_line(r) + "\n" for r in recs)
        outputs[L.DATA_V2 / "migration" / "restoration_sample.csv"] = L.csv_text(SAMPLE_COLUMNS, restoration_sample(inp))
    outputs[L.DATA_V2 / "migration" / "v1_targets.csv"] = L.csv_text(TARGET_COLUMNS, targets_rows(inp, plan, hold_keys))
    # X1 is computed against the records as they will be after this run
    recs = current_records(L.DATA_V2)
    for path, rec in list(comps.values()) + list(tasks.values()):
        have = recs.get(rec["id"])
        if have is None or (not args.x1_only and have.get("validationStatus") == "seed-v1"):
            recs[rec["id"]] = rec
    x1 = build_x1(inp, plan, recs)
    outputs[L.X1_TSV] = x1_text(x1)
    outputs[L.X1_YML] = L.dump_yaml(x1_metadata(inp))
    if not args.x1_only:
        info = {
            "script": f"scripts/migrate_v1.py {VERSION}",
            "generatedAt": MIGRATION_TS,
            "inputs": {str(p.relative_to(L.ROOT)): L.sha256_file(p) for p in sorted(
                [*(inp.base.glob("*.csv")), *(inp.base.glob("source_text/*.csv")), inp.base / "BUILD_INFO.json",
                 L.DISPOSITION, L.CANDIDATES, SOURCE_TEXT, D7_RECORD, TASK10_RECORD]) if p.exists()},
            "copyBWorkbookSha256": inp.copyb,
            "counts (generated)": {
                "competencySeeds": len(comps), "taskSeeds": len(tasks),
                "competencySeedsByDecision": dict(sorted(Counter(plan.decision(c) for c in comps).items())),
                "competencySeedsByStatus": dict(sorted(Counter(r["status"] for _, r in comps.values()).items())),
                "competencySeedsByArea": dict(sorted(Counter(r["module"] for _, r in comps.values()).items())),
                "heldCompetencySeeds": sum(1 for _, r in comps.values() if r.get("indigenousDataFlag")),
                "heldTaskSeeds": sum(1 for _, r in tasks.values() if r.get("indigenousDataFlag")),
                "priorEvidenceRecords": {str(p.relative_to(L.DATA_V2)): len(v) for p, v in sorted(batches.items())},
                "restoredIndicators": sum(1 for _, r in comps.values() for lv in r["v1Seed"]["levels"] for i in lv.get("indicators", []) if i["origin"] == "restored-from-source-text"),
                "restoredKnowledgeApplicationLevels": sum(1 for _, r in comps.values() for lv in r["v1Seed"]["levels"] if lv.get("knowledgeApplicationOrigin") == "restored-from-source-text"),
                "titleDescriptionSplits": sum(1 for _, r in comps.values() if r["v1Seed"].get("titleDescriptionSplit")),
                "x1Rows": len(x1), "x1RowsByPredicate": dict(sorted(Counter(r["predicate_id"] for r in x1).items())),
            },
            "notMigrated (stored summaries, ADR-0011 rule 5)": ["modal_* fields", "reform_flag_count", "stability_tier", "zero_core",
                                                                 "foundational_professional_prep", "core_family_count", "supporting_family_count"],
        }
        outputs[L.DATA_V2 / "migration" / "MIGRATION_INFO.json"] = L.dump_json(info)
    if args.check:
        bad = [str(p.relative_to(L.ROOT)) for p, txt in outputs.items() if not p.exists() or p.read_text(encoding="utf-8") != txt]
        bad += drift
        for b in bad[:40]:
            print("DIFFERS", b)
        print(f"{'FAIL' if bad else 'OK'}: {len(bad)} generated files differ; {len(skipped)} authored seeds left untouched")
        return 1 if bad else 0
    for p, txt in outputs.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists() or p.read_text(encoding="utf-8") != txt:
            p.write_text(txt, encoding="utf-8")
    print(f"wrote {len(outputs)} files; {len(skipped)} authored seeds left untouched; {len(drift)} untouched seeds refreshed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
