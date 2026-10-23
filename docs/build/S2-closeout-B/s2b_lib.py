"""Shared helpers for S2 close-out builder B (authoring aid; never run by CI).

Writes one record per file into data/v2/ following docs/standard/AUTHORING_GUIDE.md. Every write is guarded:
- a new file is written freely;
- an existing file is overwritten only when it is (a) an unauthored v1 seed (`validationStatus: seed-v1`) named in
  this builder's work orders (in-place rewrite, AUTHORING_GUIDE section 6), or (b) a record this builder wrote before
  (its provenance names one of BUILDER_AGENTS);
- cross-lane edits (records owned by another lane that a work order tells this builder to extend) go through
  `patch()`, which loads the live file, applies a minimal change and appends the contributing agent.
Every write is logged to manifest.csv (id, type, path, action, row).

Licence: Apache-2.0 (code).
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import emstlib as L  # noqa: E402

DATA = REPO / "data" / "v2"
MODEL = "claude-opus-5-5"
GEN_AT = "2026-10-23T16:40:00Z"
TODAY = "2026-10-23"

AG = {
    "DB": "emstagent:db-agent@s2-closeout-b",
    "FC": "emstagent:fc-agent@wp-03",          # CR-FC-001 ruling: provenance agent[] gains this ID
    "DC": "emstagent:dc-agent@s2-closeout-b",
    "LC": "emstagent:lc-agent@s2-closeout-b",
    "IO": "emstagent:io-agent@s2-closeout-b",
    "LM": "emstagent:lm-agent@s2-closeout-b",
    "FS": "emstagent:fs-agent@s2-closeout-b",
}
BUILDER_AGENTS = {v for k, v in AG.items() if k != "FC"} | {"emstagent:fc-agent@s2-closeout-b"}
PROMPT = {"DB": "s2b-db@1", "FC": "s2b-fc@1", "DC": "s2b-dc@1", "LC": "s2b-lc@1", "IO": "s2b-lc@1",
          "LM": "s2b-lm-fs@1", "FS": "s2b-lm-fs@1"}

MANIFEST = HERE / "manifest.csv"
_FIELDS = ["id", "type", "path", "action", "row"]


def _manifest_rows():
    if not MANIFEST.exists():
        return []
    return L.read_csv(MANIFEST)


def log(rid, typ, path, action, row):
    rows = [r for r in _manifest_rows() if r["id"] != rid]
    rows.append({"id": rid, "type": typ, "path": str(Path(path).relative_to(REPO)), "action": action, "row": row})
    rows.sort(key=lambda r: (r["row"], r["type"], r["id"]))
    MANIFEST.write_text(L.csv_text(_FIELDS, rows), encoding="utf-8")


def path_for(rid: str, typ: str, area: str) -> Path:
    d = L.ENTITY[typ]["store"][1]
    base = DATA / "core" if area == "core" else DATA / "modules" / area
    return base / d / (L.id_to_stem(rid) + ".yaml")


def find(rid: str) -> Path | None:
    stem = L.id_to_stem(rid) + ".yaml"
    hits = [p for p in DATA.rglob(stem) if p.is_file()]
    return hits[0] if hits else None


def load(rid: str):
    p = find(rid)
    return (p, L.load_yaml(p)) if p else (None, None)


def prov(roles, evidence="J", derived=None, sources=None, adr=None, generated=GEN_AT):
    roles = [roles] if isinstance(roles, str) else roles
    p = {"method": "llm-assisted", "agent": [AG[r] for r in roles], "generatedAt": generated,
         "toolVersion": MODEL, "promptVersion": PROMPT[roles[0]]}
    if derived:
        p["derivedFrom"] = derived
    if sources:
        p["sources"] = sources
    p["evidenceLabel"] = evidence
    p["reviewStatus"] = "unreviewed"
    if adr:
        p["adr"] = adr
    return p


def _owned(rec) -> bool:
    agents = set(((rec or {}).get("provenance") or {}).get("agent") or [])
    return bool(agents & BUILDER_AGENTS)


def put(rec: dict, area: str, row: str, allow_seed: bool = False):
    """Write a record. Refuses to overwrite another lane's authored record."""
    rid, typ = rec["id"], rec["type"]
    p = find(rid) or path_for(rid, typ, area)
    action = "new"
    if p.exists():
        old = L.load_yaml(p)
        if old.get("validationStatus") == "seed-v1" and allow_seed:
            action = "rewrite-seed"
        elif _owned(old):
            action = "rewrite-own"
        else:
            raise SystemExit(f"refusing to overwrite {p.relative_to(REPO)} (not a seed in my rows, not mine)")
    want = path_for(rid, typ, area)
    if p != want and p.exists():
        p.unlink()
    p = want
    L.write_yaml(p, rec)
    log(rid, typ, p, action, row)
    return p


