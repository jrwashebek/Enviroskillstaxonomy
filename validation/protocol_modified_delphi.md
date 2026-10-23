# Protocol: Pre-registered modified Delphi for EMST v2 content (DEL)

**WP-11 output 4** · Owner: IO (A8) · Status: draft protocol for CA approval; run with people in Stage 1 (not in Phase 4) · Date: 2026-10-23
**Decision basis:** ADR-0024 §3, §6, §7; ADR-0020 §3 (v1 Tasks 20–21 redesigned); ADR-0004 §3 (PR-4 consensus); SPEC §8.2; `vocab/lifecycle_states.yaml#validation_statuses` (`panel-retained`).
**Companion files:** `validation/lawshe.py` (exact critical values; the table in §6.2 is its output), `validation/preregistration_core.yaml`, `validation/protocol_cognitive_interviews.md` (item pretesting).
**Labels:** [E] evidence (IO source IDs), [J] judgment, [S] speculation.

---

## 1. What the Delphi decides, and what it cannot

| Decision | Output in the repo | Feeds |
|---|---|---|
| Is a competency **essential** for a function cluster? (Lawshe) | Aggregate Delphi record; `validationStatus = panel-retained` on retained competencies | Release criteria (ADR-0024 §3), use tier |
| **Level span** of each competency (lowest and highest level at which the work exists) | `levelSpan` review record | SPEC §5.2 |
| **Level placement** of each indicator (PR-4) | `publicationRuleChecks.consensus = pass` with the Delphi round as evidence | develop and select tiers (CR-IO-001) |
| **Observability designation** for selection use | per-indicator panel result plus two-coder OBS-4 = 3 | `useClass = select` eligibility |
| **Contested structural decisions** referred by CA (e.g. a merge, a home module, a craft boundary case) | structured-choice result with rationale | CA decision record |
| **Actor divergence** | `actor-variant` flag | CA enactment and role-variant decisions |

The Delphi **cannot**:
- confirm job-relatedness for a particular employer's job (that needs a job analysis, `instrument_job_analysis_survey.md`);
- establish rater reliability of tags (`protocol_reliability_study.md`);
- validate an assessment.
A competency that is "panel-retained" is retained **for a function cluster across sector actors**. It is not validated for selection in any job (ADR-0024 §1).

**No agent ratings.** Only human panelists respond. Phase 4 agents may draft items and plain-language summaries. Their involvement is disclosed in the registration and the report (ACCORD). No agent output is ever counted as a panelist response, a Delphi retention or a consensus. Nothing in Phase 4 may be described as Delphi-retained (PHASE4_BUILD_PLAN §1 rule 2).

## 2. Design

- **Round 0 (not a Delphi round).** DACUM-style workshops, 6–10 SMEs per function cluster. They:
  - critique the draft tasks, competencies and indicators;
  - generate critical incidents for BARS (≥ 10 per competency);
  - propose level spans.
  Workshop participants may join the Delphi panel but are a minority of it (≤ 30%). Workshop output revises items **before** Round 1. It is never counted as Delphi data.
- **Rounds 1–3.** Online, anonymous, asynchronous. Each round is open 14 days, with two reminders.
- **Panels.** One per function cluster plus one cross-cutting panel for the transversal layer (TX-A … TX-F). The first five clusters follow ADR-0024 §9:
  1. field monitoring and inventory;
  2. regulatory compliance, permitting and environmental review;
  3. geospatial and data analysis;
  4. water quality and drinking-water/wastewater operations;
  5. the natural-resources Job-Analysis Starter Pack series (0401/0404 variants).
- **Load.** ≤ 60 items per panelist per round (≈ 45 minutes). Where a cluster has more items, items are split into two matrix forms with a 15-item common block. Every item must still reach N ≥ 15 responding (§6.1).

## 3. Panel size and composition

### 3.1 Size

- Recruit **30 per panel**, so that 15–25 complete all rounds (planning attrition ≈ 20–30%).
- An item decision needs **N ≥ 15 responding** in that round. Below that, the item is reported as "insufficient panel" with its distribution, and no decision is made.
- v1's planned 3–5 reviewers per competency cannot support CVR decisions. At 3, significance is unattainable; at 5, only unanimity is significant [E: `validation/lawshe.py`; ADR-0024 Context].

