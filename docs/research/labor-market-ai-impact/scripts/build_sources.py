import csv, os
OUT = "/home/claude/emst/docs/research/labor-market-ai-impact"
A = "2026-10-23"
NA = "not accessed (shared web-search budget exhausted; not retrievable this session)"

S = []
def s(id_, title, pub, date, url, typ, acc, used, q, st, why):
    S.append(dict(source_id=id_, title=title, author_or_publisher=pub, date_published=date, url=url, source_type=typ,
                  accessed=acc, used_for=used, quality=q, status=st, why_chosen=why))

# --- read this session (primary data / primary pages)
s("LM-001", "Anthropic/EconomicIndex dataset README (release list)", "Anthropic", "2026-06-26 (latest release folder)",
  "https://huggingface.co/datasets/Anthropic/EconomicIndex/blob/main/README.md", "dataset", A,
  "AEI release history (2025-02-10, 2025-03-27, 2025-09-15, 2026-01-15, 2026-03-24, 2026-06-26) and the labor_market_impacts and robot_exposure folders; licence (CC-BY data, MIT code)",
  "High; primary dataset documentation (variables not documented on page)", "current", "Primary source for what AEI data exist and when; needed to design the EMST join")
s("LM-002", "The Anthropic Economic Index (landing page)", "Anthropic", "2026-06-26 (page update)", "https://anthropic.com/economic-index",
  "index", A, "Confirms the index tracks occupations, states and collaborate-vs-delegate patterns; dashboard did not render for the fetcher",
  "Medium; primary but thin as rendered", "current", "Primary landing page for the index")
s("LM-003", "Anthropic Economic Research team publication list", "Anthropic", "2026-10-16 (latest item)", "https://anthropic.com/research/team/economic-research",
  "grey-literature", A, "Dates and titles of all 2025-2026 AEI-related outputs incl. 'What work can robots do?' (2026-09-30), Cadences (2026-06-26), labor-market impacts (2026-03-05)",
  "High; primary publication list", "current", "Establishes the latest releases as of Oct 2026")
s("LM-004", "Anthropic Economic Index (wiki compendium, raw page)", "AI Wiki (aiwiki.ai), community-edited", "2026 (undated)",
  "https://www.aiwiki.ai/wiki/anthropic_economic_index/raw", "grey-literature", A,
  "Secondary summary of each AEI report's statistics (augmentation/directive shares by release; API 77% directive; Jan 2026 primitives; observed exposure; survey) and a list of critiques",
  "Medium-Low; secondary, community-edited; numbers not re-verified against primary pages", "current",
  "Only reachable synthesis of the primary AEI reports after the search budget was exhausted; used for context, never as sole support for a key claim")
s("LM-005", "Canaries in the Coal Mine? (August 2026 update)", "Brynjolfsson, Chandar, Chen; Stanford Digital Economy Lab", "2026-08-12",
  "https://digitaleconomy.stanford.edu/news/canariesaug26/", "grey-literature", A,
  "Payroll (ADP) evidence: 22-25-year-olds in most-exposed occupations ~19% below counterfactual (June 2026) vs 15% (July 2025 vintage); via hiring; concentrated where usage automates; ADP > national survey estimates, gap concentrated in education, health care and public administration",
  "High; transparent admin-data design, descriptive not causal", "current", "Latest and strongest early-outcome evidence on entry-level effects; tests the CLD hypothesis")
s("LM-006", "Canaries, interest rates and timing: more on recent drivers of employment changes for young workers", "Stanford Digital Economy Lab", "2026-02-09 (modified 2026-06-09)",
  "https://digitaleconomy.stanford.edu/news/canaries-interest-rates-and-timinga-more-on-recent-drivers-of-employment-changes-for-young-workers",
  "grey-literature", A, "Robustness: interest-rate exposure does not explain the gap; with firm-time FE the relative decline appears from 2024",
  "High; authors' own robustness note", "current", "Judging the canaries method and its timing claims")
