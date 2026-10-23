# Instrument: Matrix-sampled job-analysis survey for the first function clusters (JAS)

**WP-11 output 7** · Owner: IO (A8); FH and SL (federal and state design partners, frames, benchmarks), PS (private frames), CM (mover sub-sample), CP (approvals, privacy, platform), DE (forms, data) · Status: draft instrument for CA approval; cognitive pretest required before fielding (`protocol_cognitive_interviews.md`, M3) · Date: 2026-10-23
**Decision basis:** ADR-0024 §1, §3, §7, §8 (tasks first; ≤ ~80 tasks per respondent; importance, frequency, consequence of error, needed at entry, AI mode), §9 (first clusters); ADR-0004 §3 (PR-1 existence rule: ≥ 20% of incumbents at that level rate it important or above); SPEC §5.7 (`taskBundle` fields), §8.2; 5 CFR 300.103 as amended Jul 31 2026 (federal employment practices rest on a job analysis) [E: V4 IO-022]; Chance to Compete Act, 5 U.S.C. 3304(a)(9) (a technical assessment "is based upon a job analysis") [E: IO-031, text read via govinfo, `validation/sources.csv` IO-111].
**Labels:** [E] evidence, [J] judgment, [S] speculation.

> **What this survey is and is not.** It gives function-cluster task and competency data across sector actors. That supports EMST's `describe` and `develop` uses, and it **speeds up** an employer's own job analysis. It is **not** a job analysis of any particular employer's position. Selection use needs the employer's own confirmation, linkage, standardized scoring and standard-setting (ADR-0024 §1, §3). Every report from it carries that statement.

---

## 1. Clusters, roles and task pools (ADR-0024 §9)

| Cluster | Role profiles (mvp_role_set.csv) | Primary craft focus | Pool source |
|---|---|---|---|
| JAS-1 Field monitoring and inventory | R02 field resource technician; R03 monitoring and data technician | FC | P1 task bundles (WP-08) |
| JAS-2 Regulatory compliance, permitting and environmental review | R10 environmental review specialist; R11 environmental permit writer; R12 environmental compliance inspector | SC | P1 task bundles |
| JAS-3 Geospatial and data analysis | R04 geospatial and remote sensing analyst | DC | P1 task bundles |
| JAS-4 Water quality and drinking-water/wastewater operations | R11 (NPDES-type variant); R24 drinking water programme analyst; R25 water and wastewater treatment operator | FC, SC (non-forestry coverage test) | P1/P2 bundles; `water` and `waterq` module tasks |
| JAS-5 Natural-resources Job-Analysis Starter Pack | R09 restoration project lead; R13 resource programme manager (federal 0401/0404-type variants) | mixed | P1 bundles; AS/FH Starter Pack |

**Task pool per cluster** is the union of the cluster's role bundles: v2 task statements at `status ≥ draft`, hash-pinned, lint-clean and passing ADR-0003 G-2. Expected 60–180 tasks [J]. Held content is excluded (ADR-0007).
**Competency list per cluster** is ≤ 25 competencies linked from the pool's tasks, plus the TX-A floor competencies.

## 2. Matrix-sampling design

- **Anchor block (all respondents):**
  - 20 tasks covering every work function present in the cluster;
  - 2–3 **bogus tasks**: plausible but non-existent, written by IO, e.g. "Recalibrate the regional phenology index against satellite moisture tiles";
  - 2 instructed-response items.
- **Rotating blocks:** the remaining pool is split into blocks of 20 tasks, balanced by work function and craft. Each form = anchor + 3 rotating blocks (≤ 80 real tasks). Forms are assembled so that every pair of rotating blocks appears together on at least one form (a balanced incomplete block design). This lets ratings link across forms.
- **Respondents needed per cell** to reach ≥ 30 incumbent ratings on every task: `n_cell = 30 × B / 3`, where B is the number of rotating blocks. For example, 6 rotating blocks (120 tasks) need 60 incumbents per sector-actor × cluster cell [E: arithmetic]. Supervisors: ≥ 10 per cell, on the supervisor version.
- **Precision.** With n = 30 performers, a 1–5 importance mean has a 95% CI half-width of about ±0.36 (SD ≈ 1); with n = 50, about ±0.28 [E: IO Phase 2 computation]. Cells with 15–29 respondents are descriptive and comparative only.
- **Form assignment:** random within cell (seeded); form ID recorded.
- **Length target:** ≤ 40 minutes. The performed-screener (B1) means only performed tasks get the follow-up items.

## 3. Respondents and composition

- **Eligible:**
  - incumbents in positions mapped to the cluster's role variants (federal series lists from FH; state classes from SL; local, NGO and private positions through design partners and PS);
  - **recently separated incumbents** (left such a position within 24 months; separate stratum);
  - **supervisors** of such positions (supervisor version).
