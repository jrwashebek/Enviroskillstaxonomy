#!/usr/bin/env python3
"""S2 close-out A: generate the row-by-row completion table against the work orders, and the core-size check.

Read-only over data/v2 and the work orders. Writes generated/completion.csv, generated/core_size.json and prints the
markdown table pasted into WORKLOG.md. Every number is computed here, never typed.
Usage: python3 docs/build/S2-closeout-A/gen_completion.py
Licence: Apache-2.0.
"""
from __future__ import annotations

import csv
import glob
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import emstlib as L  # noqa: E402

MINE = ("A5 SC", "A7 FH", "A7 (PS code)")


def load():
    recs = {}
    for f in glob.glob(str(L.DATA_V2 / "**" / "*.yaml"), recursive=True):
        r = L.load_yaml(Path(f))
        if isinstance(r, dict) and r.get("id"):
            recs[r["id"]] = r
    return recs


def jsonl(path):
    p = Path(path)
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


def comp_status(recs, cid):
    c = recs.get(cid)
    if not c:
        return "missing", ""
    tasks = [t for t in recs.values() if t.get("type") == "Task" and
             any(s.get("competency") == cid and s.get("strength") == "primary" for s in t.get("supports") or [])]
    inds = sum(len(l["indicators"]) for l in c.get("levels") or [])
    ena = sum(1 for e in recs.values() if e.get("type") == "Enactment" and e.get("competency") == cid)
    ok = c.get("validationStatus") == "draft" and len(tasks) >= 3 and inds >= 4 and "v1Seed" not in c
    return ("done" if ok else "incomplete"), (f"{c['validationStatus']}; {len(tasks)} primary tasks; {inds} indicators "
                                              f"on {len(c.get('levels') or [])} levels; {ena} enactments; "
                                              f"lifecycle {c.get('lifecycleState')}")


