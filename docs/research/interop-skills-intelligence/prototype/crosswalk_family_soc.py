#!/usr/bin/env python3
"""Re-express v1's family -> SOC crosswalk as SSSOM, with code/title verification flags.

Verification source: O*NET-SOC 2019 occupation descriptions carried in the official ESCO-O*NET crosswalk (v1, Sep 2022,
ESCO Secretariat with USDOL/ETA), as redistributed in Avature/melo-benchmark (data/raw/crosswalks_standard/usa_en).
Only code/title consistency is checked here. Whether a family *should* map to a code is FH's call (CA audit §6).
"""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
from emst_link import config as C  # noqa: E402

# code -> (verified O*NET-SOC 2019 meaning from the crosswalk description, consistent with v1 title?)
VERIFIED = {
    "19-1032": ("Foresters", True), "19-1031": ("Conservation Scientists", True),
    "19-1023": ("Zoologists and Wildlife Biologists", True), "17-2081": ("Environmental Engineers", True),
    "19-2043": ("Hydrologists", True), "19-2021": ("Atmospheric and Space Scientists", True),
    "15-2051": ("Data Scientists", True), "23-1011": ("Lawyers", True), "11-9199": ("Managers, All Other", True),
    "19-3051": ("Urban and Regional Planners", True),
    "19-1012": ("Food Scientists and Technologists (description: chemistry/microbiology of food processing)", False),
    "25-2031": ("Secondary School Teachers", True), "25-4031": ("Library Technicians", True),
    "33-1021": ("First-Line Supervisors of Firefighting and Prevention Workers (Fire Inspectors are 33-2021; Forest Fire Inspectors 33-2022)", False),
    "29-9021": ("Health Information Technologists and Medical Registrars", True),
    "13-1199": ("Business Operations Specialists, All Other", True), "13-2099": ("Financial Specialists, All Other", True),
}
TARGET_DOUBT = {  # code/title consistent but the target looks wrong for the family [J]; FH to adjudicate
    ("F8", "23-1011"): "Policy roles are rarely lawyers; consider 19-3094 Political Scientists, 11-9199.02 Compliance Managers, 19-2041.01 Climate Change Policy Analysts",
    ("F11", "25-4031"): "Library Technicians is not an environmental-education target; consider 25-9031 Instructional Coordinators or interpreter roles",
    ("F13", "29-9021"): "Health information technology is not environmental health/justice; consider 19-2041 Environmental Scientists and Specialists, Including Health",
    ("F14", "11-9199"): "O*NET-SOC 2019 has 13-1199.05 Sustainability Specialists (verified in crosswalk); use detailed O*NET codes",
    ("F3", "17-2081"): "O*NET-SOC 2019 has 19-2041.02 Environmental Restoration Planners (verified in crosswalk)",
    ("F7", "19-1031"): "O*NET-SOC 2019 has 19-2099.01 Remote Sensing Scientists and Technologists (verified in crosswalk)",
}
PRED = {"High": "skos:closeMatch", "Medium": "skos:relatedMatch", "Low": "skos:relatedMatch"}

HEADER = """# curie_map:
#   EMSTv1fam: https://w3id.org/emst/v1/family/
#   SOC2018: https://www.bls.gov/soc/2018/#
#   skos: http://www.w3.org/2004/02/skos/core#
#   semapv: https://w3id.org/semapv/vocab/
#   emstagent: https://w3id.org/emst/agent/
# mapping_set_id: https://w3id.org/emst/mappings/emst-v1-family-soc2018/0.1.0
# mapping_set_version: 0.1.0-draft
# mapping_set_title: EMST v1 profession families to SOC 2018 detailed occupations (re-expressed v1 sheet)
# license: https://creativecommons.org/licenses/by/4.0/
# subject_source_version: v1 Labor Market Crosswalk sheet (data/v1_baseline/labor_market_crosswalk.csv)
# object_source_version: SOC 2018 (O*NET-SOC 2019 descriptions used for verification)
# comment: v1 mapping_quality kept in 'other'. Predicate derived from quality (High->closeMatch else relatedMatch). Not reviewed by FH.
"""


def main():
    x = pd.read_csv(C.V1_BASELINE / "labor_market_crosswalk.csv", dtype=str, keep_default_na=False)
    rows = []
    for r in x.itertuples():
        for role, code, title in [("primary", r.primary_soc_code, r.primary_soc_title), ("secondary", r.secondary_soc_code, r.secondary_soc_title)]:
            if not code:
                continue
            ver, ok = VERIFIED.get(code, ("not verified", None))
            flags = []
            if ok is False:
                flags.append(f"CODE/TITLE MISMATCH: v1 title '{title}' but {code} = {ver}")
            doubt = TARGET_DOUBT.get((r.family_code, code))
            if doubt:
                flags.append("TARGET DOUBT: " + doubt)
            rows.append({
                "record_id": f"emst-v1-fam-soc:{r.family_code}:{role}", "subject_id": f"EMSTv1fam:{r.family_code}", "subject_label": r.family_name,
                "predicate_id": PRED.get(r.mapping_quality, "skos:relatedMatch"), "object_id": f"SOC2018:{code}", "object_label": title,
                "mapping_justification": "semapv:UnspecifiedMatching", "confidence": {"High": 0.8, "Medium": 0.5, "Low": 0.3}.get(r.mapping_quality, ""),
                "author_id": "emstagent:v1-single-analyst", "mapping_date": "2026-02 (v1)", "review_status": "needs-review" if flags else "candidate",
                "other": f"v1_role={role};v1_mapping_quality={r.mapping_quality};v1_notes={r.mapping_notes}",
                "comment": " | ".join(flags),
            })
    out = pd.DataFrame(rows)
    p = HERE.parent / "crosswalks" / "emst_v1_family_to_soc2018.sssom.tsv"
    with open(p, "w") as f:
        f.write(HEADER)
        out.to_csv(f, sep="\t", index=False)
    print(len(out), out.review_status.value_counts().to_dict())


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(HERE))
    main()
