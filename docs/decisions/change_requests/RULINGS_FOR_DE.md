# What the Data Engineer must change to implement the CA rulings of 2026-10-23

- **From:** CA (Phase 4 integrator) · **To:** DE (A1), with IA as co-owner of the data model · **Date:** 2026-10-23
- **Decision record:** ADR-0029. The full rulings are under "CA ruling" in each `CR-*.md` here. SPEC is now 2.0.0-draft.2.
- **Lanes:** DE edits `schema/src/`, `schema/lint/`, `scripts/`, `tests/`, `.github/` and `docs/standard/AUTHORING_GUIDE.md`. The CA has **already** changed `vocab/*.yaml`, created `vocab/rules/`, and amended SPEC and the ADRs. Do not edit those; if a vocabulary key is wrong for the generator, file a CR.
- **Do first:** `python3 scripts/build_schema.py`. Today `--check` reports STALE for `schema/emst.schema.json` (`EmstId`, `StateClassFields`, `v_idTypePrefix`, `v_mappingSetId`). The context file is current. `tests/test_schema_build.py::…--check` fails until you regenerate. `scripts/validate_v2.py` is unaffected by the vocabulary changes: its 2–3 current errors are `E-REF-DANGLING` to `seed:FC-C02`, `seed:FC-C03` and `seed:FC-C20` from WP-03 drafts in progress.
- **When done:** bump `scripts/emstlib.py#SCHEMA_VERSION` to `2.0.0-draft.2`; regenerate the schema and context; delete every "interim / pending CA" note in `schema/src` descriptions and point them at ADR-0029; re-run `python3 -m pytest`, `validate_v2.py --strict` and `build_release.py --profile preview`.

## 1. CR-DE-001: field corrections, enumerations, ratified additions

1. **Keep** `signalStatus`, `seriesStatus`, `sourceStatus`, `prefLabel` (no `title`), the base-array VocabularyTerm `notation` (minItems 1) and the `definition` requirements as already built. All are ratified.
2. **Remove `Competency.enactments`** from `schema/src/emst.schema.src.yaml#Competency.properties`. Add `enactments` to `schema/lint/computed_fields.yaml#inverse_fields_by_type.Competency`. `Task.tools` is already listed there; keep it. Error code: the existing computed-field error.
3. **No seed-v1 at candidate.** In `RecordBase`, add `if status ∈ {candidate, published, deprecated, superseded, withdrawn} then validationStatus ≠ seed-v1`. Make `scripts/mint_id.py promote` refuse a seed-v1 record. Add validator code `E-SEED-CANDIDATE`.
4. **Generate the formerly schema-local enumerations** in `scripts/build_schema.py#generate_enums`. Every vocabulary item below is a list of `{notation, definition}` under `values`. Replace each hard-coded `enum` in `schema/src` with a `$ref`:

| New `$def` | Source (`vocab/…`) | Replaces in `schema/src` |
|---|---|---|
| `v_toolType` | `competency_types.yaml#tool_types` | `Tool.toolType` |
| `v_instrumentType` | `driver_mechanisms.yaml#instrument_types` (adds `agency-order`) | `Instrument.instrumentType` |
| `v_eventType` | `driver_mechanisms.yaml#event_types` (adds `submitted-for-review`) | `DriverEvent.eventType` |
| `v_eventDirection` | `driver_mechanisms.yaml#event_directions` | `DriverEvent.direction` |
| `v_instrumentStatus` | `driver_mechanisms.yaml#instrument_statuses` (13 values incl. `under-review`) | `DriverEvent.statusAfter` (was free string) |
| `v_credentialType`, `v_closureType` | `authority_positions.yaml#credential_types`, `#closure_types` | `Credential.credentialType`, `closureType` |
| `v_pathwayType` | `friction_types.yaml#pathway_types` | `Pathway.pathwayType` |
| `v_learningResourceType` | `friction_types.yaml#learning_resource_types` | `LearningResource.resourceType` |
| `v_frictionDirection`, `v_frictionSeverity`, `v_frictionBasis` | `friction_types.yaml#friction_directions`, `#friction_severities`, `#friction_bases` | `FrictionRecord.direction`, `severity`, `basis` |
| `v_signalStatus` | `change_types.yaml#signal_statuses` | `ChangeSignal.signalStatus` |
| `v_indicatorUseClass` | `lifecycle_states.yaml#use_tiers.indicator_use_classes` (plain list) | `Indicator.useClass` |
| `v_ratingObjectScheme` | `evidence_labels.yaml#rating_object_schemes`; items with `v1_only: true` are allowed only when `raterType = v1-analyst` (keep the existing conditional, generated) | `RelevanceRating.objectScheme` |
| `SeriesStatus` (pattern) | `mapping_predicates.yaml#series_statuses`: literal notations plus each item's `pattern` → one anchored alternation | `SeriesRecord.seriesStatus` pattern |
| `SourceStatus` (pattern) | `evidence_labels.yaml#source_statuses`, same method | `Source.sourceStatus` pattern |

   Also generate (used in §8): `v_signalFamily` (`change_types.yaml#signal_families`), `v_changeIndicatorKind` (`#change_indicator_kinds`), `v_signpost` (`scenarios.yaml#signposts[].notation`, `SP-01…SP-12`) and `v_scenarioPole` (`AX-n:<pole>` from `scenarios.yaml#axes[].poles[].notation`). Before merging, check that every value now in `data/v2/` is in the generated lists. On 2026-10-23 every `statusAfter`, `eventType`, `direction` and `instrumentType` value in the seed was covered.
