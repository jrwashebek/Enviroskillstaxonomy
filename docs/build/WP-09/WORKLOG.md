# WP-09 Crosswalks X1–X12 — worklog (A2 IA)

Owner: A2 IA (Workforce Systems Interoperability Architect / Skills Intelligence Engineer).
Co-owners for named sets: FH (X3–X5, X9), SL (X5), LC (X6, X10, X12 with DC), PS (X8, X11), DC (X12).
Binding inputs: ADR-0022, ADR-0019, ADR-0013, `vocab/mapping_predicates.yaml`, SPEC §15, AUTHORING_GUIDE.
Labels: [E] evidence, [J] judgment, [S] speculation.

All rows in every set written here are **agent drafts**: `raterType`-equivalent is the author ID
`emstagent:ia-wp09@phase4` (model `claude-opus-5-5`, prompt `wp09-crosswalk@1`), `review_status=candidate`
in `other`, no human reviewer, evidence label S unless the row cites an external code check (E). Nothing here is
a reviewed or selection-grade mapping (ADR-0022 §4). **No public alignment claim may rest on these sets.**

## Conventions adopted (pending WP-08 / CA confirmation — see CR-IA-001)

- Role keys: `seed:<role_key>` from `docs/decisions/mvp_role_set.csv` (e.g. `seed:R11-environmental-permit-writer`).
  Variant keys: `seed:<role_key>/<sector_actor>` (e.g. `seed:R11-environmental-permit-writer/state`).
  When WP-08 mints different keys, rows are re-keyed by `pipelines/crosswalks/rekey.py` (no hand edits).
- Register records (CR-DE-002, no TYPE prefix yet): `seed:opm-series/<code>`, `seed:state-class/<jur>/<code>`.
- External code namespaces: see each `.sssom.yml` `curie_map`. IDs only in CC0 files (ADR-0013 §5).
- Every row carries in `other`: `weakest_match_type=…;review_status=…;evidence=…` plus set-specific keys; the
  rationale is in `comment` (EMST-authored text, never upstream text).

## Session log

- 2026-10-23: read brief, build plan, ADR-0013/0019/0022, SPEC §15, mapping vocab, validator SSSOM rules,
  Phase 2 crosswalk method and prototype, FH/SL/LC/PS inputs, V1–V4 verification.
- Network: shell reaches PyPI and raw GitHub only; onetcenter.org, esco.ec.europa.eu, bls.gov and
  huggingface.co return proxy 403 (not retried). O*NET 31.0 and ESCO v1.2.1 bulk files could not be
  downloaded this session; see version-gap notes in X2 prep and X7.
- X3 built: `pipelines/crosswalks/x3_soc.py` + `curation/x3_role_soc.csv` → `data/v2/crosswalks/onet-soc/2019` and
  `soc/2018`. All 37 MVP roles covered; verified v1 errors recorded as `predicate_modifier: Not` rows (F10→19-1012,
  F12→33-2021, F8→23-1011, F11→25-4031, F13→29-9021) plus ADR-0022 §5 additions. Codes checked offline against
  O*NET 27.2 data-level occupations (O*NET-SOC 2019) and BLS OEWS May 2021 (SOC 2018) — `reference/*.txt`.
  Finding: mvp_role_set R19 cited stale O*NET-SOC 2010 code 19-1031.01 (CR-IA-001, accepted).
- CR-IA-001 (role/variant seed keys; series and SOC errata) and CR-IA-002 (`semapv:LLMBasedMatching` is not valid
  in the SSSOM 1.0 schema) opened and **ruled by CA the same day** (both accepted). `validate_sets.py` reports
  strict-1.0 and 1.0+1.1-values results with the affected-row count, reading
  `vocab/mapping_predicates.yaml#justifications_sssom_1_1_only`.
- X4 built: `x4_opm_series.py` → SeriesRecords in `data/v2/registers/opm_series/` (FH's 73 + 6 added for MVP
  coverage: 0201, 0601, 1712, 1801, 5408, 5409 — titles IA judgment, FH to verify); 15 series
  `proposed-realignment` per the CHCO memo re-read 2026-10-23 (0408/0482/0486 are NOT proposed);
  `crosswalks/opm-series/2026-10-23` (role→series) and `opm-series-competency/2026-10-23` (FH core/supporting
  judgments chained through X1; rows on held v1 codes omitted).
- X5 built: `x5_state_classes.py` + `curation/x5_classes.yaml`, `x5_variant_class.csv` → StateClassRecords in
  `data/v2/registers/state_classes/` (TX, WA, Lewis County WA EH, Philadelphia Water Department) and five sets
  (`state-class-tx|wa|pa`, `local-class-wa-lewis-county`, `local-class-pa-philadelphia-water`). PA class codes are
  not exposed in postings: PA rows are position overrides (allowed for pilots) with `register_record=pending`.
  Spec text stored as URL + null hash (hash-and-URL rule). Records name variants as `roleVariantKey` until WP-08
  authors the variants (re-run the script to link them; validator would otherwise report dangling refs).
- Open for SL: verify Lewis County grade 122 mapping to the 2026 schedule; retrieve PA OA job specifications (class
  codes) and current TX Park Ranger / Hydrologist pay (2019 values recorded as dated); mvp_role_set R37's PA example
  is a regulator-side class (mirror only), mapped to R12 instead.
