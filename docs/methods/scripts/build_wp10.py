#!/usr/bin/env python3
"""Build the WP-10 L5 seed (instruments, driver events, change signals, watch items, external assessments).

Run: python3 -I docs/methods/scripts/build_wp10.py   (from the repo root; -I is safe because imports are by path)
Deterministic. Writes only under data/v2/signals/, data/v2/assessments/external/ and docs/methods/generated/.
Counts are generated into docs/methods/generated/wp10_counts.json; no count is typed anywhere.
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from wp10_common import ROOT, write_jsonl  # noqa: E402
import wp10_registry  # noqa: E402

OPTIONAL = ["wp10_signals", "wp10_watch", "wp10_external"]


def main():
    counts = {}
    instruments, events, disposition = wp10_registry.build()
    write_jsonl("data/v2/signals/registry/instruments.jsonl", instruments)
    by_year = {}
    for e in events:
        by_year.setdefault(e["eventDate"][:4], []).append(e)
    for y, evs in by_year.items():
        write_jsonl("data/v2/signals/events/%s.jsonl" % y, evs)
    counts["Instrument"] = len(instruments)
    counts["DriverEvent"] = len(events)
    counts["Instrument_held_tribal"] = sum(1 for r in instruments if r.get("indigenousDataFlag"))
    counts["DriverEvent_held_tribal"] = sum(1 for r in events if r.get("indigenousDataFlag"))
    gen = os.path.join(ROOT, "docs/methods/generated")
    os.makedirs(gen, exist_ok=True)
    with open(os.path.join(gen, "sc_instrument_disposition.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sc_instrument_id", "wp10_record", "disposition", "label_or_reason"])
        for row in sorted(disposition, key=lambda r: (r[0] == "", r[0], r[1])):
            w.writerow(row)
    for modname in OPTIONAL:
        try:
            mod = __import__(modname)
        except ImportError:
            continue
        for k, v in mod.build().items():
            counts[k] = counts.get(k, 0) + v
    with open(os.path.join(gen, "wp10_counts.json"), "w", encoding="utf-8") as f:
        json.dump({"generated_by": "docs/methods/scripts/build_wp10.py", "counts": dict(sorted(counts.items()))}, f, indent=1, sort_keys=True)
        f.write("\n")
    print(json.dumps(counts, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