s("LM-007", "AEI release 2025-02-10: onet_task_mappings.csv (task share of conversations)", "Anthropic", "2025-02-10",
  "https://www.huggingface.co/datasets/Anthropic/EconomicIndex/blob/ed82ec6d3701b067db983405b214fc0d6fa580f2/onet_task_mappings.csv",
  "dataset", A + " (partial: blob view truncated alphabetically at tasks beginning 'co...')",
  "Presence and size of environmental task rows (each 0.002%-0.02% of conversations) for 19-2041, 19-1031, 19-2043, 19-2021, 13-1199.05, 11-9121.02 etc.",
  "High as data; Medium as read (partial view via fetcher, values transcribed by a summarizer)", "superseded-by:AEI release_2026_06_26 and labor_market_impacts task penetration",
  "Only AEI task-level file reachable; Hugging Face blocked from the shell")
s("LM-008", "GPTs-are-GPTs replication data (task-level E0/E1/E2 human and GPT-4 labels; occupation scores; bundled O*NET 27.x tasks, BLS files)",
  "Eloundou, Manning, Mishkin, Rock / OpenAI (GitHub openai/GPTs-are-GPTs)", "2024 (Science publication); repo snapshot cloned 2026-10-23",
  "https://github.com/openai/GPTs-are-GPTs", "dataset", A,
  "19,265 O*NET task statements with human and GPT-4 exposure labels and GPT-4 automation rubric (T0-T4); occupation-level alpha/beta/gamma; used for env occupation percentiles and the v1 calibration pilot",
  "High; open replication data, transparent rubric; ratings date from 2023", "current", "Canonical task-level theoretical exposure measure with open task-level data")
s("LM-009", "Working with AI: results files v1.1 (AI applicability scores, IWA metrics, physical-task flags)",
  "Tomlinson, Jaffe, Wang, Counts, Suri / Microsoft (GitHub microsoft/working-with-ai)", "2026 (v1.1, NeurIPS 2026 version)",
  "https://github.com/microsoft/working-with-ai", "dataset", A,
  "Usage-based AI applicability by SOC (785) and IWA (332); O*NET task-level physical flag; env occupation percentiles; pilot physical-task check",
  "High; open data, documented metrics; single platform (Bing Copilot)", "current", "Second, independent usage-based measure; only open task-level physical classification")
s("LM-010", "AIOE and related datasets (AIOE, LM-AIOE)", "Felten, Raj, Seamans (GitHub AIOE-Data/AIOE)", "2021 (SMJ); LM AIOE 2023",
  "https://github.com/AIOE-Data/AIOE", "dataset", A, "Ability-based occupation exposure for 774 SOC codes; percentiles for env occupations; detection of SOC 2010 vintage in the index",
  "Medium-High; widely used; ability-level, SOC 2010 vintage", "current", "Most-cited occupation-level AI exposure index; needed for index agreement test")
s("LM-011", "Employment Projections 2022-32, Table 1.2 Employment by detailed occupation (copy bundled in LM-008 repo)", "U.S. Bureau of Labor Statistics", "2023-09",
  "", "government", A, "2022 employment and 2022-32 projected % change for env occupations; verification of SOC titles in v1 crosswalk",
  "High; official projections", "superseded-by:BLS Employment Projections 2024-34 (released 2025; not retrieved)", "Only BLS projection vintage reachable this session; used as baseline with explicit supersession flag")
s("LM-012", "Anthropic reports on trends in occupations susceptible to AI and whether there are changes in the labor market", "GIGAZINE", "2026-03-06",
  "https://gigazine.net/gsc_news/en/20260306-labor-market-impacts-ai-anthropic/", "news", A,
  "Secondary account of AEI observed exposure: no unemployment effect in highest-exposure occupations; slight slowdown for 22-25; 30% of workers zero observed exposure; tree trimming and farm equipment operation cited as beyond reach",
  "Medium-Low; secondary summary", "current", "Primary page (LM-026) could not be fetched")
s("LM-013", "Analyzing Anthropic's...Analysis", "Talent Lab Solutions (Villanueva Blackett, Oppong)", "2026-03-31",
  "https://talentlabsolutions.substack.com/p/analyzing-anthropicsanalysis", "grey-literature", A,
  "Critiques of the AEI labor-market-impacts study: reliance on BLS projections, short window, Claude-only exposure, US-only, conflict of interest",
  "Low-Medium; practitioner blog, some critiques sound", "current", "Only located methodological critique of observed exposure")
