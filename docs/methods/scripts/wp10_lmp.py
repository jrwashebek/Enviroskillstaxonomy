"""Plan-requirement aggregates from OpenLMP for WP-10 standing demand signals (ADR-0028 s4).

Headline series weight EACH PLAN EQUALLY (component shares and rates normalized within plan, then averaged
across plans); the component-weighted value is kept alongside as the sensitivity check ADR-0028 requires
(Idaho Panhandle 2022 alone supplies ~29% of monitoring components). Read-only on /home/claude/lmps.
Term and touchpoint definitions are reused verbatim from LM's Phase 2 script so the two passes are comparable.
"""
import csv
import glob
import math
import os
import re
import statistics
from collections import Counter, defaultdict

LMPS = "/home/claude/lmps"
csv.field_size_limit(10 ** 9)

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
    out["catalog_path"] = os.path.join(LMPS, "catalog/plans.csv")
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(compute(), indent=1))
