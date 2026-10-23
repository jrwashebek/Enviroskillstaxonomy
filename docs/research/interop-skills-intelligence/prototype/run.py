#!/usr/bin/env python3
"""EMST linking prototype — one command:  python run.py

Steps
 1. sample   : 300 LMPs plan components (monitoring/standard/guideline, 8 states) + 60-item blind gold subset
 2. link     : rank all 222 v1 competencies for each component (TF-IDF + BM25 + WordLlama static embeddings)
 3. evaluate : precision@k etc. against the single-annotator gold set (strict and pooled), by variant
 4. bands    : empirical precision per a-priori confidence band; review queue
 5. drift    : competency share of plan direction by planning-rule era, all components, with plan-level bootstrap
 6. gaps     : low-similarity components clustered -> candidate coverage gaps
 7. postings : run the linker on any texts in data/job_postings/*.txt (with URL headers)

Outputs land in outputs/. Everything is deterministic (fixed seeds, no network).
Flags: --skip-drift (faster), --no-semantic (lexical only).
"""
import argparse
import glob
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

ap = argparse.ArgumentParser()
ap.add_argument("--skip-drift", action="store_true")
ap.add_argument("--no-semantic", action="store_true")
args = ap.parse_args()
if args.no_semantic:
    os.environ["EMST_SEMANTIC"] = "none"

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from emst_link import config as C  # noqa: E402
from emst_link import data, evaluate, link, sample  # noqa: E402
from emst_link import drift as drift_mod  # noqa: E402
from emst_link import gaps as gaps_mod  # noqa: E402

t0 = time.time()
C.OUT.mkdir(parents=True, exist_ok=True)
report = {"generated_by": "prototype/run.py", "semantic_backend": None}

# 1 ---------------------------------------------------------------- sample
s, g_items = sample.run()
comp, comp_manifest = data.load_competencies()
report["inputs"] = {"v1_baseline": comp_manifest, "sample": json.loads((C.DATA / "sample_manifest.json").read_text())}
report["n_competencies"] = int(len(comp))

# 2 ---------------------------------------------------------------- link
linkers = link.build_linkers(comp)
full = linkers["full"]
report["semantic_backend"] = full.sem_backend
cand, cuts = link.link_frame(s, comp, full)
cand.to_csv(C.OUT / "candidates_sample300.csv", index=False)
report["confidence_band_cuts"] = cuts

# 3 ---------------------------------------------------------------- evaluate variants (dev + held-out)
from emst_link.preprocess import prep  # noqa: E402
tlk, tasks = link.build_task_linker()


def rrf(a, b, k=60):
    sc = {}
    for lst in (a, b):
        for r, c in enumerate(lst):
            sc[c] = sc.get(c, 0) + 1 / (k + r + 1)
    return [c for c, _ in sorted(sc.items(), key=lambda x: -x[1])][: C.TOP_K]


def agreement_band(raw, fused):
    """Pre-specified after the dev-set band failure: count base rankers agreeing with fused top-1."""
    f1 = fused.argmax(axis=1)
    agree = sum((raw[k].argmax(axis=1) == f1).astype(int) for k in raw)
    n = len(raw)
    return np.where(agree == n, "high", np.where(agree >= n - 1, "medium", "low"))


def evaluate_set(gold_name, pooled_name, items_name):
    items = pd.read_csv(C.GOLD / items_name, dtype=str, keep_default_na=False)
    gold = evaluate.load_gold(gold_name, pooled_name).merge(items[["sample_id", "component_type", "state", "agency_group", "text"]], on="sample_id")
    texts = gold.text.tolist()
    ptexts = [prep(t) for t in texts]
    ids = gold.sample_id.tolist()
    rank_maps, bands = {}, {}
    for name, lk in linkers.items():
        for v in ["tfidf", "bm25", "fused"] + (["semantic"] if lk.sem is not None else []):
            order, S, raw = lk.rank(texts, variant=v)
            rank_maps[f"{name}:{v}"] = {sid: [lk.codes[j] for j in order[i]] for i, sid in enumerate(ids)}
    order, S, raw = full.rank(ptexts)
    rank_maps["full:fused+prep"] = {sid: [full.codes[j] for j in order[i]] for i, sid in enumerate(ids)}
    bands["agreement+prep"] = agreement_band(raw, S)
    order, S, raw = full.rank(texts)
    bands["agreement"] = agreement_band(raw, S)
    for v in ["tfidf", "bm25", "fused"] + (["semantic"] if tlk.sem is not None else []):
        order, M, codes, _ = link.task_rollup(tlk, tasks, texts, variant=v)
        rank_maps[f"task-max:{v}"] = {sid: [codes[j] for j in order[i]] for i, sid in enumerate(ids)}
    rank_maps["hybrid-rrf:full+task"] = {sid: rrf(rank_maps["full:fused"][sid], rank_maps["task-max:fused"][sid]) for sid in ids}
    res = {}
    for key in ["acceptable", "pooled"]:
        res[key] = {name: evaluate.evaluate_rankings(rm, gold, key=key)[0] for name, rm in rank_maps.items()}
    # tercile bands (a priori, from unlabelled 300) and agreement bands, scored on this set
    tb = cand.groupby("sample_id").confidence_band.first()
    detail = gold[["sample_id", "item_status", "fit", "gap_theme", "primary_code", "acceptable_codes", "component_type", "state", "agency_group", "text"]].copy()
    detail["band_tercile"] = detail.sample_id.map(tb)
    detail["band_agreement"] = bands["agreement"]
    detail["band_agreement_prep"] = bands["agreement+prep"]
    for nm in ["full:fused", "full:fused+prep", "task-max:fused"]:
        detail[nm + ":top5"] = detail.sample_id.map(lambda sid: "|".join(rank_maps[nm][sid][:5]))
    for nm in ["full:fused", "full:fused+prep"]:
        per = pd.DataFrame(evaluate.evaluate_rankings(rank_maps[nm], gold, key="acceptable")[1])
        detail = detail.merge(per[["sample_id", "p1", "hit5"]].rename(columns={"p1": nm + ":p1", "hit5": nm + ":hit5"}), on="sample_id", how="left")
    band_res = {}
    nn = detail[detail.item_status != "noise"]
    for bcol, sysname in [("band_tercile", "full:fused"), ("band_agreement", "full:fused"), ("band_agreement_prep", "full:fused+prep")]:
        band_res[bcol] = {}
        for b in ["high", "medium", "low"]:
            sub = nn[nn[bcol] == b]
            k = int(sub[sysname + ":p1"].sum())
            band_res[bcol][b] = {"n": int(len(sub)), "p_at_1": round(k / len(sub), 3) if len(sub) else None, "wilson95": evaluate.wilson(k, len(sub))}
        band_res[bcol]["noise_items"] = detail[detail.item_status == "noise"][bcol].value_counts().to_dict()
    meta = {"n_items": int(len(gold)), "by_status": gold.item_status.value_counts().to_dict(),
            "by_fit_non_noise": gold[gold.item_status != "noise"].fit.value_counts().to_dict()}
    return res, band_res, detail, meta


