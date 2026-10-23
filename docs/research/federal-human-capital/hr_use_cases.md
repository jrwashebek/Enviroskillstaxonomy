# EMST for Federal HR: Five Workflows an HR Specialist Could Run Tomorrow

**Role:** Federal Human Capital & Classification Advisor (FH) · **Date:** 2026-10-23 · **Status:** Phase 2 draft for CA review
**Companion files:** `opm_series_register.csv`, `opm_series_to_emst_crosswalk.csv`, `report.md` (evidence and proposals), `sources.csv`
**Labels:** [E] evidence (source ID), [J] FH professional judgment, [S] speculation.

## How to read this

Each workflow is written the way a classifier, staffing specialist, HR business partner or supervisor would run it. Each one gives:

- the trigger, who runs it, and what goes in;
- the EMST fields it uses (v1 fields where they exist; **new** where v2 must add them);
- numbered steps and the outputs;
- the legal and policy guardrails;
- what EMST must contain for the workflow to work, stated as requirements (REQ-FH-nn).

The requirements are consolidated at the end so CA, IA and DE can trace them to schema decisions.

**One rule runs through all five workflows [J]: EMST informs HR decisions but never makes them.**

- **Classification:** series and grade are set by OPM standards under 5 U.S.C. chapter 51.
- **Qualifications:** eligibility is set by OPM qualification standards.
- **Assessment:** job-relatedness comes from a position-specific job analysis under 5 CFR 300.103 [E: FH-002, FH-023].

EMST is a structured, well-sourced starting inventory that makes each of those steps faster and more consistent. Any user interface or export must say so.

---

## (a) Writing or modernizing a position description (PD) and its major duties statement

**Trigger.** Any of the following:
- a vacancy approved by a Strategic Hiring Committee under EO 14356 [E: FH-029];
- a reorganization;
- an OPM series realignment under the April 2026 consolidation [E: FH-014];
- a supervisor reporting that the PD no longer describes the work (the v1 forester PD argument [FH-037]).

**Who.** The supervisor drafts. The HR classifier reviews, determines series, title and grade, and certifies. A program SME can contribute.

**Inputs.**
- The existing PD, if there is one.
- The OPM series definition and classification standard. EMST does not choose the series.
- Agency standard PDs, where they exist.
- The EMST series profile, which is the core and supporting competencies from the crosswalk.
- Exposure and change signals for the competencies' tasks.

**EMST fields used.**

| Field | Status |
|---|---|
| Competency title and description | v1 |
| Tasks T1–T3 | v1 |
| Intermediate and advanced indicators | v1 |
| Craft primary | v1 |
| Task 13 auto type and career-ladder tags | v1 |
| Series crosswalk (core/supporting) | **new** |
| Duty-statement templates per level | **new** |
| Factor 1 knowledge statements ("Knowledge of … sufficient to …") | **new** |
| Tools/standards layer: current methods and tools named separately from the durable competency | **new** |

**Steps.**
1. **Confirm the series first.** Use the OPM series definitions, not EMST. If the position mixes disciplines, consider an interdisciplinary PD, for example 0401/0408/0486. If the series is on the Phase One realignment list, note the successor series [E: FH-014].
2. **Pull the EMST series profile.** Start from the crosswalk rows for the series (core first). Remove what the position does not do. EMST profiles are series-typical, not position-specific.
3. **Map each current duty to EMST competencies and tasks.** This exposes duties with no competency behind them, and competencies the work now requires that the PD omits. Typical omissions in v1-derived examples:
   - remote-sensing verification;
   - validating AI-drafted analyses;
   - partner agreement management (FH-C02, FH-C05, FH-C15).
