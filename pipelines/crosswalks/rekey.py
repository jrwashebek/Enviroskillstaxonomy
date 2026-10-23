#!/usr/bin/env python3
"""Re-key WP-09 crosswalk subjects/objects when WP-08 (or minting) changes role or variant IDs (CR-IA-001).

Usage: python pipelines/crosswalks/rekey.py MAP.csv [--dry-run]
MAP.csv has columns `old,new` (e.g. `seed:R11-environmental-permit-writer/state,seed:fh-r11-state`).
Rewrites `subject_id` and `object_id` in every non-X1 `*.sssom.tsv` under data/v2/crosswalks and every
`emstMapping.roleVariant` in data/v2/registers/state_classes/*.yaml. Prints a generated change count.
Licence: Apache-2.0.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sssomlib as S  # noqa: E402


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    dry = "--dry-run" in sys.argv
    m = {r["old"]: r["new"] for r in csv.DictReader(open(sys.argv[1], encoding="utf-8"))}
    changed = 0
    for tsv in sorted(S.XW.rglob("*.sssom.tsv")):
        if tsv.parent.name == "emst-v1":
            continue
        lines = tsv.read_text(encoding="utf-8").splitlines()
        head = lines[0].split("\t")
        idx = [head.index(c) for c in ("subject_id", "object_id") if c in head]
        out = [lines[0]]
        for ln in lines[1:]:
            cells = ln.split("\t")
            for i in idx:
                if cells[i] in m:
                    cells[i] = m[cells[i]]
                    changed += 1
            out.append("\t".join(cells))
        if not dry:
            tsv.write_text("\n".join(out) + "\n", encoding="utf-8")
    reg = S.L.DATA_V2 / "registers" / "state_classes"
    for y in sorted(reg.glob("*.yaml")) if reg.exists() else []:
        rec = S.L.load_yaml(y)
        maps = rec.get("emstMapping") or []
        hit = False
        for mm in maps if isinstance(maps, list) else [maps]:
            if mm.get("roleVariant") in m:
                mm["roleVariant"] = m[mm["roleVariant"]]
                changed += 1
                hit = True
        if hit and not dry:
            S.L.write_yaml(y, rec)
    print(f"{'would change' if dry else 'changed'} {changed} references")


if __name__ == "__main__":
    main()