s("LM-014", "Anthropic Economic Index: Cadences (June 2026) news summary", "Noqta", "2026-06", "https://noqta.tn/en/news/anthropic-economic-index-cadences-ai-work-patterns-2026",
  "news", A, "June 2026 release: hourly sampling, monthly breakdowns incl. Cowork and API, artifact classifier (93% of conversations produce an artifact), ~9,700 linked survey responses",
  "Low-Medium; secondary", "current", "Primary June 2026 report not reachable")
s("LM-015", "The AI Skills Shift: Mapping Skill Obsolescence, Emergence, and Transition Pathways in the LLM Era (arXiv:2604.06906)", "Jadhav and Danve", "2026-04-08",
  "https://arxiv.org/pdf/2604.06906", "grey-literature", A,
  "Confirms AEI labor_market_impacts release contains exposure for 756 occupations and task penetration for 17,998 tasks plus automation/augmentation for 3,364 tasks; critique of annotation-based exposure; 78.7% augmentation under its own aggregation",
  "Low-Medium; unreviewed preprint, heuristic scoring", "current", "Documents AEI data structure and shows how augmentation shares vary with aggregation choices")
s("LM-016", "The Impact of AI on Employment (blog)", "Irving Wladawsky-Berger", "2026-01", "https://blog.irvingwb.com/blog/2026/01/the-impact-of-ai-on-employment.html",
  "grey-literature", A, "Context only: restatement of canaries findings and skepticism (pre-trends, codified vs tacit hypothesis untested)", "Low; secondary", "current", "Context on reception of canaries")
s("LM-017", "OpenLMP plan catalog and plan components (217 plans; 58,544 components)", "OpenLMP project (sister repo /home/claude/lmps)", "2026-10-21",
  "local: /home/claude/lmps/catalog/plans.csv; /home/claude/lmps/plans/*/*/*/components.csv", "dataset", A,
  "Quantitative demand-signal pass: monitoring, standards, coordination touchpoints, authoritative data/models, rule-era comparison",
  "High for provenance; Medium representativeness (95% USFS, western states, extraction confidence mean 0.61)", "current", "Only machine-readable corpus of plan requirements")
s("LM-018", "OpenLMP data dictionary and controlled vocabularies (themes.yaml, label-taxonomy.yaml)", "OpenLMP project", "2026-10",
  "local: /home/claude/lmps/docs/data-dictionary.md; /home/claude/lmps/schema/vocab/", "standard", A, "Field definitions and vocabularies for the LMP pass", "High; primary", "current", "Required reading before analysis")
s("LM-019", "EMST v1 database 20260223_SkillsTaxonomy_Core_V3_reconciled (copyB): Dimension Tags, Data Dictionary, Labor Market Crosswalk, Workforce Signals",
  "EMST v1 project", "2026-03", "local: /home/claude/emst/legacy/v1/data/20260223_SkillsTaxonomy_Core_V3_reconciled__copyB_aaf34c8c.xlsx", "dataset", A,
  "T13 exposure distributions, collinearity, vocabulary drift, crosswalk errors", "High; primary v1 data", "current", "Object of appraisal")
s("LM-020", "EMST v1 baseline extract: tasks.csv (666 tasks with exposure dimensions)", "EMST v2 Data Engineer (DE)", "2026-10-23",
  "local: /home/claude/emst/data/v1_baseline/tasks.csv", "dataset", A, "Sampling frame and labels for the calibration pilot", "High; normalized v1 data with provenance", "current", "Normalized v1 source")
s("LM-021", "Task 12 Working Record: Exposure Instrument Finalization and Domain 4 Pilot", "EMST v1 project", "2026-02",
  "local: /home/claude/emst/legacy/v1/docs/domain4_task12_working_record.md", "grey-literature", A, "Instrument definitions (Section 1), D6 stress test (9 S calls), boundary rules",
  "Medium; single-analyst working record", "current", "Assigned reading; defines the instrument")
