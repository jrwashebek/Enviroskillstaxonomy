#!/usr/bin/env python3
"""Build the Learning & Curriculum (LC) crosswalk tables.

Outputs (written to the role folder, one level above scripts/):
  cip_soc_env_crosswalk.csv      CIP 2020 program -> SOC 2018 occupation -> EMST v1 families/domains
  accreditation_emst_crosswalk.csv  accreditor criterion -> EMST v1 competency codes (paraphrased criteria)

Inputs (read-only):
  data/v1_baseline/competencies.csv, family_assignments.csv  (EMST v1 normalized baseline)

Provenance and limits (see report.md section 6):
  * CIP codes/titles and SOC codes/titles are entered from the published CIP 2020 and SOC 2018
    structures as known to the LC analyst. The official NCES CIP2020-SOC2018 crosswalk file could
    not be retrieved in this session (O*NET OnLine crosswalk page blocked; NCES PDF is the usage
    guideline only). Every row therefore carries "nces_check=verify" in notes and must be checked
    against the official file before use in funding or supply analysis.
  * emst_v1_families is LC judgment. emst_v1_domains is COMPUTED: domains holding >=15% of the
    Core competencies of the listed families in the v1 baseline. Domain 3 (Management) is Core only
    for F14/F15 in v1, so it is under-represented by construction; this is a v1 tagging artefact.
  * Accreditation criteria are PARAPHRASED (third-party text is not copied). Criterion IDs follow
    the accreditor's own numbering so users can look up the authoritative wording.

Run:  python3 -I docs/research/learning-curriculum/scripts/build_lc_crosswalks.py   (from repo root)
"""
import csv
import collections
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # role folder (outputs live here)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
BASE = os.path.join(ROOT, "data", "v1_baseline")

# ---------------------------------------------------------------- v1 lookups
comp_codes = {r["code"] for r in csv.DictReader(open(os.path.join(BASE, "competencies.csv"), encoding="utf-8"))}
fam_dom = collections.defaultdict(collections.Counter)
fam_names = {}
for r in csv.DictReader(open(os.path.join(BASE, "family_assignments.csv"), encoding="utf-8")):
    fam_names[r["family_code"]] = r["family_name"]
    if r["assignment"].strip().lower() == "core":
        fam_dom[r["family_code"]][r["code"].split(".")[0]] += 1


def domains_for(fams, threshold=0.15):
    c = collections.Counter()
    for f in fams:
        c.update(fam_dom[f])
    tot = sum(c.values()) or 1
    return "|".join(sorted((d for d, n in c.items() if n / tot >= threshold), key=int))


