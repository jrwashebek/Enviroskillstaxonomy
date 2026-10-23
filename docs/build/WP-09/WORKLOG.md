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
