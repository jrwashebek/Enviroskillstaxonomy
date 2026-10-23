#!/usr/bin/env python3
"""WP-05 authoring aid (A5 SC; SL reviews state enactments): writes the Statecraft/regulatory-core records.

One-shot authoring tool. Content lives in content_*.py beside this file; this script turns it into one-record-per-file
YAML under data/v2/core/ (competencies, tasks, indicators, enactments) and three craft-rating passes under
data/v2/assessments/emst-craft@0.1/. After the first write the YAML records are authoritative: edit them, not this
script, unless you deliberately regenerate everything WP-05 owns (re-running overwrites WP-05 records).

v1 seed records (rewrites and re-pointed split-source tasks) are edited in place: the record id, notation, v1 facets
and derivedFrom lineage are kept; text and v2 fields are replaced; v1Seed is dropped once every published level has
v2 indicators (AUTHORING_GUIDE section 6).

Usage:  python3 docs/build/WP-05/build_wp05.py [--dry-run] [--only KEY ...]
Licence: Apache-2.0 (code). Records written are CC0-1.0.
"""
from __future__ import annotations

import argparse
import copy
import importlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(HERE))
import emstlib as L  # noqa: E402

AGENT = "emstagent:a5-sc@wp-05"
SL_REVIEW = "emstagent:a5-sl-review@wp-05"
TOOL = "claude-opus-5-5"
PROMPT = "docs/build/WP-05/build_wp05.py + content_*.py @wp05-sc-authoring@1"
GEN = "2026-10-23T14:30:00Z"
CORE = L.DATA_V2 / "core"
ASM_DIR = L.DATA_V2 / "assessments" / "emst-craft@0.1"
CONTENT_MODULES = ["content_review", "content_authorize", "content_enforce", "content_rules", "content_agreements",
                   "content_txb", "content_extra"]
ADR_BASE = ["ADR-0003", "ADR-0004", "ADR-0007", "ADR-0016", "ADR-0017", "ADR-0025", "ADR-0028", "WP-05"]
LEVELS = ["L1", "L2", "L3", "L4", "L5"]


def lm(s):
    return {"en": s}


def prov(evidence="J", sources=None, derived=None, adr=None, agents=None):
    p = {"method": "llm-assisted", "agent": agents or [AGENT], "generatedAt": GEN, "toolVersion": TOOL,
         "promptVersion": PROMPT, "evidenceLabel": evidence, "reviewStatus": "unreviewed"}
    if sources:
        p["sources"] = sorted(set(sources))
    if derived:
        p["derivedFrom"] = derived
    p["adr"] = adr or ADR_BASE
    return p


def common(rid, typ, label, layer):
    return {"id": rid, "type": typ, "prefLabel": lm(label), "layer": layer, "module": "core", "status": "draft",
            "lifecycleState": "established", "useTier": "develop", "validationStatus": "draft",
            "license": "CC0-1.0", "sensitivity": "public"}


def stem_path(sub, rid, ext=".yaml"):
    return CORE / sub / (L.id_to_stem(rid) + ext)


def load_existing(sub, rid):
    p = stem_path(sub, rid)
    return (L.load_yaml(p), p) if p.exists() else (None, p)


def merge_derived(existing, extra):
    """Keep v1 lineage rows; switch carried -> rewritten; append extra rows not already present."""
    out = []
    seen = set()
    for d in existing or []:
        d = dict(d)
        if d.get("relation") == "carried":
            d["relation"] = "rewritten"
        out.append(d)
        seen.add((d["v1Key"], d["relation"]))
    for k, rel in extra or []:
        if (k, rel) not in seen and not any(x["v1Key"] == k for x in out):
            out.append({"v1Key": k, "relation": rel})
    return out or None


# ------------------------------------------------------------------ builders
def build_task(t, comp_id):
    rid = t["id"]
    text = t["text"]
    existing, path = load_existing("tasks", rid)
    supports = [{"competency": comp_id, "strength": t.get("strength", "primary")}]
    for extra in t.get("also", []):
        supports.append({"competency": extra, "strength": "contributing"})
    rec = common(rid, "Task", text, "L2")
    rec.update({"statement": lm(text), "textSha256": L.text_sha256(text), "supports": supports,
                "workFunction": t["wf"], "fieldDependency": t.get("field", "remote-capable"),
                "formationDependency": t.get("formation", "partial"), "homeModule": "core"})
    if t.get("modes"):
        rec["modes"] = t["modes"]
    if t.get("rel"):
        rec["relationshipTypes"] = t["rel"]
    if t.get("profiles"):
        rec["workflowProfiles"] = t["profiles"]
    if t.get("regime"):
        rec["reproductionRegime"] = t["regime"]
    if t.get("signoff"):
        rec["signOffAuthority"] = {"kind": t["signoff"]}
    if t.get("accountable"):
        rec["accountabilityConstraint"] = {"required": True, "basis": lm(t["accountable"])}
    note = t.get("note")
    derived = None
    if existing is not None:
        # keep v1 facets and lineage
        for k in ("notation", "v1Tier", "v1Domain", "v1SkillArea"):
            if k in existing:
                rec[k] = existing[k]
        derived = merge_derived((existing.get("provenance") or {}).get("derivedFrom"), t.get("derived"))
        old = (existing.get("statement") or {}).get("en", "")
        note = (note + " " if note else "") + f"Rewritten from the v1 task text: \"{old}\" (WP-05)."
    elif t.get("derived"):
        derived = [{"v1Key": k, "relation": rel} for k, rel in t["derived"]]
    if note:
        rec["editorialNote"] = lm(note)
    rec["provenance"] = prov("J", t.get("sources"), derived)
    return path, rec