s("LM-022", "Task 13: AI/Robotics Exposure Classification - Cross-Domain Synthesis", "EMST v1 project", "2026-02",
  "local: /home/claude/emst/legacy/v1/docs/task13_crossdomain_synthesis.md", "grey-literature", A, "Standing rules R1-R12, CLD register, FC/DC structural claim, S register",
  "Medium; single-analyst synthesis; counts inconsistent with database", "current", "Assigned reading")
s("LM-023", "AI Workforce Futures and Environmental Management Infrastructure (deep-research-report 8)", "EMST v1 project (AI-assisted research report)", "2026-03",
  "local: /home/claude/emst/legacy/v1/docs/deep-research-report (8).md", "grey-literature", A,
  "What v1 relied on: no env-specific exposure analysis found; mentions Iceberg Index, OECD public-workforce AI report, career-ladder thinning literature",
  "Low-Medium; citations are unresolved tokens", "current", "To appraise the evidence base of v1 claims")
s("LM-024", "EMST v2 Architecture Hypotheses (provisional), sections 4 and 6", "Chief Taxonomy Architect (CA)", "2026-10-23",
  "local: /home/claude/emst/docs/research/chief-architect/architecture_hypotheses.md", "grey-literature", A, "Layered model L0-L6 and LM questions", "High; internal", "current", "Questions to answer")
s("LM-025", "EMST v1 Architecture Audit, section 10 (exposure instrument)", "Chief Taxonomy Architect (CA)", "2026-10-23",
  "local: /home/claude/emst/docs/audit/architecture-audit.md", "grey-literature", A, "Audit verdicts on the instrument to build on or challenge", "High; internal", "current", "Avoid duplicating CA's audit")
s("LM-026", "Labor market impacts of AI: A new measure and early evidence", "Massenkoff and McCrory / Anthropic", "2026-03-05",
  "https://www.anthropic.com/research/labor-market-impacts", "industry-report", "not accessed (fetch permission request timed out)",
  "Intended: definition of observed exposure and CPS-based outcome tests; reported only via LM-004 and LM-012", "Unknown; not read", "unverified",
  "Most relevant primary AEI outcome study; must be read in Phase 3")
s("LM-027", "2025 Federal Agency AI Use Case Inventory (individually reported and consolidated COTS use cases)", "OMB Office of the Federal CIO (GitHub ombegov)", "2026-04-13",
  "https://github.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory", "dataset", A,
  "Own counts: 504 use cases in env bureaus (USGS 187, NOAA 157, USDA NRE 76, EPA 29...); 61 of 347 stage-reported are deployed; 5 NEPA/permitting cases, none deployed; COTS genAI drafting/summarizing at EPA 10,000-50,000 users and DOI/USDA 50,000+ for some tools",
  "High; primary government dataset (agency self-report)", "current", "Direct, dated evidence of AI deployment stage in environmental agencies (also used by DC as DC-001)")

# --- cross-referenced from other roles (not re-read by LM)
X = "cross-referenced; not re-read by LM"
s("LM-028", "The Federal Workforce One Year into the Trump Administration (Fed Figures)", "Partnership for Public Service", "2026", "https://ourpublicservice.org/?p=47956",
  "grey-literature", X + " (FH-008)", "As reported by FH: USFS and NPS each lost >25%; park rangers -34.1%; student trainee occupations down; wildland fire management up; under-30 share 7.9%",
  "High (per FH); OPM data", "unverified", "Public environmental workforce change 2025-26; FH owns")
s("LM-029", "Forest Service wildfire season amid Trump cuts", "NewsNation", "2026-05-14", "https://www.newsnationnow.com/politics/forest-service-wildfire-season-trump-cuts/amp/",
  "news", X + " (FH-035)", "As reported by FH: USFS lost 16% of workforce in 2025 (USDA OIG data); 10,496 wildland firefighters vs 11,300 goal", "Medium (per FH)", "unverified",
  "Conflicting USFS loss estimate (16% vs >25%) flags base-definition issue")
