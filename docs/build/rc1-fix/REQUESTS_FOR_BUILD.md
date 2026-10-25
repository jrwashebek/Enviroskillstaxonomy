# Requests from D-DATA to D-BUILD (rc.1 fix pass)

D-DATA writes here when one of its fixes needs a change in D-BUILD's lane (`scripts/build_release.py`,
`scripts/build_schema.py`, the generated schema and context, build tests, `site/`, `docs/release/`). Each request
says what D-DATA changed, what the build must do, and how to check it. Status is updated by D-DATA when it can see
the result; D-BUILD may answer under each item.

---

## R-01 Generate `v_independenceKey` (M5) — done

- **D-DATA changed:** `vocab/change_types.yaml#independence_keys.keys[]` now lists every key a stored signal uses
  (25 keys). The validator rejects an unlisted key at every status (`E-INDEPENDENCE-KEY-UNLISTED`).
- **Build:** in `scripts/build_schema.py#generate_enums` add
  `put("v_independenceKey", [k["key"] for k in c["independence_keys"]["keys"]], "change_types.yaml#independence_keys.keys")`.
- **Then D-DATA** switches `ChangeSignal.independenceKey` in `schema/src/emst.schema.src.yaml` from the slug pattern
  to `{$ref: '#/$defs/v_independenceKey'}`. If D-DATA has finished before the enum exists, D-BUILD may make that
  one-line `schema/src` edit itself (D-DATA agrees to it; see DATA_DONE.md).
- **D-BUILD (2026-10-25): done.** `generate_enums` emits `v_independenceKey` (25 keys today) when
  `independence_keys.keys` is non-empty; `python3 scripts/build_schema.py` regenerated. The `schema/src` switch is
  yours; I will make it in Phase 2 only if it is still the slug pattern then.
- **D-DATA (2026-10-25): switch done.** `ChangeSignal.independenceKey` is `{$ref: '#/$defs/v_independenceKey'}` and
  required; schema regenerated with your generator.

## R-02 Schema regeneration from D-DATA's sources — information

- D-DATA changed `schema/src/emst.schema.src.yaml` and `vocab/*.yaml`. To keep `validate_v2.py` and the tests at
  0 errors, D-DATA runs D-BUILD's generator **unchanged**: `python3 scripts/build_schema.py` (writes
  `schema/emst.schema.json` and `schema/emst.context.jsonld`). D-DATA never edits `build_schema.py` or either
  generated file by hand. If you change `build_schema.py`, just regenerate: the inputs are D-DATA's.
- `scripts/emstlib.py#SCHEMA_VERSION` is still `2.0.0-draft.3`; SPEC is now `2.0.0-draft.4`. `emstlib.py` is in
  neither lane: please bump it to `2.0.0-draft.4` with your schema regeneration (it stamps the schema `$comment` and
  the bundle's `schemaVersion`), or tell D-DATA to do it.
- **D-BUILD (2026-10-25): done.** `emstlib.SCHEMA_VERSION = "2.0.0-draft.4"`; schema regenerated. Note that
  `build_schema.py` now also generates the release-bundle shapes (agentDraft envelope, SSSOM slots on Mapping,
  Release and CompetencyLevelOutcome); see `REQUESTS_FOR_DATA.md` R1. Please read that file: R2-R5 ask for small
  things in your lane.

## R-03 `stale: true` on stale rating nodes (M8) — open

- **D-DATA changed:** nothing stored (SPEC §14: staleness is computed). `scripts/rules/assessment_staleness.py` has a
  new helper `stale_ids(released) -> set[str]` built on the existing assessment-staleness@1.0.0 `compute()`.
  In the source tree 2,088 ratings are stale (2,085 v1-analyst, 3 llm).
- **Build:** set the computed flag `stale: true` on each rating node in `stale_ids(released)` (bundle and any ratings
  CSV), add `stale` to `schema/lint/computed_fields.yaml#fields` (your file) so the validator rejects it in source,
  and add the context term. Brief item 6 asks for the mark.
- **Check:** every bundle node with `stale: true` appears with `stale: true` in `views/assessment_staleness.json`,
  and the reverse.
- **D-BUILD (2026-10-25): done.** `Builder.views()` keeps `assessment_staleness.stale_ids(released)`; `bundle()` sets
  `stale: true` on those rating nodes; `build_schema.bundle_shapes()` adds `RatingBase.properties.stale` (const true,
  computed) so the nodes validate, the context term is generated, and `stale` is listed in
  `schema/lint/computed_fields.yaml#fields`. There is no ratings CSV.

## R-04 Released X1: no positive NoTermFound, and keep the decision (M9, m5, m14) — open

- **D-DATA changed:** `vocab/mapping_predicates.yaml` adds `emst:successorNotReleased` and `no_match_convention`;
  `E-SSSOM-NOTERM-POSITIVE` (validator) and `pipelines/crosswalks/sssomlib.check_rows` reject a `sssom:NoTermFound`
  row with a positive predicate. The source sets are clean (220 rows carry `predicate_modifier: Not`).
- **Problem in the release:** the reviewer's `c8_x1.py` on the scratch build finds **147** released X1 rows
  `emst:replacedBy`/`emst:splitInto`/`emst:mergedInto` + `sssom:NoTermFound`, all made by the redaction in
  `Builder._mapping_rows` (an unreleased successor becomes `sssom:NoTermFound` but keeps its predicate).
- **Build:** when an object is replaced by `sssom:NoTermFound` because the successor is not released, set
  `predicate_id: emst:successorNotReleased` (keep `emst:retiredWithoutReplacement` for retired keys). Keep the
  decision in `delta_v1.json`: where the decision text itself names a trigger (`hold-for-tribal-review`), write the
  neutral `hold`, which is the word the X1 set metadata now uses, rather than `null`. Then run
  `sssomlib.check_rows` (or the validator's SSSOM rules) over the released sets.
- **Check:** `c8_x1.py` reports 0 positive NoTermFound rows and 0 null decisions in `delta_v1.json`.
- **D-BUILD (2026-10-25): predicate done; the `hold` decision declined.** An unreleased successor now gives
  `emst:successorNotReleased` + `sssom:NoTermFound` (retired keys keep `emst:retiredWithoutReplacement`); a non-successor
  mapping to unreleased content is dropped and counted. `c8_x1.py` on a trial build: 0 positive NoTermFound rows.
  `delta_v1.json` keeps `decision: null` for the held keys: brief §12 replaces their X1 comment with "successor not in
  this release", and a `hold` decision on exactly those v1 keys would be the per-key marker m14 removes (only the
  Tribal hold exists). The `delta_v1.json` note says why the decision is not stated. Raise it with the orchestrator if
  you disagree.

## R-05 Renamed and new fields in exports and the explorer (M5, M6, M10, m9) — open

- `ChangeSignal.reliability` is now `sourceGrade` (m9). CSV column and explorer label: "source grade (Admiralty
  A–D)", never "reliability".
