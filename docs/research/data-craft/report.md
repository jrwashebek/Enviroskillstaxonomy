# Data Craft for EMST v2: definition, progression, durable vs tool-bound, and responsible AI as competency

**Role:** Data Craft Lead (DC) · **Date:** 2026-10-23 · **Phase:** 2 · **Status:** Research findings and proposals for the Chief Taxonomy Architect (CA)

Labels: **[E]** evidence (source IDs resolve to `sources.csv`), **[J]** expert judgment (basis stated), **[S]** speculation (what would confirm or refute it is stated).

---

## 0. Summary

**Definition (two sentences).** Data craft is the disciplined capacity to turn observations of environmental systems into *warranted* evidence, models and decision support: designing what gets measured, stewarding data so it stays fit for use and properly governed, analysing and modelling with honest uncertainty, and putting results in front of decision-makers in a form they can act on. Because more and more of that computation is now done by machines, data craft also includes specifying, validating, supervising and answering for AI-generated analysis, not only doing analysis oneself.

**What the evidence shows**

1. **Environmental AI in government is mostly classical machine learning on Earth-observation, hydrology, hazard and species data. It has been for years.** Generative AI is mostly at pilot stage, and agentic AI is almost entirely pre-deployment. USDA, DOI and EPA report 438 use cases in the 2025 federal inventory. Of these, 86 are deployed, and 59 of those 86 are classical ML. Eight deployed cases are generative AI. Only two deployed cases are agentic, and both are administrative. [E: DC-001]
2. **Where generative AI is deployed, it does text work in environmental review and planning.** Examples are Forest Service forest-plan review and "Turbo plan" (both deployed in 2025), FWS DocketScope for public comments (deployed and analyst-verified), and pilots at EPA, BLM and NOAA (comment summarization, NEPA categorical-exclusion drafting, biological opinions). The tools churn: DOI's comment-analysis tool PCAT was retired between the 2024 and 2025 inventories. [E: DC-001]
3. **The only high-impact AI in environmental agencies is ML that drives payments or enforcement, not the most novel AI.** The cases are USDA satellite-and-crop-model verification of farm-program reporting and EPA inspection risk scoring. Three other cases avoided the high-impact designation because a human is said to be the "principal basis" of the decision. Whether human review is substantive is therefore the hinge of federal AI compliance, and it is a data-craft skill. [E: DC-001, DC-007]
4. **The data stewardship behind AI is uneven.** In 2024, complete or widely available training and evaluation data documentation was reported for only 37% of USDA's 89 AI use cases. [E: DC-002]
5. **Plans demand durable analytical functions, not AI.** I read 58,544 land-management plan components. None mentions AI or machine learning. They do require monitoring (3,843 components) and long-lived authoritative data and analyses, including Recreation Opportunity Spectrum, natural range of variation, hydrologic modelling, Forest Inventory and Analysis (FIA) and SSURGO soils. [E: DC-035]
6. **Specific models, platforms and policy memos have half-lives of one to three years.** OlmoEarth released three model generations in about a year. Google moved its AlphaEarth embedding bucket to "provider pays" in July 2026. A Data Carpentry geospatial lesson was retired in 2026. OMB M-26-04 sunsets after two years. AI RMF 1.0 is under revision. [E: DC-025, DC-028, DC-031, DC-008, DC-004]
7. **v1 Domain 2 is organized by technology family.** Of its 35 competencies, I rate 9 as mostly durable, 16 as mixed and 10 as mainly tool fluency. My verdicts are carry 3, change 25 and retire 7. [J, applying the rule in §10.1 to DC-042]

**Top proposals.**
- **P-DC-01:** a warrant-based definition with five durable functions.
- **P-DC-02:** a five-part rule separating durable competencies (L1) from the tools layer (L4).
- **P-DC-03:** restructure Domain 2.
- **P-DC-04:** a tools layer with a review and deprecation policy (53 seed entries).
- **P-DC-05:** universal data and AI literacy (DC-CAND-01 and DC-CAND-02).
- **P-DC-06:** an assurance cluster (DC-CAND-13, -14, -15, -19, -20).
- **P-DC-07:** a stewardship cluster (DC-CAND-05, -06, -07).
- **P-DC-10:** levels defined by scope of accountability, assessed with seeded-error work samples.

---

## 1. Scope, method and limits of the evidence

**What I read.**
- **v1 material.** The v1 database (DC-042) and the normalized baseline (DC-048). The v1 craft criteria (DC-043) and Five Functional Positions (DC-044), both read from the on-disk export after the coordinator's notice. The Domain 7 tagging record (DC-045), the Domain 2 exposure working records (DC-046) and the fire-intelligence research report (DC-047).
- **Federal AI use-case inventories.** The 2025 and 2024 inventories (DC-001, DC-002). I cloned them from OMB's GitHub repositories and computed all counts myself rather than relying on press summaries.
- **Federal AI policy.** NIST AI RMF pages (DC-004, DC-005). OMB M-25-21 and M-25-22 via a law-firm summary (DC-007), M-26-04 in primary text (DC-008) and the OMB memo index (DC-009). The AI Action Plan via two law-firm summaries (DC-010, DC-011).
- **Workforce and literacy frameworks.** OPM's 2024 AI competency model and 2025 AI strategy in primary text (DC-012, DC-013). DOL TEN 07-25 (DC-015, DC-016). EU AI Act Article 4 status after the 2026 Omnibus (DC-017, DC-018). The EC/OECD AILit framework (DC-019).
- **Primary repositories for Earth-observation (EO) foundation models and environmental AI tools.** Prithvi-EO-2.0, Clay, OlmoEarth and TerraTorch (DC-023 to DC-026). Microsoft Planetary Computer (DC-027). The Google Earth Engine Satellite Embedding catalog entry (DC-028). MegaDetector, SpeciesNet, BirdNET and NIST Dioptra (DC-038 to DC-041).
- **Primary repositories for permitting technology.** PNNL PermitAI and DraftNEPABench (DC-032). The CEQ permitting data standard (DC-034).
- **Primary repositories for data stewardship and curricula.** GBIF's sensitive-data guidance (DC-029). Data Carpentry lessons (DC-030, DC-031).
- **The sister OpenLMP repository.** Its 58,544 plan components were analysed by me (DC-035). Also its governance and sensitive-data policy (DC-036), gold-set evaluation (DC-037) and verified permitting-technology research (DC-033).

**Limits I must state plainly.**
- **The team's shared web-search budget ran out early in my work.** After that, the fetch tool refused URLs that were not returned by an earlier search.
- **Several named primary sources could not be read this session.** These are the FAIR paper, the CARE principles, EPA's 2009 environmental-model guidance, the Evidence Act text, ISO/IEC 42001, NASA ESDT, Destination Earth, Digital Promise, ESIP and DataONE.
- **They are in `sources.csv` with status `unverified`.** Any claim resting on them is labelled [J], not [E].
- **Primary memo PDFs for M-25-21/22 and the AI Action Plan were not reachable.** I used detailed law-firm summaries and graded them Medium.
- **The Commerce/NOAA rows in the 2025 inventory carry use-case names only.** NOAA evidence is therefore limited to what the names say.
- **Evidence specific to state, local, Tribal and NGO data work is thin.** I found one state agency (Michigan DNR) and NGOs (TNC California) on the MegaDetector adopter list (DC-038), and little else. That thinness is a finding.

**Why these sources.** The charter asks what is *actually* changing. I therefore weighted self-reported deployment records (the inventories), what demand documents actually require (plans) and the primary documentation of the tools themselves (repositories). I gave less weight to vendor or press claims. Where I relied on secondary summaries, the reason is recorded in `sources.csv`.

---

## 2. Defining data craft for v2

### 2.1 What v1 said, and where it breaks

v1 defines Datacraft as "information management, analysis, modeling, and technology." Its irreducible value is "making patterns visible and projecting futures" (DC-043). Two features of that definition no longer hold. [J]

- **Pattern-making and projection are what machines now do cheaply.** Pre-trained detectors count animals (DC-038). Foundation-model embeddings separate land cover without hand-built features (DC-028). AI emulators produce forecast ensembles (DC-001). If data craft is defined by producing patterns, then the craft is what is being automated, and the definition predicts its own obsolescence.
- **"Technology" in the definition pulled tool fluency into the craft.** That is how v1 ended up with Domain 2 competencies for virtual meetings, project-management software and VR headsets (DC-042).

