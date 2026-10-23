#!/usr/bin/env python3
"""One-off mechanical conversion (RULINGS_FOR_DE §16.2; ADR-0030): untyped instrument links -> InstrumentLink objects.

Rewrites every string item of Enactment.characteristicInstruments and RoleVariant.instruments as {instrument: <ref>},
with no role (the role is set by SC/DB/LM; it is never defaulted). Only files that contain a string item are
rewritten, through emstlib.write_yaml. Idempotent; --check exits 1 when a file still needs converting.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emstlib as L  # noqa: E402

FIELDS = {"Enactment": "characteristicInstruments", "RoleVariant": "instruments"}


def convert(data_root: Path = L.DATA_V2, check: bool = False) -> tuple[int, int]:
    files = links = 0
    for loc, rec in L.iter_records(data_root):
        if not isinstance(rec, dict) or loc.line is not None or rec.get("type") not in FIELDS:
            continue
        field = FIELDS[rec["type"]]
        items = rec.get(field)
        if not isinstance(items, list) or not any(isinstance(x, str) for x in items):
            continue
        n = sum(1 for x in items if isinstance(x, str))
        files += 1
        links += n
        if not check:
            rec[field] = [{"instrument": x} if isinstance(x, str) else x for x in items]
            L.write_yaml(loc.path, rec)
    return files, links


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-root", type=Path, default=L.DATA_V2)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    files, links = convert(args.data_root, args.check)
    print(f"{'would convert' if args.check else 'converted'} {links} links in {files} files")
    return 1 if (args.check and files) else 0


if __name__ == "__main__":
    sys.exit(main())
