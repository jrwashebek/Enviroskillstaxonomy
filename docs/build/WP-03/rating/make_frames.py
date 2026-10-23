#!/usr/bin/env python3
"""Make blind rating frames for the WP-03 craft-rating passes (prompt wp03-craft-rating@1).

Each frame lists a random unit code and the task statement only: no competency, domain, module, v1 code or prior
label (codebook §2, XR-01). Units are the WP-03-authored tasks in docs/build/WP-03/manifest.csv (re-point-only tasks
belong to other lanes and are excluded). A private key (unit -> task id, text hash) is written beside the frames and
is not read during rating. Licence: Apache-2.0.
"""
import csv
import hashlib
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import emstlib as L  # noqa: E402

TRIBAL = [re.compile(p, re.I) for p in [r"\btrib(e|es|al)\b", r"\bindigenous\b", r"government-to-government", r"\btreat(y|ies)\b"]]


def main():
    man = list(csv.DictReader(open(ROOT / "docs/build/WP-03/manifest.csv", encoding="utf-8")))
    tasks = []
    for r in man:
        if r["type"] != "Task" or r["parent"] == "repoint":
            continue
        rec = L.load_yaml(ROOT / r["path"])
        if not any("fc-agent" in a for a in rec["provenance"]["agent"]):
            continue
        st = rec["statement"]["en"]
        if any(rx.search(st) for rx in TRIBAL):
            continue
        tasks.append((rec["id"], st, rec["textSha256"]))
    tasks = sorted(set(tasks))
    rng = random.Random(20261023)
    codes = rng.sample(range(1000, 9999), len(tasks))
    units = {f"U{c}": t for c, t in zip(codes, tasks)}
    with open(HERE / "key_private.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["unit", "task", "taskTextSha256"])
        for u, (tid, st, h) in sorted(units.items()):
            w.writerow([u, tid, h])
    for p, seed in ((1, 11), (2, 22), (3, 33)):
        order = sorted(units)
        random.Random(seed).shuffle(order)
        with open(HERE / f"frame_pass{p}.txt", "w", encoding="utf-8") as fh:
            for u in order:
                fh.write(f"{u}\t{units[u][1]}\n")
    print(f"{len(units)} units; frames written")


if __name__ == "__main__":
    main()