5. **Ratified DE additions: keep them as built.**
   - `Competency.v1Seed`: stripped from every release; the self-check fails on any `v1Seed` in a bundle.
   - `v1Values`, `mappingRule`, `sWatch` and `tacitExperienceRequirement` on rating records. `sWatch` and `tacitExperienceRequirement` must be allowed for **every** rater type, not only v1.
   - Competency-subject ratings (`competency` + `competencyTextSha256`; `subject` + `subjectTextSha256`), allowed **only** when `raterType = v1-analyst`.
   - `Indicator.obs4Flags`, `evidencePlan`, `safetyOrLegalCritical`, `distinguishingAttribute`.
   - `Competency.transversalCluster`.
   - `reviewBy` on the base.
   - `/` in seed keys (`--` in file names).
6. **`docs/standard/AUTHORING_GUIDE.md`** (your file). Add:
   - Competencies never list enactments; Enactments point to their competency.
   - Tasks never list tools.
   - Quote `'yes'`/`'no'`.
   - The renamed status fields.
   - Seed-v1 records cannot become candidates.
   - The ChangeSignal and external-index fields in §8–§9 below.
   - Waivers go in `data/v2/governance/lint_waivers.csv`.

## 2. CR-DE-002: ID prefixes, X12, quoting, state class enums

1. **`scripts/emstlib.py#ENTITY`:** set `WatchItem.prefix = "WCH"`, `SeriesRecord.prefix = "SER"`, `StateClassRecord.prefix = "SCR"`. `mint_id.py` then stops refusing them. Replace the `E-ID-PREFIX` "no prefix" branch in `validate_v2.py` with the normal prefix-matches-type check.
2. **Tests** (`tests/test_mint_id.py`, `tests/test_validate_v2.py`): turn the refusal tests into minting tests for the three types, and include them in the 10,000-ID collision test.
3. **X12** is in `mapping_predicates.yaml#mapping_sets`. Regenerating the schema adds it to `v_mappingSetId`. Nothing else is needed.
4. **`scripts/build_schema.py#state_class_fields`:** `supervisory_status` now generates an enum by itself. For `format: enum list` with a pipe-separated `vocab_or_example`, emit `{type: array, uniqueItems: true, items: {enum: [...]}}` (`appointment_route`: `open-competitive-exam | continuous-t-and-e | application-as-exam | non-competitive | provisional | transfer-list | performance-based`).
5. **New test:** loading each of the 19 vocabulary files with the YAML 1.1 loader (`yaml.safe_load`) and with `emstlib.load_yaml` must produce identical generated enumerations, so no code list contains a boolean. The CA ran this check on 2026-10-23 and it passed.
6. **Item 5 rejected:** keep `v1Values.recovered_from` plus `derivedFrom.relation = recovered`. Do not add a flag to `v1Flags`.

## 3. CR-DE-003 (1): stability tier and CLD in the migration

- **Your interim is ratified; no change to `scripts/migrate_v1.py` output.** The tier is not migrated. Reform flags, the CLD flag, R9 severity and the S-trajectory flag migrate as v1-analyst prior evidence.
- Update the comments in `migrate_v1.py` that say "interim / pending CA" to cite ADR-0011 rule 5 (amended) and ADR-0029 §3.
- **Add a test** (`tests/test_migration.py`): no `data/v2` record carries the v1 stability tier, either as `stabilityTier` (already in `computed_fields.yaml`) or as a `v1Values` key `stability_tier` or `tier`. CLD prior-evidence records never feed the computed CLD.

## 4. CR-DE-003 (2): computed-view rules from `vocab/rules/`

1. **`scripts/build_release.py`:** replace the hard-coded `RULES` dict. Load `vocab/rules/*.yaml` and stamp `ruleId`/`ruleVersion` from the file whose `status` is `active` (`interim` while 0.1.0 is still in use).
2. **CI tests** (new `tests/test_rules.py`):
   - every file parses with both loaders;
   - the file name equals `<ruleId>@<version>.yaml`;
   - every `ruleId`/`ruleVersion` stamped in a built view has a file;
   - the path part (before `#`) of each `implementation` exists;
   - every `supersededBy` or `replaces` target exists.
3. **Implement `inverse-links@1.1.0`:**
   - `Task.tools[]` comes from `Tool.servesTasks`; `Competency.enactments[]` comes from `Enactment.competency`, with `enactmentKind` and `module`.
   - Both appear in the JSON-LD bundle records and in `views/inverse_links.json`, and never list excluded records.
4. **Extend `assessment-staleness@1.0.0`** to the competency-level hash case: v1-analyst ratings with `competencyTextSha256`/`subjectTextSha256` against `emstlib.competency_text_sha256`. Role-target external-index records have no text hash and are never text-stale.
5. **Implement `effective-use-tier@1.0.0`** (it replaces 0.1.0):
   - Caps: lifecycle, evidence (validationStatus ladder; select also needs a linked critical task in a job-analysis-confirmed variant), level-rule (IO `tier_requirements` at every published level; no published level means describe), indicator-lint (an unwaived flag caps at develop), and pathway (exploratory until M-03).
   - Output `caps{…}` and `bindingCap`. Record the SHA-256 of `validation/indicator_lint_rules.yaml` in the view header.
6. **Implement `change-indicator@1.0.0`** (see §8) and **`display-gate@1.0.0`** (see §6).

## 5. CR-IO-001: publication-rule checks, PR-2, waivers