v1 also anticipated the over-reach. Its Rule 3 warns that "over-assignment of Datacraft is the most likely systematic error" (DC-043). The database confirms it: 79 competencies are DC-primary and 91 carry DC-secondary, so 170 of 222 carry a DC tag. Of the 40 Domain 1 science-knowledge competencies, 26 are DC-primary (DC-042). [E]

### 2.2 v2 definition

> **Data craft** is the disciplined capacity to turn observations of environmental systems into *warranted* evidence, models and decision support: designing what gets measured, stewarding data so it stays fit for use and properly governed, analysing and modelling with honest uncertainty, and putting results in front of decision-makers in a form they can act on. Because more and more of that computation is now done by machines, data craft also includes specifying, validating, supervising and answering for AI-generated analysis, not only doing analysis oneself.

**Irreducible contribution: warrant.** The defining deliverable of a data-craft competency is a claim about the world that the practitioner can show and answer for. That means its provenance, method, uncertainty and fitness for a stated decision. The test for data craft becomes: *if you removed the practitioner's ability to establish and defend the warrant for this evidence, would the competency collapse?* [J; it rests on the evidence below that verification, not generation, is where human work concentrates in deployed tools.]

- FWS DocketScope: "Results are verified by analysts during comment review" (DC-001).
- USDA permitting AI: "AI is not making any final decisions, only recommendations for authorized staff to review" (DC-001).
- M-26-04 requires procured LLMs to "acknowledge uncertainty" and to come with model documentation that a human must be able to read and judge (DC-008).

### 2.3 Five durable functions

I propose organizing data-craft competencies by five functions along the observation-to-decision chain. This is a deliberate generalization of v1's Five Functional Positions (DC-044), which are tool-independent and the strongest durable idea in v1. [J]

| Function | What it produces | Five Functional Positions link | v2 candidates / carried v1 |
|---|---|---|---|
| **Acquire** | Measurement and monitoring designs; field-capture and sensor data systems | Sensing & Generating (the data side; observation itself stays FC) | DC-CAND-03, DC-CAND-04; merged field data capture (v1 2.3.3/2.3.4/4.1.5) |
| **Steward** | Fit-for-use, traceable, protected, reusable data | Structuring & Curating | DC-CAND-05, -06, -07, -18; v1 2.2.1, 2.2.3 |
| **Analyze & Model** | Inferences, maps, models, forecasts with stated validity | Analyzing & Interpreting | DC-CAND-08, -09, -10, -12; v1 2.1.2, 2.1.4, 2.2.2, 2.4.1 (rewritten), 2.4.2, 2.4.4 |
| **Integrate & Communicate** | Decision-support products, uncertainty statements, traceable text analyses | Integrating & Presenting | DC-CAND-11, -16, -22 |
| **Assure & Govern** | Validations, review designs, evaluation sets, risk tiers, procurement acceptance, enterprise governance | Deciding & Directing (evidence side; authorization stays SC) | DC-CAND-13, -14, -15, -17, -19, -20, -21; v1 7.2.1 (rewritten), 7.2.3 |

The fifth function is the main structural change from v1. In v1, AI assurance is scattered across 2.6.5, 7.1.4 and 7.2. In v2 it becomes a first-class function of data craft, with statecraft holding authorization (§4.2). [J]

### 2.4 The irreducibility test, v2 wording (for rater rubrics)

The test keeps v1's architecture and changes the data-craft branch. A competency or task is **DC-defining** when all three of the following hold:

- its defining deliverable is an evidence product (dataset, analysis, model, validation, risk determination or evidence-bearing design);
- the quality of that product is judged by its warrant (provenance, method, uncertainty, fitness for use);
- performing it well requires choosing or checking methods, not merely operating a tool.

It is **not** DC-defining in three cases:

- the deliverable is an observation made in place (FC);
- the deliverable is an authorization, agreement or institutional commitment (SC);
- the content is disciplinary knowledge that all three crafts draw on (a knowledge area, not a craft practice; see P-DC-12).

[J]

---

## 3. Progression: from universal literacy to enterprise governance

The brief asks for a progression from universal data/AI literacy, through practitioner analysis and specialist modelling/engineering, to enterprise data and AI governance. I express it as **four tiers of responsibility**, not of tenure. v1's levels are tenure bands (0–2, 3–5, 6–10, 10+ years). These are not observable and are legally weak for selection. [E: DC-042; J on legal weakness, IO to confirm]

| Tier | Scope of accountability | Who (examples) | Typical observable work products | Core DC competencies at this tier |
|---|---|---|---|---|
| **DC-1 Universal literacy** | Own use of data and AI in one's own work | Every environmental professional: field crews, planners, permit staff, managers, administrative staff | A correctly interpreted data product; an AI-assisted product with checks and disclosure recorded; correct withholding of sensitive data | DC-CAND-01, DC-CAND-02, DC-CAND-07 (L1), DC-CAND-13 (L1), DC-CAND-05 (L1) |
| **DC-2 Practitioner analysis** | Own evidence products that others act on | Biologists, foresters, hydrologists, planners, environmental scientists, analysts, NEPA specialists | Monitoring designs; reproducible analyses; validation reports with stratified error; uncertainty sections; LLM extraction with measured error rates | DC-CAND-03, -06, -08, -09, -11, -13 (L2), -16, -22; v1 2.1.4, 2.2.2 |
| **DC-3 Specialist modelling & engineering** | Methods, models and data systems that other people rely on | Data scientists, modellers, remote-sensing scientists, data engineers, GIS leads, fire behaviour/long-term analysts | Validated models and pipelines; human-in-the-loop review designs; evaluation sets; effective-challenge memos; forecast systems | DC-CAND-04, -10, -12, -14, -15, -17, -18; L3 of the above |
| **DC-4 Enterprise data & AI governance** | The organization's (or a partnership's) data and AI portfolio | Chief data/AI officer staff, data governance leads, program directors, AI governance board members, procurement leads for analytics | Data strategy; model/AI inventory with risk tiers; procurement acceptance criteria; organizational validation and provenance standards | DC-CAND-19, -20, -21; L4 of the above |

**Design notes.**
- **Tiers are targets inside role profiles, not job titles.** A GIS lead may be at L3 in spatial analysis and L1 in model risk. CA's hybrid lean computes role blends from competency targets, and this fits it. [J]
- **Every role profile carries a universal floor.** That floor is L1 on DC-CAND-01 and DC-CAND-02. The federal-and-state-first audience can use it directly:
  - OPM deploys enterprise generative AI assistants "with training" for "both technical and non-technical staff" (DC-013).
  - DOL's TEN 07-25 asks state workforce systems to expand AI literacy training (DC-015).
  - Neither defines an assessable standard. EMST can. [E]
- **OPM's 2024 AI competency model is a specialist instrument, not a literacy one.** It applies to positions where AI work is at least 25% of the job. It has no proficiency levels, only which competencies apply at each GS grade (DC-012). Its technical competencies cover AI builders, not the far larger population of AI-using environmental staff. That gap is EMST's opening. [E]

---

## 4. Boundaries and blends

### 4.1 Data craft and field craft

FC owns **observation in place**: what is worth noticing, sensory judgment, site-level manipulation and ground truth (DC-043, DC-044). DC owns **the design of measurement at scale and the chain from record to evidence**.

They meet at shared **boundary objects**:
- monitoring protocols;
- reference and validation data;
- sensor and recorder deployments;
- field-capture forms;
- AI outputs that describe ecological condition.

Proposed rules [J]:
1. **Making** ground truth is FC. **Designing** the validation sample and computing accuracy from it is DC. Both are needed for DC-CAND-09, -10 and -13.
2. **Physical deployment, siting, calibration in place and maintenance** of instruments are FC-primary with DC-secondary. The data path from instrument to analysis-ready data is DC (DC-CAND-04). This splits v1 2.3.1. GNSS collection and UAS flight operations likewise go FC-primary (v1 2.1.3, 2.3.2/4.5.4). Under v1's own Rule 3 these were over-assigned to DC.
3. **Any DC competency that applies or validates models or AI describing ecological condition requires FC-secondary.** This strengthens v1's "assign secondary Fieldcraft more liberally" note (DC-043). The reason is that out-of-distribution failure is usually first seen in the field.
   - The Earth Engine embedding documentation admits bands are "not independently interpretable." The embeddings were trained against NLCD and the Cropland Data Layer (DC-028), so map-on-map agreement can be circular.
   - Field reference data is the independent check. [E for the documentation; J for the rule]
4. **Monitoring design (DC-CAND-03) is a genuine integration point.** I tag it DC-primary because its deliverable is a design for inference. FC may argue for co-equal weight (§12).

### 4.2 Data craft and statecraft

