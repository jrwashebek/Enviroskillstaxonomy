#!/usr/bin/env python3
"""Map the environmental task rows seen in the AEI 2025-02-10 onet_task_mappings.csv (partial blob view, transcribed by WebFetch summarizer)
to O*NET-SOC codes by text match against O*NET 27.x tasks. LM, EMST v2.  Usage: python3 -I aei_rows_to_onet.py <ext_dir>  Writes ../aei_env_rows_seen.csv
CAVEAT: some task texts were paraphrased by the summarizer; match similarity is reported; pct values are percent of conversations."""
import os, sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
B = sys.argv[1]; H = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
tl = pd.read_csv(os.path.join(B, "openai_GPTs-are-GPTs/repo/data/full_labelset.tsv"), sep="\t")
rows = [("advocate for accessible health care that minimizes environmental health risks",0.003257),
("analyze and distill climate-related research findings to inform legislators, regulatory agencies, or other stakeholders",0.003778),
("analyze changes designed to improve the environmental performance of complex systems and avoid unintended negative consequences",0.019935),
("analyze data to determine validity, quality, and scientific significance and to interpret correlations between human activities and environmental effects",0.003648),
("recommend chemical, biological, or other wastewater treatment methods to prevent pollution",0.006254),
("analyze results of investigations to determine measures needed to maintain or restore proper soil management",0.002345),
("analyze the efficiency of water delivery structures such as dams, canals and pipes",0.004039),
("assess or propose sustainability initiatives, considering factors such as cost effectiveness, technical feasibility, and acceptance",0.002345),
("collaborate with other professionals to develop sustainable transportation strategies at local, regional, or national levels",0.001954),
("advise on dam or road construction, land use, or resource management",0.006645),
("analyze maps and topographic or geologic data",0.002866),
("check the air quality of ventilation systems and make adjustments to ensure compliance with mandated safety codes",0.002084),
("collect, synthesize, analyze, manage, and report environmental data, such as pollution emission measurements",0.004951),
("conduct research to determine best methods of planting, spraying, cultivating, harvesting",0.008599),
("conduct educational programs that provide farmers or farm cooperative members with information that can help",0.022671),
("conduct safety training or education programs and demonstrate the use of safety equipment",0.001954),
("conduct short-term and long-term climate assessments and study storm occurrences",0.005212),
("conduct, or oversee the conduct of, chemical, physical, and biological water quality monitoring or sampling",0.003518),
("conduct meteorological research into the processes or determinants of atmospheric phenomena, weather, or climate",0.006645),
("compile and evaluate hydrologic information to prepare navigational charts and maps and to predict atmospheric conditions",0.003648),
("analyze green product marketing or sales trends to forecast future conditions",0.002476),
("calculate costs or savings for water- or energy-efficient appliances or systems",0.003909)]
v = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True).fit(pd.concat([tl.Task, pd.Series([r[0] for r in rows])]))
S = linear_kernel(v.transform([r[0] for r in rows]), v.transform(tl.Task))
out = []
for i, (t, p) in enumerate(rows):
    j = S[i].argmax(); m = tl.iloc[j]
    out.append({"aei_task_text_as_transcribed": t, "aei_pct_of_conversations": p, "matched_onet_soc": m["O*NET-SOC Code"], "matched_title": m["Title"], "match_similarity": round(float(S[i, j]), 2)})
pd.DataFrame(out).to_csv(os.path.join(H, "aei_env_rows_seen.csv"), index=False); print(pd.DataFrame(out).to_string())
