# EMST Worked Example Pathways (LC-PW-01 to LC-PW-06)

**Owner:** Learning & Curriculum Design Strategist (LC) · **Date:** 2026-10-23 · **Status:** worked examples for Phase 3 review and pilot design. They are not validated programs. All codes are EMST v1 codes (`D.SA.N@Level`). Indicator references use the baseline keys (for example `7.2.1:intermediate:I2` refers to `v1:7.2.1:intermediate:I2` in `data/v1_baseline/indicators.csv`). Task tags give automation type / tacit density / career-ladder position from v1 Task 13; they are single-analyst values and have not passed an inter-rater reliability check [E: LC-050]. Evidence labels: [E], [J], [S]. Source IDs resolve to `sources.csv`. The rules R1–R14 and the codes for modes and assessment methods are defined in `pathway_template.md`.

## Overview

| ID | Type | From → to | Sector actors | Structured hours | Calendar | Main credential |
|---|---|---|---|---|---|---|
| LC-PW-01 | new-hire | New environmental-science graduate → state Environmental Scientist (water-quality compliance) | state (local, Tribal variants) | 200–300 + supervised work | 12 months | Agency inspector qualification; EMST bundle badge |
| LC-PW-02 | upskill | NEPA/permitting specialist → AI-assisted environmental review | federal, state | 60–80 | 10–12 weeks | "AI-assisted environmental review: validation and record" bundle |
| LC-PW-03 | reskill | Field technician / timber cruiser → (A) remote-sensing inventory analyst or (B) fire intelligence/GIS specialist | federal, state, private | A: 250–400; B: course plus task book | A: 6–12 months; B: 1–2 fire seasons | Stackable certificate; "Field-to-pixel calibration" bundle; NWCG GISS (B) |
| LC-PW-04 | cross-sector | Federal wildlife biologist → state agency biologist or consulting ecologist | federal → state, private | 60–120 (after RPL) | 3–6 months | "Applicant-side permitting and project delivery" bundle; existing certifications |
| LC-PW-05 | upskill | Water/wastewater operator → sensor-based monitoring and data-driven operations | local, state, private, Tribal utilities | 40–80 CEU hours (incumbents); apprenticeship about 2 years (new entrants) | 6–12 months | State operator certificate + "Sensor-based process monitoring" bundle |
| LC-PW-06 | baseline | All environmental staff → AI and data-practice baseline (3 tiers) | all, starting with federal, state, NGO pilot | Tier 1: 6–8; Tier 2: +12–16; Tier 3: +4–6 | 1–3 months | Baseline / Practitioner / Supervisor badges |

Hour, calendar and cost figures are LC judgment [J] or speculation [S] unless a source is cited. The pilot should calibrate them (template R13).

---

## LC-PW-01 · New-hire onboarding: state Environmental Scientist (water-quality compliance)

**Header.** new-hire · state (applies with changes to county environmental health and Tribal water programs) · target role: entry-level state environmental scientist doing sampling, inspection and permit-compliance work · SOC 19-2041 (technician variant 19-4042) · typical entry CIP 03.0104 / 26.13xx (see `cip_soc_env_crosswalk.csv`). State class titles and series are the SL lane.

**Why this pathway.** State environmental agencies run most delegated permitting and compliance programs, and new hires reach independence through ad hoc shadowing [J]. EMST v1 has the parts (6.1.x, 1.2.4, 4.1.3) but nothing that states what an entry-level inspector must show at 12 months [E: LC-031]. The v1 crosswalk also omits 19-2041, the largest relevant SOC occupation [E: LC-050].

**Entry profile (assumed from degree, verified in week 1 by diagnostic).** 1.2.4@Foundational, 4.1.3@Foundational, 2.2.3@Foundational, 5.1.1@Foundational, 4.4.1@Foundational.

**Target profile at 12 months and gap**

| CLO (target) | From | Craft | Linked v1 tasks (type/tacit/ladder) | Formation? |
|---|---|---|---|---|
| 6.1.2 Regulatory compliance assessment @Intermediate | none | SC/DC | T1 A/Hi/C; T2 S/Lo/P; T3 H/Hi/C | T2 is substituted: by-hand quota |
| 6.1.5 Enforcement procedures @Foundational | none | SC | T1 A/Hi/C; T3 H/Hi/X | — |
| 6.1.3 Permitting procedures @Foundational | none | SC/DC | T3 V/Lo/C | — |
| 1.2.4 Water quality assessment @Intermediate | F | FC/DC | T1 H/Hi/P (collect samples) | **Yes**: supervised repetitions |
| 4.1.3 Water quality testing and aquatic surveys @Intermediate | F | FC/DC | T2 A/Hi/P (biological surveys) | **Yes** |
| 2.2.3 Data quality control @Intermediate | F | DC/SC | T2 Ac/Lo/P | by-hand quota |
| 3.3.5 Records management @Foundational | none | SC/DC | T2 Ac/Lo/P; CLD flagged | — |
| 4.4.1 Occupational safety @Intermediate; 4.4.4 Hazmat awareness @Foundational | F / none | FC/SC | 4.4.4 T3 H/Hi/P (PPE use) | **Yes** |
| 5.1.1 Written communication @Intermediate | F | SC | T1–T2 Ac/P; CLD flagged | by-hand quota |
| 5.5.3 Complaint resolution @Foundational | none | SC | T1 H/Hi/P (listen to public concerns) | **Yes** |
| 5.3.5 Environmental justice principles @Foundational; 6.7.2 EJ screening @Foundational | none | SC/DC | 6.7.2 T1 V/Lo/P | — |
| 6.5.2 Federal-state-local coordination @Foundational | none | SC | T2 H/Hi/C | — |
| 7.1.3 Regulatory professional integrity @Foundational | none | SC | all H/Hi | — |
| 7.2.1 Validating AI outputs @Foundational | none | DC | T1–T2 H/Hi/P | **Yes** |

