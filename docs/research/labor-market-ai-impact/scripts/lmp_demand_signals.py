#!/usr/bin/env python3
"""
LM demand-signal pass over OpenLMP land management plan components.

Role: LM (Labor Market & AI-Impact Research Lead), EMST v2, Phase 2.
Reads (read-only):  /home/claude/lmps/catalog/plans.csv
                    /home/claude/lmps/plans/<STATE>/<unit>/<year>/components.csv
                    /home/claude/lmps/schema/vocab/themes.yaml (theme keys only)
Writes:             ./lmp_outputs/*.csv, ./lmp_outputs/lmp_summary.json

What it measures (all counts are of *extracted plan components*, not atomic requirements):
  1. Component profile by agency group x planning framework x component type.
  2. Monitoring requirements by resource theme (controlled theme tags where present,
     otherwise keyword-inferred theme from component text) and by monitoring method family.
  3. Standards/guidelines (binding/semi-binding direction) by theme.
  4. Coordination / regulatory-process touchpoints (OpenLMP `coordination` field).
  5. Authoritative datasets/models plans depend on (OpenLMP `authoritative_data` field
     plus a text regex pass), normalised into families.
  6. Rule-era comparison (1982 rule vs 2012 rule) of mention rates for demand-relevant terms.
  7. Signal -> implied workforce competency (v1 EMST codes) crosswalk.

Limitations (see report.md section 4): ~95% of components are USDA Forest Service, all western
states; component segmentation differs by extraction method (section/table/code) and plan era;
keyword matching measures *mention*, not obligation; theme tags cover ~10% of components, so
keyword inference is used and is noisier. Deterministic: no randomness, no network.
"""
import csv
import glob
import json
import os
import re
import statistics
from collections import Counter, defaultdict

LMPS = "/home/claude/lmps"
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")  # outputs go to the role folder
OUT = os.path.join(HERE, "lmp_outputs")
os.makedirs(OUT, exist_ok=True)

csv.field_size_limit(10**9)


def agency_group(a):
    return "USFS" if a.strip() == "USDA Forest Service" else "State"


def era(fw):
    return {"usfs-1982-rule": "1982-rule", "usfs-2012-rule": "2012-rule",
            "state-framework": "state", "other": "other"}.get(fw, "other")


# ---------------------------------------------------------------- theme inference
THEME_RX = {
    "vegetation": r"\bvegetation\b|forest (structure|composition)|stand (structure|density)|seral|cover type",
    "old_growth": r"old[- ]growth|late[- ]successional|mature forest",
    "fire_fuels": r"\bfire\b|wildfire|fuels?\b|prescribed burn|burn(ed|ing)? area",
    "insects_disease": r"insect|disease|bark beetle|mountain pine beetle|root rot|mistletoe",
    "wildlife": r"wildlife|elk|deer|big game|bird|raptor|bat\b|bats\b|habitat (for|of) ",
    "at_risk_species": r"threatened|endangered|species of conservation concern|\bSCC\b|at-risk species|sensitive species|grizzly|lynx|spotted owl|sage[- ]grouse|bull trout|marbled murrelet",
    "aquatics_fisheries": r"aquatic|fish(eries)?\b|trout|salmon|stream habitat|spawning|redd",
    "riparian": r"riparian|RHCA|\bRMZ\b|wetland|streamside",
    "water_watersheds": r"watershed|water quality|water yield|streamflow|hydrolog|groundwater|municipal water|303\(d\)",
    "soils": r"\bsoils?\b|erosion|compaction|productivity of the land",
    "air": r"air quality|smoke|visibility|class i area|airshed",
    "climate_carbon": r"climate|carbon|drought|snowpack|sequestration",
    "timber": r"timber|harvest|sawtimber|board feet|\bASQ\b|\bPWSQ\b|regeneration harvest|silvicultur",
    "range_grazing": r"grazing|livestock|allotment|rangeland|forage|\bAUMs?\b",
    "minerals_energy": r"mineral|mining|oil and gas|geotherm|energy development|leasable|locatable",
    "recreation": r"recreation|trail|campground|visitor|\bROS\b|motorized|over-snow|ski area",
    "scenery": r"scenic|scenery|visual quality|landscape character",
    "designated_areas": r"wilderness|wild and scenic|roadless|research natural area|national monument|recreation area",
    "cultural_heritage": r"cultural resource|heritage|historic propert|archaeolog|section 106",
    "tribal": r"tribe|tribal|indigenous|native american|treaty",
    "infrastructure_access": r"\broads?\b|bridge|culvert|facilit|infrastructure|travel management",
    "lands_special_uses": r"special use|land exchange|right[- ]of[- ]way|easement|utility corridor|communication site",
    "socioeconomics": r"socioeconomic|economic|employment|local communit|county|jobs",
    "invasive_species": r"invasive|noxious weed|non-native species|weeds?\b",
    "plants_botany": r"botan|rare plant|plant species|whitebark pine|pollinator",
    "community_protection": r"wildland[- ]urban interface|\bWUI\b|community protection|values at risk",
    "ecosystem_services": r"ecosystem services",
    "partnerships_coordination": r"partner|collaborat|cooperat|shared stewardship|good neighbor",
    "monitoring_research": r"monitor|research|inventory",
}
THEME_RX = {k: re.compile(v, re.I) for k, v in THEME_RX.items()}


