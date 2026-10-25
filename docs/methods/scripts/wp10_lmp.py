"""Plan-requirement aggregates from OpenLMP for WP-10 standing demand signals (ADR-0028 s4).

Headline series weight EACH PLAN EQUALLY (component shares and rates normalized within plan, then averaged
across plans); the component-weighted value is kept alongside as the sensitivity check ADR-0028 requires
(Idaho Panhandle 2022 alone supplies ~29% of monitoring components). Read-only on /home/claude/lmps.
Term and touchpoint definitions are reused verbatim from LM's Phase 2 script so the two passes are comparable.

Interval method (CR-FIX-A-003 item 2, ADR-0031 §4; ported 2026-10-24 by the rc.1 alignment editor under the LM code):
for the 1982-rule and 2012-rule eras every plan-equal value also gets a plan-level percentile bootstrap interval
(10,000 resamples, seed 20261023), computed exactly as in Fix-A's seeded build
(docs/package/report/figures/build_figures.py, f5_f6: same document order, same resample stream, same variant order).
The bootstrap also gives the document-type sensitivity (plan documents only), which needs the document kind; doc_kind()
is copied verbatim from docs/package/report/figures/extract_openlmp_plans.py. The normal-approximation `ci95` is kept
in the output only for the state era and for the held Tribal touchpoint, which Fix-A's build did not re-compute.
"""
import csv
import glob
import math
import os
import random
import re
import statistics
from collections import Counter, defaultdict

LMPS = "/home/claude/lmps"
csv.field_size_limit(10 ** 9)

BOOT_SEED = 20261023
BOOT_RESAMPLES = 10000
BOOT_METHOD = "plan-level percentile bootstrap over documents, 10,000 resamples, seed 20261023"
BOOT_ERAS = ("1982-rule", "2012-rule")
# Variant order fixes the random stream and must match build_figures.py f5_f6 (all, no_monitoring_reports,
# plans_only, ...). Only the first three are needed here; later variants draw after them and cannot change them.
BOOT_VARIANTS = [
    ("all", lambda kind: True),
    ("no_monitoring_reports", lambda kind: kind != "monitoring_report"),
    ("plans_only", lambda kind: kind == "plan"),
]

# Document kind, from the catalog title (verbatim from extract_openlmp_plans.py). A monitoring report evaluates
# monitoring results; a monitoring plan or programme is a stand-alone monitoring document. Everything else is "plan".
RX_REPORT = re.compile(r"monitoring (and evaluation |evaluation )?report|evaluation report|\bBMER\b|"
                       r"evaluation of monitoring information|monitoring report announcement", re.I)
RX_MONPLAN = re.compile(r"monitoring (implementation )?plan\b|monitoring program", re.I)


def doc_kind(title):
    if RX_REPORT.search(title or ""):
        return "monitoring_report"
    if RX_MONPLAN.search(title or "") and not re.search(r"chapter|implementation direction", title or "", re.I):
        return "monitoring_plan"
    return "plan"


def _resamples(n, rng, b=BOOT_RESAMPLES):
    return [[int(rng.random() * n) for _ in range(n)] for _ in range(b)]


def _boot_ci(values, idx_sets):
    """Percentile bootstrap 95% interval of the mean over pre-drawn index sets (as build_figures.boot_ci)."""
    means = sorted(sum(values[i] for i in s) / len(s) for s in idx_sets)
    b = len(means)
    return means[int(0.025 * b)], means[int(0.975 * b) - 1]


def overlap(a, b):
    """True when two [low, high] intervals overlap (as build_figures.overlap, on the rounded bounds)."""
    return max(a[0], b[0]) <= min(a[1], b[1])

ERA = {"usfs-1982-rule": "1982-rule", "usfs-2012-rule": "2012-rule", "state-framework": "state", "other": "other"}

TERMS = {  # identical regexes to docs/research/labor-market-ai-impact/scripts/lmp_demand_signals.py ERA_TERMS
    "climate_change": r"climate change|changing climate|climate adaptation",
    "carbon": r"\bcarbon\b|sequestration",
    "at_risk_species_scc": r"species of conservation concern|at-risk species",
    "partnership_collaboration": r"partner|collaborat|shared stewardship|good neighbor|all[- ]lands",
    "data_or_models": r"\bdata\b|\bmodel",
    "remote_sensing_lidar_drone": r"remote sens|satellite|imagery|lidar|drone|unmanned aerial",
    "tribal_or_indigenous": r"\btribes?\b|tribal|indigenous|treaty",
}
TERMS = {k: re.compile(v, re.I) for k, v in TERMS.items()}
TOUCHPOINTS = ["partnership", "cross_boundary", "state_agency", "state_local", "federal_agency", "tribal",
               "esa_consultation", "special_use_authorization", "grazing_authorization"]


def _mean_ci(xs):
    n = len(xs)
    if n == 0:
        return None, None, 0
    m = statistics.fmean(xs)
    if n < 2:
        return m, None, n
    se = statistics.stdev(xs) / math.sqrt(n)
    return m, [round(m - 1.96 * se, 4), round(m + 1.96 * se, 4)], n


