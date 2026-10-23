"""Reproduce DC report figures from the OMB Federal AI Use Case Inventories.

Usage:
  python3 -I analysis_inventory.py <path/to/2025-Federal-Agency-AI-Use-Case-Inventory> [<path/to/2024-Federal-AI-Use-Case-Inventory>]

Clone sources (read-only, public):
  git clone --depth 1 https://github.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory.git   (DC-001; commit 06c7ebe used)
  git clone --depth 1 https://github.com/ombegov/2024-Federal-AI-Use-Case-Inventory.git          (DC-002)

Prints: stage x classification for USDA/DOI/EPA (report section 5.1), deployed GenAI/agentic cases,
high-impact and presumed-high-impact cases, bureau concentration, blockchain/AR absence checks,
and (if the 2024 repo is given) training-data documentation and data-catalog answers (section 5.6).
"""
import os, re, sys
import pandas as pd

ENV = ["USDA", "DOI", "EPA"]


def load_2025(repo):
    d = pd.read_csv(os.path.join(repo, "Data", "2025_individually_reported_AI_use_cases.csv"),
                    dtype=str, encoding="utf-8", encoding_errors="replace").fillna("")
    d["txt"] = (d.use_case_name + " " + d.problem_solved + " " + d.system_outputs + " " + d.benefits).str.lower()
    return d


def main():
    d = load_2025(sys.argv[1])
    print("2025 total rows:", len(d))
    x = d[d.agency.isin(ENV)]
    print("\nUSDA/DOI/EPA rows:", len(x))
    print(pd.crosstab(x.classification.replace("", "(unclassified)"), x.development_stage, margins=True))
    dep = x[(x.development_stage == "Deployed") & x.classification.isin(["Generative AI", "Agentic AI"])]
    print("\nDeployed GenAI/agentic:")
    for _, r in dep.iterrows():
        print(f"  {r.agency}/{r.agency_bureau[:30]} | {r.classification} | {r.use_case_name[:80]}")
    hi = x[x.is_high_impact.str.startswith("High") | x.is_high_impact.str.startswith("Presumed")]
    print("\nHigh-impact / presumed high-impact:")
    for _, r in hi.iterrows():
        print(f"  {r.agency}/{r.agency_bureau[:30]} | {r.development_stage} | {r.is_high_impact} | {r.use_case_name[:70]}")
    print("\nTopic areas:", x.topic_area.replace("", "(blank)").value_counts().head(5).to_dict())
    print("USGS rows:", (x.agency_bureau == "USGS").sum(), "| USDA Natural Resources and Environment rows:",
          (x.agency_bureau == "Natural Resources and Environment").sum())
    noaa = d[(d.agency == "DOC") & (d.agency_bureau == "NOAA")]
    print("NOAA rows (names only in 2025 consolidation):", len(noaa))
    for lab, p in [("blockchain/crypto", r"blockchain|cryptocurr|distributed ledger|\bdefi\b|smart contract"),
                   ("AR/VR", r"augmented reality|virtual reality|mixed reality|immersive|\bar-enabled")]:
        s = x[x.txt.str.contains(p, regex=True)]
        print(f"{lab} matches in USDA/DOI/EPA: {len(s)}", s.use_case_name.tolist())
    for k in ["DocketScope", "Forest Plan review", "Turbo plan", "Public Comment Analysis Tool", "I-NEPA"]:
        s = d[d.use_case_name.str.contains(k, regex=False)]
        for _, r in s.iterrows():
            print(f"  [{k}] {r.agency}/{r.agency_bureau} stage={r.development_stage} vendor={r.vendor_name[:40]} op={r.operational_date}")

    if len(sys.argv) > 2:
        a = pd.read_csv(os.path.join(sys.argv[2], "data", "2024_consolidated_ai_inventory_raw_v2.csv"),
                        dtype=str, encoding="latin-1").fillna("")
        a.columns = [c.replace("\x92", "'") for c in a.columns]
        e = a[a["Agency Abbreviation"].isin(ENV)]
        print("\n2024 rows by agency:", e.groupby("Agency Abbreviation").size().to_dict())
        q1 = [c for c in a.columns if c.startswith("Is there available documentation for the model training")][0]
        q2 = [c for c in a.columns if c.startswith("Do you have access to an enterprise data catalog")][0]
        for q in (q1, q2):
            print("\n", q[:90])
            print(pd.crosstab(e["Agency Abbreviation"], e[q].str[:45].replace("", "(blank)")).T)


if __name__ == "__main__":
    main()