def themes_of(row, text):
    tagged = [t for t in (row["themes"] or "").split(";") if t]
    if tagged:
        return set(tagged), "tag"
    inferred = {k for k, rx in THEME_RX.items() if rx.search(text) and k != "monitoring_research"}
    return inferred, "keyword"


# ---------------------------------------------------------------- monitoring method families
METHOD_RX = {
    # patterns are compiled case-SENSITIVE; phrases use scoped (?i:...) so acronyms (ADS, UAS, IMPROVE) do not match ordinary words
    "remote_sensing_imagery": (r"(?i:remote(ly)? sens|satellite|landsat|sentinel-?2|aerial (photo|imagery)|orthophoto|imagery)|\bNAIP\b", "2.1.2|2.6.1|2.4.1", "DC"),
    "lidar": (r"(?i:\blidar\b)", "2.1.2|2.7.5", "DC"),
    "uas_drone": (r"(?i:\bdrones?\b|unmanned aerial)|\bUAS\b|\bUAV\b", "2.3.2|4.5.4", "DC"),
    "fia_or_inventory_plots": (r"(?i:forest inventory and analysis|inventory plots?|stand exam|timber cruise)|\bFIA\b", "1.3.2|4.1.1|2.2.2", "FC"),
    "field_plots_transects": (r"(?i:\bplots?\b|transects?|quadrats?|photo ?points?|repeat photograph)", "4.1.1|1.1.2", "FC"),
    "wildlife_surveys": (r"(?i:survey(s|ed)?\b.{0,60}(bird|owl|goshawk|amphib|\bbats?\b|bear|lynx|wolverine|elk|deer|species)|occupancy|point counts?|camera trap|telemetry|radio[- ]collar|nest(ing)? (survey|monitor))", "1.4.2|4.1.2|2.6.2", "FC"),
    "aquatic_sampling": (r"(?i:stream temperature|water temperature|sediment|turbidity|macroinvertebrate|water quality (sampl|monitor|data)|stream (survey|habitat inventory)|redd counts?|fish (survey|population))|\bPIBO\b|\bAREMP\b", "4.1.3|1.2.4|1.4.5", "FC"),
    "edna_genetic": (r"\beDNA\b|(?i:environmental DNA|genetic (sampl|monitor))", "1.6.2|1.6.1", "DC"),
    "bmp_implementation": (r"(?i:best management practices?)|\bBMPs?\b", "6.1.2|4.2.4", "SC"),
    "burn_severity_post_fire": (r"(?i:burn severity|post-fire)|\bMTBS\b|\bRAVG\b|\bBAER\b", "4.3.5|2.1.2", "FC"),
    "insect_disease_survey": (r"(?i:aerial detection|insect and disease survey|forest health (survey|monitor))|\bADS\b", "1.3.4", "FC"),
    "range_utilization": (r"(?i:utilization|stubble height|forage|range (condition|monitor)|greenline|upland condition)", "4.6.5|1.1.5", "FC"),
    "soil_disturbance": (r"(?i:detrimental soil|soil (disturbance|compaction|monitor|condition))", "4.1.4|1.2.1", "FC"),
    "invasive_inventory": (r"(?i:(weed|invasive).{0,40}(inventor|survey|map|monitor|treat))", "4.2.2|2.1.1", "FC"),
    "visitor_use_social": (r"(?i:visitor use|national visitor use|recreation use|visitation|user (survey|conflict)|encounters?|visitor satisfaction)|\bNVUM\b", "5.6.2|5.5.1", "SC"),
    "socioeconomic_indicators": (r"(?i:socioeconomic|economic (contribution|impact|condition)|employment|income|payments to (states|counties))", "6.3.4", "DC"),
    "air_smoke": (r"\bIMPROVE\b|\bAQRV\b|(?i:visibility|air quality (monitor|data)|smoke (monitor|impact))", "6.7.5", "DC"),
    "climate_indicators": (r"(?i:climate (change )?(indicator|monitor|vulnerab)|snowpack|drought (index|monitor))|\bSNOTEL\b", "1.5.1|1.5.2", "DC"),
    "modeling_projection": (r"(?i:\bmodel(s|ed|ing)?\b|simulat|projection)", "2.4.2|1.3.3", "DC"),
    "partner_or_citizen": (r"(?i:partners?\b|volunteers?|citizen science|community science|collaborat)", "5.4.4|5.2.5", "SC"),
    "tribal_participation": (r"(?i:\btribes?\b|tribal|indigenous|traditional ecological knowledge)", "6.5.1|5.3.2|7.1.1", "SC"),
    "reporting_data_systems": (r"(?i:database|monitoring report|biennial|report(ed|ing)? (annually|every)|evaluation report)|\bNRIS\b|\bFACTS\b|\bINFRA\b", "2.2.1|3.1.5|3.3.5", "DC"),
    "adaptive_management": (r"(?i:adaptive management|management response|change in management|triggers? (for|that)|threshold)", "3.2.5|6.2.3", "SC"),
}
METHOD_RX = {k: (re.compile(v[0]), v[1], v[2]) for k, v in METHOD_RX.items()}

