#!/usr/bin/env python3
"""Build index_appraisal.csv and ecosystem.csv for LM (EMST v2 Phase 2). Content is LM analyst appraisal; see report.md section 2."""
import csv, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

IX_COLS = ["index_id","name","owner","latest_version_date","unit_of_analysis","method_summary","data_basis","env_occupation_coverage",
           "strengths","weaknesses","critiques_source_ids","use_in_emst","quality"]
IX = []
def ix(*v): IX.append(dict(zip(IX_COLS, v)))

ix("IX-01","Anthropic Economic Index (AEI) - usage releases","Anthropic Economic Research",
   "2026-06-26 (Cadences; release_2026_06_26); earlier 2025-02-10, 2025-03-27, 2025-09-15, 2026-01-15, 2026-03-24",
   "O*NET task statement x conversation; collaboration mode; occupation, state, country aggregates",
   "Privacy-preserving classification (Clio, run on Claude) of sampled conversations to O*NET tasks and collaboration modes (directive and feedback-loop = automation; task iteration, learning, validation = augmentation). From Jan 2026 adds 'economic primitives' (task complexity, human/AI skill in education-years, autonomy, success). From Jun 2026 monthly aggregates, artifact classifier and linked survey",
   "~1M Claude.ai conversations per one-week window (+1P API from Sep 2025; Cowork from 2026); CC-BY public data",
   "Env tasks present but tiny: Feb-2025 file rows for 19-2041(.01/.03), 19-1031, 19-2043, 19-2021, 13-1199.05, 11-9121.02 each 0.002%-0.02% of conversations; Farming/fishing/forestry ~0.1% of conversations; no rows seen for forestry, wildlife, fire, field-technician tasks in the partial view; government tenants not sampled",
   "Only open task-level measure of actual use with an automation/augmentation split; repeated releases support trends; native O*NET join",
   "Single vendor and self-selected consumer/developer users; usage is a lower bound on workplace use and blind to agencies that restrict consumer tools; classifier accuracy not published against a gold set; mode definitions and denominators shift across releases (augmentation 57% -> 52%; third-party reaggregation 78.7%); one-week windows",
   "LM-004|LM-013|LM-015",
   "INGEST as attributed external assessment (task penetration, directive share, success) keyed to release ID and O*NET version; treat absence or sub-threshold counts as 'insufficient usage evidence', never as 'unexposed'",
   "High for what it measures; Medium as proxy for environmental workplace adoption")
ix("IX-02","AEI observed exposure (Labor market impacts of AI: a new measure and early evidence)","Anthropic (Massenkoff and McCrory)","2026-03-05 (labor_market_impacts data folder)",
   "Occupation and task (task penetration for ~18k tasks; exposure for ~756 occupations per LM-015)",
   "Combines theoretical feasibility (Eloundou-style ratings) with observed work-related Claude usage, weighting automated/API use more; tests unemployment and young-worker employment by exposure using US survey data and BLS 2024-34 projections",
   "AEI usage + Eloundou ratings + O*NET + US survey data",
   "Covers all O*NET occupations; field occupations near zero observed exposure; 30% of workers zero observed exposure (secondary report)",
   "Moves from 'could' to 'is used'; explicit automation weighting; open data",
   "Primary page not read (fetch blocked); critics note projection-based tests, short window, Claude-only usage, conflict of interest",
   "LM-012|LM-013","INGEST task penetration as attributed assessment; occupation observed exposure as context; read primary in Phase 3",
   "Medium (not fully read)")