def build_indicator(ind, comp, level, idx, span_min):
    letter = "abcde"[idx]
    rid = f"seed:{comp['slug']}-{level.lower()}-{letter}"
    rec = common(rid, "Indicator", ind["text"], "L1")
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
    rec["provenance"] = prov("J", ind.get("sources"), derived)
    return stem_path("indicators", rid), rec


def build_enactment(e, comp):
    rid = e["id"]
    rec = common(rid, "Enactment", e["label"], "L1")
    rec.update({"competency": comp["id"], "enactmentKind": e.get("kind", "actor")})
    if rec["enactmentKind"] == "actor":
        rec.update({"actorType": e["actor"], "authorityBasis": lm(e["basis"]), "principal": lm(e["principal"]),
                    "accountabilityVenue": lm(e["venue"])})
        if e.get("position"):
            rec["authorityPosition"] = e["position"]
        if e.get("jurisdiction"):
            rec["jurisdiction"] = e["jurisdiction"]
    elif rec["enactmentKind"] == "craft":
        rec["craft"] = e["craft"]
    if e.get("instruments"):
        rec["characteristicInstruments"] = e["instruments"]
    if e.get("addTasks"):
        rec["additionalTasks"] = e["addTasks"]
    rec["note"] = lm(e["note"])
    agents = [AGENT, SL_REVIEW] if e.get("sl_reviewed") else [AGENT]
    rec["provenance"] = prov(e.get("evidence", "J"), e.get("sources"), None, agents=agents)
    if e.get("editorial"):
        rec["editorialNote"] = lm(e["editorial"])
    return stem_path("enactments", rid), rec


def build_competency(c):
    rid = c["id"]
    existing, path = load_existing("competencies", rid)
    rec = common(rid, "Competency", c["label"], "L1")
    rec.update({"definition": lm(c["definition"]), "statement": lm(c["statement"]),
                "competencyType": c.get("type", "practice")})
    if c.get("cluster"):
        rec["transversalCluster"] = c["cluster"]
    rec["levelSpan"] = {"min": c["span"][0], "max": c["span"][1]}
    rec["homeModule"] = "core"
    rec["reusability"] = c.get("reusability", "cross-subsector")
    if c.get("alt"):
        rec["altLabel"] = {"en": c["alt"]}
    if c.get("lifecycle"):
        rec["lifecycleState"] = c["lifecycle"]
    if c.get("reviewBy"):
        rec["reviewBy"] = c["reviewBy"]
    if c.get("scope"):
        rec["scopeNote"] = lm(c["scope"])
    if c.get("sensitivity"):
        rec["instrumentSensitivity"] = [
            {"mechanism": m, "rationale": lm(r), "evidenceLabel": ev, **({"sources": s} if s else {})}
            for (m, r, ev, s) in c["sensitivity"]]
    if c.get("learning"):
        rec["learningDesign"] = {"assessmentContext": lm(c["learning"])}
    note = c.get("editorial", "")
    derived = None
    if existing is not None:
        for k in ("notation", "v1Domain", "v1SkillArea"):
            if k in existing:
                rec[k] = existing[k]
        derived = merge_derived((existing.get("provenance") or {}).get("derivedFrom"), c.get("derived"))
        old_note = (existing.get("editorialNote") or {}).get("en", "")
        note = (note + " " if note else "") + ("Seed note kept: " + old_note if old_note else "")
    elif c.get("derived"):
        derived = [{"v1Key": k, "relation": rel} for k, rel in c["derived"]]
    if note.strip():
        rec["editorialNote"] = lm(note.strip())
    rec["provenance"] = prov("J", c.get("sources"), derived)
    return path, rec