# ---------------------------------------------------------------- authoritative datasets / models
AUTH_RX = {
    # case-SENSITIVE acronyms; phrases in scoped (?i:...)
    "Forest Inventory and Analysis (FIA)": (r"(?i:forest inventory and analysis|R1 Summary Database)|\bFIA\b", "1.3.2|2.2.2", "DC", "dataset"),
    "LANDFIRE": (r"(?i:LANDFIRE|biophysical setting)", "2.1.2|4.3.3|1.1.4", "DC", "dataset"),
    "Forest Vegetation Simulator (FVS)": (r"(?i:forest vegetation simulator|Prognosis model)|\bFVS\b", "1.3.3|2.4.2", "DC", "model"),
    "FSim / burn probability": (r"\bFSim\b|(?i:burn probability|large fire simulat)", "4.3.4|2.4.2|3.1.3", "DC", "model"),
    "FlamMap / FARSITE / BehavePlus": (r"(?i:FlamMap|FARSITE|BehavePlus)|\bBEHAVE\b", "4.3.4|4.3.2", "DC", "model"),
    "Wildfire risk / WUI data (SILVIS, WRC, QWRA)": (r"\bSILVIS\b|\bQWRA\b|(?i:wildfire risk to communities|quantitative wildfire risk|wildland[- ]urban interface (map|data|layer)|wildfire hazard potential)", "4.3.3|3.1.3|6.2.4", "DC", "dataset"),
    "Fire regime / FRCC": (r"\bFRCC\b|(?i:fire regime condition class|fire return interval|historic(al)? fire regime)", "1.1.4|4.3.3", "DC", "classification"),
    "Natural/historic range of variation (NRV/HRV)": (r"\bNRV\b|\bHRV\b|(?i:natural range of variation|historic(al)? range of variation|range of variability)", "1.1.4|1.7.5|2.4.2", "DC", "analysis"),
    "Vegetation maps (VMap, EVeg/CALVEG, LEMMA GNN)": (r"\bVMap\b|\bEVeg\b|\bCALVEG\b|\bLEMMA\b|\bGNN\b|(?i:existing vegetation map)", "2.1.2|2.4.1|4.1.1", "DC", "dataset"),
    "Potential vegetation / habitat type classifications": (r"\bPVTs?\b|\bPVGs?\b|(?i:potential vegetation (group|type)|habitat type classification|forest habitat type)", "1.1.1|1.3.1", "FC", "classification"),
    "Recreation Opportunity Spectrum (ROS)": (r"\bROS\b|(?i:recreation opportunity spectrum)", "6.2.3|5.5.1", "SC", "classification"),
    "Scenery management (SIO/VQO)": (r"\bSIOs?\b|\bVQOs?\b|(?i:scenic integrity objective|visual quality objective|visual management system|scenery management system)", "6.2.3", "SC", "classification"),
    "FS corporate data systems (NRIS, FACTS, INFRA, TIM)": (r"\bNRIS\b|\bFACTS\b|\bINFRA\b|\bTIM\b|(?i:FS corporate data)", "2.2.1|3.3.5|4.1.5", "DC", "dataset"),
    "Watershed Condition Framework": (r"(?i:watershed condition (framework|classification|class))", "1.2.3|2.1.4", "DC", "classification"),
    "Soil survey (SSURGO/TEUI)": (r"\bSSURGO\b|\bTEUI\b|(?i:soil survey|terrestrial ecological unit)", "1.2.1|4.1.4", "FC", "dataset"),
    "Airborne LiDAR": (r"(?i:\blidar\b)", "2.1.2|2.7.5", "DC", "dataset"),
    "Burn severity (MTBS/RAVG/BAER)": (r"\bMTBS\b|\bRAVG\b|\bBAER\b|(?i:monitoring trends in burn severity)", "4.3.5|2.1.2", "DC", "dataset"),
    "Insect & Disease Aerial Detection Survey": (r"\bADS\b|(?i:aerial detection survey|insect and disease survey)", "1.3.4|2.1.2", "FC", "monitoring_program"),
    "USFWS species lists / IPaC / critical habitat": (r"\bIPaC\b|(?i:critical habitat designation|USFWS species list)", "6.1.3|6.5.3|1.4.3", "SC", "dataset"),
    "NatureServe / Natural Heritage": (r"(?i:NatureServe|natural heritage (program|database))", "1.1.2|1.4.3", "DC", "dataset"),
    "IMPROVE / AQRV air monitoring": (r"\bIMPROVE\b|\bAQRVs?\b|(?i:air quality related value)", "6.7.5", "DC", "monitoring_program"),
    "National Visitor Use Monitoring (NVUM)": (r"\bNVUM\b|(?i:national visitor use monitoring)", "5.6.2|5.5.1", "DC", "monitoring_program"),
    "Aquatic effectiveness monitoring (PIBO, AREMP)": (r"\bPIBO\b|\bAREMP\b|(?i:PACFISH/INFISH Biological Opinion|aquatic and riparian effectiveness)", "4.1.3|1.4.5|1.2.4", "FC", "monitoring_program"),
    "Landscape simulation (SIMPPLLE, Spectrum/PRISM)": (r"\bSIMPPLLE\b|(?<!Opportunity )(?<!opportunity )\bSpectrum\b(?! of)(?! \(setting)|(?i:harvest scheduling model|PRISM forest planning)", "2.4.2|1.3.5", "DC", "model"),
    "CWA 303(d)/305(b) integrated report": (r"303\(d\)|305\(b\)|(?i:integrated report)", "1.2.4|6.1.2", "SC", "assessment"),
    "Hydrologic modeling / streamflow": (r"\bECA\b|(?i:hydrologic model|streamflow (model|analysis)|water yield (model|analysis)|equivalent clearcut area)", "1.2.3|2.4.2", "DC", "model"),
    "Climate projections / vulnerability assessments": (r"\bCMIP\d?\b|\bMACA\b|(?i:climate (projection|model)|downscaled climate|climate (change )?vulnerability assessment)", "1.5.1|1.5.2|1.5.3", "DC", "model_output"),
    "Census / economic models (IMPLAN, EPS)": (r"\bIMPLAN\b|\bEPS-HDT\b|(?i:economic profile system|census (data|bureau))", "6.3.4", "DC", "dataset"),
}
AUTH_RX = {k: (re.compile(v[0]), v[1], v[2], v[3]) for k, v in AUTH_RX.items()}

