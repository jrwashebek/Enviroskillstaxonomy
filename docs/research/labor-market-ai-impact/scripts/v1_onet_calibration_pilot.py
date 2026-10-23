#!/usr/bin/env python3
"""
Pilot external calibration of the v1 EMST exposure instrument (Task 12/13 labels).
Role: LM, EMST v2 Phase 2.  Deterministic (fixed seed).

Steps
 1. Draw a stratified sample of 60 v1 tasks (all 4 S calls; 8 V; 16 Ac; 16 A; 16 H), spread across domains.
 2. Match each v1 task to O*NET 27.x task statements (19,265 tasks; from Eloundou et al. replication data)
    by TF-IDF cosine similarity (word 1-2 grams, sublinear tf, English stop words). Keep top-5 matches.
    Preferred match = best match inside environmental/natural-resource O*NET-SOC codes if its similarity is
    >= 0.85 x the global best; otherwise the global best.
 3. Attach external labels to the matched O*NET task:
      - Eloundou et al. human exposure label (E0 no exposure / E1 direct LLM exposure / E2 exposure with
        LLM-powered software) and GPT-4 label; GPT-4 automation rubric score (T0..T4 -> 0..1)
      - Microsoft "Working with AI" v1.1 physical-task flag (O*NET task ID level)
    and a similarity-weighted top-5 "neighbourhood" exposure (E0=0, E2=0.5, E1=1; i.e. Eloundou beta weights).
 4. Compare with v1 labels (auto type, tacit density, career ladder, horizon).
Match quality: strong >= 0.45, moderate 0.30-0.45, weak < 0.30 (cosine). ALL matches need human review before use;
this is a feasibility pilot, not a calibrated crosswalk.

Usage: python3 -I v1_onet_calibration_pilot.py <ext_dir> <v1_tasks_csv>
Outputs (next to this script): v1_onet_pilot_matches.csv, v1_onet_pilot_summary.txt
AEI task-level usage could NOT be joined: Hugging Face is blocked from this environment (see report.md section 5).
"""
import os
import sys

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

EXT, V1 = sys.argv[1], sys.argv[2]
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")  # outputs go to the role folder
SEED = 20261023

ENV_PREFIXES = ("19-1", "19-2", "19-3051", "19-4", "19-5", "17-2081", "17-3025", "45-4", "45-1011", "33-2", "33-3031",
                "13-1041", "13-1199.05", "11-9121", "11-1011.03", "51-8031", "47-4041", "25-1053", "25-1043", "15-1299.02",
                "17-1022", "17-1021", "11-9013", "13-1199", "13-2099", "21-1", "25-9031", "11-9199", "19-3094", "23-1011",
                "11-3071", "41-3091", "13-1111", "11-2032", "27-3031", "39-7011", "33-9", "53-7081", "17-2051")
EVAL = {"E0": 0.0, "E2": 0.5, "E1": 1.0}


