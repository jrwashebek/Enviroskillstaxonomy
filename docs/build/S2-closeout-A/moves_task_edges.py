#!/usr/bin/env python3
"""S2 close-out A (A5 SC; LM reviews): task-level sensitivity edges for P1 COR-3 tasks (CR-SC-001 #1, ADR-0030 §1.4).

Ruling: inherited edges are computed (a task carries its primary competencies' edges in the sensitivity view); a stored
Task.instrumentSensitivity edge must add something — a mechanism the competency lacks, or task-specific evidence.
Every row of docs/build/WP-05/generated/task_sensitivity_edges.csv is an inherited draft, so none is converted as is.

Review (this script records it): every task in the R10-R13 bundles (data/v2/core/roles) whose primary competency is
SC-authored was read against its competency's edges. Where the task itself is exposed to a mechanism the competency
does not carry, a task-specific edge is stored on the task (J, rationale stated, reviewBy). All other P1 rows are
"inherited, computed" and the non-P1 rows wait for rc.2 (ADR-0030 §4). Output: generated/task_edge_review.csv.

Usage: python3 docs/build/S2-closeout-A/moves_task_edges.py [--dry-run]
Licence: Apache-2.0 (code). Records stay CC0-1.0.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import emstlib as L  # noqa: E402

AGENT = "emstagent:a5-sc@s2-closeout-a"
TASKS = L.DATA_V2 / "core" / "tasks"
REVIEW_BY = "2027-01-31"
P1_COR3 = ["R10-environmental-review-specialist", "R11-environmental-permit-writer",
           "R12-environmental-compliance-inspector", "R13-resource-program-manager"]

# task -> [(mechanism, rationale)]  — task-specific additions only (mechanism absent from the primary competency)
EDGES = {
    "seed:sc-adopt-other-agency-exclusion": [
        ("DM-05", "Adopting another agency's exclusion requires consulting that agency and documenting comparability, "
                  "so coordination rules change this task and not the rest of review-level screening.")],
    "seed:sc-respond-permit-comments": [
        ("DM-04", "Public notice and comment requirements for draft permits set when a response is owed and what it must "
                  "address.")],
    "seed:sc-draft-permit-fact-sheet": [
        ("DM-08", "Permit appeal and judicial review standards make each condition's stated basis in the fact sheet the "
                  "permit's defense.")],
    "seed:v1-6.1.3-T2": [
        ("DM-06", "Changes to species-consultation triggers change which consultations a proposal sets off."),
        ("DM-07", "Changes to historic-preservation review and its programme alternatives change which reviews a "
                  "proposal sets off.")],
    "seed:sc-negotiate-permit-conditions": [
        ("DM-10", "Substantive standards set the floor below which permit conditions cannot be negotiated.")],
    "seed:sc-select-enforcement-response": [
        ("DM-10", "Enforcement response and penalty policies set the response each finding calls for.")],
    "seed:sc-verify-reported-values": [
        ("DM-13", "Mandatory reporting rules determine which self-reported values exist to verify; their reconsideration "
                  "or removal changes the task directly.")],
    "seed:sc-prepare-staff-report": [
        ("DM-04", "Open-meeting and hearing requirements set when a staff report must be public and what it must state.")],
}


def load_all():
    recs = {}
    for path in sorted((L.DATA_V2 / "core").glob("*/*.yaml")):
        rec = L.load_yaml(path)
        if isinstance(rec, dict) and rec.get("id"):
            recs[rec["id"]] = rec
    return recs


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    recs = load_all()
    p1 = {}
    for role in P1_COR3:
        for tb in recs["seed:" + role].get("taskBundle", []):
            p1.setdefault(tb["task"], []).append(role.split("-")[0])
    # write the task-specific edges
    for tid, edges in EDGES.items():
        if tid not in p1:
            raise SystemExit(f"{tid} is not in a P1 COR-3 bundle")
        path = TASKS / (L.id_to_stem(tid) + ".yaml")
        rec = L.load_yaml(path)
        if rec["provenance"]["agent"][0] != "emstagent:a5-sc@wp-05":
            raise SystemExit(f"{tid}: not SC-authored")
        prim = [s["competency"] for s in rec["supports"] if s["strength"] == "primary"]
        have = {e["mechanism"] for c in prim for e in recs[c].get("instrumentSensitivity") or []}
        items = []
        for m, why in edges:
            if m in have:
                raise SystemExit(f"{tid}: {m} is inherited from {prim}; storing it would be W-EDGE-REDUNDANT")
            items.append({"mechanism": m, "rationale": {"en": why}, "evidenceLabel": "J", "reviewBy": REVIEW_BY})
        new = {}
        for k, v in rec.items():
            if k == "instrumentSensitivity":
                continue
            if k == "provenance":
                new["instrumentSensitivity"] = items
            new[k] = v
        if AGENT not in new["provenance"]["agent"]:
            new["provenance"]["agent"] = list(new["provenance"]["agent"]) + [AGENT]
        if not a.dry_run:
            L.write_yaml(path, new)
    # review table over the WP-05 edge rows
    out = []
    with (ROOT / "docs/build/WP-05/generated/task_sensitivity_edges.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["task"] in p1:
                dec = "P1 COR-3: inherited edge, computed by the sensitivity view (not stored)"
            else:
                dec = "not in a P1 COR-3 bundle: inherited meanwhile; per-task review deferred to rc.2"
            out.append({"task": r["task"], "competency": r["competency"], "mechanism": r["mechanism"],
                        "p1_roles": "|".join(p1.get(r["task"], [])), "decision": dec})
    for tid, edges in EDGES.items():
        for m, _ in edges:
            out.append({"task": tid, "competency": "", "mechanism": m, "p1_roles": "|".join(p1[tid]),
                        "decision": "P1 COR-3: task-specific edge stored on the task (J; reviewBy " + REVIEW_BY + ")"})
    reviewed = sorted({t for t in p1 if recs.get(t, {}).get("provenance", {}).get("agent", [""])[0] == "emstagent:a5-sc@wp-05"})
    if not a.dry_run:
        (HERE / "generated").mkdir(exist_ok=True)
        (HERE / "generated" / "task_edge_review.csv").write_text(
            L.csv_text(["task", "competency", "mechanism", "p1_roles", "decision"], out), encoding="utf-8")
    from collections import Counter
    print({"p1_cor3_tasks": len(p1), "sc_authored_p1_tasks_reviewed": len(reviewed),
           "edges_stored": sum(len(v) for v in EDGES.values()), "tasks_with_stored_edges": len(EDGES),
           "csv_rows": Counter(o["decision"].split(":")[0] for o in out)})


if __name__ == "__main__":
    main()
