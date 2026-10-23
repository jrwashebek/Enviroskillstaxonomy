# Specification: gold sets for EMST v2 rated layers and automated taggers (GS)

**WP-11 output 10** · Owner: IO (A8) for design and labelling rules; IA for linker gold-set tooling (ADR-0019); DE for storage, splits and SCORES.md generation · Status: draft for CA approval · Date: 2026-10-23
**Decision basis:** ADR-0024 §12 ("≥ 10% of tasks (≥ 60), stratified by module and craft, double-coded blind; SCORES.md per release; CI blocks automated taggers below threshold"); ADR-0019 §6 (600-item linker gold set); ADR-0022 (X2 two coders); P-DE-10 (LMPs gold-set pattern).
**Labels:** [E] evidence, [J] judgment, [S] speculation.

---

## 1. What a gold set is for

A **gold set** is a frozen, hash-pinned sample of units whose labels were produced by independent blind human coders and adjudicated. It measures **accuracy**: how close a coder or tagger comes to the best available human judgment. It complements, and does not replace, the **agreement** study (`protocol_reliability_study.md`), which measures reproducibility.

Gold sets serve four uses:
1. the LLM-coder gate (`protocol_llm_coder_gate.md`);
2. evaluation of automated taggers and the competency linker (ADR-0019);
3. regression tests for codebook revisions;
4. calibration and training sets for new human raters (development split only).

**Gold labels are never produced by agents.** Agent pre-fills are never shown to gold coders. A gold label is `reviewStatus = gold` on the L5 rating record (`vocab/evidence_labels.yaml#review_statuses`).

## 2. Size