report["evaluation"], report["bands"], report["gold"] = {}, {}, {}
for tag, gname, pname, iname in [("dev", "gold_set.csv", "gold_pooled_additions.csv", "gold_items_blind.csv"),
                                 ("heldout", "gold_heldout.csv", None, "gold_items_heldout_blind.csv")]:
    res, band_res, detail, meta = evaluate_set(gname, pname, iname)
    report["evaluation"][tag], report["bands"][tag], report["gold"][tag] = res, band_res, meta
    detail.to_csv(C.OUT / f"gold_eval_detail_{tag}.csv", index=False)
report["gold"]["annotator"] = "single AI annotator (IA role, Claude); judged blind to system output; NOT a human SME gold set"
results = report["evaluation"]

# 4 ---------------------------------------------------------------- review queue (sample of 300)
report["bands_on_sample300"] = cand.groupby("sample_id").confidence_band.first().value_counts().to_dict()
rq = cand[(cand["rank"] <= 5)].merge(s[["sample_id", "plan_id", "component_id", "component_type", "text"]], on="sample_id")
rq = rq[rq.confidence_band != "high"]
rq.to_csv(C.OUT / "review_queue.csv", index=False)

# 5 ---------------------------------------------------------------- drift (change over plan eras)
if not args.skip_drift:
    report["drift"], linked_all = drift_mod.run(comp, full)
else:
    linked_all = s.copy()
    linked_all["linked"] = linked_all.sample_id.map(cand.groupby("sample_id").confidence_band.first()) != "low"
# 6 ---------------------------------------------------------------- coverage-gap candidates
report["gaps"] = gaps_mod.run(linked_all)

# 7 ---------------------------------------------------------------- postings / PDs
post_files = sorted(glob.glob(str(C.DATA / "job_postings" / "*.txt")))
if post_files:
    recs = []
    for f in post_files:
        lines = Path(f).read_text().splitlines()
        meta = {l.split(":", 1)[0].strip().lower(): l.split(":", 1)[1].strip() for l in lines[:6] if ":" in l and l.split(":", 1)[0].strip().lower() in {"url", "title", "source", "accessed", "kind"}}
        body = "\n".join(l for l in lines if l.split(":", 1)[0].strip().lower() not in {"url", "title", "source", "accessed", "kind"})
        # link paragraph-sized chunks, aggregate by max score per competency
        chunks = [c.strip() for c in body.split("\n\n") if len(c.split()) >= 8] or [body]
        order, S, raw = full.rank(chunks)
        agg = S.max(axis=0)
        top = np.argsort(-agg)[:10]
        per_chunk = [{"chunk": c[:90], "top3": [f"{full.codes[j]} {comp.title.values[j]}" for j in order[i][:3]]} for i, c in enumerate(chunks)]
        recs.append({"file": Path(f).name, **meta, "n_chunks": len(chunks), "per_chunk": per_chunk,
                     "top10": [{"code": full.codes[j], "title": comp.title.values[j], "score": round(float(agg[j]), 3)} for j in top]})
    (C.OUT / "postings_links.json").write_text(json.dumps(recs, indent=1))
    report["postings"] = {"n_files": len(recs)}

report["runtime_sec"] = round(time.time() - t0, 1)
(C.OUT / "eval_report.json").write_text(json.dumps(report, indent=1, default=str))
print(json.dumps({k: report[k] for k in ["semantic_backend", "gold", "bands"]}, indent=1))
for tag in results:
    for key in ["acceptable", "pooled"]:
        print(f"\n== {tag} / {key} ==")
        for name, m in results[tag][key].items():
            print(f"{name:24s} P@1 {m['p1']['mean']:.3f} {m['p1']['ci95']}  Hit@3 {m['hit3']['mean']:.3f}  Hit@5 {m['hit5']['mean']:.3f}  P@3 {m['p3']['mean']:.3f}  MRR {m['rr']['mean']:.3f}  n={m['n']}")
print(f"\nruntime {report['runtime_sec']}s")