ix("IX-03","GPTs are GPTs (theoretical LLM exposure)","Eloundou, Manning, Mishkin, Rock (OpenAI / Science 2024)","2024 (ratings made 2023)",
   "O*NET 27.x task statement (19,265) and O*NET-SOC occupation",
   "Human annotators and GPT-4 apply a rubric: E0 no exposure; E1 LLM alone can cut task time by at least half at equal quality; E2 needs complementary software; occupation alpha/beta/gamma. Separate GPT-4 automation rubric T0-T4",
   "O*NET task statements; open labels",
   "All env O*NET-SOC codes: Environmental Scientists 98th pct (human beta 0.71), Climate Change Policy Analysts 99th, Sustainability Specialists 97th, Planners 90th; Foresters 59th; Forest & Conservation Workers 17th; Firefighters 22nd",
   "Transparent rubric; task-level; human and model raters; open data; E1 is an operational definition of task-time compression",
   "Capability feasibility not adoption; 2023 vintage (pre-agent); raters not occupation SMEs; label instability (in LM pilot, 13 of 21 tasks with two plausible O*NET matches got different human labels); LLM-cognitive only - blind to robotics and sensing",
   "LM-015|LM-025",
   "INGEST as attributed 'theoretical LLM exposure' via EMST-task -> O*NET-task crosswalk; aggregate over top-k matches and report spread",
   "High (method), Medium (currency)")
ix("IX-04","AI Occupational Exposure (AIOE) and Language-Modeling AIOE","Felten, Raj, Seamans","2021 (SMJ); LM-AIOE 2023",
   "Occupation (6-digit SOC 2010 codes for some occupations)",
   "Links 10 AI application categories to 52 O*NET abilities via an mTurk relatedness survey; occupation score = ability prevalence x importance weighted; LM-AIOE re-weights for language modelling",
   "O*NET abilities; EFF AI progress categories; mTurk survey",
   "774 SOC codes; env technicians indexed under SOC 2010 (19-4091, 19-4093, 29-9011) so naive 2018 joins drop them; Natural Sciences Managers 90th pct; Forest & Conservation Technicians 33rd",
   "Stable, widely cited, simple; correlates 0.86-0.98 with other indices",
   "Ability-level: cannot see within-occupation task variation; no automation/augmentation distinction; lay raters; SOC vintage issues",
   "LM-046","CONTEXT only (occupation benchmark); do not attach to EMST tasks","Medium")
ix("IX-05","Webb patent-based exposure (AI, software, robots)","Michael Webb","2020",
   "Occupation (from O*NET task verb-object pairs)","Measures overlap between patent text and occupation task descriptions for AI, software and robot patents",
   "Google patents; O*NET tasks","All SOC; the robot measure is one of few covering physical field tasks",
   "Separates AI, software and robots; technology-side signal","Pre-LLM; patents are not deployment; crude verb-noun matching",
   "","CONTEXT; robot exposure as comparator for v1 Ro/Cv until a task-level robotics index is validated","Medium (not re-read)")
ix("IX-06","ILO generative-AI occupational exposure (2023; refined global index 2025)","International Labour Organization (Gmyrek et al.)","2025 (refined index; verify)",
   "ISCO-08 4-digit occupation and its tasks","LLM-scored task exposure with expert validation; gradients of exposure by occupation; global employment weights",
   "ISCO-08 task descriptions; labour force surveys","ISCO groups for environmental protection professionals, forestry technicians and workers; coarse",
   "International and ISCO/ESCO-compatible; gradient categories","Coarse ISCO tasks; model-scored; exposure not impact","",
   "CONTEXT and crosswalk for ESCO/international adopters","Medium-High (not re-read)")
ix("IX-07","Working with AI (AI applicability scores)","Microsoft Research (Tomlinson et al.)","2026 (data v1.1; NeurIPS 2026)",
   "O*NET intermediate work activity (332 IWAs) aggregated to SOC (785); O*NET task physical flag",
   "Maps 200k Bing Copilot conversations to IWAs as user goals and AI actions; completion, impact scope and feedback; applicability = coverage x completion x scope; v1.1 adds nonphysical score",
   "Bing Copilot conversations (2024); O*NET",
   "Water/wastewater operators 0.6th pct, Forest & Conservation Technicians 6th, Foresters 20th, Environmental Scientists 61st, Planners 94th; usage-based score ranks 20 of 24 env occupations below their Eloundou percentile",
   "Usage-based; separates assisting (user goal) from performing (AI action); open data; task physical flag",
   "Single platform and period; IWA level is coarse; applicability is not impact (authors caution)",
   "","INGEST IWA metrics as attributed context on EMST tasks via O*NET task->DWA->IWA; INGEST physical flag as task attribute","High")