# ---------------------------------------------------------------- rule-era comparison terms
ERA_TERMS = {
    "climate_change": r"climate change|changing climate|climate adaptation",
    "carbon": r"\bcarbon\b|sequestration",
    "drought": r"drought",
    "tribal_or_indigenous": r"\btribes?\b|tribal|indigenous|treaty",
    "partnership_collaboration": r"partner|collaborat|shared stewardship|good neighbor|all[- ]lands",
    "best_available_science": r"best available scientific information|best available science",
    "adaptive_management": r"adaptive management",
    "monitoring": r"\bmonitor",
    "at_risk_species_scc": r"species of conservation concern|at-risk species",
    "ecological_integrity": r"ecological integrity|resilien",
    "wildfire_risk_wui": r"wildland[- ]urban interface|\bWUI\b|wildfire risk|community protection",
    "invasive_species": r"invasive|noxious weed",
    "recreation_sustainable": r"sustainable recreation|visitor use|recreation opportunit",
    "ecosystem_services": r"ecosystem services",
    "timber_volume": r"board feet|\bASQ\b|allowable sale quantity|\bPWSQ\b|\bPTSQ\b|timber production",
    "grazing": r"grazing|livestock|allotment",
    "data_or_models": r"\bdata\b|\bmodel",
    "remote_sensing_lidar_drone": r"remote sens|satellite|imagery|lidar|drone|unmanned aerial",
}
ERA_TERMS = {k: re.compile(v, re.I) for k, v in ERA_TERMS.items()}

