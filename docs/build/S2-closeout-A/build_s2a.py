#!/usr/bin/env python3
"""S2 close-out A authoring aid: writes the core competencies of builder A's work orders.

Rows (docs/decisions/integration/s2_work_orders.csv): FH-C13, FH-C14, CC-CM-02, v1-5.3.4-B (A7 FH, CM co-author on
CC-CM-02); PS-C15 (A7, PS code); v1-3.2.4, v1-3.2.5, v1-6.2.5, v1-5.3.5, v1-5.3.4-A, v1-5.3.1 (A5 SC, SL reviewing
state and local enactments); SC-C02 additions (A5 SC; separate function, the record is extended, not rebuilt).

Content lives in content_*.py beside this file. This script writes one record per file under data/v2/core/
(competencies, tasks, indicators, enactments). After the first write the YAML records are authoritative; re-running
overwrites only the records this script defines (it never deletes). The frozen S1 builders are not used (ADR-0030 §5).

v1 seeds (rewrites, split targets, tasks re-pointed by DE's ADR-0030 merges) are edited in place: the record id,
notation, v1 facets and derivedFrom lineage are kept (carried -> rewritten); text and v2 fields are replaced; v1Seed is
dropped because every published level gets v2 indicators (AUTHORING_GUIDE §6).

Usage:  python3 docs/build/S2-closeout-A/build_s2a.py [--dry-run] [--only ID ...] [--list-tasks]
Licence: Apache-2.0 (code). Records written are CC0-1.0.
"""
from __future__ import annotations

import argparse
import csv
import importlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(HERE))
import emstlib as L  # noqa: E402

TOOL = "claude-opus-5-5"
PROMPT = "docs/build/S2-closeout-A/build_s2a.py + content_*.py @s2-closeout-a@1"
GEN = "2026-10-23T17:15:00Z"
CORE = L.DATA_V2 / "core"
LEVELS = ["L1", "L2", "L3", "L4", "L5"]
CONTENT_MODULES = ["content_fh", "content_sc", "content_sc_s3", "content_ps"]
AGENTS = {
    "SC": "emstagent:a5-sc@s2-closeout-a",
    "SL": "emstagent:a5-sl-review@s2-closeout-a",
    "FH": "emstagent:fh-agent@s2-closeout-a",
    "CM": "emstagent:cm-code@s2-closeout-a",
    "PS": "emstagent:ps-code@s2-closeout-a",
}
ADR_BASE = ["ADR-0003", "ADR-0004", "ADR-0016", "ADR-0017", "ADR-0025", "ADR-0030"]
HOLD_RX = re.compile(r"\btrib(e|es|al)\b|\bindigenous\b|\btreat(y|ies)\b|government-to-government|\bTHPO", re.I)
V1_TASK_TEXT = {r["key"]: r["text"] for r in L.read_csv(ROOT / "data" / "v1_baseline" / "tasks.csv")}
V1_DISPOSITION = {r["v1_code"]: r for r in L.read_csv(ROOT / "docs" / "decisions" / "v1_disposition.csv")}
WRITTEN: list[str] = []


def lm(s):
    return {"en": s}


def prov(agents, evidence="J", sources=None, derived=None, adr=None):
    p = {"method": "llm-assisted", "agent": [AGENTS[a] for a in agents], "generatedAt": GEN, "toolVersion": TOOL,
         "promptVersion": PROMPT, "evidenceLabel": evidence, "reviewStatus": "unreviewed"}
    if sources:
        p["sources"] = sorted(set(sources))
    if derived:
        p["derivedFrom"] = derived
    p["adr"] = adr or ADR_BASE
    return p


def common(rid, typ, label, layer, lifecycle="established"):
    return {"id": rid, "type": typ, "prefLabel": lm(label), "layer": layer, "module": "core", "status": "draft",
            "lifecycleState": lifecycle, "useTier": "develop", "validationStatus": "draft",
            "license": "CC0-1.0", "sensitivity": "public"}


def path_for(sub, rid):
    return CORE / sub / (L.id_to_stem(rid) + ".yaml")


def load_existing(sub, rid):
    p = path_for(sub, rid)
    return (L.load_yaml(p), p) if p.exists() else (None, p)


def merge_derived(existing, extra):
    out, seen = [], set()
    for d in existing or []:
        d = dict(d)
        if d.get("relation") == "carried":
            d["relation"] = "rewritten"
        out.append(d)
        seen.add((d["v1Key"], d["relation"]))
    for k, rel in extra or []:
        if (k, rel) not in seen and not any(x["v1Key"] == k and x["relation"] == rel for x in out):
            out.append({"v1Key": k, "relation": rel})
    return out or None