s("LM-030", "Federal workforce shrank significantly in 2025, though a few offices saw gains", "Agri-Pulse", "2026-01-21",
  "https://www.agri-pulse.com/articles/24058-federal-workforce-shrank-significantly-in-2025-though-a-few-offices-saw-gains", "news", X + " (FS-042)",
  "As reported by FS: USFS -5,325 net; NRCS -23.8%", "Medium-High (per FS)", "unverified", "USDA agency-level changes")
s("LM-031", "EPA Hits 40-Year Lows in Staffing After Trump Targets Its Public Health Experts", "Inside Climate News", "2026-03-06",
  "https://insideclimatenews.org/news/06032026/trump-epa-staffing-lows/", "news", X + " (FS-003)", "As reported by FS: EPA staffing at 40-year lows; departing staff median tenure 30.3 years vs 10.8 for those remaining",
  "Medium-High (per FS)", "unverified", "Top-of-ladder tacit-knowledge loss signal")
s("LM-032", "Federal workforce down 317,000 (OPM Director statement)", "Transport Topics (wire)", "2025-12-10", "https://www.ttnews.com/article/federal-workforce-down-317000",
  "news", X + " (FH-030)", "As reported by FH: 2025 departures ~317,000 incl. DRP ~144k; hires 68k by end-Aug", "Medium (per FH)", "unverified", "Scale of federal contraction")
s("LM-033", "Neguse, Huffman press US Forest Service for answers on staffing levels ahead of summer", "Office of Rep. Joe Neguse", "2026-03-23",
  "https://neguse.house.gov/media/press-releases/neguse-huffman-press-us-forest-service-answers-staffing-levels-ahead-summer", "government", X + " (FC-014)",
  "As reported by FC: no non-fire seasonal hiring in 2025; 2,000 seasonals committed 2026; up to 1,400 red-card holders left", "Medium (per FC)", "unverified", "Entry-path (seasonal) disruption")
s("LM-034", "Letter to USFS regarding trail maintenance", "Rep. Kim Schrier et al.", "2026-03-23",
  "https://schrier.house.gov/sites/evo-subsites/schrier.house.gov/files/evo-media-document/letter-to-usfs-regarding-trail-maintenance-final.pdf", "government", X + " (FC-015)",
  "As reported by FC: trail miles maintained -22% in 2025; lost skills (equipment operation, rock masonry)", "Medium (per FC)", "unverified", "Output consequence of field-workforce loss")
s("LM-035", "U.S. Department of Interior Launches U.S. Wildland Fire Service", "Wildfire Task Force", "2026", "https://wildfiretaskforce.org/?p=106979",
  "grey-literature", X + " (AS-010)", "As reported by AS: USWFS established Jan 2026; ~5,780 federal + ~900 Tribal fire personnel", "Medium (per AS)", "unverified", "Fire workforce reorganization")
s("LM-036", "Forest Service to move HQ out of DC, shutter regional offices in sweeping overhaul", "Government Executive", "2026-04",
  "https://www.govexec.com/management/2026/04/forest-service-move-hq-out-dc-shutter-regional-offices-sweeping-overhaul/412566", "news", X + " (AS-020)",
  "As reported by AS: HQ to Salt Lake City, 9 regional offices closed, 15 state directors, 57 of 77 research stations closing", "Medium-High (per AS)", "unverified", "Reorganization affecting roles")
s("LM-037", "Forest Service shake-up will boost states' role - but even supporters have concerns", "Stateline (via Source NM)", "2026-04-14", "https://sourcenm.com/?p=28752",
  "news", X + " (AS-021)", "As reported by AS: state role expansion; Good Neighbor Authority; USFS lost ~16% (~5,900)", "Medium (per AS)", "unverified", "State response / devolution")
s("LM-038", "Executive Order 14356: Ensuring Continued Accountability in Federal Hiring", "The White House", "2025-10-15",
  "https://whitehouse.gov/presidential-actions/2025/10/ensuring-continued-accountability-in-federal-hiring", "legal", X + " (FH-029)",
  "As reported by FH: strategic hiring committees approve each vacancy; annual staffing plans", "High (per FH)", "unverified", "Why USAJOBS volume is now a policy signal, not a demand signal")