1. **`schema/src#PublicationRuleCheck`:** drop "interim" from its description. In `Competency.levels[].publicationRuleChecks`, require `evidence` with `minItems: 1` when `existence.result = pass` or `consensus.result = pass`.
2. **`validate_v2.py` must run IO's indicator lint** (`validation/lint_indicators.py`, including the new PUB-14) on every Indicator and Competency in CI, if it does not already.
3. **PUB-14 is IO's code.** It rejects `pass` on existence unless an indicator at that level is `≥ job-analysis-confirmed`, and on consensus unless `≥ panel-retained`. Your validator must not duplicate it with a different message.
4. **New cross-record rule `E-PR2-ATTRIBUTE`:** an Indicator with `status ≥ candidate` at a level above the lowest level of its competency that has indicators must carry `distinguishingAttribute`. The lowest level is computed from the competency's `levels[]`, not from `levelSpan.min`.
5. **Waivers:**
   - read `data/v2/governance/lint_waivers.csv` (columns per `validation/indicator_lint_rules.yaml#waivers`; IO changes its default path);
   - a waiver applies only while `recordId`, `ruleId` and the normalized-text SHA-256 all match;
   - the signer must match `^pid:`; `emstagent:` signers are an error (`E-WAIVER-SIGNER`);
   - `build_release.py` release notes count waivers by rule.

## 6. CR-IO-002: display gate

1. Emit agreement results in `validation/display_gates.yaml#agreement_result_schema` to `dist/views/agreement/`. Build the emitter now against `validation/tests` fixtures; no study data exists yet.
2. In `build_release.py`, build `views/display_gate.json` by calling `validation/display_gate.py::decide()` for every gated value. Use `vocab/rules/display-gate@1.0.0.yaml#editorial_fields` and `#gated_fields`. Record the SHA-256 of `validation/display_gates.yaml` in the view header.
3. CP reads gated values only from that view (or through `decide()`). The bundle and the CSVs keep every value with its `validationStatus`; the data download is not gated.

## 7. CR-IO-003: E-level order

- Add `emstlib.exposure_level_order()` that returns `vocab/exposure_instrument_v2.yaml#constructs.technical_exposure.ordinal_order`. Every view or distribution that sorts E-levels uses it, never code order.
- No schema change. Code order stays the enum order.

## 8. CR-LM-001: change-signal fields, independence, targets, evidence rule

1. **`schema/src#ChangeSignal`:**
   - `signalStatus`: `$ref v_signalStatus`.
   - `signalFamily`: `$ref v_signalFamily`.
   - `independenceKey`: string, pattern `^[a-z0-9][a-z0-9-]{1,60}$`. Not an enumeration.
   - `registeredDeployment`: boolean, allowed only when `signalFamily = deployment`.
   - `impact`: integer 1–3.
   - `scenarioSignposts`: array of strings `^vocab:scenarios#SP-(0[1-9]|1[0-2])$`, or a generated enum of the form `vocab:scenarios#` + `v_signpost`.
   - `pointsToward`: array, each item `v_scenario` or `v_scenarioPole`.
   - `measure`: add `baseline {value, ci95, n, note}` and `sensitivity {weighting, value, baselineValue}`, both closed.
   - `if signalStatus = active then required [signalFamily, independenceKey]`.
   - `targetType`: `anyOf [v_entityType, {const: organization}]`. When it is `organization`: `targetId` matches `^(opm-agency|census-gov):[A-Za-z0-9-]+$`, `tribalPrograms` is false, and `sectorActor` is not `tribal` or any Tribal subtype.
2. **`validate_v2.py`:**
   - `E-INDEPENDENCE-KEY-UNLISTED`: an active signal whose key is not in `vocab/change_types.yaml#independence_keys`. For watch signals the same check is `W-…`.
   - `E-NOTATION-INTERIM`: an `EMST-*` notation scheme on a `candidate` or later record. Warn on drafts.
   - `E-ORG-TARGET-TRIBAL`: an organization target that is Tribal by any route.
   - `W-ORG-SMALL-N`: an organization target with `measure.n < 5`. The release gate suppresses it.
   - SP-12: a signal citing `SP-12` is quarantined like `careFlag` (release gate exclusion; the evidence rule ER-0).
   - `W-MVP-ROLE-TARGET`: a `targetId` starting `mvp-role:`. The release gate excludes these records.
   - Computed `Instrument.currentStatus` must never become an in-force value through a `submitted-for-review` event.
3. **Port the evidence rule:**
   - Port `docs/methods/ci/evidence_rule.py` to `scripts/rules/change_indicator.py`, the path named in the rule file. If you choose another path, tell the CA and the rule file's `implementation` will be updated.
   - Read families and `counts_toward` from `vocab/change_types.yaml#signal_families`, and providers from `#independence_keys`, instead of constants. Read the external-index instrument map from `vocab/rules/change-indicator@1.0.0.yaml#external_index_instruments`.
   - Count only `signalStatus = active` signals. Watch signals are evaluated for the "what's coming" view only.
4. **Move tests:**
   - `docs/methods/ci/test_evidence_rule.py` → `tests/test_evidence_rule.py`.
   - `evidence_rule_cases.yaml` → `tests/fixtures/evidence_rule_cases.yaml`.
   - Keep the regression that no seeded agent signal moves an indicator.
   - LM deletes the `docs/methods/ci/` copies once your port passes.
5. **`build_release.py`:** write `views/change_indicators.json` per the rule file.
6. **Ratified as built:** `_load_source_ids` reads every `docs/**/sources.csv`, including `docs/methods/sources.csv`.

## 9. CR-LM-002: occupation-grain external-index assessments

1. **`schema/src#ExposureAssessment`:**
   - Replace top-level `required: [task, taskTextSha256]` with two branches:
     - **if** `raterType = external-index` and `externalSource.unit = occupation`: **then** required `[targetType, targetId, crosswalkPath, crosswalkMinMatchType]`, `task` forbidden, and `targetType ∈ {RoleProfile, RoleVariant}`;
     - **else**: required `[task, taskTextSha256]`, with `targetType`, `targetId`, `crosswalkPath` and `crosswalkMinMatchType` forbidden.
   - Add the properties `targetType`, `targetId` (`AnyRef`), `crosswalkPath` (array, minItems 1) and `crosswalkMinMatchType` (`v_mappingPredicate`).
