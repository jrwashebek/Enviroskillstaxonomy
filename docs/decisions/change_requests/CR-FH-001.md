# CR-FH-001: Homes for the WP-08 generated views, change-view atoms, mirror links and the applicant variant

- **From:** FH (A7, with SL, PS, CM), WP-08 · **To:** CA (decider), DE and IA (schema, build), LM (signals) · **Date:** 2026-10-23 · **Type:** X (structural; computed views and two optional fields) · **SemVer impact:** minor
- **Affects:** SPEC §5.7, §5.8, §5.21, §14; `vocab/rules/`; `scripts/build_release.py`; `docs/decisions/mvp_role_set.csv` (only if item 3 is decided the other way)
- **Evidence label:** J (FH; found while authoring WP-08 against schema 2.0.0-draft.2)

## Problem and proposed change

1. **The generated HR views have no registered rule and are not in the build.** ADR-0006 §4 and SPEC §14 list the Federal Series Profile, the State Class View and job-family membership as computed views. ADR-0029 rule 3 requires every view to stamp a registered `ruleId`/`ruleVersion`, and rule 4 keeps build code in `scripts/`, which authoring agents may not edit. WP-08 therefore wrote deterministic generators in its own lane, `pipelines/views/` (with tests), writing to `docs/build/WP-08/generated/`, each stamped `ruleStatus: proposed`:
   - `federal-series-profile@0.1.0` (`federal_series_profile.py`)
   - `state-class-view@0.1.0` (`state_class_view.py`)
   - `job-family-membership@0.1.0` (`job_families.py`; parameters in `pipelines/views/rules/job-family-membership@0.1.0.yaml`, already in rule-file format; `JobFamily.memberRule` points at it)
   - `role-change-inputs@0.1.0` (`change_view.py`) and `mirror-links@0.1.0` (`mirror_links.py`)

   **Proposed:** CA registers the five rules in `vocab/rules/`; DE ports the generators into `scripts/rules/` and `build_release.py` (outputs `views/federal_series_profiles/*.json`, `views/state_class_views/*.json`, `views/job_families.json`, `views/role_change/*.json`, `views/mirror_links.json`) and moves `pipelines/views/tests/test_views.py` into `tests/`.

2. **Change-view atoms have no record type.** WP-08 must give View 1 "which tasks are being reshaped, by what driver, with evidence status". No field carries a task-level reshaping claim with driver tags: `ExposureAssessment` has no `drivers`, `ChangeSignal` has no task target, and `RoleProfile` has no change field. The atoms are in `docs/build/WP-08/change_view_inputs.yaml` (generated from the role specs, agent drafts), and `change_view.py` joins them with signals, external context and v1 prior pointers. **Proposed (preferred):** add optional `drivers[]` (`vocab/change_types.yaml#driver_tags`) and `contentChangeType` to `ExposureAssessment` construct (b), so the atoms become `raterType: llm` deployment-mode rows owned by LM/FS under WP-10. **Alternative:** an optional `RoleProfile.changeClaims[] {task, contentChangeType, drivers[], instruments[], signals[]}`. Either way the atoms migrate mechanically.

3. **Where the applicant variant sits.** The acceptance criterion links R11 ↔ R37 ↔ "applicant variant"; ADR-0017 §4 names the triad permit writer ↔ permittee compliance manager ↔ consultant preparer. `mvp_role_set.csv` lists no private variant for R11, and the X5/X11 builders reject actors that the role set does not list. WP-08 therefore authored the applicant-side preparer as **`seed:R37-facility-environmental-compliance-specialist/private/applicant-preparer`** (service-provider, contracted, consulting-engineering), linked by X11 `emst:mirrorRole` rows from R11/state and R11/federal (TR-17). **Decision needed:** keep it there, or add `private` to R11's variants by erratum and move the slice to `seed:R11-environmental-permit-writer/private/applicant-preparer` (a re-key; nothing else changes).

4. **Mirror links between variants have one home only.** Variant-to-variant mirrors are X11 rows (`emst:mirrorRole`); `RoleVariant` has no mirror field, and WP-08 does not store one. **Proposed:** ratify X11 as the single source and treat `mirror_links.json` as the computed view (no stored inverse; ADR-0029 rule 2). This complements CR-SC-001 item 3 (competency-level mirrors).

5. **`StateClassRecord.emstMapping.competencyTargets` would duplicate role data.** SPEC §5.21 lists "competency targets with level" in the EMST mapping record as MUST. Copying them from the RoleProfile into each class record stores a second copy that goes stale when the role changes. After WP-08 authored the variants, the X5 re-run linked `roleVariant` and left `competencyTargets: []`; the State Class View computes the targets at the mapped role level. **Proposed:** amend SPEC §5.21 and `vocab/state_class_fields.yaml` so that `competencyTargets` is computed (view only) and the stored mapping keeps role variant, role level, match type, confidence, reviewer and review date.

6. **Per-level indicative bands.** `indicativeGradeOrBand` holds one `band` string per variant, but the Federal Series Profile groups by grade band within a role. WP-08 uses a documented micro-format, `"GS-9 to GS-11 [journey]; GS-12 to GS-13 [senior]"`, parsed by `viewlib.parse_band`. **Proposed:** ratify it, or add an optional `byRoleLevel {roleLevel: band}` object inside `indicativeGradeOrBand` (label unchanged: "not a classification criterion").

7. **Role targets in L5 records still use placeholders (to LM, not CA).** 159 `W-MVP-ROLE-TARGET` warnings: LM's ChangeSignals and external-index ExposureAssessments target `mvp-role:<role_key>`. The RoleProfiles now exist as `seed:<role_key>`, so LM can re-key them in WP-10's builder. The WP-08 change view already reads both forms.

