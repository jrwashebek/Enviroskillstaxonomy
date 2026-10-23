#!/usr/bin/env python3
"""Join analyst-curated v1->O*NET matches (../v1_onet_pilot_curation.csv) to external labels and compare with v1 labels. LM, EMST v2.
Usage: python3 -I pilot_curated_compare.py <ext_dir>   Writes ../v1_onet_pilot_curated.csv and ../v1_onet_pilot_curated_summary.txt"""
import os, sys
import pandas as pd
B = sys.argv[1]; H = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
m = pd.read_csv(os.path.join(H, "v1_onet_pilot_matches.csv")); c = pd.read_csv(os.path.join(H, "v1_onet_pilot_curation.csv"))
assert (m["v1_task_key"].values == c["v1_task_key"].values).all()
tl = pd.read_csv(os.path.join(B, "openai_GPTs-are-GPTs/repo/data/full_labelset.tsv"), sep="\t")
ph = pd.read_csv(os.path.join(B, "microsoft_working-with-ai/repo/physical_tasks.csv")); ph["Task ID"] = ph["Task ID"].astype(float)
tl = tl.merge(ph, on="Task ID", how="left").drop_duplicates("Task ID").set_index("Task ID")
def lab(i, col):
    return tl.loc[float(i), col] if pd.notna(i) and float(i) in tl.index else None
for col, src in [("onet_soc", "O*NET-SOC Code"), ("onet_title", "Title"), ("onet_task_text", "Task"), ("eloundou_human", "human_labels"),
                 ("eloundou_gpt4", "gpt4_exposure"), ("gpt4_automation", "gpt4_automation"), ("ms_physical", "Physical")]:
    c[col] = [lab(i, src) for i in c.curated_onet_task_id]
c["alt_eloundou_human"] = [lab(i, "human_labels") for i in c.alt_onet_task_id]
for col in ["v1_code", "v1_task_text", "v1_auto_type", "v1_tacit", "v1_career", "v1_vector", "v1_horizon"]:
    c[col] = m[col]
cols = ["row","v1_task_key","v1_code","v1_task_text","v1_auto_type","v1_tacit","v1_career","v1_vector","v1_horizon","curated_onet_task_id","match_type","onet_soc",
        "onet_title","onet_task_text","eloundou_human","eloundou_gpt4","gpt4_automation","ms_physical","alt_onet_task_id","alt_eloundou_human","curation_note"]
c[cols].to_csv(os.path.join(H, "v1_onet_pilot_curated.csv"), index=False)
L = ["CURATED pilot (analyst judgment on top-7 candidates; n=60)", "match_type: " + str(c.match_type.value_counts().to_dict()),
     "No O*NET analogue by v1 auto type:\n" + pd.crosstab(c.v1_auto_type, c.match_type == "none").to_string()]
mm = c[c.match_type != "none"]
L.append("\nMatched (equivalent/close/partial) n=%d" % len(mm))
for a, b, t in [("v1_auto_type", "eloundou_human", "Eloundou HUMAN label"), ("v1_auto_type", "eloundou_gpt4", "Eloundou GPT-4 label"),
                ("v1_auto_type", "gpt4_automation", "GPT-4 automation rubric"), ("v1_auto_type", "ms_physical", "MS physical"),
                ("v1_tacit", "eloundou_human", "Eloundou HUMAN"), ("v1_career", "eloundou_human", "Eloundou HUMAN")]:
    L.append(f"{a} x {t}:\n" + pd.crosstab(mm[a], mm[b], margins=True).to_string())
st = mm[mm.match_type.isin(["equivalent", "close"])]
L.append("\nEquivalent/close only n=%d:\n" % len(st) + pd.crosstab(st.v1_auto_type, st.eloundou_human, margins=True).to_string())
alt = c[c.alt_eloundou_human.notna() & c.eloundou_human.notna()]
L.append("\nLabel stability: tasks with a second plausible O*NET match: %d; human labels differ in %d" % (len(alt), (alt.alt_eloundou_human != alt.eloundou_human).sum()))
txt = "\n".join(L); open(os.path.join(H, "v1_onet_pilot_curated_summary.txt"), "w").write(txt + "\n"); print(txt)