2. **`technicalExposure[]` items:** `oneOf` `{vector, level}` or `{vector, levelDistribution, basis}`. `levelDistribution` is a closed object with optional `E0`–`E3` numbers in [0, 1]. The validator checks that they sum to 1 ± 0.01 (`E-LEVEL-DISTRIBUTION`).
3. **Non-v1 branch:** for `external-index`, require `technicalExposure` **or** `externalSource.values` (`anyOf`). Other rater types still require `technicalExposure`.
4. **`externalSource`:**
   - add `unit` (enum `onet-task | dwa | iwa | occupation`; required), `values` (object) and `dispersion` (`number | object`);
   - `matchedOnetTasks` is required with `minItems: 1` unless `unit = occupation`, when it may be empty or absent.
5. **`assessedAt`:** if `raterType = external-index`, `$ref PartialDate`, otherwise `Date`. Move the property out of `RatingBase` into a conditional, or use `anyOf` with an `if`.
6. **Release gate:**
   - exclude every record with `license = LicenseRef-EMST-third-party-index-derived` from all bundle, CSV and view outputs;
   - report the exclusions as a count in release notes;
   - add the check to the self-check;
   - records attached to a held target inherit the hold.
7. **Then:** LM runs `python3 docs/methods/scripts/build_wp10.py --promote-external`, which writes to `data/v2/assessments/external/<index>/<batch>.jsonl`. Re-run the validator.

## 10. CR-LM-003: lanes

- Keep `E-LOCATION` for L5 registry types under `signals/`.
- Add a CI test that `.github/workflows/*.yml` and `scripts/` never invoke `docs/methods/scripts/`.
- `emstlib` already iterates `assessments/` recursively, so `assessments/external/<index>/` needs nothing.

## Checklist for the DE worklog

`build_schema.py` regenerated · new enums wired (§1.4) · prefixes (§2.1) · state-class `enum list` (§2.4) · YAML 1.1 equality test (§2.5) · tier test (§3) · rules loaded from `vocab/rules/` and tested (§4) · inverse-links 1.1.0 · effective-use-tier 1.0.0 · PR-2 rule and waivers (§5) · agreement emitter and display-gate view (§6) · `exposure_level_order` (§7) · ChangeSignal schema, validator codes and evidence-rule port with tests (§8) · ExposureAssessment occupation grain and licence gate (§9) · lane test (§10) · AUTHORING_GUIDE · SCHEMA_VERSION 2.0.0-draft.2.

## 11. CR-IA-001: role and variant seed keys (arrived mid-session; ruled)

- **Seed-key convention:** `RoleProfile` = `seed:<role_key>` and `RoleVariant` = `seed:<role_key>/<sector_actor>[/<slice>]`, where `<sector_actor>` is a `vocab/sector_actors.yaml` notation. Add both forms to `docs/standard/AUTHORING_GUIDE.md`.
- **Validator:** add `W-ROLE-KEY` for a RoleProfile or RoleVariant seed key that does not match this form, or whose `<role_key>` is not in `docs/decisions/mvp_role_set.csv`. Use a warning, not an error, because P4 and later roles may come from elsewhere.
- **No schema change.** The CA has corrected `mvp_role_set.csv` (R09, R15, R16, R19, R20).

## 12. CR-IA-002: SSSOM justification values (arrived mid-session; ruled)

1. **`validate_v2.py` SSSOM checks:** accept every justification in `vocab/mapping_predicates.yaml#justifications`; it is already generated into `v_mappingJustification`. Report rows using a `justifications_sssom_1_1_only` value as `I-SSSOM-1_1-EXTENSION`, with a count per set.
2. **Reviewed rows:**
   - allow the SSSOM `other` column;
   - `W-SSSOM-REVIEW-PROVENANCE` when a row with `semapv:MappingReview` and a `reviewer_id` lacks `original_justification=` in `other` where the set's metadata says it was agent-drafted;
   - `E-SSSOM-SELECTION-1_1` when a row flagged for selection use still carries `semapv:LLMBasedMatching`.
3. **Optional, after rc.1 essentials:** `build_release.py` may write `sssom/strict-1.0/<set>.sssom.tsv`, with `semapv:UnspecifiedMatching` plus `other: original_justification=semapv:LLMBasedMatching`. It is a generated export only.

Checklist additions: role seed-key warning and AUTHORING_GUIDE (§11) · SSSOM 1.1-extension reporting, `other` column, review-provenance and selection checks (§12).

## Batch 2 (S1 close)

- **From:** CA · **To:** DE (A1), with IA as co-owner of the data model · **Date:** 2026-10-23
- **Decision record:** ADR-0030. The full rulings are under "CA ruling" in CR-DB-001, CR-DC-001, CR-DE-004, CR-FC-001, CR-FC-002, CR-LC-001 and CR-SC-001, and in CR-CP-001 and CR-FH-001, which arrived mid-session (§19). SPEC is now **2.0.0-draft.3**.
- **Already done by the CA, so do not redo it:**
  - `vocab/authority_positions.yaml`: `closure_types` gains `employer-mandated`, `voluntary` is narrowed, and the new key `mirror_relations` is added.
  - `vocab/driver_mechanisms.yaml`: new key `instrument_link_roles`.
  - `vocab/friction_types.yaml`: new key `formation_responses`.
  - `vocab/identifiers.yaml#form.clo_iri`.
  - `vocab/rules/venue-applicability@1.0.0.yaml` (new, `active`), `vocab/rules/inverse-links@1.2.0.yaml` (new, `draft`), the reason codes and implementation pointer in `change-indicator@1.0.0.yaml`, and `#Release.views` → `#Builder.views` in six rule files.
  - `vocab/rules/display-gate@1.1.0.yaml` (new, `draft`; IO implements), and six interim view rules: `federal-series-profile`, `state-class-view`, `job-family-membership`, `role-change`, `mirror-links` and `pathway-edges`, all `@0.1.0`.
  - `vocab/state_class_fields.yaml#emst_mapping`: competency targets are computed.
  - `data/v2/governance/three_module_exceptions.yaml` (empty register).
  - `tests/test_rules.py` passes on these files.