ix("IX-08","Canaries in the Coal Mine? (payroll outcomes by age x exposure)","Brynjolfsson, Chandar, Chen (Stanford DEL)","2026-08-12 (update; paper rev. 2025-11-13)",
   "Worker-month employment by age band x occupation exposure quintile",
   "ADP payroll microdata; event-study style comparisons with firm-time fixed effects; exposure from Eloundou et al. and usage-based automation/augmentation splits",
   "ADP payroll records (millions of workers, tens of thousands of firms)",
   "No environmental breakdown; public administration is where ADP and national surveys diverge most; government payroll largely outside ADP",
   "High-frequency administrative data; age detail; robustness to interest rates, tech exclusion, alternative measures",
   "Descriptive not causal; pre-trends; gaps shrink with education controls; ADP sample composition; cannot speak to public agencies",
   "LM-006|LM-016","BENCHMARK for entry-level (CLD) hypotheses; replicate design on OPM FWD for federal env series","High")
ix("IX-09","Yale Budget Lab labor-market AI tracker","The Budget Lab at Yale","2025-10 onward (verify latest)","Occupational mix (CPS)",
   "Dissimilarity index of occupational mix over time compared with earlier technology waves; exposure groups",
   "Current Population Survey","Env occupations too small in CPS for reliable cells","Simple, transparent, macro null benchmark","Coarse; cannot detect task-level change",
   "","BENCHMARK (macro context)","Medium-High (not re-read)")
ix("IX-10","Large Language Models, Small Labor Market Effects","Humlum and Vestergaard","2025",
   "Worker (11 exposed occupations), employer","Linked Danish administrative registers with surveys on chatbot adoption, employer encouragement and time savings; difference-in-differences on earnings and hours",
   "Danish registers + surveys of ~25k workers","None environmental","Strong design linking adoption to outcomes; separates time saved from earnings/hours",
   "2023-24 tools; Denmark; 11 occupations","","BENCHMARK for the Ac -> staffing inference (time savings need not change headcount)","High (not re-read)")
ix("IX-11","Future of Jobs Report","World Economic Forum","2025-01 (biennial; next expected ~2027)","Employer expectations by job family and skill",
   "Survey of large employers on expected job creation/displacement and skill change to 2030","Employer survey across economies",
   "Green transition and environmental-stewardship skills discussed at aggregate level; no US public-sector or field coverage",
   "Wide coverage; tracks employer intent","Self-report by large firms; expectations not outcomes; opaque aggregation",
   "LM-015","CONTEXT only; never as an EMST task assessment","Medium")
ix("IX-12","LinkedIn Economic Graph green-skills research (Global Green Skills Report; Climate Talent)","LinkedIn","2024 (latest seen by team; 2025-26 editions not verified)",
   "Member profile skills and job postings; green skills taxonomy","Classifies member skills/postings as green; green talent share; hiring-rate comparisons","LinkedIn member and posting data",
   "Biased to white-collar, private and profile-curating workers; field, seasonal, Tribal and many public workers under-represented",
   "Large panel; career-transition data (useful to CM)","Platform selection; inferred skills; taxonomy not open","",
   "CONTEXT; possible crosswalk of green-skill labels; partner for transition data","Medium")
ix("IX-13","Lightcast postings, Open Skills taxonomy and green/AI-skills reports","Lightcast","continuous (taxonomy ~4-weekly)","Job posting x extracted skill",
   "Web-scraped, deduplicated postings; NLP skill extraction to Open Skills taxonomy; green and AI skill flags","Postings from employer sites and job boards incl. state systems",
   "Good coverage of state/local and private env postings; federal via USAJOBS; seasonal crews weaker","Granular, timely, used by states and workforce boards",
   "Proprietary postings and extraction; postings are not hires; vendor lock-in risk","",
   "INGEST posting-skill signals where licence allows (via state partners); crosswalk EMST to Open Skills IDs","Medium")
