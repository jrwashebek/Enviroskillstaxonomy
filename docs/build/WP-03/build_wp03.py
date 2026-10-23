#!/usr/bin/env python3
"""Build WP-03 (Field Craft) records from the authored specs in docs/build/WP-03/src/.

Usage: python3 docs/build/WP-03/build_wp03.py [--only g1_assess,g2_datafield]
Writes YAML records under data/v2/core/{competencies,tasks,indicators,enactments}/ and a manifest of every file it
wrote (docs/build/WP-03/manifest.csv). Re-running is idempotent: records are regenerated from the specs, and v1
seed fields (id, notation, legacy facets, lineage) are read from the original seed on first edit and preserved in a
cache (docs/build/WP-03/.seed_cache/) so later runs never lose them.
"""
from __future__ import annotations

import argparse
import csv
import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))
import wp03lib as W  # noqa: E402

L = W.L
CACHE = HERE / ".seed_cache"
GROUPS = ["g1_assess", "g2_datafield", "g3_build", "g4_safety_ops", "g5_people", "g6_enactments"]


def original(path: Path):
    """The v1 seed as migrated (cached the first time WP-03 touches it)."""
    CACHE.mkdir(exist_ok=True)
    c = CACHE / (path.parent.name + "__" + path.name)
    if c.exists():
        return L.load_yaml(c)
    if not path.exists():
        return None
    rec = L.load_yaml(path)
    if rec.get("validationStatus") == "seed-v1" or rec.get("provenance", {}).get("method") == "v1-migration":
        c.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        return rec
    return None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    args = ap.parse_args(argv)
    groups = [g for g in GROUPS if not args.only or g in args.only.split(",")]
    written = []
    for g in groups:
        try:
            mod = importlib.import_module(g)
        except ModuleNotFoundError:
            continue
        for c in getattr(mod, "COMPS", []):
            cpath = W.comp_path(c["id"])
            cexist = original(cpath)
            alias = {}
            for t in c["tasks"]:
                if t["alias"]:
                    alias[t["alias"]] = t["id"]
            for t in c["tasks"]:
                tpath = W.task_path(t["id"])
                texist = original(tpath)
                if t["repoint_only"]:
                    rec = W.repoint_task(texist, t["supports"], t["note"])
                else:
                    rec = W.build_task(t, c, texist)
                L.write_yaml(tpath, rec)
                written.append(("Task", rec["id"], c["id"], str(tpath.relative_to(L.ROOT))))
            ind_ids = {}
            for lv in W.LEVELS:
                for n, i in enumerate(c["levels"].get(lv, [])):
                    rec = W.build_indicator(c, lv, "abcdefg"[n], i, alias)
                    ipath = W.ind_path(rec["id"])
                    L.write_yaml(ipath, rec)
                    ind_ids.setdefault(lv, []).append(rec["id"])
                    written.append(("Indicator", rec["id"], c["id"], str(ipath.relative_to(L.ROOT))))
            rec = W.build_competency(c, cexist, ind_ids)
            L.write_yaml(cpath, rec)
            written.append(("Competency", rec["id"], c["id"], str(cpath.relative_to(L.ROOT))))
        for tid, supports, note in getattr(mod, "REPOINTS", []):
            tpath = W.task_path(tid)
            texist = original(tpath)
            rec = W.repoint_task(texist, supports, note)
            if rec is None:
                print(f"skip repoint {tid}: no longer a v1 seed (another lane edited it)")
                continue
            L.write_yaml(tpath, rec)
            written.append(("Task", tid, "repoint", str(tpath.relative_to(L.ROOT))))
        for builder in getattr(mod, "EXTRA", []):
            for kind, rec, path in builder():
                L.write_yaml(path, rec)
                written.append((kind, rec["id"], rec.get("competency", ""), str(path.relative_to(L.ROOT))))
    man = HERE / "manifest.csv"
    old = []
    if man.exists() and args.only:
        with open(man, encoding="utf-8") as fh:
            old = [r for r in csv.DictReader(fh) if r["group"] not in groups]
    rows = old + [{"group": g, "type": k, "id": i, "parent": p, "path": pa} for g in groups for (k, i, p, pa) in []]
    # rebuild per group for clarity
    rows = old
    gi = 0
    for k, i, p, pa in written:
        rows.append({"group": "", "type": k, "id": i, "parent": p, "path": pa})
    with open(man, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["group", "type", "id", "parent", "path"])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(written)} records from groups {groups}")


if __name__ == "__main__":
    main()