def patch(rid: str, fn, role: str, row: str, note: str | None = None):
    """Minimal cross-lane edit: load, apply fn(rec) in place, add agent, append editorial note; write."""
    p, rec = load(rid)
    if rec is None:
        raise SystemExit(f"patch target {rid} not found")
    fn(rec)
    prov_ = rec.setdefault("provenance", {})
    agents = prov_.setdefault("agent", [])
    if AG[role] not in agents:
        agents.append(AG[role])
    if note:
        en = (rec.get("editorialNote") or {}).get("en", "")
        if note not in en:
            rec["editorialNote"] = {"en": (en + " | " if en else "") + note}
    L.write_yaml(p, rec)
    log(rid, rec["type"], p, "patch", row)
    return p


# ------------------------------------------------------------------ record builders

def _label(text: str, n: int = 14) -> str:
    words = text.rstrip(".").split()
    cut = text.rstrip(".").split(",")[0].split()
    pick = cut if 4 <= len(cut) <= n else words[:n]
    return " ".join(pick)


def indicator(cid, key, level, text, mode, methods, area, roles, served, att=None, obs4=3, jv=False,
              use="develop", derived=None, evidence_plan=None, safety=None, subsectors=None):
    rec = {"id": key, "type": "Indicator", "prefLabel": {"en": _label(text)}, "competency": cid, "level": level,
           "statement": {"en": text}, "augmentationMode": mode, "assessmentMethods": methods, "useClass": use,
           "obs4": obs4}
    if evidence_plan or obs4 == 2:
        rec["evidencePlan"] = {"en": evidence_plan or "Second coder confirms observability; collect a work sample before release."}
    rec["jurisdictionVariable"] = jv
    if served:
        rec["servedTasks"] = served
    if att:
        rec["distinguishingAttribute"] = att
    if safety is not None:
        rec["safetyOrLegalCritical"] = safety
    rec.update({"layer": "L1", "module": area, "status": "draft", "lifecycleState": "established", "useTier": use,
                "validationStatus": "draft", "license": "CC0-1.0", "sensitivity": "public",
                "provenance": prov(roles, derived=derived, adr=["ADR-0004", "ADR-0003"])})
    return rec


def task(tid, text, supports, wf, field, formation, area, roles, regime=None, gates=None, signoff=None,
         modes=None, rel=None, derived=None, notation=None, keep=None, note=None, lifecycle="established",
         subsectors=None, sources=None, accountability=None):
    rec = {"id": tid, "type": "Task", "prefLabel": {"en": text}, "statement": {"en": text},
           "textSha256": L.text_sha256(text), "supports": supports, "workFunction": wf}
    if modes:
        rec["modes"] = modes
    if rel:
        rec["relationshipTypes"] = rel
    rec["fieldDependency"] = field
    rec["formationDependency"] = formation
    if regime:
        rec["reproductionRegime"] = regime
    if gates:
        rec["credentialGates"] = gates
    if signoff:
        rec["signOffAuthority"] = signoff
    if accountability:
        rec["accountabilityConstraint"] = accountability
    rec["homeModule"] = area
    if subsectors:
        rec["subsectors"] = subsectors
    if notation:
        rec["notation"] = notation
    rec.update({"layer": "L2", "module": area, "status": "draft", "lifecycleState": lifecycle, "useTier": "describe",
                "validationStatus": "draft"})
    if keep:
        rec.update(keep)
    if note:
        rec["editorialNote"] = {"en": note}
    rec.update({"license": "CC0-1.0", "sensitivity": "public",
                "provenance": prov(roles, derived=derived, sources=sources, adr=["ADR-0003", "ADR-0005", "ADR-0011"] if derived else ["ADR-0003", "ADR-0005"])})
    if lifecycle in ("emerging", "proposed"):
        rec["reviewBy"] = "2027-10-23"
    return rec


def knowledge(kid, text, cid, lowest, area, roles, derived=None):
    return {"id": kid, "type": "KnowledgeStatement", "prefLabel": {"en": _label(text, 10)}, "statement": {"en": text},
            "lowestLevel": lowest, "supports": [cid], "assessmentMethods": ["knowledge-test"], "layer": "L2",
            "module": area, "status": "draft", "lifecycleState": "established", "useTier": "describe",
            "validationStatus": "draft", "license": "CC0-1.0", "sensitivity": "public",
            "provenance": prov(roles, derived=derived, adr=["ADR-0003", "ADR-0004"])}