- **Lanes: as in Batch 1, with four exceptions that DE may make:**
  1. the mechanical record changes in §16.2 (link shape), §18.3 (task moves), §18.4 (ADR-0030 merges) and §19.4 (empty `competencyTargets`);
  2. the eight `docs/decisions/v1_disposition.csv` rows listed in `docs/decisions/integration/disposition_amendments.csv` (§18.4), and no other row;
  3. the `status` flips on `inverse-links@1.2.0` and `@1.1.0` when §16.3 lands, and on the six view rules when §19.1 lands;
  4. nothing else in `vocab/`, ADRs or SPEC.
- **Do first:** run `python3 scripts/build_schema.py`. `--check` now reports two STALE definitions: `v_closureType`, from the new `employer-mandated` value, and `StateClassFields`, from the amended `emst_mapping` definition. Then wire the three new keys (§16.2, §16.3, §17.2).
- **Priority, because WP-08 and WP-12 need it in S2:** §16.2 and §16.4 (typed links and the venue view), §19.1 (HR and role-change views), §17.1–§17.3 (planned role references, Pathway fields), §15, §14, §18, §13.
- **When done:**
  - bump `SCHEMA_VERSION` to `2.0.0-draft.3`;
  - regenerate the schema and context;
  - re-run `python3 -m pytest`, `validate_v2.py --strict` and `build_release.py --profile preview`;
  - point every "pending CA" note in `schema/src` at ADR-0030.

## 13. CR-DE-004: seed-v1 stubs, reason codes, pointers

1. **Keep `E-SEED-CANDIDATE` as built:** it applies to candidate, published and deprecated always, and to superseded and withdrawn only with a minted `emst:` ID. Point its message and `tests/test_schema_rulings.py::test_seed_v1_never_reaches_candidate` at ADR-0030 §1.1. If the schema condition in `RecordBase` still lists superseded and withdrawn unconditionally, narrow it to match the validator.
2. **Reason codes:** `ER-0-NOT-ACTIVE` and `ER-0-ORGANIZATION-TARGET` are now in `change-indicator@1.0.0.yaml#reason_codes`. Remove any "documented extra" special-casing from `tests/test_evidence_rule.py`, and add a test that every reason code `scripts/rules/change_indicator.py` can emit is in the rule file.
3. **Pointers:** keep `Release = Builder` until rc.1 is tagged. The rule files now name `#Builder.views`.

## 14. CR-DC-001: case-sensitive product matching

1. In `Validator`, compile each `productExamples` entry with `_term_rx({"term": ex, "cs": True})`.
2. In `schema/lint/typing_lexicon.yaml`: `Field Maps` gets `cs: true`. Review every multi-word term and set `cs: true` where the lower-case phrase is ordinary English, listing the changes in your worklog. A case-insensitive product term belongs only in this file, without `cs`; do **not** add a Tool field.
3. **New test:** `validate_v2.py` and `validation/lint_indicators.py` flag and pass the same fixture strings for product names, e.g. "InVEST" flagged, "invest", "slack water" and "maple" not flagged, "Field Maps" flagged, "field maps" not.
4. Tell DC (A4) when it lands; DC then moves names in `data/v2/tools/tools.jsonl` (data-only).

## 15. CR-DB-001: three-module rule, Enactment subsectors

1. **`W-THREE-MODULE` / `E-THREE-MODULE`.**
   - **Scope:** every live Competency with `module = core` and `competencyType = practice`.
   - **Count:** M = the distinct `enactedInModule` values of its live Enactments with `enactmentKind = module`.
   - **Fires when** |M| ∈ {1, 2} and there is no row for it in `data/v2/governance/three_module_exceptions.yaml` (`exceptions[]`, matched on `competency`). Warning on drafts; error when `status ∈ {candidate, published, deprecated}`.
   - |M| = 0 passes.
   - **Register checks:**
     - each row needs `competency`, `modules[]`, `rationale`, `decidedBy` (`^pid:` or `CA`), `decidedOn`, `reviewBy` and `decidedIn`, otherwise `E-THREE-MODULE-EXCEPTION-FORMAT`;
     - `W-THREE-MODULE-EXCEPTION-EXPIRED` when `reviewBy` is past;
     - `E-REF-DANGLING` when the competency does not resolve.
2. **`I-THREE-MODULE-RECURRENCE`** for each such competency: the sorted distinct modules among M, the `homeModule` of live tasks supporting it, and, once role records exist, the `homeModule` of RoleProfiles whose `competencyTargets` name it.
   - In `build_release.py` release notes, add the count of core practice competencies with recurrence below 3. It is not a gate.
3. **`Enactment.subsectors`:** optional, `{type: array, uniqueItems: true, minItems: 1, items: {$ref: v_subsector}}`.
   - Extend `E-MODULE-SUBSECTOR`: an Enactment with `enactmentKind = module` and status ≥ candidate without `subsectors` is an error; on drafts it is `W-MODULE-SUBSECTOR`.
   - Indicators get no field; their subsectors are inherited from the competency in views.

## 16. CR-SC-001: task edges, typed instrument links, mirrors, venue view, delegated constraints