### 3.2 Composition rules (correction for contraction bias; ADR-0024 §7)

| Rule | Value |
|---|---|
| Cap per sector actor | ≤ 30% of any panel |
| Field practitioners | in proportion to the field share of the cluster's workforce (benchmarks: FH for federal series, SL for state classes) |
| Current or recent field- or statecraft-primary roles | ≥ 1/3 of each panel |
| Early-career members (< 5 years in the field; sampling attribute only, never a proficiency level) | ≥ 20% |
| Members who have moved between sector actors (CM) | ≥ 20% |
| Recently separated incumbents (left a relevant position within 24 months) | target 10–20%, analysed separately and pooled |
| Federal and state representation | both present in every panel for the federal and state release |
| Private-sector data-craft practitioners | ≤ their population share in federal/state release panels |
| Independent panelists where recruitment runs through adopters | ≥ 50% |
| Participation costs | removed: on-duty authorization for public employees; stipends for NGO, Tribal and separated participants; phone or interviewer modes for field staff; fielding outside peak field and fire season |
| Tribal participation | only through Tribal research approval, on Tribal time (P-TN-16). **No Tribal-related item enters any non-Tribal panel** (held content, ADR-0007) |

**SME qualification**, documented per member: current or recent performance of the work, supervision of it, or training others in it. Conflicts of interest are recorded: vendor relationships, authorship of the items, and employment by an adopter that funds the panel.

**Steering group** (IO, CA, FH, SL, DE, IA; TN for anything touching Tribal content):
- does not vote;
- does not see identified responses;
- appoints an **independent coordinator** who did not author items (CREDES item 5).

## 4. Items and response formats

| Item type | Rating(s) | Required comment |
|---|---|---|
| Competency (title + statement) for the panel's cluster | Lawshe: essential / useful but not essential / not necessary; clarity 1–4; "cannot judge" | any "not necessary" or clarity ≤ 2 |
| Level span | lowest and highest level at which the work exists (A, L1–L5, with generic descriptors shown) | if span differs from the draft by ≥ 2 levels |
| Indicator | level placement (A, L1–L5, or "not a real performance"); observability (directly / with specification / not observable); essential / useful / not necessary | placement ≥ 2 levels from the round median (R2, R3) |
| Contested structural decision | structured choice among the options CA lists, plus rationale | always |

Items are pretested in cognitive interviews (`protocol_cognitive_interviews.md`) before Round 1. "Cannot judge" is excluded from N for that item and reported.

## 5. Feedback between rounds

Each panelist sees, per item:
- the distribution;
- the median and IQR;
- the CVR and its critical value at the current N;
- anonymized verbatim comments;
- their own previous rating.

Subgroup breakdowns (by sector actor or craft) are shown **only** when the actor-divergence rule fires (§6.3), to limit conformity pressure [J; IO-069].

**LLM summaries of comments.** Allowed only if all of the following hold:
1. a human checks each summary against the verbatim comments;
2. the verbatim comments remain available to panelists;
3. the use is disclosed in the report (ACCORD) [E-u: IO-063].
An LLM never proposes revised item wording that goes to the panel without a human author of record.

## 6. Decision rules (pre-registered)

### 6.1 Per item, per round

