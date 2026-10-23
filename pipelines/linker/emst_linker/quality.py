"""Evaluation and error-corrected aggregation (ADR-0019 §2, §5; IO spec_gold_sets.md §6-§8).

`evaluate` computes P@1, Hit@5, MRR and abstention recall with bootstrap CIs against a gold set in the MELO-style
layout (items with acceptable label sets). `aggregate` is the ONLY way this package produces counts: it refuses to
run without a held-out evaluation (`linker_quality`) and returns misclassification-corrected shares with bootstrap
intervals over both items and gold labels, never uncorrected top-1 counts (P-IA-11).
"""
from __future__ import annotations

import math
from collections import Counter

import numpy as np

from . import config as C


class UncorrectedCountError(RuntimeError):
    pass


def wilson(k, n, z=1.96):
    if n == 0:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 3), round(c + h, 3)]


def evaluate(ranked: dict, gold: list[dict], n_boot=2000, seed=C.SEED):
    """ranked: item_id -> ranked competency IDs (empty list = abstained). gold rows: {item_id, acceptable:set,
    noise:bool, split}. Returns metrics with bootstrap CIs; noise items enter only the abstention metric."""
    rng = np.random.default_rng(seed)
    per, noise_abst = [], []
    for g in gold:
        r = ranked.get(g["item_id"], [])
        if g.get("noise"):
            noise_abst.append(1.0 if not r else 0.0)
            continue
        rel = [c in g["acceptable"] for c in r]
        first = next((i for i, x in enumerate(rel) if x), None)
        per.append({"p1": float(bool(rel) and rel[0]), "hit5": float(any(rel[:5])),
                    "rr": 0.0 if first is None else 1 / (first + 1)})
    out = {"n": len(per), "n_noise": len(noise_abst)}
    for m in ("p1", "hit5", "rr"):
        v = np.array([p[m] for p in per]) if per else np.array([0.0])
        boots = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(n_boot)]
        out[m] = {"mean": round(float(v.mean()), 3),
                  "ci95": [round(float(np.quantile(boots, .025)), 3), round(float(np.quantile(boots, .975)), 3)]}
    k = int(sum(noise_abst))
    out["noise_abstention_recall"] = {"mean": round(k / len(noise_abst), 3) if noise_abst else None,
                                      "ci95": wilson(k, len(noise_abst))}
    return out


def linker_quality(gold_set_id: str, heldout_eval: dict) -> dict:
    """The linkerQuality object every derived ChangeSignal must carry (SPEC §5.16)."""
    if heldout_eval.get("n", 0) < 1:
        raise ValueError("held-out evaluation is empty")
    return {"goldSet": gold_set_id, "precisionAt1": heldout_eval["p1"]["mean"], "ci95": heldout_eval["p1"]["ci95"]}


def aggregate(top1: list[str], confusion: dict | None, quality: dict | None, n_boot=2000, seed=C.SEED):
    """Misclassification-corrected prevalence of each competency among linked items.

    top1: fused top-1 competency per (non-abstained) item. confusion: {predicted: Counter(true)} from the held-out
    gold set (true may be 'none' for items with no acceptable competency). quality: linker_quality(...).
    Correction: P(true=c) = sum_p P(pred=p) * P(true=c | pred=p), with bootstrap over items and over the gold rows
    of each predicted class. Raises UncorrectedCountError if confusion or quality is missing.
    """
    if not quality or not confusion:
        raise UncorrectedCountError("refusing to aggregate: no held-out gold-set evaluation attached (ADR-0019 §5)")
    rng = np.random.default_rng(seed)
    preds = list(top1)
    labels = sorted({c for row in confusion.values() for c in row} | set(preds))
    gold_rows = {p: [t for t, n in cnt.items() for _ in range(n)] for p, cnt in confusion.items()}

    def corrected(sample):
        cnt = Counter(sample)
        tot = sum(cnt.values()) or 1
        est = Counter()
        for p, n in cnt.items():
            rows = gold_rows.get(p)
            if not rows:              # predicted class never seen in gold: its share is unidentified
                est["unidentified"] += n / tot
                continue
            rs = rng.choice(rows, size=len(rows), replace=True)
            for t, m in Counter(rs).items():
                est[t] += (n / tot) * (m / len(rs))
        return est

    point = corrected(preds)
    boots = [corrected(list(rng.choice(preds, size=len(preds), replace=True))) for _ in range(n_boot)]
    res = {}
    for c in sorted(set(point) | {"unidentified"}):
        v = np.array([b.get(c, 0.0) for b in boots])
        res[c] = {"share": round(float(point.get(c, 0.0)), 4),
                  "ci95": [round(float(np.quantile(v, .025)), 4), round(float(np.quantile(v, .975)), 4)]}
    return {"n_items": len(preds), "linkerQuality": quality, "correctedShares": res,
            "method": "misclassification-corrected prevalence (gold confusion matrix), bootstrap over items and gold"}