ix("IX-14","BLS Employment Projections (with AI occupational case studies)","U.S. Bureau of Labor Statistics","2024-34 cycle (released 2025); 2025-35 expected ~Sep 2026 (verify)",
   "Occupation (National Employment Matrix)","Structural 10-year projections by industry-occupation matrix; recent cycles include judgmental AI adjustments for selected occupations",
   "OEWS, CPS, industry models","All env SOC; 2022-32 vintage read: Environmental Scientists +6.1%, Conservation Scientists +4.1%, Foresters +2.4%, Forest & Conservation Workers -8.7%, Water/Wastewater Operators -6.3%, OHS Specialists +13.3%",
   "Official, consistent, occupation-complete","Assumes full employment; slow to policy shocks (2025 federal cuts); AI adjustments few and judgmental",
   "LM-013","CONTEXT/baseline per occupation; refresh each cycle","High (method); values here superseded")
ix("IX-15","OECD Employment Outlook and AI-and-work programme","OECD","2023-2026 (verify)","Country, sector, occupation",
   "Employer/worker surveys, exposure indices, posting analyses, public-sector AI workforce reviews","Multiple","No environment-specific cut seen",
   "International comparison; public-sector capability work","Heterogeneous methods","","CONTEXT","Medium-High (not re-read)")
ix("IX-16","AI Index Report","Stanford HAI","2026-04","Indicator compendium","Aggregates third-party indicators incl. AI job postings and talent","Lightcast, LinkedIn and others",
   "Indirect","Convenient compendium","Secondary; inherits source biases","","WATCH","Medium-High (not re-read)")
ix("IX-17","AI at Work / AI-mention tracking","Indeed Hiring Lab","2025-09 (verify later)","Posting skill",
   "Rates GenAI capability against skills listed in postings; tracks AI mentions in postings","Indeed postings","Env postings included; no env cut seen",
   "Posting-side, frequent","Model-rated capability; postings not hires","","CONTEXT; AI-mention share in env postings is a candidate signal","Medium (not re-read)")
ix("IX-18","Burning Glass Institute research (entry-level, AI tracking, skills-first)","Burning Glass Institute","2026-10 (latest item per AS)","Postings and career histories",
   "Posting requirements and resume trajectories; entry-level requirement inflation","Postings and profiles","No env cut seen","Career-path data rare elsewhere","Proprietary data","",
   "BENCHMARK and potential partner for entry-path signals","Medium-High (per AS)")
ix("IX-19","Global AI Jobs Barometer","PwC","2025-06 (2026 edition not verified)","Job ads by occupation and industry","Links AIOE exposure to wage premia and productivity growth","~1bn job ads",
   "No env cut seen","Scale","Correlational; vendor; reuses AIOE","","CONTEXT only","Low-Medium")
ix("IX-20","Agents, robots, and us","McKinsey Global Institute","2025-11","Work activity (DWA-like)","Expert-judged technical automation potential of activities and adoption scenarios","Proprietary",
   "Not environment-specific","Activity-level framing; robots and agents together","Opaque capability judgments; technical potential misread as job loss","","CONTEXT only","Low-Medium")
ix("IX-21","Project Iceberg / Iceberg Index","MIT and Oak Ridge National Laboratory","2025-11","Worker-skill x tool capability (simulation)","Agent-based skills-capability overlap simulation",
   "Simulated workforce","No env-specific analysis found (per v1 research)","Skills-level","Simulation, not observation; not read","LM-023","WATCH","Low-Medium (not read)")
ix("IX-22","GDPval","OpenAI","2025-09","Expert-built task deliverable","Blind expert grading of model vs professional deliverables for 44 occupations",
   "Expert task set","No environmental occupations (per LM recollection; verify)","Direct capability evidence on realistic work products","Narrow occupation set; vendor-run",
   "","BENCHMARK METHOD: build environmental task evals (cf. DraftNEPABench, DC-032) to evidence S/Ac claims","Medium-High (not re-read)")
