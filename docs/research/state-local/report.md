# State & Local Government Workforce: Fitting EMST to 50 State Systems and Thousands of Local Employers

**Role:** SL, State & Local Government Workforce Advisor · **Phase:** 2 · **Date:** 2026-10-23
**Folder:** `docs/research/state-local/` · **Evidence labels:** [E] evidence (source IDs in `sources.csv`), [J] expert judgment, [S] speculation.

---

## 0. Summary

1. **Most state and local environmental work happens on the regulator's and operator's side of the counter. v1 is written from the land manager's and applicant's side.** In the 70 classes I sampled, the v1 competencies that map most often are 6.1.2 Regulatory compliance assessment (29 classes) and 6.1.3 Permitting procedures (18). v1 frames both from the regulated party's point of view. Its stage S3 is "securing regulatory authorization for management activities" [E: SL-088]. The state jobs that use these competencies are permit writers, inspectors, enforcement case managers and primacy program staff [E: SL-079, SL-072, SL-071, SL-050]. v1 has no text at all on drinking water or wastewater operations, operator certification, sanitarians, septic, food safety, landfills, primacy, delegation or state environmental policy acts [E: SL-087].
2. **Federal-centric design breaks across state systems in eight concrete ways** (§3):
   - Binding qualifications sit in different places: the spec, the exam bulletin, the posting, the agency, or decided at recruitment.
   - Degree rules diverge for the same work.
   - One state class spans many roles.
   - Level ladders and pay encodings are incompatible with one another.
   - Bargaining units shape the class plan itself (Washington "shadow classes").
   - Licensure statutes split classes.
   - Some specs are decades old.
   - States already maintain native crosswalks that EMST should use, not replace.
3. **The minimal role layer** that crosswalks to 50 systems has three parts:
   - Function-defined role profiles with sector-actor variants, keyed by an **authority-position** facet (regulator, operator, resource manager, applicant/regulated party, funder, advisor).
   - A **jurisdiction overlay**: a dated crosswalk record per state class, carrying the 28 fields in `minimal_common_fields.csv`.
   - **Licensure** as a first-class entity.
   Roles should not be duplicated per state. A role becomes separate (not a variant) only when its task bundle differs materially or a license defines a legal scope of practice. Examples are the certified operator and the registered environmental health specialist (§9).
4. **Mobility.** The live federal-to-state instruments in 2025–26 are equivalency orders and fast-track portals, not IPA or Good Neighbor Authority (GNA) staffing:
   - Pennsylvania counts federal experience as equivalent, writes federal titles into MQ text, and matched titles with generative AI. It reports 1,350 hires with federal experience by August 2026 [E: SL-031, SL-080].
   - No retrieved source shows environmental agencies being targeted [E: SL-026, SL-021].
   - The top barriers are pay ratios (federal pay is 77%–183% of state pay depending on the state), list and status gates, divergent degree regimes, licensure scope and reciprocity, hiring time (90 days state, 136 local), pension non-portability [J], and residency [E: SL-021, SL-036, SL-084].
5. **Workforce system status, verified:**
   - WIOA remains unreauthorized. H.R. 8210 was ordered reported 19–14 on a party-line vote on 2026-04-21, with no floor vote or Senate companion found [E: SL-005, SL-004].
   - PY2026–27 state plan modifications were due 2026-03-03 under TEGL 07-25. Its priorities include competency-based assessments and AI literacy [E: SL-009].
   - 32 states have taken skills-based hiring actions since 2021 [E: SL-010]. Hire-level outcomes are rare. Colorado's are the best: 25% of 2024 hires in skills-emphasizing classes had no degree [E: SL-014].

**Limits.** The team-wide web-search budget ran out after my first 14 searches. I then worked only from URLs those searches had returned, about 85 page reads in total. Planned class-spec samples for Colorado, Oregon, North Carolina and Montana could not be retrieved, so those states appear only through policy evidence. Water-operator certification, REHS workforce data, IPA, GNA staffing, pension portability, public-sector bargaining law and state climate corps are labelled [J] and listed in the verification queue (§15). Three URLs were blocked (§1.3).

---

## 1. Scope, method and limits

### 1.1 Sample design and justification

I sampled state systems for **diversity of civil-service model** first, because model differences are what break crosswalks. Region, size and environmental mission came second.

| State | Model feature tested | Environmental mission covered | Evidence obtained |
|---|---|---|---|
| CA | Exam and eligible-list system; continuous online T&E; LEAP performance-based appointment; very broad generalist class | Water boards, transportation (CEQA/NEPA), water resources lab | 9 classes/postings [E: SL-032–SL-039] |
| WA | "Desirable" (not minimum) qualifications; annual July 1 revisions; union shadow classes | Natural resources (DNR), research scientists, reclamation | 9 [E: SL-040–SL-049] |
| TX | Decentralized: statewide plan sets classes and pay, agencies set qualifications; statutory military crosswalk | Environmental protection, natural resources, hydrology, geoscience, sanitarians, parks | 19 [E: SL-050–SL-057] |
| FL | Broadband statute; experience-for-degree statute (SB 1310) | Solid waste, food safety, county vector control | 3 [E: SL-058–SL-060] (People First postings mostly closed) |
| NY | Competitive exams; NY HELPS exam-free appointments; Section 70.1 transfer lists | DEC programs, climate policy, forestry, enforcement | 11 [E: SL-061–SL-065] |
| MN | Old specs with no MQs; experience-only postings; strong bargaining units | Pollution control, MEPA environmental review | 4 [E: SL-066–SL-070] |
| MI | Constitutional civil service [J]; degrees retained | Drinking water primacy, water permits, enforcement, UST fund | 8 [E: SL-071–SL-076, SL-049] |
| PA | EO 2023-03 degree removal; EO 2025-01 federal equivalency; application-as-exam | Cleanup, waste, oil and gas, NPDES permits | 6 [E: SL-077–SL-084] |
| WI | Qualifications set per recruitment; title-protection statute | Agricultural water quality, air stack testing | 1 [E: SL-085] |
| Local | Municipal class; county class | San José environmental services; Polk County mosquito control | 2 [E: SL-086, SL-060] |

