#!/usr/bin/env python3
"""Rank agreement among public AI-exposure indices (all occupations and environmental subset). LM, EMST v2.
Usage: python3 -I index_agreement.py <ext_dir>   Output: ../index_agreement_spearman.csv"""
import os, sys
import pandas as pd
B = sys.argv[1]; OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "index_agreement_spearman.csv")
e = pd.read_csv(os.path.join(B, "openai_GPTs-are-GPTs/repo/data/occ_level.csv")); e["soc"] = e["O*NET-SOC Code"].str[:7]
e = e.groupby("soc")[["human_rating_beta", "dv_rating_beta"]].mean()
ms = pd.read_csv(os.path.join(B, "microsoft_working-with-ai/repo/soc_metrics.csv")).set_index("SOC Code")[["ai_applicability_score_ai_nonphysical"]]
msa = pd.read_csv(os.path.join(B, "microsoft_working-with-ai/repo/ai_applicability_scores.csv")).set_index("SOC Code")[["ai_applicability_score"]]
a = pd.read_excel(os.path.join(B, "AIOE-Data_AIOE/repo/AIOE_DataAppendix.xlsx"), sheet_name="Appendix A")
lm = pd.read_excel(os.path.join(B, "AIOE-Data_AIOE/repo/Language Modeling AIOE and AIIE.xlsx"), sheet_name="LM AIOE")
a = a.merge(lm[["SOC Code", "Language Modeling AIOE"]], on="SOC Code", how="outer")
a["SOC Code"] = a["SOC Code"].replace({"19-4091": "19-4042", "19-4093": "19-4071", "29-9011": "19-5011", "29-9012": "19-5012"})
a = a.drop_duplicates("SOC Code").set_index("SOC Code")[["AIOE", "Language Modeling AIOE"]]
d = e.join(msa, how="inner").join(ms, how="left").join(a, how="left")
ENV = ['19-1031','19-1032','19-1023','19-1013','19-2041','19-2043','19-2042','19-2021','19-3051','19-4042','19-4071','19-4044','19-5011','19-5012',
       '11-9121','17-2081','17-3025','13-1041','45-4011','33-2011','33-2022','33-3031','51-8031','47-4041']
rows = []
for scope, df in [("all_occupations", d), ("environmental_24", d.loc[[x for x in ENV if x in d.index]])]:
    c = df.corr(method="spearman")
    for i in c.index:
        for j in c.columns:
            if i < j:
                rows.append({"scope": scope, "n": len(df), "index_a": i, "index_b": j, "spearman_rho": round(c.loc[i, j], 3)})
r = d.rank(pct=True)
gap = (r["ai_applicability_score"] - r["human_rating_beta"]).loc[[x for x in ENV if x in r.index]]
rows.append({"scope": "environmental_24", "n": len(gap), "index_a": "MS_usage_pct_minus_Eloundou_human_pct", "index_b": "share_negative", "spearman_rho": round((gap < 0).mean(), 3)})
pd.DataFrame(rows).to_csv(OUT, index=False); print(pd.DataFrame(rows).to_string())
