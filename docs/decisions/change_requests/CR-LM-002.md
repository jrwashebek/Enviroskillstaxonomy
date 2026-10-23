# CR-LM-002: Let external-index ExposureAssessments exist at an occupation-to-role grain

- **From:** LM (A9), WP-10 · **To:** CA (decider), DE (schema) · **Date:** 2026-10-23 · **Type:** X (structural; schema) · **SemVer impact:** minor
- **Affects:** SPEC §5.12, §11.4; `schema/emst.schema.json` `ExposureAssessment`, `RatingBase.assessedAt`; ADR-0008 §4; XR-06
- **Evidence label:** J (LM)

## Problem

The orchestrating brief for WP-10 asks for external-index assessments **only at an aggregated, defensible grain: occupation-level indices attached to role crosswalk targets, never single-task matches**. That is also what XR-06 and the LM pilot support: single external matches disagreed in 13 of 21 two-match cases. The schema can express only task-grain assessments:

- `task` and `taskTextSha256` are required.
- `technicalExposure[]` requires a single `{vector, level}`. An occupation aggregate is a **distribution** over E0–E2.
- `externalSource.matchedOnetTasks` needs at least one item, and `dispersion` must be a number.
- `assessedAt` must be a full date. Several index releases are dated only to a year.

No EMST task can be matched yet, because X2 (two-coder EMST task → O*NET 31.0) does not exist. So nothing external can be ingested today without either faking task matches or breaking the schema.

## What the seed does meanwhile

`docs/methods/scripts/wp10_external.py` writes the records to **`docs/methods/staging/assessments-external/`**, outside the validated tree. Each one is an occupation value attached to every MVP role that lists the code in `mvp_role_set.csv`:

- Eloundou human/GPT-4 β, percentiles and the E0/E1/E2 task shares.
- Microsoft "Working with AI" v6 applicability.

Each record carries `targetType: RoleProfile`, `targetId: mvp-role:<key>`, a two-step `crosswalkPath` and `crosswalkMinMatchType` (close for single-SOC roles, broad otherwise). Counts are generated in `docs/methods/generated/wp10_counts.json`.

## Proposed change

1. When `raterType = external-index`, make `task`/`taskTextSha256` optional if `targetType ∈ {RoleProfile, RoleVariant}` and `targetId`, `crosswalkPath[]` and `crosswalkMinMatchType` are present. This mirrors ChangeSignal.
2. Allow `technicalExposure[].levelDistribution {E0, E1, E2, E3}` as an alternative to `level`, with `basis`.
3. For external-index records, let `externalSource` carry `unit`, `values{}` (the index's own published numbers), and `dispersion` as either a number or an object. `matchedOnetTasks` may be empty when `unit` is an occupation.
4. Allow `assessedAt` as a PartialDate for external-index records.
5. Confirm the licence label `LicenseRef-EMST-third-party-index-derived` for values derived from third-party datasets whose licence the V-pass did not verify (Eloundou replication repo; Microsoft results files). These records are excluded from CC0 bundles until AS/CP confirm.
6. The CI rule keeps them out of any indicator unless paired with an independent family (CR-LM-001). Role views may show them only as context, labelled "occupation-level; not specific to this role's tasks".

On acceptance, run `python3 docs/methods/scripts/build_wp10.py --promote-external`. This writes the staged files to `data/v2/assessments/external/<index>/<batch>.jsonl`.

## Consequences if not accepted

External-index evidence waits for X2. The P1 role-change briefs (WP-14) then have no capability or observed-use family except through prose, and the "two exposure profiles" finding (analytical roles at the 81st–99th percentile, field roles at the 10th–33rd) stays outside the data.