def enactment(eid, cid, module, label, note, roles, subsectors, position=None, tasks=None, variants=None,
              instruments=None, editorial=None):
    rec = {"id": eid, "type": "Enactment", "prefLabel": {"en": label}, "competency": cid, "enactmentKind": "module"}
    if position:
        rec["authorityPosition"] = position
    rec["enactedInModule"] = module
    rec["subsectors"] = subsectors
    if instruments:
        rec["characteristicInstruments"] = instruments
    if tasks:
        rec["additionalTasks"] = tasks
    if variants:
        rec["indicatorVariants"] = variants
    rec["note"] = {"en": note}
    rec.update({"layer": "L1", "module": module, "status": "draft", "lifecycleState": "established",
                "useTier": "describe", "validationStatus": "draft", "license": "CC0-1.0", "sensitivity": "public"})
    if editorial:
        rec["editorialNote"] = {"en": editorial}
    rec["provenance"] = prov(roles, adr=["ADR-0018", "ADR-0003", "ADR-0030"])
    return rec


def seed_derived_from(old: dict) -> list:
    """Keep a v1 seed's lineage; its own 'carried' row becomes 'rewritten'."""
    out = []
    own = None
    for n in (old.get("notation") or []):
        if n.get("scheme") == "EMSTv1":
            own = f"v1:{n['value']}"
    for d in (old.get("provenance") or {}).get("derivedFrom") or []:
        d = dict(d)
        if d.get("relation") == "carried" and d.get("v1Key") == own:
            d["relation"] = "rewritten"
        out.append(d)
    return out


def competency(c: dict, old: dict | None = None) -> dict:
    """Build a Competency record from a content spec; keep a seed's id/notation/facets when rewriting in place."""
    rec = {"id": c["id"], "type": "Competency", "prefLabel": {"en": c["label"]}}
    if c.get("alt"):
        rec["altLabel"] = {"en": c["alt"]}
    rec["definition"] = {"en": c["definition"]}
    rec["statement"] = {"en": c["statement"]}
    if old and old.get("notation"):
        rec["notation"] = old["notation"]
    rec["competencyType"] = c.get("ctype", "practice")
    if c.get("cluster"):
        rec["transversalCluster"] = c["cluster"]
    if c.get("ctype", "practice") != "knowledge-area":
        lv = c["levels"]
        rec["levelSpan"] = {"min": min(lv), "max": max(lv)}
        rec["levels"] = [{"level": k, "indicators": [i["id"] for i in v]} for k, v in sorted(lv.items())]
    elif c.get("span"):
        rec["levelSpan"] = {"min": c["span"][0], "max": c["span"][1]}
    if c.get("knowledge"):
        rec["knowledge"] = [k["id"] for k in c["knowledge"]]
    rec["homeModule"] = c.get("area", "core")
    if c.get("subsectors"):
        rec["subsectors"] = c["subsectors"]
    rec["reusability"] = c.get("reusability", "cross-subsector")
    if c.get("learningDesign"):
        rec["learningDesign"] = c["learningDesign"]
    if c.get("sensitivity_edges"):
        rec["instrumentSensitivity"] = c["sensitivity_edges"]
    if c.get("mirrors"):
        rec["mirrors"] = c["mirrors"]
    area = c.get("area", "core")
    rec.update({"layer": "L1", "module": area, "status": "draft", "lifecycleState": c.get("lifecycle", "established"),
                "useTier": c.get("useTier", "develop"), "validationStatus": "draft"})
    if c.get("lifecycle") in ("emerging", "proposed"):
        rec["reviewBy"] = c.get("reviewBy", "2027-10-23")
    if old:
        for k in ("v1Domain", "v1SkillArea"):
            if old.get(k):
                rec[k] = old[k]
    rec["editorialNote"] = {"en": c["note"]}
    rec["license"] = "CC0-1.0"
    rec["sensitivity"] = "public"
    derived = (seed_derived_from(old) if old else []) + list(c.get("derived") or [])
    seen, dd = set(), []
    for d in derived:
        k = (d["v1Key"], d["relation"])
        if k not in seen:
            seen.add(k)
            dd.append(d)
    rec["provenance"] = prov(c["roles"], derived=dd or None, sources=c.get("sources"), adr=c.get("adr"))
    return rec