| Decision | Rule |
|---|---|
| **Retain** (competency or indicator) | number of "essential" ratings ≥ the exact critical value for the item's responding N (§6.2) **and** ≥ 75% "essential" or "useful" |
| **Exclude** | ≥ 75% "not necessary", or, in the final round, < 50% "essential" or "useful" |
| **Revise** | neither retain nor exclude. One wording revision is allowed; the revised item re-enters the next round as a new version (old version's data kept) |
| **Clarity** | ≥ 80% rate 3–4; otherwise revise wording (counts as the one revision) |
| **Level placement (PR-4)** | ≥ 70% at the modal level **and** IQR ≤ 1 level |
| **Level span** | the modal lowest and modal highest level each reach ≥ 70%; otherwise "span unresolved" and the draft span stands, labelled pending |
| **Selection-use designation** (indicator) | retained **and** ≥ 75% "directly observable" **and** OBS-4 = 3 by two independent human coders (`spec_gold_sets.md` §4) |
| **Stability (item stops)** | consensus reached, **or** ≤ 15% of panelists change category between consecutive rounds **and** a Wilcoxon signed-rank test shows no significant shift (p ≥ .05) |
| **Insufficient panel** | responding N < 15: no decision; distribution reported |

### 6.2 Exact Lawshe critical values (one-tailed exact binomial, α = .05; Ayre & Scally method)

Generated by `python validation/lawshe.py --markdown --min 5 --max 40` and checked against ADR-0024 §6 (N = 15 → 12; 20 → 15; 25 → 18) in `validation/tests/test_display_gates.py`. **Do not hand-edit**; regenerate from the script [E: computed; method IO-065, IO-066].

| N responding | critical n essential | critical CVR | exact one-tailed p |
|---|---|---|---|
| 5 | 5 | 1.000 | 0.0312 |
| 6 | 6 | 1.000 | 0.0156 |
| 7 | 7 | 1.000 | 0.0078 |
| 8 | 7 | 0.750 | 0.0352 |
| 9 | 8 | 0.778 | 0.0195 |
| 10 | 9 | 0.800 | 0.0107 |
| 11 | 9 | 0.636 | 0.0327 |
| 12 | 10 | 0.667 | 0.0193 |
| 13 | 10 | 0.538 | 0.0461 |
| 14 | 11 | 0.571 | 0.0287 |
| **15** | **12** | **0.600** | 0.0176 |
| 16 | 12 | 0.500 | 0.0384 |
| 17 | 13 | 0.529 | 0.0245 |
| 18 | 13 | 0.444 | 0.0481 |
| 19 | 14 | 0.474 | 0.0318 |
| **20** | **15** | **0.500** | 0.0207 |
| 21 | 15 | 0.429 | 0.0392 |
| 22 | 16 | 0.455 | 0.0262 |
| 23 | 16 | 0.391 | 0.0466 |
| 24 | 17 | 0.417 | 0.0320 |
| **25** | **18** | **0.440** | 0.0216 |
| 26 | 18 | 0.385 | 0.0378 |
| 27 | 19 | 0.407 | 0.0261 |
| 28 | 19 | 0.357 | 0.0436 |
| 29 | 20 | 0.379 | 0.0307 |
| 30 | 20 | 0.333 | 0.0494 |
| 31 | 21 | 0.355 | 0.0354 |
| 32 | 22 | 0.375 | 0.0251 |
| 33 | 22 | 0.333 | 0.0401 |
| 34 | 23 | 0.353 | 0.0288 |
| 35 | 23 | 0.314 | 0.0448 |
| 36 | 24 | 0.333 | 0.0326 |
| 37 | 24 | 0.297 | 0.0494 |
| 38 | 25 | 0.316 | 0.0365 |
| 39 | 26 | 0.333 | 0.0266 |
| 40 | 26 | 0.300 | 0.0403 |

N < 5: significance is not attainable. CVR = (2·n_e − N)/N. The critical value is always taken at the item's **own** responding N in that round, never at the recruited N.

### 6.3 Panel-level rules

| Rule | Trigger | Action |
|---|---|---|
| **Actor divergence** | overall consensus reached, but a sector-actor subgroup with n ≥ 5 differs by ≥ 25 percentage points on "essential or useful" | flag `actor-variant` to CA; show subgroup feedback in the next round |
| **Composition sensitivity** | after each round | Recompute every retain/exclude decision (a) with panelists raked to the target composition (sector actor × craft background), weights trimmed at 5× the median, and (b) dropping the most over-represented stratum. A decision that flips under either is reported as **contested** to CA and is not marked panel-retained until CA decides [J] |
| **Attrition** | < 70% of Round 1 completers remain in any later round | flag the panel; compare dropouts with completers by sector actor, craft and career stage; report |
| **Recently separated incumbents** | always | report their ratings separately and pooled; a ≥ 25-point difference is flagged as actor divergence |

## 7. Stop rules

1. **Hard stop after Round 3.** Items without consensus are published as "no consensus" with their distributions. They are never forced.
2. **Early completion.** If every item reaches a decision or stability after Round 2, Round 3 is not run.
3. **Panel failure.** If fewer than 15 panelists complete a round, that round's decisions for the panel are void. The round may be re-fielded once after topping up recruitment under the same composition rules; otherwise the panel is reported as failed.
4. **Integrity stop.** A breach of anonymity, a coordinated response pattern (identical response vectors across ≥ 3 panelists on ≥ 90% of items), or discovery of held content in the item set pauses the round. The steering group reviews, and actions are logged as deviations.
5. **No adaptive thresholds.** Thresholds are never changed after Round 1 opens.

## 8. Pre-registration fields

All `preregistration_core.yaml#core_required` fields, plus:

| Field | Content |
|---|---|
| `panels` | function clusters, panel IDs, item counts, matrix forms and common block |
| `item_set` | frozen item text with SHA-256 per item; version of each competency and indicator record |
| `composition_targets` | §3.2 caps and minima per panel; benchmark sources for field share |
| `sme_qualification_and_coi` | criteria and the conflict-of-interest form |
| `round_schedule` | open and close dates; reminder plan |
| `decision_rules` | §6.1 table; §6.2 critical-value source (`validation/lawshe.py` commit) |
| `feedback_content` | §5, including whether LLM comment summaries are used and how they are checked |
| `sensitivity_and_raking` | §6.3 composition sensitivity specification |
| `stop_rules` | §7 |
| `reporting` | CREDES (§9) and ACCORD |
| `registry` | OSF Registries entry, mirrored as repo release `prereg/DEL-nn` (ADR-0024 §6) |

## 9. Reporting: CREDES checklist mapping

The 16 CREDES items [E: IO-062; item list confirmed from a reproduced checklist, `validation/sources.csv` IO-112]. Paraphrased:

| # | CREDES item | Where this protocol meets it |
|---|---|---|
| 1 | Justification for choosing Delphi | §1 (decisions needing expert consensus across sector actors without a job-specific sample) |
| 2 | Planning and process, with any modification justified | §2 (modified: Round 0 workshop, matrix forms, structured items) |
| 3 | A priori definition of consensus, next-round handling and end point | §6, §7 |
| 4 | Informational input reviewed and piloted | §4 (cognitive-interview pretest); item SHA-256 in registration |
| 5 | Prevention of bias, incl. an independent coordinator | §3.2 steering-group rule; §5 feedback limits; composition sensitivity §6.3 |
| 6 | Interpretation: consensus is not correctness; non-consensus is informative | §1 limits; §7.1 "no consensus" published with distributions |
| 7 | External validation of the final output | CA decision and Editorial Board review; public comment window on the release (ADR-0009) |
| 8 | Purpose and rationale reported | report §1 |
| 9 | Expert panel: selection, recruitment, characteristics, response rates per round | report: aggregate composition table; response and attrition by round |
| 10 | Methods described (evidence base, piloting, design, rounds, analysis) | report: methods, pointing to this protocol and its SHA-256 |
| 11 | Procedure flow chart | report: generated flow chart (recruited → R1 → R2 → R3, with counts computed) |
| 12 | Definition and attainment of consensus, and handling of non-consensus | report: per-item decisions with N, CVR and critical value |
| 13 | Results per round, incl. changes between rounds and item changes | report: per-round tables; item version history |
| 14 | Limitations discussed | report: composition, attrition, contraction bias, Tribal exclusion, NGO-pilot scope |
| 15 | Conclusions match the results and scope | report: retained-for-cluster wording; no selection claims |
| 16 | Publication and dissemination plan | release notes; OSF; repo `validation/studies/DEL-nn/` |

**ACCORD supplement** [E-u: IO-063]: report any AI use in item drafting, comment summarization or translation; who checked it; and the verbatim-availability safeguard.

## 10. Outputs and data handling

- **Into the repo, aggregates only:**
  - per-item, per-round counts by response option;
  - N; CVR; critical value; decision;
  - subgroup aggregates only where n ≥ 5 (small cells suppressed).
- **Outside the repo** (ADR-0012; SPEC §16.2): panel rosters, contact details and person-level responses, held by the study host.
- DE sets `validationStatus = panel-retained` and `publicationRuleChecks.consensus = pass` from the aggregate Delphi record, never by hand. Each status change cites the study ID and round.

## 11. Timeline (per panel; planning estimate [J])

| Step | Weeks |
|---|---|
| Round 0 workshop; item revision; cognitive pretest | 1–6 |
| Registration (OSF + repo tag) | 6 |
| Recruitment (parallel from week 2) | 2–8 |
| Rounds 1–3 (14 days open + 7 days analysis each) | 8–17 |
| Report | 17–19 |
