#!/usr/bin/env python3
"""Inter-coder agreement for X2 (ADR-0022: kappa >= 0.6 on match type).

Usage: python pipelines/x2/kappa.py coding/coder-a.csv coding/coder-b.csv [--out work/x2_kappa.json]
Reports Cohen's kappa on the 5-category match type {close, broad, narrow, related, none} and on the binary
any-match vs none, with bootstrap 95% CIs, plus exact agreement on the chosen O*NET task. If only one coder file
exists, it reports that kappa is not computable (it never substitutes a ranker or a second look by the same coder).
Coder types are read from coder_id: `emstagent:` IDs are agents (reported as agent agreement), `pid:` are humans.
Licence: Apache-2.0.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from collections import Counter
from pathlib import Path

CAT = {"skos:closeMatch": "close", "skos:broadMatch": "broad", "skos:narrowMatch": "narrow",
       "skos:relatedMatch": "related"}


def cat(row):
    return "none" if row["object_id"] == "NoTermFound" else CAT[row["predicate"]]


def cohen(a, b):
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb.get(k, 0) for k in ca) / (n * n)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def boot(a, b, fn, n=2000, seed=20261023):
    rng = random.Random(seed)
    idx = list(range(len(a)))
    vals = []
    for _ in range(n):
        s = [rng.choice(idx) for _ in idx]
        v = fn([a[i] for i in s], [b[i] for i in s])
        if v is not None:
            vals.append(v)
    vals.sort()
    return [round(vals[int(0.025 * len(vals))], 3), round(vals[int(0.975 * len(vals)) - 1], 3)] if vals else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("coder_a")
    ap.add_argument("coder_b", nargs="?")
    ap.add_argument("--out")
    x = ap.parse_args()
    A = {r["unit_id"]: r for r in csv.DictReader(open(x.coder_a, encoding="utf-8"))}
    res = {"units_coder_a": len(A), "coder_a_distribution": dict(Counter(cat(r) for r in A.values()))}
    if not x.coder_b or not Path(x.coder_b).exists():
        res["kappa_match_type"] = None
        res["status"] = "not computable: one coder only; a second blind coder pass is required (CODING_PROTOCOL.md §4)"
    else:
        B = {r["unit_id"]: r for r in csv.DictReader(open(x.coder_b, encoding="utf-8"))}
        units = sorted(set(A) & set(B))
        a5 = [cat(A[u]) for u in units]
        b5 = [cat(B[u]) for u in units]
        a2 = ["none" if v == "none" else "match" for v in a5]
        b2 = ["none" if v == "none" else "match" for v in b5]
        both = [u for u in units if A[u]["object_id"] != "NoTermFound" and B[u]["object_id"] != "NoTermFound"]
        types = {("agent" if r["coder_id"].startswith("emstagent:") else "human") for r in list(A.values())[:1] + list(B.values())[:1]}
        res.update({
            "units_both": len(units),
            "coder_types": sorted(types),
            "agreement_label": "agent agreement (not human reliability)" if types == {"agent"} else "inter-coder agreement",
            "kappa_match_type": round(cohen(a5, b5), 3), "kappa_match_type_ci95": boot(a5, b5, cohen),
            "kappa_any_vs_none": round(cohen(a2, b2), 3), "kappa_any_vs_none_ci95": boot(a2, b2, cohen),
            "exact_object_agreement_when_both_matched": round(sum(A[u]["object_id"] == B[u]["object_id"] for u in both) / len(both), 3) if both else None,
            "coder_b_distribution": dict(Counter(b5)),
            "target_kappa": 0.6,
        })
    s = json.dumps(res, indent=1)
    print(s)
    if x.out:
        Path(x.out).write_text(s + "\n")


if __name__ == "__main__":
    main()