s("LM-039", "State works to recruit workers after thousands of federal employees laid off", "WHEC", "2025-02-25",
  "https://whec.com/top-news/state-works-to-recruit-workers-after-thousands-of-federal-employees-laid-off", "news", X + " (SL-023)", "As reported by SL: NY 'You're Hired' state recruitment of former federal staff", "Low (per SL)", "unverified", "State response example")
s("LM-040", "State of the Sustainability Profession 2026", "Trellis", "2026", "https://trellis.net/article/state-of-the-sustainability-profession-2026/",
  "industry-report", X + " (PS-010)", "As reported by PS: 46% grew headcount/budget vs 25% cut; 58% higher priority on compliance", "Medium (per PS)", "unverified", "Private-sector sustainability demand")
s("LM-041", "WEF's Future of Jobs Report 2025 highlights that green transition is a major driver of job growth", "ESG News (summary of WEF)", "2025-01", "https://esgnews.com/?p=33096",
  "news", X + " (FS-041)", "Existence and framing of WEF FoJ 2025 green-transition findings", "Low-Medium (per FS)", "unverified", "WEF primary not reachable")
s("LM-042", "LinkedIn Global Climate Talent coverage (green talent demand vs supply)", "Sustainability Magazine", "2024-10-02",
  "https://sustainabilitymag.com/articles/we-need-to-double-green-talent-to-meet-global-demand-by-2050", "news", X + " (PS-022)",
  "As reported by PS: green talent demand +11.6% vs supply +5.6% (2023-24)", "Medium (per PS)", "outdated", "Latest LinkedIn green-skills figure available to the team")
s("LM-043", "Burning Glass Institute (homepage: AI tracking, Skills-First)", "Burning Glass Institute", "2026-10-15", "https://www.burningglassinstitute.org/",
  "grey-literature", X + " (AS-038)", "Existence of AI tracking and skills-first programs; potential partner", "Medium-High (per AS)", "unverified", "Index/partner entry")
s("LM-044", "OPM Launches New Workforce Data Site", "U.S. Office of Personnel Management", "2026-01", "https://www.opm.gov/news/news-releases/opm-launches-new-workforce-data-site/",
  "government", X + " (FH-010)", "Federal Workforce Data (FWD) replaces FedScope; monthly updates", "High (per FH)", "unverified", "Source for headcount/entry-level signals")
s("LM-045", "O*NET What's New (release notes 2025-2026)", "National Center for O*NET Development", "2026-10", "https://onetcenter.org/whatsnew.html",
  "government", X + " (AS-004)", "O*NET 30.x-31.0 releases and formats; crosswalk must track O*NET versions", "High (per AS)", "unverified", "Crosswalk versioning")
s("LM-046", "Occupational, industry, and geographic exposure to artificial intelligence: A novel dataset and its potential uses (SMJ 42(12):2195-2217)",
  "Felten, Raj, Seamans", "2021", "https://onlinelibrary.wiley.com/doi/full/10.1002/smj.3286", "peer-reviewed", "not re-read (method known; data read via LM-010)",
  "AIOE method description", "High; peer-reviewed", "current", "Primary paper behind LM-010")
s("LM-047", "Working with AI: Measuring the Applicability of Generative AI to Occupations (arXiv:2507.07935; NeurIPS 2026)", "Tomlinson, Jaffe, Wang, Counts, Suri",
  "2025-07 (rev. 2026)", "https://arxiv.org/abs/2507.07935", "peer-reviewed", "not re-read (README of LM-009 read)", "Method of LM-009", "High; peer-reviewed venue", "current", "Primary paper behind LM-009")

# --- known, not accessed this session (unverified)
def u(id_, title, pub, date, typ, used, q, why, st="unverified", url=""):
    s(id_, title, pub, date, url, typ, NA, used, q, st, why)
u("LM-048", "GPTs are GPTs: Labor market impact potential of LLMs (Science)", "Eloundou, Manning, Mishkin, Rock", "2024", "peer-reviewed",
  "Rubric definitions (E1 = LLM alone can cut task time by at least half at equal quality; E2 = with complementary software)", "High; peer-reviewed", "Paper for LM-008 data", st="current")
