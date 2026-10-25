# rc.1 fix pass: D-DATA worklog (IO, LM, IA, CA codes; AI agent)

Brief: `docs/review/DATA_FIX_BRIEF.md` (binding). Findings: `docs/review/data_method_review.md`.
Lane: `schema/src/`, `vocab/`, `data/v2/`, `scripts/validate_v2.py`, `scripts/rules/`, `scripts/migrate_v1.py`,
`pipelines/` (x2, crosswalks, views), `validation/`, `docs/standard/` (SPEC → 2.0.0-draft.4, AUTHORING_GUIDE),
build-plan and brief wording for M4, ADR-0032, and `docs/package/report/figures/build_figures.py` (m13 only).
Findings: M2–M10, m5–m10, m13, m14 (data parts). Every data edit is a re-runnable script in `docs/build/rc1-fix/`.

## 2026-10-25

### Baseline (before any edit; tree at b8fea76)
- `validate_v2.py`: 0 errors, 156 warnings. `--strict`: 0 errors, 156 warnings
  (W-INDEPENDENCE-KEY-UNLISTED 74, W-LINT-* 48, W-REF-DEFERRED 19, W-X1-DEFERRED 12, W-SUPERSEDED-TARGET 3).
- `pytest -q tests`: see below.
- Validator run time is about 75 s per mode on this 2-CPU container; runs are serialised.

### Plan
Phase A (schema and vocabulary first, so D-BUILD can work against them): M2, M4, M5, M6, M7, M8, m8, m9 fields and
terms; regenerate the schema with D-BUILD's unchanged generator (requests in REQUESTS_FOR_BUILD.md).
Phase B (data, by script): M2, M4, M8 via migrate_v1 and rating scripts; M5/M6 signals; M7 lifecycle; M3/M9/m14
crosswalks; m5, m6, m7, m8, m10 records; M10 view rules; m13 figure script.
Phase C: validator rules and tests per finding; SPEC draft.4, AUTHORING_GUIDE, ADR-0032, DECISION_LOG; DATA_DONE.md.
- True baseline failure before any edit: `tests/test_migration.py::test_migration_is_deterministic_and_current`
  (MIGRATION_INFO.json stale: `PROJECT_LEAD_DECISIONS.md` changed after the migration last ran). Fixed by the
  migrate_v1 regeneration below.

### Phase A: vocabulary and schema (done)
- `vocab/change_types.yaml`: direction `indeterminate` with definitions; `independence_keys` lists all 25 keys a
  signal uses (13 added; agency self-reports and enacted-appropriations readings share providers); new
  `processing_chain_steps` and `observations`; `signal_reliability` documented as `sourceGrade`; projection family
  `confidence_cap` and `direction_rule`.
- `vocab/lifecycle_states.yaml` (CR-CA-001): `established` = long-standing work, validation is validationStatus;
  `watch` may label L1-L4 records; `max_use_tier` removed; machine-readable `entry_test` for proposed and emerging.
- `vocab/exposure_instrument_v2.yaml`: `intensityRank`; EMST E3 is not Eloundou's E3; v1 mapping is documentation only.
- `vocab/mapping_predicates.yaml`: `emst:successorNotReleased`; `no_match_convention`; `review_statuses` incl.
  `two-llm-coders-agreed-target`.
- `schema/src`: LifecycleBasis + `lifecycleBasis` (required for proposed/emerging from candidate); Indicator `obs4`
  nullable + `obs4Draft`; Competency `levelSpanBasis`; RatingBase `validationStatus` required, `passIndex`,
  `sessionId`, `sampleFrame`, v1-analyst constants (S, llm-assisted, toolVersion/promptVersion), llm needs
  passIndex+sessionId; ExposureAssessment v1-analyst carries no v2 construct field, `mappingRule` removed;
  ChangeSignal `sourceGrade` (was reliability), `upstreamSource`, `processingChain`, `observationId`,
  `independenceKey` required and `$ref v_independenceKey` (D-BUILD added the enum, R-01), `measure.difference`,
  `measure.nullReason`.
- Schema regenerated with D-BUILD's unchanged generator (`python3 scripts/build_schema.py`), R-02.

### Phase B: data, by script (all idempotent; second runs change nothing)
- `scripts/migrate_v1.py` 1.1.0: v1 ratings S / llm-assisted / toolVersion "unknown (v1 sessions)" / promptVersion
  "legacy/v1 working records" / validationStatus draft; no deploymentMode, sWatch, tacitExperienceRequirement or
  mappingRule; X1 `semapv:LLMBasedMatching` + `other: decision_source=...`; holds applied to v1 ratings of held
  records (`apply_holds`). `--check` OK.
- `fix_ratings.py` (M4, M2, M8): 4,107 llm ratings -> one raterId per model+prompt family, passIndex, sessionId,
  caveat in method; validationStatus on all ratings; sampleFrame on the 171 emst-exposure@2.0 records.
- `openlmp_difference.py` + `fix_signals.py` (M5, M6, m9): team stream reproduced for all 10 OpenLMP signals;
  difference intervals stored; 5 OpenLMP signals indeterminate (6SMSZRG plans-only, 4G9Z4EK, SS0M0J6, HGAGZE8,
  EDTT3Y9), SIG-84J3FBK indeterminate, SIG-VFA30PA indeterminate (below baseline), 43 broadMatch BLS -> low,
  confidence harmonized within observations; 70 distinct observations (68 released) of 110 signals.
