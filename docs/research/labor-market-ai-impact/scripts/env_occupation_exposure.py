#!/usr/bin/env python3
"""
Score environmental occupations on three public AI-exposure indices and BLS projections, as
percentiles of the full occupational distribution.  Role: LM, EMST v2 Phase 2.

Inputs (cloned public GitHub repos; pass the parent folder as argv[1]):
  openai_GPTs-are-GPTs/repo/data/occ_level.csv        Eloundou et al. (Science 2024) occupation scores
  openai_GPTs-are-GPTs/repo/data/full_labelset.tsv    task-level E0/E1/E2 labels (O*NET 27.x tasks)
  openai_GPTs-are-GPTs/repo/data/occupation_2023_final.xlsx  BLS Employment Projections 2022-32 (Table 1.2)
  microsoft_working-with-ai/repo/ai_applicability_scores.csv, soc_metrics.csv, physical_tasks.csv  (Tomlinson et al., v1.1)
  AIOE-Data_AIOE/repo/AIOE_DataAppendix.xlsx, "Language Modeling AIOE and AIIE.xlsx"  (Felten, Raj & Seamans)
Output: ./env_occupation_exposure_scores.csv  (next to this script)

Percentiles are computed over all occupations present in each index (higher = more exposed / applicable).
BLS 2022-32 is SUPERSEDED by the 2024-34 cycle (released 2025) which could not be retrieved this session.
"""
import csv
import os
import sys

import pandas as pd

BASE = sys.argv[1]
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")  # outputs go to the role folder

ENV = [
    # soc6, label, emst_v1_family_hint
    ("19-1031", "Conservation Scientists", "F1|F3|F5|F10"),
    ("19-1032", "Foresters", "F1"),
    ("19-1023", "Zoologists and Wildlife Biologists", "F2|F5"),
    ("19-1013", "Soil and Plant Scientists", "F10"),
    ("19-2041", "Environmental Scientists and Specialists, Including Health", "F3|F5|F13"),
    ("19-2043", "Hydrologists", "F4"),
    ("19-2042", "Geoscientists, Except Hydrologists and Geographers", "F4"),
    ("19-2021", "Atmospheric and Space Scientists", "F6"),
    ("19-3051", "Urban and Regional Planners", "F9"),
    ("19-4042", "Environmental Science and Protection Technicians, Including Health", "F4|F13"),
    ("19-4071", "Forest and Conservation Technicians", "F1|F12"),
    ("19-4044", "Hydrologic Technicians", "F4"),
    ("19-5011", "Occupational Health and Safety Specialists", "F13"),
    ("19-5012", "Occupational Health and Safety Technicians", "F13"),
    ("11-9121", "Natural Sciences Managers", "F5|F8"),
    ("17-2081", "Environmental Engineers", "F3|F4"),
    ("17-3025", "Environmental Engineering Technologists and Technicians", "F4"),
    ("13-1041", "Compliance Officers", "F8|F13"),
    ("13-1199", "Business Operations Specialists, All Other (incl. Sustainability Specialists)", "F14"),
    ("45-4011", "Forest and Conservation Workers", "F1|F12"),
    ("33-2011", "Firefighters", "F12"),
    ("33-2022", "Forest Fire Inspectors and Prevention Specialists", "F12"),
    ("33-3031", "Fish and Game Wardens", "F2"),
    ("51-8031", "Water and Wastewater Treatment Plant and System Operators", "F4"),
    ("47-4041", "Hazardous Materials Removal Workers", "F13"),
    ("15-2051", "Data Scientists", "F7"),
    ("19-1029", "Biological Scientists, All Other", "F2|F5"),
    ("25-1053", "Environmental Science Teachers, Postsecondary", "F11"),
    ("25-1043", "Forestry and Conservation Science Teachers, Postsecondary", "F11"),
    ("13-2099", "Financial Specialists, All Other", "F15"),
    ("17-1022", "Surveyors", "F7"),
    ("17-1021", "Cartographers and Photogrammetrists", "F7"),
]
# O*NET-SOC detailed codes worth reporting separately (Eloundou index is at O*NET-SOC level)
ONET_EXTRA = ["19-1031.02", "19-1031.03", "19-2041.01", "19-2041.02", "19-2041.03", "13-1041.01",
              "13-1199.05", "11-1011.03", "15-1299.02", "19-4099.03", "19-2099.01", "19-1029.04"]