- **Strata:** sector actor × cluster × region (4 Census regions + Alaska/Pacific) × career stage (sampling and analysis only; never a proficiency level).
- **Composition correction (ADR-0024 §7):**
  - recruitment targets at 1.5× quota for public field and statecraft roles, field-season staff, early-career and term employees;
  - participation costs removed (on-duty time; stipends for NGO and separated respondents; phone or interviewer mode for field staff; fielding outside peak field and fire season);
  - weekly response monitoring by stratum.
- **Weighting.** Rake to benchmarks: OPM workforce data by series for federal (FH); BLS OEWS by ownership and SOC plus state class headcounts (SL); OEWS private (PS). Trim weights at 5× the median. Report the design effect.
- **Tribal employers and employees:** not sampled except through Tribal research approval, on Tribal terms. No benchmark is assumed (TN; CARE).

## 4. The instrument (text as fielded; version `JAS-instrument@1.0.0-draft`)

### 4.0 Introduction and consent (shown first)

> This survey asks what work is done in your kind of position and what it takes to do it well. It is part of building an open, public description of environmental work (the Environmental Management Skills Taxonomy). It is **not** an evaluation of you or your performance, and your answers will not be shared with your employer.
> We do not ask your name, and we do not record your exact duty station or your computer's address. Results are reported only for groups of at least five people.
> The survey takes about 35–40 minutes. You can skip any question, pause and come back, or stop at any time.
> [I agree to take part] [I do not want to take part]

### 4.1 Section A — About your work (no identifiers)

| # | Item | Response options |
|---|---|---|
| A1 | Who employs you in this position? | Federal agency · State agency · County, city or special district · Tribal government or organization (routes to the Tribal protocol notice; no further items) · Nonprofit or NGO · Private company · College or university · Other |
| A2 | Which best describes your position? | list of the cluster's role variants in plain language (function-based titles), plus "None of these" (screen-out) |
| A3 | (Federal) Occupational series of your position, if you know it | dropdown of series in the cluster; "Don't know"; "Prefer not to say". Reported only in aggregate, n ≥ 5 |
| A4 | Do you supervise others in this kind of work? | No · Yes, 1–4 people · Yes, 5 or more |
| A5 | Which stage of responsibility best fits your position? | Entry (work is closely directed and checked) · Journey (standard work on your own) · Senior (non-routine work; you plan your own approach) · Lead (you set the technical approach for a team or programme) · Strategic (you set direction across programmes or organizations). *Used to place respondents in role-level bands (SPEC §5.7). Not a self-rating of proficiency* |
| A6 | Region of your work | Northeast · Midwest · South · West · Alaska or Pacific islands · Multiple or national |
| A7 | About how many years have you done this kind of work, in any organization? | < 2 · 2–4 · 5–9 · 10–19 · 20+. *Sampling and analysis only; never used to define a level* |
| A8 | Have you done this kind of work for more than one kind of employer (e.g. federal and state, or agency and consulting)? | No · Yes (select all that apply from the A1 list) |
| A9 | Are you in this position now? | Yes · No, I left it within the past two years · No, longer ago (screen-out) |
| A10 | Roughly what share of your working time is spent in the field or at a site, plant or lab, rather than at a desk? | 0–10% · 11–30% · 31–60% · 61–90% · > 90% |
| A11 | Over the past year, roughly how was your working time split across these kinds of work? (total 100%) | the cluster's work functions in plain language (e.g. "Assess and survey conditions", "Write or review permits and approvals", "Inspect and enforce"), plus "Other". Sliders that must sum to 100 |

### 4.2 Section B — Tasks (anchor block + three rotating blocks)

Instruction:
> For each task, first say whether you do it in your position (or did, if you left within the past two years). If you do, answer the follow-up questions. Think about the **past 12 months**.

| # | Item | Response options (anchors shown on every page) |
|---|---|---|
| B1 | Do you perform this task in your position? | Yes · No · I don't understand this task (logged for review) |
| B2 | How often? | 1 Less than once a year · 2 About yearly · 3 About monthly · 4 About weekly · 5 Daily |
| B3 | Compared with your other tasks, how much of your time does it take? | 1 Very little · 2 Less than most · 3 About average · 4 More than most · 5 A great deal |
| B4 | How important is doing this task well to effective performance in your position? | 1 Not important · 2 Of minor importance · 3 Important · 4 Very important · 5 Critical |
| B5 | If this task were done wrong, what is the most likely consequence? | 1 Negligible · 2 Minor rework · 3 Significant cost, delay or legal exposure · 4 Serious harm to people, the environment or legal standing · 5 Severe or irreversible harm |
| B6 | Must someone in your position be able to do this on their **first day**, without further training? | Yes · No · Not sure |
| B7 | How is this task done in your position **now**? | No AI or automation involved · I do it with tools that help (I still produce the result) · A system produces a draft or result and I review and sign off · A system does it and I supervise and step in when needed · Not sure |
| B8 | Has how this task is done changed materially in the past 12 months? | Yes · No · Not sure |

