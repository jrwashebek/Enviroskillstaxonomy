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

## Phase 2 (after DATA_DONE.md)

- `python3 scripts/build_schema.py`: regenerated; `--check` current.
- Minted the eight m7 review tasks with the single writer (`mint_id.py promote-batch
  docs/build/rc1-fix/generated/promote_keys_build.txt --by emstagent:de-build-rc1-fix@claude-opus-5-5 --today 2026-10-25`):
  core TSK-43K3RCD, TSK-R34PM4N, TSK-SBZYHH1, TSK-K1JC1NN, TSK-RZ8F70W, TSK-EGRFG19; parks TSK-PZQBN33; wildlife
  TSK-201M258. New IDs only; none reused or re-pointed (ADR-0010). `mint_id.py verify`: OK, 10,480 rows.
- `validate_v2.py --strict --no-git-base`: 0 errors, 128 warnings. `migrate_v1.py --check`: OK.
- `update_readme_status.py`: README status block regenerated (schema draft.4, new counts); generated block only.
- CP re-issue: `site/ACR.md` (version evaluated: 2.0.0-rc.1 release profile) and `site/SECURITY_PACKET.md` (release
  covered, stop-gap inputs, point 7 under Q13 and withholding, point 6 profile).
- Running the one-command re-cut: `python3 scripts/recut_release.py --version 2.0.0-rc.1 --pending --as-of 2026-10-25`.
- Re-cut run 1 (`--pending`): schema check OK; two release builds byte-identical (123 files in SHA256SUMS, 10,436
  records, released 2026-10-25, stamp `be77601…+recut-pending-commit`); views regenerated; explorer 764 pages, 0
  problems; release docs written. The gate step stopped on a parsing bug (validator `--json` keeps counts in
  `stats.issues`); fixed in `release_gate.collect_ci`, gate re-run on its own.
- Reviewer scripts over the new dist: c1/c1b 0 schema failures after the documented inverse fields; 0 dangling refs;
  c1c registry OK (41 held candidate IDs, none released); c2b round trip loses only null-valued keys; c2c 438,035
  quads, every id a subject; c2d SKOS 1,628 concepts, 0 mapping triples (no human-reviewed row); c2e every SSSOM set
  parses with no row loss, strict renderings valid; c3 counts match; c4 triggers only in the exempt build statements
  and vocabulary SKOS; c4b recomputation without the overlay still differs for CMP-6035KC2 state, and the shipped view
  says `indeterminate (basis withheld)`; c8 0 positive NoTermFound rows; Frictionless VALID.
- Gate re-run (`release_gate.py --run-ci --twin`): items 1-4 and 8 pass, 5 conditional (M10 leaves 16 of 28 P1-P2
  federal variants without a series profile and 26 of 30 state variants without a class view), 6 and 7 fail.
  pytest 472 passed; validator 0 errors (128 warnings) in both modes; `npm test` OK (764 pages, 0 problems; 71
  pages, 0 axe violations). `GATE_REPORT.md`, `gate_evidence.json`, `RELEASE_NOTES.md`, `counts.json` (counts@1.2.0),
  `delta_v1.json`, `BUILD.md` regenerated; `release_docs.py --check` current.
- `site/tools/sbom.mjs` keeps the committed SBOM when only npm's random serial and timestamp change, so a rebuild of
  the same tree leaves it clean.
- For the orchestrator: commit, then run `python3 scripts/recut_release.py --version 2.0.0-rc.1` from the clean
  commit (stamp = HEAD), then commit the regenerated `docs/release/2.0.0-rc.1/` before tagging. Nothing committed or
  tagged by D-BUILD.