u("LM-049", "The Impact of Artificial Intelligence on the Labor Market (patent-based exposure)", "Webb", "2020 (working paper)", "grey-literature",
  "AI, software and robot exposure from patent-task text overlap", "Medium-High; influential working paper; pre-LLM", "Separate robot exposure measure relevant to Ro vector")
u("LM-050", "Generative AI and Jobs: A Refined Global Index of Occupational Exposure", "ILO (Gmyrek et al.)", "2025", "government",
  "ISCO-08 task-level genAI exposure gradients with expert validation", "Medium-High; international organization", "International comparator for ESCO/ISCO adopters")
u("LM-051", "Large Language Models, Small Labor Market Effects", "Humlum and Vestergaard", "2025", "grey-literature",
  "Danish register-survey evidence: widespread chatbot adoption, small time savings, no detectable earnings/hours effects", "High; strong design (per author knowledge)", "Benchmark for Ac -> staffing inference")
u("LM-052", "Evaluating the Impact of AI on the Labor Market: Current State of Affairs (and updates)", "The Budget Lab at Yale", "2025-10 onward", "grey-literature",
  "Occupational-mix dissimilarity vs earlier technology waves; no broad disruption detected through 2025", "Medium-High", "Macro null benchmark")
u("LM-053", "Employment Projections 2024-34 and Monthly Labor Review AI occupational case studies", "U.S. Bureau of Labor Statistics", "2025", "government",
  "Current official 10-year projections incl. judgmental AI adjustments for selected occupations", "High", "Current projection cycle; replaces LM-011 values in Phase 3")
u("LM-054", "Future of Jobs Report 2025", "World Economic Forum", "2025-01", "industry-report", "Employer expectations 2025-2030 on job and skill churn, green and AI skills",
  "Medium; employer survey, large firms", "Named reference point; appraised as context only")
u("LM-055", "Global Green Skills Report (2023/2024 editions)", "LinkedIn Economic Graph", "2023-2024", "industry-report", "Green skills taxonomy, green talent share and hiring rates from member profiles",
  "Medium; platform-biased", "Named reference point")
u("LM-056", "Lightcast job-postings data, Open Skills taxonomy, green-skills and AI-skills reports", "Lightcast", "continuous (taxonomy ~4-weekly)", "industry-report",
  "Posting-based skill demand; green and AI skill mentions", "Medium; proprietary extraction", "Named reference point; posting-signal source")
u("LM-057", "OECD Employment Outlook and OECD AI-and-work programme (incl. public-sector AI workforce work)", "OECD", "2023-2026", "government",
  "International exposure, adoption and skills-demand evidence", "Medium-High", "Named reference point")
u("LM-058", "AI Index Report 2026", "Stanford HAI", "2026-04", "index", "Compendium of AI labor indicators (postings, talent)", "Medium-High; aggregator", "Named reference point")
u("LM-059", "AI at Work (GenAI capability rating of skills in postings) and AI-mention trackers", "Indeed Hiring Lab", "2025-09", "industry-report",
  "Share of posting skills with GenAI transformation potential; AI mentions in postings", "Medium", "Posting-side exposure measure")
u("LM-060", "Global AI Jobs Barometer", "PwC", "2025-06 (2026 edition not verified)", "industry-report", "Job-ad analysis linking AIOE exposure to wages and productivity",
  "Low-Medium; correlational vendor study", "Named in brief")
u("LM-061", "Agents, robots, and us: Skill partnerships in the age of AI", "McKinsey Global Institute", "2025-11", "industry-report",
  "Technical automation potential of work activities; skill partnership scenarios", "Low-Medium; proprietary method", "Named in brief")
u("LM-062", "O*NET Green Economy program (green increased demand / enhanced skills / new and emerging occupations; green task statements)", "National Center for O*NET Development",
  "2009 onward", "government", "Green occupation flags and green task statements", "Medium; designations not refreshed systematically", "Green-jobs measure", st="outdated")
