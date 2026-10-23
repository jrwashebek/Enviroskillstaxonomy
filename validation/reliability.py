#!/usr/bin/env python3
"""EMST v2 reliability statistics (WP-11 reference implementation; numpy only).

- krippendorff_alpha(data, level): Krippendorff's alpha for nominal, ordinal, interval or ratio data with missing
  values (coincidence-matrix formulation; Krippendorff 2018, IO-067; Hayes & Krippendorff 2007, IO-068).
- bootstrap_alpha(data, level, B, seed): unit-level (cluster) bootstrap; percentile 95% CI; the gate decides on
  the 2.5th percentile (display_gates.yaml#thresholds).
- panel_split_alpha(data, k, level): reliability of a k-rater consensus value, estimated by splitting raters into
  disjoint panels of k and computing alpha between panel consensus values (protocol_craft_scale_pilot.md §6).
- gate(lower_bound): production | tentative | hidden.
- agreement_result(...): builds the object display_gates.yaml#agreement_result_schema expects.

`data` is a units x raters matrix (list of lists or ndarray); missing values are None or NaN. Values must be
numeric codes; map category labels to integers before calling (for ordinal data, in scale order).
Only human raters may be passed when the result is used for the display gate; agent runs are analysed separately
(protocol_llm_coder_gate.md) and never pooled into the gate statistic.
"""
from __future__ import annotations

import itertools
import math
from typing import Sequence

import numpy as np

LEVELS = ("nominal", "ordinal", "interval", "ratio")


def _as_matrix(data) -> np.ndarray:
    arr = np.array([[np.nan if v is None else float(v) for v in row] for row in data], dtype=float)
    if arr.ndim != 2:
        raise ValueError("data must be units x raters")
    return arr