1. **Task edges.**
   - `Task.instrumentSensitivity`: `{type: array, items: {$ref: SensitivityEdge}}`. `SensitivityEdge` gains optional `reviewBy: {$ref: Date}`.
   - **Validator:**
     - `W-EDGE-REDUNDANT`: a Task edge whose `mechanism` is already on a competency the task supports as `primary`, with no `sources` beyond that competency's edge.
     - `E-EDGE-REVIEWBY`, from `candidate` on: an edge, on a Task or a Competency, with `evidenceLabel ∈ {J, S}` and no `reviewBy`.
     - `W-EDGE-REVIEW-OVERDUE`: `reviewBy` earlier than the validation date.
   - The sensitivity view (when built) gives each task the union of its own edges and its primary competencies' edges, with the inherited ones marked `inherited: true`.
2. **Typed instrument links.**
   - **Schema.** New `$def` `InstrumentLink = {type: object, additionalProperties: false, required: [instrument], properties: {instrument: RecordRef, role: {$ref: v_instrumentLinkRole}, note: Text}}`.
     - Generate `v_instrumentLinkRole` from `vocab/driver_mechanisms.yaml#instrument_link_roles`.
     - `Enactment.characteristicInstruments` and `RoleVariant.instruments` become `{type: array, items: {$ref: InstrumentLink}}`, unique by `instrument`. The validator checks uniqueness: two items with the same `instrument` are `E-INSTRUMENT-LINK-DUPLICATE`.
   - **Conversion, in the same change.** Rewrite every existing string item `seed:ins/x` as `{instrument: seed:ins/x}`, with no role. On 2026-10-23 that is 119 links on 49 enactments: 38 SC, 11 DB. Do not default the role. Keep YAML key order and quoting as `emstlib.write_yaml` does.
   - **Validator:**
     - add `("Enactment", "characteristicInstruments.instrument")` and `("RoleVariant", "instruments.instrument")` → `{"Instrument"}` to `TYPED_LINKS`;
     - `W-INSTRUMENT-ROLE-MISSING` on drafts, `E-INSTRUMENT-ROLE-MISSING` from `candidate` on.
   - **`DriverEvent.actingInstrument`:** optional `RecordRef`, typed `Instrument` in `TYPED_LINKS`; `E-ACTING-SELF` when it equals `instrument`.
   - Tell SC (A5), DB (A6) and LM (A9) when it lands; they set the roles (CR-SC-001 ruling, item 2).
3. **Mirrors.**
   - **Schema.** `Competency.mirrors`: `{type: array, items: {type: object, additionalProperties: false, required: [target, relation], properties: {target: RecordRef, relation: {$ref: v_mirrorRelation}}}}`. Generate `v_mirrorRelation` from `vocab/authority_positions.yaml#mirror_relations`.
   - **Validator:**
     - `target` must be a Competency or an Enactment (`TYPED_LINKS`);
     - `E-MIRROR-TWICE` when A lists B and B lists A, or when an Enactment's competency lists a mirror back to a competency that lists that Enactment;
     - `E-MIRROR-SELF` when `target` is the record itself or one of its own enactments.
   - **Computed field:** add `mirroredBy` to `schema/lint/computed_fields.yaml#inverse_fields_by_type` for Competency and Enactment.
   - **Implement `inverse-links@1.2.0#mirrored_by`.** Then set `status: active` on 1.2.0 and `status: superseded` (add `supersededBy: inverse-links@1.2.0`) on 1.1.0, and update `tests/test_rules.py::test_one_active_or_interim_version_per_rule`.
4. **Venue view** (`vocab/rules/venue-applicability@1.0.0.yaml`, already `active`):
   - Implement it in `scripts/rules/venue_applicability.py`, called from `Builder.views`, and write `views/venue_applicability.json`, stamped. Follow the rule file exactly: only `requires` links decide the value, plus the `basisLinked`, `basisVerified` and `untypedLinks` flags, `deciding[]` and `context[]`.
   - Map subtypes to families from `vocab/sector_actors.yaml`. Skip Tribal and held enactments. `asOf` is `SOURCE_DATE_EPOCH`, or the `--date` value.
   - **Tests:**
     - Move `docs/build/WP-05/ci/fixtures/` to `tests/fixtures/venue/` and `test_venue_applicability.py` to `tests/`.
     - Add the typed-role cases named in the rule file's `tests`. The fixtures must validate with `validate_v2.py --data-root`.
     - Leave WP-05's prototype where it is. CI never runs it.
   - Add `venueApplicability` and `federalApplicability` to `computed_fields.yaml` if they are not already listed.
5. **`Enactment.delegatedConstraints`:** optional `Text`.

## 17. CR-LC-001: planned references, Pathway fields, CLOs

1. **Planned targets** (extend `_load_planned_targets`):
   - every `target_key` of `v1_targets.csv` (as now);
   - `seed:<cand_id>` for each `docs/decisions/candidate_disposition.csv` row with `decision ∈ {core-v2.0, module-v2.0}`;
   - every role reference matching `^seed:(R\d{2}-[a-z0-9-]+)(/([a-z-]+)(/[a-z0-9-]+)?)?$` whose group 1 is a `role_key` in `docs/decisions/mvp_role_set.csv` and whose group 3, if present, is a `vocab/sector_actors.yaml` notation (family or subtype).
   - Planned references stay `W-REF-PENDING`, and are errors under `--strict` (as now).
   - **Hold:** a planned reference whose key is in `tribal_hold.yaml#heldSeedKeys`, or whose sector-actor segment is `tribal` or a Tribal subtype, is held: the referencing record must be held, otherwise `E-TRIBAL-INHERIT`.
   - Keep `W-ROLE-KEY` (§11) for role keys that are not in the set.
