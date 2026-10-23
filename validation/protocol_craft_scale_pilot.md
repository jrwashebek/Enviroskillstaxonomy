# Protocol: Craft-scale pilot, which decides ADR-0005's provisional rating scale (CSP)

**WP-11 output 6** · Owner: IO (A8); FC, DC and SC leads nominate key-panel members and SME raters · Status: draft protocol for CA approval; runs with people in Stage 1 (planned 6–8 weeks) · Date: 2026-10-23
**Decision basis:** ADR-0005 §4, §7 (pilot design and pre-registered rules), status line ("provisional on the scale until IO's craft-rating pilot reports"); ADR-0024 §4, §10; SPEC §5.13, §7.2.
**Companion files:** `validation/codebook_craft_ratings.md` (definitions, §9 formats, calibration set), `validation/reliability.py` (α, bootstrap, `panel_split_alpha`), `validation/preregistration_core.yaml`, `validation/protocol_llm_coder_gate.md`.
**Labels:** [E] evidence, [J] judgment, [S] speculation.

---

## 1. Questions and the decision this pilot makes

1. Can trained human raters produce task-level craft ratings reliably enough to show them? Under which format: **F1 constant-sum weights**, **F2 three-level ordinal** (0/1/2), or a **nominal "defining craft"** derived from either?
2. Are **competency-level** ratings more reliable than task-level ratings (evidence for or against v1's Option A)?
3. Is a frozen LLM coder promising enough to enter the formal LLM-coder gate?

The outcome sets `CraftRating.scale` for v2.0 (`ordinal-0-2`, `constant-sum-100` or `nominal-defining`). The schema accepts all three, so no migration is needed (ADR-0005 §4). If the pilot is admissible (§6.6), the adopted format's agreement result also becomes the display-gate result for `craft.FC`, `craft.DC` and `craft.SC`.

**Caution carried from Phase 2.** Coarsening a continuous judgment into three categories lowers α: in simulation, latent single-rater reliability of .80 becomes an ordinal α of about .68 [E: IO Phase 2 simulation]. The ordinal is a usability choice that must be confirmed. It is not a reliability guarantee. Only the head-to-head comparison settles it (ADR-0005 §Dissent, IO).

## 2. Units

| Set | Size | Composition |
|---|---|---|
| **Task units** | 150 v2 task statements, hash-pinned | Stratified by **prior craft**: 50 per v1 primary craft. For migrated tasks, prior craft is the parent's v1 craft; for net-new tasks, the Phase 4 agent draft. Used for sampling only and never shown. Also ≥ 40% from subsectors beyond public lands and forestry; ≥ 20% known boundary cases (v1 Delphi flags and integration points, excluding held point 2); ≥ 20% from D3 text v1 inferred |
| **Competency units** | 40 competency records (title + statement) | Each has ≥ 2 linked tasks in the task set, so the competency rating can be compared with the computed blend |
| **Calibration set** | 15 units (`codebook_craft_ratings.md` §8) + 10 practice tasks | Excluded from analysis |
| **Exclusions** | — | Held content (ADR-0007); tasks the raters authored; GS-TASK held-out units |

## 3. Raters

| Group | Size | Composition | Design |
|---|---|---|---|
| **(a) Trained taxonomy raters** | 6 | Analysts trained on the codebook; not authors of the units | fully crossed: every rater rates every unit in every format |
| **(b) Practitioner SMEs** | 6 | Balanced across FC/DC/SC backgrounds (2 each); ≥ 4 sector actors; no actor > 2 raters; ≥ 2 with current or recent field-primary roles | fully crossed |
| **LLM arm** | 1 frozen configuration × 3 independent runs per format | Configuration hashed (`protocol_llm_coder_gate.md` §3); prompt contains only the codebook and the unit text (XR-01) | separate; never pooled with humans |

All human raters are paid or on duty. They use pseudonymous IDs. Group (b) is recruited through FC/DC/SC networks with CM's mover sub-sample where possible.

## 4. Formats and procedure

1. **Training:** 60-minute frame-of-reference session; then the 10 practice tasks with feedback [E-u: IO-042].
2. **F1 constant-sum.** Distribute 100 points across **FC, DC, SC and "general professional practice"** by how much each is irreducible to doing the task.
   - *Change from the Phase 2 design (which used three buckets).* The fourth bucket lets a task with no defining craft be rated honestly (ADR-0003 G-7). Analysis uses the FC, DC and SC weights; the fourth bucket is reported. [J; CA to note.]
3. **F2 ordinal.** 0/1/2 per craft (`codebook_craft_ratings.md` §1–§4).
4. **Derived nominal "defining craft".** The set of crafts at 2 (F2) or at ≥ 40 points (F1); an empty set means general practice.
5. **Counterbalancing.** Within each group, three raters do F1 first and three do F2 first. The second format comes ≥ 10 days later, with task order re-randomized (seeds recorded). Each rating carries confidence 1–5.
6. **Competency arm.** One session ≥ 10 days after the last task session. Raters rate the 40 competencies in both formats (order counterbalanced within the session). Raters are told nothing about which tasks link to which competency.
7. **Task attributes** (`fieldDependency`, `formationDependency`, reproduction regime) are rated once, in the F2 session. They are analysed under `protocol_reliability_study.md` block A rules.
8. **Burden** (planning estimate [J]): about 60–90 s per task per format, so roughly 3–4 hours per rater per format plus 1 hour for the competency arm. Time per unit is logged.

## 5. Interim check and stop rules

| Rule | Trigger | Action |
|---|---|---|
| **Interim futility** | After each group's first 50 units in its first format, single-rater α < .30 for any craft in **both** groups | Pause; the key panel reviews the codebook; the pilot restarts on fresh units (deviation logged). Allowed once |
| **Attrition** | A group falls below 5 raters completing both formats | Recruit a replacement with the same profile; the replacement rates all units. Analysis requires ≥ 5 raters per group with both formats |
| **Contamination** | A rater reports seeing prior craft labels, competency links or LLM output | Exclude that rater's affected sessions; replace |
| **Held content** | A held unit is found | Remove; log; notify TN |
| **Hard stop** | 10 weeks after the first rating | Analyse what exists under the same rules; report the shortfall |

## 6. Analysis (pre-registered; `validation/reliability.py`)

All statistics are computed per craft (FC, DC, SC) and per group, with unit-bootstrap 95% CIs (B = 10,000, recorded seed).

1. **F1 weights:**
   - ICC(2,1) and ICC(2,3), two-way random effects, absolute agreement [E-u: IO-085];
   - interval α (single rater);
   - **triad-consensus α** (`panel_split_alpha`, k = 3, interval, triad mean).
2. **F2 ordinal:**
   - ordinal α (single rater);
   - **triad-consensus α** (k = 3, ordinal, triad lower median).
3. **Defining craft (nominal):** nominal α (single rater) and triad-consensus α (k = 3, two-thirds majority; no majority counts as missing).
4. **F1 vs F2, like for like.** The paired difference in triad-consensus α (same units, same raters), with bootstrap CI. Triad-consensus α estimates the reliability of the 3-rater consensus value that production would use, so it compares formats on the quantity that would actually be displayed.
5. **Raters needed.** Spearman–Brown projection from ICC(2,1) to the number of raters for ICC ≥ .80 (F1). Panel-split α at k = 2 and k = 3 (F2) to choose production raters per task.
6. **Admissibility for the display gate.** Is the adopted format's single-rater α result admissible (≥ 120 units, ≥ 3 raters, pre-registered, blind, B ≥ 10,000)? If so, it is emitted in the `display_gates.yaml#agreement_result_schema` shape for `craft.FC/DC/SC`. It is computed separately per group and pooled across all 12 humans (missing-data α); the **pooled** result is the gate result.
7. **Group (a) vs (b).**
   - Difference in single-rater α per craft.
   - Cross-group α between group consensus values (do analysts and practitioners reach the same consensus?).
   - A cross-group α below .667 is reported as a **construct concern**: the codebook may measure analysts' reading rather than practice.
8. **Competency vs task level.** Single-rater α for competency-level ratings vs task-level ratings, same format; unpaired bootstrap of the difference. Convergent check: Spearman correlation between competency-level ratings and blends computed from linked task ratings (ADR-0005 §5: link-strength weighted).
9. **LLM arm (exploratory):**
   - run-to-run α across the 3 runs;
   - α between the LLM's majority value and each group's 6-rater consensus;
   - compared with the mean single-human α against the **other** group's consensus;
   - calibration of stated confidence.
   This is development-level evidence only. The pilot units are not held-out gold, so it cannot admit the LLM beyond G0 (`protocol_llm_coder_gate.md`).
10. **Burden and usability:** median seconds per unit by format; confidence by format; raters' stated preference (secondary; never decisive).

## 7. Decision rules (pre-registered; from ADR-0005 §7)

A scale must work for all three crafts, because the schema stores one scale per release. A criterion is met only if it is met **in both rater groups**. If it is met in one group only, the result is reported and the next rung down applies, unless CA decides otherwise on the record.

| Rung | Rule | Outcome |
|---|---|---|
| 1 | F1 ICC(2,3) lower bound ≥ .80 for FC, DC and SC, **and** F1 triad-consensus α ≥ F2 triad-consensus α (point estimates) for each craft | **Adopt weights** (`constant-sum-100`), 3 raters per task in production |
| 2 | Else: F2 triad-consensus α lower bound ≥ .667 for FC, DC and SC | **Adopt ordinal** (`ordinal-0-2`), labelled tentative where the lower bound is < .80 |
| 3 | Else: defining-craft triad-consensus α lower bound ≥ .667 | **Store defining craft only** (`nominal-defining`) at task level |
| 4 | None of the above | No craft values are displayed; codebook iteration 2 (fresh units). After a second failure, CA receives a change request to redesign the craft representation |
| A | Competency-level single-rater α exceeds task-level by ≥ .10 (same format), in both groups | Report to CA as evidence for moving toward v1 "Option A" (competency-level craft); does not by itself change the representation |
| L | LLM run-to-run α ≥ .80 and LLM-vs-consensus α within .05 of the mean single human | The configuration may proceed to the formal LLM-coder gate. Otherwise it stays G0 |

## 8. Pre-registration fields

All `preregistration_core.yaml#core_required` fields, plus:
- `unit_sets` (task and competency lists with SHA-256; strata and prior-label sources);
- `rater_groups` (composition, recruitment);
- `formats_and_counterbalancing` (incl. the four-bucket F1 change);
- `session_schedule` (≥ 10-day gaps; seeds);
- `statistics` (§6, incl. the triad-consensus definition and consensus rules);
- `decision_ladder` (§7, incl. the both-groups rule);
- `llm_configuration` (hash; 3 runs; exploratory status);
- `gate_emission` (§6.6).

## 9. Outputs

1. A decision memo to CA: the ladder outcome with all statistics; group differences; the Option A evidence; LLM status. If the scale is not `ordinal-0-2`, a change request to `vocab/crafts.yaml#rating_scale` and ADR-0005's status line.
2. Agreement results for `craft.FC`, `craft.DC`, `craft.SC` and `craft.defining` (if admissible), and for the task attributes rated in the F2 session.
3. Codebook PATCH with the key panel's rulings on contested calibration items (C6, C9, C12, C14; `codebook_craft_ratings.md` §8).
4. Report under `validation/studies/CSP-01/` (generated), including the burden table.

## 10. What the pilot cannot show

- That ratings are *correct*. That requires a gold set with adjudication (`spec_gold_sets.md`).
- That blends predict mobility. ADR-0023 rejects blends as the similarity measure.
- Anything about individuals: blends are never shown about people (ADR-0005 §8).
- Results generalize to raters like these. Twelve raters is a pilot. The production gate result accrues from the reliability study and gold-set coding as more raters join.