ix("IX-23","WORKBank / Human Agency Scale","Shao et al. (Stanford)","2025","Task x occupation","Worker survey of desire for automation vs expert-assessed capability; H1-H5 human agency scale",
   "~1,500 workers, 844 tasks, 104 occupations","Limited env coverage (verify)","Adds the worker-preference dimension; closest analogue to v1 A/Ac/V/H","Survey sample; capability ratings by experts",
   "","CROSSWALK v1 automation types to HAS levels; use as rater codebook reference","Medium (not re-read)")
ix("IX-24","What work can robots do? (AEI robot_exposure)","Anthropic","2026-09-30","Job task","Index of how well current robots can perform US job tasks (description only)",
   "Not read","Potentially covers field tasks (planting, equipment operation, sampling)","First task-level robotics index tied to AEI data","Unread; method unknown","",
   "INGEST candidate for Ro/Cv vector after review","Unknown")
ix("IX-25","O*NET Green Economy designations and green task statements","National Center for O*NET Development","2009 onward (not systematically refreshed)","O*NET-SOC occupation; task",
   "Expert classification of occupations as green increased demand, enhanced skills, or new and emerging; green task statements","O*NET","Defines e.g. Climate Change Policy Analysts, Industrial Ecologists, Environmental Restoration Planners",
   "Official, task-level green statements","Aging; designations not tied to current demand","","CROSSWALK (green flags as attributes)","Medium")
ix("IX-26","U.S. Energy and Employment Report (USEER)","U.S. Department of Energy","annual to 2024; 2025 status not verified","Energy employer establishment",
   "Employer survey of energy and energy-efficiency jobs by technology","~30k+ employer survey","Energy subsector; not natural resources","Large employer survey","Continuity uncertain","",
   "CONTEXT for energy module (DB lane)","Medium-High (not re-read)")
ix("IX-27","World Energy Employment","International Energy Agency","2025 (verify)","Country x technology","Modelled energy employment and skills shortages","IEA modelling","Energy only","Global consistency","Modelled",
   "","CONTEXT","Medium-High (not re-read)")
ix("IX-28","Renewable Energy and Jobs: Annual Review","IRENA","2025 (verify)","Country x technology","Compiled and modelled renewable employment","Mixed","Energy only","Global","Mixed methods","",
   "CONTEXT","Medium (not re-read)")
ix("IX-29","Clean Jobs America / clean economy tracker","E2","2026 (verify)","State x clean-energy sector; project announcements","BW Research employer survey; project cancellation tracking","Survey + announcements",
   "Energy and efficiency","Timely policy-shock tracking","Advocacy-commissioned","","CONTEXT","Low-Medium (not re-read)")
ix("IX-30","Business Trends and Outlook Survey - AI use","U.S. Census Bureau","biweekly (verify latest)","Firm","Share of firms using AI by sector","Firm survey","Private sector only; no government",
   "Official adoption base rate","Firm-level binary; excludes agencies","","CONTEXT (private adoption base rates)","High (not re-read)")
ix("IX-31","Federal Agency AI Use Case Inventory","OMB Office of the Federal CIO","2026-04-13 (2025 inventory)","Agency AI use case; COTS product use",
   "Agency self-reported use cases with development stage, classification, high-impact flags; consolidated COTS tool use with license bands","Agency submissions",
   "LM count: 504 use cases in env bureaus; 61 of 347 stage-reported deployed; 5 NEPA/permitting cases, none deployed; genAI drafting/summarizing COTS at EPA 10,000-50,000 users and DOI/USDA 50,000+ for some tools",
   "Primary, dated deployment-stage evidence for public agencies","Self-report; uneven completeness (NOAA stage blank); COTS rows lack function detail",
   "","INGEST as adoption-stage evidence per function x agency; gate S/V/Horizon-1 claims on it","High")