SC owns **making decisions stick**: authorization, agreement and the administrative record. DC owns **the warrant of the evidence that goes into those decisions**.

They meet at these boundary objects:
- decision briefs;
- public-comment analyses;
- LLM-assisted regulatory and plan analyses;
- AI risk determinations;
- procurement requirements;
- oversight designs.

Proposed rules [J]:
1. **Whether an analysis is legally sufficient, and how it enters the record, is SC.** Whether the analysis is accurate, complete and traceable is DC. DC-CAND-16 is therefore DC-primary with SC-secondary.
2. **Authorizing the adoption of AI is SC.** v1 7.1.4 stays SC-primary for this. Specifying the technical conditions (risk tier, validation level, review sampling, escalation thresholds) is DC: DC-CAND-14 and DC-CAND-19.
   - v1 judged a DC-secondary on 7.1.4 "not warranted" because SC practitioners can "engage DC collaborators" (DC-045).
   - The inventory shows why this fails in practice. Three environmental use cases escaped the high-impact designation by asserting that humans remain the "principal basis" (DC-001).
   - Whether that assertion is true is a measurable property of the review design: override rates, seeded-error catch rates. It is exactly what an SC-only governance competency cannot check. [E for the inventory; J for the inference]
3. **Uncertainty communication (DC-CAND-11) carries SC-secondary.** Framing a probability for an authorizing official is a statecraft act. Producing a correct probability is a data-craft act.

### 4.3 Blended roles (examples for CM/FH role profiles)

| Role | Blend (judgment) | Data-craft content | Source |
|---|---|---|---|
| Fire behaviour analyst / long-term analyst (FBAN/LTAN) | FC + DC, SC-secondary | Model calibration and validation, uncertainty and confidence briefing | DC-047 (citations unresolved) |
| UAS data specialist / incident GIS specialist (GISS) | DC + FC | Data products, delivery, data management plan | DC-047 |
| NEPA interdisciplinary team lead | SC + DC | Validating machine-drafted sections, traceable analyses | DC-001, DC-032 |
| Comment analysis lead | DC + SC | LLM coding, error-rate measurement, response tracing | DC-001 |
| Monitoring program lead | DC + FC + SC | Design for inference; adaptive-management triggers (SC per v1 Rule 2) | DC-035, DC-043 |
| Carbon/biodiversity measurement, reporting and verification (MRV) analyst | DC + FC + SC | Measurement design, model validation, provenance for registries | J |
| Farm-program remote-sensing compliance analyst | DC + SC | High-impact model risk, appeal support | DC-001 |
| Data steward working with Tribal partners | DC + SC (TN-governed) | Sensitivity determinations, access control under CARE | DC-029, DC-050 |

---

## 5. What is actually deployed: evidence versus hype

### 5.1 The federal record

The 2025 inventory was compiled under M-25-21. It reports 3,611 use cases across 56 submissions, up from 1,757 in 2024. 445 are high-impact (DC-001, DC-003). The environmental agencies report as follows (DC-001 README):

| Agency | Total use cases | Deployed + piloted | High-impact |
|---|---|---|---|
| USDA | 162 | 86 | 4 |
| Interior | 247 | 129 | 0 |
| EPA | 29 | 14 | 2 |
| Commerce | 223 | 223 | 0 |

- **Growth.** From 2024 to 2025, DOI grew from 180 to 247, USDA from 89 to 162 and EPA from 17 to 29 (DC-002, DC-001). [E]
- **Where the cases sit.** USGS accounts for 187 of DOI's 247. USDA's Natural Resources and Environment mission area (Forest Service) accounts for 76 of USDA's 162. NOAA accounts for 157 of Commerce's 223.
- **What they are.** Across USDA, DOI and EPA, "Science" is the most common topic area (232 of 438). [E: DC-001]

My classification of the 438 USDA/DOI/EPA rows, using the agencies' own fields [E: DC-001]:

| Class (agency-reported) | All stages | Deployed |
|---|---|---|
| Classical ML | 259 | 59 |
| Computer vision | 38 | 5 |
| Generative AI | 53 | 8 |
| NLP | 33 | 11 |
| Agentic AI | 8 | 2 (both administrative) |
| Other / reinforcement learning | 9 | 1 |
| Unclassified (all "Retired") | 38 | 0 |
| **Total** | **438** | **86** |

**Implications for competencies.** [J]
- **The bulk of environmental AI is old.** It is model-based mapping, classification and prediction. Examples are the Ecosystem Management Decision Support system, operational since 1997; regional forest mapping, since 2002; spotted-owl habitat time series, since 2011; and NLCD deep-learning change mapping.
- **The durable competencies those uses need are not new.** They are model evaluation, validation against field reference data, uncertainty, and stewardship of training data.
- **v1 framed AI mainly as "emergent".** 2.6.x is tagged Emergent (DC-042). That framing misreads a mature practice as a frontier, and hides the validation and stewardship debt behind it.

### 5.2 Generative AI: text work in review and planning

The deployed or advanced generative and NLP uses in environmental agencies are all text-heavy [E: DC-001]:

| Agency / tool | Function | Stage (vendor, date where reported) |
|---|---|---|
| USFS "Forest Plan review and planning support" | Plan review | Deployed (Google, 2025-06) |
| USFS "Turbo plan" | NEPA planning document optimization | Deployed (Wildfire.org, 2025-07) |
| FWS DocketScope | Extractive comment summaries, sentiment, extension requests; analyst-verified | Deployed (2025-08) |
| EPA Region 8 | Comment summarization and draft responses | Pilot |
| USDA OCIO | Public-comment analysis | Pre-deployment |
| USDA OCIO | Categorical-exclusion triage and comment processing | Pilot |
| BLM | GraphRAG comment analysis; NEPA categorical-exclusion document generation ("about 35% of the information" pre-mapped from ePlanning/MLRS); small language model to consolidate land-use-plan decisions | Pre-deployment |
| NOAA | "Generative AI for Biological Opinions"; Essential Fish Habitat (EFH) consultation templates; Coastal Zone Management Act (CZMA) §312 evaluation pilot | Names only reported |

PNNL's PermitAI provides shared services (SearchNEPA, CommentNEPA, WriteNEPA, EngageNEPA). Its DraftNEPABench benchmarks LLMs and coding agents on drafting Environmental Impact Statement (EIS) sections. It uses SME-curated rubrics, but grades with LLM judges (DC-032, DC-033). That is itself a validation risk: a judge model's agreement with humans must be measured before its scores mean anything. [E for the method; J for the risk]

**Churn.** DOI's I-NEPA and PCAT tools appear as "Retired" in the 2025 inventory (DC-001). Tools in this space have shorter lives than the roles they serve. [E]

These are the uses v1 6.4.4 (public comment management) and 6.1.1/6.4.1 (policy analysis) code as **S (substitution)**. The deployment record does not support S. Every deployed comment or review tool is described as supplemental, with human verification (DC-001). The evidence supports compressed and supervised work (Ac/V), not substitution. LM owns exposure coding; this is DC's evidence for re-coding. [E]

### 5.3 Agentic AI: pilots, not practice

There are 8 agentic cases across USDA, DOI and EPA.
- **Deployed (2):** both administrative. One is a DOI grants utility; the other is USDA supply-chain security.
- **Environmental (pilot or pre-deployment):**
  - NRCS automated waterway design (vendor-built, pilot);
  - BLM "AI Trapline for Fire", which scrapes weather and fuels products for national briefings (pre-deployment);
  - USGS DiscoverDOI and VoiceAtlas (pilots).

Source: DC-001. A competency for supervising agentic workflows (DC-CAND-17) is justified by trajectory, not by current practice. I label it **[S]**. It is confirmed if the 2026 inventory or PermitAI adoption shows agents in production environmental workflows. It is refuted if agentic entries stay administrative or are retired.

### 5.4 Earth-observation foundation models and embeddings

The models are real and moving fast:
- **Prithvi-EO-2.0** (IBM-NASA): 300M and 600M parameters, trained on Harmonized Landsat Sentinel-2 (HLS) at 30 m. Released December 2024 with fine-tuning examples for floods, burn scars, landslides, crops and biomass. Benchmarked on GEO-Bench (DC-023).
- **OlmoEarth** (Ai2): v1, v1.1 and v1.2 within roughly a year (DC-025).
- **Clay**: open weights (DC-024).
- **Google's Satellite Embedding V1** (AlphaEarth Foundations): 64-dimensional annual embeddings at 10 m. Dataset v1.1 was released 2025-11-17 and the model is v2.1 (DC-028).
- **USGS** reports a "Foundation Models to Advance Earth Science" pilot and deep-learning NLCD change mapping (DC-001). [E]