def assemble(comps):
    out = []          # (path, rec)
    for c in comps:
        c.setdefault("slug", c["id"].split(":", 1)[1].lower().replace(".", "-"))
        for t in c["tasks"]:
            out.append(build_task(t, c["id"]))
        levels = []
        for lv in LEVELS:
            inds = c["levels"].get(lv) or []
            if not inds:
                continue
            ids = []
            for i, ind in enumerate(inds):
                p, r = build_indicator(ind, c, lv, i, c["span"][0])
                out.append((p, r))
                ids.append(r["id"])
            levels.append({"level": lv, "indicators": ids})
        enas = []
        for e in c.get("enactments", []):
            p, r = build_enactment(e, c)
            out.append((p, r))
            enas.append(r["id"])
        p, r = build_competency(c)
        r["levels"] = levels
        # Competency.enactments is an inverse link computed in bundles (ADR-0029; RULINGS_FOR_DE 1.2):
        # enactments point to their competency only.
        out.append((p, r))
    return out


def ratings(comps, passes):
    """passes: {1: {task_id: (FC, DC, SC, conf)}, 2: ..., 3: ...}."""
    texts = {t["id"]: t["text"] for c in comps for t in c["tasks"]}
    files = {}
    for n, table in passes.items():
        rows = []
        for tid in sorted(table):
            if tid not in texts:
                raise SystemExit(f"rating pass {n}: unknown task {tid}")
            fc, dc, sc, conf = table[tid]
            stem = L.id_to_stem(tid)
            rows.append({
                "id": f"seed:asm/wp05-sc-pass{n}/{stem}", "type": "CraftRating",
                "prefLabel": lm(f"WP-05 pass {n} craft rating of {tid}"), "layer": "L5", "module": "core",
                "status": "draft", "license": "CC0-1.0", "sensitivity": "public",
                "task": tid, "taskTextSha256": L.text_sha256(texts[tid]), "scale": "ordinal-0-2",
                "values": {"FC": fc, "DC": dc, "SC": sc}, "raterType": "llm",
                "raterId": f"emstagent:a5-sc-rater-{n}@wp-05", "assessedAt": "2026-10-23",
                "method": ("codebook emst-craft-codebook@1.0.0-draft sections 3-6 applied to task text only, units in "
                           f"a pass-specific random order (seed {n}); same model and session as the author, so not "
                           "blind to authoring context: run-to-run consistency only, LLM-coder gate level G0"),
                "confidence": conf, "instrument": "emst-craft@0.1",
                "codebookVersion": "emst-craft-codebook@1.0.0-draft (vocab/crafts.yaml 1.0.0-draft)",
                "evidenceLabel": "S", "sources": [],
                "provenance": {"method": "llm-assisted", "agent": [f"emstagent:a5-sc-rater-{n}@wp-05"],
                               "generatedAt": GEN, "toolVersion": TOOL,
                               "promptVersion": f"docs/build/WP-05/ratings_pass{n}.csv@wp05-craft@1",
                               "evidenceLabel": "S", "reviewStatus": "unreviewed", "adr": ["ADR-0005", "WP-05"]}})
        files[ASM_DIR / f"wp05-sc-pass{n}.jsonl"] = rows
    return files


def load_passes():
    import csv
    passes = {}
    for n in (1, 2, 3):
        p = HERE / f"ratings_pass{n}.csv"
        if not p.exists():
            continue
        table = {}
        for r in csv.DictReader(p.open(encoding="utf-8")):
            table[r["task_id"]] = (int(r["FC"]), int(r["DC"]), int(r["SC"]), r["confidence"])
        passes[n] = table
    return passes


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--list-tasks", action="store_true", help="print task ids and texts (for rating passes)")
    args = ap.parse_args(argv)
    comps = []
    for m in CONTENT_MODULES:
        try:
            mod = importlib.import_module(m)
        except ModuleNotFoundError:
            continue
        comps.extend(copy.deepcopy(mod.COMPETENCIES))
    if args.only:
        comps = [c for c in comps if c["id"].split(":", 1)[1] in args.only]
    if args.list_tasks:
        for c in comps:
            for t in c["tasks"]:
                print(t["id"], "\t", t["text"])
        return 0
    out = assemble(comps)
    seen = {}
    for p, r in out:
        if r["id"] in seen:
            raise SystemExit(f"duplicate id {r['id']}")
        seen[r["id"]] = p
    passes = load_passes()
    asm = ratings(comps, passes) if passes else {}
    if args.dry_run:
        print(f"{len(out)} records; {sum(len(v) for v in asm.values())} ratings")
        return 0
    for p, r in out:
        p.parent.mkdir(parents=True, exist_ok=True)
        L.write_yaml(p, r)
    for p, rows in asm.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        L.write_jsonl(p, rows)
    counts = {}
    for _, r in out:
        counts[r["type"]] = counts.get(r["type"], 0) + 1
    counts["CraftRating"] = sum(len(v) for v in asm.values())
    (HERE / "generated").mkdir(exist_ok=True)
    (HERE / "generated" / "wp05_written.json").write_text(json.dumps(
        {"counts": counts, "records": sorted(seen)}, indent=1), encoding="utf-8")
    print(json.dumps(counts, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
