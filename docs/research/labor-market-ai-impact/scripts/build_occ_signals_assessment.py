#!/usr/bin/env python3
"""Build env_occupations_in_scope.csv, role_signals.csv, v1_assessment.csv, candidate_competencies.csv (LM, EMST v2 Phase 2).
Exposure numbers are read from ../env_occupation_exposure_scores.csv (scripts/env_occupation_exposure.py); narrative fields are LM appraisal."""
import csv, os
import pandas as pd
H = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sc = pd.read_csv(os.path.join(H, "env_occupation_exposure_scores.csv")).set_index("soc_code")

def pct(x):
    return "n/a" if pd.isna(x) else str(int(round(100 * x)))

def sig(code):
    if code not in sc.index:
        return "not scored"
    r = sc.loc[code]
    parts = [f"Eloundou human-beta pct {pct(r['eloundou_human_rating_beta_pct'])} (GPT-4 pct {pct(r['eloundou_dv_rating_beta_pct'])})"]
    if not pd.isna(r.get("share_E0_human")):
        parts.append(f"tasks E0 {int(round(100*r['share_E0_human']))}%")
    if not pd.isna(r.get("share_physical_tasks")):
        parts.append(f"physical tasks {int(round(100*r['share_physical_tasks']))}% (MS v1.1)")
    if not pd.isna(r.get("ms_ai_applicability_pct")):
        parts.append(f"MS usage applicability pct {pct(r['ms_ai_applicability_pct'])} (nonphysical {pct(r['ms_nonphysical_pct'])})")
    if not pd.isna(r.get("aioe_pct")):
        parts.append(f"AIOE pct {pct(r['aioe_pct'])}")
    return "; ".join(parts)

def bls(code):
    if code not in sc.index or pd.isna(sc.loc[code].get("bls_pct_change_2022_32")):
        return ""
    r = sc.loc[code]
    return f"BLS 2022-32 (superseded vintage): {r['bls_pct_change_2022_32']:+.1f}% on {r['bls_emp_2022_thousands']}k"

