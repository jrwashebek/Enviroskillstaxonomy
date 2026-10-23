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

## CA ruling

- **Ruling:** **accept with changes** · **Date:** 2026-10-23 · **Decider:** CA · **Recorded in:** ADR-0008 and ADR-0013 (amendments), ADR-0029 §9, SPEC §5.12, §11.4, §17.1, DECISION_LOG `CR-LM-002`
- **Implementation:** DE (schema; validator; release gate) per `RULINGS_FOR_DE.md` §9; then LM runs `--promote-external`.

1. **Role-grain external records: accepted.** For `raterType = external-index`, `task` and `taskTextSha256` may be omitted only when all of these are present: `targetType ∈ {RoleProfile, RoleVariant}`, `targetId`, `crosswalkPath[]`, `crosswalkMinMatchType`, and `externalSource.unit = occupation`. A record carries **either** a task **or** a role target, never both. No other rater type may use a role target.
2. **`levelDistribution`: accepted with a change.**
   - `technicalExposure[]` items carry either `level` or `levelDistribution {E0, E1, E2, E3}` (shares 0–1 summing to 1 ± 0.01), plus `basis`. The `basis` states, per index, how the index's own labels map to EMST E-levels. The codebook's E3 is "end to end", which is not every index's third label.
   - **Change:** where an index has no E-level construct (e.g. Microsoft applicability), `technicalExposure` is omitted and the index's numbers go only in `externalSource.values`. An external-index record must carry `technicalExposure` or `externalSource.values`, or both.
   - Displays order distributions by `ordinal_order` (CR-IO-003).
3. **`externalSource`: accepted.** It gains `unit ∈ {onet-task, dwa, iwa, occupation}`, `values{}` (the index's published numbers) and `dispersion` as a number or an object. `matchedOnetTasks` may be empty only when `unit = occupation`. `release` must name the index release (ADR-0008 §4).
4. **Partial dates: accepted** for external-index records only. `assessedAt` is then the date of the index release the values come from; EMST's ingestion date is `provenance.generatedAt`.
5. **Licence: accepted as an interim label.**
   - Records carrying `LicenseRef-EMST-third-party-index-derived` are excluded from the CC0 data files and from **every** release bundle until AS (with CP) records the index's terms in the third-party licence register (ADR-0013).
   - Once the terms are verified, the values ship under the index's own terms in `external/`, or in the bundle with attribution where the terms allow.
   - No index text is copied, only IDs and numbers.
6. **Evidence rule and display: accepted, with a display change.**
   - Evidence rule: these records never move an indicator unless paired with an independent family under `change-indicator@1.0.0`.
   - Role views show them only as context, labelled "Occupation-level external index; not specific to this role's tasks", with dispersion, the index release and the crosswalk match type.
   - **Change:** values whose `crosswalkMinMatchType` is broader than `skos:closeMatch` appear only in the evidence drawer, not on the role summary.
   - They are never averaged across indices into one number and never appear in `select` views.
   - Records attached to a held (Tribal) target inherit the hold.

**Sequence:** LM runs `python3 docs/methods/scripts/build_wp10.py --promote-external` only after DE's schema implements items 1–4 and `scripts/validate_v2.py` passes on the staged files. The target path `data/v2/assessments/external/<index>/<batch>.jsonl` is ratified (SPEC §17.1).