STANDARD_TYPES = {"standard", "guideline", "standard_or_guideline"}
# A cleaner atomic unit than "monitoring component": a monitoring QUESTION (2012-rule plans and many 1982-rule
# monitoring tables state explicit questions). Table fragments ("Data", year cells) are excluded by this filter.
MQ_RX = re.compile(r"\?|(?i:monitoring question)|\bMQ\s?\d+|\bMON-[A-Z]+-\d+")


def main():
    plans = {r["plan_id"]: r for r in csv.DictReader(open(os.path.join(LMPS, "catalog/plans.csv"), newline="", encoding="utf-8"))}
    files = sorted(glob.glob(os.path.join(LMPS, "plans/*/*/*/components.csv")))

    profile = Counter()
    profile_plans = defaultdict(set)
    mon_theme = Counter(); mon_theme_plans = defaultdict(set); mon_theme_src = Counter()
    mon_method = Counter(); mon_method_plans = defaultdict(set); mon_method_units = defaultdict(set)
    std_theme = Counter(); std_theme_mand = Counter(); std_theme_plans = defaultdict(set)
    coord = Counter(); coord_plans = defaultdict(set); coord_era = defaultdict(Counter)
    auth_field = Counter(); auth_text = Counter(); auth_any_plans = defaultdict(set); auth_any_units = defaultdict(set)
    auth_era = defaultdict(Counter)
    era_n = Counter(); era_hits = defaultdict(Counter); era_plans = defaultdict(set)
    per_plan_mon = Counter(); per_plan_n = Counter(); plan_era = {}
    unmapped_auth = Counter()
    n_total = 0
    n_mon = 0
    n_mq = 0; mq_theme = Counter(); mq_method = Counter(); mq_plans = set(); mq_units = set(); mq_method_plans = defaultdict(set); mq_theme_plans = defaultdict(set)
    mon_by_plan = Counter()

    for f in files:
        with open(f, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                n_total += 1
                pid = r["plan_id"]; unit = r["unit_id"]
                ag = agency_group(r["agency"]); er = era(r["framework"])
                ctype = r["component_type"] or "unknown"
                text = r["text"] or ""
                plan_era[pid] = er
                per_plan_n[pid] += 1
                profile[(ag, er, ctype)] += 1
                profile_plans[(ag, er, ctype)].add(pid)
                th, src = themes_of(r, text)

                # rule-era mention rates (component-level)
                era_n[er] += 1
                era_plans[er].add(pid)
                for k, rx in ERA_TERMS.items():
                    if rx.search(text):
                        era_hits[er][k] += 1

                if ctype == "monitoring":
                    n_mon += 1
                    per_plan_mon[pid] += 1
                    if MQ_RX.search(text) and len(text) >= 40:
                        n_mq += 1; mq_plans.add(pid); mq_units.add(unit)
                        for t in (th or {"(no theme detected)"}):
                            mq_theme[t] += 1; mq_theme_plans[t].add(pid)
                        for k, (rx, _, _) in METHOD_RX.items():
                            if rx.search(text):
                                mq_method[k] += 1; mq_method_plans[k].add(pid)
                    for t in (th or {"(no theme detected)"}):
                        mon_theme[t] += 1; mon_theme_plans[t].add(pid); mon_theme_src[(t, src)] += 1
                    for k, (rx, _, _) in METHOD_RX.items():
                        if rx.search(text):
                            mon_method[k] += 1; mon_method_plans[k].add(pid); mon_method_units[k].add(unit)

                if ctype in STANDARD_TYPES:
                    for t in (th or {"(no theme detected)"}):
                        std_theme[t] += 1; std_theme_plans[t].add(pid)
                        if r["modality"] == "mandatory" or ctype == "standard":
                            std_theme_mand[t] += 1

                for c in [c for c in (r["coordination"] or "").split(";") if c]:
                    coord[c] += 1; coord_plans[c].add(pid); coord_era[c][er] += 1

                field_vals = [v.strip() for v in (r["authoritative_data"] or "").split(";") if v.strip()]
                hit_fams = set()
                for v in field_vals:
                    matched = False
                    for fam, (rx, _, _, _) in AUTH_RX.items():
                        if rx.search(v):
                            auth_field[fam] += 1; hit_fams.add(fam); matched = True
                    if not matched:
                        unmapped_auth[v] += 1
                for fam, (rx, _, _, _) in AUTH_RX.items():
                    if rx.search(text):
                        auth_text[fam] += 1; hit_fams.add(fam)
                for fam in hit_fams:
                    auth_any_plans[fam].add(pid); auth_any_units[fam].add(unit); auth_era[fam][er] += 1

    # ------------------------------------------------------------ write outputs
    def w(name, header, rows):
        with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as fh:
            wr = csv.writer(fh); wr.writerow(header); wr.writerows(rows)

    w("lmp_component_profile.csv", ["agency_group", "framework_era", "component_type", "n_components", "n_plans"],
      [[a, e, c, n, len(profile_plans[(a, e, c)])] for (a, e, c), n in sorted(profile.items())])

    w("lmp_monitoring_by_theme.csv", ["theme", "n_monitoring_components", "share_of_monitoring", "n_plans", "n_from_tags", "n_from_keywords"],
      [[t, n, round(n / n_mon, 4), len(mon_theme_plans[t]), mon_theme_src[(t, "tag")], mon_theme_src[(t, "keyword")]]
       for t, n in mon_theme.most_common()])

    w("lmp_monitoring_methods.csv", ["method_family", "n_monitoring_components", "share_of_monitoring", "n_plans", "n_units", "implied_v1_codes", "craft_signal"],
      [[k, n, round(n / n_mon, 4), len(mon_method_plans[k]), len(mon_method_units[k]), METHOD_RX[k][1], METHOD_RX[k][2]]
       for k, n in mon_method.most_common()])

    n_std = sum(n for (a, e, c), n in profile.items() if c in STANDARD_TYPES)
    w("lmp_standards_by_theme.csv", ["theme", "n_standard_or_guideline_components", "share_of_standards", "n_mandatory_or_standard", "n_plans"],
      [[t, n, round(n / n_std, 4), std_theme_mand[t], len(std_theme_plans[t])] for t, n in std_theme.most_common()])

    eras = ["1982-rule", "2012-rule", "state", "other"]
    w("lmp_coordination_touchpoints.csv", ["touchpoint_subtype", "n_components", "n_plans"] + [f"n_{e}" for e in eras] + [f"per_1000_{e}" for e in eras],
      [[c, n, len(coord_plans[c])] + [coord_era[c][e] for e in eras] + [round(1000 * coord_era[c][e] / era_n[e], 2) if era_n[e] else "" for e in eras]
       for c, n in coord.most_common()])

    w("lmp_authoritative_data.csv", ["data_or_model_family", "kind", "n_components_field", "n_components_text", "n_plans_any", "n_units_any",
                                     "n_components_1982", "n_components_2012", "n_components_state", "implied_v1_codes", "craft_signal"],
      [[fam, AUTH_RX[fam][3], auth_field[fam], auth_text[fam], len(auth_any_plans[fam]), len(auth_any_units[fam]),
        auth_era[fam]["1982-rule"], auth_era[fam]["2012-rule"], auth_era[fam]["state"], AUTH_RX[fam][1], AUTH_RX[fam][2]]
       for fam in sorted(AUTH_RX, key=lambda k: -len(auth_any_plans[k]))])

    rows = []
    for k in ERA_TERMS:
        r82 = era_hits["1982-rule"][k] / era_n["1982-rule"] if era_n["1982-rule"] else 0
        r12 = era_hits["2012-rule"][k] / era_n["2012-rule"] if era_n["2012-rule"] else 0
        rst = era_hits["state"][k] / era_n["state"] if era_n["state"] else 0
        rows.append([k, era_hits["1982-rule"][k], round(1000 * r82, 1), era_hits["2012-rule"][k], round(1000 * r12, 1),
                     era_hits["state"][k], round(1000 * rst, 1), round(r12 / r82, 2) if r82 else ""])
    rows.sort(key=lambda x: -(x[-1] or 0))
    w("lmp_rule_era_comparison.csv", ["term_family", "n_1982_rule", "per_1000_1982_rule", "n_2012_rule", "per_1000_2012_rule",
                                       "n_state", "per_1000_state", "ratio_2012_to_1982"], rows)

    w("lmp_monitoring_questions.csv", ["dimension", "value", "n_monitoring_questions", "share_of_questions", "n_plans"],
      [["theme", t, n, round(n / max(1, n_mq), 4), len(mq_theme_plans[t])] for t, n in mq_theme.most_common()] +
      [["method_family", k, n, round(n / max(1, n_mq), 4), len(mq_method_plans[k])] for k, n in mq_method.most_common()])
    top = sorted(per_plan_mon.items(), key=lambda x: -x[1])[:15]
    w("lmp_monitoring_concentration_top15.csv", ["plan_id", "framework_era", "n_monitoring_components", "share_of_all_monitoring"],
      [[pid, plan_era[pid], n, round(n / n_mon, 4)] for pid, n in top])

    w("lmp_unmapped_authoritative_data_top.csv", ["authoritative_data_value", "n"], unmapped_auth.most_common(150))

    # per-plan monitoring intensity by era
    by_era = defaultdict(list)
    for pid, n in per_plan_n.items():
        by_era[plan_era[pid]].append((per_plan_mon[pid], n))
    era_stats = {}
    for e, lst in by_era.items():
        mons = [m for m, _ in lst]
        era_stats[e] = {"plans": len(lst), "components": sum(n for _, n in lst), "monitoring_components": sum(mons),
                        "median_monitoring_per_plan": statistics.median(mons), "share_plans_with_any_monitoring": round(sum(1 for m in mons if m) / len(lst), 3),
                        "monitoring_share_of_components": round(sum(mons) / max(1, sum(n for _, n in lst)), 4)}

    summary = {
        "generated_by": "lmp_demand_signals.py",
        "lmps_catalog_generated": json.load(open(os.path.join(LMPS, "catalog/summary.json"))).get("generated"),
        "n_component_files": len(files), "n_component_files_nonempty": len(per_plan_n), "n_components": n_total, "n_plans_catalog": len(plans),
        "n_monitoring_components": n_mon,
        "n_monitoring_questions": n_mq, "n_plans_with_monitoring_questions": len(mq_plans), "n_units_with_monitoring_questions": len(mq_units),
        "n_standard_guideline_components": n_std,
        "era_component_counts": dict(era_n),
        "era_monitoring_stats": era_stats,
    }
    ag = Counter()
    for (a, e, c), n in profile.items():
        ag[a] += n
    summary["agency_group_components"] = dict(ag)
    summary["n_coordination_tag_instances"] = sum(coord.values())
    json.dump(summary, open(os.path.join(OUT, "lmp_summary.json"), "w"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