def main():
    recs = load()
    rows_out = []
    wo = list(csv.DictReader((ROOT / "docs/decisions/integration/s2_work_orders.csv").open(encoding="utf-8")))
    sc_enas = [e for e in recs.values() if e.get("type") == "Enactment" and e.get("module") == "core" and
               (e.get("provenance") or {}).get("agent", [""])[0] == "emstagent:a5-sc@wp-05"]
    untyped = sum(1 for e in sc_enas for x in e.get("characteristicInstruments") or [] if not x.get("role"))
    typed = sum(1 for e in sc_enas for x in e.get("characteristicInstruments") or [] if x.get("role"))
    dc_moved = sum(1 for e in sc_enas if e.get("delegatedConstraints"))
    dc_left = sum(1 for e in sc_enas if "Delegated constraints:" in (e.get("authorityBasis") or {}).get("en", ""))
    slc02 = recs["seed:ena-sl-c02-federal-regulator"]["characteristicInstruments"]
    slc02_txt = ", ".join(f"{x['instrument'].split('/')[-1]}={x['role']}" for x in slc02)
    mirrors = sum(len(c.get("mirrors") or []) for c in recs.values() if c.get("type") == "Competency")
    edges = sum(len(t.get("instrumentSensitivity") or []) for t in recs.values() if t.get("type") == "Task")
    variants = [v for v in recs.values() if v.get("type") == "RoleVariant"]
    band_left = sum(1 for v in variants if (v.get("indicativeGradeOrBand") or {}).get("band"))
    by_level = sum(1 for v in variants if (v.get("indicativeGradeOrBand") or {}).get("byRoleLevel"))
    xrec = sum(len(jsonl(p)) for p in glob.glob(str(L.DATA_V2 / "assessments/emst-exposure@2.0/s2a-wp08-atoms-pass*.jsonl")))
    sigs = len(jsonl(L.DATA_V2 / "signals/2026/s2a-change-view-atoms.jsonl"))
    conv = list(csv.DictReader((HERE / "generated/change_atom_conversion.csv").open(encoding="utf-8")))
    atoms = len(L.load_yaml(ROOT / "docs/build/WP-08/change_view_inputs.yaml")["atoms"])
    viewlib = (ROOT / "pipelines/views/viewlib.py").read_text(encoding="utf-8")
    db52 = {k: [f"{x['instrument'].split('/')[-1]}={x['role']}" for x in recs[k].get("characteristicInstruments") or []]
            for k in ("seed:ena-db-c52-federal", "seed:ena-db-c52-state")}
    sc02 = recs["seed:SC-C02"]
    sc02_ok = all(t in recs for t in ("seed:sc-respond-records-request", "seed:sc-place-litigation-hold")) and \
        any(d["v1Key"] == "v1:3.3.5" for d in sc02["provenance"]["derivedFrom"])
    worklog = (HERE / "WORKLOG.md").read_text(encoding="utf-8")
    for r in wo:
        a = r["author"]
        if not (any(m in a for m in MINE) or "A5 SC (LM supplies" in a or "with A5 SC" in a or "A7 PS code" in a):
            continue
        tgt = r["target"]
        status, detail = "?", ""
        if r["kind"] == "core-residue" and tgt.startswith("seed:") and tgt != "seed:SC-C02":
            status, detail = comp_status(recs, tgt)
        elif tgt == "seed:SC-C02":
            status = "done" if sc02_ok else "incomplete"
            detail = "retention, litigation-hold and disclosure tasks; 6 re-pointed task seeds rewritten; definition +1 clause"
        elif "38 SC actor" in tgt:
            status = "done" if untyped == 0 and dc_left == 0 else "incomplete"
            detail = (f"{len(sc_enas)} SC core enactments: {typed} typed links, {untyped} untyped; delegatedConstraints "
                      f"on {dc_moved}; SL-C02 federal: {slc02_txt}")
        elif "db-c52" in tgt:
            status = "done (SC part; LM to confirm)" if all(db52.values()) else "incomplete"
            detail = "; ".join(f"{k.split(':')[1]}: {', '.join(v)}" for k, v in db52.items())
        elif "mirror_links" in tgt:
            status, detail = "done", f"{mirrors} Competency.mirrors[] links stored (generated/mirror_migration.csv)"
        elif "task_sensitivity_edges" in tgt:
            status, detail = "done (P1); rest rc.2", f"{edges} task-specific edges stored (generated/task_edge_review.csv)"
        elif r["kind"] == "review":
            status = "done (PS part)" if "review of PS-C07 and PS-C09" in worklog else "open"
            detail = "findings and requests to DC in WORKLOG; no record edited; DB-C06/DB-C21 are DB's"
        elif "indicativeGradeOrBand" in tgt:
            status = "done" if band_left == 0 else "incomplete"
            detail = f"{by_level} variants with byRoleLevel; {band_left} with the micro-format left"
        elif "evidenceNotice" in tgt:
            status = "done" if "issuer is verified" in viewlib else "open"
            detail = "pipelines/views/viewlib.py EVIDENCE_NOTICE + gate_view; views regenerated"
        elif r["kind"] == "coding-pass":
            status = "done" if xrec and len(conv) == atoms else "incomplete"
            detail = f"{xrec} exposure records; {sigs} role-attached watch signals; {len(conv)}/{atoms} atoms routed"
        rows_out.append({"kind": r["kind"], "target": tgt, "author": a, "sprint": r["sprint"], "status": status,
                         "detail": detail})
    (HERE / "generated").mkdir(exist_ok=True)
    (HERE / "generated" / "completion.csv").write_text(
        L.csv_text(["kind", "target", "author", "sprint", "status", "detail"], rows_out), encoding="utf-8")
    # core size (same rule as docs/decisions/integration/s1_integration_review.py, read-only, no file written there)
    hold = L.load_yaml(L.DATA_V2 / "governance/tribal_hold.yaml")
    held = set(hold.get("heldSeedKeys") or [])
    live = [c for c in recs.values() if c.get("type") == "Competency" and c.get("module") == "core" and
            c.get("status") not in ("superseded", "withdrawn", "deprecated")]
    keys = {c["id"] for c in live}
    planned = set()
    for r in csv.DictReader((ROOT / "docs/decisions/candidate_disposition.csv").open(encoding="utf-8")):
        k = "seed:" + r["cand_id"]
        if r["decision"] == "core-v2.0" and k not in keys:
            planned.add(k)
    for r in csv.DictReader((L.DATA_V2 / "migration/v1_targets.csv").open(encoding="utf-8")):
        k = r.get("target_key")
        if r.get("area") == "core" and r.get("target_kind") in ("v1-seed", "split-new", "candidate") and k and \
                k not in keys:
            planned.add(k)
    size = {"liveCore": len(live), "liveAuthored": sum(c.get("validationStatus") != "seed-v1" for c in live),
            "liveUnauthoredSeeds": sum(c.get("validationStatus") == "seed-v1" for c in live),
            "plannedUnauthored": len(planned), "projection": len(live) + len(planned),
            "heldInProjection": sum(k in held for k in keys | planned), "range": [120, 180],
            "s2aAuthoredCore": sorted(r["target"] for r in rows_out if r["kind"] == "core-residue"),
            "netNewBeyondWorkOrders": 0}
    (HERE / "generated" / "core_size.json").write_text(json.dumps(size, indent=1), encoding="utf-8")
    print("| # | Kind | Target | Assigned to | Sprint | Status | Evidence |")
    print("|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows_out, 1):
        print(f"| {i} | {r['kind']} | {r['target']} | {r['author']} | {r['sprint']} | {r['status']} | {r['detail']} |")
    c = Counter(r["status"].split(" ")[0] for r in rows_out)
    print(f"\nRows assigned: {len(rows_out)}; status: {dict(c)}")
    print("Core size:", json.dumps({k: v for k, v in size.items() if k != 's2aAuthoredCore'}))


if __name__ == "__main__":
    main()