# ---------------------------------------------------------------- CIP -> SOC -> EMST
# (cip_code, cip_title, [(soc_code, soc_title, soc_note)], families, program_note)
CIP = [
    ("03.0101", "Natural Resources/Conservation, General",
     [("19-1031", "Conservation Scientists", ""),
      ("19-4071", "Forest and Conservation Technicians", "associate/technician level"),
      ("11-9121", "Natural Sciences Managers", "advancement occupation")],
     ["F5", "F3"], "Broad NR programs; often SAF NREM-standard candidates."),
    ("03.0103", "Environmental Studies",
     [("19-2041", "Environmental Scientists and Specialists, Including Health", "policy-leaning roles; O*NET 19-2041.01 Climate Change Policy Analysts"),
      ("25-1053", "Environmental Science Teachers, Postsecondary", "graduate level only")],
     ["F8", "F5", "F13"], "Interdisciplinary (GCSE/IES) programs; no specialized accreditor; outcomes vary widely by program."),
    ("03.0104", "Environmental Science",
     [("19-2041", "Environmental Scientists and Specialists, Including Health", "largest single env-science SOC; absent from v1 crosswalk"),
      ("19-4042", "Environmental Science and Protection Technicians, Including Health", "associate/entry level"),
      ("11-9121", "Natural Sciences Managers", "advancement occupation")],
     ["F5", "F4", "F13"], "Core supply program for state environmental scientist classes (pathway LC-PW-01)."),
    ("03.0201", "Natural Resources Management and Policy",
     [("19-1031", "Conservation Scientists", ""),
      ("19-2041", "Environmental Scientists and Specialists, Including Health", ""),
      ("11-9121", "Natural Sciences Managers", "")],
     ["F5", "F8", "F9"], "Statecraft-heavy NR programs; SAF NREM standard applies where accredited."),
    ("03.0204", "Environmental/Natural Resource Economics",
     [("19-3011", "Economists", "graduate level typical")],
     ["F15", "F8"], "Supplies resource-economics and valuation competencies (6.3.x)."),
    ("03.0205", "Water, Wetlands, and Marine Resources Management",
     [("19-1031", "Conservation Scientists", ""),
      ("19-2041", "Environmental Scientists and Specialists, Including Health", "wetland/permitting roles"),
      ("11-9121", "Natural Sciences Managers", "O*NET 11-9121.02 Water Resource Specialists")],
     ["F4", "F3"], "Wetland delineation and permitting roles (state/consulting)."),
    ("03.0206", "Land Use Planning and Management/Development",
     [("19-3051", "Urban and Regional Planners", ""),
      ("19-1031", "Conservation Scientists", "public-lands planning roles")],
     ["F9"], "Public land management planning (6.2.3) and comprehensive planning (6.2.1)."),
    ("03.0207", "Natural Resource Recreation and Tourism",
     [("19-1031", "Conservation Scientists", "O*NET 19-1031.03 Park Naturalists")],
     ["F11", "F5"], "Interpretation and visitor-services roles (5.1.3, 5.5.1)."),
    ("03.0208", "Natural Resources Law Enforcement and Protective Services",
     [("33-3031", "Fish and Game Wardens", ""),
      ("33-2022", "Forest Fire Inspectors and Prevention Specialists", "")],
     ["F2", "F12"], "Enforcement (6.1.5) and safety (4.4.x); state POST requirements apply (SL lane)."),
    ("03.0209", "Energy and Environmental Policy",
     [("19-2041", "Environmental Scientists and Specialists, Including Health", "O*NET 19-2041.01 Climate Change Policy Analysts")],
     ["F8", "F6"], "Policy and permitting statecraft; NEPA/permitting specialist supply (pathway LC-PW-02)."),
    ("03.0301", "Fishing and Fisheries Sciences and Management",
     [("19-1023", "Zoologists and Wildlife Biologists", "fisheries biologists"),
      ("11-9121", "Natural Sciences Managers", "")],
     ["F2"], "AFS certification is the professional credential (not accreditation)."),
    ("03.0501", "Forestry, General",
     [("19-1032", "Foresters", ""),
      ("19-4071", "Forest and Conservation Technicians", ""),
      ("45-4011", "Forest and Conservation Workers", "entry/field level"),
      ("25-1043", "Forestry and Conservation Science Teachers, Postsecondary", "graduate level only")],
     ["F1", "F12"], "SAF Forestry standard; see accreditation_emst_crosswalk.csv."),
    ("03.0502", "Forest Sciences and Biology",
     [("19-1032", "Foresters", ""), ("19-1031", "Conservation Scientists", "")],
     ["F1", "F5"], "Science-leaning forestry programs."),
    ("03.0506", "Forest Management/Forest Resources Management",
     [("19-1032", "Foresters", ""), ("11-9121", "Natural Sciences Managers", "")],
     ["F1"], "SAF Forestry standard."),
    ("03.0508", "Urban Forestry",
     [("19-1032", "Foresters", "urban foresters"),
      ("37-3013", "Tree Trimmers and Pruners", "arborist field roles; ISA credentials common")],
     ["F1", "F3"], "SAF Urban Forestry standard (tree risk assessment criterion)."),
    ("03.0510", "Forest Resources Production and Management",
     [("19-1032", "Foresters", ""),
      ("45-1011", "First-Line Supervisors of Farming, Fishing, and Forestry Workers", "operations supervision")],
     ["F1"], "Operations/production focus; v1 lacks harvesting-systems competency (gap)."),
    ("03.0511", "Forest Technology/Technician",
     [("19-4071", "Forest and Conservation Technicians", ""),
      ("45-4011", "Forest and Conservation Workers", "")],
     ["F1", "F12"], "SAF Forest Technology standard (2-year). Feeder for reskilling pathway LC-PW-03."),
    ("03.0601", "Wildlife, Fish and Wildlands Science and Management",
     [("19-1023", "Zoologists and Wildlife Biologists", ""),
      ("19-1031", "Conservation Scientists", ""),
      ("33-3031", "Fish and Game Wardens", "")],
     ["F2", "F5"], "TWS Certified Wildlife Biologist uses coursework standards (credential, not accreditation). Pathway LC-PW-04 origin."),
    ("01.0308", "Agroecology and Sustainable Agriculture",
     [("19-1013", "Soil and Plant Scientists", ""),
      ("25-9021", "Farm and Home Management Educators", "extension roles; v1 mislabels this as 19-1012")],
     ["F10"], "Extension/NRCS-type roles."),
    ("01.1201", "Soil Science and Agronomy, General",
     [("19-1013", "Soil and Plant Scientists", ""),
      ("19-4012", "Agricultural Technicians", "")],
     ["F10", "F4"], "Soil survey and conservation planning."),
    ("04.0301", "City/Urban, Community, and Regional Planning",
     [("19-3051", "Urban and Regional Planners", "")],
     ["F9"], "PAB-accredited planning programs (accreditor not reviewed this session)."),
    ("14.1401", "Environmental/Environmental Health Engineering",
     [("17-2081", "Environmental Engineers", ""),
      ("11-9041", "Architectural and Engineering Managers", "advancement occupation")],
     ["F4", "F13", "F3"], "ABET EAC Environmental Engineering program criteria; PE licensure path."),
    ("14.0805", "Water Resources Engineering",
     [("17-2051", "Civil Engineers", ""), ("17-2081", "Environmental Engineers", "")],
     ["F4"], "ABET EAC civil/environmental criteria."),
    ("15.0506", "Water Quality and Wastewater Treatment Management and Recycling Technology/Technician",
     [("51-8031", "Water and Wastewater Treatment Plant and System Operators", "state operator certification required"),
      ("19-4042", "Environmental Science and Protection Technicians, Including Health", "lab/compliance technician")],
     ["F4"], "Workforce Pell and Registered Apprenticeship candidate; v1 lacks treatment-operations competencies (pathway LC-PW-05)."),
    ("15.0507", "Environmental Engineering Technology/Environmental Technology",
     [("17-3025", "Environmental Engineering Technologists and Technicians", ""),
      ("19-4042", "Environmental Science and Protection Technicians, Including Health", "")],
     ["F4", "F13"], "ABET ETAC Environmental Engineering Technology program criteria."),
    ("15.0508", "Hazardous Materials Management and Waste Technology/Technician",
     [("47-4041", "Hazardous Materials Removal Workers", "HAZWOPER required"),
      ("19-4042", "Environmental Science and Protection Technicians, Including Health", ""),
      ("19-5011", "Occupational Health and Safety Specialists", "")],
     ["F13", "F14"], "Waste/remediation sector; v1 coverage thin (3.7.2, 4.4.4)."),
    ("15.0599", "Environmental Control Technologies/Technicians, Other",
     [("19-4042", "Environmental Science and Protection Technicians, Including Health", ""),
      ("17-3025", "Environmental Engineering Technologists and Technicians", "")],
     ["F4", "F13"], "Residual code; check program content before relying on mapping."),
    ("15.1102", "Surveying Technology/Surveying",
     [("17-1022", "Surveyors", "state licensure"),
      ("17-3031", "Surveying and Mapping Technicians", "")],
     ["F7"], "Geospatial supply (2.1.3, 2.1.4)."),
    ("26.1301", "Ecology",
     [("19-1029", "Biological Scientists, All Other", "ecologists fall here"),
      ("19-2041", "Environmental Scientists and Specialists, Including Health", "consulting ecologists")],
     ["F5", "F3"], "ESA Certified Ecologist is the credential (not accreditation). Pathway LC-PW-04 destination."),
    ("26.1304", "Aquatic Biology/Limnology",
     [("19-1029", "Biological Scientists, All Other", ""),
      ("19-1023", "Zoologists and Wildlife Biologists", "fisheries/aquatic roles")],
     ["F2", "F4"], ""),
    ("26.1305", "Environmental Biology",
     [("19-1029", "Biological Scientists, All Other", ""),
      ("19-2041", "Environmental Scientists and Specialists, Including Health", "")],
     ["F5"], ""),
    ("26.1307", "Conservation Biology",
     [("19-1029", "Biological Scientists, All Other", ""),
      ("19-1023", "Zoologists and Wildlife Biologists", "")],
     ["F5", "F2"], ""),
    ("30.3301", "Sustainability Studies",
     [("13-1199", "Business Operations Specialists, All Other", "O*NET 13-1199.05 Sustainability Specialists"),
      ("11-1011", "Chief Executives", "O*NET 11-1011.03 Chief Sustainability Officers; advancement only"),
      ("19-2041", "Environmental Scientists and Specialists, Including Health", "")],
     ["F14", "F8"], "Fast-growing degree category (GCSE 2024); no specialized accreditor."),
    ("30.4401", "Geography and Environmental Studies",
     [("19-3092", "Geographers", ""),
      ("19-2041", "Environmental Scientists and Specialists, Including Health", "")],
     ["F9", "F7"], "New in CIP 2020."),
    ("30.7001", "Data Science, General",
     [("15-2051", "Data Scientists", "no environmental-informatics SOC exists")],
     ["F7"], "New in CIP 2020; environmental data roles undercounted (v1 F7 note)."),
    ("40.0401", "Atmospheric Sciences and Meteorology, General",
     [("19-2021", "Atmospheric and Space Scientists", "")],
     ["F6"], "Fire-weather (IMET) and climate services feeder."),
    ("40.0601", "Geology/Earth Science, General",
     [("19-2042", "Geoscientists, Except Hydrologists and Geographers", ""),
      ("19-4043", "Geological Technicians, Except Hydrologic Technicians", "")],
     ["F4"], ""),
    ("40.0605", "Hydrology and Water Resources Science",
     [("19-2043", "Hydrologists", ""),
      ("19-4044", "Hydrologic Technicians", "new detailed code in SOC 2018")],
     ["F4"], ""),
    ("43.0206", "Wildland/Forest Firefighting and Investigation",
     [("33-2011", "Firefighters", "wildland firefighters; federal GS-0456 series (FH lane)"),
      ("33-2022", "Forest Fire Inspectors and Prevention Specialists", ""),
      ("33-1021", "First-Line Supervisors of Firefighting and Prevention Workers", "v1 mislabels this code as 'Fire Inspectors'")],
     ["F12"], "Operational qualification runs through NWCG, not degrees; credit-for-NWCG-training is the academic hook."),
    ("43.0302", "Crisis/Emergency/Disaster Management",
     [("11-9161", "Emergency Management Directors", "")],
     ["F12", "F6"], "Fire intelligence and all-hazards coordination roles (pathway LC-PW-03 branch B)."),
    ("45.0701", "Geography",
     [("19-3092", "Geographers", ""),
      ("25-1064", "Geography Teachers, Postsecondary", "graduate level only")],
     ["F9", "F7"], ""),
    ("45.0702", "Geographic Information Science and Cartography",
     [("15-1299", "Computer Occupations, All Other", "O*NET 15-1299.02 Geographic Information Systems Technologists and Technicians"),
      ("17-1021", "Cartographers and Photogrammetrists", ""),
      ("19-2099", "Physical Scientists, All Other", "O*NET 19-2099.01 Remote Sensing Scientists and Technologists"),
      ("19-4099", "Life, Physical, and Social Science Technicians, All Other", "O*NET 19-4099.03 Remote Sensing Technicians")],
     ["F7"], "Primary academic home for remote-sensing reskilling (pathway LC-PW-03); certificates are Workforce Pell candidates."),
    ("51.2202", "Environmental Health",
     [("19-2041", "Environmental Scientists and Specialists, Including Health", "REHS/RS and state sanitarian registration"),
      ("19-4042", "Environmental Science and Protection Technicians, Including Health", ""),
      ("19-5011", "Occupational Health and Safety Specialists", "")],
     ["F13"], "EHAC-accredited programs (180-hour practicum). v1 lacks food/vector/epidemiology competencies."),
    ("51.2206", "Occupational Health and Industrial Hygiene",
     [("19-5011", "Occupational Health and Safety Specialists", ""),
      ("19-5012", "Occupational Health and Safety Technicians", "")],
     ["F13"], "ABET ANSAC accredits some IH programs (not reviewed this session)."),
    ("22.0207", "Energy, Environment, and Natural Resources Law",
     [("23-1011", "Lawyers", "post-JD/LLM")],
     ["F8"], "Graduate law; statecraft depth (6.1.x, 6.4.x)."),
    ("44.0501", "Public Policy Analysis, General",
     [("19-3094", "Political Scientists", "weak fit: SOC has no policy-analyst code")],
     ["F8"], "Environmental policy analysts are scattered across SOC codes (v1 F8 'Low' mapping quality)."),
    ("13.1316", "Science Teacher Education/General Science Teacher Education",
     [("25-2031", "Secondary School Teachers, Except Special and Career/Technical Education", "")],
     ["F11"], "No dedicated environmental-educator CIP verified this session; nonformal educators map poorly to SOC."),
]