**Sample learning outcomes (rule R2)**

- **LO-01** (6.1.2@I; `6.1.2:intermediate:I2`, `I4`, `I5`). Given a permitted facility, its permit and its inspection history, the learner independently conducts a compliance inspection. The learner interprets each applicable permit condition in its site context and drafts a deficiency finding with a corrective-action request that a senior inspector accepts without substantive revision.
- **LO-02** (1.2.4@F→I, 4.1.3@F; `1.2.4:foundational:I1`, `I3`; `4.1.3:foundational:I1`, `I6`). Given a sampling plan and field meters, the learner calibrates the meters, then collects grab samples and field parameters with full chain of custody. Standard: zero chain-of-custody defects across five observed sampling events.
- **LO-03** (6.1.5@F; `6.1.5:foundational:I1`–`I4`). During a site visit with a potential violation, the learner recognizes it and documents it with photos, notes and evidence handling that meet the agency's enforcement-file standard, then reports it through the proper channel.
- **LO-04** (7.2.1@F; `7.2.1:foundational:I3`, `I4`). Given an AI-generated compliance summary containing seeded errors, the learner applies the agency validation checklist, flags every error that changes a compliance conclusion, and records which outputs need expert review.
- **LO-05** (5.5.3@F; v1 text for 5.5.3 Foundational, currently misparsed into indicator cells [E: LC-031]). Handles a routine public complaint under supervision, using de-escalation and agency policy, and documents the outcome.

**Modes and hours [J].**
- CL/OL 40–60 h: statutes and agency procedures, safety, state data systems.
- FD 60–100 h: sampling and biological surveys in two seasons.
- WBL: shadow 10 inspections, then lead 5 under observation.
- SIM 8 h: mock enforcement case; complaint call role-play.
- AIP/VAL 6 h: validation drills.
- MEN: 1 h per week with a named mentor.
- CAP: one end-to-end inspection file at month 11.

**Assessment.**
- OBS with evaluator sign-off: sampling events and inspections, context-coded *field*.
- WS: inspection report and deficiency letter.
- SIM-P: complaint call.
- VAL: AI summary drill.
- CR: explaining the regulatory framework.

IO sets rubric calibration. This pathway is for training, not selection (template §6).

**Sequence.**
1. Months 0–2: safety, agency framework, and supervised sampling (formation repetitions start here, before any AI or automated QC tools are credited).
2. Months 2–6: shadowed inspections, data QC by hand, and records.
3. Months 6–10: lead inspections under observation; enforcement documentation; AI validation.
4. Months 10–12: capstone and qualification review.

**Recognition.**
- RPL: prior sampling experience (an internship log or a state lab training record) can satisfy LO-02 after one observed event. Any course-to-competency transfer follows the SAF-style rule that faculty or an evaluator must judge equivalence to the outcomes [E: LC-001 C2-6].
- Credential: agency inspector qualification (state-defined), mirrored as an Open Badges 3.0 bundle badge, "Water-quality compliance inspection: Intermediate". It carries the EMST IDs and is renewed every 3 years [J].
- External inputs where duties require them: HAZWOPER training for hazardous-waste site work (hours per 29 CFR 1910.120; not re-read this session [S: LC-039]); EPA training such as APTI or NETI courses (offerings not verified this session).

**Duration and cost signals.**
- 12 months, with 200–300 structured hours alongside productive work [J].
- The main cost is staff time: about 50–100 mentor hours a year plus evaluator time for five observed inspections [J].
- External course fees are likely under $2,000 per hire [S].
- Funding: agency training budgets; federal program grants to states may cover training [S, not verified].

**Exposure-informed design.**
- Two entry tasks are tagged substitution or compressive augmentation: 6.1.2 T2 (develop checklists, S/Lo/P) and 2.2.3 T2 (data audits, Ac/Lo/P).
- The pathway therefore requires a **by-hand quota**: two checklists built from the permit text, and one full manual data audit, before automated tools are credited (R7b).
- Sampling and complaint handling are human-essential entry tasks (H/Hi/P), so they are taught through work-based learning, not online (R7c).

