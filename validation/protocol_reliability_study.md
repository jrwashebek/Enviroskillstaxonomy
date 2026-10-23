# Protocol: Inter-rater reliability study for EMST v2 tags (REL)

**WP-11 output 3** · Owner: IO (A8) · Status: draft protocol for CA approval; to be pre-registered before any data collection · Date: 2026-10-23
**Decision basis:** ADR-0024 §2–§5, §12; ADR-0005 §6–§7; ADR-0008 §1–§3; ADR-0017 (status line); SPEC §7.2, §10.5, §13.1; `vocab/lifecycle_states.yaml#reliability_gate`.
**Machine-readable gate:** `validation/display_gates.yaml`; statistics: `validation/reliability.py`; shared pre-registration fields: `validation/preregistration_core.yaml`.
**Labels:** [E] evidence (source IDs resolve to `docs/research/io-validation/sources.csv` or `validation/sources.csv`), [J] expert judgment, [S] speculation.

---

## 1. Purpose and the claim it supports

Every tag a user can see (a craft rating, a work function, an exposure level, a deployment mode) is a judgment. ADR-0024 §4 requires that the judgment be reproducible by independent trained raters before it is shown. This study produces the **only** evidence the display gate accepts: a pre-registered, human-only Krippendorff's α per dimension and codebook version, with a unit-bootstrap 95% CI, decided on the lower bound.

| If the lower bound is | Then (display_gates.yaml) |
|---|---|
| ≥ .80 | production: values render; agreement shown in the evidence drawer |
| .667 – < .80 | tentative: values render with a "Tentative" badge stating α, CI and n |
| < .667, or no admissible study | hidden: fallback label ("Assessment pending" / "Not shown: agreement below threshold") |

The study supports the claim "independent trained raters applying codebook *v* to EMST v2 task texts reproduce these values to a stated degree." It does **not** support claims that the values are *correct* (accuracy is assessed against gold sets, `spec_gold_sets.md`), that tasks are job-related (job-analysis survey), or that any assessment is valid for selection.

**No agent ratings as human agreement.** Phase 4 agent passes (WP-03 to WP-08 "three independent agent passes recorded as `llm` raters") are **not** raters in this study. They count as one rater type, `llm`, which `display_gates.yaml#admissibility` never counts. Agreement among agent passes is *run-to-run consistency* and is reported only under `protocol_llm_coder_gate.md`. No document may describe agent-pass agreement as inter-rater reliability [J; PHASE4_BUILD_PLAN §1 rule 2].

## 2. Dimensions, metrics and study blocks

Dimensions are those listed in `display_gates.yaml#dimensions`. Each is gated separately. FC, DC and SC are three gates, and each exposure vector is its own gate.

| Block | Unit | Dimensions (metric) | Codebook | Units | Raters/unit |
|---|---|---|---|---|---|
| **A Craft and task attributes** | v2 task statement (hash-pinned) | craft.FC, craft.DC, craft.SC (ordinal 0/1/2, or the scale chosen by `protocol_craft_scale_pilot.md`); craft.defining (nominal); fieldDependency, formationDependency (ordinal); reproduction-regime attributes (ordinal; placeBoundness nominal) | `codebook_craft_ratings.md` | 150 | 6 |
| **B Work function and modes** | v2 task statement | task.workFunction (nominal, 13); sub-function within parent (nominal); MODE-ENGAGE present (nominal); relationshipType (nominal); MODE-RESOLVE present (nominal) | `codebook_work_function_authority.md` | 160 | 6 |
| **C Authority position** | public position description, job posting or state class specification, de-identified (no names, contact details or duty-station identifiers) | unit.authorityPosition (nominal, 8) | `codebook_work_function_authority.md` | 120 | 6 |
| **D Exposure** | v2 task statement × sector actor (b, c); task (a, tacit) | technical exposure per vector (ordinal E0–E3); deploymentMode (ordinal); deploymentStage (ordinal); strategy (nominal); tacitExperienceRequirement (ordinal); scenario rows only for eligible tasks (nominal or ordinal) | `codebook_exposure_XR.md` | 150 (a, b); 120 eligible task × scenario rows (c) | 6 |
| **E Indicators and the core/module rule** | Indicator statement; competency record with task links | OBS-4 (ordinal 0–3; plus flags P/C/O/T as nominal); G-4 core vs home module (nominal) | `docs/research/io-validation/indicator_writing_rules.md` §2; ADR-0003 G-4, ADR-0018 home-module rule | 150 indicators; 120 competencies | 6 (OBS-4); 6 (G-4) |
| *Deferred* | task | ethical lens triggers (nominal) | written only if CA keeps lenses | — | — |

