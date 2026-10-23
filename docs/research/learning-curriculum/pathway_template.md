# EMST Learning Pathway Template (v0.1, draft for Phase 3)

**Owner:** Learning & Curriculum Design Strategist (LC) · **Date:** 2026-10-23 · **Status:** draft. Assessment rules are co-owned with IO (job analysis and validation). Credential data fields are co-owned with IA (interoperability). Evidence labels: [E] evidence (source IDs in `sources.csv`), [J] judgment, [S] speculation.

A **pathway** is a reusable plan for moving a defined group of people from a verified current profile to a target role profile. It states the competency-levels to reach, the learning outcomes, the learning modes, the assessments, the recognition earned, and the time and cost. The template serves three types of user:

- **Learners and supervisors** read the header, the target profile, the gap and the credential.
- **Instructors and training officers** use the outcomes, modes, assessments and sequence.
- **Program and HR leads** use the alignment, duration, cost and evaluation sections.

The six worked examples in `example_pathways.md` use this template. A pathway must not change the taxonomy. When a pathway needs an outcome that no EMST indicator supports, it raises a change request (rule R3).

---

## 1. The unit of design: the competency-level outcome (CLO)

The atomic unit is **one EMST competency at one target level** (for example `7.2.1@Intermediate`). Each CLO carries the following:

| Field | Content | Source |
|---|---|---|
| `clo_id` | `<competency_id>@<level>` (v1 code now; v2 persistent ID later) | EMST |
| `level_descriptor` | The generic level text (§2) | EMST L0 scale |
| `outcomes[]` | 2–5 learning outcomes written by rule R2 | Derived from EMST indicators |
| `indicator_refs[]` | EMST indicator IDs each outcome rests on (e.g. `v1:7.2.1:intermediate:I2`) | EMST |
| `assessment_context` | `field` · `desk-data` · `stakeholder` · `legal-administrative` · `incident` (one or more) | Craft and task tags |
| `formation_flag` | true when any linked task is a formation task (§7) | v1 Task 13 tags |
| `typical_hours` | Learning hours to move one level, stated as a range | Pathway authors; calibrated by pilot |

**Why this grain** [J]:
- Accreditors already work at this grain. SAF states each minimum competency as one capability at one depth ("knowledge of", "an understanding of", "an ability to") [E: LC-001, Criterion IV]. Programs then map courses to those statements on an Introduce/Reinforce/Emphasize-Apply scale [E: LC-001, Section III Education Summary].
- Course syllabi state learning outcomes per course [E: LC-001 C4-2].
- A whole competency is too coarse to assess. An indicator is too fine to credential. One competency at one level is the smallest unit that is both assessable and meaningful to a learner.

---

## 2. Level descriptors (decoupled from years)

v1 defines levels by years in practice (0–2, 3–5, 6–10, 10+). This is unworkable for competency-based learning: a reskilling learner can reach Intermediate on a competency in months, and a 15-year veteran can still be Foundational in a new one [J; also LC-050 §4.3]. The template uses responsibility-based descriptors, following the pattern of the EQF's knowledge, skills and autonomy descriptors [S: LC-048 not re-read this session]. IO owns validation of these descriptors and the number of levels (CA DP-4).

| Level | Descriptor used for outcome writing | Typical time in practice (note only) | Is it a training target? |
|---|---|---|---|
| **Foundational** | Performs defined tasks using established protocols under guidance. Recognizes when a case falls outside the protocol and escalates it. | 0–2 years | Yes |
| **Intermediate** | Performs independently across normal variation. Selects methods. Documents the basis for decisions. Troubleshoots. Explains limits of the method to others. | 3–5 years | Yes |
| **Advanced** | Handles novel, complex or high-consequence cases. Designs or adapts methods and protocols. Evaluates and develops others' work. Accountable at program level. | 6–10 years | Yes, through work-based projects. Not through courses alone. |
| **Expert** | Sets standards for an organization or the sector. Others rely on the person's judgment. | 10+ years | **No.** Recognized through evidence (portfolio, peer review). Never taught as a course. |

---

## 3. Pathway record (fields)