**Equity and risks.**
- Field placements must be paid.
- The binding constraint is mentor and evaluator capacity [J; see LC-R-05].
- State variation is large. SL should test the target profile against 3–5 state class specifications before the pilot.

**Evaluation.** Outcome attainment by month 12, time to independent inspection, supervisor-observed transfer at 90 days after qualification, and first-year retention.

---

## LC-PW-02 · Upskilling a NEPA/permitting specialist for AI-assisted environmental review

**Header.** upskill · federal; state environmental-review programs (state "little NEPA" laws, SC/SL to confirm which) · target role: environmental review specialist / NEPA coordinator, Intermediate going to Advanced · SOC 19-2041 (policy variant); federal series per FH.

**Why now [E: LC-030].**
- CEQ's NEPA regulations were removed by a final rule published 2026-01-08. Agencies now follow their own procedures: USDA's 7 CFR part 1b was finalized 2026-04-03 and includes a 75-page limit and a 1-year deadline for EAs; DOI moved its procedures to a departmental handbook on 2026-02-24; EPA proposed procedures on 2026-06-25.
- The CEQ Permitting Technology Action Plan (2025-05-30) sets minimum functional requirements for agency systems, including automated project screening, published screening criteria, integrated GIS, document management and administrative-record management.
- PNNL's DraftNEPABench covers 102 EIS-section drafting tasks across 19 agencies. A vendor estimates 1–5 hours saved per subsection (up to about 15%). That figure is the vendor's own and has not been independently verified [E for the claim existing; S for its accuracy].

The work is shifting from first-draft writing toward screening, validation and record defensibility [J; role signal LC-R-02].

**Entry profile.** 6.1.4@Intermediate (writes EA/EIS sections), 6.1.3@Intermediate, 6.4.4@Foundational–Intermediate, 5.1.1@Intermediate.

**Gap**

| CLO (target) | From | Linked tasks | Note |
|---|---|---|---|
| 6.1.4 NEPA process implementation @Intermediate (re-anchored) → @Advanced for leads | I | T1 A/Hi/C; T2–T3 H | v1 indicators still cite CEQ regulations; re-anchor to agency procedures (v1_assessment) |
| 7.2.1 Validating AI outputs @Intermediate | none/F | T2 H/Hi/P | core of the pathway |
| 7.2.3 Calibrating professional judgment @Intermediate | none | all H/Hi | — |
| 7.1.4 AI governance in decision support @Intermediate | none | all H/Hi | oversight specifications |
| 6.4.4 Public comment management @Intermediate | F/I | T2 S/Lo/P (comment-theme analysis) | substituted entry task: by-hand quota for juniors |
| 2.2.5 Metadata standards @Foundational; 3.3.5 Records management @Intermediate | none/F | 2.2.5 T1–T2 Ac/Lo/P | data standard and administrative record |
| 2.1.4 Spatial analysis @Foundational; 2.4.3 Decision support systems @Foundational | none | 2.4.3 T1 Ac/Lo/P | screening logic and GIS screens |
| 6.5.1 Tribal consultation @Intermediate | F/I | T1–T2 H/Hi/C | **protected**: no AI substitution; scenario materials only under the TN protocol |
| 7.1.3 Regulatory professional integrity @Intermediate | F | all H | disclosure of AI assistance; dissenting findings |

**Sample learning outcomes**

- **LO-01** (7.2.1@I; `7.2.1:intermediate:I2`, `I4`). Given an AI-drafted EA section and the governing agency NEPA procedures, the learner identifies missing authorities, misapplied categorical-exclusion thresholds, unexamined extraordinary circumstances and unsupported effects conclusions. The learner documents an accept, qualify or reject decision with citations a reviewer can follow. Standard: detects at least 90% of seeded consequential errors and makes no false rejection of a correct conclusion without stated grounds [threshold J; IO to set].
- **LO-02** (6.1.4@I; `6.1.4:intermediate:I1`, re-anchored). Given a proposed action, the learner determines the level of review under the *current* agency procedures, including extraordinary-circumstances screening, and records the basis in the format those procedures require.
- **LO-03** (6.4.4@I; `6.4.4:intermediate:I2`, `I3`). Given a large comment set and an AI-generated theme analysis, the learner checks coverage by structured sampling, recovers substantive comments the tool missed, and drafts responses.
- **LO-04** (7.1.4@I; `7.1.4:intermediate:I2`, `I3`). The learner writes an oversight specification for one AI-assisted step in the office's workflow. It names where human judgment is mandatory and whether the step removes entry-level formation tasks.
- **LO-05** (3.3.5@I + 2.2.5@F; `3.3.5:intermediate:I3`; `2.2.5:foundational:I1`). The learner builds an administrative-record entry and the dataset metadata that conform to the agency's implementation of the CEQ data standard.