ix("IX-32","Federal Workforce Data (FWD)","U.S. Office of Personnel Management","2026-01 launch; monthly","Employee record aggregates (agency x series x grade x age)",
   "Administrative personnel data replacing FedScope","OPM EHRI","All federal env series (0401, 0408, 0454, 0455, 0460, 0462, 0486, 0819, 1301, 0456 etc.)",
   "Authoritative, monthly, series-level","Federal only; series not tasks","","INGEST headcount, accessions/separations, under-30 share, trainee series as change signals","High (per FH)")
ix("IX-33","OpenLMP machine-readable land management plans","OpenLMP project","2026-10-21 (v0.1.0)","Plan component (desired condition, standard, monitoring, coordination)",
   "PDF extraction with provenance, controlled vocabularies, enrichment","217 plans, 58,544 components (95% USFS; western states)",
   "Demand for monitoring, standards and coordination in public-lands work","Provenance on every record; requirements written into law-like documents",
   "USFS-dominated; extraction segmentation varies; themes tagged on ~10% of components","","INGEST requirement counts by theme and method as demand signals; map to EMST tasks","High (provenance), Medium (representativeness)")
ix("IX-34","USAJOBS job opportunity announcements (Search and Historic JOA APIs)","OPM / USAJOBS","continuous","Job announcement",
   "Announcement metadata and duties/qualification text","Federal postings","All federal env series","Primary; duties text enables NLP; long history",
   "Since 2025 volume reflects hiring freeze, EO 14356 staffing plans and Merit Hiring Plan more than labour demand","LM-038",
   "INGEST duties/qualification text changes (content signal); treat volume as policy signal","High (data), Medium (as demand signal)")

