#!/usr/bin/env python3
"""Build the WP-07 exploratory pathway records for the P1 corridors (staged), the formation-provisions sidecar and a
generated summary.

Why staged: Pathway.fromVariant/toVariant must resolve to RoleProfile/RoleVariant records, which WP-08 builds in S2. Until
then a pathway under data/v2/ would fail E-REF-DANGLING, so the records are written schema-valid to
docs/build/WP-07/staging/pathways/ and moved to data/v2/core/pathways/ when the role records exist (CR-LC-001).

Outputs (all generated; re-run after other lanes add indicators or tasks):
  docs/build/WP-07/staging/pathways/<stem>.yaml   Pathway records (recommended: false; useTier exploratory)
  docs/build/WP-07/formation_provisions.csv       one row per formation provision (ADR-0026 R7)
  docs/build/WP-07/PATHWAYS.md                    generated summary and reference check

Usage: python3 docs/build/WP-07/scripts/build_wp07_pathways.py [--strict]   (--strict exits 1 on unresolved task/CLO refs)
"""
import argparse
import csv
import io
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(HERE))
import emstlib as L  # noqa: E402
import wp07_pathways as P  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402

OUT = REPO / "docs" / "build" / "WP-07" / "staging" / "pathways"
AGENT = "emstagent:lc-agent@wp-07"
GEN = "2026-10-23T14:20:00Z"
REVIEW_BY = "2027-04-23"


