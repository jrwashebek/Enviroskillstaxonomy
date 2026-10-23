#!/usr/bin/env python3
"""Generate top-7 O*NET task candidates (environment-related O*NET-SOC pool) for each sampled v1 task, for analyst curation.
Similarity = 0.5 * word(1-2gram) TF-IDF cosine + 0.5 * char_wb(3-5) TF-IDF cosine. LM, EMST v2.
Usage: python3 -I pilot_candidates.py <ext_dir>   Reads ../v1_onet_pilot_matches.csv (sample); writes ../v1_onet_pilot_candidates.txt"""
import os, sys
import numpy as np, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
B = sys.argv[1]; H = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
P = ("19-1","19-2","19-3051","19-4","19-5","17-2081","17-3025","45-4","45-1011","33-2","33-3031","13-1041","13-1199.05","11-9121","11-1011.03","51-8031","47-4041",
     "25-1053","25-1043","15-1299.02","17-1022","17-1021","11-9013","13-2099","19-3094","11-3071","13-1111","11-2032","53-7081","17-2051","13-1071","13-1151","13-1082",
     "11-9151","21-1094","19-3011","13-2051","43-6014","43-4171","15-2051","11-9199","13-1161","43-9061","27-3031","11-3013","11-9033","13-1023","13-1199","11-9161",
     "45-2091","45-2041","49-9021","47-2061","37-3011","37-3013","53-3032","25-9031","25-2031","39-9032","11-3031","29-9011")
tl = pd.read_csv(os.path.join(B, "openai_GPTs-are-GPTs/repo/data/full_labelset.tsv"), sep="\t")
tl = tl[tl["O*NET-SOC Code"].astype(str).str.startswith(P)].reset_index(drop=True)
s = pd.read_csv(os.path.join(H, "v1_onet_pilot_matches.csv"))
corpus = pd.concat([tl["Task"].astype(str), s["v1_task_text"].astype(str)])
v1 = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, stop_words="english").fit(corpus)
v2 = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True).fit(corpus)
S = 0.5 * linear_kernel(v1.transform(s["v1_task_text"]), v1.transform(tl["Task"])) + 0.5 * linear_kernel(v2.transform(s["v1_task_text"]), v2.transform(tl["Task"]))
with open(os.path.join(H, "v1_onet_pilot_candidates.txt"), "w") as fh:
    fh.write("pool tasks %d\n" % len(tl))
    for i, r in s.iterrows():
        fh.write(f"\n## {i} {r.v1_task_key} [{r.v1_auto_type}/{r.v1_tacit}/{r.v1_career}] {r.v1_task_text}\n")
        for j in np.argsort(-S[i])[:7]:
            t = tl.iloc[j]
            fh.write(f"  {int(t['Task ID'])} {t['O*NET-SOC Code']} {t['Title'][:30]} | {t['Task'][:110]} | {t['human_labels']} {S[i,j]:.2f}\n")
print("written")
