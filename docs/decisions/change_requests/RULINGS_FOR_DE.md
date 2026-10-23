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