def v1_task_text(rid):
    if not rid.startswith("seed:v1-"):
        return ""
    return V1_TASK_TEXT.get("v1:" + rid[len("seed:v1-"):].replace("-T", ":T"), "")


def v1_disposition_note(rid):
    d = V1_DISPOSITION.get(rid[len("seed:v1-"):]) if rid.startswith("seed:v1-") else None
    if not d:
        return ""
    return L.normalize_text(f"v1 disposition (ADR-0011; docs/decisions/v1_disposition.csv): {d['decision']} → "
                            f"{d['target']}. Rationale: {d['rationale']}")


# ------------------------------------------------------------------ builders
def build_task(t, comp):
    rid = t["id"]
    text = t["text"]
    existing, path = load_existing("tasks", rid)
    supports = [{"competency": t.get("primary", comp["id"]), "strength": t.get("strength", "primary")}]
    for extra in t.get("also", []):
        supports.append({"competency": extra, "strength": "contributing"})
    rec = common(rid, "Task", text, "L2", t.get("lifecycle", "established"))
    rec.update({"statement": lm(text), "textSha256": L.text_sha256(text), "supports": supports,
                "workFunction": t["wf"], "fieldDependency": t.get("field", "remote-capable"),
                "formationDependency": t.get("formation", "partial"), "homeModule": "core"})
    for key, field in (("modes", "modes"), ("rel", "relationshipTypes"), ("profiles", "workflowProfiles")):
        if t.get(key):
            rec[field] = t[key]
    if t.get("signoff"):
        rec["signOffAuthority"] = {"kind": t["signoff"]}
    if t.get("accountable"):
        rec["accountabilityConstraint"] = {"required": True, "basis": lm(t["accountable"])}
    if t.get("reviewBy"):
        rec["reviewBy"] = t["reviewBy"]
    note = t.get("note", "")
    derived = None
    if existing is not None:
        for k in ("notation", "v1Tier", "v1Domain", "v1SkillArea"):
            if k in existing:
                rec[k] = existing[k]
        derived = merge_derived((existing.get("provenance") or {}).get("derivedFrom"), t.get("derived"))
        old = v1_task_text(rid)
        if old and HOLD_RX.search(old):
            note = (note + " " if note else "") + ("Rewritten from the v1 task text (not quoted: it names held "
                                                   "content; see data/v1_baseline/tasks.csv).")
        elif old:
            note = (note + " " if note else "") + f"Rewritten from the v1 task text: \"{old}\"."
        if existing.get("supports") and existing["supports"][0]["competency"] != supports[0]["competency"]:
            note += f" Re-pointed from {existing['supports'][0]['competency']} to {supports[0]['competency']}."
    elif t.get("derived"):
        derived = [{"v1Key": k, "relation": rel} for k, rel in t["derived"]]
    if note.strip():
        rec["editorialNote"] = lm(("S2 close-out A. " + note.strip()))
    rec["provenance"] = prov(comp["agents"], "J", t.get("sources"), derived, comp.get("adr"))
    return path, rec


def build_indicator(ind, comp, level, idx, span_min):
    rid = f"seed:{comp['slug']}-{level.lower()}-{'abcde'[idx]}"
    rec = common(rid, "Indicator", ind["text"], "L1", comp.get("lifecycle", "established"))
    rec.update({"competency": comp["id"], "level": level, "statement": lm(ind["text"]),
                "augmentationMode": ind.get("mode", "unaided"), "assessmentMethods": ind["methods"],
                "useClass": "develop", "obs4": ind.get("obs4", 3),
                "jurisdictionVariable": bool(ind.get("jv", False))})
    if rec["obs4"] == 2:
        rec["evidencePlan"] = lm(ind.get("plan") or "Pilot the assessment method with two trained raters on "
                                 "synthetic cases before use; promote to obs4 3 only after IO double-coding.")
    if ind.get("evidence"):
        rec["evidenceTypes"] = ind["evidence"]
    if ind.get("tasks"):
        rec["servedTasks"] = ind["tasks"]
    if level != span_min:
        rec["distinguishingAttribute"] = ind["attr"]
    if ind.get("critical"):
        rec["safetyOrLegalCritical"] = True
    derived = [{"v1Key": k, "relation": "rewritten"} for k in ind.get("v1", [])] or None
    rec["provenance"] = prov(comp["agents"], "J", ind.get("sources"), derived, comp.get("adr"))
    return path_for("indicators", rid), rec