OCC = [
 # soc, onet_soc, title, families, in_aei, trend_extra, notes, sources
 ("19-1031","19-1031.00|.02|.03","Conservation Scientists (incl. Range Managers, Park Naturalists)","F1|F3|F5|F10",
  "yes - 19-1031.00 soil-management task row seen (0.002% of conversations, Feb-2025 file, partial view)",
  "Public: NRCS -23.8% (2025, via LM-030); NPS lost >25% and park rangers -34.1% (via LM-028)",
  "Core of NRCS/USFS/NPS/BLM conservation workforce; analytical tasks highly exposed, field tasks not; Park Naturalists 77th pct","LM-008|LM-009|LM-010|LM-011|LM-007|LM-028|LM-030"),
 ("19-1032","19-1032.00","Foresters","F1","not seen in partial AEI view (rows a-co only)",
  "Public: USFS lost ~16% (USDA OIG via LM-029) to >25% (PPS via LM-028) in 2025 - base definitions differ; reorganization 2026 (LM-036)",
  "Largest gap between theoretical exposure (59th pct) and usage applicability (20th pct); remote sensing/LiDAR inventory shifting tasks inside the role","LM-008|LM-009|LM-011|LM-028|LM-029|LM-036"),
 ("19-1023","19-1023.00","Zoologists and Wildlife Biologists","F2|F5","not seen in partial AEI view",
  "Public: FWS reductions reported but not quantified by team sources; state fish & wildlife agencies unmeasured","Species-identification and analysis tasks exposed (E2); AI species detection is the largest env AI use-case family in federal inventory (89 cases)","LM-008|LM-009|LM-027"),
 ("19-1013","19-1013.00","Soil and Plant Scientists","F10","yes - research/methods task row seen (0.009%)","Public: NRCS -23.8% (via LM-030)","High theoretical exposure (94th pct) despite 59% physical tasks: rubric rates written analysis tasks exposed","LM-008|LM-009|LM-007|LM-030"),
 ("19-2041","19-2041.00|.01|.02|.03","Environmental Scientists and Specialists, Including Health (incl. Climate Change Policy Analysts, Environmental Restoration Planners, Industrial Ecologists)","F3|F5|F13|F8",
  "yes - rows seen for .00, .01, .03 (0.004%-0.02% each; Industrial Ecologists 0.02%)",
  "Public: EPA staffing at 40-year lows (via LM-031); state agency demand visible in postings (SL-038, SL-073)",
  "Most LLM-exposed env occupation (98th pct; .01 99th, .03 98th); only 4% of tasks E0; prime site for Ac in documentation, review and reporting","LM-008|LM-009|LM-010|LM-011|LM-007|LM-031"),
 ("19-2043","19-2043.00","Hydrologists","F4","yes - two task rows seen (0.004%-0.005%)","Public: USGS (largest env AI inventory: 187 use cases) headcount change not quantified here","Hydrology/forecasting AI use cases mostly classical ML (36 water/hydrology cases, 10 deployed)","LM-008|LM-009|LM-007|LM-027"),
 ("19-2042","19-2042.00","Geoscientists, Except Hydrologists and Geographers","F4","yes - advisory task row seen (0.007%)","","Included for water/minerals/carbon storage roles","LM-008|LM-009|LM-007"),
 ("19-2021","19-2021.00","Atmospheric and Space Scientists","F6","yes - two rows seen (0.005%-0.007%)","Public: NOAA reductions reported in team sources (FS-002) but not quantified here","High on all indices (93rd/92nd/95th); NOAA reports 157 AI use cases","LM-008|LM-009|LM-010|LM-007|LM-027"),
 ("19-3051","19-3051.00","Urban and Regional Planners","F9","not seen in partial AEI view","","Planning analysis highly exposed (90th; usage 94th); public-meeting and mediation tasks remain relational","LM-008|LM-009|LM-010|LM-011"),
 ("19-4042","19-4042.00","Environmental Science and Protection Technicians, Including Health","F4|F13","not seen in partial AEI view","","Entry-level sampling/inspection; 40% physical tasks; AIOE indexed as SOC 2010 19-4091","LM-008|LM-009|LM-010|LM-011"),
 ("19-4071","19-4071.00","Forest and Conservation Technicians","F1|F12","not seen in partial AEI view",
  "Public: no non-fire seasonal hiring 2025; 2,000 seasonals titled forestry technician in 2026 (via LM-033); under-30 share of federal workforce 7.9% (via LM-028)",
  "The federal entry rung for land management (GS-0462); usage applicability 6th pct; entry path disrupted by hiring policy, not AI","LM-008|LM-009|LM-010|LM-011|LM-028|LM-033"),
 ("19-4044","19-4044.00","Hydrologic Technicians","F4","not seen","","Small; sensor-network supervision is the change vector","LM-008|LM-009|LM-011"),
 ("19-5011","19-5011.00","Occupational Health and Safety Specialists","F13","yes - safety-training task row seen (0.002%)","","Fastest-growing env-adjacent occupation in 2022-32 BLS vintage; AIOE indexed as 29-9011","LM-008|LM-009|LM-010|LM-011|LM-007"),
 ("19-5012","19-5012.00","Occupational Health and Safety Technicians","F13","not seen","","","LM-008|LM-009|LM-010|LM-011"),
 ("11-9121","11-9121.00|.01|.02","Natural Sciences Managers (incl. Water Resource Specialists)","F5|F8","yes - 11-9121.02 water-quality monitoring oversight row seen (0.004%)","Public: management layers affected by reorganizations (USFS regional office closures, via LM-036)","Indices disagree most here (AIOE 90th vs usage 38th)","LM-008|LM-009|LM-010|LM-011|LM-007|LM-036"),
 ("17-2081","17-2081.00","Environmental Engineers","F3|F4","not seen in partial view (17-2051.02 water/wastewater engineer rows seen)","","Consulting-heavy; exposure high on all indices","LM-008|LM-009|LM-010|LM-011"),
 ("17-3025","17-3025.00","Environmental Engineering Technologists and Technicians","F4","not seen","","","LM-008|LM-009|LM-010|LM-011"),
 ("13-1041","13-1041.00|.01","Compliance Officers (incl. Environmental Compliance Inspectors)","F8|F13","not seen","","Inspection (field) vs documentation (desk) split within occupation; Env Compliance Inspectors 78th pct","LM-008|LM-009|LM-010|LM-011"),
 ("13-1199","13-1199.05","Sustainability Specialists (within Business Operations Specialists, All Other)","F14","yes - sustainability-initiative assessment row seen (0.002%)",
  "Private: 46% of large-firm sustainability functions grew headcount vs 25% cut; compliance priority up (via LM-040)","97th pct theoretical exposure; disclosure-rule volatility drives demand more than AI","LM-008|LM-009|LM-007|LM-040"),
 ("11-1011","11-1011.03","Chief Sustainability Officers","F14","not seen","","","LM-008"),
 ("45-4011","45-4011.00","Forest and Conservation Workers","F1|F12","not seen",
  "Public: probationary firings incl. trail crews (FC sources); trail miles maintained -22% in 2025 (via LM-034)","Least exposed env occupation (17th pct; 82% physical tasks); robotics/sensing not LLMs is the relevant vector","LM-008|LM-009|LM-010|LM-011|LM-034"),
 ("33-2011","33-2011.00","Firefighters (incl. wildland)","F12","not seen",
  "Public: USWFS established Jan 2026 (via LM-035); wildland fire management series up while other land-management occupations fell (via LM-028); USFS 10,496 WFF vs 11,300 goal (via LM-029)",
  "No dedicated wildland SOC; OPM 0456/0462 are the real units; low LLM exposure; fire intelligence roles are the AI frontier (FS/DC)","LM-008|LM-009|LM-010|LM-011|LM-028|LM-029|LM-035"),
 ("33-2022","33-2022.00","Forest Fire Inspectors and Prevention Specialists","F12","not seen","","Small; v1 crosswalk misses this code","LM-008|LM-009|LM-011"),
 ("33-1021","33-1021.00","First-Line Supervisors of Firefighting and Prevention Workers","F12","not seen","","v1 crosswalk mistitles this code as 'Fire Inspectors'","LM-011"),
 ("33-3031","33-3031.00","Fish and Game Wardens","F2","not seen","","State-employer dominated; low exposure","LM-008|LM-009|LM-010|LM-011"),
 ("51-8031","51-8031.00","Water and Wastewater Treatment Plant and System Operators","F4 (v1 has no drinking-water/wastewater competencies)","not seen",
  "Local/utility employer; 2022-32 decline projected","Lowest usage applicability of any env occupation (0.6th pct); SCADA automation and cyber, not LLMs, drive change","LM-008|LM-009|LM-010|LM-011"),
 ("47-4041","47-4041.00","Hazardous Materials Removal Workers","F13","not seen","","Remediation field work; very low exposure","LM-008|LM-009|LM-010|LM-011"),
 ("15-2051","15-2051.00","Data Scientists","F7","not seen","","Env data science has no SOC; generic data scientist is the proxy (v1 F7)","LM-008|LM-009|LM-011"),
 ("15-1299","15-1299.02","Geographic Information Systems Technologists and Technicians","F7","not seen","","92nd pct theoretical exposure; core of env geospatial work","LM-008"),
 ("19-2099","19-2099.01","Remote Sensing Scientists and Technologists","F7","not seen","","Imagery processing tasks E2; USGS remote sensing is the largest env AI use-case cluster","LM-008|LM-027"),
 ("19-1029","19-1029.00|.04","Biological Scientists, All Other (incl. Biologists)","F2|F5","not seen","","","LM-008|LM-009|LM-010|LM-011"),
 ("25-1053","25-1053.00","Environmental Science Teachers, Postsecondary","F11","not seen","","Academic actor; high exposure on usage indices","LM-008|LM-009|LM-010|LM-011"),
 ("13-2099","13-2099.00","Financial Specialists, All Other (conservation/climate finance proxy)","F15","not seen","","Weak proxy; conservation finance unmeasured","LM-008|LM-009|LM-010|LM-011"),
]
cols = ["soc_code","onet_soc","title","emst_v1_families","in_aei_data","exposure_signals","employment_trend_signal","notes","source_ids"]
with open(os.path.join(H, "env_occupations_in_scope.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
    for soc, onet, title, fam, aei, trend, notes, srcs in OCC:
        key = soc
        if soc == "13-1199": key = "13-1199.05"
        if soc == "11-1011": key = "11-1011.03"
        if soc == "15-1299": key = "15-1299.02"
        if soc == "19-2099": key = "19-2099.01"
        es = sig(key) if key in sc.index else sig(soc)
        bt = bls(soc)
        w.writerow(dict(soc_code=soc, onet_soc=onet, title=title, emst_v1_families=fam, in_aei_data=aei, exposure_signals=es,
                        employment_trend_signal="; ".join(x for x in [bt, trend] if x), notes=notes, source_ids=srcs))

RS_COLS = ["signal_id","role_title","sector_actor","subsector","signal_type","description","driver","horizon","evidence_label","source_ids","related_v1_codes","proposed_by"]
RS = [
 ("RS-LM-01","Federal entry-level land-management technicians and student trainees (GS-0462/0404/0499)","federal","public lands; forestry; recreation","entry-path-at-risk",
  "2025 hiring freeze, probationary firings and no non-fire seasonal hiring cut the federal entry rung; 2,000 seasonals restored in 2026; under-30 share 7.9%; student trainee occupations down. Driver is fiscal/policy, not AI; v1 CLD logic attributes ladder risk to automation only",
  "fiscal|policy-reform","now","E","LM-028|LM-033|LM-032|LM-038","4.1.1|4.2.5|1.3.2|4.1.5"),
 ("RS-LM-02","Early-career analysts in high-LLM-exposure environmental occupations (environmental specialists, planners, compliance and sustainability analysts)","private|ngo|state","environmental consulting; corporate sustainability; planning","entry-path-at-risk",
  "Env analytical occupations sit at the 90th-99th exposure percentile; private payroll evidence shows 22-25-year-olds in top-exposure quintiles ~19% below counterfactual by June 2026 via reduced hiring. No environment-specific employment evidence exists yet; ADP undercovers government",
  "AI","1-3y","S","LM-005|LM-006|LM-008","6.1.1|6.1.2|6.4.1|6.4.4|3.6.2|5.1.1"),
 ("RS-LM-03","Environmental review and NEPA document specialists","federal|state|private","environmental review; permitting","transforming-role",
  "Enterprise genAI drafting/summarizing tools are available near agency-wide at EPA (10,000-50,000 users) and DOI/USDA (50,000+ for some tools) while custom NEPA/permitting AI remains pilot or pre-deployment (5 cases, 0 deployed). NEPA procedure changes (SC) shorten documents and timelines. Task compression is plausible; staffing effect unobserved",
  "AI|policy-reform","1-3y","J","LM-027|LM-008","6.1.4|6.1.2|6.4.4|6.4.1"),
 ("RS-LM-04","Wildland fire operations and management positions","federal|tribal|state","wildland fire","merging-roles",
  "DOI fire programs consolidated into the U.S. Wildland Fire Service (Jan 2026) with aligned USWFS/USFS qualification standards due Jan 2027; wildland fire management series grew while other land-management occupations fell",
  "policy-reform","now","E","LM-035|LM-028|LM-029","4.3.1|4.3.2|4.3.3|4.3.4"),
 ("RS-LM-05","Forest plan monitoring coordinators and resource data stewards","federal|state","public lands","skill-shift",
  "2012-rule plans devote 22% of components to monitoring (median 34 per plan) vs 1.8% in 1982-rule plans; 1,506 monitoring questions across 45 plans; reporting/data-system language is the most-named method (16% of questions). Demand is for indicator design, evaluation reporting and data stewardship rather than for specific field methods",
  "policy-reform","now","E","LM-017","3.1.5|3.2.5|2.2.1|2.2.5|1.1.2"),
 ("RS-LM-06","Partnership, cross-boundary and Tribal coordination roles","federal|state|tribal|ngo","public lands","transforming-role",
  "Per 1,000 components, 2012-rule plans name partnership touchpoints 31.4 vs 10.0 (1982 rule), Tribal 27.3 vs 10.0, cross-boundary 13.8 vs 4.5; USFS reorganization expands states' role (via AS). GNA/shared stewardship rarely appear in plan text (21 components) because they operate through agreements",
  "policy-reform|fiscal","now","E","LM-017|LM-037","5.2.5|6.5.1|6.5.2|6.5.3|6.5.4"),
 ("RS-LM-07","Geospatial, remote-sensing and environmental data analysts in science bureaus","federal","geospatial; monitoring","transforming-role",
  "Of 504 AI use cases in environmental bureaus, 232 are classical ML; remote sensing/imagery (63; 11 deployed), species detection (89; 11 deployed) and hydrology (36; 10 deployed) dominate. AI is entering the analysis pipeline, mostly pre-deployment/pilot",
  "AI|sensing-tech","1-3y","E","LM-027","2.1.2|2.6.1|2.6.2|2.6.4|2.4.1"),
 ("RS-LM-08","Field survey biologists and technicians (species and habitat surveys)","federal|state|tribal|ngo|private","wildlife; fisheries; botany","skill-shift",
  "Sensor-based detection (acoustic, camera, eDNA, imagery) is the main technology vector for field surveys, but plans rarely name methods (remote sensing in 3 monitoring questions, eDNA in 3). Method change will appear in protocols, PDs and postings, not plans; no index measures this sensing-substitution vector",
  "sensing-tech|AI","3-5y","J","LM-017|LM-027","1.4.2|4.1.2|2.6.2|1.6.2|1.1.2"),
 ("RS-LM-09","Corporate sustainability and GHG/ESG reporting analysts","private","corporate sustainability","transforming-role",
  "Sustainability Specialists are at the 97th exposure percentile; large-firm functions report growth (46%) more than cuts (25%) and higher compliance priority. Disclosure-rule volatility, not AI, is the dominant short-run driver",
  "AI|market|policy-reform","1-3y","J","LM-008|LM-040","3.6.2|3.6.5|6.6.1"),
 ("RS-LM-10","Senior scientific and technical staff in regulatory agencies (EPA and similar)","federal","environmental health; regulation","declining-role",
  "EPA staffing at 40-year lows; departing staff median tenure ~30 years vs ~11 years for those remaining (via FS). This removes the top of the ladder - the reviewers who certify AI-compressed work - a CLD mechanism v1 does not model",
  "fiscal|policy-reform|demographic","now","E","LM-031","6.7.1|6.7.4|7.2.1|7.2.2"),
 ("RS-LM-11","Park rangers and interpretive staff","federal","recreation; interpretation","declining-role",
  "Park rangers -34.1% (via PPS/FH). v1 records a High CLD on 5.5.1 T1 (visitor services) attributed to AI compression; the observed decline is fiscal/policy-driven",
  "fiscal|policy-reform","now","E","LM-028","5.5.1|5.1.3|5.4.5"),
 ("RS-LM-12","Recreation, travel-management and special-uses specialists","federal|state","recreation; lands","skill-shift",
  "Recreation is the largest theme in plan standards (3,819 components, 15%) and monitoring questions (17%); ROS and scenery classifications appear in 62 and 68 plans; special-use authorizations 363 touchpoints. v1 has no recreation planning or travel management competency",
  "policy-reform|demographic","now","E","LM-017","5.5.1|5.5.2|6.2.3"),
 ("RS-LM-13","Water and wastewater operators","local|private","drinking water; wastewater","skill-shift",
  "Lowest usage-based AI applicability of any env occupation (0.6th pct) and 75% physical tasks; change vector is SCADA/automation and cybersecurity, not LLMs; v1 has no water-utility competencies (audit)",
  "automation-robotics","3-5y","J","LM-009|LM-011|LM-025",""),
]
with open(os.path.join(H, "role_signals.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(RS_COLS)
    for r in RS: w.writerow(list(r) + ["LM"])

VA_COLS = ["element","v1_location","verdict","rationale","evidence_label","source_ids","proposed_by"]
VA = [
 ("Automation type vocabulary A/Ac/H/S/V (single dimension)","Dimension Tags: T13 Tx Auto Type","change",
  "One code mixes three constructs: technical exposure, deployment mode (who executes) and staffing outcome. In the pilot, v1 'A' covers both LLM-augmented desk tasks and tool-assisted physical tasks (6 of 9 matched A tasks are physical; 3 of 9 are E0). Split into exposure-by-vector, deployment mode and role-level outcome","E","LM-020|LM-008|LM-009"),
 ("Ac (compressive augmentation)","T13 Auto Type = Ac; DD-2","change",
  "Keep the idea; tighten the definition. Its measurable core equals Eloundou E1 (task time cut by at least half at equal quality): 11 of 13 matched Ac tasks are E1/E2 and 10 of 13 sit at T2-T4 on the GPT-4 automation rubric. Move 'headcount compression plausible' to a role/organization outcome that depends on demand, budget and policy (Bessen; Humlum and Vestergaard)","E","LM-008|LM-048|LM-073|LM-051"),
 ("S (substitution) calls","T13 Auto Type = S (4 in database; 9 in synthesis)","needs-evidence",
  "All 4 database S tasks are rated exposed (E1/E2), but none at T4 (full automation) on the GPT-4 rubric; federal inventory shows NEPA/permitting AI at pilot/pre-deployment (0 deployed) and public-comment tools at pilot. Present S only where deployment is registered and directive usage is high. The synthesis-database discrepancy (9 vs 4) must be reconciled","E","LM-027|LM-008|LM-022|LM-019"),
 ("V (supervision)","T13 Auto Type = V; R4, R10","carry",
  "The A/V current-deployment rule matches the AEI distinction between directive (system executes) and collaborative modes and Microsoft's 'AI action' vs 'user goal'. Re-anchor examples to registered deployments","J","LM-004|LM-009|LM-027"),
 ("H (human-essential)","T13 Auto Type = H","change",
  "Separate descriptive 'no current technical pathway' from normative 'should remain human' (accountability). Of 10 matched H tasks, 7 are E0 but 3 are E2 (e.g., land-use dispute mediation): the work is LLM-exposed in capability terms even where authority must stay human. Domain 7 all-H is normative (agrees with CA)","E","LM-008|LM-025"),
 ("FC/DC structural pattern ('H only in FC/SC primary')","task13_crossdomain_synthesis.md Section 4.3; R1","retire",
  "Circular (R1 told coders to expect it; FC and H share criteria) and contradicted by the data: the database holds 9 H tasks on DC-primary competencies, not the 1 anomaly claimed. Re-test only with blind coding","E","LM-019|LM-022|LM-025"),
 ("Tacit knowledge density Hi/Med/Lo","T13 Tx Tacit","change",
  "Near-deterministic with auto type in v1 (no Hi-tacit Ac/S/V) - a coder-inference signature. Externally, tacit density is predictive but not determinative (Lo: 17 of 19 matched tasks exposed; Hi: 5 of 11 exposed). Rate independently (SME panel; O*NET experience/job-zone and work-context descriptors) before linking to exposure","E","LM-020|LM-008"),
 ("Career-ladder position P/C/X","T13 Tx Career","change",
  "Derive from role profiles (grade band, job zone, FWD grade distribution), not assert per task. P tasks in the pilot are more often E0 (9 of 22) than C tasks (4 of 20) because entry work is physical; ladder risk concentrates in desk entry tasks","E","LM-008|LM-044"),
 ("Automation vector AI/Ro/Cv","T13 Tx Vector","change",
  "Add a sensing/remote-observation vector (field observation replaced by sensors, imagery, eDNA, acoustic monitoring) - the dominant environment-specific vector, measured by no index; calibrate Ro against the Sep 2026 robot task index and Webb robots","J","LM-027|LM-070|LM-049"),
 ("Time horizon 1/2/3/N","T13 Tx Horizon","change",
  "Replace with dated assessments plus deployment-stage evidence (OMB inventory stages; adoption shares). Horizon 3 is never used; N fuses 'no horizon' with H; all Ac are Horizon 1 and all H are N (collinear)","E","LM-019|LM-027"),
 ("Career-ladder destruction (CLD) flag and severity","T13 CLD Flag, CLD Severity; R9","change",
  "Keep the concept (strongly supported by canaries evidence in private payroll). Compute at pathway level and attribute drivers: the observed 2025-26 public-sector ladder damage is fiscal/policy (hiring freeze, seasonal halt, senior exits), not AI. Add a 'top-of-ladder loss' mechanism. Fix vocabulary drift (Yes/True; 'Highest', 'Ungraded' not in dictionary)","E","LM-005|LM-028|LM-031|LM-019"),
 ("S-trajectory flag","T13 S-Trajectory Flag","change",
  "Convert to a watchlist with explicit external triggers (e.g., matched AEI tasks show high directive share and success; deployment registered in inventory; posting volumes fall)","J","LM-001|LM-027"),
 ("Stability tier","Dimension Tags: Stability Tier","retire",
  "Compute from dated signals rather than store; current rule mixes reform flags and exposure into one label","J","LM-025"),
 ("Labor Market Crosswalk (family -> SOC)","Labor Market Crosswalk sheet","change",
  "Code/title errors verified against BLS matrix: 19-1012 is Food Scientists and Technologists (Farm and Home Management Educators is 25-9021); 33-1021 is First-Line Supervisors of Firefighting and Prevention Workers, not Fire Inspectors; 29-9021 (Health Information Technologists) and 25-4031 (Library Technicians) are poor fits. O*NET-SOC details exist for several 'no SOC' families (13-1199.05, 11-1011.03, 19-2041.01-.03, 15-1299.02, 19-2099.01, 19-1031.02/.03). Rebuild at O*NET-SOC 8-digit, many-to-many, with OPM series","E","LM-011|LM-008|LM-019"),
 ("Database vs synthesis counts","Dimension Tags vs task13_crossdomain_synthesis.md","needs-evidence",
  "666 tasks in database vs 645 in synthesis; S 4 vs 9; H 146 vs 136; Ac 101 vs 92. Treat the database as authoritative and archive synthesis counts as superseded","E","LM-019|LM-022"),
 ("Exposure provenance column","T13 Data Provenance","carry","Correct instinct; extend to rater type, codebook version and date for every assessment","J","LM-025"),
 ("Workforce Signals dashboard","Workforce Signals sheet","retire","Static counts; recompute from the change-signal layer","J","LM-019"),
 ("External exposure assessments (none in v1)","n/a","add",
  "Add attributed external assessments per task (Eloundou labels, AEI task penetration/directive share, Microsoft IWA metrics, physical flag), with crosswalk match type and confidence; show agreement with v1 analyst labels","E","LM-008|LM-009|LM-001"),
]
with open(os.path.join(H, "v1_assessment.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(VA_COLS)
    for r in VA: w.writerow(list(r) + ["LM"])

CC_COLS = ["cand_id","proposed_title","description","craft_primary","craft_secondary","subsector","sector_actors","change_type","driver","evidence_label","source_ids","related_v1_codes","rationale","proposed_by"]
CC = [
 ("C-LM-01","Design and run plan-level monitoring programs that answer management questions",
  "Translate plan components into monitoring questions and indicators, select methods and data sources, run evaluation cycles and report results that trigger management responses",
  "DC","SC","public lands; water; wildlife","federal|state|tribal|ngo","transforming","policy-reform|AI","E","LM-017",
  "3.1.5|3.2.5|1.1.2|2.2.5","2012-rule plans: 22% of components are monitoring; 1,506 explicit monitoring questions; v1 covers performance monitoring and adaptive management generically but not plan monitoring programs"),
 ("C-LM-02","Manage recreation settings and visitor use to sustain resources and experiences",
  "Apply recreation opportunity and scenery classifications, estimate visitor use and capacity, manage travel and access, and monitor social and resource conditions",
  "SC","FC","recreation; public lands","federal|state|local|tribal|ngo|private","stable","demographic|policy-reform","E","LM-017",
  "5.5.1|6.2.3|5.6.2","Recreation is the largest theme in standards (15%) and monitoring questions (17%); ROS in 62 plans, scenery classes in 68; v1 has only visitor information services. Flag to DB/FC for drafting"),
 ("C-LM-03","Administer resource-use authorizations (grazing, minerals, special uses) and their compliance",
  "Process, condition, monitor and enforce authorizations for grazing, mineral activity and special uses, coordinating required consultations",
  "SC","FC","public lands; range; minerals","federal|state|tribal","stable","policy-reform","E","LM-017",
  "5.5.2|6.1.3|6.1.5","Plan components mention grazing in 1,785, mining in 1,075 and special uses in 924; authorization touchpoints total 796; v1 5.5.2 is generic permit administration. Overlaps SC lane"),
 ("C-LM-04","Steward and interpret the authoritative datasets and models behind plan requirements",
  "Maintain, quality-check and analyse agency corporate data and reference models (inventory, vegetation maps, range-of-variation analyses, watershed condition, fire regime, visitor monitoring) and explain their limits in decisions",
  "DC","FC","public lands; forestry; water; fire","federal|state|tribal|ngo|private|academic","transforming","AI|sensing-tech","E","LM-017",
  "2.2.1|2.2.3|1.3.2|2.4.2","Plans depend on agency classifications and corporate systems (ROS 62 plans; hydrologic models 53; NRV 37; corporate systems 28; FIA 18; LANDFIRE 14) more than on named AI tools; durable data-stewardship competence, tool names belong in L4"),
 ("C-LM-05","Sustain institutional knowledge through workforce attrition and succession",
  "Identify critical tacit knowledge held by departing staff, design capture and transfer (paired work, after-action records, mentoring), and rebuild review capacity when senior reviewers leave",
  "SC","FC","cross-cutting","federal|state|tribal|ngo|local","emerging","demographic|fiscal|AI","E","LM-031|LM-028",
  "7.2.2|3.3.1|3.5.3","EPA departing staff median tenure ~30 years; USFS/NPS losses >16-25%; v1 7.2.2 addresses tacit formation under AI but not knowledge loss under attrition - the binding constraint in 2025-26"),
 ("C-LM-06","Use labor-market and AI-change evidence in workforce and training plans",
  "Read exposure indices, usage data, posting and headcount signals with their limits; set staffing and training priorities; avoid treating exposure scores as job-loss forecasts",
  "DC","SC","cross-cutting","federal|state|local|tribal|ngo","new","AI|fiscal","J","LM-008|LM-001|LM-038",
  "3.5.1|3.3.1|3.1.5","EO 14356 annual staffing plans and AI strategies require managers to justify positions; no v1 competency covers evidence-based workforce planning for program managers (borderline; IO/FH to judge whether it belongs in a manager role profile)"),
]
with open(os.path.join(H, "candidate_competencies.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(CC_COLS)
    for r in CC: w.writerow(list(r) + ["LM"])
print("ok")