**Modes and hours [J].**
- OL 8 h: briefing on the procedure changes, built from the agency's own procedures.
- CL 12 h: workshop.
- AIP/VAL 10 h: seeded-error drills. The item bank uses public DraftNEPABench tasks and the agency's past documents, with errors inserted [E that the public benchmark exists: LC-030; drill design J].
- WBL 40 h over 8–12 weeks: one live project under a reviewer.
- COP: monthly.

**Assessment.**
- VAL drills, scored for detection and false alarms.
- WS: oversight specification and record entry.
- ORAL: defend the level-of-review decision to a panel that includes agency counsel.

**Sequence.**
1. Procedures (what changed).
2. Validation fundamentals (7.2.1 and 7.2.3 at Foundational, as review).
3. Domain validation drills.
4. Data standard and record.
5. Live project.
6. Oral defense.

**Recognition.**
- RPL: specialists with documented review of AI-assisted products can challenge LO-01 directly.
- Credential: bundle "AI-assisted environmental review: validation and record defensibility (Intermediate)" with **2-year currency**. The competencies are Emergent and the procedures are reform-sensitive [J].

**Duration and cost signals.**
- 60–80 hours over 10–12 weeks [J].
- Content is built once per agency or consortium; delivery cost is mostly staff time [S].
- Sharing the item bank across agencies is the main saving [J].

**Exposure-informed design.**
- For junior staff entering review work, the substituted entry tasks must stay in the pathway as a by-hand quota (R7b). These are comment-theme analysis (6.4.4 T2 S/Lo/P), comparing laws (6.1.1 T2 S/Lo/P) and drafting summaries (5.1.1 T1–T2 Ac/P).
- The quota: analyze one comment set of at least 200 comments manually, and draft two EA sections unaided, before the person is credited for reviewing AI drafts.
- 7.2.2 (formation workflows) is required for the supervisors of these staff.

**Risks.**
- Tribal consultation content must follow TN's protocol. Simulations must not appropriate real Tribal positions.
- Statute and procedure content belongs to SC. LC owns the pedagogy.

**Evaluation.** Detection rate on VAL drills before and after training; downstream revision rate of AI-assisted sections; objection or litigation flags on documents the learner reviewed (long-run; AS and LM data access).

---

## LC-PW-03 · Reskilling a field technician or timber cruiser into (A) remote-sensing forest inventory or (B) fire intelligence

**Header.** reskill · federal (forestry technician roles), state forestry, private timber and consulting · origin: SOC 19-4071 / 45-4011 (federal forestry technician series per FH) · destination A: SOC 19-4099 (O*NET 19-4099.03 Remote Sensing Technicians) or 19-1032 · destination B: wildland fire GIS and intelligence roles (NWCG GISS and related positions; USWFS intelligence capability) · academic home: CIP 45.0702; feeder CIP 03.0511.

**Why now.**
- LiDAR and modeled inventory are compressing the field-cruising hours through which juniors formed judgment [J: LC-035, LC-034; role signal LC-R-01].
- DOI's Secretarial Order 3448 directs the new U.S. Wildland Fire Service to establish an integrated wildland fire intelligence and data capability [E: LC-026].
- No accredited U.S. fire-intelligence pipeline exists; training is modular (NWCG courses plus remote-sensing and data certificates) [J: LC-032].
- SAF Forest Technology graduates are already expected to determine area and scale from imagery and to make stand-type maps [E: LC-001 FT C4-B.8, B.9]. The foundation is in place.

**Leverage (recognized, not taught).**
- 1.3.2 Forest mensuration @Intermediate: designs inventories, judges in/out trees, knows plot protocols.
- 4.4.x field safety.
- This field ground truth is the learner's comparative advantage (template R6).

**Why a role delta, not a family delta.** CM's analysis lists 23 F7 core competencies that an F1 profile lacks [E: LC-037]. Branch A needs about 8 of them, at Foundational or Intermediate (R1).

**Gap: Branch A (remote-sensing inventory analyst)**

| CLO | From | Linked tasks | Note |
|---|---|---|---|
| 2.1.1 GIS operation @Intermediate | F | T1 A/Lo/P; T3 Ac/Lo/P | tool modules tagged (R8) |
| 2.1.2 Remote sensing data analysis @Intermediate | F/none | T2 Ac/Lo/P; T3 A/Med/C (field validation) | |
| 2.1.4 Spatial analysis @Foundational | none | A/Med | |
| 2.2.3 Data quality control @Intermediate | F | T2 Ac/Lo/P | |
| 2.2.4 Programming and scripting @Foundational | none | T1 Ac/Lo/P | tool-agnostic (R or Python) |
| 2.6.5 AI model interpretation @Foundational | none | A/Hi/C | |
| 7.2.1 Validating AI outputs @Intermediate | none | T1 H/Hi/P | field-validation core |
| LC-C-04 Ground-truth and calibrate remote-sensing products (candidate) @Intermediate | — | links 1.3.2@Advanced `I3` ("Integrates remote sensing… with field inventory") | candidate; or a rewrite of 2.1.2 T3 |
| 2.3.2 / 4.5.4 Drone operation @Foundational (optional) | none | 4.5.4 T2 V/Med/P | FAA Part 107 as evidence |