Relevance and linkage ratings (competency × role, task × competency) come from the job-analysis and linkage studies (`instrument_job_analysis_survey.md`). They are gated by ICC(2,k) and the display gate's rules for `relevance.competencyRole`, not by this protocol.

**Why 120–200 units × 6 raters.** α's sampling range is about ±0.15 with 40 units, too wide to tell .667 from .80. With 120–200 units and 6 raters it narrows to about ±0.04–0.07 [E: IO Phase 2 simulation, `docs/research/io-validation/analysis/alpha_precision_simulation.py`; reproduced on synthetic data in `validation/tests/test_display_gates.py::test_simulated_study_precision_supports_120_units_x_6_raters`]. Blocks are sized at the low end where units are scarce (C: few public PDs exist per authority position) and higher where categories are many (B: 13 functions).

## 3. Sampling units

1. **Frame.** v2 task statements with `status ∈ {draft, candidate}` and a current `textSha256`, drawn from the seed records of WP-02 to WP-06. Indicator and competency frames come from WP-03 to WP-07. Authority-position units come from a dated snapshot of public postings, PDs and state class specs (FH, SL and PS supply candidates; IO de-identifies them).
2. **Stratification** follows `spec_gold_sets.md` §3:
   - home module (core plus the nine wave-1 modules);
   - prior craft (v1 craft or Phase 4 agent draft);
   - prior work function;
   - sector actor where the dimension is actor-specific;
   - source type (v1-carried, v1-rewritten, net-new, D3 text that v1 inferred).
   At least 40% of units come from outside public lands and forestry (P-DB-17).
3. **Rare categories.** The target is ≥ 10 units expected in every category of every gated dimension. It is met by oversampling on prior labels: system-executes, E3, the robotics vector, WF-RULE, WF-RESOURCE, `independent-verifier`, `funder`. Prior labels are used **only to sample**. They are never shown to raters. Because oversampling changes prevalence, α is reported both unweighted (the gate statistic) and with prevalence weights back to the frame (descriptive).
4. **Exclusions.** Held content is never in any frame. That covers records with `approvalStatus = pending-tribal-review`, `indigenousDataFlag = true` or `governedData = tribal`, and tasks with relationshipType government-to-government (ADR-0007). Units also exclude anything the raters authored, and any unit in a gold set's held-out evaluation split (`spec_gold_sets.md` §5). Gold-set development units may overlap.
5. **Freezing.** The unit list is frozen with each unit's `textSha256` before registration. A unit whose text changes after freezing is dropped and logged. It is not re-rated within the study.

## 4. Raters

| Element | Specification |
|---|---|
| Rater types counted | `expert-panel`, `sme`, `analyst` (human) only |
| Pool per block | 8–10 people, so every unit gets 6 independent ratings. Fully crossed (every rater rates every unit) where the block is ≤ 160 units; otherwise a balanced incomplete design |
| Composition | ≥ 2 trained taxonomy analysts; ≥ 4 practitioner SMEs. For A and D: balanced across FC/DC/SC backgrounds and ≥ 4 sector actors, no sector actor > 30% of a pool, and ≥ 1/3 with current or recent field- or statecraft-primary roles (ADR-0024 §7). For C: classification or HR practitioners from federal, state and private employers (FH, SL, PS recruit) |
| Qualification | Documented current or recent performance, supervision, classification or training of the work. Conflicts of interest recorded. Authors of the rated text excluded for those units |
| Independence | No discussion of units during the study. Raters never see others' ratings, prior labels or any LLM output |
| Compensation | Paid or on-duty time for every rater (removes the participation cost that biases toward over-represented strata, ADR-0024 §7) |
| Identity | Pseudonymous rater IDs. The key is held outside the repo (ADR-0012) |

## 5. Procedure