def build_enactment(e, comp):
    rid = e["id"]
    rec = common(rid, "Enactment", e["label"], "L1", comp.get("lifecycle", "established"))
    rec.update({"competency": comp["id"], "enactmentKind": "actor", "actorType": e["actor"],
                "authorityBasis": lm(e["basis"])})
    if e.get("delegated"):
        rec["delegatedConstraints"] = lm(e["delegated"])
    rec.update({"principal": lm(e["principal"]), "accountabilityVenue": lm(e["venue"])})
    if e.get("position"):
        rec["authorityPosition"] = e["position"]
    if e.get("links"):
        links = []
        for ins, role, note in e["links"]:
            item = {"instrument": f"seed:ins/{ins}", "role": role}
            if note:
                item["note"] = lm(note)
            links.append(item)
        rec["characteristicInstruments"] = links
    rec["note"] = lm(e["note"])
    agents = list(comp["agents"]) + (["SL"] if e.get("sl_reviewed") and "SL" not in comp["agents"] else [])
    if e.get("editorial"):
        rec["editorialNote"] = lm(e["editorial"])
    rec["provenance"] = prov(agents, e.get("evidence", "J"), e.get("sources"), None, comp.get("adr"))
    return path_for("enactments", rid), rec


def build_competency(c):
    rid = c["id"]
    existing, path = load_existing("competencies", rid)
    rec = common(rid, "Competency", c["label"], "L1", c.get("lifecycle", "established"))
    rec.update({"definition": lm(c["definition"]), "statement": lm(c["statement"]),
                "competencyType": c.get("type", "practice"),
                "levelSpan": {"min": c["span"][0], "max": c["span"][1]}, "homeModule": "core",
                "reusability": c.get("reusability", "cross-subsector")})
    if c.get("alt"):
        rec["altLabel"] = {"en": c["alt"]}
    if c.get("reviewBy"):
        rec["reviewBy"] = c["reviewBy"]
    if c.get("scope"):
        rec["scopeNote"] = lm(c["scope"])
    if c.get("sensitivity"):
        rec["instrumentSensitivity"] = [
            {"mechanism": m, "rationale": lm(r), "evidenceLabel": ev, **({"sources": s} if s else {}),
             **({"reviewBy": "2027-01-31"} if ev in ("J", "S") else {})}
            for (m, r, ev, s) in c["sensitivity"]]
    if c.get("mirrors"):
        rec["mirrors"] = [{"target": t, "relation": r} for t, r in c["mirrors"]]
    note = c.get("editorial", "")
    derived = None
    if existing is not None:
        for k in ("notation", "v1Domain", "v1SkillArea"):
            if k in existing:
                rec[k] = existing[k]
        derived = merge_derived((existing.get("provenance") or {}).get("derivedFrom"), c.get("derived"))
        old = v1_disposition_note(rid)
        if old:
            note = (note + " " if note else "") + "Seed note kept: " + old
    elif c.get("derived"):
        derived = [{"v1Key": k, "relation": rel} for k, rel in c["derived"]]
    if note.strip():
        rec["editorialNote"] = lm(note.strip())
    rec["provenance"] = prov(c["agents"], "J", c.get("sources"), derived, c.get("adr"))
    return path, rec


def assemble(comps):
    out = []
    for c in comps:
        c.setdefault("slug", c["id"].split(":", 1)[1].lower().replace(".", "-"))
        for t in c["tasks"]:
            out.append(build_task(t, c))
        levels = []
        for lv in LEVELS:
            inds = c["levels"].get(lv) or []
            if not inds:
                continue
            if not 2 <= len(inds) <= 5:
                raise SystemExit(f"{c['id']} {lv}: {len(inds)} indicators (2-5 required)")
            ids = []
            for i, ind in enumerate(inds):
                p, r = build_indicator(ind, c, lv, i, c["span"][0])
                out.append((p, r))
                ids.append(r["id"])
            levels.append({"level": lv, "indicators": ids})
        for e in c.get("enactments", []):
            out.append(build_enactment(e, c))
        p, r = build_competency(c)
        r["levels"] = levels
        out.append((p, r))
    return out