**Gap: Branch B (fire intelligence / GIS specialist)**
- 2.1.1@Intermediate and 2.1.5@Intermediate (incident map products).
- 4.3.4 Fire weather and behavior analysis, Foundational→Intermediate.
- 2.4.2 Predictive modeling @Foundational.
- 4.4.5 Emergency communication, Foundational→Intermediate.
- 2.6.1 Computer vision (detection products) @Foundational.
- 7.2.1@Intermediate.
- 5.1.2 Public speaking (briefings) @Intermediate.

**Sample learning outcomes**

- **LO-A1** (LC-C-04 / 1.3.2@A `I3`; `2.1.2:intermediate:I6`). Given LiDAR-derived plot metrics and a set of field-cruised plots, the learner designs a calibration sample, computes plot-level error (bias and RMSE for height and basal area) and explains which stand conditions drive the error.
- **LO-A2** (2.1.2@I; `2.1.2:intermediate:I3`, `I6`). The learner classifies multispectral imagery into stand types and validates the result with an accuracy assessment against field reference data. Standard: reports per-class accuracy and the sources of confusion.
- **LO-A3** (7.2.1@I; `7.2.1:intermediate:I1`). Using field knowledge, the learner identifies where a model's training data or assumptions do not match site conditions (understory, slope, species mix) and flags those outputs for qualified use.
- **LO-A4** (2.2.4@F; task 2.2.4 T1). The learner writes and documents a script that automates one repetitive processing step. Standard: a peer can re-run it on new data.
- **LO-B1** (4.3.4@I; `4.3.4:intermediate:I2`, `I3`, `I5`). Given a spot forecast and fuel data, the learner calculates flame length and rate of spread, then delivers a fire-behavior briefing to a crew.
- **LO-B2** (2.1.1@I, 2.1.5@I). The learner produces incident map products to standard within operational-period deadlines. Evidence: task-book sign-off on incidents (context *incident*).
- **LO-B3** (7.2.1@I). The learner validates an automated perimeter or detection product against IR interpretation or field observation and states a confidence level.