The catalog entry for the Google embeddings is unusually candid about what a practitioner must handle [E: DC-028]:
- the bands "are not independently interpretable";
- the training targets included NLCD and the USDA Cropland Data Layer;
- production depends on "the ongoing availability of input data streams from USGS and ESA";
- the Cloud Storage bucket became "provider pays" as of July 2026.

Each of these maps to a durable competency, not a tool skill [J]:
- **Interpretability limits:** DC-CAND-09 and DC-CAND-11.
- **Circular validation:** DC-CAND-10.
- **Upstream dependence:** DC-CAND-05 provenance.
- **Cost-shifting:** DC-CAND-20 procurement, plus an equity issue for small organizations (§13).

### 5.5 Digital twins and forecast systems

NOAA's inventory includes:
- an AI-driven global forecast model and ensemble;
- an Ai2 Climate Emulator collaboration;
- AI bias correction and downscaling;
- physics-informed neural networks;
- hybrid physics-ML precipitation models;
- a "Digital Twin for Earth Observations Using AI" pilot (DC-001).

This is model–data fusion and validation work. v1 files digital twins under "Immersive Technologies" (2.7.3), which is a category error. NASA ESDT and Destination Earth could not be verified this session (DC-054, DC-055). [E for NOAA; unverified for the others]

### 5.6 The data-readiness debt behind AI

In 2024 the inventory asked whether training and evaluation data were documented. The 2025 schema dropped the question. [E: DC-002]

| Agency (2024 use cases) | Complete or widely available documentation | Partial | Missing | Not reported |
|---|---|---|---|---|
| USDA (89) | 33 (37%) | 23 (26%) | 13 (15%) | 20 (22%) |
| DOI (180) | 126 (70%) | 7 | 3 | 44 |
| EPA (17) | mostly not reported | | | 12 blank |

Enterprise data catalog access was reported for 172 of 180 DOI and all 89 USDA cases (DC-002). Catalogs exist. What is missing for a large share of models is documentation of the data they learned from. Removing the question from the 2025 schema removes the main public signal of this debt. That is an issue for LM and IA's signal design. [E for the counts; J for the interpretation]

### 5.7 What plans actually demand (OpenLMP)

I searched all 58,544 components from 154 plan records (1987–2025) in the sister repository (DC-035) [E]:

| Term found | Components |
|---|---|
| AI, machine learning, deep learning or neural networks | 0 |
| Remote sensing, satellite, imagery or LiDAR | 55 |
| Modelling | 381 |
| Uncertainty | 38 |
| Best available scientific information (BASI) | 19 |

- **Monitoring** components number 3,843.
- **Authoritative data** is cited by 2,453 components. The most frequent references are long-lived analytical products and systems: Recreation Opportunity Spectrum (614), natural range of variation analysis (224), hydrologic modelling (151), Forest Service corporate data such as NRIS/FACTS/INFRA (140), potential vegetation groups (133), the Watershed Condition Framework (70), FIA (25) and SSURGO (9).
- **A cautionary note for IA.** A naive regular expression for "AI" matched 19 components. All of them were "MON-AI-01"-style codes for *American Indian Rights and Interests* monitoring questions.

**Implications.**
- **Plans lag technology by a decade and are written at the function level.** As a demand signal they argue *for* durable competencies (monitoring design, reproducible analyses of authoritative data, model use) and *against* tool competencies. They cannot tell us about AI adoption; postings and PDs must (LM, IA). [J]

### 5.8 Beyond the federal government (thin)

- **State.** The MegaDetector adopter list names the Michigan DNR Wildlife Division (DC-038). DOL's AI literacy notice targets state workforce agencies, boards and tribal colleges (DC-015).
- **NGO.** The Nature Conservancy in California runs a camera-trap AI platform (DC-038). Ai2's OlmoEarth platform targets mission-driven users (DC-025).
- **Private.** Vendors build many of the deployed federal tools (Google, Wildfire.org, The Regulatory Group; DC-001).

I found no systematic evidence on state environmental agencies' AI use. The thinness is a finding, for SL and PS to fill.

---

## 6. Frameworks and policy: current state and implications

| Framework | Status at 2026-10-23 | Implication for data-craft competencies | Flag |
|---|---|---|---|
| NIST AI RMF 1.0 (2023) | Being revised under the AI Action Plan; no "2.0" released. Critical-infrastructure profile concept note 2026-04-07 [E: DC-004, DC-021] | The trustworthiness characteristics and GOVERN/MAP/MEASURE/MANAGE functions are durable vocabulary for anchors (DC-005). Version-specific content belongs in the tools layer | current; revision pending |
| NIST-AI-600-1 GenAI Profile | 2024-07-26; still the current GenAI profile [E: DC-006] | Reference for DC-CAND-13/-16 risks; content not re-read [J] | current |
| AI Action Plan (2025-07-23) | Directs NIST to remove references to misinformation, DEI and climate change from the AI RMF; recommends new data-center NEPA categorical exclusions [E: DC-010, DC-011] | Competencies must be written at the function level, so they survive changes in political vocabulary (e.g., validating climate-model outputs stays a need whatever the RMF says) [J] | current |
| OMB M-25-21 / M-25-22 (2025-04-03) | Replace M-24-10 (and the Biden-era acquisition memo) [E: DC-007, DC-009] | High-impact definition; minimum practices (pre-deployment testing, impact assessment, human oversight, appeal); CAIOs and governance boards; contract terms (no training on government data, portability, performance monitoring). Maps to DC-CAND-14, -19, -20, -21 | current; M-24-10 and M-24-18 superseded |
| OMB M-26-04 (2025-12-11) | LLM procurement: acceptable-use policy, model/system/data cards, user feedback; sunsets after two years [E: DC-008] | Reading and judging model documentation is now a procurement duty (DC-CAND-20); "acknowledge uncertainty" sets a floor for humans too (DC-CAND-11) | current; short half-life |
| OPM AI competency model (2024-04-29) | 43 general and 14 technical competencies; no proficiency levels; for positions with ≥25% AI work [E: DC-012] | Useful crosswalk target ("Testing and Validation", "Sociotechnical Systems", "Values-Driven Design"). Does not cover AI-using environmental staff. It was issued under EO 14110, which I understand was revoked in January 2025 [J, not re-verified]; OPM's 2025 strategy still cites it (DC-013) | current, no successor found |
| OPM AI Strategy (2025-09) | Role-based learning tracks; enterprise GenAI with training; AI Impact Assessments on data [E: DC-013] | Federal HR is treating AI literacy as training, not as an assessable competency; EMST can supply the standard | current |
| DOL AI Literacy Framework, TEN 07-25 (2026-02-13) | Voluntary guidance for the public workforce system. Content areas: understanding AI, exploring applications, prompting, evaluating outputs, managing responsibly [E: DC-015; content areas via secondary DC-016] | The best US anchor for Tier DC-1 and the state-first audience; crosswalk DC-CAND-02 to it | current; attachment not read directly |
| EU AI Act Art. 4 (with the 2026 Digital Omnibus) | Still an obligation on providers and deployers to "take measures"; no guaranteed individual level; in force 2026-07-27 [E: DC-017, DC-018] | Relevant for multinational private employers (PS). Signals that literacy duties drift toward "measures" rather than verified competence; EMST should measure anyway | current |
| EC/OECD AILit | Final version published; domains Engage/Create/Manage/Shape AI; built for schools and PISA 2029 [E: DC-019] | Good structure; poor fit as a workforce standard | current; poor-fit for workforce |
| CEQ NEPA & Permitting Data and Technology Standard | v1.2 adds record-origin and record-version fields; agency adoption required by the 2025 action plan [E: DC-034, DC-033] | A concrete provenance model for DC-CAND-05 in permitting | current |
| FAIR (2016), CARE (2020) | Durable principles [J; not re-read: DC-049, DC-050] | Knowledge statements in DC-CAND-06/-07; CARE implementation is TN/SC-led | unverified this session |
| Evidence Act / Chief Data Officer function | Statute in force; no 2025–26 OMB memo titled for Evidence Act or Federal Data Strategy [E: DC-009; statute not re-read: DC-052] | Anchor for Tier DC-4 (DC-CAND-21) | unverified |
| EPA 2009 model guidance (CREM) | Not re-read this session (DC-051) | Strongest environment-specific model-evaluation precedent; DB/LM to confirm currency | unverified |
| Digital Promise AI literacy, ESIP, DataONE | Not reached (search budget) [DC-056 to DC-058] | No claims rely on them | unverified |

