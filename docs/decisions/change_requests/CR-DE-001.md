# CR-DE-001: SPEC field-name clashes, unstated paths and DE schema additions found while building WP-01

- **From:** DE (A1), WP-01/WP-02 · **To:** CA (decider); IA (co-owner of the data model) · **Date:** 2026-10-23 · **Type:** X (structural; SPEC correction) · **SemVer impact:** none for data (no release yet); schema 2.0.0-draft.1
- **Affects:** SPEC §4, §5.1, §5.14, §5.16, §5.20, §5.24, §12.2, §17.1; `schema/src/emst.schema.src.yaml`; `docs/standard/AUTHORING_GUIDE.md`
- **Evidence label:** J (DE; each item was found by implementing the SPEC as a closed JSON Schema and running the v1 migration and other agents' records through it)

## Problem and interim implementation

The schema follows the SPEC wherever the SPEC is implementable as written. Where it is not, the interim choice below is already in `schema/emst.schema.json`; each is reversible by a schema rebuild before any ID is published.

| # | SPEC text | Problem | Interim in schema 2.0.0-draft.1 |
|---|---|---|---|
| 1 | §5.14 ChangeSignal `status ∈ {watch, active, retired}`; §5.20 SeriesRecord `status ∈ {active, proposed-realignment, …}`; §5.24 Source `status` (current/outdated/…) | Clashes with the common-base `status` (editorial status, §4/§10.1) on the same record | Renamed `signalStatus`, `seriesStatus`, `sourceStatus` |
| 2 | §5.20 `title`, §5.24 `title` | Duplicates common-base `prefLabel` | Use `prefLabel`; no `title` field |
| 3 | §5.1 VocabularyTerm `notation` = short code string | Common base defines `notation` as an array of `{scheme, value}` | VocabularyTerm uses the base array (`[{scheme: work_functions, value: WF-ASSESS}]`), minItems 1 |
| 4 | §12.2 and ADR-0010 name `scripts/mint_ids.py`; the build plan names `scripts/mint_id.py` | Two names for the single writer | `mint_id.py` is the implementation; `mint_ids.py` is a three-line alias to the same code |
| 5 | §17.1 lists no path for the L5 Instrument registry | WP-10 needed one | `data/v2/instruments/*.jsonl` (registry, one per line), consistent with CR-LM-003 option 1 |
| 6 | §4 "definition MUST for L1" | Applies naturally to Competency; for Indicator and Enactment the `statement`/`note` is the definition | `definition` required on authored Competency, RoleProfile, RoleVariant, JobFamily, Pathway; not on Indicator/Enactment |
| 7 | §5.2, §5.5 required fields | v1 seeds cannot honestly supply `competencyType`, `workFunction`, `fieldDependency`, `formationDependency`, `lifecycleState`, `definition` | Required only when `validationStatus ≠ seed-v1`; seeds are never released and the validator lists their gaps |
| 8 | §5.5 Task `tools[]` "inverse convenience, computed in bundles" | A stored inverse link would drift | Forbidden in source (`schema/lint/computed_fields.yaml#inverse_fields_by_type`) |
| 9 | §5.2 Competency `enactments[]` | Pointing core competencies at module enactments breaks "core must not depend on module" (§3.2) | Allowed only to core enactments; module enactments link from the Enactment side |

Enumerations the SPEC fixes but no vocabulary carries are schema-local for now (not generated from `vocab/`): `Tool.toolType`, `Instrument.instrumentType`, `DriverEvent.eventType` and `direction`, `Credential.credentialType` and `closureType`, `Pathway.pathwayType`, `LearningResource.resourceType`, `FrictionRecord.direction/severity/basis`, `ChangeSignal.signalStatus`, `Indicator.useClass`, `RelevanceRating.objectScheme`. **Proposal:** move them into vocabularies (e.g. `vocab/l5_registry.yaml`, `vocab/l6_registers.yaml`) so a change goes through a vocabulary PR like every other code list.

DE additions not named in the SPEC (all optional, all closed objects):

- `Competency.v1Seed`: the restored v1 text (four v1 levels mapped to L1–L4 with Knowledge/Application and every source indicator with its `v1Key`; sector notes) carried as reference-only seed material per ADR-0011 ("indicators carried as draft seeds only"). It is stripped from every release. The alternative, ~6,600 seed Indicator records without assessable metadata, would invite counting or display as v2 indicators.
- Rating records (`ExposureAssessment`, `CraftRating`, `FunctionRating`, `RelevanceRating`): `v1Values` (the v1 codes verbatim, snake_case) and, for exposure, `mappingRule`, `sWatch`, `tacitExperienceRequirement` (XR-04 and the codebook's v1 mapping). Competency-level v1 tags (craft, workflow stage, family, reform flags, lenses, CLD) need a subject that is a competency; the SPEC rating types are task-level, so `competency` + `competencyTextSha256` (and `subject`/`subjectTextSha256` on RelevanceRating) are allowed **only for `raterType = v1-analyst`**, with legacy `objectScheme` values `v1-family | v1-reform-flags | v1-ethical-lens | v1-cld`.
- `Indicator.obs4Flags`, `evidencePlan`, `safetyOrLegalCritical`, `distinguishingAttribute` (IO metadata; the last per CR-IO-001); `Competency.transversalCluster` (TX-A…TX-F, required when `competencyType = transversal`); `reviewBy` on the common base (§10.2 requires it for proposed/emerging records).
- Seed keys may contain `/` (WP-10 uses `seed:evt/<instrument>/<event>/<date>`); in file names `/` becomes `--`.

## Proposed change

Correct SPEC §4, §5.1, §5.14, §5.20, §5.24, §12.2 and §17.1 to the interim choices above (or decide otherwise, and DE rebuilds the schema); ratify the DE additions; move the schema-local enumerations into vocabularies.

## Consequences if not accepted

Each alternative is a schema rebuild plus a migration rerun; no IDs depend on it yet. After the first `candidate` mint, renaming fields becomes a MAJOR schema change.