def pct_rank(series):
    return series.rank(pct=True)


def main():
    e = pd.read_csv(os.path.join(BASE, "openai_GPTs-are-GPTs/repo/data/occ_level.csv"))
    e["soc6"] = e["O*NET-SOC Code"].str[:7]
    for c in ["human_rating_beta", "dv_rating_beta"]:
        e[c + "_pct"] = pct_rank(e[c])
    e_soc = e.groupby("soc6")[["human_rating_beta", "dv_rating_beta", "human_rating_beta_pct", "dv_rating_beta_pct"]].mean()

    tl = pd.read_csv(os.path.join(BASE, "openai_GPTs-are-GPTs/repo/data/full_labelset.tsv"), sep="\t")
    tl["soc6"] = tl["O*NET-SOC Code"].str[:7]
    phys = pd.read_csv(os.path.join(BASE, "microsoft_working-with-ai/repo/physical_tasks.csv"))
    phys["Task ID"] = phys["Task ID"].astype(float)
    tl = tl.merge(phys, on="Task ID", how="left")
    tl["is_E1"] = tl["human_labels"].eq("E1")
    tl["is_E2"] = tl["human_labels"].eq("E2")
    tl["is_E0"] = tl["human_labels"].eq("E0")
    task_stats = tl.groupby("soc6").agg(n_tasks=("Task ID", "nunique"), share_E0_human=("is_E0", "mean"),
                                        share_E1_human=("is_E1", "mean"), share_E2_human=("is_E2", "mean"),
                                        share_physical_tasks=("Physical", "mean"))

    ms = pd.read_csv(os.path.join(BASE, "microsoft_working-with-ai/repo/soc_metrics.csv"))
    ms["ms_applic_pct"] = pct_rank(ms["ai_applicability_score_user"].add(0))
    msa = pd.read_csv(os.path.join(BASE, "microsoft_working-with-ai/repo/ai_applicability_scores.csv"))
    msa["ms_ai_applicability_pct"] = pct_rank(msa["ai_applicability_score"])
    ms = ms.merge(msa[["SOC Code", "ai_applicability_score", "ms_ai_applicability_pct"]], on="SOC Code", how="left")
    ms["ms_nonphys_pct"] = pct_rank(ms["ai_applicability_score_ai_nonphysical"])
    ms = ms.set_index("SOC Code")

    a = pd.read_excel(os.path.join(BASE, "AIOE-Data_AIOE/repo/AIOE_DataAppendix.xlsx"), sheet_name="Appendix A")
    a["aioe_pct"] = pct_rank(a["AIOE"])
    lm = pd.read_excel(os.path.join(BASE, "AIOE-Data_AIOE/repo/Language Modeling AIOE and AIIE.xlsx"), sheet_name="LM AIOE")
    lm["lm_aioe_pct"] = pct_rank(lm["Language Modeling AIOE"])
    a = a.merge(lm[["SOC Code", "Language Modeling AIOE", "lm_aioe_pct"]], on="SOC Code", how="outer")
    # AIOE is indexed on SOC 2010 codes for some occupations; map the unambiguous 2010->2018 changes used here
    soc2010_to_2018 = {"19-4091": "19-4042", "19-4093": "19-4071", "29-9011": "19-5011", "29-9012": "19-5012"}
    a["SOC Code"] = a["SOC Code"].replace(soc2010_to_2018)
    a = a.drop_duplicates("SOC Code").set_index("SOC Code")

    b = pd.read_excel(os.path.join(BASE, "openai_GPTs-are-GPTs/repo/data/occupation_2023_final.xlsx"), sheet_name="Table 1.2", header=None)
    # locate header row
    hdr = b.index[b.apply(lambda r: r.astype(str).str.contains("National Employment Matrix code").any(), axis=1)][0]
    b.columns = [str(c).strip() for c in b.iloc[hdr]]
    b = b.iloc[hdr + 1:]
    code_col = [c for c in b.columns if "Matrix code" in c][0]
    emp22 = [c for c in b.columns if "Employment, 2022" in c][0]
    chg = [c for c in b.columns if "Employment change, percent" in c][0]
    opn = [c for c in b.columns if "openings" in c.lower()][0]
    b = b[[code_col, emp22, chg, opn]].rename(columns={code_col: "soc", emp22: "bls_emp_2022_thousands", chg: "bls_pct_change_2022_32", opn: "bls_annual_openings_2022_32_thousands"})
    b = b.drop_duplicates("soc").set_index("soc")

    rows = []
    for soc, label, fam in ENV:
        r = {"soc_code": soc, "title": label, "emst_v1_families": fam}
        if soc in e_soc.index:
            for c in e_soc.columns:
                r["eloundou_" + c] = round(float(e_soc.loc[soc, c]), 3)
        if soc in task_stats.index:
            for c in task_stats.columns:
                r[c] = round(float(task_stats.loc[soc, c]), 3)
        if soc in ms.index:
            r["ms_ai_applicability"] = round(float(ms.loc[soc, "ai_applicability_score"]), 3)
            r["ms_ai_applicability_pct"] = round(float(ms.loc[soc, "ms_ai_applicability_pct"]), 3)
            r["ms_nonphysical_applicability"] = round(float(ms.loc[soc, "ai_applicability_score_ai_nonphysical"]), 3)
            r["ms_nonphysical_pct"] = round(float(ms.loc[soc, "ms_nonphys_pct"]), 3)
            r["ms_coverage_user"] = round(float(ms.loc[soc, "coverage_user"]), 3)
        if soc in a.index:
            r["aioe"] = round(float(a.loc[soc, "AIOE"]), 3) if pd.notna(a.loc[soc, "AIOE"]) else ""
            r["aioe_pct"] = round(float(a.loc[soc, "aioe_pct"]), 3) if pd.notna(a.loc[soc, "aioe_pct"]) else ""
            r["lm_aioe_pct"] = round(float(a.loc[soc, "lm_aioe_pct"]), 3) if pd.notna(a.loc[soc, "lm_aioe_pct"]) else ""
        if soc in b.index:
            for c in b.columns:
                r[c] = b.loc[soc, c]
        rows.append(r)
    for oc in ONET_EXTRA:
        sub = e[e["O*NET-SOC Code"] == oc]
        if len(sub):
            s = sub.iloc[0]
            rows.append({"soc_code": oc, "title": s["Title"] + " (O*NET-SOC detail)", "emst_v1_families": "",
                         "eloundou_human_rating_beta": round(s["human_rating_beta"], 3), "eloundou_dv_rating_beta": round(s["dv_rating_beta"], 3),
                         "eloundou_human_rating_beta_pct": round(s["human_rating_beta_pct"], 3), "eloundou_dv_rating_beta_pct": round(s["dv_rating_beta_pct"], 3)})
    cols = ["soc_code", "title", "emst_v1_families", "eloundou_human_rating_beta", "eloundou_human_rating_beta_pct", "eloundou_dv_rating_beta",
            "eloundou_dv_rating_beta_pct", "n_tasks", "share_E0_human", "share_E1_human", "share_E2_human", "share_physical_tasks",
            "ms_ai_applicability", "ms_ai_applicability_pct", "ms_nonphysical_applicability", "ms_nonphysical_pct", "ms_coverage_user",
            "aioe", "aioe_pct", "lm_aioe_pct", "bls_emp_2022_thousands", "bls_pct_change_2022_32", "bls_annual_openings_2022_32_thousands"]
    out = os.path.join(HERE, "env_occupation_exposure_scores.csv")
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(pd.read_csv(out).to_string())
    # reference points
    print("\nReference: median occupation Eloundou human beta =", round(e["human_rating_beta"].median(), 3),
          "; MS applicability median =", round(msa["ai_applicability_score"].median(), 3))


if __name__ == "__main__":
    main()