**Two cross-cutting observations.** [J]
- **Policy is now the fastest-moving layer.** In 18 months federal AI governance went from M-24-10 to M-25-21, added M-26-04 with a built-in sunset, and opened a revision of the AI RMF. Any competency that cites a memo or framework version by name will be wrong within a review cycle. The fix is in §7 and §10.1: competencies name the function, and the tools layer names the instrument.
- **No federal AI framework defines assessable proficiency for AI use.** OPM defines specialist competencies without levels. DOL defines literacy content without assessment. NIST defines organizational risk practices. The individual, observable, level-anchored layer is EMST's distinctive contribution. That is why §9 matters more than any framework crosswalk.

---

## 7. Durable versus tool-bound

### 7.1 The principle (rule in §10.1)

A durable competency names a **function whose output can be judged without knowing which tool produced it**. Tool fluency is the ability to get a particular product, platform, model, format or policy instrument to do something. The two have different half-lives and are assessed differently. They belong in different layers, L1 and L4 in CA's hypothesis. [J]

### 7.2 Results for v1 Domain 2 (and 7.x)

I classified every Domain 2 competency into durable core and tool-bound content (`durable_vs_tool_classification.csv`; verdicts in `v1_assessment.csv`). [J applied to DC-042]

| Durable share | Count | Examples |
|---|---|---|
| High (durable capability; tool is incidental) | 9 | 2.1.2 remote sensing, 2.1.4 spatial analysis, 2.1.5 cartography, 2.2.1 databases, 2.2.2 statistics, 2.2.3 QC, 2.4.2 modelling, 2.4.4 networks, 2.4.5 time series |
| Medium (durable core inside a tool-framed competency) | 16 | 2.1.1 GIS operation, 2.2.4 programming, 2.2.5 metadata, 2.3.1 sensors, 2.4.1 ML, 2.4.3 DSS, 2.5.4 KM systems, 2.6.1–2.6.5, 2.7.3 digital twins |
| Low (mainly tool fluency or misfiled) | 10 | 2.1.3 GPS, 2.3.2 drones, 2.3.4 mobile apps, 2.3.5 radios, 2.5.1 virtual meetings, 2.5.2 collaborative documents, 2.5.3 PM software, 2.7.1 AR, 2.7.2 VR, 2.7.4 immersive |

**Verdicts for the 35 competencies: carry 3, change 25, retire 7.**
- **Retire:** 2.3.4, 2.3.5, 2.5.1, 2.5.3, 2.7.1, 2.7.2 and 2.7.4.
- **Carry:** 2.2.1, 2.2.2 and 2.4.4. Their anchors are rewritten under P-DC-10.
- **Change:** the main changes are merges and rewrites.
  - 2.6.1/2.6.2 are modality-specific AI and fold into a rewritten 2.4.1.
  - 2.6.3/2.6.4 duplicate 2.4.2/2.2.3.
  - 2.3.2 duplicates 4.5.4.
  - 2.3.3/2.3.4 overlap 4.1.5.
  - 2.7.3 becomes DC-CAND-12; 2.5.4 becomes DC-CAND-18; 2.2.4 becomes DC-CAND-08; 2.4.3 becomes DC-CAND-22.

My findings agree with CA's audit, which types 2.1.1 and 2.5.3 as tool or software fluency and EJSCREEN in 6.7.2 as date-sensitive. [E: CA audit §4.1]

**Beyond Domain 2.**
- **Domain 3 (3.4–3.7).** Nearly every task names "AI-powered", "IoT", "blockchain", "RPA bots" or "real-time dashboards". These should be rewritten by function. The 2025 inventory has zero blockchain, cryptocurrency or ledger use cases among 438 USDA/DOI/EPA entries, so 3.4.3 (cryptocurrency/DeFi) should be retired (DC-001). CA's audit also flags 3.6.2's tool and standard embedding for DC and PS to confirm. [E]
- **Named tools in tasks.** 6.3.2 names InVEST/ARIES and 6.7.2 names EJSCREEN/CalEnviroScreen. These names move to the tools layer. My recollection that EPA removed EJScreen from its website in early 2025 is [J], not verified this session. If it is true, it is a textbook case of a tool-bound task text dating within a year.
- **v1 database integrity.** The SA 2.6 working record records Ac for 2.6.1 T1–T2 (and Ac in 2.6.3 and 2.6.5). The database and normalized baseline record A/Hi/X for 2.6.1 T1 (DC-046, DC-048). DE and LM should reconcile this before any exposure value is carried forward. [E]

### 7.3 Evidence on half-lives

| Item | Observed churn | Source | Suggested half-life |
|---|---|---|---|
| EO foundation models | OlmoEarth v1 → v1.1 → v1.2 in about a year; Prithvi-EO-2.0 replaced Prithvi-100M | DC-025, DC-023 | ~1–2 years |
| Embedding products / platform terms | AlphaEarth dataset re-versioned; bucket became provider-pays July 2026 | DC-028 | ~3 years (dataset); platform terms unpredictable |
| Domain AI tools | DOI PCAT and I-NEPA retired between inventories | DC-001 | ~2 years |
| Curricula tied to package stacks | Data Carpentry geospatial R lesson retired 2026 (already on terra), while the ecology R lesson has been "stable" since 2015 | DC-031, DC-030 | lesson ~5–10 years; tool chapters less |
| Policy instruments | M-24-10 → M-25-21 within 13 months; M-26-04 sunsets after 2 years; AI RMF under revision | DC-007, DC-008, DC-004 | ~2–3 years |
| Plan-level analytical functions | ROS, natural range of variation, hydrologic modelling and FIA cited by plans from 1987 to 2025 | DC-035 | decades |

[E for the observations; the half-life figures are J]

### 7.4 The tools & technologies layer (L4) and its review and deprecation policy

`tools_layer_proposal.csv` seeds 53 entries across desktop GIS, cloud EO platforms, EO data products, EO foundation models and embeddings, field-data apps, sensor hardware, camera-trap and bioacoustic AI, programming ecosystems, reproducibility infrastructure, metadata standards, LLM assistants, coding agents, RAG frameworks, domain AI services, evaluation benchmarks, AI test platforms, documentation artifacts, decision-support systems, process models, forecast systems and governance instruments. Each entry carries `serves_competency_refs` (L1/L2 IDs it serves), `maturity`, `expected_half_life_years`, `replacement_risk` and sources.