**Modes and hours [J].**
- *Branch A:*
  - A stackable community-college GIS / remote-sensing certificate (150–300 clock hours), or a mix of NASA ARSET modules and agency modules (ARSET's 2026 status not verified this session).
  - FD calibration practicum, 40–80 h.
  - WBL detail with an inventory or remote-sensing unit, 4–8 weeks.
  - CAP: a calibration report on a real project area.
- *Branch B:*
  - NWCG S-341 (GIS Specialist for Incident Management), then the GISS position task book completed on incidents [J: LC-032; course and task-book details not verified directly, LC-044 blocked].
  - SIM: sand-table and briefing practice.
  - MEN with a qualified SITL or GISS.

**Assessment.**
- WS: calibration report; classification accuracy assessment.
- POR.
- OBS through the task book for Branch B.
- VAL: model-output drills.
- ORAL: briefing.

**Recognition.**
- RPL: the cruiser's inventory record establishes 1.3.2@I. Evidence can be cruise data, a supervisor attestation, or SAF Forest Technology coursework [E for the SAF criteria: LC-001].
- Credentials:
  - Academic certificate (stackable into an AAS or BS).
  - Bundle badge "Field-to-pixel inventory calibration (Intermediate)".
  - Optional: FAA Part 107 Remote Pilot Certificate [S: LC-040]; ASPRS technologist-level certification [unverified].
  - Branch B: NWCG GISS qualification.
- Workforce Pell can fund an approved certificate of 150–599 clock hours lasting at least 8 and fewer than 15 weeks, provided it meets the 70% completion and placement thresholds and the value-added-earnings test [E: LC-019, LC-020, LC-021]. A new program must operate for 12 months before approval [E: LC-020].

**Duration and cost signals.**
- Branch A: 6–12 months part-time, 250–400 hours [J].
- Branch B: depends on incident assignments; task books commonly take 1–2 seasons [J].
- Community-college certificate tuition is roughly $1,500–6,000 [S].
- Agency details cost salary only.

**Exposure-informed design.**
- 1.3.2 T1 (measure trees, H/Hi/P) is a formation task. This reskilling pathway must **not** become a reason to stop giving new entrants cruising seasons.
- Branch A explicitly keeps the analyst in the field 20–30% of the time as calibration lead. This is rule R6, and the answer to the field-craft concern that the taxonomy underrates judgment earned outdoors [J].
- Branch B is credited only through incident-context evaluation (R5).

**Risks.**
- Federal staffing reductions and reorganization reduce detail slots and mentors [E for staffing declines: LC-028; J for the effect].
- The USFS–USWFS boundary is unsettled [E: LC-027, LC-029].

**Evaluation.**
- Calibration error achieved on real projects.
- Time to independent production.
- Placement into remote-sensing or intelligence roles within 12 months.
- Retention of field calibration duties.

---

## LC-PW-04 · Cross-sector move: federal wildlife biologist → state agency biologist or consulting ecologist

**Header.** cross-sector · federal → state or private · origin: SOC 19-1023, federal biologist series per FH, F2 · destinations: state wildlife agency biologist (19-1023), consulting ecologist (19-2041 / 19-1029), F5 or F3 · CIP origin 03.0601; destination 26.1301.

**Why now.**
- Public-land agency staffing fell by double-digit percentages in several western states, as high as 26% in Colorado per reporting cited by KUNC [E: LC-028, second-hand figure].
- Outflows to state and consulting roles are plausible, but no flow data were found [S; role signal LC-R-06; CM to test].

**What transfers (recognized through RPL).**
- 1.4.1–1.4.5 at Intermediate or Advanced.
- 1.1.2 and 4.1.2 field survey.
- 6.1.4 from the federal reviewer's side.
- 6.5.1 consultation experience.

CM's family-pair analysis shows F2→F5 needs only three core additions (1.7.1, 5.6.2, 6.3.2). F2→F3 needs six field-implementation competencies (4.1.4, 4.2.4, 4.3.5, 4.5.3, 4.7.1, 4.7.4) [E: LC-037]. The real barriers are mostly *sector-actor* differences, not science [J].

**Gap: Variant S (state agency)**
- 6.5.2 Federal-state-local coordination @Intermediate (now from the state side).
- 5.2.1 Stakeholder analysis and 5.2.5 Partnership development @Intermediate (hunters, anglers, landowners, county governments).
- 5.6.2 Social science research methods @Intermediate (human-dimensions surveys).
- 3.1.2 Budget development @Intermediate (federal-aid grant budgets to states [J]).
- State administrative process: no v1 competency; SC lane.

**Gap: Variant C (consulting)**

| CLO | From | Linked tasks | Note |
|---|---|---|---|
| 6.1.3 Permitting procedures @Intermediate (applicant side) | F/I | T1–T2 A/Med/C | e.g., preparing biological assessments for clients |
| 3.1.1 Project planning @Intermediate; 3.1.2 Budget development @Intermediate | F | 3.1.2 T1 Ac/Med/P | fixed-fee and time-and-materials budgets |
| 3.1.4 Contract and agreement administration @Intermediate | F | T3 H/Hi/C | contractor side |
| 6.6.2 Biodiversity credits and habitat banking @Intermediate | none/F | T2 H/Hi/C | mitigation and conservation banking |
| 6.3.2 Ecosystem services assessment @Foundational | none | T2 Ac/Lo/P | |
| 4.1.4 Soil characterization @Foundational | none | T1, T3 H/Hi/P | wetland-delineation support; **formation**: supervised field repetitions |
| 7.1.3 Regulatory professional integrity @Intermediate | F | all H | integrity under client pressure |
| Business development and proposal writing | — | — | **v1 gap**; PS to define |

**Sample learning outcomes**

- **LO-C1** (6.1.3@I; `6.1.3:intermediate:I1`, `I2`, `I3`). For a client project, the learner determines the complete permitting requirements, prepares the biological-assessment section, and anticipates the agency's questions in the submittal.
- **LO-C2** (3.1.2@I; `3.1.2:intermediate:I1`, `I2`, `I4`). Using historical effort data, the learner prepares a survey-scope budget and forecasts the cost to complete at the project midpoint.
- **LO-C3** (7.1.3@I; `7.1.3:intermediate:I3`). Under simulated schedule and client pressure, the learner reports negative survey results and uncertainty honestly in a client deliverable (SIM-P).
- **LO-C4** (6.6.2@I; `6.6.2:intermediate:I2`, `I3`). The learner quantifies project impacts and proposed offsets with appropriate metrics and shows equivalence.
- **LO-S1** (5.6.2@I). The learner designs and fields a short human-dimensions survey on a management question and reports the results with their limitations.

**Modes and hours [J].**
- OL/CL 20–40 h: consulting project delivery, applicant-side permitting, mitigation markets.
- WBL: the first project run alongside a senior project manager.
- MEN: 6 months.
- FD 16–24 h: soils/delineation field days (Variant C).
- Variant S: an intergovernmental mobility detail before a move [J; FH lane for authorities].

**Assessment.**
- WS: BA section and budget.
- SIM-P: the client-pressure scenario.
- OBS: delineation support in the field.
- POR for RPL.

**Recognition.**
- RPL carries most of the load. The learner submits a portfolio of federal survey, consultation and review work, and is assessed per CLO (R10).
- External credentials that travel across sectors: The Wildlife Society's Certified Wildlife Biologist, ESA Certified Ecologist, SWS Professional Wetland Scientist, and optionally a PMI project-management certification (details unverified this session).
- Bundle badge: "Applicant-side permitting and project delivery (Intermediate)".

**Duration and cost signals.**
- 60–120 structured hours after RPL, over 3–6 months [J].
- Course fees $500–3,000 [S].
- Separated federal employees may qualify for WIOA dislocated-worker services, depending on the state [J; SL lane].

**Exposure-informed design.** The project-management entry tasks are compressive augmentation (3.1.1 T2 and 3.1.2 T2, Ac/Lo/P). Because the learners are experienced, the by-hand quota is waived and replaced by a challenge assessment (R10).

**Sector-actor frictions to teach explicitly.**
- Post-federal-employment ethics restrictions on representing clients before a former agency [J: federal post-employment rules exist; FH and CP to brief].
- Billable-time culture.
- Client confidentiality versus public-records norms.

These frictions are first-class content, not footnotes (CM's transfer-friction attributes).

**Evaluation.**
- Placement within 6 months.
- Retention in the destination sector at 12 months.
- Whether the destination employer accepts the EMST bundle (credential portability, R13).

---

## LC-PW-05 · Upskilling a water/wastewater operator for sensor-based monitoring

**Header.** upskill (incumbents) and apprenticeship (new entrants) · local utilities, special districts, state facilities, private operators, Tribal utilities · SOC 51-8031 · CIP 15.0506 · state operator certification is the license anchor.

**Why now.**
- The National Rural Water Association runs registered apprenticeships through state affiliates, typically about 2 years [E: LC-025, LC-024].
- Since September 2025 it has awarded EPA-funded apprentice and mentor stipends: $1,450,000 by March 2026, running to July 2027 [E: LC-023].
- EO 14278 sets a goal of 1 million new active apprentices and calls for upskilling incumbent workers, including in AI use [E: LC-022].
- Registered-apprenticeship related instruction can be funded by Workforce Pell. Up to 49% of instruction can come from employers or sponsors under written agreements [E: LC-020].
- Operators increasingly run processes from online-analyzer and control-system data [J; role signal LC-R-04].

**Coverage warning.** v1 has **no** treatment-operations competency and no operational-technology cybersecurity content [E: LC-031]. This pathway therefore depends on candidates LC-C-05 and LC-C-06, which DB should own.

**Entry profile.** State operator certificate (grade per state). 1.2.4@F/I; 4.1.3@F (field and lab tests); 4.4.1@I.

**Gap**

| CLO | From | Linked tasks | Note |
|---|---|---|---|
| 2.3.1 Sensor deployment and maintenance @Intermediate | F | T1 A/Hi/P; T2 A/Hi/C; T3 Ac/Lo/P | calibration and troubleshooting |
| 2.2.3 Data quality control @Intermediate | F | T2 Ac/Lo/P | continuous-data QC |
| 2.4.5 Time series analysis @Foundational | none | T1 Ac/Lo/P | trends, seasonality, anomalies |
| 2.6.4 Automated data processing and QC with AI @Foundational | none | T2 V/Lo/P | reviewing machine flags |
| 2.4.3 Decision support systems @Foundational | none | T1 Ac/Lo/P | dashboards and control recommendations |
| 7.2.1 Validating AI outputs @Foundational; 7.2.3 Calibrating judgment @Foundational | none | H/Hi/P | sensor drift versus a real event; automation bias at alarms |
| 3.3.5 Records management @Intermediate | F | T2 Ac/Lo/P | electronic compliance records |
| LC-C-05 Operate treatment processes using real-time data @Intermediate (candidate) | — | — | DB module |
| LC-C-06 OT cybersecurity practices @Foundational (candidate, S) | — | — | DC/DB to evidence |

**Sample learning outcomes**

- **LO-01** (2.3.1@I; `2.3.1:intermediate:I2`, `I4`). The learner calibrates an online analyzer (for example turbidity or chlorine residual) against grab-sample laboratory results and systematically troubleshoots a drift. Standard: stays within the method's and the state's tolerances.
- **LO-02** (2.4.5@F, 2.6.4@F; `2.4.5:foundational:I3`, `I5`; `2.6.4:foundational:I5`, `I6`). The learner reviews a week of historian data with automated QC flags, distinguishes a sensor fault from a process change, and records each decision.
- **LO-03** (7.2.3@F; `7.2.3:foundational:I3`). In a high-consequence condition (for example low disinfection residual), the learner applies an explicit decision checkpoint before accepting an automated control recommendation.
- **LO-04** (3.3.5@I; `3.3.5:intermediate:I3`, `I4`). The learner maintains electronic compliance records that survive a mock audit.

**Modes and hours [J].**
- Incumbents: 40–80 state-approved continuing-education hours over 6–12 months:
  - OL/CL modules;
  - vendor and tool modules tagged and expiring (R8);
  - SIM "replay" drills on real historian data;
  - WBL with a lead operator;
  - MEN.
- New entrants: the NRWA-type registered apprenticeship (about 2 years), with these CLOs written into the work-process schedule.

**Assessment.**
- OBS: analyzer calibration and troubleshooting.
- SIM-P: replay drills.
- WS: compliance records.
- VAL: machine-flag review.

**Recognition.**
- RPL: the state operator certificate and continuing-education history recognize 1.2.4, 4.1.3 and 4.4.1.
- Credentials:
  - State certificate (unchanged).
  - Continuing-education hours toward renewal (state-specific).
  - Bundle badge "Sensor-based process monitoring (Intermediate)", with 3-year currency.
  - Registered-apprenticeship completion for new entrants.

**Duration and cost signals.**
- 6–12 months; 40–80 hours [J].
- Funding: EPA workforce grants through NRWA stipends [E: LC-023]; Workforce Pell for an eligible related-instruction component of 150–599 hours [E: LC-020]; utility training budgets.

**Exposure-informed design.**
- Grab sampling and manual lab verification (1.2.4 T1, H/Hi/P) stay in routine practice as a standing by-hand check against sensors (R7b).
- A manual-fallback operation drill is required (LC-C-06).

**Risks.**
- Small systems have one or two operators, so mentors are scarce [J].
- State certification rules differ.

**Evaluation.**
- Analyzer-related violations or alarms caught.
- Time to diagnose drift in drills.
- Completion and retention of apprentices.

---

## LC-PW-06 · AI and data-practice baseline for all environmental staff

**Header.** baseline · all sector actors; first for federal and state agencies and the NGO pilot · three tiers.

**Why this is the first pathway to build [J].**
- It rests on the best-written v1 content. The 7.2.x and 7.1.x competencies have observable indicators with conditions and escalation behavior [E: LC-031].
- Three of its competencies (7.1.3, 7.1.4, 7.2.2) are the top cross-community "bridges" in CM's analysis [E: LC-037]. That makes it portable across every family.
- It addresses career-ladder destruction (CLD) at the source, because supervisors learn to design formation (7.2.2).
- It is cheap and modular.
- EO 14278 explicitly calls for upskilling incumbent workers in AI use [E: LC-022]. Agency AI-use and training policies were not verified this session [S].

**Tiers and CLOs**

| Tier | Audience | CLOs | Hours [J] |
|---|---|---|---|
| 1 Baseline | all staff | 7.2.1@F, 7.2.3@F, 2.2.3@F, 7.1.3@F (disclosure), 7.1.1@F (CARE awareness), 3.3.5@F (keeping records of AI use) | 6–8 |
| 2 Practitioner | staff whose products rely on AI outputs | 7.2.1@I in own domain, 2.6.5@F, 2.2.5@F, 5.1.1@I (writing with AI, by-hand quota) | +12–16 |
| 3 Supervisor | supervisors, training officers | 7.2.2@F→I, 7.1.4@I, 3.5.5@I | +4–6 |

**Sample learning outcomes**

- **LO-01** (7.2.1@F; `7.2.1:foundational:I1`, `I3`). The learner explains why an AI confidence score is not ecological or regulatory accuracy, then applies the agency checklist to an AI output drawn from their own work area.
- **LO-02** (7.2.3@F; `7.2.3:foundational:I1`, `I3`, `I4`). The learner identifies the conditions in their workflow that invite automation bias and applies a decision checkpoint before accepting a high-consequence output.
- **LO-03** (7.1.1@F; `7.1.1:foundational:I2`, `I3`). Before entering data into any AI tool, the learner identifies the CARE principles and recognizes when Indigenous data sovereignty obligations apply. Content must be co-designed under TN's protocol and must not speak for any nation.
- **LO-04** (7.1.3@F; `7.1.3:foundational:I4`). The learner discloses AI assistance in a work product as agency policy requires and keeps the records that support the disclosure.
- **LO-05** (Tier 3; 7.2.2@I; `7.2.2:intermediate:I2`, `I3`). The learner designs a staged exposure protocol for one junior role in their unit. The protocol states which tasks are performed unaided, and for how long, before AI assistance is allowed.

**Modes.**
- Tier 1: OL with short AIP practice.
- Tier 2: VAL drills built from the learner's own domain outputs; a peer-review community of practice.
- Tier 3: CL case workshop, plus a WS formation plan.

**Assessment.**
- Tier 1: a scenario-based mix of selected-response and constructed-response items, pass mark 80% [J].
- Tier 2: VAL drill.
- Tier 3: WS formation plan reviewed by a peer supervisor.

**Recognition.** Open Badges 3.0 badges "EMST AI and Data Practice: Baseline / Practitioner / Supervisor", aligned to EMST IDs, with **2-year currency** because the competencies are Emergent [J]. The NGO pilot can issue these first.

**Duration and cost signals.**
- Tier 1 is about one working day.
- The full three tiers take under 30 hours.
- Content can be shared across agencies. Most cost is development and drill-bank upkeep [S].

**Evidence caveat.** Recalled experimental work suggests that unguarded generative-AI assistance can raise practice performance while lowering unassisted performance, and that carefully designed AI tutors can help [S until re-read: LC-042, LC-041; URLs blocked this session]. The tiers therefore teach *use with validation*, not tool fluency. Tool modules sit in the tools layer (R8).

**Evaluation.**
- VAL drill scores before and after.
- Rate of disclosed AI use in sampled products.
- For Tier 3: the share of units with a documented formation plan at 6 months.
