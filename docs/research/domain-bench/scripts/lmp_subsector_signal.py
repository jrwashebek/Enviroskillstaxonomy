#!/usr/bin/env python3
"""DB (Domain Expert Bench) - subsector demand signal from OpenLMP plan components.

Reads the read-only sister repo /home/claude/lmps (OpenLMP: machine-readable federal land
management plans) and counts plan components whose text matches subsector term patterns.
Purpose: show how often public-land plans themselves require competencies from subsectors
that EMST v1 covers thinly (minerals, energy corridors, air/smoke, water quality, cultural).

Caveats (read before citing):
- Regex matching on component text; no disambiguation. Counts are upper-bound signals, not
  validated classifications. Patterns are deliberately conservative (see PATTERNS).
- Corpus = OpenLMP plans as present on disk (217 component files: USDA Forest Service plus
  several state forestry/land agencies, grouped here as State_agencies); not representative of state,
  local, utility or private environmental work. It is a federal-land demand signal only.
Usage: python3 -I lmp_subsector_signal.py [/path/to/lmps] > lmp_subsector_demand_signal.csv
"""
import csv, glob, re, sys, os
from collections import Counter, defaultdict

ROOT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/lmps"
csv.field_size_limit(10**9)

PATTERNS = {
    # subsector_id: (label, regex)
    "W06": ("Water quality regulation (CWA/TMDL/303d/water quality)", r"water quality|\bTMDL|303\(d\)|Clean Water Act|best management practices? for water"),
    "W01": ("Drinking/source water protection", r"drinking water|source water|municipal (water|watershed)|public water suppl"),
    "W05": ("Groundwater", r"groundwater|ground water|aquifer"),
    "P01": ("Air quality & smoke", r"air quality|\bsmoke\b|Clean Air Act|class I (area|airshed)|visibility|regional haze"),
    "E04": ("Minerals, mining & reclamation", r"\bmining\b|\bmines?\b(?! the)|locatable|leasable mineral|mineral (material|development|exploration|withdrawal|entry|lease)|abandoned mine|reclamation"),
    "E03": ("Oil & gas / fluid minerals", r"oil and gas|oil & gas|fluid mineral|\bwell pads?\b|natural gas"),
    "E01": ("Renewable energy siting", r"renewable energy|\bsolar\b|wind (energy|turbine|farm|development|facilit)|geothermal"),
    "E02": ("Transmission, pipelines & utility corridors", r"transmission line|utility corridor|energy corridor|\bpipelines?\b|power ?lines?|right[- ]of[- ]way"),
    "P04": ("Hazardous materials & contamination", r"hazardous (materials?|substances?|wastes?)|CERCLA|contaminat"),
    "C01": ("Climate & carbon", r"climate change|carbon (storage|sequestration|stocks?)|greenhouse gas"),
    "L11": ("Cultural resources & heritage", r"cultural resource|heritage resource|historic propert|archaeolog|Section 106|National Historic Preservation"),
    "L10": ("Recreation", r"recreation"),
    "L05": ("Rangeland & grazing", r"grazing|livestock|rangeland|allotment"),
    "L07": ("Wildland fire & fuels", r"\bfire\b|\bfuels?\b|wildfire|prescribed burn"),
    "L01": ("Timber & silviculture", r"timber|silvicultur|harvest"),
    "L02L03": ("Wildlife, fish & habitat", r"wildlife|\bfish|habitat"),
    "U02": ("Roads & transportation", r"\broads?\b|transportation system|travel management"),
    "C03": ("Hazards, floods & emergencies", r"\bflood|landslide|emergency|public safety|avalanche"),
    "P02": ("Solid waste & sanitation", r"solid waste|garbage|\btrash\b|sanitation|wastewater|sewage"),
}

def main():
    files = sorted(glob.glob(os.path.join(ROOT, "plans/*/*/*/components.csv")))
    total = 0
    counts = Counter()
    by_agency = defaultdict(Counter)
    agency_totals = Counter()
    comp = {k: re.compile(p, re.I) for k, (_, p) in PATTERNS.items()}
    for f in files:
        with open(f, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                total += 1
                ag_raw = " ".join((r.get("agency", "") or "unknown").split())
                ag = "USDA_Forest_Service" if ag_raw.startswith("USDA Forest Service") else "State_agencies"
                agency_totals[ag] += 1
                t = r.get("text") or ""
                for k, rx in comp.items():
                    if rx.search(t):
                        counts[k] += 1
                        by_agency[k][ag] += 1
    w = csv.writer(sys.stdout)
    agencies = sorted(agency_totals)
    w.writerow(["subsector_id", "label", "components_matching", "share_of_all_components", "total_components", "files"]
               + [f"matching_{a.replace(' ', '_')}" for a in agencies] + ["pattern"])
    for k, (label, pat) in PATTERNS.items():
        w.writerow([k, label, counts[k], f"{counts[k]/total:.4f}" if total else "", total, len(files)]
                   + [by_agency[k][a] for a in agencies] + [pat])

if __name__ == "__main__":
    main()