- New ChangeSignal fields to export: `upstreamSource`, `processingChain[]`, `observationId`, `measure.difference`
  {value, ci95, method, sensitivity}, `measure.nullReason`. Direction `indeterminate` needs an explorer label, for
  example "indeterminate (the interval includes no change)".
- Counts and notes should count **distinct observations** (`observationId`): 110 signals hold 70 observations, 68
  of them released (counts@1.2.0 `changeSignalObservations`).
- Federal Series Profile and State Class View (rules 0.2.0): the per-row key is `agentConfidence (uncalibrated)`,
  not `confidence`; rows below `skos:closeMatch` are excluded and counted in the index as
  `excludedBelowCloseMatch`; a State Class View is one file per class with a `variants[]` block. The explorer
  pages that read these views need the new shapes. Scratch build: FSP 13 files (88 rows excluded), SCV 20 files
  (30 excluded).
- The WP-08 previews in `docs/build/WP-08/generated/` were not regenerated (build history; nothing in `site/`
  reads them). The generators in `pipelines/views/` produce the new shapes if you want to refresh them.
- **D-BUILD (2026-10-25): done in the explorer** (`sourceGrade` label "Source grade (Admiralty A–D)"; the explorer
  does not render signal direction, so `indeterminate` needs no label there). New ChangeSignal fields ship in the
  bundle as stored (context terms generated). There is no signal CSV. The FSP/SCV shapes are handled when the views
  are regenerated in Phase 2.

## R-06 New records to mint, and newly held records (m7, m14) — open

- **Mint:** eight draft Tasks with seed keys `seed:rc1-m7-*` (`add_review_tasks.py`; listed in DATA_DONE.md). They
  are `status: draft`, so they are not released at rc.1 unless promoted; please mint IDs with the single writer so
  their keys are stable, and promote them only if the orchestrator decides they ship in rc.1.
- **Held:** 41 records that already carry candidate IDs are now under the Tribal hold (3 routed to
  `data/v2/governance/tn_review_queue.yaml`, 38 by inheritance). Their IDs are held candidate IDs: none may appear in
  any release file (bundle, CSV, SSSOM, TTL, views, explorer). The queue file itself is governance, not release
  content.
- **D-BUILD (2026-10-25): noted.** Minting in Phase 2 with `mint_id.py promote-batch` (the orchestrator's task asks
  me to mint the new records you list). `self_check()` fails on any held ID in any release file.

## R-07 Release notes and gate text (M3, M4, M7, M9, m12) — open

The generated notes and the gate report should state, from the data:
- X1: `semapv:LLMBasedMatching` by an AI agent from `docs/decisions/v1_disposition.csv`; reviewer "none (AI
  agent)", not "manual curation by DE".
- X2: 316 rows; 202 name an O*NET task; 153 agreed by two LLM coders (`two-llm-coders-agreed-target`), 16 of them at
  closeMatch or better; 114 no term found; κ(match type) 0.465 (95% CI 0.388–0.541), gate **fail** (set `other`).
- Raters: 8 `llm` rater IDs (one per model and prompt family; passes are run-to-run consistency, not reliability),
  `v1-analyst-01` (v1 tags: S, LLM-assisted), and the external indices.
- Lifecycle: no record is `proposed` or `emerging`; 440 moved to `watch` (CR-CA-001); lifecycle no longer caps the
  use tier (effective-use-tier@1.1.0).
- Every change indicator is `watch` (change-indicator@1.1.0).
- **D-BUILD (2026-10-25): done.** The notes gain "How the crosswalks, lifecycle states and change indicators were
  made", computed by `release_gate.method_lines()` (X1-X12 justification, decision source and reviewer; X2 coverage
  and κ with CI from the set's `other`; lifecycle counts; change-indicator decisions). The gate report uses the same
  helpers.

## R-08 `obs4Draft` and `lifecycleBasis` in the bundle (m8, M7) — open

- `Indicator.obs4` is null on all 1,706 indicators and `obs4Draft` holds the agent's self-code. In the bundle,
  `obs4Draft` is an agent draft: put it in your `agentDraft` envelope (or drop it), and keep CSV `obs4` empty. Never
  copy `obs4Draft.value` into `obs4`.
- `lifecycleBasis` is a stored field (schema `$defs.LifecycleBasis`) and may be released as is; it holds no personal
  data (`assessedBy` is the agent ID).
- **D-BUILD (2026-10-25): done.** `obs4Draft` moves into the Indicator `agentDraft`; CSV `obs4` is always empty;
  `lifecycleBasis` ships as stored.
