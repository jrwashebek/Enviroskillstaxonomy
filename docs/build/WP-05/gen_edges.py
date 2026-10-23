#!/usr/bin/env python3
"""Generate WP-05's draft task-level sensitivity edges (task -> mechanism -> L5 instrument) until the schema can hold
them on Task (CR-SC-001 item 1). Licence: Apache-2.0.

Edges are DRAFT assertions: each primary task of a WP-05 competency inherits that competency's mechanism edges
(instrumentSensitivity), and is linked to every registered instrument that (a) is a characteristic instrument of
one of the competency's actor enactments and (b) shares the mechanism. Unregistered instruments are listed by name
in instruments_to_register.csv. Output: generated/task_sensitivity_edges.csv.
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import emstlib as L  # noqa: E402


def main():
    written = set(json.loads((HERE / "generated" / "wp05_written.json").read_text())["records"])
    comps, tasks, enas = {}, [], []
    for loc, rec in L.iter_records(L.DATA_V2):
        if not isinstance(rec, dict) or rec.get("id") not in written:
            continue
        t = rec.get("type")
        if t == "Competency":
            comps[rec["id"]] = rec
        elif t == "Task":
            tasks.append(rec)
        elif t == "Enactment":
            enas.append(rec)
    ins_mech = {}
    for line in (L.DATA_V2 / "instruments" / "instruments.jsonl").read_text(encoding="utf-8").splitlines():
        d = json.loads(line)
        ins_mech[d["id"]] = set(d["mechanisms"])
    by_comp_ins = {}
    for e in enas:
        by_comp_ins.setdefault(e["competency"], set()).update(e.get("characteristicInstruments") or [])
    pending = {}
    with (HERE / "instruments_to_register.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            for m in r["mechanism"].split("|"):
                pending.setdefault((r["competency"], m), []).append(r["instrument_name"])
    rows = []
    for t in sorted(tasks, key=lambda x: x["id"]):
        prim = [s["competency"] for s in t["supports"] if s["strength"] == "primary"]
        for cid in prim:
            c = comps.get(cid)
            if not c:
                continue
            for edge in c.get("instrumentSensitivity") or []:
                m = edge["mechanism"]
                linked = sorted(i for i in by_comp_ins.get(cid, ()) if m in ins_mech.get(i, set()))
                rows.append({"task": t["id"], "competency": cid, "mechanism": m,
                             "instruments_registered": "|".join(linked),
                             "instruments_to_register": "|".join(pending.get((cid, m), [])),
                             "evidenceLabel": edge["evidenceLabel"], "sources": "|".join(edge.get("sources") or []),
                             "assertion": "inherited-draft (competency edge applied to task; per-task review pending)",
                             "reviewBy": "2027-01-31"})
    out = HERE / "generated" / "task_sensitivity_edges.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} edges; {sum(1 for r in rows if r['instruments_registered'])} with a registered instrument -> {out}")


if __name__ == "__main__":
    main()