```yaml
pathway_id: LC-PW-NN              # stable; versioned (semver) when content changes
title: "<verb-led, role-named title>"
pathway_type: new-hire | upskill | reskill | cross-sector | baseline
emst_version: "v1 (codes) -> v2 IDs at migration"
sector_actors: [federal, state, local, tribal, ngo, private, academic]
target_role:
  title: "<function-defined role, not an org-chart title>"
  soc_2018: ["19-2041"]            # crosswalk layer, versioned
  public_classification: "<OPM series / state class (FH, SL own); optional>"
  role_profile_ref: "<CA L3 role profile ID when it exists>"
entry_profile:
  assumed: [{clo: "1.2.4@Foundational", basis: "degree in CIP 03.0104"}]
  diagnostics: "<how current levels are verified: self-assessment + supervisor + evidence>"
target_profile:                    # what the role requires at the end of the pathway
  - {clo: "6.1.2@Intermediate", criticality: required, demand_source: "<PD / posting / plan component / regulation>"}
gap: computed = target_profile - verified_current   # only the gap is taught (R1)
outcomes:                          # per CLO in the gap (R2, R3)
  - {clo: "...", lo_id: "LO-01", text: "...", indicator_refs: [...], verb_band: apply}
modes:                             # per outcome; hours by mode (section 5)
assessment_plan:                   # per outcome; method, context, evaluator, standard (R4, R5)
sequence:                          # modules, prerequisites, gates (R9)
recognition:
  rpl_methods: [...]               # (R10)
  credential: {name, level, bundle_of: [clo...], standard: "Open Badges 3.0 / CLR 2.0", alignment: "EMST URIs", currency: "<refresh interval> (R11)"}
  external_credentials: [...]      # earned or accepted
duration_cost:
  hours_by_mode: {...}
  calendar: "<weeks/months>"
  cost_signal: "<range + basis>"
  funding: ["agency training budget", "WIOA", "Workforce Pell", "Registered Apprenticeship", "grant"]
exposure_design_notes: "<how Task 13 tags shaped the design (R6, R7)>"
equity_access_sovereignty: "<paid placements, travel, accessibility, Tribal data/knowledge rules>"
evaluation: {metrics: [...], data_owner: "...", review_date: "..."}
provenance: {authors, sources, decisions, change_log}
```

---

## 4. Rules

**R1 Teach the gap only.**
- A pathway covers `target − verified current`, never a whole family.
- Example: CM's family-pair analysis lists 23 F7 core competencies that an F1 forester lacks [E: LC-037]. A reskilling pathway into a remote-sensing role needs a small subset of those, at specific levels. That subset is a **role-profile delta**, not a family delta. [J]