def _unit_coincidences(arr: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return (values, O) where O[u] is unit u's contribution to the coincidence matrix (pairable units only)."""
    vals = np.unique(arr[~np.isnan(arr)])
    idx = {v: i for i, v in enumerate(vals)}
    V = len(vals)
    mats = []
    for row in arr:
        r = row[~np.isnan(row)]
        m = len(r)
        if m < 2:
            continue
        counts = np.zeros(V)
        for v in r:
            counts[idx[v]] += 1
        o = (np.outer(counts, counts) - np.diag(counts)) / (m - 1)
        mats.append(o)
    O = np.array(mats) if mats else np.zeros((0, V, V))
    return vals, O


def _delta2(vals: np.ndarray, n_c: np.ndarray, level: str) -> np.ndarray:
    c = vals[:, None]
    k = vals[None, :]
    if level == "nominal":
        return (c != k).astype(float)
    if level == "interval":
        return (c - k) ** 2
    if level == "ratio":
        s = c + k
        with np.errstate(divide="ignore", invalid="ignore"):
            d = np.where(s == 0, 0.0, ((c - k) / s) ** 2)
        return d
    if level == "ordinal":
        cum = np.cumsum(n_c)
        V = len(vals)
        d = np.zeros((V, V))
        for i in range(V):
            for j in range(V):
                lo, hi = min(i, j), max(i, j)
                s = cum[hi] - (cum[lo - 1] if lo > 0 else 0.0)
                d[i, j] = (s - (n_c[i] + n_c[j]) / 2.0) ** 2
        return d
    raise ValueError(f"level must be one of {LEVELS}")


def _alpha_from_o(o: np.ndarray, vals: np.ndarray, level: str) -> float:
    n_c = o.sum(axis=1)
    n = n_c.sum()
    if n <= 1:
        return float("nan")
    d2 = _delta2(vals, n_c, level)
    d_o = (o * d2).sum() / n
    d_e = (np.outer(n_c, n_c) * d2).sum() / (n * (n - 1))
    if d_e == 0:
        return float("nan")
    return float(1.0 - d_o / d_e)


def krippendorff_alpha(data, level: str = "nominal") -> float:
    arr = _as_matrix(data)
    vals, O = _unit_coincidences(arr)
    if len(O) == 0:
        return float("nan")
    return _alpha_from_o(O.sum(axis=0), vals, level)


def bootstrap_alpha(data, level: str = "nominal", B: int = 10000, seed: int = 20261023,
                    ci: float = 0.95) -> dict:
    """Unit-level bootstrap. Returns alpha, CI bounds, B, seed and the number of pairable units."""
    arr = _as_matrix(data)
    vals, O = _unit_coincidences(arr)
    U = len(O)
    if U == 0:
        return {"alpha": float("nan"), "ciLower": float("nan"), "ciUpper": float("nan"), "B": B, "seed": seed, "nUnits": 0}
    point = _alpha_from_o(O.sum(axis=0), vals, level)
    rng = np.random.default_rng(seed)
    flat = O.reshape(U, -1)
    draws = rng.multinomial(U, np.full(U, 1.0 / U), size=B)  # B x U weights
    sums = draws @ flat                                       # B x V*V
    V = len(vals)
    boots = np.array([_alpha_from_o(s.reshape(V, V), vals, level) for s in sums])
    boots = boots[~np.isnan(boots)]
    lo_q, hi_q = (1 - ci) / 2, 1 - (1 - ci) / 2
    return {"alpha": point, "ciLower": float(np.quantile(boots, lo_q)) if len(boots) else float("nan"),
            "ciUpper": float(np.quantile(boots, hi_q)) if len(boots) else float("nan"),
            "B": B, "validResamples": int(len(boots)), "seed": seed, "nUnits": U}


def _consensus(values: np.ndarray, level: str) -> float:
    v = values[~np.isnan(values)]
    if len(v) == 0:
        return float("nan")
    if level == "interval" or level == "ratio":
        return float(np.mean(v))
    if level == "ordinal":
        return float(np.median(v)) if len(v) % 2 else float(np.sort(v)[len(v) // 2 - 1])  # lower median, stays on scale
    vals, counts = np.unique(v, return_counts=True)
    top = counts.max()
    if (counts == top).sum() > 1 or top / len(v) < 2 / 3:
        return float("nan")  # no nominal consensus
    return float(vals[counts.argmax()])


def panel_split_alpha(data, k: int = 3, level: str = "ordinal", max_splits: int = 50, seed: int = 20261023) -> dict:
    """Alpha between consensus values of two disjoint k-rater panels, averaged over rater splits.
    Requires a fully or largely crossed design with >= 2k raters."""
    arr = _as_matrix(data)
    R = arr.shape[1]
    if R < 2 * k:
        raise ValueError(f"need >= {2 * k} raters for two panels of {k}")
    splits = []
    for a in itertools.combinations(range(R), k):
        rest = [r for r in range(R) if r not in a]
        for b in itertools.combinations(rest, k):
            key = tuple(sorted([a, b]))
            if key not in splits:
                splits.append(key)
    rng = np.random.default_rng(seed)
    if len(splits) > max_splits:
        splits = [splits[i] for i in rng.choice(len(splits), max_splits, replace=False)]
    alphas = []
    for a, b in splits:
        ca = np.array([_consensus(row[list(a)], level) for row in arr])
        cb = np.array([_consensus(row[list(b)], level) for row in arr])
        alphas.append(krippendorff_alpha(np.column_stack([ca, cb]), level))
    alphas = [x for x in alphas if not math.isnan(x)]
    return {"alpha": float(np.mean(alphas)) if alphas else float("nan"), "nSplits": len(alphas), "k": k, "level": level}


def gate(lower_bound: float, production: float = 0.80, tentative: float = 0.667) -> str:
    if lower_bound is None or math.isnan(lower_bound):
        return "hidden"
    if lower_bound >= production:
        return "production"
    if lower_bound >= tentative:
        return "tentative"
    return "hidden"


def agreement_result(dimension: str, codebook_version: str, level: str, data, rater_types: Sequence[str],
                     preregistration_id: str, study_id: str, study_date: str, build_commit: str,
                     blind_coding_attested: bool, B: int = 10000, seed: int = 20261023, strata: dict | None = None) -> dict:
    """Build the agreement-result object for display_gates.yaml from a HUMAN units x raters matrix.
    `strata` maps (key, value) -> list of row indices."""
    arr = _as_matrix(data)
    bs = bootstrap_alpha(arr, level, B, seed)
    pairable = (~np.isnan(arr)).sum(axis=1)
    raters_used = int(((~np.isnan(arr[pairable >= 2])).sum(axis=0) > 0).sum())
    out = {"dimension": dimension, "codebookVersion": codebook_version, "metric": level, "alpha": bs["alpha"],
           "ciLower": bs["ciLower"], "ciUpper": bs["ciUpper"], "bootstrapResamples": B, "seed": seed,
           "nUnits": bs["nUnits"], "nDistinctRaters": raters_used,
           "meanRatersPerUnit": float(pairable[pairable >= 2].mean()) if (pairable >= 2).any() else 0.0,
           "raterTypesCounted": sorted(set(rater_types)), "preregistrationId": preregistration_id, "studyId": study_id,
           "studyDate": study_date, "blindCodingAttested": blind_coding_attested, "ruleId": "display-gate",
           "ruleVersion": "1.0.0-draft", "buildCommit": build_commit}
    if strata:
        out["strata"] = []
        for (key, val), rows in strata.items():
            sb = bootstrap_alpha(arr[rows], level, B, seed)
            out["strata"].append({"key": key, "value": val, "nUnits": sb["nUnits"], "alpha": sb["alpha"],
                                  "ciLower": sb["ciLower"], "ciUpper": sb["ciUpper"]})
    return out