- `fix_lifecycle.py` (M7): 440 records proposed/emerging -> watch with lifecycleBasis (8 roles, 26 competencies,
  44 variants, 147 tasks, 201 indicators, 3 enactments, 11 pathways); list in generated/lifecycle_changes.csv.
- `fix_records.py` (m5, m6, m8, m10): derivedFrom on 4 successor competencies; 5 L5 spans -> L4 and
  levelSpanBasis on 224 competencies; obs4 -> null + obs4Draft on 1,706 indicators; 38 state class records url-only.
- `fix_holds.py` (m14): 3 records routed to `data/v2/governance/tn_review_queue.yaml`, 38 held by inheritance.
- `fix_crosswalks.py` (M9, m14): 220 NoTermFound rows get predicate_modifier Not in 9 sets; X2 status renamed (198)
  and kappa plus honest numbers on the set; 129 held_variants markers dropped; metadata reworded (D-BUILD R3).
- `add_review_tasks.py` (m7): 8 draft review tasks (seed keys; need minting).
- `fix_rules.py`: role-change@0.2.0, federal-series-profile@0.2.0, state-class-view@0.2.0, counts@1.2.0 (D-BUILD
  R4); change-indicator@1.1.0 and effective-use-tier@1.1.0 written with their code.
- Pipelines updated so a re-run gives the same shapes: sssomlib (NoTermFound convention, no held marker), x3, x4,
  x8, x2 merge (status, kappa on set), views FSP/SCV (M10), change_view (sourceGrade).

### Validator after Phase B
- Normal: 0 errors, 132 warnings (W-LINT-PRODUCTION-REVIEW 46 new, W-OBSERVATION-SPLIT 4 false positives fixed by
  adding denominator and subject to the split key).
- After the fix: normal 0 errors; `--strict` 0 errors, 128 warnings (W-LINT-PRODUCTION-REVIEW 46, W-LINT-LENGTH 35,
  W-REF-DEFERRED 19, W-X1-DEFERRED 12, W-LINT-TYPING 8, W-LINT-INDICATOR 5, W-SUPERSEDED-TARGET 3).

### Phase C: validator rules, tests, documents
- `scripts/validate_v2.py`: new codes E-INDEPENDENCE-KEY-UNLISTED (every status), E-PROCESSING-CHAIN-STEP,
  E-OBSERVATION-INCONSISTENT, W-OBSERVATION-SPLIT, E-DIRECTION-INDETERMINATE, E-PROJECTION-CONFIDENCE,
  E-PROJECTION-DIRECTION, E-MEASURE-NULL-REASON, E-LLM-RATER, E-LLM-PASS-METHOD, E-LLM-PASS-DUPLICATE,
  E/W-LIFECYCLE-BASIS, E/W-LEVELSPAN-BASIS, E/W-OBS4-SELF-CODED, E-SCR-HASH, E-SSSOM-MANUAL-AGENT,
  E-SSSOM-NOTERM-POSITIVE, E-SSSOM-AGREEMENT-LABEL, E-SSSOM-HELD-MARKER, E-TN-QUEUE, W-LINT-PRODUCTION-REVIEW.
- `validation/lint_indicators.py`: an uncoded OBS-4 (null with obs4Draft) is PR-3 pending, not missing.
- `scripts/rules/assessment_staleness.py`: `stale_ids()` for the bundle flag (R-03).
- Tests: `tests/test_rc1_data_fixes.py` (44 collected), plus updates to the evidence-rule cases (C22-C27), fixtures,
  `test_rules.py`, `test_validate_v2.py`. Reviewer checks: c5, c6, c7 (all 10 MATCH), c8 (source clean; 147 positive
  NoTermFound rows only in the released X1, from redaction: R-04), c4 (only EXT cultural-resources mentions).
- m13: `build_figures.py` labels by the difference interval; tested in a scratch mirror; package outputs not
  regenerated (package edit).
- Docs: AUTHORING_GUIDE (rule 3, examples, the repeated-passes rule, v1 tags, §12 rows 7 and 10, new §14);
  PHASE4_BUILD_PLAN §WP-03 and S1_AUTHORING_BRIEF ("repeated"); SPEC 2.0.0-draft.4 with "Changes since draft.3";
  ADR-0032; CR-CA-001; DECISION_LOG rows DP-31 and CR-CA-001.
- Requests: REQUESTS_FOR_BUILD R-03..R-08 written; REQUESTS_FOR_DATA R1-R6 answered (R5 declined: keep the overlay).
- `tests/test_authoring_guide.py` passes after the guide edits; `pipelines/views/tests` pass.

### Final checks
- Full `pytest -q tests` (471 tests): 3 failures on the first run. `test_migration.py::test_v1_tags_are_prior_evidence_only`
  still asserted the v1 XR-04 mapping (deploymentMode/sWatch) that M8 removed; updated to assert the M2/M8 invariants
  instead. The two `test_build_release.py` failures came from D-BUILD editing that file during the run (the current
  test reads the active rule versions); all three pass on re-run.
- `validate_v2.py` and `--strict`: 0 errors, 128 warnings. `migrate_v1.py --check`: OK. `build_schema.py --check`: current.
- TN queue reasons reworded to name the review finding only (the file says "IDs only, never content"); `fix_holds.py`
  re-run, only the queue file changed.
- AUTHORING_GUIDE §12 rows 16-17 point to §14 (lifecycle is no longer an effective-tier cap).
- Second full run after those edits: `pytest -q tests` 472 tests, 0 failures; `--strict` 0 errors, 128 warnings.
- `DATA_DONE.md` written. Lane done.