def compute():
    plans = {r["plan_id"]: r for r in csv.DictReader(open(os.path.join(LMPS, "catalog/plans.csv"), newline="", encoding="utf-8"))}
    per_plan = defaultdict(lambda: {"n": 0, "mon": 0, "terms": Counter(), "tp": Counter()})
    era_of, year_of = {}, {}
    comp_tot = Counter()
    comp_mon = Counter()
    comp_terms = defaultdict(Counter)
    comp_tp = defaultdict(Counter)
    for f in sorted(glob.glob(os.path.join(LMPS, "plans/*/*/*/components.csv"))):
        with open(f, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                pid = r["plan_id"]
                er = ERA.get(r["framework"], "other")
                era_of[pid] = er
                y = (plans.get(pid) or {}).get("plan_year") or r.get("plan_year") or ""
                if y[:4].isdigit():
                    year_of[pid] = int(y[:4])
                p = per_plan[pid]
                p["n"] += 1
                comp_tot[er] += 1
                text = r["text"] or ""
                if (r["component_type"] or "") == "monitoring":
                    p["mon"] += 1
                    comp_mon[er] += 1
                for k, rx in TERMS.items():
                    if rx.search(text):
                        p["terms"][k] += 1
                        comp_terms[er][k] += 1
                for c in [c for c in (r["coordination"] or "").split(";") if c]:
                    if c in TOUCHPOINTS:
                        p["tp"][c] += 1
                        comp_tp[er][c] += 1
    out = {"eras": {}}
    for er in ["1982-rule", "2012-rule", "state"]:
        pids = sorted(pid for pid, e in era_of.items() if e == er and per_plan[pid]["n"] > 0)
        years = sorted(year_of[p] for p in pids if p in year_of)
        e = {"n_plans": len(pids), "n_components": comp_tot[er],
             "years": [years[0], years[-1]] if years else None}
        mon_shares = [per_plan[p]["mon"] / per_plan[p]["n"] for p in pids]
        m, ci, n = _mean_ci(mon_shares)
        e["monitoring_share_plan_equal"] = {"value": round(m, 4) if m is not None else None, "ci95": ci, "n": n,
                                            "median": round(statistics.median(mon_shares), 4) if mon_shares else None}
        e["monitoring_share_component_weighted"] = round(comp_mon[er] / comp_tot[er], 4) if comp_tot[er] else None
        e["terms_per_1000_plan_equal"] = {}
        e["terms_per_1000_component_weighted"] = {}
        for k in TERMS:
            xs = [1000 * per_plan[p]["terms"][k] / per_plan[p]["n"] for p in pids]
            m, ci, n = _mean_ci(xs)
            e["terms_per_1000_plan_equal"][k] = {"value": round(m, 2), "ci95": [round(c, 2) for c in ci] if ci else None, "n": n}
            e["terms_per_1000_component_weighted"][k] = round(1000 * comp_terms[er][k] / comp_tot[er], 2) if comp_tot[er] else None
        e["touchpoints_per_1000_plan_equal"] = {}
        e["touchpoints_per_1000_component_weighted"] = {}
        for k in TOUCHPOINTS:
            xs = [1000 * per_plan[p]["tp"][k] / per_plan[p]["n"] for p in pids]
            m, ci, n = _mean_ci(xs)
            e["touchpoints_per_1000_plan_equal"][k] = {"value": round(m, 2), "ci95": [round(c, 2) for c in ci] if ci else None, "n": n}
            e["touchpoints_per_1000_component_weighted"][k] = round(1000 * comp_tp[er][k] / comp_tot[er], 2) if comp_tot[er] else None
        out["eras"][er] = e
    # Plan-level percentile bootstrap (CR-FIX-A-003 item 2). Index sets are drawn once per (variant, era), in
    # build_figures.py's order, and shared by every measure, so the intervals equal Fix-A's F05 and F06 values.
    kind_of = {pid: doc_kind((plans.get(pid) or {}).get("title", "")) for pid in era_of}
    rng = random.Random(BOOT_SEED)
    sub, idx = {}, {}
    for vid, keep in BOOT_VARIANTS:
        for er in BOOT_ERAS:
            sub[(vid, er)] = [pid for pid in sorted(p for p, e_ in era_of.items() if e_ == er and per_plan[p]["n"] > 0)
                              if keep(kind_of[pid])]
            idx[(vid, er)] = _resamples(len(sub[(vid, er)]), rng)

    def bstat(vid, er, fn, nd):
        v = [fn(per_plan[p]) for p in sub[(vid, er)]]
        lo, hi = _boot_ci(v, idx[(vid, er)])
        return {"value": round(statistics.fmean(v), nd), "ci95": [round(lo, nd), round(hi, nd)], "n": len(v)}

    for er in BOOT_ERAS:
        e = out["eras"][er]
        bs = {"method": BOOT_METHOD,
              "doc_kinds": dict(sorted(Counter(kind_of[p] for p in sub[("all", er)]).items())),
              "monitoring_share": {}, "terms_per_1000": {k: {} for k in TERMS},
              "touchpoints_per_1000": {k: {} for k in TOUCHPOINTS}}
        for vid in ("all", "plans_only"):
            bs["monitoring_share"][vid] = bstat(vid, er, lambda p: 1.0 * p["mon"] / p["n"], 4)
            for k in TERMS:
                bs["terms_per_1000"][k][vid] = bstat(vid, er, lambda p, k=k: 1000.0 * p["terms"][k] / p["n"], 2)
            for k in TOUCHPOINTS:
                bs["touchpoints_per_1000"][k][vid] = bstat(vid, er, lambda p, k=k: 1000.0 * p["tp"][k] / p["n"], 2)
        # the bootstrap's point estimates must equal the plan-equal values above (same documents, same weighting)
        assert bs["monitoring_share"]["all"]["value"] == e["monitoring_share_plan_equal"]["value"], er
        assert all(bs["terms_per_1000"][k]["all"]["value"] == e["terms_per_1000_plan_equal"][k]["value"] for k in TERMS), er
        e["bootstrap"] = bs
    out["catalog_path"] = os.path.join(LMPS, "catalog/plans.csv")
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(compute(), indent=1))