| Gold set | Unit | Minimum size (computed at build from the release's counts; never typed) |
|---|---|---|
| **GS-TASK** craft, task attributes, work function, modes | v2 task | `max(ceil(0.10 × tasks in the release), 60)`. If an LLM gate is sought for any dimension: `max(that, 160)`, so the held-out split reaches ≥ 120 |
| **GS-EXPO** exposure constructs (a), (b), tacit | task (a, tacit); task × sector actor (b) | as GS-TASK, drawn as a stratified subsample of GS-TASK plus actor contexts |
| **GS-AUTH** authority position | de-identified position document | ≥ 60 (≥ 160 if an LLM gate is sought); plus SL's native state crosswalks used as external gold for X5 (ADR-0022) |
| **GS-IND** OBS-4 code, P/C/O/T flags, lint evaluation | indicator | `max(ceil(0.10 × indicators), 150)`; **every** indicator proposed for `useClass = select` is double-coded in addition (ADR-0024 §3) |
| **GS-G4** core vs home module | competency + linked tasks | ≥ 60 competencies, incl. all CA-referred boundary disputes |
| **GS-LINK** competency linker | plan component, posting or PD segment → EMST ID | 600 items per ADR-0019 §6 (IA owns tooling; IO's labelling rules apply) |
| **GS-X2** task → O*NET task/DWA mapping | EMST task | the P1-corridor tasks double-coded under ADR-0022; κ reported |

## 3. Stratification (applies to GS-TASK, GS-EXPO, GS-IND, GS-G4)

Sampling uses **prior labels only to stratify**: v1 values, Phase 4 agent drafts and home module. Priors are never shown to coders. Allocation, in order:

1. **Home module.** Core plus the nine wave-1 modules (`water`, `waterq`, `air`, `waste`, `envhealth`, `hazards`, `forest`, `wildlife`, `parks`). At least **6 units per module**; the remainder is proportional to the module's task count. **≥ 40% of units outside public lands and forestry** (P-DB-17).
2. **Prior craft.** Each prior defining-craft class (FC, DC, SC, multiple, none) ≥ 15% of units, except "none" (general practice) ≥ 5%.
3. **Prior work function.** Each of the 13 functions ≥ 3 units; WF-RULE, WF-RESOURCE and WF-RESPOND oversampled to ≥ 6.
4. **Boundary cases ≥ 20%.** These are:
   - v1 Delphi flags;
   - the craft integration points, except v1 integration point 2, which is held;
   - the pair-rule confusions in `codebook_work_function_authority.md` §A3;
   - CA-referred disputes.
5. **Text origin.** v1-carried, v1-rewritten, net-new, and D3 text that v1 inferred (≥ 20%, ADR-0005 §7) are each represented.
6. **Rare categories.** For every gated dimension, target ≥ 10 units expected per category: E3, robotics, system-executes, independent-verifier, funder, `on-site-preferred`. Draw targeted top-ups from module tasks (XR-07 subsectors). Categories that still have < 10 units are reported as "not estimable".
7. **Exclusions.** Held content never enters a gold set: Tribal-related records, `governedData = tribal`, and government-to-government relationship tasks (ADR-0007).

The sampling script, seed and frame snapshot are recorded. Each unit is pinned by `textSha256`. A unit whose text later changes is retired from the gold set, not relabelled in place.

## 4. Labelling

| Step | Rule |
|---|---|
| Coders | two qualified human coders per unit, coding independently and blind (XR-01). Qualification as in `protocol_reliability_study.md` §4. A coder may not label units they authored |
| Codebook | the dimension's codebook at a pinned version (`codebook_*.md`) |
| Adjudication | a third, senior human adjudicates every disagreement. The adjudicator sees both codes and rationales, not the coders' identities, and records a rationale. Agreements are spot-checked (10%) by the adjudicator |
| Gold value | the agreed or adjudicated value. Both original codes remain stored as atomic ratings (`reviewStatus = reviewed`); the gold value carries `reviewStatus = gold` |
| Cannot code | units either coder marks "cannot code" for the same reason are removed and logged. Units only one coder marks go to adjudication |
| Agreement reported | α between the two coders per dimension, with bootstrap CI. If the gold coders number ≥ 3 distinct people across ≥ 120 units, this result is also **admissible** for the display gate (`display_gates.yaml#admissibility`) |
| OBS-4 (GS-IND) | OBS-4 code and P/C/O/T flags (`docs/research/io-validation/indicator_writing_rules.md` §2). An indicator may carry `useClass = select` only if both coders independently give OBS-4 = 3 with no flags |

## 5. Splits and contamination control

- **Development split (25%)**: used to train human raters, tune prompts and fix codebook examples. May be published.
- **Held-out evaluation split (75%)**: used only for evaluation. Stratified like the whole. **Stored outside the public CC0 repo until each evaluation has run**, then published with the release. Held-out files carry canary strings; a contamination probe runs before each LLM evaluation (`protocol_llm_coder_gate.md` §6.3).
- **Rotation.** ≥ 20% of held-out units are replaced with newly sampled units each release. Retired held-out units move to development.
- **No leakage.** Prompt authors, codebook revisers and linker developers have no access to held-out labels. Access is logged.

## 6. Linker and crosswalk gold sets (IO requirements on IA- and FH-owned sets)

- **GS-LINK** (ADR-0019 §6): 600 items, double-annotated by human SMEs with IO, MELO layout, dev/held-out split, ≥ 40% from outside public lands, noise items labelled as such. The Phase 2 72-item set is single-annotator AI judgement and is **engineering data only** (ADR-0019 Context). It may seed development, never evaluation.
- **GS-X2:** two independent human coders per task with κ reported (ADR-0022). Disagreements are adjudicated and recorded with SSSOM `mapping_justification`. The weakest match type is retained.

## 7. Metrics and SCORES.md

Per gold set × dimension × coder or tagger (human, LLM configuration, linker version, lint version), **computed by the build and never typed**:
- n (held-out);
- α(coder, gold) with bootstrap 95% CI;
- per-category precision, recall and F1;
- abstention rate;
- calibration (LLM);
- P@1 and Hit@5 with CIs (linker);
- lint precision and recall against OBS-4 codes 0–1 and flags (GS-IND);
- date;
- codebook version;
- configuration or tool hash.

`SCORES.md` is generated per release, LMPs pattern (P-DE-10). Each row links to its study or evaluation ID.

## 8. CI enforcement (DE)

| Check | Rule |
|---|---|
| LLM-first values | rejected unless a passing LLM-gate decision exists for the dimension and configuration hash (`protocol_llm_coder_gate.md` §10) |
| Linker-derived ChangeSignals | must carry `linkerQuality{goldSet, precisionAt1, ci95}` from a GS-LINK held-out evaluation (ADR-0019 §5); uncorrected top-1 counts are never published |
| Select designation | every `useClass = select` indicator has two independent human OBS-4 = 3 codes in GS-IND |
| Gold integrity | gold labels carry `reviewStatus = gold`, ≥ 2 human coder IDs and an adjudication record where they disagreed; no `llm` or `emstagent:` ID among them |
| Held content | no unit with a Tribal flag in any gold file |

## 9. Pre-registration fields (gold-set construction)

All `preregistration_core.yaml#core_required` fields, plus:
- `gold_set_id`;
- `frame_snapshot`;
- `strata_and_minimums` (§3);
- `sampling_seed`;
- `coder_pool_and_qualification`;
- `adjudicator_rules`;
- `split_ratios_and_storage`;
- `rotation_plan`;
- `canary_ids`;
- `access_list` (roles, not names).

## 10. Maintenance

- Gold labels are corrected only through a change record (type E, errata) with a human reviewer and rationale. The old label is kept in history.
- A codebook MINOR change triggers relabelling of the affected dimension's gold units by two new coders. Until then, the gold set is marked stale for that dimension.
- Gold sets are re-sampled for every MINOR taxonomy release (annual), keeping the rotation rule.