2. **Pathway schema:**
   - `emstRelease: {$ref: SemVer}`, required when `status ∈ {candidate, published, deprecated}`.
   - `cloOutcomes` (on Pathway and on each `sequence[]` item): `{type: array, items: {type: object, additionalProperties: false, required: [competency, level], properties: {competency: RecordRef, level: {$ref: v_level}}}}`, typed Competency.
   - `sequence[].formationProvisions`: `{type: array, items: {type: object, additionalProperties: false, required: [task, responses, releaseCriterion, mentorRequired], properties: {task: RecordRef, responses: {type: array, minItems: 1, uniqueItems: true, items: {$ref: v_formationResponse}}, quota: {type: object, additionalProperties: false, required: [count, unit], properties: {count: {type: integer, minimum: 1}, unit: Text}}, releaseCriterion: Text, mentorRequired: {type: boolean}}, if: {properties: {responses: {contains: {enum: [by-hand-quota, supervised-repetitions]}}}}, then: {required: [quota]}}}`.
   - Generate `v_formationResponse` from `vocab/friction_types.yaml#formation_responses`.
   - **Validator:** `E-PROVISION-TASK` when a provision's `task` is not in that step's `tasks`; `E-REF-TYPE` when a `cloOutcomes` competency has no published-or-draft level equal to `level` in its `levels[]`.
3. **CLO nodes in the build:**
   - For each released competency and each level in its `levels[]`, emit a node `{"@id": "<competency IRI>/levels/<Lx>", "type": "CompetencyLevelOutcome", competency, level, indicators[]}`, where `indicators[]` is that level's `levels[].indicators` only.
   - For each released enactment with `indicatorVariants`, emit `<enactment IRI>/levels/<Lx>` with the generic indicators plus that enactment's variants at the level.
   - Seed-keyed drafts in the preview profile use `seed:<key>/levels/<Lx>`.
   - Add `CompetencyLevelOutcome` to the context. It is a computed node, never a source record.
   - Derived UUIDv5 IDs for CLOs follow SPEC §12.3.
4. **`E-CLO-ENACTMENT-INDICATOR`:** an Indicator ID listed in any `Enactment.indicatorVariants` and also in its competency's `levels[].indicators`.
5. **Closure type:** regenerate `v_closureType`. Nothing else is needed.

## 18. S1 integration-review items (ADR-0030 §3)

1. **Hold hardening in release outputs.**
   - The preview build on 2026-10-23 carried the description of a held successor (`TN-C11 …`) in the X1 `comment` of `EMSTv1:5.3.3`, which is copied from `v1_disposition.csv#target`.
   - In `build_release.py`, for every X1 row whose v1 key's disposition target names a held key, replace the comment with `decision=<decision>; ADR-0011; one or more successors held (ADR-0007 §D)`.
   - Add to the self-check: no released file contains any `tribal_hold.yaml#heldSeedKeys` value, or the bare candidate ID of one (e.g. `TN-C11`, `SC-C13`).
   - This is the only hold finding of the S1 review (ADR-0030 §3.3).