**R2 Write outcomes by formula.** Each outcome reads: *Given* [condition: data, tools, setting, level of support], *the learner* [one observable verb from the level's verb band] [object taken from the competency] [to a criterion: protocol, accuracy, standard, legal requirement].

| Level | Verb band (choose one) | Never use |
|---|---|---|
| Foundational | identify, record, measure, follow (protocol), explain, flag/escalate, perform under guidance | understands, knows, is aware of, appreciates |
| Intermediate | conduct independently, select, analyze, troubleshoot, interpret, document the basis for, compare, prepare | is proficient in, is familiar with |
| Advanced | design, adapt, evaluate (others' work), lead (a defined effort), advise, defend | is expert in, shapes, is recognized |

- Knowledge statements become *explain / justify* outcomes, assessed by constructed response.
- The verb bands follow the revised Bloom taxonomy [S: LC-047, not re-read]. They also mirror SAF's tiers: "knowledge of" maps to Foundational explain/identify; "an ability to" maps to Intermediate or above [E: LC-001].

**R3 Trace every outcome.**
- Each outcome cites at least one EMST indicator ID.
- If none fits, the author files a taxonomy change request; the pathway does not invent competencies.
- This is the feedback loop from learning back to the taxonomy. [J]

**R4 Align assessment with performance.**
- Every Intermediate or Advanced outcome needs at least one performance method (WS, OBS, SIM or POR in §6).
- Selected-response items alone can certify only Foundational *explain/identify* outcomes. [J; IO to set standards]

**R5 Code the context.** The craft of the linked task sets where the outcome is assessed:
- Fieldcraft (FC) outcomes are assessed at least once in the field.
- Statecraft (SC) outcomes are assessed in a live or simulated stakeholder or legal-administrative setting.
- Datacraft (DC) outcomes are assessed on real or realistic data, and the learner produces a reproducible artifact.

The pattern follows NWCG task books, where tasks coded for a wildfire must be evaluated on a wildfire [J: LC-033 secondary description of PMS 311-series task books; LC-044 not read directly].

**R6 Craft balance ("no pixel without plot; no model without a decision owner").**
- Any pathway in which most hours are DC or AI-related includes at least one FC ground-truth activity and one SC accountability activity (a decision memo, briefing or defense).
- Basis: SAF already requires graduates to recognize when results from an application fall outside a reasonable range [E: LC-001 Forestry C4-B.2; Forest Technology C4-B.6]. That recognition depends on having seen the real thing. [J]

**R7 Protect formation (CLD response).** A **formation task** is a v1 task with career-ladder position P (entry), tacit density Hi or Med, and either automation type H or a formation role. For pathways that include formation tasks:
- **(a) Supervised repetitions.** Include a stated number of supervised repetitions of the task performed *without* AI or automation before AI-assisted performance is credited.
- **(b) By-hand quota.** Where the task is assessed Ac, V or S (being compressed or substituted), require a by-hand quota. The learner produces N unaided products, such as drafts, classifications or QC passes, before moving to a review-and-certify role. N is set so the learner can recognize the tool's characteristic errors.
- **(c) WBL share.** The share of learning hours spent in work-based learning scales with tacit density: Hi ≥ 50%, Med ≥ 30%, Lo has no minimum.

All three thresholds are [J]. They are to be tested in pilot. The direction is supported by v1's structural analysis [J: LC-034] and by recalled experimental evidence that unguarded generative-AI help can raise practice scores while lowering unassisted performance [S until re-read: LC-042].

**R8 Keep tools in their layer.**
- Tool training (named software, instruments, vendor platforms) appears as separate modules tagged `tool:<name>@<version>` with an expiry date.
- Competency credit requires either a tool-agnostic assessment or demonstrated transfer to a second tool where feasible.
- Basis: SAF's guidance expects graduates to know what technologies exist and to judge outputs; it does not require any particular product [E: LC-001 C4-B.2 guidance]. CA's R-4 requirement points the same way [E: LC-051].

**R9 Sequence.**
- Within a competency-level, explain before apply.
- Foundational data quality (2.2.3) comes before AI validation (7.2.1 and 7.2.3).
- Each module ends with spaced retrieval practice.
- Every pathway longer than 40 hours ends with an integrative capstone. The capstone uses at least 3 CLOs across at least 2 crafts in a real work product.
- SAF requires courses to be "sequentially integrated" [E: LC-001 C4-4]. Pathways follow the same rule. [J]

**R10 Recognize prior learning.**
- Accepted evidence: an existing credential or qualification listed in the evidence-equivalence register (P-LC-07); a portfolio of work products; a challenge assessment (the pathway's own performance assessment taken directly); or supervisor attestation backed by an observed task.
- Evidence is accepted per CLO, with a currency limit (default 5 years; 2 years for emerging competencies).
- Hook: SAF lets programs grant transfer credit for work or life experience when faculty judge it equivalent to course outcomes [E: LC-001 C2-6, Section III]. Evidence that PLA improves completion exists outside this sector [S: LC-046 not re-read].

**R11 Credentials at bundle grain.**
- Issue credentials for **bundles** of 3–8 CLOs that together make one work function. Examples: "Field-to-pixel inventory calibration", "AI-assisted environmental review: validation". Do not issue one credential per CLO.
- Each credential carries the EMST IDs and version, the evidence type and the assessment context, and uses Open Badges 3.0 / CLR 2.0 [E: LC-016, LC-015].
- Currency follows the competency's computed change velocity or lifecycle status (Emergent: 2 years; Transition: 3 years; Stable: 5 years), with a short refresh module rather than full retake. [J]
- Rationale: the US already has 1,850,034 distinct credentials, 1,022,028 of them badges [E: LC-017]. Per-CLO badges would add noise. Bundles match how employers read capability and can stack into certificates. Stacking shows modest positive returns in community-college data (about 4 percentage points employment, about 4% wages) [E: LC-018; not environmental-specific].

**R12 Use more than one sector actor.** For competencies CM identifies as bridges, at least one activity uses a second sector actor's context. Example: a federal learner also works a state or consulting case. v1 sector-application notes are the seed for these cases [E: LC-037, LC-031].

**R13 Evaluate.** Every pathway reports:
- outcome attainment (pass rates by outcome)
- time-to-proficiency
- 90-day transfer (the supervisor observes the outcome on the job)
- credential uptake and portability (accepted by a second employer)
- completion by subgroup

CM defines the mobility metrics these feed [J].

**R14 Version.**
- Each pathway pins an EMST version.
- When v2 IDs replace v1 codes, a migration table maps every `clo_id`.
- Outcome text changes increment the pathway version, and issued credentials keep the version they were issued under. [J]

---

## 5. Learning-mode codes

| Code | Mode | Best for | Notes |
|---|---|---|---|
| CL | Live instruction (in person or virtual) | Explain/identify outcomes; norms; case discussion | |
| OL | Online self-paced | Knowledge; tool modules (R8) | Cheapest; weakest for transfer [J] |
| FD | Field practicum | FC outcomes; calibration | SAF requires field exercises [E: LC-001 C4-1]. EHAC requires at least 180 practicum hours [E: LC-005] |
| WBL | Work-based learning: details, rotations, apprenticeship on-the-job learning, task-book assignments | Intermediate and Advanced outcomes; formation tasks | Registered Apprenticeship and Workforce Pell can co-fund (RA providers up to 49% of an eligible program) [E: LC-020] |
| SIM | Simulation: tabletop, sand table, scenario, VR/digital twin | High-consequence SC and FC decisions; incident and briefing practice | v1 sources see immersive simulation as a training accelerant [J: LC-033]. Meta-analytic support for simulation-based learning [S: LC-043 not re-read] |
| AIP | AI-assisted practice: tutor, adaptive drills, seeded-error validation drills | Knowledge retrieval; validation skill (7.2.x) | Guardrails required (R7). Evidence is mixed and setting-specific [S: LC-041, LC-042 not re-read] |
| MEN | Mentoring (structured) | Tacit transmission; formation | Needs qualified mentors (candidate LC-C-02) |
| COP | Community of practice | Advanced; currency | |
| CAP | Capstone or work project | Integration (R9) | |

## 6. Assessment-method codes (with IO)

| Code | Method | Use | Evaluator |
|---|---|---|---|
| SR | Selected response | Foundational knowledge only | Automated |
| CR | Constructed response (explain, justify) | Knowledge; reasoning | Rubric-trained grader |
| WS | Work sample (product judged against a standard) | DC and SC products (analysis, memo, map, permit draft) | Qualified reviewer |
| OBS | Observed performance in context (task-book style) | FC and incident tasks; inspections | Qualified evaluator with sign-off (R5) |
| SIM-P | Performance in simulation | High-stakes decisions; public meetings; briefings | Two raters |
| POR | Portfolio with reflective rationale | Advanced; RPL | Panel |
| ORAL | Structured oral defense | Defending alternatives (SAF Forestry C4-D.8) | Panel |
| VAL | Seeded-error validation drill (learner reviews AI or tool output containing known errors) | 7.2.1, 7.2.3, 2.2.3 | Automated scoring of detections plus reviewer check of the documented rationale |

IO sets reliability and validity standards. LC proposes that a pathway used **for training only** may use these methods with rubric calibration. Any use **for selection or promotion** requires IO's validity evidence first [J].

## 7. Exposure-informed design (how v1 analytical layers are used)

| v1 tag on a linked task | Design response |
|---|---|
| H (human-essential), tacit Hi | WBL or FD with OBS assessment. AIP only for knowledge support |
| A (augmentation) | Teach the augmented workflow. Assess with the tool *and* with a VAL drill |
| Ac (compressive augmentation) or V | By-hand quota (R7b), then review-and-certify outcomes. Credit judgment, not throughput |
| S (substitution) | Teach the oversight and exception-handling role. Remove repetitive practice beyond the quota |
| Career ladder P + CLD flag | Formation task: supervised repetitions (R7a). Supervisor plan required (7.2.2) |
| Emergent lifecycle status | Short currency (R11); refresh module scheduled |

These tags come from a single analyst and have not been checked for inter-rater reliability [E: LC-050 §10]. Until IO's reliability study is done, pathways treat them as design prompts, not as rules that bind funding. [J]

## 8. Minimum documentation for a pathway to be published in the registry

1. Every field in §3 is completed. Every outcome traces to an indicator (R3).
2. Every Intermediate or higher outcome has a performance assessment and a context code (R4, R5).
3. Formation tasks are identified and R7 is applied, or a written justification explains why not.
4. Duration and cost signals are stated as ranges with their basis, and each is labeled [E], [J] or [S].
5. Equity and access review is complete:
   - field placements are paid or stipended where possible;
   - travel and equipment costs are listed;
   - Section 508/WCAG applies to digital content (CP lane);
   - no Indigenous knowledge or Tribal data is used without the consent protocol set by TN.
6. Evaluation metrics and data owner are named (R13).