4. **Draft 3–6 major duties.** Each needs a percentage of time and duty statements in the form *action + object + purpose/standard*. Use the duty-statement template at the target proficiency level. Name tools and methods only as examples, so the PD does not go stale when tools change.
5. **Check grade-controlling duties.** In federal classification, the grade generally rests on duties performed a substantial share of the time on a regular and recurring basis; the common rule of thumb is at least 25% [J]. If AI or remote sensing compresses a duty that controls the grade, for example inventory or document production, **send it to the classifier before finalizing.** The grade or series may change. Do not assume time freed up is absorbed by higher-grade work [J; corrects FH-037].
6. **Draft Factor 1 (Knowledge Required).** Start from EMST knowledge statements at the target level, then edit to the language of the OPM standard. Factors 2–9 come from the standard and the classifier.
7. **Classify.** The classifier evaluates the PD against the OPM standard (FES factors or the job-family criteria) and documents the evaluation. EMST is not cited as the classification basis.
8. **Certify and file.** The supervisor and the classification official certify accuracy. Attach the EMST competency profile as a non-classification attachment. It becomes the seed for workflow (b).

**Outputs.**
- A classified PD.
- A position competency profile listing competencies, target levels, importance and a needed-at-entry flag.
- A change log showing which duties changed and why, which feeds L5 change signals.

**Guardrails.**
- Classification must follow OPM standards (5 U.S.C. 5106–5107; 5 CFR 511) [J].
- PDs must describe duties actually assigned. Do not inflate PDs to justify a grade [J].
- AI-assisted PD drafting is generally not high-impact when drafting "does not affect an individual's access to employment," provided the use is documented, human-reviewed and adopted [E: FH-015]. Keep the record.
- Changing PDs for bargaining-unit positions can trigger notice and bargaining obligations, which the series-consolidation memo also stresses [E: FH-014].
- Do not use EMST to designate or justify Schedule Policy/Career placement. That is a presidential/OPM determination with litigation pending [E: FH-021, FH-028].

**What EMST must contain.** REQ-FH-01, 02, 03, 04, 05, 06, 12.

---

## (b) Job analysis feeding SME-QA, USA Hire and other technical assessments under the Merit Hiring Plan (with IO)

**Trigger.** An approved vacancy in the competitive service. Every hiring process must include at least one technical or alternative assessment. Since 30 September 2025, self-assessment questionnaires may be used only for minimum qualifications and eligibility, not for rating and ranking [E: FH-002, FH-017].

**Context an HR specialist should know [E].**
- In FY2025, 91% of delegated examining announcements still relied only on self-report questionnaires [FH-017].
- As of FY2026 Q2, 34.3% of delegated examining announcements used technical or off-the-shelf assessments [FH-001].
- OPM's targets are 75% of positions in FY2026 and 100% by FY2027 or FY2028. OPM's own documents disagree on which year [FH-016, FH-001].
- Only 15% of agencies have I-O psychologists on staff [FH-017].
- USA Hire Standard batteries measure general competencies such as reading, reasoning, judgment, math reasoning and interaction competencies, by series and grade. In March 2026 they expanded to 412 series [E: FH-026, FH-001].
- **The gap for environmental series is the technical assessment. EMST should fill exactly that gap [J].**

**Who.**
- Staffing specialist or the agency talent team, which leads.
- 2–5 SMEs. The Chance to Compete Act defines an SME as someone who understands the duties and the KSAs [E: FH-023].
- The hiring manager.
- IO, for method and validation design. FH covers process integration.

**Inputs.**
- The classified PD and position competency profile from workflow (a).
- EMST task statements for those competencies.
- USA Hire coverage for the series and grade.
- OPM general competency definitions, and later the Federal Workforce Competency Initiative (FWCI) models [E: FH-017, FH-044].

**EMST fields used.**

| Field | Status |
|---|---|
| Tasks | v1 seed, expanded |
| Competency definitions | v1 |
| Intermediate/advanced indicators | v1, rewritten as behavioral anchors |
| Needed-at-entry flag | **new** |
| Distinguishing-competency flag (separates superior from adequate performers) | **new** |
| Proficiency benchmarks per grade band | **new** |
| Structured-interview question bank keyed to competency and level | **new** |
| Work-sample scenarios | **new**, optional |
| Map to USA Hire general competency names | **new** |