1. **Training.** 60–90 minutes of frame-of-reference training per block on the codebook definitions, decision rules and anchored examples [E-u: IO-042].
2. **Calibration set.** 15 units per block with keyed answers and feedback, excluded from analysis. The keys are the provisional calibration keys in each codebook, ratified by a three-person key panel before the study (the FC, DC and SC leads' nominees, or FH/SL/PS for block C).
3. **Qualification check (pre-registered).** A rater whose agreement with the calibration key is below α = .50 on the calibration set gets one retraining and a second calibration set. If still below, the rater is replaced **before** the main study. No rater is removed on main-study data except under §7.4.
4. **Blind coding (XR-01; ADR-0005 §6).** The interface shows only:
   - the unit text;
   - the minimal context the codebook requires (sector actor for blocks D-b and D-c; role-variant summary for block C);
   - the response options with their codebook definitions on hover and in text.
   It never shows parent competency, domain, v1 codes, prior craft, prior exposure or any agent suggestion.
5. **Order and fatigue.** Unit order is randomized per rater with a recorded seed. Sessions are ≤ 45 minutes. The time per unit is logged and flagged below 20% of the median.
6. **Response options.** Each unit carries:
   - the codebook value;
   - confidence (1–5);
   - "cannot code" with a reason (missing information / two categories equally apply / category set does not fit), which is analysed as missing;
   - an optional free-text note.
   A dimension where > 10% of ratings are "cannot code" is treated as a codebook defect (see §8).
7. **Burden** (planning estimate [J]):
   - block A: about 90 s per unit for three crafts plus attributes, about 4 h per rater;
   - block D: about 3 min per unit, about 7.5 h per rater;
   - blocks B and C: about 45–60 s per unit, about 2–3 h per rater.

## 6. Analysis plan (pre-registered; code in `validation/reliability.py`)

1. **Gate statistic.** Krippendorff's α, human raters only, at the metric in `display_gates.yaml#dimensions`. Missing values are handled natively by α. Only units with ≥ 2 pairable human values are counted [E: IO-067, IO-068].
2. **Interval.** Unit-level bootstrap with B = 10,000 resamples and a recorded seed. Percentile 95% CI. **Decision on the 2.5th percentile.** No rounding before comparison with .667 and .80.
3. **Per-category agreement.** One-vs-rest binary α for every category, plus the coincidence matrix and confusion counts. Categories coded in < 10 units are reported as "not estimable".
4. **Strata.** α with bootstrap CI for every stratum value with ≥ 30 units (home module; sector actor where relevant). `display_gates.yaml#strata` applies the stratum gate.
5. **Consensus reliability for production values.** Production values are ≥ 3-rater consensus values (median for ordinal, mean for interval, two-thirds plurality for nominal). The reliability of a 3-rater consensus is estimated by `panel_split_alpha` (split the 6 raters into disjoint triads; α between triad consensus values; averaged over splits). It is reported to size production rating (how many raters per task in production).
6. **Rater diagnostics.** Each rater's α against the leave-one-out consensus; drift by session (first vs last third); confidence calibration (does confidence predict agreement with the consensus?).
7. **Supplementary.** Percent agreement and Gwet's AC1 are reported for skewed dimensions so prevalence effects are visible. They are **not** gate statistics. For interval data, ICC(2,1) and ICC(2,k) (absolute agreement) are reported alongside α [E-u: IO-085].
8. **What is not done.** No pooling of agent runs into any α; no weighting of the gate statistic; no exclusion of hard units after the fact; no codebook revision on main-study data within an iteration.

## 7. Decision rules and stop rules (pre-registered)

### 7.1 Decisions per dimension (iteration 1)

| Result (lower bound) | Decision |
|---|---|
| ≥ .80 | Production. The display gate renders ≥ 3-rater consensus values |
| .667 – < .80 | Tentative. The display gate renders values with the badge. Iteration 2 is optional, at CA's discretion |
| < .667 | Hidden. Iteration 2: revise the codebook (definitions, decision rules, examples) **using only calibration and iteration-1 diagnostics**, then re-run on a **fresh** sample of the same size and design |
| Category-level one-vs-rest α point estimate < .50 with ≥ 10 units, even when the dimension passes | Category flagged to CA. Values in that category render with the tentative badge at best until iteration 2 [J] |

### 7.2 Iteration 2 and retirement

- **Pre-registered collapses** allowed in iteration 2 only if registered with iteration 1. Each needs a CA change request if it changes an L0 vocabulary:
  - deploymentMode: supervises-system + system-executes → "system-executes or supervises";
  - technical exposure: E1 + E2 → "E1–E2";
  - deploymentStage: pilot + deployed-limited;
  - reproduction-regime currencyDecay and mentorshipDependence: three to two levels;
  - relationshipType: stakeholder + public;
  - workFunction: no collapse (ADR-0017 kept the functions distinct on purpose). A failing function pair is reported to CA.
- **After two failed iterations** a dimension is demoted: values stay as stored L5 ratings for research, are never rendered, and CA receives a change request to retire or redesign the dimension. This is the same rule ADR-0024 §10 applies to ethical lenses.

### 7.3 Stop rules

| Rule | Trigger | Action |
|---|---|---|
| **Futility (interim)** | After the first 40 main-study units in a block, a dimension's point α < .50 | Stop that dimension. The block continues for the other dimensions. The stop counts as iteration 1. The interim is computed by an analyst who does not revise the codebook |
| **No early success** | — | Success is never declared early; the planned n is completed (early stopping on success inflates α) |
| **Attrition** | > 20% of units have < 4 human ratings at the planned end | Recruit replacement raters (same qualification) until every unit has ≥ 4. Analysis requires ≥ 120 units with ≥ 2 pairable human values |
| **Codebook defect** | "cannot code" > 10% of ratings for a dimension, or ≥ 3 raters report the same misreading at calibration | Pause the dimension and fix the codebook before the main study (pre-main only) |
| **Held content found** | A held or Tribal-related unit is found in a frame | Remove it, log it, notify TN (gate G-TN). Not rated, not analysed |
| **Text change** | A unit's `textSha256` changes after freezing | Drop the unit and log it. If > 10% are dropped, top up from the frame with the same strata |
| **Hard stop** | 16 weeks after the first rating in a block | Analyse what exists; report under the same rules |

### 7.4 Rater exclusion (the only post-hoc exclusion allowed)

A rater is excluded from the gate statistic only if they (a) completed < 50% of their assigned units, or (b) failed instructed-response checks embedded at 2% of units. Results are reported with and without excluded raters.

## 8. Pre-registration fields

All fields in `preregistration_core.yaml#core_required`, plus:

| Field | Content |
|---|---|
| `blocks_and_dimensions` | the table in §2 for this run, with codebook versions and SHA-256 |
| `frame_snapshot` | release or commit of the seed records; frozen unit list with `textSha256` per unit |
| `strata_and_oversampling` | strata, targets, oversampled categories, prior-label source (never shown to raters) |
| `rater_pool` | composition targets and caps; qualification criteria; design (crossed or balanced incomplete) |
| `calibration_keys` | calibration units, keys and key-panel ratification record |
| `gate_parameters` | `display_gates.yaml` version and SHA-256; B; seed; bound used |
| `interim_and_stop_rules` | §7.3 as registered |
| `collapse_schemes` | pre-registered collapses (§7.2) |
| `supplementary_statistics` | AC1, percent agreement, ICC, panel-split α |
| `llm_separation_statement` | "No LLM or agent output is shown to raters or pooled into any statistic; LLM arms are analysed under LLM-nn." |

## 9. Outputs

1. One agreement result per dimension and codebook version, in the `display_gates.yaml#agreement_result_schema` shape. It is computed by the build from stored atomic ratings (`CraftRating`, `FunctionRating`, `ExposureAssessment`, all with `raterType ∈ {sme, analyst, expert-panel}`), and never typed into documents.
2. Report (`validation/studies/REL-nn/report.md`, generated). It contains:
   - frame and sample flow;
   - rater pool (aggregate composition only);
   - per-dimension α with CI;
   - per-category and per-stratum tables;
   - rater diagnostics;
   - deviations;
   - decisions;
   - limitations.
3. SCORES.md rows for every dimension (`spec_gold_sets.md` §7).
4. Change requests to CA for any collapse or retirement.

## 10. Limitations and threats

- **Agreement is not accuracy.** Six raters can agree on a wrong value. Gold sets with adjudicated keys test accuracy (`spec_gold_sets.md`) [J].
- **Prevalence.** Skewed dimensions (e.g., most tasks `human-executes` today) can yield modest α with high percent agreement. Oversampling rare categories counters this, and AC1 is reported, but the gate still uses α [J].
- **Rater-pool dependence.** α generalizes to raters like those sampled. The composition caps and the sector-actor spread are what make "trained raters" mean something across the sector [J].
- **Text dependence.** Results hold for the text rated. Editing task text invalidates values through the hash rule, but does not invalidate the dimension's α unless the codebook changes [J].
- **Time.** Exposure values are dated. α for technical exposure says raters agree *now* about *current* technology. Revalidation follows `display_gates.yaml#admissibility.max_age_months` and any codebook change [J].

## 11. Responsibilities and timeline

| Step | Lead | Weeks (from approval) |
|---|---|---|
| Frame snapshot, de-identification of block C units | DE, IO (FH, SL, PS supply units) | 1–3 |
| Calibration keys ratified; interface built (blind) | IO with FC/DC/SC leads; DE | 2–5 |
| Pre-registration (OSF + repo tag) | IO; CA approves | 5 |
| Recruitment (paid or on-duty) | AS, FH, SL; CM for movers | 3–8 |
| Rating, blocks A–E | IO | 8–16 |
| Analysis, report, agreement results into the build | IO, DE | 16–18 |
