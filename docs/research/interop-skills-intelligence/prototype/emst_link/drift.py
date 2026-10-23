"""Step 5: change-over-time indicator — share of plan direction linked to each competency, by planning-rule era.

This is a demonstration of the L5 output shape, not a finding about workforce demand:
 * the 1982-rule and 2012-rule corpora differ in plan structure and in how LMPs extracted them;
 * linker precision@1 is far from perfect (see eval_report.json), so small shifts are noise;
 * uncertainty is a plan-level cluster bootstrap (components within a plan are not independent).
"""
import numpy as np
import pandas as pd

from . import config as C
from . import data

BINDING = ["standard", "guideline", "standard_or_guideline"]


def run(comp, linker, n_boot=1000):
    df, _ = data.load_components()
    df = df[(df.agency_group == "USFS") & df.framework.isin(["usfs-1982-rule", "usfs-2012-rule"])]
    df = df[df.component_type.isin(BINDING + ["monitoring"])]
    df = df[df.text.map(data.usable_text)].drop_duplicates(subset=["plan_id", "text"]).reset_index(drop=True)
    texts = df.text.tolist()
    top1, raw1 = [], []
    B = 4000
    for i in range(0, len(texts), B):
        order, S, raw = linker.rank(texts[i:i + B], k=1)
        top1.extend(order[:, 0].tolist())
        raw1.extend(raw["tfidf"].max(axis=1).tolist())
    df["top1"] = [linker.codes[j] for j in top1]
    df["top1_raw_cos"] = raw1
    lo_cut = float(np.quantile(df.top1_raw_cos, 1 / 3))
    df["linked"] = df.top1_raw_cos >= lo_cut
    df[["plan_id", "framework", "component_type", "component_id", "top1", "top1_raw_cos", "linked"]].to_csv(
        C.OUT / "all_components_top1.csv", index=False)

    rng = np.random.default_rng(C.SEED)
    codes = sorted(comp.code, key=lambda c: [int(x) for x in c.split(".")])
    rows = []
    sub = df[df.linked & df.component_type.isin(BINDING)]
    eras = {"1982": sub[sub.framework == "usfs-1982-rule"], "2012": sub[sub.framework == "usfs-2012-rule"]}

    def shares(frame):
        vc = frame.top1.value_counts()
        return np.array([vc.get(c, 0) for c in codes]) / max(len(frame), 1)

    point = {e: shares(f) for e, f in eras.items()}
    plans = {e: f.plan_id.unique() for e, f in eras.items()}
    groups = {e: dict(tuple(f.groupby("plan_id"))) for e, f in eras.items()}
    boots = []
    for _ in range(n_boot):
        bs = {}
        for e in eras:
            pick = rng.choice(plans[e], size=len(plans[e]), replace=True)
            bs[e] = shares(pd.concat([groups[e][p] for p in pick]))
        boots.append(bs["2012"] - bs["1982"])
    boots = np.vstack(boots)
    lo, hi = np.quantile(boots, 0.025, axis=0), np.quantile(boots, 0.975, axis=0)
    title = dict(zip(comp.code, comp.title))
    for j, c in enumerate(codes):
        rows.append({"code": c, "title": title[c], "share_1982": round(point["1982"][j], 4), "share_2012": round(point["2012"][j], 4),
                     "delta": round(point["2012"][j] - point["1982"][j], 4), "ci95_lo": round(lo[j], 4), "ci95_hi": round(hi[j], 4),
                     "ci_excludes_zero": bool(lo[j] > 0 or hi[j] < 0)})
    out = pd.DataFrame(rows).sort_values("delta")
    out.to_csv(C.OUT / "era_shift_by_competency.csv", index=False)
    summ = {
        "n_components_linked": int(df.linked.sum()), "n_components_total": int(len(df)),
        "n_plans": {e: int(len(plans[e])) for e in plans}, "n_binding_linked": {e: int(len(f)) for e, f in eras.items()},
        "n_competencies_ci_excludes_zero": int(out.ci_excludes_zero.sum()),
        "largest_increases": out.tail(5)[["code", "title", "delta", "ci95_lo", "ci95_hi"]].to_dict("records")[::-1],
        "largest_decreases": out.head(5)[["code", "title", "delta", "ci95_lo", "ci95_hi"]].to_dict("records"),
        "caveat": "Era contrast confounds plan format, extraction method and linker error with real change; see report.",
    }
    return summ, df