# ------------------------------------------------------------------ SC-C02: extend, do not rebuild
def extend_sc_c02(spec):
    """spec: dict with definition, tasks (T dicts), indicators {level: [I dicts]}, derived."""
    out = []
    comp = {"id": "seed:SC-C02", "agents": ["SC"], "slug": "sc-c02", "adr": ADR_BASE}
    for t in spec["tasks"]:
        out.append(build_task(t, comp))
    path = path_for("competencies", "seed:SC-C02")
    rec = L.load_yaml(path)
    if spec["definition_old"] not in rec["definition"]["en"] and spec["definition"] != rec["definition"]["en"]:
        raise SystemExit("SC-C02 definition changed by someone else; merge by hand")
    rec["definition"] = lm(spec["definition"])
    levels = {lv["level"]: lv["indicators"] for lv in rec["levels"]}
    for lv, inds in spec["indicators"].items():
        cur = [i for i in levels.get(lv, []) if not i.startswith("seed:sc-c02-s2a-")]
        for n, ind in enumerate(inds):
            rid = f"seed:sc-c02-s2a-{lv.lower()}-{'abcde'[n]}"
            rec_i = common(rid, "Indicator", ind["text"], "L1")
            rec_i.update({"competency": "seed:SC-C02", "level": lv, "statement": lm(ind["text"]),
                          "augmentationMode": ind.get("mode", "unaided"), "assessmentMethods": ind["methods"],
                          "useClass": "develop", "obs4": ind.get("obs4", 3), "jurisdictionVariable": bool(ind.get("jv"))})
            if ind.get("evidence"):
                rec_i["evidenceTypes"] = ind["evidence"]
            if ind.get("tasks"):
                rec_i["servedTasks"] = ind["tasks"]
            if lv != "L1":
                rec_i["distinguishingAttribute"] = ind["attr"]
            if ind.get("critical"):
                rec_i["safetyOrLegalCritical"] = True
            rec_i["provenance"] = prov(["SC"], "J", ind.get("sources"),
                                       [{"v1Key": k, "relation": "rewritten"} for k in ind.get("v1", [])] or None)
            out.append((path_for("indicators", rid), rec_i))
            cur.append(rid)
        if len(cur) > 5:
            raise SystemExit(f"SC-C02 {lv}: more than 5 indicators")
        levels[lv] = cur
    rec["levels"] = [{"level": lv, "indicators": levels[lv]} for lv in LEVELS if lv in levels]
    rec["provenance"]["derivedFrom"] = merge_derived(rec["provenance"].get("derivedFrom"), spec["derived"])
    src = set(rec["provenance"].get("sources") or []) | set(spec.get("sources") or [])
    rec["provenance"]["sources"] = sorted(src)
    if AGENTS["SC"] not in rec["provenance"]["agent"]:
        rec["provenance"]["agent"] = list(rec["provenance"]["agent"]) + [AGENTS["SC"]]
    ed = rec.get("editorialNote", {}).get("en", "")
    if spec["editorial"] not in ed:
        rec["editorialNote"] = lm((ed + " " + spec["editorial"]).strip())
    # keep editorialNote before provenance and levels last, as written by WP-05
    order = [k for k in rec if k not in ("editorialNote", "provenance", "levels")]
    rec = {**{k: rec[k] for k in order}, "editorialNote": rec["editorialNote"], "provenance": rec["provenance"],
           "levels": rec["levels"]}
    out.append((path, rec))
    return out


def load_content(only=None):
    comps, extra = [], []
    for m in CONTENT_MODULES:
        try:
            mod = importlib.import_module(m)
        except ModuleNotFoundError:
            continue
        comps += getattr(mod, "COMPETENCIES", [])
        if getattr(mod, "SC_C02", None):
            extra.append(mod.SC_C02)
    if only:
        comps = [c for c in comps if c["id"] in only]
        extra = [x for x in extra if "seed:SC-C02" in only]
    return comps, extra


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--list-tasks", action="store_true")
    a = ap.parse_args(argv)
    comps, extra = load_content(set(a.only) if a.only else None)
    out = assemble(comps)
    for x in extra:
        out += extend_sc_c02(x)
    if a.list_tasks:
        for p, r in out:
            if r["type"] == "Task":
                print(r["id"], "\t", r["statement"]["en"])
        return
    ids = [r["id"] for _, r in out]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        raise SystemExit(f"duplicate ids: {sorted(dup)}")
    for p, r in out:
        n = L.word_count(r["statement"]["en"]) if r["type"] in ("Task",) else 0
        if r["type"] == "Task" and not 8 <= n <= 30:
            print(f"WARN task length {n}: {r['id']}")
        if not a.dry_run:
            p.parent.mkdir(parents=True, exist_ok=True)
            L.write_yaml(p, r)
    manifest = sorted(({"id": r["id"], "type": r["type"], "path": str(p.relative_to(ROOT))} for p, r in out),
                      key=lambda x: (x["type"], x["id"]))
    if not a.dry_run:
        gen = HERE / "generated"
        gen.mkdir(exist_ok=True)
        prev = {}
        mp = gen / "s2a_written.json"
        if mp.exists() and a.only:
            prev = {x["id"]: x for x in json.loads(mp.read_text())["records"]}
        for m in manifest:
            prev[m["id"]] = m
        mp.write_text(json.dumps({"records": sorted(prev.values(), key=lambda x: (x["type"], x["id"]))}, indent=1),
                      encoding="utf-8")
    from collections import Counter
    print(json.dumps(Counter(r["type"] for _, r in out), indent=1))


if __name__ == "__main__":
    main()
