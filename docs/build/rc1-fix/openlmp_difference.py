#!/usr/bin/env python3
"""rc.1 fix pass, M6: bootstrap the 2012-rule minus 1982-rule DIFFERENCE for every OpenLMP signal (D-DATA; ADR-0032).

The stored per-era intervals come from the team's stream (Fix-A F05/F06; ADR-0031 §4 CR-FIX-A-003): random.Random
(20261023), 10,000 document resamples per (variant, era), drawn in the order variants x eras. This script re-draws
exactly that stream, checks that it reproduces every stored era value and interval, and then takes the difference of
the paired resample means (resample b of 2012 minus resample b of 1982; the two eras are resampled independently).
Intervals are percentile intervals with linear interpolation (numpy's default definition). The plans-only variant
(monitoring reports and stand-alone monitoring plans excluded) is the document-type sensitivity check the records
already describe.

Input: the OpenLMP corpus (default /home/claude/lmps; catalog SHA-256 pinned below; read-only).
Output: docs/build/rc1-fix/generated/openlmp_differences.csv (read by fix_signals.py, so the data edit does not need
the corpus). Run: python3 -I docs/build/rc1-fix/openlmp_difference.py [--lmps DIR]. Licence: Apache-2.0.
Document typing and term patterns follow the WP-10 derivation as re-implemented in the data-method review (check 7),
which reproduced every stored value and interval to the last digit.
"""
from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import json
import os
import random
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rc1lib as R  # noqa: E402

CATALOG_SHA256 = "e5cabd686e7c0bbd8c48aaeaf8d418de57f3fa313df8bb55a2f3bc27ed23b1f5"
SEED, B = 20261023, 10000
ERA = {"usfs-1982-rule": "1982-rule", "usfs-2012-rule": "2012-rule"}
TERMS = {
    "climate_change": r"climate change|changing climate|climate adaptation",
    "carbon": r"\bcarbon\b|sequestration",
    "at_risk_species_scc": r"species of conservation concern|at-risk species",
    "partnership_collaboration": r"partner|collaborat|shared stewardship|good neighbor|all[- ]lands",
    "data_or_models": r"\bdata\b|\bmodel",
    "remote_sensing_lidar_drone": r"remote sens|satellite|imagery|lidar|drone|unmanned aerial",
}
TERMS = {k: re.compile(v, re.I) for k, v in TERMS.items()}
TPS = ["partnership", "cross_boundary", "state_agency"]
RX_REPORT = re.compile(r"monitoring (and evaluation |evaluation )?report|evaluation report|\bBMER\b|"
                       r"evaluation of monitoring information|monitoring report announcement", re.I)
RX_MONPLAN = re.compile(r"monitoring (implementation )?plan\b|monitoring program", re.I)
VARIANTS = [("all", lambda d: True), ("no_monitoring_reports", lambda d: d["kind"] != "monitoring_report"),
            ("plans_only", lambda d: d["kind"] == "plan"), ("with_monitoring", lambda d: d["mon"] > 0),
            ("plans_only_with_monitoring", lambda d: d["kind"] == "plan" and d["mon"] > 0)]
COLUMNS = ["signal_id", "measure", "value_2012", "ci_2012", "n_2012", "value_1982", "ci_1982", "n_1982", "stored_match",
           "difference", "difference_ci_low", "difference_ci_high", "plans_only_difference", "plans_only_ci_low",
           "plans_only_ci_high", "plans_only_n_2012", "plans_only_n_1982"]


def doc_kind(t):
    if RX_REPORT.search(t or ""):
        return "monitoring_report"
    if RX_MONPLAN.search(t or "") and not re.search(r"chapter|implementation direction", t or "", re.I):
        return "monitoring_plan"
    return "plan"


def pct(sorted_vals, p):
    """Percentile with linear interpolation between closest ranks (numpy 'linear')."""
    k = (len(sorted_vals) - 1) * p
    f = int(k)
    c = min(f + 1, len(sorted_vals) - 1)
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


def load_docs(lmps):
    cat_path = os.path.join(lmps, "catalog/plans.csv")
    sha = hashlib.sha256(open(cat_path, "rb").read()).hexdigest()
    if sha != CATALOG_SHA256:
        raise SystemExit(f"catalog sha256 {sha} != pinned {CATALOG_SHA256}")
    csv.field_size_limit(10 ** 9)
    cat = {r["plan_id"]: r for r in csv.DictReader(open(cat_path, encoding="utf-8"))}
    per = defaultdict(lambda: {"n": 0, "mon": 0, "terms": Counter(), "tp": Counter(), "era": None})
    for f in sorted(glob.glob(os.path.join(lmps, "plans/*/*/*/components.csv"))):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            er = ERA.get(r["framework"])
            if er is None:
                continue
            p = per[r["plan_id"]]
            p["era"] = er
            p["n"] += 1
            t = r["text"] or ""
            p["mon"] += (r["component_type"] or "") == "monitoring"
            for k, rx in TERMS.items():
                p["terms"][k] += bool(rx.search(t))
            for c in (r["coordination"] or "").split(";"):
                if c in TPS:
                    p["tp"][c] += 1
    docs = [dict(pid=pid, **v, kind=doc_kind(cat.get(pid, {}).get("title", ""))) for pid, v in sorted(per.items()) if v["n"] > 0]
    return {e: [d for d in docs if d["era"] == e] for e in ("1982-rule", "2012-rule")}