Bogus tasks and instructed-response items ("For this row, please select 'About monthly'") appear in fixed positions per form, randomized across forms.

**Supervisor version:** items are reworded for "the position(s) you supervise". B7 and B8 ask what the supervisor observes.

### 4.3 Section C — Competencies (≤ 25 for the cluster)

Instruction:
> These are broader capabilities that the tasks draw on. Each one has a short description. Levels are described by responsibility, not years: hover over or open "What the levels mean" (the generic L1–L5 descriptors, in plain language).

| # | Item | Response options |
|---|---|---|
| C1 | How important is this capability for full performance in your position? | 1 Not important · 2 Of minor importance · 3 Important · 4 Very important · 5 Critical · Not part of my work |
| C2 | What level does full performance in your position require? | Awareness only · L1 Supervised · L2 Independent · L3 Senior · L4 Lead/Expert · L5 Strategic · Not required |
| C3 | What level is needed on the first day in the position? | same options |
| C4 (optional) | About how long does it typically take someone to reach the level in C2 in this kind of position? | < 6 months · 6–12 months · 1–2 years · 3–5 years · > 5 years · Don't know. *Descriptive only (`typicalTimeToLevel`); never a criterion (ADR-0004 §7)* |

### 4.4 Section D — What is missing

| # | Item |
|---|---|
| D1 | Is there important work in your position that none of these tasks describes? Please describe up to three tasks in a sentence each. *(Do not include names, places or anything that identifies you or others.)* |
| D2 | Is there work that has recently become **new** in your position (e.g. reviewing outputs of a new system)? Describe it in a sentence. |

D1 and D2 text is screened for personal and held content before analysis. It feeds change requests and new-work signals (LM; `ChangeSignal` with `raterType` context `sme`, evidence label S until reviewed).

### 4.5 Close

> Thank you. Group results will be published in the taxonomy's open release, with no individual answers.

## 5. Data quality and exclusions (pre-registered)

| Check | Rule |
|---|---|
| Bogus tasks | exclude a respondent who reports performing ≥ 2 bogus tasks, or 1 bogus task at frequency ≥ 3. A respondent who endorses 1 bogus task at frequency ≤ 2 is kept, flagged, and included in a sensitivity analysis without them [E-u: IO-078] |
| Instructed response | exclude if either instructed-response item fails |
| Straight-lining | exclude if ≥ 90% identical responses on two or more task pages |
| Speed | exclude if total time < 1/3 of the median for the form |
| "I don't understand this task" | a task with > 10% such responses is flagged as a wording defect. It is reported, and excluded from retention decisions in that cell |
| Investigation trigger | if bogus-task exclusions exceed 15% of a cell, pause analysis of that cell and investigate fielding (panel quality, form display) |

## 6. Analysis and decision rules (pre-registered; illustrative thresholds from Phase 2 confirmed here)

All estimates are weighted (§3), with unweighted results and design effects reported. Means of B2–B6 are among performers. All counts and shares are computed by the analysis code and never typed into documents.

| Output | Rule |
|---|---|
| **Task retained** for a cluster × sector actor | ≥ 25% of incumbents perform it, **and** (weighted mean importance ≥ 3.0 **or** mean consequence of error ≥ 4.0). The consequence route keeps rare, high-stakes tasks such as spill response |
| **Criticality index** | per performer: importance × consequence (1–25), averaged across performers |
| **Critical task** (`taskBundle.critical`) | retained **and** criticality index in the top tercile of retained tasks for the cluster |
| **Needed at entry** (`neededAtEntry`) | ≥ 50% of incumbents **and** ≥ 50% of supervisors say "Yes", each computed separately. Otherwise the task is a development target, not an entry criterion |
| **Importance** (`taskBundle.importance`) | weighted mean B4, rounded to the 1–5 scale for the profile; unrounded value kept in the computed view |
| **Time share** (`taskBundle.timeShare`) | Within each respondent: B3 relative-time ratings are normalized across the performed tasks of each work function. Each is then scaled by that function's A11 allocation, then averaged across respondents. The method is pre-registered; the limitation (matrix forms show a subset of tasks) is reported, and the anchor block covers every function |
| **Actor-variant task** | retention differs by ≥ 25 percentage points between sector actors with n ≥ 15 each. Feeds CA's enactment and variant decisions |
| **Competency existence at a level (PR-1)** | ≥ 20% of incumbents whose A5 band includes that level rate the competency C1 ≥ 3 |
| **Required and entry levels** | the distribution of C2 and C3 by A5 band; the modal level with ≥ 50% gives a draft target level. Placement still needs the Delphi (PR-4) |
| **AI-mode distribution** (B7) | reported by task × sector actor as **incumbent-reported** evidence for construct (b) (`raterType = sme`). A share ≥ 20% reporting "a system does it and I supervise" is a **signal**, not deployment evidence on its own. XR-04 still requires a registered deployment or documented directive use, corroborated in ≥ 2 organizations [J] |
| **Change sentinel** (B8) | ≥ 20% reporting material change in a task triggers targeted re-rating of level placement and augmentation mode (validation_protocol §11) |
| **Reliability** | ICC(2,k) of mean importance per task within a cluster × actor cell; target ≥ .80; r_wg(j) alongside [E-u: IO-044, IO-085]. Cells below target are descriptive only |
| **Inflation check** | incumbent vs supervisor means per task; standardized difference > 0.5 flagged [E-u: IO-043, IO-087] |
| **Composition sensitivity** | re-run retention and critical decisions (a) unweighted and (b) dropping the most over-represented stratum. A decision that flips under either is **contested** and goes to the Delphi for that cluster |
| **Nonresponse bias** | early vs late responders; respondents vs frame on available attributes |

