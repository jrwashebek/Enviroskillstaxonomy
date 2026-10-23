"""Step 3: evaluate rankings against the single-annotator gold set; bootstrap CIs; per-band precision."""
import math

import numpy as np
import pandas as pd

from . import config as C


def load_gold(name="gold_set.csv", pooled_name="gold_pooled_additions.csv"):
    g = pd.read_csv(C.GOLD / name, dtype=str, keep_default_na=False)
    g["acceptable"] = g.acceptable_codes.map(lambda s: set(s.split("|")) if s else set())
    pooled = C.GOLD / pooled_name if pooled_name else None
    g["pooled"] = g["acceptable"]
    if pooled is not None and pooled.exists():
        p = pd.read_csv(pooled, dtype=str, keep_default_na=False)
        add = p.groupby("sample_id").code.apply(set).to_dict()
        g["pooled"] = g.apply(lambda r: r["acceptable"] | add.get(r["sample_id"], set()), axis=1)
    return g


def item_metrics(ranked_codes, acceptable, primary):
    rel = [c in acceptable for c in ranked_codes]
    first = next((i for i, r in enumerate(rel) if r), None)
    return {
        "p1": float(rel[0]), "primary1": float(ranked_codes[0] == primary),
        "p3": float(np.mean(rel[:3])), "hit3": float(any(rel[:3])), "hit5": float(any(rel[:5])),
        "hit10": float(any(rel[:10])),
        "rr": 0.0 if first is None else 1.0 / (first + 1),
        "recall5": (sum(rel[:5]) / len(acceptable)) if acceptable else 0.0,
    }


def summarize(per_item, n_boot=2000, seed=C.SEED):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame(per_item)
    out = {}
    for m in ["p1", "primary1", "p3", "hit3", "hit5", "hit10", "rr", "recall5"]:
        v = df[m].values
        boots = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(n_boot)]
        out[m] = {"mean": round(float(v.mean()), 3), "ci95": [round(float(np.quantile(boots, 0.025)), 3),
                                                              round(float(np.quantile(boots, 0.975)), 3)]}
    out["n"] = int(len(df))
    return out


def wilson(k, n, z=1.96):
    if n == 0:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 3), round(c + h, 3)]


def evaluate_rankings(rank_map, gold, key="acceptable", statuses=("requirement", "generic")):
    """rank_map: sample_id -> list of codes (rank order)."""
    g = gold[gold.item_status.isin(statuses)]
    per = []
    for r in g.itertuples():
        ranked = rank_map[r.sample_id]
        m = item_metrics(ranked, getattr(r, key), r.primary_code)
        m.update({"sample_id": r.sample_id, "fit": r.fit, "component_type": r.component_type if hasattr(r, "component_type") else None})
        per.append(m)
    return summarize(per), per