u("LM-063", "U.S. Energy and Employment Report (USEER)", "U.S. Department of Energy", "annual to 2024; 2025 status not verified", "government",
  "Energy and energy-efficiency employment by technology", "Medium-High", "Green-jobs measure for energy subsector (DB lane)")
u("LM-064", "World Energy Employment", "International Energy Agency", "2025", "government", "Global energy employment and skills shortages", "Medium-High", "Green-jobs measure")
u("LM-065", "Renewable Energy and Jobs: Annual Review", "IRENA", "2025", "government", "Global renewable energy jobs estimates", "Medium", "Green-jobs measure")
u("LM-066", "Clean Jobs America / clean-economy project tracker", "E2 (Environmental Entrepreneurs)", "2026", "industry-report", "Clean-energy job counts and project cancellations", "Low-Medium; advocacy-commissioned", "Green-jobs measure")
u("LM-067", "Project Iceberg / Iceberg Index", "MIT and Oak Ridge National Laboratory", "2025-11", "grey-literature", "Skills-capability overlap simulation of technical exposure (known only via LM-023)",
  "Low-Medium; simulation, not read", "Newer index named in v1 research")
u("LM-068", "GDPval: Evaluating AI model performance on real-world economically valuable tasks", "OpenAI", "2025-09", "grey-literature",
  "Expert-graded model-vs-professional deliverables across 44 occupations", "Medium-High; strong design, narrow occupations", "Capability-evidence template for environmental tasks")
u("LM-069", "Future of Work with AI Agents (WORKBank; Human Agency Scale)", "Shao et al. (Stanford)", "2025", "grey-literature",
  "Worker desire vs expert-rated capability for 844 tasks; Human Agency Scale H1-H5", "Medium", "Closest published analogue to v1 A/Ac/V/H")
u("LM-070", "What work can robots do? (robot task-capability index; AEI robot_exposure data)", "Anthropic", "2026-09-30", "industry-report",
  "Title, date and one-line description seen on LM-003; content not read", "Unknown; not read", "First task-level robotics exposure index; comparator for v1 Ro/Cv",
  url="")
u("LM-071", "Anthropic Economic Index reports: Sep 2025 (geography/enterprise), Jan 2026 (economic primitives), Mar 2026 (learning curves), Apr 2026 (survey)",
  "Anthropic", "2025-09-15 to 2026-04-22", "industry-report", "Statistics reported via LM-004 only (directive share 27%->39%->32% on Claude.ai; API 77% then 64% directive; success rates; primitives)",
  "Medium; primary not re-read", "Release-level context for AEI appraisal")
u("LM-072", "Business Trends and Outlook Survey (AI use supplement)", "U.S. Census Bureau", "biweekly since 2023", "government", "Firm-level AI use rates by sector", "High; official survey",
  "Adoption base rates (private sector only)")
u("LM-073", "Automation and jobs: when technology boosts employment (Economic Policy)", "Bessen", "2019", "peer-reviewed",
  "Demand elasticity determines whether task-time compression reduces or raises employment", "High", "Theory for splitting Ac into time compression vs staffing outcome")
u("LM-074", "Automation and New Tasks: How Technology Displaces and Reinstates Labor (JEP)", "Acemoglu and Restrepo", "2019", "peer-reviewed",
  "Displacement vs reinstatement (new tasks) framework", "High", "Theory for 'new work' measurement")
u("LM-075", "New Frontiers: The Origins and Content of New Work, 1940-2018 (QJE)", "Autor, Chin, Salomons, Seegmiller", "2024", "peer-reviewed",
  "Measures new work via new occupation/title entries in Census Index of Occupations and links to patents", "High", "Method template for detecting new environmental work")
u("LM-076", "USAJOBS Search and Historic JOA APIs", "U.S. Office of Personnel Management (USAJOBS)", "continuous", "dataset",
  "Federal job opportunity announcements by series, grade, location, duties text", "High; primary postings; volume now constrained by hiring policy", "Federal posting signal source")

with open(os.path.join(OUT, "sources.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["source_id","title","author_or_publisher","date_published","url","source_type","accessed","used_for","quality","status","why_chosen"])
    w.writeheader(); w.writerows(S)
print("sources", len(S))