def build(c: dict, row: str):
    """Write a competency spec with its indicators, tasks and knowledge statements."""
    area = c.get("area", "core")
    old = None
    seed = False
    p, existing = load(c["id"])
    if existing is not None and existing.get("validationStatus") == "seed-v1":
        old, seed = existing, True
    elif existing is not None and not _owned(existing):
        raise SystemExit(f"{c['id']} exists and is not mine or a seed")
    for lvl, inds in c.get("levels", {}).items():
        for i in inds:
            put(indicator(c["id"], i["id"], lvl, i["text"], i["mode"], i["methods"], area, c["roles"], i.get("served"),
                          att=i.get("att"), obs4=i.get("obs4", 3), jv=i.get("jv", False), derived=i.get("derived"),
                          evidence_plan=i.get("plan"), safety=i.get("safety")), area, row)
    for k in c.get("knowledge", []):
        put(knowledge(k["id"], k["text"], c["id"], k["lowest"], area, c["roles"], derived=k.get("derived")), area, row)
    for t in c.get("tasks", []):
        build_task(t, c, area, row)
    put(competency(c, old), area, row, allow_seed=seed)


def build_task(t, c, area, row):
    tid = t["id"]
    p, old = load(tid)
    keep, derived, notation, allow = {}, list(t.get("derived") or []), None, False
    if old is not None:
        if old.get("validationStatus") == "seed-v1":
            allow = True
            notation = old.get("notation")
            for k in ("v1Tier", "v1Domain", "v1SkillArea"):
                if old.get(k):
                    keep[k] = old[k]
            for d in (old.get("provenance") or {}).get("derivedFrom") or []:
                d = dict(d)
                if d.get("relation") == "carried":
                    d["relation"] = "rewritten"
                derived.insert(0, d)
        elif not _owned(old):
            raise SystemExit(f"task {tid} exists and is not mine or a seed")
    supports = t.get("supports") or [{"competency": c["id"], "strength": "primary"}]
    for extra in t.get("contrib", []):
        supports.append({"competency": extra, "strength": "contributing"})
    note = t.get("note")
    if old is not None and allow:
        base = "Rewritten to v2 task rules (one verb, 8-30 words, no product or instrument names; ADR-0003 G-2)."
        note = base + (" " + note if note else "")
    rec = task(tid, t["text"], supports, t["wf"], t["field"], t["formation"], t.get("area", area), c["roles"],
               regime=t.get("regime"), gates=t.get("gates"), signoff=t.get("signoff"), modes=t.get("modes"),
               rel=t.get("rel"), derived=derived or None, notation=notation, keep=keep, note=note,
               lifecycle=t.get("lifecycle", c.get("lifecycle", "established") if c.get("lifecycle") != "emerging" else "emerging"),
               subsectors=t.get("subsectors"), sources=t.get("sources"))
    put(rec, t.get("area", area), row, allow_seed=allow)


def supersede_task(tid, into, row, role, note):
    """Supersede a duplicate v1 task seed into a surviving task (merged-from lineage kept)."""
    p, old = load(tid)
    if old is None:
        raise SystemExit(f"{tid} not found")
    if old.get("validationStatus") != "seed-v1" and not _owned(old):
        raise SystemExit(f"{tid} is not a seed or mine")
    old["status"] = "superseded"
    old["replacedBy"] = [into]
    old["editorialNote"] = {"en": ((old.get("editorialNote") or {}).get("en", "") + " | " if old.get("editorialNote") else "") + note}
    pv = old.setdefault("provenance", {})
    ag = pv.setdefault("agent", [])
    if AG[role] not in ag:
        ag.append(AG[role])
    L.write_yaml(p, old)
    log(tid, "Task", p, "supersede-seed", row)


def check_words(c):
    """Fast local checks before writing (the validator is authoritative)."""
    errs = []
    if L.word_count(c["statement"]) > 60:
        errs.append(f"{c['id']} statement {L.word_count(c['statement'])} words")
    for lvl, inds in c.get("levels", {}).items():
        if not 2 <= len(inds) <= 5:
            errs.append(f"{c['id']} {lvl} has {len(inds)} indicators")
        for i in inds:
            n = L.word_count(i["text"])
            if n > 30:
                errs.append(f"{i['id']} {n} words")
            if i["text"].count(". ") or not i["text"].endswith("."):
                errs.append(f"{i['id']} sentence form")
    for t in c.get("tasks", []):
        n = L.word_count(t["text"])
        if not 8 <= n <= 30:
            errs.append(f"{t['id']} task {n} words")
        if re.match(r"^\s*\w+\s+(and|or)\s+\w+\b", t["text"]):
            errs.append(f"{t['id']} compound verb")
    return errs