**Gaps.** No Mountain West class specs (CO, MT), no Southeast specs beyond FL (NC), no special-district or utility class specs, and no Tribal specs (TN's lane). For CO, NC, MT, MD, VA, UT, AK, NJ, GA, TN, MO, AZ, CT, IN and HI, policy-level evidence comes from SL-010 and SL-013 through SL-016.

### 1.2 Source choices

- I preferred **primary state HR artifacts**: SAO job descriptions, OFM specs, CalCareers bulletins, MMB specs, DPM specs and state position extracts.
- Where a state's own job board had closed the posting, I used **mirrors of state postings** (ClimateChangeJobs, Terra.do, Handshake). These are labelled Medium quality and cross-checked where possible.
- For federal workforce policy I used DOL's primary TEGL and two independent bill trackers, because congress.gov was not reached.
- For skills-based hiring outcomes I separated **posting-level** sources (Lightcast, Institute for Responsive Government) from **hire-level** sources (Colorado figures in SL-014). Posting changes overstate impact; Burning Glass/HBS found fewer than 1 in 700 private hires benefited [E: SL-014].
- I marked as **outdated** the NCSL 2023 brief, the 2019 CA bulletin salary, the 2021 DWR posting, the 2023 TPWD posting and a stale NY DEC page reporting the last EPS exam in 2007. The stale page is itself evidence of exam-cycle lag.

### 1.3 Blocked or unreachable

- `dec.ny.gov/about/employment/explore-career-descriptions`: permission timeout.
- `ofm.wa.gov/.../job-classes-salaries/listing/`: permission timeout.
- `apps.co.marion.or.us` WebLink: a cookie wall blocked a county class spec.
- Several Florida People First postings returned "no longer advertised".

---

## 2. What state and local environmental employment actually is

Four kinds of work dominate the classes I sampled. Each fits v1 differently.

**(a) Regulatory program delivery under delegation or primacy.** Most federal environmental statutes are implemented by state agencies (and some Tribal and local agencies) under federal authorization [J]. The sampled jobs are permit writers, inspectors, enforcement case managers, compliance analysts and program administrators:
- PA DEP's NPDES permit writer derives effluent limits, reviews treatment design, drafts fact sheets and builds TMDL documents [E: SL-079].
- Michigan's EGLE runs a Lead and Copper Rule compliance analyst [E: SL-071], wetland permit analysts [E: SL-076] and dedicated enforcement case managers who carry cases "through final settlement" [E: SL-072, SL-075].
- Texas's Environmental Protection Specialist series is defined by inspection, impact assessment and permit/license review [E: SL-050].

**(b) Public service operations.** Utilities, health departments, vector control and parks run services continuously:
- Polk County's mosquito-control technicians need a state pest-control license within a year of hire [E: SL-060].
- Texas's Natural Resources Specialist knowledge list includes "water treatment operations" [E: SL-051].
- California requires REHS registration for some environmental scientist positions [E: SL-035].
- Water and wastewater operators are the largest group here [J]. I could not retrieve evidence on them this session.

**(c) State land, forest and wildlife management.** This is v1's home ground. Washington's Natural Resource Specialist 6 (new in 2025) combines district land management, corrections-camp crews and fire [E: SL-045]. TPWD's fisheries biologists match v1 1.4.5 well [E: SL-056].

**(d) Intergovernmental administration and oversight.** States oversee local delivery:
- Wisconsin DATCP specialists hold "technical authority" over county land conservation staff [E: SL-085].
- State DOT staff carry out federal environmental review (Caltrans CEQA and NEPA) [E: SL-038].
- State staff administer cleanup and financial-assistance funds (MI MUSTA) [E: SL-074].

**Implication [J].** Only (c) fits v1's project lifecycle (S1–S6) and its land-manager framing. (a), (b) and (d) need regulator-side, operator-side and overseer-side tasks, which v1 lacks. This matches the CA audit's findings on coverage and workflow stages. It goes further: the gap is in perspective, not only subsector. The same statute generates two jobs, the applicant's and the regulator's, and v1 describes only the first.

---

## 3. How state systems differ, and why a federal template breaks

### 3.1 Binding qualifications live in different places

| Where MQs live | States in sample | Evidence |
|---|---|---|
| In the class spec or exam bulletin | CA, WA (as "desirable"), NY career descriptions | SL-032, SL-040, SL-061 |
| In the posting; spec has none | MN (specs have no MQs; postings carry them) | SL-066, SL-069 |
| Set by each agency under a statewide plan | TX (SAO: "agencies may establish..."); TPWD stricter than the plan | SL-050, SL-056 |
| Set at recruitment for each position | WI ("Specific qualifications... determined at the time of recruitment") | SL-085 |
| In position extracts plus postings | PA | SL-077, SL-080 |

**Why it breaks federal design [J].** OPM qualification standards are series-wide and centrally published. A crosswalk built on spec text would be wrong in Minnesota (the spec has no MQs and dates from 1968–1998 [E: SL-066–SL-068]), wrong at TPWD (which requires a B.S. that the state plan does not [E: SL-056]) and empty in Wisconsin. The crosswalk record needs an `mq_location` field and must be able to sit at the agency or position level.

### 3.2 Degree regimes diverge for the same work

Of the 52 sampled classes with a known rule:

| Rule | Classes | Share |
|---|---|---|
| Degree required | 16 | 31% |
| Degree substitutable by experience | 19 | 37% |
| Not required | 7 | 13% |
| Set by agency or at recruitment | 10 | 19% |

Comparable environmental-analyst work needs a science degree in California's Environmental Scientist class [E: SL-032] and Michigan's EQA series [E: SL-071]. It needs four years' experience with the degree optional in Florida's ES II [E: SL-059]. It needs experience only in Minnesota's MPCA supervisor classes [E: SL-069] and in Pennsylvania's Oil and Gas compliance class [E: SL-080].

The policy landscape explains part of this:
- Pennsylvania removed degree requirements from about 92% of positions [E: SL-012].
- Florida's SB 1310 sets 2 years of experience equal to an associate degree and 4 years equal to a bachelor's [E: SL-016].
- Minnesota's executive order excludes positions that require a professional license or training [E: SL-015].
- California is listed among executive-order states, yet its core science class still requires a degree [E: SL-016, SL-032].

**Implication [J].** EMST cannot carry a single "entry requirement" per role. It must carry a degree rule plus a machine-readable substitution formula per jurisdictional class. Its proficiency evidence should be designed to slot into those substitution rules. That is the practical meaning of "skills-based" in state HR.

### 3.3 One state class covers many EMST roles

- California's Environmental Scientist (0762) covers a Water Board nonpoint-source scientist, a Caltrans biologist doing CEQA/NEPA, and a DWR laboratory chemist [E: SL-036, SL-037, SL-039].
- Texas's Natural Resources Specialist spans botany, water treatment operations and wildlife management area planning [E: SL-051].
- Washington's NRS 1 includes geoduck compliance diving [E: SL-044].

The mapping from class to role is one-to-many, and from role to class many-to-one across states.

**Implication [J].** The crosswalk needs a class-level record that lists several candidate role variants with weights. A position-level override (from the posting or PD) is needed wherever the class is broad.

### 3.4 Level ladders and pay encodings are incompatible

| State | Level ladder | Pay encoding |
|---|---|---|
| TX | I–V or I–VI | Salary groups B16–B25, annual dollars [E: SL-050] |
| WA | 1–6 | Range numbers 44–70 against a separate table [E: SL-044, SL-046] |
| CA | Alternate ranges A/B/C within one class, plus Senior Specialist/Supervisor | Monthly [E: SL-032, SL-035] |
| NY | Trainee 1, Trainee 2, then EPS 1 | SG-13/14/18; management grades (M-4) separate [E: SL-061, SL-065] |
| MI | 9, 10, P11, 12 ("P" = progression level [J]) | Hourly [E: SL-073] |
| MN | — | Hourly ranges in postings; specs have no pay [E: SL-069] |

**Implication.** v1's tenure bands (0–2, 3–5, 6–10, 10+ years) partly match state experience minimums. TPWD uses 0/2/6/10 years [E: SL-056]. But years are substitutable and are not how states separate levels. States use supervisory status and autonomy language ("moderate," "general," "limited," "minimal" supervision in Texas [E: SL-050, SL-051]). Level crosswalks should key on supervisory status and autonomy first and years second (P-SL-10).

### 3.5 Labor relations shape the class plan

- Washington adopted bargaining-unit "shadow classes" (e.g., Natural Resource Scientist 1 – WPEA, 516K) on 2025-07-01 and abolished one (NRS 4 – WPEA, 523V) on 2026-07-01 [E: SL-042, SL-048].
- Minnesota specs are tied to bargaining units 207, 216 and 220. Its supervisory spec requires "administering labor agreements" [E: SL-066–SL-068].
- NY DEC titles sit in PEF's PS&T unit [E: SL-061].

Where collective bargaining exists, reclassification and class consolidation are usually subject to bargaining or meet-and-confer [J]. Some states bar public-sector collective bargaining contracts (for example North Carolina) [J; verify].

**Implication [J].** Any EMST product that implies "reclassify these positions" will meet labor-relations review. EMST should map *onto* existing classes without demanding class changes. Shadow classes must resolve to the same role variant, with `bargaining_unit` recorded as context.

### 3.6 Licensure statutes split classes

- Texas's Engineering Specialist series "must not be assigned duties" that require a PE license [E: SL-055].
- Texas's Geologic Specialist is the sub-licensure track for Geoscientists-in-Training working under a licensed P.G. [E: SL-054].
- Wisconsin had to retitle its Environmental Engineering Specialist series after 2017 Act 111 restricted "engineer" in classified titles [E: SL-085].
- Washington layers geologist and hydrogeologist licenses onto research classes [E: SL-047].
- California layers REHS registration onto Environmental Scientist positions [E: SL-035].

**Implication.** Licensure is a hard boundary on skills-based substitution and a major cross-state mobility barrier. It needs to be a first-class entity (credential, issuing jurisdiction, scope, timing such as "at hire" or "within 12 months", reciprocity) linked to role variants (P-SL-11).

### 3.7 Spec currency varies by decades

Washington revises specs every July 1 and removed knowledge-and-abilities statements from NRS specs in 2025 [E: SL-044]. Minnesota's Pollution Control Technician spec was established in 1968 and last substantively revised in 1976 [E: SL-066].

**Implication [J].** Spec text is an unreliable input for NLP mapping in some states. The crosswalk must be dated (`spec_effective_date`) and should prefer current postings or PDs where specs are stale.

### 3.8 States already maintain native crosswalks

| Native crosswalk | What it records | Evidence |
|---|---|---|
| Texas SAO military crosswalk | Military occupation codes to each Natural Resources class | SL-052 |
| New York Section 70.1 transfer lists | Related titles for lateral transfer (EPS 2 accepts Climate Policy Analyst 2, Forester 2, Sanitary Construction Inspector 3, and others) | SL-062 |
| Minnesota postings | Internal equivalent classes (Environmental Specialist 4, Planner Principal, Hydrologist 2, Engineer 2 Graduate) | SL-069 |
| Pennsylvania MQs and "Careers for Federal Employees" | Qualifying titles across media; equivalent federal titles | SL-080, SL-029 |

**Implication.** These are **state-validated adjacency judgments**. They are the best available gold set for EMST's NLP crosswalk (IA) and transferability metrics (CM). They also show that states will maintain crosswalks when a statute or executive order requires it, which is the governance model to copy (P-SL-08).

---

## 4. Local government, special districts and utilities

**What the evidence shows.**
- San José's Environmental Services Specialist series (8201–8203) is a flexibly staffed ladder. It bundles program management, contracts, legislative advocacy and policy work, and lets experience substitute year for year for the bachelor's [E: SL-086]. v1 spreads these across Domains 3, 5 and 6. Local roles are **broad by necessity** [J].
- Local environmental health and vector control are **credential-gated after hire**. Polk County requires the state license within a year [E: SL-060]. California requires REHS registration under Health & Safety Code 514–534 [E: SL-035].
- Local hiring is slower than state hiring: 136 days versus 90 on average [E: SL-021].
- 26% of local and 27% of state government workers (excluding education and hospitals) are 55 or older [E: SL-011]. This is the only retrieved retirement-pressure statistic, and it is not environment-specific.

**What I could not evidence this session [J].** These are standard practitioner knowledge, flagged for verification:
- Water and wastewater operator certification is state-run, graded by facility class and tied to federal guidelines for drinking water.
- Reciprocity between states for operators is partial.
- Utilities face retirement-driven operator shortages and are adopting Registered Apprenticeship.
- Air districts (e.g., California's local districts) are separate employers with their own classes.
- Special districts (water, sanitation, conservation, mosquito-abatement and fire districts) are separate public employers with their own HR rules.

**Implication [J].** Local employers do not have one civil-service system. They have thousands, many with merit systems run by county HR, some under state-imposed merit rules for grant-funded positions, and many without published specs. The local entry point therefore cannot be class-spec crosswalking at scale. It should be **role-variant self-mapping**: an HR generalist or department head picks the EMST role variant and level, and EMST supplies a draft class description and MQ language (P-SL-09). This is the "design for the last user" path for counties, cities and districts.

---

## 5. Workforce system levers

Full table: `state_policy_levers.csv` (29 levers). The key points follow.

**WIOA status (verified).**
- *A Stronger Workforce for America Act of 2026* (H.R. 8210) was introduced 2026-04-06 and ordered reported 19–14 on a party-line vote on 2026-04-21 [E: SL-005, SL-003].
- No floor vote or Senate companion was found as of late July 2026 [E: SL-004, SL-005]. WIOA has not been reauthorized since 2014 [E: SL-004].
- The bill would: require 50% of Adult and Dislocated Worker funds to go to training; raise the governor's reserve to as much as 25%; allow single-area designations; hold authorizations flat with Dislocated Worker funding down 4.5%; and move adult education to DOL [E: SL-002, SL-001].
- The FY27 budget request keeps a "Make America Skilled Again" block grant (10% for apprenticeship; about $1.23B cut) [E: SL-008]. Counties object to the loss of local share and flexibility [E: SL-001].

**State plans.** TEGL 07-25 (2026-01-26) required PY2026–27 modifications by 2026-03-03. It ties priorities to *America's Talent Strategy*: industry-driven training, Registered Apprenticeship, "competency-based assessments," AI literacy across the public workforce system, refreshed LMI and Workforce Pell readiness [E: SL-009]. Public employers are not mentioned.

**Implication [J].** EMST's WIOA hook is sector strategy for utility and environmental-services occupations, where public employers are large employers and the apprenticeship emphasis fits operators and technicians. It is not state government HR. That framing should be built for the PY2028 four-year plans.

**Skills-based hiring.**
- 32 states acted between 2021 and 2025 [E: SL-010]. Over half have policies [E: SL-011].
- The state share of postings requiring a degree is 61%, against 70% in the private sector [E: SL-012].
- Hire-level outcomes are scarce. Colorado reports about 80% of classifications emphasizing skills and 25% of 2024 hires in those classes without degrees (1,588). Maryland and Pennsylvania track applicants rather than hires [E: SL-014].
- NGA's *Skills in the States* initiative published a Skills-Based Talent Metrics Toolkit on 2026-09-24 [E: SL-017]. It is the obvious channel for EMST.

**Assessment routes that can carry EMST indicators.**
- NY HELPS: exam-free appointments, about 28,473 hires by May 2025 [E: SL-013].
- California's continuous training-and-experience exams [E: SL-032].
- Pennsylvania's application-as-exam [E: SL-080].
- California's LEAP job examination period, where performance on the job is the exam [E: SL-033].

Each is a place where EMST behavioral indicators could become the assessment content (IO and LC to design).

**Displaced federal workers (2025–26).**
- Pennsylvania: EO 2025-01 equivalency, with 1,350 hires by 2026-08-20 [E: SL-031].
- Hawaii: Operation Hire Hawai'i, a 14-day target [E: SL-021].
- Maryland: an expedited single application for HR, procurement and accounting roles [E: SL-026].
- New York: "You're Hired", 1,300 applications and 28 hires in the first month [E: SL-024].
- North Carolina (joinNC), Virginia, New Mexico and a Washington priority bill [E: SL-018, SL-021, SL-025].

None of the retrieved sources targets environmental or natural-resource agencies by name. Pennsylvania's open vacancies included an aquatic biologist and an air-monitoring specialist [E: SL-028]. **This is the clearest near-term use case for EMST:** a federal-to-state role crosswalk that routes released federal environmental staff to state environmental vacancies (P-SL-08).

**Apprenticeship, corps, unions.**
- Pennsylvania's Environmental Engineer Trainee is a one-year formal and on-the-job program [E: SL-079]. It is a de facto apprenticeship that could be registered [J].
- Washington's NRS 5 class supervises youth-corps crews [E: SL-040], an entry pipeline.
- I could not verify the 2025–26 status of AmeriCorps-funded state climate corps this session [S: verify].
- Union constraints on reclassification are discussed in §3.5.

---

## 6. Mobility map

Full table: `mobility_map.csv` (11 instruments and bridges, 10 barriers).

**Instruments that are working now [E].**
- Equivalency orders and MQ text naming federal titles (Pennsylvania) [SL-031, SL-080].
- Fast-track portals (Hawaii, Maryland, New York, North Carolina) [SL-021, SL-026, SL-024, SL-025].
- Native transfer lists (New York 70.1; Minnesota equivalents) [SL-062, SL-069].
- Statutory military crosswalks (Texas) [SL-052].
- State staff performing federal review (Caltrans) [SL-038].
- State technical authority over county staff (Wisconsin) [SL-085].

**Instruments that matter but were not evidenced this session [J].**
- IPA assignments.
- Good Neighbor Authority and Shared Stewardship staffing.
- Interagency wildland fire qualifications and mutual aid. This is the only environmental-sector qualification already portable across federal, state, local and Tribal employers, and the model for portable EMST proficiency records.
- Cooperative agreements and federal categorical grants that fund state positions.

Land management plans barely encode these instruments. OpenLMP components mention Good Neighbor 9 times and shared stewardship 12 times, against 726 components naming state or local entities [E: SL-090]. Plan-derived demand signals therefore undercount the state staffing these agreements create.

**Barriers, ranked by my judgment of severity for federal-to-state moves [J, with evidence where cited].**
1. **Pay.** Federal pay is 183% of state pay in Maryland, 175% in Virginia and about 3x in Hawaii, but 97% in California and 77% in New York [E: SL-021]. The friction is strongly state-specific.
2. **Status and list gates.** California requires list, transfer, reinstatement, LEAP or SROA eligibility on top of MQs [E: SL-036]. New York transfers require permanent competitive service [E: SL-061].
3. **Degree and licensure divergence** (§3.2, §3.6).
4. **Speed.** State hiring averages 90 days and local 136 [E: SL-021].
5. **Pensions.** Separate defined-benefit plans and vesting rules [J].
6. **Residency.** Pennsylvania DEP requires in-state residency [E: SL-084].
7. **Bargaining-unit change** on transfer [E: SL-042, SL-069].
8. **Perceived non-transferability.** A laid-off federal worker reports that "people with 20 years in government... are being told their experience isn't transferable" [E: SL-021]. This is the user problem EMST exists to solve.

**State and NGO/private bridges [E/J].**
- Regulator and applicant roles mirror each other. Texas EPS II "may review consultant work" [E: SL-050], so permit writers and consultants share task bundles from opposite sides. This is the most natural public–private corridor and PS's counterpart.
- Corps-to-entry-level is an NGO-to-state corridor [E: SL-040].

---

## 7. Designing for 50 systems

### 7.1 Minimal common fields

`minimal_common_fields.csv` defines 28 fields (16 MUST, 10 SHOULD, 2 MAY), each tied to evidence of variation in the sample. The MUST set:
- jurisdiction and employer type
- agency
- class code, title and series
- level index and supervisory status
- spec effective date
- work-description text
- MQ text and MQ location
- degree rule
- licenses with issuer and timing
- pay basis, range and effective date
- provenance
- the EMST mapping record (role variant, competency targets with level, match type, confidence, reviewer, review date)

Observed availability:
- Class code was exposed for 40 of 70 sampled classes. New York career pages and Pennsylvania postings did not expose it.
- Pay was stated for 40 of 70.
- No sampled spec exposed an SOC code. I recommend SOC and EEO-4 job category as SHOULD fields, because most state and local employers already report against them [J; verify EEO-4 coverage].

### 7.2 Crosswalk method

This is my requirements contribution; IA owns the engine.

1. **Ingest.** Pull class specs, exam bulletins, postings and PDs into the minimal-fields record, with provenance. Prefer postings where specs are stale (MN) or carry no MQs (MN, WI, TX agencies).
2. **Candidate generation.** LLM or semantic matching from work-description and duties text to EMST tasks, then roll up to role variants. Generate several candidates per class, because classes are broad (§3.3).
3. **Level assignment.** Use rules on supervisory status and autonomy phrases first, then experience minimums (P-SL-10).
4. **Authority-position tagging.** Classify the class as regulator, operator, resource manager, applicant/regulated party, funder or advisor from duty verbs ("issue," "inspect," "enforce," "operate," "review consultant work").
5. **Human review.** A state classification analyst or agency training officer reviews each mapping. Record reviewer, date and match type (exact, close, broad, narrow, related; SKOS-style), plus confidence. Publish confidence, as Pennsylvania's GenAI matching did not [E: SL-027].
6. **Evaluation gold sets.** Use native crosswalks (Texas military crosswalk, New York 70.1 lists, Minnesota equivalents, Pennsylvania federal equivalencies) to test whether EMST similarity reproduces state-validated adjacency (CM and IA).
7. **Versioning.** Crosswalk records are dated, re-run each July 1 or when the state plan revises, and never overwritten.

### 7.3 What a state HR analyst or training officer needs tomorrow [J]

- **HR or classification analyst.** For a given class, the mapped role variant(s), level and competency targets. Draft MQ language with substitution formulas the state already permits. The licensure boundary. The federal series equivalent for displaced-worker hiring.
- **Training officer.** For a role variant and level, the competency gaps between an incoming federal employee or new hire and the role. A short list of learning resources (LC). Indicators usable in a probationary or job-examination period (CA LEAP model).
- **County or city department head.** Pick a role variant and get a draft class description, MQs and a career ladder. No crosswalking needed.

### 7.4 Adoption hooks

| Channel | What it reaches | Status |
|---|---|---|
| NGA Skills in the States | Governors' offices and state CHROs; toolkit and learning community | Active [E: SL-017] |
| NASPE (state personnel executives) | State CHROs | [J; verify] |
| NASWA and state workforce boards | WIOA LMI and sector strategies | [J] |
| ECOS (state environmental agency leaders) | Workforce leads for Delphi and pilot | [J] |
| Program associations: ASDWA, ACWA, NACAA, ASTSWMO, NASF, AFWA | Module validation; candidate stewards | [J] |
| NEHA and NACCHO | Environmental public health module and local health departments | [J] |
| NACo, NLC, USCM | County and municipal employers | NACo, NLC and USCM co-signed a 2026 letter on ASWA funding [E: SL-003] |
| Work for America Civic Match | Distribution for federal-to-state matching | [E: SL-022] |

All are recorded in `ecosystem.csv` (33 entities). The first ask to each should be small: endorse the minimal common fields and contribute 20–50 specs to the pilot crosswalk.

---

## 8. Verdicts on v1 for state and local use

Full table: `v1_assessment.csv` (20 rows). Headlines:

- **Retire** the "Public Agencies" note. Of 222 notes, 13 match state terms and 10 local terms; 167 name no level of government [E: SL-087]. This agrees with CA audit §7.
- **Change** the federal-only reform flags to dated, jurisdiction-tagged driver events. Examples: state environmental policy act amendments, delegation or assumption changes, skills-based hiring orders, federal grant cuts [E: SL-088; J].
- **Change** S3 and the stage model. Add regulator-side authorize, inspect and enforce functions and operator-side "operate" [E: SL-088, SL-079, SL-072]. This extends CA audit §8.
- **Change** 6.1.2, 6.1.3 and 6.1.4 into role-variant enactments and generalize them beyond NEPA. **Deepen** 6.1.5. **Split** 6.7.5 [E].
- **Carry** 4.7.3 (stormwater/MS4) and 3.3.1 (supervision; add labor-agreement administration) [E: SL-067].
- **Add** water and wastewater operations, environmental public health services, solid waste facility regulation, oil and gas regulation, remediation-fund administration and environmental financial assistance. There are 16 candidates in `candidate_competencies.csv`, most [E], with SL-C05 and SL-C12 at [J].
- **Change** two family-to-SOC mappings that look wrong [J; FH and IA to confirm]: F13 maps to 29-9021 (Health Information Technologists) and F11 to 25-4031 (Library Technicians) [E: SL-089].
- **Coverage signal.** The 70 sampled classes map to only 73 of 222 v1 competencies. Domain 6 dominates and Domain 7 never maps.

---

## 9. Answers to CA architecture questions

### SL-Q1. What does a minimum role layer need to look like to crosswalk to 50 state classification systems? Role variants or separate roles?

**Answer: role variants with a jurisdiction overlay, not per-state roles. Separate roles only where the task bundle or legal scope of practice differs.**

1. **Role profile = function × authority position.** The authority-position facet has six values: regulator, operator, resource manager, applicant/regulated party, funder/grantor, advisor/researcher. Example: "Water quality permit writer" (function: authorize; position: regulator) is one role. **Sector-actor variants** sit beneath it: state agency, Tribal program under treatment-as-state, local, federal (EPA direct implementation). Each variant adds tasks, authority and frictions; the core task bundle is shared.
   - Evidence [E]: the same function appears across very different state classes. Permit writing shows up in PA Environmental Engineering Specialist, MI EQA, TX EPS III and CA Environmental Scientist [SL-079, SL-073, SL-050, SL-038]. Inspection shows up in TX EPS, PA EPS and FL ES II [SL-050, SL-078, SL-059].
   - Judgment [J]: per-state roles would multiply about 50-fold without adding information. The real variation sits in qualifications, pay, licensure and appointment route, which are class attributes.
2. **Jurisdiction overlay = a dated crosswalk record per state class (and optionally per agency or position)** carrying the minimal common fields (§7.1). This is where degree rules, substitution formulas, licensure, pay band, bargaining unit and appointment route live.
   - Evidence [E]: these attributes vary within a single role across states (§3.1–3.6). Agency overlays exist (TPWD) [SL-056], and MQs are set per recruitment in Wisconsin [SL-085].
3. **Cardinality.** One class maps to many role variants (weighted). One role variant maps to many classes across states. Shadow classes map to the same variant [E: SL-036/037/039; SL-042].
4. **Separate role, not a variant, when** either:
   - (a) a license or certification defines a legal scope of practice that changes what tasks can be done (certified operator in responsible charge; REHS inspector; licensed PE or PG versus sub-licensure specialist) [E: SL-055, SL-054, SL-035]; or
   - (b) the core task bundle overlaps below a threshold. I suggest less than about 60% shared core tasks as a starting rule [S]; IO and CM should calibrate it against the native crosswalk gold sets.
5. **Levels.** Each role variant carries the EMST level-of-responsibility scale. State levels map through supervisory status and autonomy, with years as a secondary signal (§3.4) [E/J].

### SL-Q2. Which state and local roles must be in the MVP?

**Criteria [J]:**
- (i) large state or local employment;
- (ii) absent or misframed in v1;
- (iii) high mobility value (federal-to-state or public–private);
- (iv) evidence in hand.

Employment sizing could not be verified this session. LM should confirm with Census ASPEP functions (sewerage, water supply, solid waste, natural resources, parks, health) [J].

| # | MVP role (function × position) | Primary state/local variants | Why MVP | Evidence |
|---|---|---|---|---|
| 1 | Environmental permit writer (water/air/waste/wetlands) | State agency; local air district | Core delegated-program job; v1 applicant-side only | [E] SL-079, SL-073, SL-076 |
| 2 | Environmental compliance inspector | State; county | Modal state task; maps to 29 of 70 sampled classes via 6.1.2 | [E] SL-050, SL-078, SL-059 |
| 3 | Enforcement case manager | State | Distinct specialized role | [E] SL-072, SL-075, SL-069 |
| 4 | Drinking water program compliance analyst (primacy) | State | No v1 coverage; high public-health stakes | [E] SL-071 |
| 5 | Water/wastewater treatment operator (certified) | Municipal utility; special district | Largest local environmental workforce [J]; absent in v1 | [J] |
| 6 | Environmental health specialist / sanitarian | County/city health department; state | Credential-defined; absent in v1 | [E] SL-035, SL-052, SL-060 |
| 7 | Contaminated-site / remediation project manager | State; county | Standing state role; private consulting mirror | [E] SL-077, SL-082, SL-074 |
| 8 | Environmental review analyst (state acts and NEPA) | State agency; state DOT | Generalizes v1 6.1.4; dual-regime jobs | [E] SL-070, SL-038 |
| 9 | State natural resource specialist / land and forest manager (incl. GNA work) | State lands, forestry | v1 strength; federal-to-state corridor | [E] SL-040, SL-045, SL-051 |
| 10 | State fish and wildlife biologist | State F&W agency | v1 strength; direct federal counterpart (0401/0486 [J]) | [E] SL-056 |
| 11 | Air quality specialist (monitoring/testing/planning) | State; local air district | v1 has one competency | [E] SL-085, SL-050 |
| 12 | Solid waste and materials program specialist | State; county | v1 waste content is strategy, not regulation | [E] SL-059, SL-083 |

**Phase-2 candidates** (not MVP):
- Oil and gas environmental compliance (state-specific) [E: SL-080].
- Stormwater/MS4 coordinator [J].
- Municipal sustainability/environmental services specialist [E: SL-086].
- Climate policy analyst [E: SL-061].
- Vector control technician [E: SL-060].
- County conservation technician [E: SL-085].
- Environmental financial assistance (SRF) program manager [J].

---

## 10. Proposals

**P-SL-01 — Role variants plus jurisdiction overlay, not per-state roles.** Adopt the structure in §9 (SL-Q1). Put the state-class crosswalk record in L6 with the minimal common fields. *Change.* [E/J]

**P-SL-02 — Add an authority-position facet to role profiles** (regulator | operator | resource manager | applicant/regulated party | funder/grantor | advisor/researcher). It fixes v1's single-perspective S3 and pairs public and private mirror roles for mobility. *Add.* [E: SL-079, SL-050; J]

**P-SL-03 — Extend the work-function facet** with *inspect*, *enforce*, *operate*, *fund/assist* and *oversee delegated or local delivery*. This aligns with CA's proposed facet (assess → plan → authorize → implement/operate → monitor → enforce → learn → engage) and adds the two missing state functions, fund/assist and oversee. *Change.* [E: SL-085, SL-074; J]

**P-SL-04 — Adopt the 12-role state and local MVP set** (§9, SL-Q2), with LM sizing from ASPEP before final selection. *Add.* [E/J]

**P-SL-05 — Add candidate competencies SL-C01 to SL-C16** (`candidate_competencies.csv`). SL-C01 (delegated program administration), SL-C02 (permit writing as authority), SL-C03 (inspection), SL-C04 (enforcement cases), SL-C08 (environmental review under state acts) and SL-C16 (practice within licensure scope) are core or transversal. The rest go to subsector modules (water, environmental public health, waste and remediation, air, energy). *Add.* [E except SL-C05 and SL-C12, J]

**P-SL-06 — Replace the six federal reform flags with dated, jurisdiction-tagged driver events in L5.** Seed it with state events from this research: skills-based hiring orders and statutes (SL-L01), EO 2025-01, MEPA/CEQA-type amendments, WIOA and MASA milestones, and delegation or assumption changes. *Change.* [E: SL-010, SL-031, SL-005; J]

**P-SL-07 — Publish the Minimal Common Fields v0.1** as the state and local ingestion schema. IA formalizes it in JSON Schema; DE adds validation tests. *Add.* [E: §3; J]

**P-SL-08 — Build the federal-to-state environmental crosswalk first and validate it with Pennsylvania.** Seed gold sets from native crosswalks (Texas military crosswalk, New York 70.1, Minnesota equivalents, Pennsylvania federal equivalencies). Use AI matching with human review and published confidence. Offer it to states hiring displaced federal staff. It is the highest-value, lowest-friction first product. *Add.* [E: SL-031, SL-052, SL-062, SL-069; J]

**P-SL-09 — Pilot three contrasting state models plus local self-mapping.**
- Pennsylvania (equivalency order, GenAI, application-as-exam).
- Texas (decentralized plan with agency MQs and a statutory crosswalk).
- Washington (desirable qualifications, union shadow classes, annual revisions).
- One county environmental health department and one municipal utility, using role-variant self-mapping (pick a role and level, get a draft class description and MQs).

*Add.* [J]

**P-SL-10 — Map levels by supervisory status and autonomy first, years second.** Retire the tenure-band definition of v1 levels as the crosswalk key. *Change.* [E: SL-050, SL-071, SL-056]

**P-SL-11 — Make licensure a first-class entity** (credential, issuing jurisdiction, scope of practice, timing, reciprocity) linked to role variants. Show where skills-based substitution stops. *Add.* [E: SL-055, SL-054, SL-085, SL-035, SL-060]

**P-SL-12 — Record mobility frictions on role-variant pairs:** pay ratio by state, appointment-route gates, licensure reciprocity, pension portability, residency, bargaining-unit change. Hand to CM. *Add.* [E: SL-021, SL-036, SL-084; J]

**P-SL-13 — Design proficiency indicators for state assessment routes**: training-and-experience questionnaires (CA, PA), NY HELPS appointments and LEAP-style job examination periods. Hand to IO and LC. *Add.* [E: SL-032, SL-033, SL-080, SL-013]

**P-SL-14 — Use WIOA as a sector-strategy hook, not an HR hook.** Offer EMST utility and environmental-services role profiles to state boards for plan implementation and PY2028 plans. Don't make adoption contingent on reauthorization or MASA. *Add.* [E: SL-009, SL-005, SL-008]

**P-SL-15 — Measure pilot outcomes at hire and promotion level**, following Colorado's model, not postings. Hand to CM and AS. *Add.* [E: SL-014, SL-012]

**P-SL-16 — Retire the "Public Agencies" sector note** and replace it with federal, state, local and Tribal enactment notes only where performance differs. *Retire.* [E: SL-087]

---

## 11. Disagreements and trade-offs

1. **With v1's perspective.** v1 describes environmental management from the land manager's and applicant's chair. State and local workforces sit mostly in the regulator's, operator's and overseer's chairs. Adding regulator-side variants grows the role layer by roughly a third [S]. Not adding them makes EMST unusable for most state environmental-agency jobs. I think the growth is unavoidable.
2. **With a pure task-graph (Option B) user experience.** State HR analysts work in classes, MQs and substitution rules, not task graphs. I support CA's hybrid, but the state-facing view must be **class-shaped** (role variant, level, MQ draft, licensure). The CA's Option A note ("matches the language federal and state HR already uses") is right for presentation and wrong for the crosswalk engine, which needs tasks (§3.3).
3. **With an OPM-anchored role layer (likely FH position).** OPM series are being consolidated [CA audit, CA-044], and state classes do not align with OPM series: they are broader, and agency- and level-specific. Anchoring roles to OPM series would make state crosswalks second-class. The trade-off is that federal HR loses a familiar backbone. Function-defined roles with OPM and state crosswalks as peers in L6 are the better choice.
4. **With degree-removal enthusiasm.** Skills-based hiring stops at licensure boundaries (Minnesota's own order says so) [E: SL-015]. Posting-level change also overstates hiring change [E: SL-014]. EMST should not claim degree-free pathways where practice acts require education. The trade-off is less aspirational messaging in exchange for legal defensibility (IO's concern too).
5. **With LMPS as a state demand signal (LM).** OpenLMP is about 95% USFS western plans (per LM) and barely encodes GNA or shared stewardship [E: SL-090]. It should not stand in for state and local demand. State posting data and class specs should.
6. **Fidelity versus maintainability.** Position-level crosswalks are accurate but expensive. Class-level crosswalks are cheap but wrong for broad classes. My proposal is class-level with position overrides only in pilots and where the class is flagged broad. CA should decide.
7. **Self-mapping for local employers versus validated crosswalks.** Self-mapping scales to thousands of local employers but carries no validation. I accept that trade-off for local adoption and keep validated crosswalks for state systems.

---

## 12. Issues outside my area that affect the vision

- **Tribal programs under treatment-as-state** run the same regulator-side functions. TN should decide whether the "regulator" authority position applies to Tribal programs and how [J].
- **Privacy and public records (CP).** Class specs and postings are public. Incumbent payroll is public in some states (the Texas Tribune explorer [E: SL-057]) and protected in others. Position-level crosswalks may touch personnel records.
- **Federal funding volatility (FS, LM).** State environmental positions co-funded by federal program grants move with federal budgets [J]. This belongs in L5 as dated driver events and in foresight scenarios.
- **Credential pathways (LC).** Operator certification and REHS registration are credential-defined entry paths that run through community colleges and apprenticeships. LC should own the learning-path design.
- **Stewardship (AS).** Program associations (ASDWA, ACWA, NACAA, ASTSWMO, NEHA) are natural module stewards [J]. Their buy-in decides whether federated modules (Option C) work for state programs.
- **Labor relations (AS, CP).** Any reclassification recommendation will trigger bargaining obligations where bargaining exists [J]. EMST outputs should be framed as mapping and guidance, not mandates.

---

## 13. Open questions for the Chief Taxonomy Architect

1. Is **authority position** a facet on role variants (my proposal) or an L0 vocabulary applied to tasks? The answer affects how public–private mirror roles are computed.
2. Are **water and wastewater operations** and **environmental public health services** core or modules? If modules, who commissions them for the federal and state MVP, given stewards won't be ready in time?
3. What **crosswalk grain** for state systems: class-level only, or class-level plus position overrides in the pilot?
4. Where does **licensure** live: an L0 credential vocabulary, an L6 crosswalk target, or both?
5. Should **state HR events** (skills-based hiring orders, class-plan revisions, equivalency orders) count as L5 change signals that move a role's change indicator?
6. Will CA endorse a **federal-to-state environmental crosswalk** (P-SL-08) as the first shippable product, ahead of the broader role library?

---

## 14. Files in this folder

| File | Contents |
|---|---|
| `report.md` | This report |
| `sources.csv` | 91 sources (SL-001 to SL-091), with quality, status and reason chosen |
| `state_classification_sample.csv` | 70 state and local classes across 9 states plus 2 local governments, mapped to v1 codes (all codes validated against `data/v1_baseline/competencies.csv`) |
| `state_policy_levers.csv` | 29 levers (state, local, multi) with relevance to EMST |
| `mobility_map.csv` | 11 mobility instruments and bridges plus 10 barriers (extra file, for CM) |
| `minimal_common_fields.csv` | 28-field crosswalk ingestion spec with requirement level and observed availability (extra file, for IA and DE) |
| `candidate_competencies.csv` | 16 candidates (SL-C01 to SL-C16) |
| `role_signals.csv` | 13 role signals (SL-R01 to SL-R13) |
| `v1_assessment.csv` | 20 verdicts on v1 elements |
| `ecosystem.csv` | 33 entities (SL-E01 to SL-E33) |
| `scripts/sources.py`, `classes.py`, `levers.py`, `cands.py` | Deterministic builders that regenerate every CSV above from inline, source-cited data (run with `python3 -I`) |
| `scripts/validate.py` | Checks headers against TEAM_BRIEF §5 schemas, row widths, source-ID resolution, v1 code validity, controlled vocabularies, and that every [E] row cites a source. Current result: `OK: all SL CSVs valid` |

**Vocabulary note for `degree_required`:** required | substitutable (experience can replace the degree) | not-required | agency-set | per-recruitment | not-stated.

---

## 15. Verification queue (claims labelled [J] that need sources next session)

1. Water and wastewater operator certification: state programs, grades, reciprocity, the federal guideline basis for drinking water, and workforce or retirement data (EPA, ASDWA, AWWA, ABC).
2. Environmental health workforce size, REHS/RS coverage and shortage data (NEHA, NACCHO).
3. IPA (5 U.S.C. 3371–3376): usage counts in environmental agencies.
4. Good Neighbor Authority: number of agreements, state staff funded, and county and Tribal eligibility.
5. Wildland fire qualification portability across state, local and federal employers (NWCG position standards; FH and FC overlap).
6. Public pension portability and service-credit purchase rules for federal service, in sample states.
7. State public-sector bargaining law: which states prohibit or permit bargaining, and whether reclassification is a mandatory subject (sample states plus NC and VA).
8. 2025–26 status of AmeriCorps-funded and state climate and conservation corps.
9. EEO-4 reporting coverage for state and local governments; Census ASPEP function codes for environmental functions.
10. Montana and Florida: whether state job codes are SOC-based.
11. Section 404 assumed programs: current states.
12. Colorado, Oregon, North Carolina and Montana class specifications, to complete the planned 12-state sample.
