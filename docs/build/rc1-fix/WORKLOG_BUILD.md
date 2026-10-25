# rc.1 fix pass: D-BUILD worklog (DE, CP codes; AI agent)

Brief: `docs/review/DATA_FIX_BRIEF.md` (binding). Findings: `docs/review/data_method_review.md`.
Lane: `scripts/build_release.py`, `scripts/build_schema.py` + generated schema, `schema/emst.context.jsonld`,
`tests/test_build_release.py` + new build tests, `site/`, `docs/release/`, `docs/methods/WP15_SIGNOFF.md`,
gate item 7 text in `docs/decisions/PHASE4_BUILD_PLAN.md` §5.

## 2026-10-25

- Read the brief, the review, ADR-0031, SPEC §12, §17, §18, `docs/release/2.0.0-rc.1/`. Tree clean at `cd7a279`.
- Baseline `pytest -q tests`: 1 failure, `test_migration_is_deterministic_and_current` (D-DATA's in-progress
  `vocab/` edits; not in this lane). Full suite takes about 8.5 min.
- Wrote `REQUESTS_FOR_DATA.md` (R1 FYI on generated bundle shapes; R2 obs4 null; R3 trigger text in SSSOM
  metadata and `held_variants`; R4 counts@1.2.0; R5 venue overlay).
- New `scripts/agent_draft.py`: the agentDraft envelope (hosts and fields from `validation/display_gates.yaml`),
  its inverse `fold()`, and `add_to_schema()` for the generator.
- `scripts/build_schema.py`: `bundle_shapes()` (AgentDraft<Host> defs, `agentDraft` on hosts with "in place or
  agentDraft" required-ness, SSSOM slots on Mapping, Release and CompetencyLevelOutcome defs); context terms for
  `other`, `mapping_tool`, `mapping_tool_version`, `creator_id`, `see_also` and the StateClassRecord sub-keys;
  `agentDraft` as `@json`; `v_independenceKey` enum (D-DATA R-01). `emstlib.SCHEMA_VERSION` -> 2.0.0-draft.4
  (R-02). Schema regenerated.
- `schema/lint/computed_fields.yaml` (owner DE): `agentDraft` listed, so no source record may carry it.
- `scripts/build_release.py`:
  - B1: `_lang` is schema-driven (`schema_text_paths()`: only Text/LangMap-typed paths, field names in
    `TEXT_FIELDS_TO_LANG`); `close()` holds back a record whose required field redaction would empty, to a fixed
    point; `self_check()` adds `schema_check()` (every node: records minus documented inverse fields, Mapping,
    Release, CompetencyLevelOutcome), `context_check()` (every key a term) and `trigger_scan()` (m14).
  - M1: `agentDraft` envelope in the bundle (labels from `views/display_gate.json`, so views now run before the
    bundle); CSV `tasks.csv` `*_status` columns; `indicators.csv` `use_class_declared`, `obs4` empty,
    `effective_use_tier`; `competencies.csv` `effective_use_tier`; manifest notice names all of it.
  - M11: Mapping nodes typed (numeric, multivalued) with `other` and `mapping_tool`; SKOS mapping triples only for
    pid:-reviewed rows; `mappings.csv` adds `mapping_tool`, `other`.
  - m1: `check_build_commit()` (refuses `+uncommitted`, or a bare sha that is not a clean HEAD; allows
    `<HEAD>+recut-pending-commit`); `SOURCE_DATE_EPOCH` ignored under release profile. m2: `created` datetime.
  - m3, m11, m12, m15: notes carry the publication status line (from `release_gate.publication_status`), ID
    stability, omitted SPEC §12.5/§17.2 artifacts, ratings by rater type and distinct units (counts@1.2.0 fields
    switch on with that rule version). HCM `notice` column carries the ID note.
  - m4: `venue_overlay()` sets `indeterminate (basis withheld)` where an actor enactment lost a requires, enables or
    constrains link to redaction. m14: X1 comments say "successor not in this release"; `held_variants=` stripped.
- New `scripts/release_gate.py` (publication status for items 6-7; evidence collection; generated GATE_REPORT.md),
  `scripts/recut_release.py` (the one-command re-cut), `docs/release/2.0.0-rc.1/PUBLICATION_SIGNOFF.yaml` (empty
  record: no human review, no signature). `scripts/release_docs.py` BUILD.md documents the re-cut command.
- Sign-off path (brief §11, Q13): build plan §5 item 7 and the WP-15 heading; `docs/methods/WP15_SIGNOFF.md` header,
  §4, closing check and new §5. No human sign-off recorded anywhere.
- Trial release build of the current tree (scratch): 0 schema failures (reviewer c1/c1b), frictionless VALID (m2),
  round trip loses only null-valued keys, 3 records held back (TL-GJKKYR2, TL-HR0B6Z3, WCH-6ZCVRRF), 15 venue rows
  indeterminate (CMP-6035KC2 state among them), trigger scan blocked only by R3 texts in D-DATA's lane.
- New tests: `tests/test_agent_draft.py` (9), `tests/test_jsonld_roundtrip.py` (4), `tests/test_release_gate.py` (6),
  10 more in `tests/test_build_release.py`. All pass.
- `obs4Draft` (D-DATA's m8 field: the agents' OBS-4 self-code) added to the Indicator agentDraft host.
- Explorer: `site/lib/model.mjs`, `src/_includes/macros.njk`, `src/roles/variant.njk`, `src/federal-series/series.njk`
  render `indeterminate (a linked instrument is withheld from this release)` for withheld-basis venue rows. A trial
  explorer build from the trial release: 764 pages, 0 problems; `npm test`: 71 pages, 0 axe violations, OK. No page
  shows a field dependency, formation dependency, time share or importance value.
- Trial gate report (scratch) renders all eight items; X4 now counts only the variant -> series set.
- Test assertions on rule versions now read the active rule (D-DATA bumped effective-use-tier and change-indicator
  to 1.1.0). Both real-tree build tests pass now that D-DATA reworded the R3 texts.
- Phase 1 done; waiting for `DATA_DONE.md`.
- D-DATA requests R-03..R-08 (answered in `REQUESTS_FOR_BUILD.md`): `stale: true` on stale rating nodes (2,003 in a
  trial build, equal to the staleness view) with `RatingBase.stale` in the generated schema and `stale` in
  `computed_fields.yaml`; unreleased successors -> `emst:successorNotReleased` + NoTermFound (0 positive NoTermFound
  rows by `c8_x1.py`), non-successor mappings to unreleased content dropped; `hold` decision in `delta_v1.json`
  declined (would re-create the m14 marker); notes gain a computed method section (crosswalks, X2 coverage and κ,
  lifecycle, change indicators); explorer: `sourceGrade` labels, watch-state records listed as "may be forming",
  use-tier text without the lifecycle cap.
- Tests: `test_m8_stale_ratings_are_marked_in_the_bundle`, `test_m9_unreleased_successor_is_never_a_positive_no_term_found`.
- Ran `pipelines/views/build_views.sh` early to test the explorer against the M10 view shapes. Explorer (my lane):
  series and class pages list only closeMatch-or-stronger crosswalk rows, with the rest in an "Unreviewed agent
  candidates (not an alignment)" section; every confidence shown is "agent confidence (uncalibrated)"; the model
  reads only the HR view files the generators' indexes list (23 FSP and 17 SCV files are stale leftovers; R7 to
  D-DATA). Build: 764 pages, 0 problems.
- Candidates disclosure uses the existing `emst-disclosure` style (24 px target); `npm test` OK (71 pages, 0 axe violations).
