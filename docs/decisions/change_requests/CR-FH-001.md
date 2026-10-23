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