def main():
    tl = pd.read_csv(os.path.join(EXT, "openai_GPTs-are-GPTs/repo/data/full_labelset.tsv"), sep="\t")
    phys = pd.read_csv(os.path.join(EXT, "microsoft_working-with-ai/repo/physical_tasks.csv"))
    phys["Task ID"] = phys["Task ID"].astype(float)
    tl = tl.merge(phys, on="Task ID", how="left").reset_index(drop=True)
    tl["env_occ"] = tl["O*NET-SOC Code"].astype(str).str.startswith(ENV_PREFIXES)

    v1 = pd.read_csv(V1)
    rng = np.random.default_rng(SEED)
    quota = {"S": 4, "V": 8, "Ac": 16, "A": 16, "H": 16}
    picks = []
    for t, q in quota.items():
        pool = v1[v1["auto_type"] == t]
        # spread across domains: shuffle, then round-robin by domain
        pool = pool.iloc[rng.permutation(len(pool))]
        pool = pool.assign(dom=pool["code"].astype(str).str.split(".").str[0])
        groups = [g for _, g in pool.groupby("dom")]
        out, i = [], 0
        while len(out) < min(q, len(pool)):
            for g in groups:
                if i < len(g) and len(out) < q:
                    out.append(g.iloc[i])
            i += 1
        picks.extend(out)
    s = pd.DataFrame(picks).reset_index(drop=True)

    vec = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, stop_words="english", min_df=1)
    X = vec.fit_transform(pd.concat([tl["Task"].astype(str), s["text"].astype(str)]))
    Xo, Xv = X[: len(tl)], X[len(tl):]
    sims = linear_kernel(Xv, Xo)

    rows = []
    for i, r in s.iterrows():
        sim = sims[i]
        top = np.argsort(-sim)[:5]
        env_idx = np.where(tl["env_occ"].values)[0]
        best_env = env_idx[np.argmax(sim[env_idx])]
        choice = best_env if sim[best_env] >= 0.85 * sim[top[0]] else top[0]
        m = tl.iloc[choice]
        w = sim[top]
        neigh = float(np.dot(w, [EVAL.get(tl.iloc[j]["human_labels"], np.nan) for j in top]) / w.sum()) if w.sum() > 0 else np.nan
        neigh_phys = float(np.dot(w, [1.0 if tl.iloc[j]["Physical"] is True else 0.0 for j in top]) / w.sum()) if w.sum() > 0 else np.nan
        simv = float(sim[choice])
        rows.append({
            "v1_task_key": r["key"], "v1_code": r["code"], "v1_task_text": r["text"],
            "v1_auto_type": r["auto_type"], "v1_tacit": r["tacit_density"], "v1_career": r["career_ladder"],
            "v1_vector": r["vector"], "v1_horizon": r["horizon"],
            "onet_soc": m["O*NET-SOC Code"], "onet_title": m["Title"], "onet_task_id": int(m["Task ID"]), "onet_task_text": m["Task"],
            "match_similarity": round(simv, 3),
            "match_quality": "strong" if simv >= 0.45 else ("moderate" if simv >= 0.30 else "weak"),
            "env_occupation_match": bool(m["env_occ"]),
            "eloundou_human_label": m["human_labels"], "eloundou_gpt4_label": m["gpt4_exposure"],
            "eloundou_gpt4_automation": m["gpt4_automation"], "ms_physical_task": m["Physical"],
            "neighbourhood_beta_top5": round(neigh, 3), "neighbourhood_physical_top5": round(neigh_phys, 3),
        })
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(HERE, "v1_onet_pilot_matches.csv"), index=False)

    lines = []
    P = lines.append
    P("v1 -> O*NET calibration pilot summary (n=%d; seed %d)" % (len(out), SEED))
    P("Match quality: " + str(out["match_quality"].value_counts().to_dict()))
    P("Matched to environmental O*NET-SOC: %d of %d" % (out["env_occupation_match"].sum(), len(out)))
    P("\nCrosstab v1 auto type x Eloundou HUMAN label (matched task):")
    P(pd.crosstab(out["v1_auto_type"], out["eloundou_human_label"], margins=True).to_string())
    P("\nCrosstab v1 auto type x GPT-4 automation rubric (matched task):")
    P(pd.crosstab(out["v1_auto_type"], out["eloundou_gpt4_automation"], margins=True).to_string())
    P("\nCrosstab v1 auto type x Microsoft physical-task flag:")
    P(pd.crosstab(out["v1_auto_type"], out["ms_physical_task"], margins=True).to_string())
    P("\nMean neighbourhood exposure (beta, top-5 similarity-weighted) by v1 auto type:")
    P(out.groupby("v1_auto_type")[["neighbourhood_beta_top5", "neighbourhood_physical_top5", "match_similarity"]].mean().round(3).to_string())
    P("\nSame, strong+moderate matches only:")
    sm = out[out["match_quality"] != "weak"]
    P(out.assign(_=1).groupby("v1_auto_type")["_"].count().rename("n_all").to_frame().join(
        sm.groupby("v1_auto_type")[["neighbourhood_beta_top5", "neighbourhood_physical_top5"]].mean().round(3)).to_string())
    P("\nMean neighbourhood exposure by v1 tacit density:")
    P(out.groupby("v1_tacit")[["neighbourhood_beta_top5", "neighbourhood_physical_top5"]].mean().round(3).to_string())
    P("\nMean neighbourhood exposure by v1 career-ladder position:")
    P(out.groupby("v1_career")[["neighbourhood_beta_top5", "neighbourhood_physical_top5"]].mean().round(3).to_string())
    # simple concordance tests
    hset = out[out["v1_auto_type"] == "H"]
    exp_set = out[out["v1_auto_type"].isin(["Ac", "S", "V"])]
    P("\nConcordance checks (matched task):")
    P("  v1 H tasks whose matched O*NET task is human-rated E0: %d/%d" % ((hset["eloundou_human_label"] == "E0").sum(), len(hset)))
    P("  v1 Ac/S/V tasks whose matched O*NET task is human-rated E1 or E2: %d/%d" % (exp_set["eloundou_human_label"].isin(["E1", "E2"]).sum(), len(exp_set)))
    P("  v1 Ac/S/V tasks matched E1 (direct exposure): %d/%d" % ((exp_set["eloundou_human_label"] == "E1").sum(), len(exp_set)))
    a_set = out[out["v1_auto_type"] == "A"]
    P("  v1 A tasks matched E0 (external says unexposed): %d/%d" % ((a_set["eloundou_human_label"] == "E0").sum(), len(a_set)))
    txt = "\n".join(lines)
    open(os.path.join(HERE, "v1_onet_pilot_summary.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
