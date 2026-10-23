"""Step 2: link plan components (or any text) to v1 competencies; write top-k candidates with confidence."""
import json

import numpy as np
import pandas as pd

from . import config as C
from . import data
from .index import Linker


def build_linkers(comp):
    docs = [data.competency_document(r) for r in comp.to_dict("records")]
    short = [f"{r['title']}. {r['description']} {r['tasks']}" for r in comp.to_dict("records")]
    full = Linker(docs, comp.code, comp_short=short)
    # title+description only: shows what the extra v1 text (tasks, indicators) buys
    td_docs = [f"{r['title']} {r['title']} {r['skill_area_name']} {r['description']}" for r in comp.to_dict("records")]
    titledesc = Linker(td_docs, comp.code, comp_short=td_docs)
    return {"full": full, "titledesc": titledesc}


def build_task_linker():
    """Task-level index: each v1 task statement is its own document (+ its competency title as context)."""
    tasks = pd.read_csv(C.V1_BASELINE / "tasks.csv", dtype=str, keep_default_na=False)
    comp = pd.read_csv(C.V1_BASELINE / "competencies.csv", dtype=str, keep_default_na=False)
    title = {r.code: (r.suggested_title or r.title) for r in comp.itertuples()}
    tasks["doc"] = tasks.apply(lambda r: f"{r.text} {r.text} {title.get(r.code, '')}", axis=1)
    lk = Linker(tasks["doc"].tolist(), tasks["key"].tolist(), comp_short=tasks["doc"].tolist())
    return lk, tasks


def task_rollup(lk, tasks, texts, k=None, variant="fused"):
    """Score competency = max over its task scores; returns (order over competency codes, scores, codes, best task)."""
    k = k or C.TOP_K
    raw = lk.scores(texts)
    S = lk.fuse(raw) if variant == "fused" else raw[variant]
    codes = sorted(tasks.code.unique(), key=lambda c: [int(x) for x in c.split(".")])
    idx = {c: np.where(tasks.code.values == c)[0] for c in codes}
    M = np.vstack([S[:, idx[c]].max(axis=1) for c in codes]).T
    arg = {c: idx[c][S[:, idx[c]].argmax(axis=1)] for c in codes}
    order = np.argsort(-M, axis=1)[:, :k]
    return order, M, codes, arg


def bands_from_unlabelled(raw_top1, margin):
    """Confidence bands fixed from the unlabelled 300-sample distribution (terciles), never from gold."""
    hi_cut, lo_cut = np.quantile(raw_top1, 2 / 3), np.quantile(raw_top1, 1 / 3)
    m_cut = np.median(margin)
    return {"hi_cut_raw_cos": float(hi_cut), "lo_cut_raw_cos": float(lo_cut), "margin_cut": float(m_cut)}


def assign_band(top1, margin, cuts):
    if top1 >= cuts["hi_cut_raw_cos"] and margin >= cuts["margin_cut"]:
        return "high"
    if top1 < cuts["lo_cut_raw_cos"]:
        return "low"
    return "medium"


def link_frame(df, comp, linker, cuts=None, text_col="text", id_col="sample_id"):
    texts = df[text_col].tolist()
    order, S, raw = linker.rank(texts)
    tf = raw["tfidf"]
    srt = np.sort(tf, axis=1)
    raw_top1 = srt[:, -1]
    margin = srt[:, -1] - srt[:, -2]
    if cuts is None:
        cuts = bands_from_unlabelled(raw_top1, margin)
    rows = []
    codes = comp.code.values
    titles = comp.title.values
    for i in range(len(df)):
        band = assign_band(raw_top1[i], margin[i], cuts)
        for rnk, j in enumerate(order[i], start=1):
            rows.append({
                id_col: df.iloc[i][id_col], "rank": rnk, "code": codes[j], "title": titles[j],
                "fused": round(float(S[i, j]), 4), "tfidf": round(float(tf[i, j]), 4),
                "bm25": round(float(raw["bm25"][i, j]), 3),
                "semantic": round(float(raw["semantic"][i, j]), 4) if "semantic" in raw else None,
                "item_top1_raw_cos": round(float(raw_top1[i]), 4), "item_margin": round(float(margin[i]), 4),
                "confidence_band": band,
                "abstain_candidate_gap": bool(raw_top1[i] < C.ABSTAIN_RAW_COS),
            })
    return pd.DataFrame(rows), cuts