with open(os.path.join(OUT, "index_appraisal.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=IX_COLS); w.writeheader(); w.writerows(IX)

EC_COLS = ["entity_id","name","entity_type","owner_or_host","sector_focus","what_it_illuminates","latest_release_or_status","how_emst_connects","integration_detail","url","evidence_label","source_ids","proposed_by"]
EC = []
def ec(*v): EC.append(dict(zip(EC_COLS, v + ("LM",))))
ec("ECO-LM-01","Anthropic Economic Index (dataset and reports)","index","Anthropic","economy-wide","Task-level AI usage, automation vs augmentation, economic primitives, geography","release_2026_06_26; labor_market_impacts; robot_exposure","ingest|benchmark|watch",
   "Map EMST tasks to O*NET task IDs; join AEI task penetration, directive share and success per release; store as dated external_index assessments","https://huggingface.co/datasets/Anthropic/EconomicIndex","E","LM-001|LM-003")
ec("ECO-LM-02","AEI observed exposure (labor_market_impacts)","index","Anthropic","economy-wide","Usage-weighted exposure by occupation; task penetration","2026-03-05","ingest|benchmark","Join occupation observed exposure to EMST role profiles via O*NET-SOC; task penetration to tasks","https://www.anthropic.com/research/labor-market-impacts","J","LM-026|LM-012")
ec("ECO-LM-03","Anthropic robot task-capability index (What work can robots do?)","index","Anthropic","economy-wide","Robot capability on job tasks","2026-09-30","ingest|watch","Candidate calibration for Ro/Cv vector on field tasks after method review","","S","LM-003|LM-070")
ec("ECO-LM-04","Anthropic Economic Futures program","fund","Anthropic","economy-wide","Grants and symposia on AI economic impacts","launched 2025-06 (per LM-004)","funder|partner","Possible funding for environmental-sector exposure research and AEI-EMST crosswalk","","J","LM-004")
ec("ECO-LM-05","GPTs-are-GPTs exposure labels","dataset","OpenAI (Eloundou et al.)","economy-wide","Theoretical LLM task exposure E0/E1/E2; automation rubric","2024","ingest|crosswalk","Attach human and GPT-4 labels to EMST tasks through curated O*NET matches; aggregate top-k","https://github.com/openai/GPTs-are-GPTs","E","LM-008")
ec("ECO-LM-06","Microsoft Working with AI results files","dataset","Microsoft Research","economy-wide","Usage-based applicability by IWA and SOC; physical task flags","v1.1 (2026)","ingest|benchmark","Join IWA metrics via O*NET task->DWA->IWA; physical flag as task attribute","https://github.com/microsoft/working-with-ai","E","LM-009")
ec("ECO-LM-07","AIOE datasets","dataset","Felten, Raj, Seamans","economy-wide","Ability-based occupation AI exposure","2021/2023","benchmark","Occupation-level comparator only; handle SOC 2010 codes","https://github.com/AIOE-Data/AIOE","E","LM-010")
ec("ECO-LM-08","Stanford Digital Economy Lab canaries indicators","research-program","Stanford Digital Economy Lab","economy-wide","Young-worker employment by AI exposure (ADP)","2026-08-12 update; dashboard","benchmark|partner|watch","Replicate age x exposure design on OPM FWD for environmental series; request env-occupation cut","https://digitaleconomy.stanford.edu/news/canariesaug26/","E","LM-005|LM-006")
ec("ECO-LM-09","The Budget Lab at Yale AI labor tracker","research-program","Yale University","economy-wide","Occupational mix change vs past tech waves","2025-10 onward","benchmark|watch","Use method on env SOC set with OEWS","","J","LM-052")
ec("ECO-LM-10","Humlum and Vestergaard LLM adoption study","paper","University of Chicago / Copenhagen (authors)","economy-wide","Adoption, time savings and earnings effects","2025","benchmark","Evidence that time savings (Ac) need not translate to headcount","","J","LM-051")
ec("ECO-LM-11","ILO generative AI exposure index","index","International Labour Organization","global","ISCO task exposure gradients","2025 refined index","crosswalk|benchmark","ISCO-08 bridge for ESCO and international adopters","","J","LM-050")
ec("ECO-LM-12","Webb exposure measures","index","Michael Webb","economy-wide","AI, software and robot patent exposure","2020","benchmark","Robot exposure comparator for field tasks","","J","LM-049")
ec("ECO-LM-13","WEF Future of Jobs Report","index","World Economic Forum","global","Employer expectations on jobs and skills","2025-01","watch","Context only","https://esgnews.com/?p=33096","J","LM-041|LM-054")
ec("ECO-LM-14","LinkedIn Economic Graph green skills","research-program","LinkedIn","global","Green skills and talent flows","2024 (latest seen)","watch|partner","Possible transition data for CM; crosswalk green-skill labels","","J","LM-042|LM-055")
ec("ECO-LM-15","Lightcast postings and Open Skills","platform","Lightcast","economy-wide","Posting skill demand","continuous","ingest|crosswalk","Map EMST tasks/competencies to Open Skills IDs; ingest env posting skill counts via state partners","","J","LM-056")
ec("ECO-LM-16","BLS Employment Projections and OEWS","dataset","U.S. Bureau of Labor Statistics","economy-wide","Occupation employment, wages, projections","EP 2024-34 (2025)","ingest|benchmark","Occupation baseline trend per role profile; refresh each cycle","","E","LM-011|LM-053")
ec("ECO-LM-17","OECD AI and work programme","research-program","OECD","global","International adoption and skills evidence","ongoing","watch","Context; public-sector AI workforce comparators","","J","LM-057")
ec("ECO-LM-18","Stanford AI Index","index","Stanford HAI","global","AI indicators compendium","2026-04","watch","Context","","J","LM-058")
ec("ECO-LM-19","Indeed Hiring Lab AI at Work","research-program","Indeed","economy-wide","GenAI capability vs posting skills; AI mentions","2025-09","watch|ingest","AI-mention share in env postings as signal","","J","LM-059")
ec("ECO-LM-20","Burning Glass Institute","organization","Burning Glass Institute","economy-wide","Entry-level requirements, career paths, AI tracking","2026","partner|benchmark","Entry-path signals; skills-first validation (see AS)","https://www.burningglassinstitute.org/","J","LM-043")
ec("ECO-LM-21","PwC Global AI Jobs Barometer","index","PwC","economy-wide","Job-ad AI exposure vs wages","2025-06","watch","Context only","","J","LM-060")
ec("ECO-LM-22","McKinsey Global Institute work automation research","research-program","McKinsey","economy-wide","Technical automation potential of activities","2025-11","watch","Context only","","J","LM-061")
ec("ECO-LM-23","Project Iceberg","index","MIT / Oak Ridge National Laboratory","economy-wide","Skills-capability overlap simulation","2025-11","watch","Context only","","S","LM-067")
ec("ECO-LM-24","GDPval","tool","OpenAI","economy-wide","Expert-graded AI performance on occupational deliverables","2025-09","benchmark","Template for an environmental-task evaluation suite (with DC; cf. DraftNEPABench)","","J","LM-068")
ec("ECO-LM-25","WORKBank / Human Agency Scale","dataset","Stanford","economy-wide","Worker preference vs capability for task automation","2025","crosswalk|benchmark","Map v1 A/Ac/V/H to HAS levels for rater codebook","","J","LM-069")
ec("ECO-LM-26","O*NET database and Green Economy designations","standard","National Center for O*NET Development","economy-wide","Tasks, DWAs, IWAs, green flags","30.x-31.0 (2025-26)","crosswalk|ingest","EMST task -> O*NET task/DWA crosswalk versioned per O*NET release","https://onetcenter.org/whatsnew.html","E","LM-045|LM-062")
ec("ECO-LM-27","Federal Agency AI Use Case Inventory","dataset","OMB OFCIO","federal","AI deployment stage by agency and function","2025 inventory (2026-04-13)","ingest|validator","Gate S/V and Horizon-1 claims on registered deployment; annual refresh","https://github.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory","E","LM-027")
ec("ECO-LM-28","OPM Federal Workforce Data (FWD)","dataset","OPM","federal","Headcount, accessions, separations by series/grade/age","monthly since 2026-01","ingest","Entry-level and series headcount change signals for role profiles","https://www.opm.gov/news/news-releases/opm-launches-new-workforce-data-site/","J","LM-044")
ec("ECO-LM-29","USAJOBS APIs","platform","OPM","federal","Federal announcements and duties text","continuous","ingest","Duties/qualification text diff by series as content signal (IA pipeline)","","J","LM-076")
ec("ECO-LM-30","OpenLMP","dataset","OpenLMP project","public lands","Plan requirements (monitoring, standards, coordination, data dependencies)","v0.1.0 (2026-10-21)","ingest|partner","Requirement counts by theme/method mapped to EMST tasks (lmp_demand_signals.py)","local: /home/claude/lmps","E","LM-017")
ec("ECO-LM-31","Partnership for Public Service Fed Figures","research-program","Partnership for Public Service","federal","Federal workforce composition change","2026","benchmark|partner","Context for public env workforce change; method for series-level analysis","https://ourpublicservice.org/?p=47956","J","LM-028")
ec("ECO-LM-32","Trellis State of the Sustainability Profession","index","Trellis","private (corporate sustainability)","Sustainability function headcount, priorities, pay","2026","benchmark","Private-sector signal for sustainability roles (PS lane)","https://trellis.net/article/state-of-the-sustainability-profession-2026/","J","LM-040")
ec("ECO-LM-33","USEER / IEA World Energy Employment / IRENA / E2","index","DOE; IEA; IRENA; E2","energy","Energy and clean-economy employment","2024-2026 (verify)","watch","Context for energy module (DB lane)","","J","LM-063|LM-064|LM-065|LM-066")
ec("ECO-LM-34","Census Business Trends and Outlook Survey (AI)","dataset","U.S. Census Bureau","private sector","Firm AI adoption rates","biweekly","benchmark","Private adoption base rates for PS role profiles","","J","LM-072")
ec("ECO-LM-35","Autor et al. new-work measurement","paper","Autor, Chin, Salomons, Seegmiller","economy-wide","How new work appears as new titles/tasks","2024","benchmark","Method for 'new' signals: new titles in postings/PDs vs taxonomy","","J","LM-075")

with open(os.path.join(OUT, "ecosystem.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=EC_COLS); w.writeheader(); w.writerows(EC)
print(len(IX), len(EC))
