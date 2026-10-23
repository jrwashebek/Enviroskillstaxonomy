#!/usr/bin/env python3
"""Write the plan-level OpenLMP extract that build_figures.py uses for F05 and F06.

Review-fix pass (Fix-A), EMST v2, 2026-10-23. Licence of this script: Apache-2.0. The extract is
derived from OpenLMP 0.1.0 (CC0-1.0) and is released CC0-1.0.

Why it exists: the independent evidence review (docs/review/evidence_review.md, R80 and section 5)
asked for (a) a sensitivity check on the plan-monitoring comparison that drops monitoring-report
files and plans with no extracted monitoring components, and (b) confidence intervals for the
plan-content rates that cannot go below zero. Both need per-plan values, which the L5 signal
records (data/v2/signals/2026/openlmp.jsonl) do not hold. This script writes those per-plan
values once, from the corpus on disk, so that build_figures.py can stay byte-reproducible from
repository files alone.

Definitions are copied verbatim from docs/methods/scripts/wp10_lmp.py (TERMS, TOUCHPOINTS, the
era mapping and the "non-empty plan" rule). build_figures.py fails unless the plan-equal means
recomputed from this extract equal the values stored in openlmp.jsonl.

Tribal and Indigenous terms and touchpoints are not extracted (quarantined under ADR-0007 until
a Tribal Advisory Council decides how they are shown).

Run (reads the corpus read-only; default path as in wp10_lmp.py):
    python3 -I docs/package/report/figures/extract_openlmp_plans.py [/path/to/lmps]
"""
import csv
import glob
import os
import re
import sys
from collections import Counter, defaultdict

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "openlmp_plan_level_extract.csv")
LMPS = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/lmps"
csv.field_size_limit(10 ** 9)

ERA = {"usfs-1982-rule": "1982-rule", "usfs-2012-rule": "2012-rule"}
TERMS = {  # identical to wp10_lmp.py TERMS (Tribal term excluded here)
    "climate_change": r"climate change|changing climate|climate adaptation",
    "carbon": r"\bcarbon\b|sequestration",
    "at_risk_species_scc": r"species of conservation concern|at-risk species",
    "partnership_collaboration": r"partner|collaborat|shared stewardship|good neighbor|all[- ]lands",
    "data_or_models": r"\bdata\b|\bmodel",
    "remote_sensing_lidar_drone": r"remote sens|satellite|imagery|lidar|drone|unmanned aerial",
}
TERMS = {k: re.compile(v, re.I) for k, v in TERMS.items()}
TOUCHPOINTS = ["partnership", "cross_boundary", "state_agency"]  # the three charted in F06

# Document kind, from the catalog title. A monitoring report evaluates monitoring results; a
# monitoring plan or programme is a stand-alone monitoring document. Everything else is "plan".
RX_REPORT = re.compile(r"monitoring (and evaluation |evaluation )?report|evaluation report|\bBMER\b|"
                       r"evaluation of monitoring information|monitoring report announcement", re.I)
RX_MONPLAN = re.compile(r"monitoring (implementation )?plan\b|monitoring program", re.I)


def doc_kind(title):
    if RX_REPORT.search(title or ""):
        return "monitoring_report"
    if RX_MONPLAN.search(title or "") and not re.search(r"chapter|implementation direction", title or "", re.I):
        return "monitoring_plan"
    return "plan"


def main():
    plans = {r["plan_id"]: r for r in csv.DictReader(open(os.path.join(LMPS, "catalog/plans.csv"), newline="", encoding="utf-8"))}
    per = defaultdict(lambda: {"n": 0, "mon": 0, "terms": Counter(), "tp": Counter()})
    era_of = {}
    for f in sorted(glob.glob(os.path.join(LMPS, "plans/*/*/*/components.csv"))):
        with open(f, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                er = ERA.get(r["framework"])
                if er is None:
                    continue
                pid = r["plan_id"]
                era_of[pid] = er
                p = per[pid]
                p["n"] += 1
                text = r["text"] or ""
                if (r["component_type"] or "") == "monitoring":
                    p["mon"] += 1
                for k, rx in TERMS.items():
                    if rx.search(text):
                        p["terms"][k] += 1
                for c in [c for c in (r["coordination"] or "").split(";") if c]:
                    if c in TOUCHPOINTS:
                        p["tp"][c] += 1
    hdr = ["plan_id", "rule", "plan_year", "record_type", "doc_kind", "title", "n_components", "n_monitoring"] + \
          [f"term_{k}" for k in TERMS] + [f"touchpoint_{k}" for k in TOUCHPOINTS]
    rows = []
    for pid in sorted(era_of):
        p = per[pid]
        if p["n"] == 0:
            continue
        cat = plans.get(pid, {})
        row = {"plan_id": pid, "rule": era_of[pid], "plan_year": cat.get("plan_year", ""), "record_type": cat.get("record_type", ""),
               "doc_kind": doc_kind(cat.get("title", "")), "title": cat.get("title", ""), "n_components": p["n"], "n_monitoring": p["mon"]}
        for k in TERMS:
            row[f"term_{k}"] = p["terms"][k]
        for k in TOUCHPOINTS:
            row[f"touchpoint_{k}"] = p["tp"][k]
        rows.append(row)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=hdr, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"extract_openlmp_plans: wrote {len(rows)} plans to {OUT}")


if __name__ == "__main__":
    main()
