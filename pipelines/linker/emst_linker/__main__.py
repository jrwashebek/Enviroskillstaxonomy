"""CLI: python -m emst_linker {link,info} ...

  link --input items.csv [--k 10] [--out links.jsonl] [--no-semantic]
       items.csv columns: item_id,text[,employer_type]. Writes candidate rows (review_status=candidate) and prints
       generated counts of items linked, quarantined and PII substitutions. Never prints per-competency counts.
  info  prints the corpus and index hashes (the linker version stamp carried by every output row).
"""
from __future__ import annotations

import argparse
import csv
import json
import sys

from . import config as C
from .link import CompetencyLinker


def main(argv=None):
    ap = argparse.ArgumentParser(prog="emst_linker")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a1 = sub.add_parser("link")
    a1.add_argument("--input", required=True)
    a1.add_argument("--out", default="-")
    a1.add_argument("--k", type=int, default=C.TOP_K)
    a1.add_argument("--no-semantic", action="store_true")
    sub.add_parser("info")
    a = ap.parse_args(argv)
    lk = CompetencyLinker(semantic="none" if getattr(a, "no_semantic", False) else None)
    if a.cmd == "info":
        print(json.dumps({**lk.version, "competencies_indexed": len(lk.comps)}, indent=1))
        return
    items = list(csv.DictReader(open(a.input, encoding="utf-8")))
    rows, q, pii = lk.link(items, a.k)
    fh = sys.stdout if a.out == "-" else open(a.out, "w", encoding="utf-8")
    for r in rows:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    if fh is not sys.stdout:
        fh.close()
    print(json.dumps({"items_in": len(items), "items_quarantined": q, "pii_substitutions": pii,
                      "candidate_rows": len(rows), **lk.version}), file=sys.stderr)


if __name__ == "__main__":
    main()