**Proposed policy** [J; it borrows CA's per-layer cadence (audit §15) and NICE's retained/new/withdrawn status pattern (CA's CA-033)]:

1. **Direction of reference.** L4 entries point to L1/L2 entities. L1/L2 text never names an L4 entry.
2. **Lifecycle states:** `watch` → `active` → `legacy` → `retired`. A retired entry keeps its ID and gets a successor pointer.
3. **Cadence.**
   - A light **quarterly** review covers entries with half-life of 2 years or less, or High replacement risk.
   - A full **annual** review covers everything.
   - **Out-of-cycle** review is triggered by any of:
     - a vendor end-of-life or major-version announcement;
     - a platform pricing or access change (e.g., provider-pays);
     - a policy instrument issued, rescinded or sunset;
     - an inventory retirement;
     - a curriculum retirement;
     - a security or privacy advisory.
4. **Entry criteria.** A tool enters `active` when evidenced in use by at least two organizations or two sector actors (inventory row, adopter list, posting, PD). Otherwise it enters `watch`.
5. **Deprecation criteria.** An entry moves to `legacy` when a successor serves the same L1/L2 refs and the original's maintainer has announced end of support or stopped releasing. It moves to `retired` after one further annual cycle.
6. **Promotion to L1.** A tool class is promoted to L1 only under rule DC-R5 (§10.1): when it creates a new judgment-bearing work product, not merely a faster way to do an old one.
7. **Ownership.** DC stewards the data and AI entries, FC the field-instrument entries, and PS the private-sector reporting tools. DE automates triggers (e.g., GitHub release feeds, inventory diffs). This is fast-layer maintenance and must be cheap. AS's question "who maintains this in year five?" applies most sharply here.

---

## 8. New and transformed data-craft competencies

Full text is in `candidate_competencies.csv` (22 candidates). Summary:

| ID | Title (abbreviated) | Function | Tier entry | Change type | Evidence |
|---|---|---|---|---|---|
| DC-CAND-01 | Interpret and question environmental data products | Integrate & Communicate | DC-1 | transforming | J |
| DC-CAND-02 | Use AI tools responsibly in everyday work | Assure & Govern | DC-1 | new | E |
| DC-CAND-03 | Design monitoring and sampling for valid inference | Acquire | DC-2 | transforming | J |
| DC-CAND-04 | Engineer sensor-network and streaming data pipelines | Acquire | DC-3 | emerging | E |
| DC-CAND-05 | Document data provenance and lineage | Steward | DC-1 | new | E |
| DC-CAND-06 | Steward and publish environmental data for reuse | Steward | DC-2 | transforming | J |
| DC-CAND-07 | Protect sensitive ecological, cultural and personal information | Steward | DC-1 | new | E |
| DC-CAND-08 | Reproducible, auditable analysis incl. AI-assisted code | Analyze & Model | DC-2 | transforming | E |
| DC-CAND-09 | Evaluate model fitness-for-purpose; validate independently | Analyze & Model | DC-2 | transforming | E |
| DC-CAND-10 | Apply EO foundation models and learned embeddings | Analyze & Model | DC-3 | new | E |
| DC-CAND-11 | Quantify and communicate uncertainty | Integrate & Communicate | DC-2 | transforming | E |
| DC-CAND-12 | Build, run and validate forecast systems and digital twins | Analyze & Model | DC-3 | emerging | E |
| DC-CAND-13 | Validate AI-generated environmental analyses (rewrites v1 7.2.1) | Assure & Govern | DC-1 | transforming | E |
| DC-CAND-14 | Design human-in-the-loop review | Assure & Govern | DC-3 | new | E |
| DC-CAND-15 | Build task-specific evaluation sets; benchmark AI tools | Assure & Govern | DC-3 | new | E |
| DC-CAND-16 | LLM-assisted analysis of regulatory, plan and comment text with traceable citations | Integrate & Communicate | DC-2 | new | E |
| DC-CAND-17 | Supervise agentic AI workflows | Assure & Govern | DC-3 | emerging | **S** |
| DC-CAND-18 | Curate authoritative knowledge corpora for retrieval-augmented AI | Steward | DC-3 | new | E |
| DC-CAND-19 | Assess and manage model risk for consequential decisions | Assure & Govern | DC-4 | new | E |
| DC-CAND-20 | Specify, evaluate and accept AI/analytics services in procurement | Assure & Govern | DC-4 | new | E |
| DC-CAND-21 | Govern enterprise data and AI portfolios | Assure & Govern | DC-4 | transforming | E |
| DC-CAND-22 | Design decision support for actual decision contexts (rewrites 2.4.3) | Integrate & Communicate | DC-2 | transforming | J |

**Notes on three candidates.**
- **DC-CAND-07 (sensitive information) must be co-designed with TN.** It is the technical execution layer under Indigenous data governance (v1 7.1.1, CARE), not a substitute for it.
- **The GBIF practices make DC-CAND-07 unusually assessable** (DC-029):
  - documented reason and review date for every sensitivity call;
  - generalization to 0.1° or 0.01° by category;
  - restrict only the distributed copy;
  - never alter the stored record;
  - replace withheld fields with explanatory wording.

  AI raises the stakes. Training sets, embeddings and retrieval corpora can leak locations that a redacted table does not. [J]
- **DC-CAND-18 (corpus curation) is the least obvious but most immediately useful.** Retrieval chatbots over agency guidance are among the most common environmental generative-AI pilots: the BLM AIM chatbot over guidance for 73,000+ monitoring locations, the Forest Vegetation Simulator (FVS) helpdesk, ASKTERRA and a GIS help desk (DC-001). Answer quality depends on whether withdrawn guidance has been removed and authority marked. That is a stewardship act, not a model choice. [J]

`role_signals.csv` records 16 role signals. The strongest [E] are:
- comment analysts (DC-SIG-01) and planners on ID teams (DC-SIG-03): transforming now;
- camera-trap image taggers (DC-SIG-04): entry path at risk;
- fisheries electronic-monitoring reviewers (DC-SIG-05);
- a new farm-program remote-sensing compliance analyst (DC-SIG-07).

The entry-path signals for junior comment reviewers and GIS technicians are [S] until LM finds posting or staffing data.

---

## 9. Responsible AI as competency, not policy text

### 9.1 Design principles for the anchors

Policy texts say what organizations must ensure: testing, oversight, documentation, appeal (DC-007, DC-008, DC-005). A competency must say what a person *does* that someone else can observe and score. `datacraft_proficiency_anchors.csv` holds 48 anchors: 12 competencies × 4 levels. They follow five principles. [J; IO to validate]

1. **Every anchor names a work product** (a validation record, a sensitivity determination, a review specification, a risk assessment), not a state of mind.
   - "Understands automation bias" (v1 7.2.3 Foundational) becomes "applies explicit decision checkpoints and records the basis of acceptance or override".
2. **Levels are scope of accountability:** own work → own products → systems others rely on → organizational portfolio. Tenure is not a level.
3. **Assessments are tool-agnostic and seeded.** Work samples contain planted defects: a fabricated citation, an ecologically implausible species ID, a sensitive location, a misattributed plan statement, an agent that drifts out of scope. The candidate is scored on catching them.
   - The exercise runs on whatever AI tool the employer has, so the assessment survives tool churn.
4. **Volume-aware validation.** At L2 and above, practitioners validate by sample and estimate error rates. Checking every output is impossible at deployed volumes (DocketScope-scale comment sets; camera-trap batches).
5. **Measure the review, not just the reviewer** (DC-CAND-14 L3). Override rates, seeded-error catch rates and time-on-item show whether human review is substantive. These numbers decide whether an organization's "principal basis" claim (DC-001) is true.

### 9.2 What a practitioner must be able to do, by level (condensed)

| Level | Observable core of responsible AI use (across DC-CAND-02, -05, -07, -13, -14, -15, -16, -17, -19) |
|---|---|
| **1 Foundational** (everyone) | Checks whether the tool is approved for the data class; keeps sensitive data out; verifies each factual claim or citation against a source before use; records AI involvement; follows defined review steps and escalates; stops an agent acting outside its task |
| **2 Intermediate** (practitioners) | Decides when *not* to use AI; validates by sample and estimates error rates; records prompt/version/output for products; measures omission and fabrication on extractions; builds a small evaluation set with agreement statistics; completes a model/AI risk assessment |
| **3 Advanced** (specialists) | Designs review rates, thresholds and escalation; measures whether review is substantive; tests LLM-judge scoring against humans; designs leakage controls for training and retrieval data; provides effective challenge; sets re-validation triggers; designs least-privilege agent workflows |
| **4 Expert** (enterprise) | Sets organizational requirements for AI use, provenance, validation and oversight by risk tier; runs a model-risk program and local evaluation before procurement; measures literacy outcomes, not training completion; accounts to data holders and governance bodies |

### 9.3 Hand-offs

- **IO:** a pilot of seeded-error work samples for DC-CAND-13, -05 and -09 (reliability, adverse impact, cost).
- **LC:** a crosswalk of the DC-1 anchors to DOL TEN 07-25 content areas so state boards can fund aligned training (DC-015).
- **FH:** whether the DC-4 anchors can inform CAIO and CDO-office position descriptions.

---

## 10. Answers to CA architecture questions

### 10.1 DC-Q1: Where exactly is the line between durable data competencies (L1) and tool fluency (L4)? A rule.

**Rule set DC-R (for DP-3).** It applies to all three crafts, not only data craft. [J; tested against all 35 Domain 2 competencies and the tool-laden Domain 3 and Domain 6 tasks in `v1_assessment.csv`]

- **DC-R1 Substitution invariance.**
  - *Rule:* A statement belongs in L1 (or as an L2 task) only if it stays true, performable and assessable when every named product, platform, model, library, file format, vendor service and policy instrument is replaced by a functional equivalent.
  - *Consequence:* If substitution would force a rewrite of the statement, its anchors or its assessment, the named thing goes to L4 and the statement is rewritten to the function.
  - *Example:* "Use EJSCREEN to identify overburdened communities" fails. It becomes the L2 task "apply cumulative-burden screening and evaluate the indicators and data behind it", plus an L4 entry, DC-TOOL-042.
- **DC-R2 Judgment-bearing evidence.**
  - *Rule:* L1 content is evidenced by a judgment-bearing work product (a design, inference, validation, determination or decision) whose quality can be scored without knowing which tool produced it.
  - *Consequence:* Content evidenced by successfully operating an interface (configured, exported, ran, logged in) is L4 fluency, however difficult it is.
  - *Example:* "Performs basic GIS operations" (v1 2.1.1 Foundational) is L4. "Detects a coordinate-reference mismatch and states its effect on the overlay result" is L1.
- **DC-R3 Half-life threshold.**
  - *Rule:* Content whose expected useful life is shorter than two L1 review cycles (under 2 years at an annual cadence) is L4, whatever its importance.
  - *Consequence:* Long-lived named standards (SQL, ISO 19115, FAIR-aligned repositories) also sit in L4, flagged long-half-life, because they are named artifacts that can be superseded. L1 says "apply the applicable metadata standard".
  - *Example:* Policy instruments (M-25-21, M-26-04, AI RMF 1.0) are L4 under this rule.
- **DC-R4 Reference direction and tool classes.**
  - *Rule:* L4 points to L1/L2; L1/L2 never names an L4 entry.
  - *Exception:* A task may name a tool *class* when the class changes the work condition itself. Examples are "review machine-generated metadata", "validate AI detections", "supervise an AI agent".
  - *Rationale:* The class describes the situation the human judges, not the product.
- **DC-R5 Promotion.**
  - *Rule:* A tool class is promoted from L4 to an L1 competency when two things are true: its adoption creates a *new judgment-bearing work product*, and that use is evidenced in at least two sector actors or three organizations.
  - *Consequence:* Tools that only speed up existing work stay in L4.
  - *Examples:* LLM text analysis passes, because it created citation-tracing validation and omission/fabrication rates (DC-CAND-16). Agentic AI creates delegation and supervision products but is not yet evidenced in production environmental work, so DC-CAND-17 sits at lifecycle status "proposed" with an [S] label.

**Edge cases the rule settles.**
- **"Prompting AI effectively"** (a DOL content area) splits. The durable part is "specify a task for a delegate, human or machine, with context, constraints and acceptance criteria" (L1). Prompt patterns are L4.
- **Specialized instruments** (eddy-covariance towers, mass spectrometers) split the same way. Calibration judgment and drift detection are L1/L2, with the instrument class named per DC-R4. The instrument model is L4.
- **UAS flight operations** are an FC L2 practice because they carry site-safety judgment. The aircraft and photogrammetry software are L4.

**Evidence that the line matters.** Specific models, AI tools, curricula and memos turned over in one to three years (§7.3), while plan-level analytical functions persist for decades (DC-035). [E] CA's audit reaches the same diagnosis from external frameworks: ESCO, SFIA ("not a catalogue of tools") and the Australian Skills Classification all separate competencies from technology tools, and O*NET has stopped updating its "Tools Used" file (CA audit §§4.1, 13). [E via CA]

### 10.2 DC-Q2: Are responsible-AI capabilities transversal practice, Datacraft competencies, or both, with enactments?

**Both, in three layers.** [J, with E as cited]

1. **A transversal floor in L1 transversal practice, required of every role.**
   - Contents: DC-CAND-02 (use AI responsibly), DC-CAND-13 at L1–L2 (validate AI outputs in one's own work), v1 7.2.3 (calibrate trust), and the universal part of DC-CAND-05 (record AI involvement in work products).
   - Evidence that it is transversal: the people verifying deployed environmental AI are comment analysts, planners and permit staff, not data scientists (DC-001). DOL frames AI literacy for the whole public workforce (DC-015).
2. **Specialist Datacraft competencies.** These are where the methods live: DC-CAND-14, -15, -16, -17, -19, -20, DC-CAND-05 at L3–L4, and DC-CAND-13 at L3–L4.
   - Their deliverables are designs and determinations whose quality depends on statistical and technical judgment. Examples are review sampling rates, evaluation-set construction, risk tiering, and judging model cards.
3. **Craft enactment notes on the transversal floor**, where the craft changes how the same competency is performed:
   - **FC enactment of validation:** ecological plausibility and field ground truth.
   - **SC enactment:** legal sufficiency, administrative record, authorization of the oversight design (v1 7.1.4).
   - **DC enactment:** sampling design and error estimation.

**What this answers in v1.** It answers v1's Delphi flag 8 (is 7.2 a coherent skill area?). Yes, as a function. The cluster should be split across a transversal floor and a DC specialist set, not housed as one mixed-craft skill area. DC proposes to steward the technical content of all responsible-AI anchors so they stay methodologically sound, with SC co-owning the authorization parts and IO validating them.

### 10.3 DC-Q3: What progression from data literacy to expert modelling fits a level-of-responsibility scale?

A **four-level, scope-of-accountability scale** fits data craft and maps onto the tiers in §3 [J; anchors demonstrate feasibility for 12 competencies, E: `datacraft_proficiency_anchors.csv`]:

| Level | Accountable for | Data-craft meaning |
|---|---|---|
| 1 | Own use | Consume and check |
| 2 | Own evidence products | Produce warranted analyses others act on |
| 3 | Methods and systems others rely on | Design, validate, challenge |
| 4 | Organizational or sector portfolio | Set standards, govern |

- **Relationship to tiers.** Tiers DC-1 to DC-4 are the typical *highest* level a role needs across its data-craft competencies, computed from role-profile targets as CA's hybrid lean proposes. A role can be L3 in one competency and L1 in another.
- **Universal floor.** L1 on DC-CAND-01 and DC-CAND-02 for every role profile.
- **Relation to SFIA's seven levels** (rough, [J], SFIA not re-read by me): L1 ≈ SFIA 2–3, L2 ≈ 3–4, L3 ≈ 5, L4 ≈ 6–7.
- **Why four, not seven.** Four keeps v1's migration path (four levels exist), is enough to separate own-work from others'-systems accountability, and matches what can be anchored with distinct work products. Seven would force artificial distinctions in the literacy tier. If IO finds four levels too coarse at specialist grades, splitting L3 is the natural extension.
- **Evidence.** OPM's AI model has no proficiency levels at all, only grade applicability (DC-012). v1's levels are tenure bands (DC-042). Neither is usable as is.

---

## 11. Proposals

- **P-DC-01 Adopt the warrant-based definition of data craft (§2.2) and the five durable functions (§2.3) as the internal organization of data-craft content.**
  - *Carry:* the irreducibility test, Five Functional Positions and Rule 3.
  - *Change:* the DC criterion from "making patterns visible" to "establishing and defending warrant".
  - *Why:* pattern production is what AI automates; warrant is where human accountability sits (§2, §5.2). [J/E]
- **P-DC-02 Adopt rule set DC-R1 to DC-R5 (§10.1) as the DP-3 typing rule separating L1 competencies from L4 tools, for all crafts.**
  - *Why:* a rule, not examples, is needed to keep 50 years of tool churn out of the core.
- **P-DC-03 Restructure v1 Domain 2.**
  - Retire 7 (2.3.4, 2.3.5, 2.5.1, 2.5.3, 2.7.1, 2.7.2, 2.7.4).
  - Change 25 by merge or rewrite (`v1_assessment.csv`).
  - Carry 3 (2.2.1, 2.2.2, 2.4.4).
  - No v2 data-craft competency title names a technology family. Move 2.1.3 and the flight-operations part of 2.3.2/4.5.4 to FC-primary.
- **P-DC-04 Stand up the L4 tools & technologies layer.**
  - Seed it with the 53 entries in `tools_layer_proposal.csv`.
  - Adopt the review and deprecation policy in §7.4: lifecycle states, quarterly/annual/triggered review, entry and deprecation criteria, and DE automation of triggers.
- **P-DC-05 Add universal Tier DC-1 competencies DC-CAND-01 (data literacy) and DC-CAND-02 (AI use), required at L1 for every role profile.**
  - Crosswalk DC-CAND-02 to DOL TEN 07-25 for state workforce systems.
- **P-DC-06 Add the assurance cluster: DC-CAND-13 (rewritten v1 7.2.1), -14, -15, -19, -20.**
  - Split responsible AI into a transversal floor, DC specialist competencies and craft enactments (§10.2).
- **P-DC-07 Add the stewardship cluster: DC-CAND-05 (provenance), -06 (publication), -07 (sensitive information; co-design with TN) and -18 (knowledge corpora).**
- **P-DC-08 Add or transform the analysis and acquisition competencies DC-CAND-03, -04, -08, -09, -10, -11, -12, -22.**
  - Fold the modality-specific v1 2.6.x into a rewritten ML-lifecycle competency (2.4.1).
- **P-DC-09 Populate v1's planned-but-never-drafted 7.2.4–7.2.5 with DC-CAND-16 (LLM text analysis, [E]) and DC-CAND-17 (agentic supervision, [S]).**
  - Give DC-CAND-17 lifecycle status "proposed" and re-test it annually against the inventory.
- **P-DC-10 Replace tenure-band proficiency with the four scope-of-accountability levels (§10.3).**
  - Assess with seeded-error, tool-agnostic work samples (§9.1).
  - Ask IO to pilot on DC-CAND-13, -05 and -09.
- **P-DC-11 Make the federal AI use-case inventory an annual L5 ingest, and OpenLMP plan components an annual demand-signal recompute.**
  - IA classifies each use case to EMST tasks and emits new, retired and stage-change signals.
  - Ask OMB, through AS, to restore the 2024 training-data documentation field. [J]
- **P-DC-12 Separate knowledge areas from craft practices.**
  - Domain 1's 26 DC-primary science competencies should not carry a DC primary tag. Knowledge areas list which crafts draw on them.
  - *Why:* reduces DC over-assignment (Rule 3) and fixes CA's grain finding (audit §4.1). Decision for CA/IA.
- **P-DC-13 Data integrity before carry-forward.**
  - Reconcile the SA 2.6 exposure codes between the working record and the database (DE/LM).
  - Re-examine the v1 S codes on 6.4.4 T2, 6.1.1 T2, 6.1.2 T2 and 6.4.1 T1 against deployment evidence (LM).
- **P-DC-14 Strip tool and trend content from Domain 3 tasks (3.4–3.7) and from 6.3.2/6.7.2; retire 3.4.3.**
- **P-DC-15 Add DC-secondary to v1 7.1.4.**
  - Move technical risk tiering to DC-CAND-19 and oversight-design specification to DC-CAND-14; SC keeps authorization.

---

## 12. Disagreements and trade-offs

**With SC (AI governance ownership).**
- *v1 position:* 7.1.4 is SC-primary with no DC-secondary; SC practitioners "engage DC collaborators" (DC-045).
- *My position:* authorization is SC, but risk tiering and review-design specification are DC. The federal record shows that compliance turns on a measurable property of review (§4.2).
- *Trade-off:* cleaner single-craft ownership and fewer competencies, versus governance that cannot verify its own key claim.
- *Resolution I propose:* co-equal integration point, or craft weights on the 7.1.4 tasks under CA's DP-5.

**With FC (monitoring design and field technology).**
- *Monitoring design:* FC may argue DC-CAND-03 is FC-primary, because indicator choice and site representativeness are field judgments. I tag DC-primary because the deliverable is a design for inference. *Trade-off:* craft clarity versus honouring field judgment. Either way, task-level weights should show both.
- *Where I concede ground:* GNSS, UAS flight operations and sensor siting and maintenance should be FC-primary. I expect FC to agree with stronger FC-secondary on AI validation.

**With LM (what counts as AI exposure in environmental work).**
- *My claim:* environmental AI is dominated by classical ML and computer vision on sensor and EO data (§5.1). Exposure indices built from LLM usage logs or occupation-level text similarity will therefore under-measure environmental data work. They will also over-weight document tasks. [J/E]
- *My contest of v1 codes:* v1's S codes on comment and policy analysis are not supported by deployment evidence (§5.2).
- *Trade-off:* comparability with external indices versus validity for this sector. I propose environmental-specific deployment signals (inventory diffs, adopter lists) alongside the indices.

**With IO (cost of assessment).** Seeded-error work samples are more valid than self-report, but they cost more to build and to score. They also need re-seeding as tools change. The trade-off is defensibility versus scale. A shared, versioned item bank is the mitigation.

**With IA (scope of the tools layer).** I put policy instruments (memos, framework versions) in L4 because they churn like tools. IA or SC may prefer a separate "governance reference" vocabulary. The trade-off is one fast layer versus semantically cleaner typing. I can accept either, as long as L1 never cites an instrument by name.

**With v1 itself.**
- I replace v1's defining DC idea, from patterns to warrant, and dismantle Domain 2's technology structure.
- I keep v1's best data-craft ideas: Five Functional Positions, the irreducibility test, Rule 3, 7.2.1 and 7.2.3.
- *Trade-off:* migration effort versus durability.

**With CA's hypothesis.** "Human-AI practice" is listed as transversal practice in L1. I agree for the floor. I disagree if it means all responsible-AI content is transversal, because the methods would lose an expert owner and anchors would drift into generic language (§10.2).

---

## 13. Issues outside my area that affect the vision

1. **Platform concentration and cost-shifting threaten the last user** (Tribal, local, small NGO). The Google embedding bucket moved to provider-pays (DC-028). Planetary Computer's public repository has been quiet since 2024-11 (DC-027). Competencies and curricula that assume free cloud EO access will exclude the users the charter says not to shut out. (AS, CP, LC) [E/J]
2. **Upstream data continuity.** The flagship EO products depend on USGS and ESA input streams (DC-028). Workforce strategy for data craft assumes those streams continue. (FS should carry this as a scenario driver.) [E/J]
3. **The public signal of data-readiness debt disappeared.** The 2025 inventory schema dropped the training-data documentation question (DC-001 vs DC-002). (LM, IA, AS) [E]
4. **Inventory quality limits the signal pipeline.** Commerce/NOAA rows carry names only. EPA relabelled AI as "SI" (DC-022). (IA must build vocabulary normalization.) [E]
5. **Political volatility of AI vocabulary.** The Action Plan directs removal of "climate change" from the AI RMF (DC-010). EMST's environmental AI competencies must be written so they do not depend on any one administration's vocabulary, and must be defensible to users of every political orientation. (CA, AS) [J]
6. **EMST's own pipeline handles sensitive data.** Position descriptions, postings and plan appendices can contain personal and sensitive location data. The NLP pipeline should apply DC-CAND-07 practices to itself, following the OpenLMP never-publish list (DC-036). (IA, CP, DE) [J]
7. **Evidence outside the federal government is thin.** State, local, Tribal and NGO data and AI practice is largely undocumented in public sources I could reach. (SL, TN, PS, CM) [E for absence in what I read]

---

## 14. Open questions for the Chief Taxonomy Architect

1. Do you accept the warrant-based redefinition of data craft and the five functions (P-DC-01)? Are they compatible with your craft-weights-on-tasks hypothesis?
2. Will rule set DC-R1 to DC-R5 be adopted for all crafts as part of DP-3, or only for data craft?
3. Where do policy instruments live: L4 (my proposal) or a separate governance-reference vocabulary?
4. Do you accept four scope-of-accountability levels (DP-4), or do you want a seven-level SFIA-style scale, with the cost of artificial literacy-tier distinctions?
5. Will Domain 1 science content become typed knowledge areas without craft-primary tags (P-DC-12)?
6. Will responsible-AI content be split into a transversal floor, DC specialist competencies and craft enactments (§10.2)? Who is the steward of record?
7. May candidates with [S] evidence (DC-CAND-17) enter v2 with lifecycle status "proposed", or should they wait in L5 as signals?
8. Who owns the L4 tools layer in year five? I propose DC/FC/PS co-stewardship with DE-automated triggers. Does AS see a host willing to fund fast-layer maintenance?

---

## 15. Files in this folder

| File | Contents |
|---|---|
| `report.md` | This report |
| `sources.csv` | 60 sources (DC-001 to DC-060), including 12 marked `unverified` that could not be read this session |
| `candidate_competencies.csv` | 22 candidate competencies (DC-CAND-01 to DC-CAND-22) |
| `role_signals.csv` | 16 role signals (DC-SIG-01 to DC-SIG-16) |
| `v1_assessment.csv` | 57 verdicts on v1 elements: all 35 Domain 2 competencies, 7.1.4, 7.2.1, 7.2.3, plus structural and data-integrity elements |
| `durable_vs_tool_classification.csv` | Extra file: per-competency split of durable core vs tool-bound content, durable share, disposition and v2 target (38 rows) |
| `tools_layer_proposal.csv` | Proposed L4 tools & technologies layer, 53 seed entries with half-life and replacement risk |
| `datacraft_proficiency_anchors.csv` | 48 observable anchors (12 competencies × 4 levels) with evidence of performance and assessment method |
| `ecosystem.csv` | 32 entities (datasets, standards, policies, programs, tools, platforms) and how EMST connects to each |

**Reproducibility.**
- Inventory counts come from `Data/2025_individually_reported_AI_use_cases.csv` (OMB repo commit 06c7ebe) and `data/2024_consolidated_ai_inventory_raw_v2.csv` (2024 repo).
- Rows were filtered to agency in {USDA, DOI, EPA}, with NOAA rows from DOC, using the agencies' own `development_stage`, `classification` and `is_high_impact` fields.
- OpenLMP counts come from `plans/*/*/*/components.csv` at commit b3e55df, using case-insensitive regular expressions on the `text` and `authoritative_data` fields.
- DE can turn these into scripted checks.