**Steps** (method detail is IO's lane; this is the HR sequence).
1. **Assemble a draft task inventory.** Combine PD duties with EMST tasks for the profile competencies, aiming for 15–40 tasks. Delete tasks the position does not perform.
2. **SME ratings.** SMEs rate each task for importance and frequency. They rate each competency for importance, needed at entry, and distinguishing. They link tasks to competencies. Document everything; this is the 5 CFR 300.103 job analysis record [E: FH-002].
3. **Select the critical competencies.** These are competencies that are important, needed at entry and linked to critical tasks. Typically 4–8.
4. **Allocate assessment methods by competency.**
   - **General competencies** (reading, reasoning, writing, interpersonal): use USA Hire where the series and grade are covered, to avoid duplication [E: FH-026].
   - **Technical competencies:** use SME-QA resume review against the EMST-derived benchmark for the target grade band, a structured interview built from EMST behavioral anchors, and/or a work sample. Examples of work samples:
     - interpret a stand-exam summary and draft a prescription rationale (0460);
     - review a discharge monitoring dataset for violations (0028);
     - QC a provisional streamflow record (1315).
   - **Credentials** such as NWCG qualifications for 0456 or FAC-COR: treat as minimum qualifications, selective factors or conditions of employment, not as ranking content [J].
5. **Set benchmarks and cut scores.** SMEs write "what qualified looks like at GS-X" from EMST anchors, edited to the position. Set minimum passing scores, as the Merit Hiring Plan requires agencies to do [E: FH-012].
6. **Build the announcement.** Specialized experience language comes from the benchmark. Keep the Merit Hiring Plan essay questions separate from technical assessment content. Essay Question 3 was stayed in *AFGE v. Kupor* on 11 September 2026 and replaced. A new Question 5 tied to agency priorities is due by 2 November 2026 [E: FH-032].
7. **After the hire, record outcomes.** Log assessments used, pass rates, adverse-impact checks and hiring-manager satisfaction. These are EMST validation evidence, and they are also the Chance to Compete metrics OPM tracks [E: FH-017, FH-027].

**Outputs.**
- A job analysis record.
- A crediting plan or SME-QA benchmark.
- A structured interview guide.
- An optional work sample.
- An assessment plan showing which competency is measured by which method.

**Guardrails.**
- A technical assessment must be "position-specific," "based upon a job analysis," and must not "solely or principally rely on" self-assessment [E: FH-023]. **An EMST profile is not a job analysis.** SMEs must adapt and rate it for the position.
- Follow the Uniform Guidelines on Employee Selection Procedures and validation evidence requirements (IO lane) [J].
- Veterans' preference and rule-of-many category rating apply [E: FH-012].
- If AI helps write questions or summarize resumes, it remains subject to job-analysis and validation requirements. Any flag that removes a candidate must be verified against source documents [E: FH-015].
- Shared certificates now let other agencies reuse a certificate without reassessing for rating and ranking. That raises the value of common EMST-based benchmarks across bureaus [E: FH-013].

**What EMST must contain.** REQ-FH-02, 05, 06, 07, 08, 09, 10, 12.

---

## (c) Skills-gap analysis for a work unit, and Individual Development Plans

**Trigger.**
- Annual workforce or training planning.
- After separations. Many units lost a quarter of staff in 2025; the Forest Service and the National Park Service each lost more than 25% from September 2024 to January 2026 [E: FH-008].
- After a reorganization or a new mission requirement, for example a land management plan's monitoring requirements (from OpenLMP, LM lane).

**Who.**
- First-line supervisor, who leads.
- Employees, through self-assessment for development only.
- Training officer or HR business partner.
- LC, for learning resources.

**Inputs.**
- Unit roster with series and grade.
- Position competency profiles from workflow (a), or EMST series profiles as defaults.
- Mission requirements.
- Training catalogs: NCTC, DOI University, OPM supervisory and leader development programs [E: FH-046].

**EMST fields used.**

| Field | Status |
|---|---|
| Proficiency levels and anchors | v1, rewritten |
| Default target level by grade band | **new** |
| Tacit density | v1 |
| Career-ladder position | v1 |
| Exposure and CLD flags | v1 |
| Typical time to proficiency | **new** |
| Development-method tags (course / OJT / task book / mentoring / detail) | **new** |
| Links to learning resources | **new**, LC |

**Steps.**
1. **Set the target profile for each position.** List the core competencies at the default target level for the grade band, adjusted by the supervisor.
2. **Assess current proficiency.** The employee self-rates and the supervisor rates against behavioral anchors, with examples as evidence. For development, self-assessment is acceptable. It is not acceptable for hiring.
3. **Aggregate unit gaps.** Weight them by mission criticality and by single-point-of-failure risk, meaning a competency held at the target level by one person or nobody.
4. **Choose development methods by competency type.**
   - High-tacit competencies (v1 tacit density "Hi") need mentoring, details and task books, not courses [J].
   - Competencies whose entry tasks are compressing (v1 CLD flag) need deliberately designed field experiences (FH-C06).
5. **Write IDPs.** Each IDP has 2–4 competencies, methods, dates and the evidence that will show progress.
6. **Review quarterly and roll up.** Unit gaps feed workflow (d) and the agency training plan.

**Outputs.** A unit gap heat map by competency and level, IDPs, and training requests.

**Guardrails.**
- Training authority is 5 U.S.C. chapter 41 and 5 CFR 410 [J].
- Keep development assessments separate from performance appraisal. The new appraisal rules and the FY2026 forced-distribution guidance make any leakage high-stakes [E: FH-045 titles].
- Competency ratings retrieved by employee name are likely a Privacy Act system of records and may need a SORN. Report at unit level by default (CP lane) [J].
- Consult unions where required [J].
- Do not use gap scores for RIF retention, which follows statute and regulation (see d).

**What EMST must contain.** REQ-FH-04, 07, 11, 13, 14, 15.

---

## (d) Workforce planning under contraction and reorganization: critical skills, retention and knowledge transfer

**Trigger.**
- Annual Staffing Plans and quarterly updates under EO 14356, which began in Q2 FY2026. OPM issued staffing plan guidance on 30 July 2026 [E: FH-029, FH-045].
- RIF planning under the final RIF regulations of 2 September 2026 [E: FH-045, title only].
- Bureau consolidations, for example DOI's phased consolidation of wildland fire programs [E: FH-035].

**Context [E].**
- About 317,000 departures in 2025: deferred resignation program about 144k, early retirement or buyouts about 21k, routine attrition about 129k, involuntary separations about 24k [FH-030].
- Hires totalled about 68k by the end of August 2025 [FH-030].
- The under-30 share fell to 7.9% while the share aged 50 or over rose to about 40% [FH-008].
- Strategic Hiring Committees approve every vacancy [FH-029].
- **Every hire now needs a competency-gap argument.**

**Who.** HR strategic workforce planner, program managers, and the CHCO staff who prepare staffing plans.

**Inputs.**
- Federal Workforce Data (data.opm.gov) headcounts, separations and retirement eligibility by series, grade and organization [E: FH-010].
- Mission and statutory requirements, including plan-required monitoring, consultation and permits.
- Position competency profiles.
- EMST exposure data.

**EMST fields used.**

| Field | Status |
|---|---|
| Series register (incl. consolidation status) | **new** |
| Series → competency crosswalk | **new** |
| Tacit density and career-ladder position | v1 |
| Exposure type per task | v1 |
| CLD flag and severity | v1 |
| Critical-function tags tied to statutory or plan requirements | **new** |
| Time to proficiency | **new** |
| Candidate knowledge-transfer method per competency | **new** |

**Steps.**
1. **Map mission to functions to competencies.** For each statutory or plan-required function, for example ESA consultation, permit administration, BAER and inventory, list the EMST competencies required and the minimum bench strength.
2. **Overlay supply.** Count who holds each competency at the target level, by unit, with retirement eligibility. Flag single-incumbent and retirement-eligible holders.
3. **Score risk.** Risk equals criticality × scarcity × time to proficiency × tacit density. High-tacit, long-time-to-proficiency competencies held by retirement-eligible staff come first.
4. **Choose a response for each risk.**
   - retention incentive (5 CFR 575);
   - knowledge capture (FH-C07);
   - detail or cross-training;
   - partner or contract delivery, which is now explicit Forest Service practice [E: FH-018];
   - hire.
5. **Write the staffing plan justification.** For each requested hire, cite the function, the competency gap and the risk score. This is the evidence a Strategic Hiring Committee can act on (FH-C14).
6. **Track entry pipelines.** Use EMST CLD and P-position exposure to show where entry-level work is disappearing. Example: v1 tags code 6 of 7 entry tasks under 0028 core competencies as compressive, substitution or supervision [J, derived from FH-038]. Plan deliberate developmental assignments so the agency does not hire only at the journey level.

**Outputs.**
- A critical-skills risk register.
- Staffing plan justifications.
- A knowledge-transfer plan.
- An entry-pipeline plan.

**Guardrails.**
- RIF retention order and competitive levels are set by statute and 5 CFR 351 (as revised in 2026), not by competency scores. Competitive levels are built from position descriptions, series and grade [J].
- EMST may support placement analysis but must not rank people for separation.
- Collective bargaining duties apply to RIFs and reorganizations [E: FH-011 memo titles].
- Note pending legislation such as the proposed Public Lands Workforce Stability Act RIF moratorium [E: FH-020].

**What EMST must contain.** REQ-FH-01, 11, 13, 15, 16, 17, 18.

---

## (e) Reskilling displaced or surplus staff into adjacent series

**Trigger.**
- RIF notices.
- Abolished organizations.
- Series realignment.
- Voluntary career moves into growth areas, for example wildland fire management, whose headcount grew while others shrank [E: FH-008].

**Who.**
- The employee, with the HR career-transition specialist.
- The receiving supervisor.
- CM, for transferability metrics.
- LC, for bridge learning.

**Inputs.**
- The employee's PD and competency profile.
- Target series profiles.
- The series register's positive-education flags.
- Career Transition Assistance Plan (CTAP) and Interagency Career Transition Assistance Plan (ICTAP) eligibility.
- OPM-led pooled hiring and shared certificates [E: FH-013].

**EMST fields used.**

| Field | Status |
|---|---|
| Series crosswalk | **new** |
| Competency overlap and transfer distance between profiles | computed; CM lane |
| Positive-education flag and coursework requirements | **new** |
| Bridge-competency sets per series pair | **new** |
| Learning resources | **new** |

**Steps.**
1. **Find adjacent series with real overlap.** Compare the current and target core competency sets. Examples from the crosswalk [J]:
   - 0462 to 0456: fire core overlaps and there is no positive-education barrier.
   - 0401, 0482 or 0486 to 0028: NEPA, permitting and compliance core overlaps, and 0028 has no positive-education requirement.
   - 1315 to 1560: the data core overlaps, but an education requirement or approved combination applies.
   - 0457 to 0401/0454: conservation planning and range work overlap.
2. **Check qualification barriers first.** Positive education requirements cannot be waived by competency evidence. Examples: 0460 requires a forestry degree or 24 semester hours; 1315 and 1560 have degree requirements. Verify against the current IOR (FH-042), because the series register flags are unverified this session.
3. **Size the gap.** List the target core competencies the employee lacks, at the required level, with time to proficiency.
4. **Choose the authority and route.**
   - reassignment or change to lower grade within the agency;
   - CTAP or ICTAP selection priority, which requires a well-qualified determination under the qualification standard;
   - OPM-led pooled hiring;
   - upward mobility or training agreements under 5 U.S.C. chapter 41.
5. **Build the bridge plan.** Combine coursework where an education requirement applies (LC), developmental details and task books, and a dated readiness check.
6. **Record the move.** Origin and destination series, competencies bridged and time to placement are the mobility evidence CM needs to test the theory of change.

**Outputs.** A ranked list of feasible target series, a bridge plan, and a placement record.

**Guardrails.**
- Qualification standards, positive education requirements, veterans' preference and CTAP/ICTAP order of selection are binding [J].
- Competency overlap supports a placement case. It does not create eligibility.
- Moves into federal service from state or other sectors raise different rules (SL and CM lanes).

**What EMST must contain.** REQ-FH-01, 02, 07, 16, 19, 20.

---

## Consolidated requirements: what EMST v2 must contain for federal HR use

| ID | Requirement | Why (workflow) | v1 status |
|---|---|---|---|
| REQ-FH-01 | **Versioned OPM series register.** Code, title, group, status (active / proposed realignment / realigned-to), effective date, successor series. | a, d, e | absent |
| REQ-FH-02 | **Series → competency crosswalk.** Core/supporting, basis, confidence, date; keyed to series version. | a, b, e | absent (family→SOC only) |
| REQ-FH-03 | **Duty-statement templates per competency and level** (action + object + purpose), tool-neutral. | a | absent; v1 tasks partial |
| REQ-FH-04 | **Level definitions by independence, complexity and scope** (not years), with an indicative GS grade-band map labelled "not a classification criterion". | a, b, c | tenure bands |
| REQ-FH-05 | **Factor 1-style knowledge statements** ("Knowledge of X sufficient to Y"). | a, b | absent |
| REQ-FH-06 | **Tools/standards layer** separate from competencies, so PDs and assessments name current tools as examples. | a, b | tools embedded in 27+ competencies |
| REQ-FH-07 | **Behavioral anchors at each level** usable as SME-QA benchmarks and structured-interview rating scales. No reputational indicators. | b, c, e | Intermediate good; Advanced/Expert weak (38.4% of Expert indicators reputational) |
| REQ-FH-08 | **Needed-at-entry and distinguishing flags** per competency within a role profile. | b | absent |
| REQ-FH-09 | **General vs technical typing.** General competencies mapped to OPM general competency names and USA Hire coverage. | b | mixed |
| REQ-FH-10 | **Assessment-method suggestions** per competency: work-sample prompts and structured-interview questions, IO-reviewed. | b | absent |
| REQ-FH-11 | **Typical time to proficiency** and **development-method tags**. | c, d | absent; tacit density exists |
| REQ-FH-12 | **Provenance and disclaimers on every export.** Source, version, evidence label, "not a job analysis / not a classification basis". | a, b | absent |
| REQ-FH-13 | **Default role profiles per series × grade band** (L3), function-defined, with sector-actor variants. | c, d | absent |
| REQ-FH-14 | **Learning-resource links** (NCTC, DOI University, OPM programs, academic). | c | absent (LC) |
| REQ-FH-15 | **Privacy-safe aggregation design.** Unit-level by default; individual records only in agency systems. | c, d | n/a (CP) |
| REQ-FH-16 | **Positive-education and credential flags per series**, with coursework detail. | d, e | absent |
| REQ-FH-17 | **Critical-function tags** linking competencies to statutory and plan requirements (OpenLMP). | d | absent |
| REQ-FH-18 | **Exposure and CLD tags** carried as attributed, dated assessments. | c, d | present (single analyst) |
| REQ-FH-19 | **Computed transfer distance** between role profiles, with qualification barriers shown separately from competency overlap. | e | absent (CM) |
| REQ-FH-20 | **Bridge-competency sets** for priority series pairs (0462→0456, 0401→0028, 1315→1560, 0457→0401). | e | absent |

**Minimum viable federal package [J].** REQ-FH-01, 02, 04, 07, 08, 12 and 13 for the 13 crosswalked series. That is enough to run workflows (a) and (b) in a pilot with one land-management talent team. The rest can follow.