SRC_BASE = "LC-012|LC-013|LC-038|LC-031"
ACCRED = {"03.0501": "LC-001", "03.0502": "LC-001", "03.0506": "LC-001", "03.0508": "LC-001",
          "03.0510": "LC-001", "03.0511": "LC-001", "03.0101": "LC-001", "03.0201": "LC-001",
          "14.1401": "LC-002|LC-003", "14.0805": "LC-002", "15.0507": "LC-004", "51.2202": "LC-005",
          "30.3301": "LC-011", "03.0103": "LC-010", "13.1316": "LC-009"}
PATHWAY = {"03.0104": "LC-PW-01", "03.0209": "LC-PW-02", "03.0511": "LC-PW-03", "45.0702": "LC-PW-03",
           "43.0302": "LC-PW-03", "03.0601": "LC-PW-04", "26.1301": "LC-PW-04", "15.0506": "LC-PW-05"}


def write_cip():
    out = os.path.join(HERE, "cip_soc_env_crosswalk.csv")
    rows = []
    for cip, title, socs, fams, pnote in CIP:
        for f in fams:
            assert f in fam_names, f"unknown family {f}"
        doms = domains_for(fams)
        for soc, stitle, snote in socs:
            notes = ["nces_check=verify"]
            if snote:
                notes.append(snote)
            if pnote:
                notes.append(pnote)
            if cip in PATHWAY:
                notes.append("pathway=" + PATHWAY[cip])
            src = SRC_BASE + ("|" + ACCRED[cip] if cip in ACCRED else "")
            rows.append({"cip_code": cip, "cip_title": title, "soc_code": soc, "soc_title": stitle,
                         "emst_v1_families": "|".join(fams), "emst_v1_domains": doms,
                         "notes": "; ".join(notes), "source_ids": src})
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        w.writerows(rows)
    return out, len(rows), len(CIP)