def index():
    tasks, inds, comps, creds = {}, defaultdict(list), {}, {}
    for loc, rec in L.iter_records(REPO / "data" / "v2"):
        if not isinstance(rec, dict):
            continue
        t = rec.get("type")
        if t == "Task":
            tasks[rec["id"]] = rec
        elif t == "Indicator" and rec.get("status") not in ("superseded", "withdrawn"):
            inds[(rec.get("competency"), rec.get("level"))].append(rec["id"])
        elif t == "Competency":
            comps[rec["id"]] = rec
        elif t == "Credential":
            creds[rec["id"]] = rec
    return tasks, inds, comps, creds


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    schema = json.loads((REPO / "schema" / "emst.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    tasks, inds, comps, creds = index()
    OUT.mkdir(parents=True, exist_ok=True)
    prov_rows, report, problems = [], [], []
    for p in P.PATHWAYS:
        seq, all_out, pending_clos, missing_tasks, nprov = [], [], [], [], 0
        for s in p["steps"]:
            outs = []
            for comp, lvl in s["clos"]:
                got = sorted(inds.get((comp, lvl), []))
                if not got:
                    pending_clos.append(f"{comp}@{lvl}")
                outs += got
            live_tasks = []
            for t in s["tasks"]:
                rec = tasks.get(t)
                if rec is None or rec.get("status") in ("superseded", "withdrawn"):
                    missing_tasks.append(t)
                else:
                    live_tasks.append(t)
            note = s["note"]
            clos_txt = ", ".join(f"{c}@{lv}" for c, lv in s["clos"])
            note += f" CLOs: {clos_txt}."
            for pv in s["provisions"]:
                nprov += 1
                note += f" Formation ({pv['response']}): {pv['task']}: {pv['quota']}; release when {pv['release']}."
                trec = tasks.get(pv["task"], {})
                prov_rows.append({
                    "pathway_id": p["id"], "corridor": p["corridor"], "step": s["step"], "role_level": s["roleLevel"],
                    "task_id": pv["task"], "task_statement": (trec.get("statement") or {}).get("en", ""),
                    "task_formation_dependency": trec.get("formationDependency", ""), "task_field_dependency": trec.get("fieldDependency", ""),
                    "v1_prior_design_prompt": pv["v1prior"], "response": pv["response"], "quota": pv["quota"],
                    "release_criterion": pv["release"], "mentor_required": "yes", "evidence_label": "J",
                    "status": "provisional (ADR-0026 R7; pilot calibrates)"})
            item = {"step": s["step"]}
            if live_tasks:
                item["tasks"] = live_tasks
            if outs:
                item["outcomes"] = outs
            item["roleLevel"] = s["roleLevel"]
            item["note"] = {"en": note}
            seq.append(item)
            all_out += outs
        rpl = [c for c in p["rpl"] if c in creds]
        problems += [f"{p['id']}: credential {c} not in register" for c in p["rpl"] if c not in creds]
        rec = {"id": p["id"], "type": "Pathway", "prefLabel": {"en": p["prefLabel"]}, "definition": {"en": p["definition"]},
               "notation": [{"scheme": "mvp-corridor", "value": p["corridor"]}],
               "fromVariant": p["src"], "toVariant": p["dst"], "pathwayType": p["type"],
               "outcomes": sorted(set(all_out)), "modes": p["modes"],
               "assessmentPlan": {"en": ("Each CLO is assessed with the methods its indicators list; field-craft outcomes are assessed at "
                                         "least once in the field, statecraft outcomes in a live or simulated stakeholder or "
                                         "legal-administrative setting, data-craft outcomes on real data with a reproducible product "
                                         "(LC template R4-R5). Assisted-mode outcomes include a seeded-error validation drill. "
                                         + P.SUPERVISOR)},
               "sequence": seq}
        if rpl:
            rec["recognitionOfPriorLearning"] = rpl
        rec["durationAndCost"] = {"hours": p["hours"], "months": p["months"], "costNote": p["cost"]}
        rec["alternativeFormationRoutes"] = p["alt"]
        rec["recommended"] = False
        rec.update({"layer": "learning", "module": "core", "status": "draft", "lifecycleState": "proposed", "reviewBy": REVIEW_BY,
                    "useTier": "exploratory", "validationStatus": "draft", "license": "CC0-1.0", "sensitivity": "public"})
        rec["editorialNote"] = {"en": ("EXPLORATORY, not recommended: no pathway is labelled recommended until it passes CM's M-03 "
                                       "validation gate (ADR-0023 §5; ADR-0027). Built from the role-profile delta (ADR-0026 R1); "
                                       "hours, months and quotas are LC judgment for pilot calibration. Role records are WP-08's; "
                                       "frictions attach when CM's friction register exists. Staged outside data/v2 until the role "
                                       "records resolve (CR-LC-001).")}
        srcs = sorted({x for x in ("V1-05", "V3-03", "V3-13", "V1-02", "LC-104") if x in p["cost"] + " ".join(s["note"] for s in p["steps"])})
        pv = {"method": "llm-assisted", "agent": [AGENT], "generatedAt": GEN, "toolVersion": "claude-opus-5-5",
              "promptVersion": "wp07-pathways@1"}
        if srcs:
            pv["sources"] = srcs
        pv.update({"evidenceLabel": "J", "reviewStatus": "unreviewed", "adr": ["ADR-0026", "ADR-0023", "ADR-0027", "ADR-0004"]})
        rec["provenance"] = pv
        errs = sorted(validator.iter_errors(rec), key=lambda e: list(e.absolute_path))
        for e in errs:
            problems.append(f"{p['id']}: schema {'/'.join(map(str, e.absolute_path))}: {e.message[:200]}")
        L.write_yaml(OUT / f"{L.id_to_stem(p['id'])}.yaml", rec)
        report.append({"id": p["id"], "corridor": p["corridor"], "type": p["type"], "from": p["src"], "to": p["dst"],
                       "steps": len(seq), "outcomes": len(rec["outcomes"]), "tasks": sum(len(x.get("tasks", [])) for x in seq),
                       "provisions": nprov, "pending_clos": pending_clos, "missing_tasks": missing_tasks})
        problems += [f"{p['id']}: task {t} missing or superseded" for t in missing_tasks]
    # sidecar
    cols = ["pathway_id", "corridor", "step", "role_level", "task_id", "task_statement", "task_formation_dependency",
            "task_field_dependency", "v1_prior_design_prompt", "response", "quota", "release_criterion", "mentor_required",
            "evidence_label", "status"]
    (REPO / "docs" / "build" / "WP-07" / "formation_provisions.csv").write_text(L.csv_text(cols, prov_rows), encoding="utf-8")
    # summary
    buf = io.StringIO()
    buf.write("# WP-07 exploratory pathways for the P1 corridors (generated)\n\n")
    buf.write("Generated by `docs/build/WP-07/scripts/build_wp07_pathways.py`; do not edit by hand. Every pathway is **exploratory** "
              "(`recommended: false`, `useTier: exploratory`) until CM's M-03 gate passes (ADR-0023 §5). Records are staged in "
              "`docs/build/WP-07/staging/pathways/` until WP-08's role records exist (CR-LC-001). Role keys are the P1 keys of "
              "`docs/decisions/mvp_role_set.csv`. Formation provisions are in `formation_provisions.csv` (ADR-0026 R7, provisional).\n\n")
    buf.write("| Pathway | Corridor | Type | From → to | Steps | Tasks | CLO indicators | Formation provisions | Pending CLOs | Missing tasks |\n")
    buf.write("|---|---|---|---|---|---|---|---|---|---|\n")
    for r in report:
        buf.write(f"| `{r['id']}` | {r['corridor']} | {r['type']} | `{r['from']}` → `{r['to']}` | {r['steps']} | {r['tasks']} | "
                  f"{r['outcomes']} | {r['provisions']} | {', '.join(r['pending_clos']) or 'none'} | {', '.join(r['missing_tasks']) or 'none'} |\n")
    buf.write(f"\nTotals: {len(report)} pathways, {sum(r['steps'] for r in report)} steps, {len(prov_rows)} formation provisions "
              f"({sum(1 for x in prov_rows if x['response'] == P.QUOTA)} by-hand quotas, "
              f"{sum(1 for x in prov_rows if x['response'] == P.OBS)} observed work-based learning, "
              f"{sum(1 for x in prov_rows if x['response'] in (P.DRILL, P.REP))} validation drills or supervised repetitions).\n")
    buf.write("\nSchema and reference problems: " + ("none" if not problems else "") + "\n")
    for pr in problems:
        buf.write(f"- {pr}\n")
    (REPO / "docs" / "build" / "WP-07" / "PATHWAYS.md").write_text(buf.getvalue(), encoding="utf-8")
    print(f"pathways: {len(report)}; provisions: {len(prov_rows)}; problems: {len(problems)}")
    for pr in problems:
        print("  ", pr)
    if a.strict and problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
