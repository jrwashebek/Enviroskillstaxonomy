#!/usr/bin/env python3
"""Count 2025 Federal AI Use Case Inventory entries in environmental bureaus by stage and function; extract COTS genAI rows. LM, EMST v2.
Usage: python3 -I omb_inventory_env.py <path to cloned ombegov/2025-Federal-Agency-AI-Use-Case-Inventory>
Writes ../omb_ai_inventory_env_bureaus_2025.csv, ../omb_ai_inventory_env_function_counts.csv, ../omb_cots_ai_env_departments_2025.csv"""
import os, sys
import pandas as pd
R = sys.argv[1]; H = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
d = pd.read_csv(os.path.join(R, "Data/2025_individually_reported_AI_use_cases.csv"), encoding="utf-8", low_memory=False)
envb = {"USGS","FWS","BOR","BLM","BSEE","NPS","BIA","OSMRE","BOEM","Natural Resources and Environment","Farm Production and Conservation","NOAA"}
e = d[(d.agency_bureau.isin(envb)) | (d.agency == "EPA")].copy()
e["unit"] = e.agency_bureau.where(e.agency != "EPA", "EPA")
print("env-bureau use cases", len(e)); print(pd.crosstab(e.unit, e.development_stage.fillna("not reported")).to_string()); print(e.classification.value_counts().to_dict())
txt = e.use_case_name.fillna("") + " " + e.problem_solved.fillna("") + " " + e.system_outputs.fillna("")
kw = {"species/wildlife/acoustic/camera": r"species|wildlife|acoustic|camera trap|\bbird|\bfish|marine mammal|whale|coral",
      "fire/smoke": r"wildfire|\bfire\b|smoke|burn sever", "remote sensing/imagery/lidar": r"satellite|imagery|remote sens|lidar|aerial|orthoimag",
      "NEPA/env review/permitting": r"NEPA|environmental review|environmental impact|permit", "public comment": r"public comment|comment analysis",
      "genAI drafting/summarization/chat": r"generative|\bLLM|large language|chatbot|summariz|\bdraft", "inspection/compliance/enforcement": r"inspect|compliance|enforcement|violation",
      "data QA/QC & processing": r"quality control|QA/QC|\bQC\b|data processing|anomal|data cleaning", "water/hydrology": r"streamflow|hydrolog|water quality|groundwater|flood",
      "weather/climate forecasting": r"forecast|weather|climate model", "records/admin/HR/finance": r"records|FOIA|invoice|procure|human resources|\bHR\b|budget|finance|acquisition"}
rows = []
for k, v in kw.items():
    mk = txt.str.contains(v, case=False, regex=True); sub = e[mk]
    rows.append((k, int(mk.sum()), int((sub.development_stage == "Deployed").sum()), ", ".join(f"{a}:{b}" for a, b in sub.unit.value_counts().head(5).items())))
e[["agency","agency_bureau","unit","use_case_name","development_stage","topic_area","classification"]].to_csv(os.path.join(H, "omb_ai_inventory_env_bureaus_2025.csv"), index=False)
pd.DataFrame(rows, columns=["function_keyword_family","n_use_cases","n_deployed","top_units"]).to_csv(os.path.join(H, "omb_ai_inventory_env_function_counts.csv"), index=False)
c = pd.read_csv(os.path.join(R, "Data/2025_consolidated_COTS_AI_use_cases.csv"), encoding="utf-8", low_memory=False)
c[c.Agency.str.contains("Agriculture|Interior|Commerce|Environmental", case=False, na=False)].to_csv(os.path.join(H, "omb_cots_ai_env_departments_2025.csv"), index=False)
print(pd.DataFrame(rows).to_string())