def rnd(x):
    """Four significant digits, so a bound just below 0 is never printed as -0.0 (the sign decides the direction rule)."""
    return float(f"{x:.4g}")


def val(d, col):
    if col == "mon":
        return d["mon"] / d["n"]
    kind, key = col
    return 1000.0 * (d["terms"][key] if kind == "term" else d["tp"][key]) / d["n"]


def col_of(name):
    if name.startswith("monitoring_component_share"):
        return "mon"
    k, key = name.split(":")
    if key not in TERMS and key not in TPS:
        return None
    return ("term", key) if k.startswith("mentions") else ("tp", key)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lmps", default="/home/claude/lmps")
    a = ap.parse_args(argv)
    eras = load_docs(a.lmps)
    rng = random.Random(SEED)
    sub, idx = {}, {}
    for vid, keep in VARIANTS:
        for e in ("1982-rule", "2012-rule"):
            sub[(vid, e)] = [d for d in eras[e] if keep(d)]
            n = len(sub[(vid, e)])
            idx[(vid, e)] = [[int(rng.random() * n) for _ in range(n)] for _ in range(B)]

    def means(vid, e, col):
        v = [val(d, col) for d in sub[(vid, e)]]
        return statistics.fmean(v), [sum(v[i] for i in s) / len(s) for s in idx[(vid, e)]], len(v)

    rows = []
    for line in (R.L.DATA_V2 / "signals" / "2026" / "openlmp.jsonl").read_text(encoding="utf-8").splitlines():
        s = json.loads(line)
        if s.get("status") == "draft":
            continue                      # the held draft (Tribal touchpoints) is not computed or released
        m = s["measure"]
        col = col_of(m["name"])
        if col is None:
            continue
        nd = 4 if col == "mon" else 2
        v12, b12, n12 = means("all", "2012-rule", col)
        v82, b82, n82 = means("all", "1982-rule", col)
        s12, s82 = sorted(b12), sorted(b82)
        stored = (m["value"], m["ci95"][0], m["ci95"][1], m["n"], m["baseline"]["value"], m["baseline"]["ci95"][0],
                  m["baseline"]["ci95"][1], m["baseline"]["n"])
        team = (round(v12, nd), round(s12[250], nd), round(s12[9749], nd), n12,
                round(v82, nd), round(s82[250], nd), round(s82[9749], nd), n82)
        diff = sorted(x - y for x, y in zip(b12, b82))
        p12, pb12, pn12 = means("plans_only", "2012-rule", col)
        p82, pb82, pn82 = means("plans_only", "1982-rule", col)
        pdiff = sorted(x - y for x, y in zip(pb12, pb82))
        rows.append({"signal_id": s["id"], "measure": m["name"], "value_2012": team[0], "ci_2012": f"{team[1]}|{team[2]}",
                     "n_2012": n12, "value_1982": team[4], "ci_1982": f"{team[5]}|{team[6]}", "n_1982": n82,
                     "stored_match": "yes" if stored == team else "NO",
                     "difference": rnd(v12 - v82), "difference_ci_low": rnd(pct(diff, 0.025)),
                     "difference_ci_high": rnd(pct(diff, 0.975)),
                     "plans_only_difference": rnd(p12 - p82), "plans_only_ci_low": rnd(pct(pdiff, 0.025)),
                     "plans_only_ci_high": rnd(pct(pdiff, 0.975)), "plans_only_n_2012": pn12, "plans_only_n_1982": pn82})
    bad = [r["signal_id"] for r in rows if r["stored_match"] != "yes"]
    out = R.write_report("openlmp_differences.csv", R.L.csv_text(COLUMNS, rows))
    print(f"wrote {out.relative_to(R.ROOT)}: {len(rows)} signals; stored era values reproduced for {len(rows) - len(bad)}")
    for r in rows:
        print(f"  {r['signal_id']} diff {r['difference']} [{r['difference_ci_low']}, {r['difference_ci_high']}] "
              f"plans-only {r['plans_only_difference']} [{r['plans_only_ci_low']}, {r['plans_only_ci_high']}]")
    if bad:
        raise SystemExit(f"stored era values NOT reproduced for {bad}")


if __name__ == "__main__":
    main()