## What WP-08 did meanwhile
Nothing in the schema, `scripts/` or `vocab/` was changed. All five views are generated, tested (`python -m pytest -q pipelines/views/tests`) and rebuilt by `pipelines/views/build_views.sh`.

## CA ruling

- **Ruling:** **accept 1, 4, 5, 6 and 7; accept 2 with a narrower field; decide 3 (keep under R37)** · **Date:** 2026-10-23 · **Decider:** CA · **Recorded in:** ADR-0030 §1.9, SPEC §5.8, §5.12, §5.21, §14.2 (draft.3), `vocab/state_class_fields.yaml#emst_mapping`, `vocab/rules/` (five rules), build plan WP-08 acceptance, DECISION_LOG `CR-FH-001`
- **Note:** this CR arrived during the CA's S1-close session and is ruled with the batch.
- **Implementation:** DE per `RULINGS_FOR_DE.md` §19; LM for items 2 and 7; FH for item 6.

1. **Rules: registered, with display constraints.** The CA has registered five rule files as `interim`, each with its WP-08 generator as `reference_implementation`:
   - `federal-series-profile@0.1.0`
   - `state-class-view@0.1.0`
   - `job-family-membership@0.1.0` (FH's file, with the importance rule from CR-CP-001 B4)
   - `role-change@0.1.0`, which merges FH's `role-change-inputs` with CP's summary
   - `mirror-links@0.1.0`

   DE ports the generators into `scripts/rules/` and `Builder.views`, and moves `pipelines/views/tests/test_views.py` into `tests/`. The view paths are `views/federal_series_profiles/<code>.json`, `views/state_class_views/<jur>--<code>.json`, `views/job_families.json`, `views/role_change/<role_key>.json` and `views/mirror_links.json`. The release then serves them, and CP stops reading `docs/build/WP-08/generated/`.
   - **Display constraints the ported views follow (CR-CP-001 B4):** no `timeShare` or `importance` in the FSP or SCV before `job-analysis-confirmed`; no `critical` or `neededAtEntry` before a named human review; target levels as editorial drafts. The series status still comes from the dated register and is never shown as realigned while only proposed.
2. **Change-view atoms: accepted with a narrower field.**
   - `ExposureAssessment` gains optional `contentChangeType` (`vocab/change_types.yaml#content_change_types`) in construct (b).
   - **No `drivers[]` on ExposureAssessment.** For technology drivers the driver is already given by `technicalExposure[].vector` (llm-cognitive → AI, sensing → sensing-tech, robotics → automation-robotics, convergent → AI with others). A second field would store the fact twice.
   - **Non-technology claims are not task assessments.**
     - Policy-reform reshaping is computed from task and competency sensitivity edges and instrument events. A task-specific policy claim becomes a task edge, reviewed by SC (CR-SC-001 ruling, item 1).
     - Fiscal, demographic, workforce-capacity, climate and market claims are role- or organization-level ChangeSignals (LM).
   - **Migration is not mechanical:** an ExposureAssessment needs codebook E-levels that the atoms lack. For rc.1, `change_view_inputs.yaml` stays WP-08's authoring input, and View 1 shows "assessment pending" (CR-CP-001 B6). Converting technology atoms into `raterType: llm` ExposureAssessment rows requires a coding pass under `emst-exposure@2.0`: three passes, recorded like craft ratings, by FH's raters into a WP-10-lane file written by LM. That pass is scheduled for S3, or rc.2 if S3 is full.
   - `RoleProfile.changeClaims[]` is rejected. Judgments are L5 records, not L3 fields (SPEC §5.5).
3. **Applicant variant: keep `seed:R37-facility-environmental-compliance-specialist/private/applicant-preparer`. No erratum.**
   - A variant shares its role's function and core task bundle (SPEC §5.8). The applicant-side preparer prepares and defends applications for the regulated party; it does not decide them. Its authority position is R37's, not R11's (ADR-0017).
   - The X11 `emst:mirrorRole` rows from R11/state and R11/federal satisfy the acceptance criterion. The build plan's WP-08 acceptance now names this key.
4. **Variant mirrors: X11 ratified as the single source.** `mirror_links.json` is the computed view (`mirror-links@0.1.0`), with no stored inverse. It also lists competency-level mirrors from `Competency.mirrors[]` (CR-SC-001 ruling, item 3), labelled by level.
5. **State class mapping: accepted.**
   - `StateClassRecord.emstMapping` stores role variant, role level(s), match type, confidence, reviewer and review date. Competency targets are computed by the State Class View and are never stored.
   - The CA has amended `vocab/state_class_fields.yaml#emst_mapping` and SPEC §5.21. DE adds `emstMapping.competencyTargets` to the computed-field lint. The empty `competencyTargets: []` arrays are removed in the same change.
6. **Per-level bands: optional `indicativeGradeOrBand.byRoleLevel` accepted** (`{<roleLevel key>: band}`). `band` becomes optional when `byRoleLevel` is present, and the label is unchanged ("not a classification criterion"). FH writes `byRoleLevel` and drops the micro-format; `viewlib.parse_band` is retired once the port lands.
7. **Placeholders: confirmed for LM.** LM re-keys the 159 `mvp-role:<role_key>` targets to `seed:<role_key>` and `seed:<role_key>/<sector_actor>` in WP-10's builder in S2, before WP-12 reads signals. Records that stay unkeyed remain excluded from releases.