2. **Held tasks with held successors:** report `W-SUPERSEDED-TARGET` as `I-SUPERSEDED-TARGET-HELD` when both the task and every successor are held (v1 5.3.2, 6.5.1, 7.1.1: 9 tasks). They cannot be re-pointed before a Tribal Advisory Council exists.
3. **Mechanical task moves and re-points** (S2; text unchanged; `provenance.derivedFrom` kept; then `migrate_v1.py --x1-only`):

   | Task seeds | Action |
   |---|---|
   | `seed:v1-4.6.2-T2`, `-T3` | move to `modules/worklands/tasks/`; `supports: [{competency: seed:v1-4.6.1, strength: primary}]` (CR-FC-002 #4) |
   | `seed:v1-4.5.3-T1` | move to `modules/worklands/tasks/`; supports planned `seed:v1-4.5.3-B` (CR-FC-002 #4) |
   | `seed:v1-1.8.5-T1`…`-T3` | move to `modules/worklands/tasks/`; supports `seed:v1-1.8.1` (WP-07 handoff) |
   | `seed:v1-6.3.5-T1`…`-T3`, `seed:v1-6.6.1-T2` | move to `modules/markets/tasks/`; supports the markets successor that X1 maps each to (wave 3; they stay drafts) |
   | `seed:v1-3.4.1-T1`…`-T3`, `seed:v1-3.4.4-T1`…`-T3`, `seed:v1-3.4.5-T1`…`-T3` | tool-bound tasks of move-to-tools parents: set `status: superseded` with `replacedBy` = the parent's L4 tool and L1 successor (`seed:SC-C10`; `seed:DB-C26` for 3.4.4; `seed:v1-3.2.5` for 3.4.5 after item 4), as X1 records |
   | `seed:v1-5.3.3-T*`, `seed:v1-5.3.4-T*` | leave for the S2 authors of DB-C50 and v1 5.3.4-A/B (`docs/decisions/integration/s2_work_orders.csv`) |

4. **ADR-0030 core merges** (apply together, in one change, before the survivors are authored):
   - edit exactly the eight `v1_disposition.csv` rows in `docs/decisions/integration/disposition_amendments.csv` (`decision`, `target`, `rationale`);
   - set `status: superseded` and `replacedBy: [<survivor>]` on `seed:v1-5.6.1`, `seed:v1-5.5.4`, `seed:v1-5.4.3`, `seed:v1-3.1.5` and `seed:v1-3.3.5`;
   - re-point their task seeds to the survivor as `primary`, text unchanged;
   - run `python3 scripts/migrate_v1.py --x1-only`, then `validate_v2.py`.
   - Expect 0 new errors. `docs/decisions/integration/s1_integration_review.py` then reports 175 core competencies (164 releasable plus 11 held).
5. **`counts@1.0.0#coreCompetencies`:** add the G-9 range check to the release self-check for `--profile release` builds whose `--version` is `2.0.0-rc.1` or later, not `-dev` or the `rc.0` test fixtures. Fail when `coreCompetencies` plus held core is above 180 or below 120. Report the held part only as a count. For other builds, print the value with the range as `I-CORE-SIZE`.

6. **`docs/standard/AUTHORING_GUIDE.md`** (your file). Add:
   - typed instrument links, with one example per role;
   - task edges only when they are task-specific;
   - `mirrors[]` on the authority side;
   - `Enactment.subsectors` and `delegatedConstraints`;
   - `formationProvisions` and `cloOutcomes` on pathways;
   - the CLO rule (enactment variants never in `levels[]`);
   - planned role references;
   - the three-module exception register (rows by the CA only);
   - the S1 builder freeze (ADR-0030 §5).

Checklist additions:
- schema rebuilt, `v_closureType` current;
- `v_instrumentLinkRole`, `v_mirrorRelation` and `v_formationResponse` generated;
- InstrumentLink shape and the 119-link conversion (§16.2);
- `actingInstrument`;
- venue view and moved tests (§16.4);
- mirrors and `inverse-links@1.2.0` (§16.3);
- Task edges and edge checks (§16.1);
- planned targets and hold (§17.1);
- Pathway fields (§17.2);
- CLO nodes and `E-CLO-ENACTMENT-INDICATOR` (§17.3–§17.4);
- three-module checks and Enactment subsectors (§15);
- case-sensitive products (§14);
- seed-v1 wording (§13);
- X1 comment redaction and self-check (§18.1);
- held superseded-target downgrade (§18.2);
- task moves (§18.3);
- merges (§18.4);
- G-9 release check (§18.5);
- AUTHORING_GUIDE (§18.6);
- `SCHEMA_VERSION` set to 2.0.0-draft.3.

## 19. CR-FH-001 and CR-CP-001: WP-08 and WP-12 views (arrived mid-session; ruled)

1. **Port six views into the release.** The CA has registered the rules as `interim`, with `implementation: scripts/build_release.py#Builder.views`:

   | Rule | Port from | View |
   |---|---|---|
   | `federal-series-profile@0.1.0` | `pipelines/views/federal_series_profile.py` | `views/federal_series_profiles/<code>.json` |
   | `state-class-view@0.1.0` | `pipelines/views/state_class_view.py` | `views/state_class_views/<jur>--<code>.json` and `index.json` |
   | `job-family-membership@0.1.0` | `pipelines/views/job_families.py` | `views/job_families.json` |
   | `role-change@0.1.0` | `pipelines/views/change_view.py` and CP's `site/lib/model.mjs` summary | `views/role_change/<role_key>.json` and `summary.json` |
   | `mirror-links@0.1.0` | `pipelines/views/mirror_links.py` | `views/mirror_links.json` |
   | `pathway-edges@0.1.0` | CP's `site/lib/model.mjs` edge functions | `views/pathway_edges.json` |

   - Ported code goes in `scripts/rules/<rule>.py` and reads **released records only**, after the release gate. It never reads `data/v2/` directly and never reads `docs/build/WP-08/change_view_inputs.yaml`.
   - Move `pipelines/views/tests/test_views.py` into `tests/`. The WP-08 acceptance-pair checks (R11 ↔ R37, R12 ↔ R37, R11 ↔ `…/private/applicant-preparer`) become tests, not view content.
   - **Display constraints** (`display-gate@1.1.0`, below) apply in the ported code:
     - no `timeShare` or `importance` in the FSP or SCV before `job-analysis-confirmed`;
     - no `critical` or `neededAtEntry` before `validationStatus ≥ reviewed` with a `pid:` reviewer;
     - job-family weights are 1 unless importance is job-analysis-confirmed;
     - role-change summaries count tasks, not time.
   - When a view is ported with tests, you may set its rule file's `status: active` (authorized flip).
2. **Display gate 1.1.0 (IO's lane; DE only wires it).** IO implements `editorial_design_values` and `job_analysis_values` in `validation/display_gates.yaml` and `display_gate.py#decide`, then flips `display-gate@1.1.0` active and `@1.0.0` superseded. `views/display_gate.json` then carries decisions for role-profile fields too.
3. **Schema:**
   - `ExposureAssessment.contentChangeType`: optional, `$ref v_contentChangeType`. Generate it from `vocab/change_types.yaml#content_change_types` if it is not generated yet. No `drivers` field.
   - `RoleVariant.indicativeGradeOrBand.byRoleLevel`: optional, `{type: object, propertyNames: {$ref: v_roleLevelKey}, additionalProperties: {type: string, minLength: 1}}`. Make `band` required only when `byRoleLevel` is absent.
4. **State class mapping:** `vocab/state_class_fields.yaml#emst_mapping` is amended, so regenerating makes `StateClassFields` current.
   - Add `emstMapping.competencyTargets` to `schema/lint/computed_fields.yaml` (`E-COMPUTED-FIELD`).
   - Remove the empty `competencyTargets: []` keys from `data/v2/registers/state_classes/`, a mechanical change you are authorized to make.
5. **Release gate for the HR views:** held records, Tribal variants and LicenseRef-EMST-third-party-index-derived records never enter these views. The §18.1 self-check covers their outputs.

Checklist additions (§19): six views ported and stamped; WP-08 view tests moved; `contentChangeType`; `byRoleLevel`; `StateClassFields` regenerated; `emstMapping.competencyTargets` computed-field lint and cleanup.
