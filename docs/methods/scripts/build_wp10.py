#!/usr/bin/env python3
"""Build the WP-10 L5 seed (instruments, driver events, change signals, watch items, external assessments).

Run: python3 -I docs/methods/scripts/build_wp10.py   (from the repo root; -I is safe because imports are by path)
Deterministic. Layout follows docs/standard/AUTHORING_GUIDE.md s2 (DE): ChangeSignal -> data/v2/signals/<yyyy>/;
Instrument -> data/v2/instruments/; DriverEvent -> data/v2/events/<yyyy>.jsonl; WatchItem -> data/v2/core/watch-items/;
external-index ExposureAssessments are STAGED in docs/methods/staging/ until CR-LM-002 lets the schema express their
occupation/role grain. Counts are generated into docs/methods/generated/wp10_counts.json; no count is typed anywhere.
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


def promote_external():
    """After CR-LM-002 is accepted: copy staged external-index assessments into the validated tree."""
    import shutil
    src = os.path.join(ROOT, "docs/methods/staging/assessments-external")
    dst = os.path.join(ROOT, "data/v2/assessments/external")
    for dirpath, _, files in os.walk(src):
        for fn in files:
            if fn.endswith(".jsonl"):
                rel = os.path.relpath(os.path.join(dirpath, fn), src)
                os.makedirs(os.path.dirname(os.path.join(dst, rel)), exist_ok=True)
                shutil.copyfile(os.path.join(dirpath, fn), os.path.join(dst, rel))
                print("promoted", rel)


def main():
    if "--promote-external" in sys.argv:
        promote_external()
        return
    counts = {}
    instruments, events, disposition = wp10_registry.build()
    write_jsonl("data/v2/instruments/instruments.jsonl", instruments)
    by_year = {}
    for e in events:
        by_year.setdefault(e["eventDate"][:4], []).append(e)
    for y, evs in by_year.items():
        write_jsonl("data/v2/events/%s.jsonl" % y, evs)
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
    fam, files = {}, {}
    sig_root = os.path.join(ROOT, "data/v2/signals")
    for dirpath, _, fns in os.walk(sig_root):
        for fn in sorted(fns):
            if not fn.endswith(".jsonl"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), ROOT)
            for line in open(os.path.join(dirpath, fn), encoding="utf-8"):
                if not line.strip():
                    continue
                r = json.loads(line)
                files[rel] = files.get(rel, 0) + 1
                f_ = next((n["value"] for n in r.get("notation", []) if n["scheme"] == "EMST-signalFamily"), "unset")
                fam[f_] = fam.get(f_, 0) + 1
    with open(os.path.join(gen, "wp10_counts.json"), "w", encoding="utf-8") as f:
        json.dump({"generated_by": "docs/methods/scripts/build_wp10.py", "counts": dict(sorted(counts.items())),
                   "ChangeSignal_by_family": dict(sorted(fam.items())), "ChangeSignal_by_file": dict(sorted(files.items()))},
                  f, indent=1, sort_keys=True)
        f.write("\n")
    print(json.dumps(counts, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