## 7. Linkage study (separate SME panel; job-relatedness for selection)

- **Panel:** ≥ 7 SMEs per cluster, not the Delphi panelists where avoidable, with the same composition caps.
- **Rating:** every retained task × candidate competency: 0 not needed · 1 helpful · 2 essential.
- **Link established** if mean ≥ 1.5 or ≥ 60% rate 2. Linkage reliability: ICC(2,k) of linkage means ≥ .75.
- A competency is **job-related for a cluster** only if it has an established link to ≥ 1 **critical** task. Competencies without one stay for description and development but may not be marked `criticalForSelection` in that cluster's role profiles [J; ADR-0024 §8].
- **Indicator ↔ task:** every indicator cites its served tasks (`servedTasks[]`). An assessment blueprint maps components to indicators and reports coverage of critical tasks.

## 8. Stop rules

| Rule | Trigger | Action |
|---|---|---|
| Fielding close | every cell reaches its target, or 10 weeks after launch | close |
| Small cells | a cell with 15–29 completes | descriptive and comparative only; no retention decision for that actor |
| Very small cells | a cell with < 5 completes | suppressed entirely (SPEC §16.2) |
| Defect | > 10% "I don't understand" on ≥ 5 tasks in the first 50 completes of a cluster | pause the cluster; fix wording; restart with a new form version (deviation logged) |
| Harm | a respondent reports distress or employer pressure | contact route in the consent text; the study host handles it; logged without identifiers |
| Held content | Tribal-related content found in the pool or in D1/D2 | remove; notify TN |

## 9. Approvals and privacy (CP lane)

- **Paperwork Reduction Act.** Applies if a federal agency sponsors or conducts a survey of ten or more members of the public (NGO, private and academic respondents). Federal employees answering within the scope of their employment are generally outside it. Choose the conducting entity deliberately [J; validation_protocol §2].
- **Other approvals:** IRB or exemption through an academic partner if publication is intended; agency survey approval; union notification or bargaining where participation affects working conditions.
- **Data handling:**
  - no names, email or IP addresses stored with responses;
  - the platform meets CP's security requirements;
  - person-level data stay with the study host and never enter the repo;
  - the repo receives cell aggregates with n ≥ 5 (ADR-0012).

## 10. Pre-registration fields

All `preregistration_core.yaml#core_required` fields, plus:
- `cluster_and_pool` (task and competency lists with SHA-256);
- `forms` (blocks, assembly, form IDs, bogus and instructed items);
- `frames_and_benchmarks`;
- `cell_targets` (formula §2);
- `composition_correction`;
- `weighting` (raking variables, trimming);
- `exclusions` (§5);
- `decision_rules` (§6, incl. the criticality formula and time-share method);
- `linkage_study` (§7);
- `stop_rules` (§8);
- `approvals` (§9).

## 11. Outputs

- Computed views per cluster × sector actor:
  - task retention;
  - importance, frequency and consequence;
  - criticality;
  - critical and needed-at-entry flags;
  - time share;
  - competency importance and required-level distributions;
  - PR-1 existence results;
  - AI-mode distributions;
  - change-sentinel rates;
  - reliability.
  WP-08 replaces agent-estimated `importance`, `timeShare`, `critical` and `neededAtEntry` values with these. Every such field cites the study.
- `validationStatus = job-analysis-confirmed` is set by DE from the computed results, never by hand. It applies to competencies with established linkage to critical tasks for that cluster.
- Report `validation/studies/JAS-n/report.md` (generated), with the "not a job analysis of your position" statement on its face.
