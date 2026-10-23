#!/usr/bin/env python3
"""DB - keyword scan of all v1 competency text (title, description, tasks, proficiency,
indicators, sector notes) for subsector terms. Supports v1_coverage judgments in
subsector_coverage_map.csv (judgments were then made by reading the matched text).
Usage: python3 -I v1_keyword_scan.py [--context PATTERN]
Input: /home/claude/emst/data/v1_baseline/*.csv (DE extract of the v1 database)."""
import csv, re, sys, glob, os
from collections import defaultdict
B = "/home/claude/emst/data/v1_baseline"
csv.field_size_limit(10**9)
text = defaultdict(str)
for fn in ["competencies.csv", "tasks.csv", "proficiency.csv", "indicators.csv", "sector_applications.csv"]:
    p = os.path.join(B, fn)
    if not os.path.exists(p):
        continue
    for r in csv.DictReader(open(p, encoding="utf-8")):
        code = r.get("code") or ""
        text[code] += " " + " ".join(v for k, v in r.items() if v and k not in ("key", "competency_key", "code"))
TERMS = {
 "drinking_water": r"drinking water|potable|water treatment|public water system|Safe Drinking",
 "wastewater": r"wastewater|sewage|sewer|biosolids|NPDES|POTW",
 "stormwater": r"stormwater|MS4|green infrastructure",
 "groundwater": r"groundwater|aquifer",
 "air": r"air quality|Clean Air|NAAQS|air permit",
 "solid_haz_waste": r"solid waste|landfill|hazardous waste|RCRA",
 "remediation": r"remediat|CERCLA|Superfund|brownfield",
 "energy": r"renewable|solar|wind energy|transmission line|oil and gas",
 "mining": r"\bmining\b|mine reclamation",
 "emergency_mgmt": r"emergency management|hazard mitigation|FEMA|Incident Command|\bNIMS\b",
 "esg": r"\bESG\b|sustainability report|ISSB|CSRD|\bGRI\b",
 "marine": r"marine|coastal|ocean",
 "cultural": r"cultural resource|archaeolog|Section 106",
 "transport": r"transportation|highway",
}
if len(sys.argv) > 2 and sys.argv[1] == "--context":
    pat = re.compile(sys.argv[2], re.I)
    for code, t in sorted(text.items()):
        for m in pat.finditer(t):
            print(code, "::", t[max(0, m.start()-70):m.end()+70].replace("\n", " "))
    sys.exit()
w = csv.writer(sys.stdout); w.writerow(["term_group", "n_competencies", "codes"])
for k, p in TERMS.items():
    hits = sorted(c for c, t in text.items() if re.search(p, t, re.I))
    w.writerow([k, len(hits), "|".join(hits)])