# ---------------------------------------------------------------- accreditation -> EMST
# (accreditor, standard, criterion_id, paraphrase, verb_tier, emst_codes, target_level, coverage, gap_note, source_ids)
# verb_tier mirrors SAF's own three tiers: knowledge | understanding | ability (ABET/EHAC rows use 'ability' or 'content').
A = [
    # SAF Forestry Standard (professional degree) - integrative components
    ("SAF", "Forestry", "C4-5", "Builds oral and written communication for professional and lay audiences", "ability", "5.1.1|5.1.2", "intermediate", "full", ""),
    ("SAF", "Forestry", "C4-6", "Fosters analytical and critical reasoning, systematic problem solving and decision making", "ability", "2.2.2|3.1.3|6.2.5", "intermediate", "partial", "No generic critical-reasoning competency in v1; distributed across codes."),
    ("SAF", "Forestry", "C4-7", "Recognizes connections among natural, technical, economic and social systems", "ability", "1.1.1|6.3.2|6.3.4", "intermediate", "partial", "Systems thinking appears only in two proficiency statements (1.8.5, 4.6.1)."),
    ("SAF", "Forestry", "C4-8", "Recognizes and demonstrates professional behaviors and safe outdoor work practices, including PPE", "ability", "4.4.1|4.4.2", "foundational", "partial", "Workplace conduct not explicit in v1."),
    ("SAF", "Forestry", "C4-9", "Recognizes and addresses ethical questions; role of professional codes of ethics", "ability", "7.1.3|3.5.5", "foundational", "partial", "v1 D7.1 is specialized (data sovereignty, intervention, regulatory integrity, AI); no general professional-ethics competency."),
    # Disciplinary A: Ecology and biology
    ("SAF", "Forestry", "C4-A.1", "Knows woody-plant taxonomy, identification, distribution and associated forest biota", "knowledge", "4.1.1", "foundational", "partial", "GAP: no plant/tree identification competency in v1 (only 4.1.1 indicators). Candidate LC-C-03."),
    ("SAF", "Forestry", "C4-A.2", "Identifies regionally important trees by leaf, twig, bark and fruit", "ability", "4.1.1", "foundational", "none", "GAP: dendrology absent. Candidate LC-C-03."),
    ("SAF", "Forestry", "C4-A.3", "Knows physical ecosystem attributes: geology, topography, soils, watershed function, classification systems", "knowledge", "1.2.1|1.2.3|1.2.4", "foundational", "partial", "Geology/topography not explicit."),
    ("SAF", "Forestry", "C4-A.4", "Knows interactions between physical attributes and forest communities", "knowledge", "1.1.1|1.3.1", "foundational", "partial", ""),
    ("SAF", "Forestry", "C4-A.5", "Understands ecological principles (communities, competition, diversity, population dynamics, succession, disturbance, nutrient cycling)", "understanding", "1.1.1|1.1.3|1.1.4|1.4.1", "intermediate", "full", ""),
    ("SAF", "Forestry", "C4-A.6", "Understands tree physiology and the effects of disturbance and climate on forest communities", "understanding", "1.1.4|1.3.4|1.5.2", "intermediate", "partial", "Tree physiology absent."),
    ("SAF", "Forestry", "C4-A.7", "Recognizes and anticipates effects of disturbance, climate and other factors on forest health and productivity", "ability", "1.3.4|1.1.4|1.5.2", "intermediate", "full", ""),
    ("SAF", "Forestry", "C4-A.8", "Assesses forests and stands, including trees and other community components", "ability", "1.3.4|4.1.1|1.3.2", "intermediate", "full", ""),
    # B: Measurement
    ("SAF", "Forestry", "C4-B.1", "Knows basic orienteering: compass, pacing, map reading, bearings and distances", "knowledge", "2.1.3", "foundational", "partial", "v1 covers GPS; non-electronic navigation appears only in 3 indicators/tasks. Proposed edit to 2.1.3."),
    ("SAF", "Forestry", "C4-B.2", "Uses contemporary technology and recognizes when application results fall outside a reasonable range", "ability", "2.1.1|2.3.4|7.2.1", "foundational", "full", "Direct accreditation hook for 7.2.1 (validating AI/tool outputs)."),
    ("SAF", "Forestry", "C4-B.3", "Knows land measurement and geospatial methods, ground-based and remotely sensed, with pros and cons", "knowledge", "2.1.2|2.1.3|2.1.4", "foundational", "full", ""),
    ("SAF", "Forestry", "C4-B.4", "Identifies and measures discrete land areas and conducts geospatial analyses", "ability", "2.1.1|2.1.4", "intermediate", "full", ""),
    ("SAF", "Forestry", "C4-B.5", "Designs and implements forest inventories for specific objectives", "ability", "1.3.2", "intermediate", "full", ""),
    ("SAF", "Forestry", "C4-B.6", "Understands tradeoffs among inventory methods and their effect on precision; recommends a method", "understanding", "1.3.2|2.2.2", "intermediate", "full", ""),
    ("SAF", "Forestry", "C4-B.7", "Analyzes inventory data and projects future forest, stand and tree conditions", "ability", "1.3.2|1.3.3", "intermediate", "full", ""),
    # C: Policy, economics, administration
    ("SAF", "Forestry", "C4-C.1", "Knows how forest policy is developed and enacted", "knowledge", "6.4.1|6.4.5", "foundational", "partial", ""),
    ("SAF", "Forestry", "C4-C.2", "Knows elements of environmental justice and how they appear in natural resource policy", "knowledge", "5.3.5|6.7.2", "foundational", "full", ""),
    ("SAF", "Forestry", "C4-C.3", "Knows federal, state and local laws and regulations affecting forest management", "knowledge", "6.1.1|6.1.2|6.1.3", "foundational", "full", "Reform-sensitive: v1 6.1.4 still cites CEQ regulations (removed 2026)."),
    ("SAF", "Forestry", "C4-C.4", "Knows sustainable-forest-management certification systems and their effects", "knowledge", "1.3.5", "foundational", "none", "GAP: forest certification appears in one indicator only."),
    ("SAF", "Forestry", "C4-C.5", "Knows structures, management principles and business operations of public and private enterprises", "knowledge", "3.1.1|3.1.2|3.3.1", "foundational", "partial", ""),
    ("SAF", "Forestry", "C4-C.6", "Understands market and non-market valuation procedures in forest decisions", "understanding", "6.3.1|6.3.2", "intermediate", "full", ""),
    ("SAF", "Forestry", "C4-C.7", "Synthesizes utilization, pricing, costs, discounting and land/timber valuation in a plan or alternative comparison", "ability", "1.3.5|6.3.1", "intermediate", "partial", "Timber appraisal/financial discounting appear in one indicator."),
    ("SAF", "Forestry", "C4-C.8", "Understands non-market social, cultural and ecological values of forests", "understanding", "6.3.2|5.3.2|5.3.3", "foundational", "full", ""),
    # D: Silviculture and management
    ("SAF", "Forestry", "C4-D.1", "Understands silviculture", "understanding", "1.3.1", "intermediate", "full", ""),
    ("SAF", "Forestry", "C4-D.2", "Develops and applies silvicultural prescriptions and anticipates results", "ability", "1.3.1", "intermediate", "full", ""),
    ("SAF", "Forestry", "C4-D.3", "Knows means to mitigate biotic and abiotic threats", "knowledge", "1.3.4|4.2.2", "foundational", "full", ""),
    ("SAF", "Forestry", "C4-D.4", "Knows fire ecology and the role of fire in forest management", "knowledge", "1.1.4|4.3.2|4.3.3", "foundational", "full", ""),
    ("SAF", "Forestry", "C4-D.5", "Knows harvesting, processing and transportation systems for forest products", "knowledge", "1.3.5|4.5.3", "foundational", "none", "GAP: no forest operations/harvesting-systems competency (DB/FC lane)."),
    ("SAF", "Forestry", "C4-D.6", "Analyzes data to predict economic, environmental and social consequences of strategies", "ability", "6.3.4|2.4.2|6.2.5", "intermediate", "full", ""),
    ("SAF", "Forestry", "C4-D.7", "Develops forest management plans with multiple objectives and constraints", "ability", "1.3.5|6.2.3", "intermediate", "full", ""),
    ("SAF", "Forestry", "C4-D.8", "Explains feasible alternatives and defends recommended actions orally and in writing", "ability", "5.1.1|5.1.2|6.1.4", "intermediate", "full", "Assess by structured oral defense (statecraft context)."),
    # SAF Forest Technology Standard (selected items that differ from Forestry)
    ("SAF", "Forest Technology", "C4-A.2", "Uses dichotomous keys", "ability", "4.1.1", "foundational", "none", "GAP: identification keys absent. Candidate LC-C-03."),
    ("SAF", "Forest Technology", "C4-B.4", "Gathers accurate inventory data with appropriate sampling, equipment and units (including in/out trees)", "ability", "1.3.2", "foundational", "full", "Observed field performance; human-essential task (v1 T1 = H/Hi/P)."),
    ("SAF", "Forest Technology", "C4-B.5", "Orienteers without battery-powered devices", "knowledge", "2.1.3", "foundational", "partial", "Non-electronic navigation; proposed edit to 2.1.3."),
    ("SAF", "Forest Technology", "C4-B.6", "Uses contemporary technology and recognizes out-of-range results", "ability", "2.3.4|7.2.1", "foundational", "full", "Accreditation hook for 7.2.1 at technician level."),
    ("SAF", "Forest Technology", "C4-B.7", "Acquires and processes GPS data into maps or products", "ability", "2.1.3|2.1.5", "foundational", "full", ""),
    ("SAF", "Forest Technology", "C4-B.8", "Determines area and scale from remotely sensed images and identifies features", "ability", "2.1.2", "foundational", "full", ""),
    ("SAF", "Forest Technology", "C4-B.9", "Creates stand-type maps from remotely sensed images", "ability", "2.1.2|2.1.5", "foundational", "full", "Entry point for remote-sensing reskilling (LC-PW-03)."),
    ("SAF", "Forest Technology", "C4-C.5", "Knows major commercial tree species and wood-product uses", "knowledge", "", "foundational", "none", "GAP: wood products absent from v1."),
    ("SAF", "Forest Technology", "C4-D.6", "Understands water-quality BMPs during harvesting and their suitability", "understanding", "1.2.5|4.2.4", "foundational", "partial", ""),
    ("SAF", "Forest Technology", "C4-D.7", "Knows wood scaling practices", "knowledge", "", "foundational", "none", "GAP: scaling/log grading absent from v1."),
    # SAF NREM Standard (selected)
    ("SAF", "NREM", "C4-B.6", "Designs and implements accurate inventories and assessments of ecosystem attributes", "ability", "1.1.2|4.1.1|1.3.2", "intermediate", "full", ""),
    ("SAF", "NREM", "C4-D.4", "Knows the adaptive management process and its application", "knowledge", "3.2.5|1.7.4", "foundational", "full", ""),
    ("SAF", "NREM", "C4-D.5", "Knows procedures for managing conflicts in setting management objectives", "knowledge", "5.2.4|5.2.3", "foundational", "full", ""),
    # SAF Urban Forestry (selected)
    ("SAF", "Urban Forestry", "C4-D.6", "Understands tree risk assessment using a recognized protocol", "understanding", "4.7.2", "foundational", "partial", "Tree risk assessment not explicit in v1 4.7.2."),
    # SAF program-level requirements relevant to pathways
    ("SAF", "All standards", "C2-6", "Transfer credit, including for work/life experience, must be judged equivalent to course learning outcomes by program faculty", "process", "", "", "process", "Hook for recognition of prior learning against EMST competency-levels (template rule R10)."),
    ("SAF", "All standards", "C5-5", "Program identifies and facilitates work experience or internships tied to graduate careers", "process", "", "", "process", "Hook for work-based learning modes (WBL) in pathways."),
    ("SAF", "Self-evaluation", "Education Summary", "Courses mapped to competency areas using Introduce/Reinforce/Emphasize-Apply", "process", "", "", "process", "EMST curriculum map should reuse the I/R/E scale so one mapping serves both."),
    # ABET EAC Environmental Engineering program criteria (2026-27) - paraphrased
    ("ABET-EAC", "Environmental Engineering (program criteria 2026-27)", "Curriculum (a)", "Mathematics through differential equations, probability/statistics, calculus-based physics, chemistry, earth and biological science, fluid mechanics", "content", "1.2.2|1.2.3|2.2.2", "foundational", "partial", "EMST is not a math/science foundations framework; by design."),
    ("ABET-EAC", "Environmental Engineering (program criteria 2026-27)", "Curriculum (b)", "Material and energy balances; fate and transport of substances in and between air, water and soil", "content", "6.7.4|3.7.5", "intermediate", "partial", "GAP: no fate-and-transport competency; proposed 2027-28 change adds interactions with biota."),
    ("ABET-EAC", "Environmental Engineering (program criteria 2026-27)", "Curriculum (c)", "Hands-on laboratory experiments and data interpretation in more than one focus area (air, water, land, environmental health)", "ability", "1.2.4|4.1.3|2.2.2|2.2.3", "intermediate", "partial", ""),
    ("ABET-EAC", "Environmental Engineering (program criteria 2026-27)", "Curriculum (d)", "Design of environmental engineering systems considering risk, uncertainty, sustainability, life-cycle principles and impacts", "ability", "3.7.3|3.1.3|4.7.1", "intermediate", "partial", "GAP: engineering design of treatment systems absent; proposed 2027-28 change requires computational tools in design."),
    ("ABET-EAC", "Environmental Engineering (program criteria 2026-27)", "Curriculum (e)", "Professional practice, project management, and roles of public and private organizations in environmental policy and regulation", "knowledge", "3.1.1|6.1.1|6.1.2|6.5.2", "foundational", "full", "Proposed 2027-28 change adds economics and ethics (6.3.4, 7.1.3)."),
    ("ABET-EAC", "General criteria", "SO-7", "Acquire and apply new knowledge using appropriate learning strategies", "ability", "7.2.3", "foundational", "partial", "Lifelong-learning outcome; EMST has no 'learning to learn' competency."),
    # ABET ETAC Environmental Engineering Technology program criteria
    ("ABET-ETAC", "Environmental Engineering Technology", "Associate topics", "Field/lab measurement with common instruments; permit applications and reports; QC and basic statistics; professional practice; regulatory roles; unit-process operating principles", "ability", "4.1.3|2.3.1|6.1.3|5.1.1|2.2.3|2.2.2|3.1.1|6.1.2", "foundational", "partial", "GAP: unit-process (treatment) operation absent from v1. Candidate LC-C-05."),
    ("ABET-ETAC", "Environmental Engineering Technology", "Baccalaureate added topics", "Probability/statistics and risk analysis; material balances; environmental science principles; design of unit processes", "ability", "2.2.2|6.7.1|1.2.4", "intermediate", "partial", "Unit-process design absent from v1."),
    # EHAC undergraduate requirements (in force July 2025)
    ("EHAC", "Undergraduate requirements (July 2025)", "Methodology", "Separate courses in epidemiology, statistical methods and toxicology", "content", "2.2.2|6.7.4", "foundational", "partial", "GAP: epidemiology absent from v1."),
    ("EHAC", "Undergraduate requirements (July 2025)", "Cross-cutting: risk", "Risk assessment, communication and management", "ability", "6.7.1|3.1.3|5.1.5", "foundational", "full", ""),
    ("EHAC", "Undergraduate requirements (July 2025)", "Cross-cutting: management and law", "Policy analysis, emergency management systems, program administration; administrative law and process", "knowledge", "6.1.1|4.4.5|6.4.2|6.1.5", "foundational", "partial", "Administrative law not explicit in v1."),
    ("EHAC", "Undergraduate requirements (July 2025)", "Cross-cutting: justice", "Environmental justice, equity and social determinants of health", "knowledge", "5.3.5|6.7.2|6.7.3", "foundational", "full", ""),
    ("EHAC", "Undergraduate requirements (July 2025)", "Technical List 1", "Required exposure: air quality; food protection; occupational health and safety; solid and hazardous waste; water and wastewater; zoonotic and vector-borne disease", "knowledge", "6.7.5|4.4.1|3.7.2|4.4.4|1.2.4|4.7.3", "foundational", "partial", "GAPS: food protection, vector/zoonotic disease and water/wastewater treatment operations absent. Candidates LC-C-05, LC-C-07."),
    ("EHAC", "Undergraduate requirements (July 2025)", "Practicum", "At least 180 clock hours of field practicum or internship with documented work", "process", "", "", "process", "WBL mode benchmark for environmental-health pathways."),
    # NAAEE core competencies for EE certification (six themes)
    ("NAAEE", "EE certification core competencies (2006; 2025 guidelines supersede)", "Theme 1", "Environmental literacy", "ability", "1.1.1|1.2.3|1.5.1", "foundational", "partial", "Broad; maps across D1."),
    ("NAAEE", "EE certification core competencies (2006; 2025 guidelines supersede)", "Theme 2", "Foundations of environmental education", "knowledge", "5.4.2", "foundational", "partial", ""),
    ("NAAEE", "EE certification core competencies (2006; 2025 guidelines supersede)", "Theme 3", "Professional responsibilities, including distinguishing education from advocacy", "ability", "7.1.3|5.1.3", "foundational", "partial", ""),
    ("NAAEE", "EE certification core competencies (2006; 2025 guidelines supersede)", "Theme 4", "Planning and implementing environmental education", "ability", "5.4.1|5.4.2|5.4.5", "intermediate", "full", ""),
    ("NAAEE", "EE certification core competencies (2006; 2025 guidelines supersede)", "Theme 5", "Fostering learning in inclusive, responsive settings", "ability", "5.4.1|5.5.5|5.3.1", "intermediate", "partial", ""),
    ("NAAEE", "EE certification core competencies (2006; 2025 guidelines supersede)", "Theme 6", "Assessment and evaluation of learners and programs", "ability", "5.4.1|3.1.5", "intermediate", "partial", "Learner assessment not explicit in v1 5.4.x."),
]
ASRC = {"SAF": "LC-001", "ABET-EAC": "LC-002|LC-003", "ABET-ETAC": "LC-004", "EHAC": "LC-005", "NAAEE": "LC-009|LC-008"}


def write_accred():
    out = os.path.join(HERE, "accreditation_emst_crosswalk.csv")
    fields = ["accreditor", "standard", "criterion_id", "criterion_paraphrase", "verb_tier",
              "emst_v1_codes", "target_level", "coverage", "gap_note", "source_ids"]
    rows = []
    for acc, std, cid, para, tier, codes, lvl, cov, note in A:
        for c in filter(None, codes.split("|")):
            assert c in comp_codes, f"unknown v1 code {c} in {acc} {cid}"
        rows.append(dict(zip(fields, [acc, std, cid, para, tier, codes, lvl, cov, note, ASRC[acc]])))
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    return out, len(rows)


if __name__ == "__main__":
    p1, n1, ncip = write_cip()
    p2, n2 = write_accred()
    print(f"wrote {p1}: {n1} CIP-SOC rows for {ncip} CIP codes")
    print(f"wrote {p2}: {n2} accreditation criterion rows")
    cov = collections.Counter(r[7] for r in A)
    print("accreditation coverage:", dict(cov))
    sys.exit(0)
