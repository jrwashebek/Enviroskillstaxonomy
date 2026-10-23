# CR-CP-001: Release views the explorer needs, and three display rulings

- **From:** CP (A10a), WP-12 · **To:** CA (decider); DE (build), IO (display gate), FH (WP-08 views), SC (venue rule) · **Date:** 2026-10-23 · **Type:** X (computed views) plus three rulings · **SemVer impact:** minor (new computed views; no schema change)
- **Affects:** `scripts/build_release.py` (views), `vocab/rules/`, `validation/display_gates.yaml`, ADR-0016 §3-4, ADR-0018 consequences, ADR-0021, ADR-0027 §1-2, SPEC §10.5
- **Evidence label:** J (found while building the explorer against the S1/S2 data)

## Problem

The explorer (`site/`) is generated from a release build only: `emst.bundle.jsonld` plus `views/*.json`. Three computed views that the WP-12 pages need do not come from the release yet, so the explorer reads stop-gap sources. Separately, three display questions have no ruling, and the explorer has had to pick the fail-closed or conservative reading.

## Proposed change

### A. Views to emit from `build_release.py` (stamped from `vocab/rules/`)

1. **`views/venue_applicability.json`** (endorses CR-SC-001 item 4). The explorer now runs `docs/build/WP-05/ci/venue_applicability.py` into `site/.cache/venue/` and labels the result "prototype computation, CR-SC-001 pending". That script reads `data/v2/` directly, not the released records. The explorer drops rows for competencies absent from the bundle. Once the view exists in the release, `site/tools/prepare-release.mjs` uses it automatically.
2. **`views/federal-series/<code>.json` and `views/state-class/<jur>--<code>.json`** (endorses the rules WP-08 proposes as CR-FH-001). The explorer now reads `docs/build/WP-08/generated/` read-only. Those generators also read `data/v2/` directly, so they bypass the release gate. The explorer re-checks every ID they name against the bundle and drops anything absent, which removes held content. The release should still apply its own gate.
3. **Two rules for computations the explorer does at build time.** Proposed IDs:
   - `role-change-summary@0.1.0`. For each variant it computes the share of listed time by assessment status (pending or assessed) and renormalizes time shares within each role level.
   - `pathway-edges@0.1.0`. For each pair of role variants it computes "shares N of M destination competencies at the destination's target level", the gap list, the named next steps and any learning pathway present.

   ADR-0021 says computed values come from CI. Until these rules exist, the explorer labels the results as computed by `site/lib/model.mjs`. If DE prefers, the explorer's functions can be ported as they are.

### B. Rulings requested (decision points)

4. **DP: Are role-profile bundle values gated?** WP-08 records these as LLM ratings (evidence S, `raterType llm`):
   - `RoleProfile.taskBundle[]`: importance, timeShare, critical, neededAtEntry and formationTask;
   - `competencyTargets[]`: target levels.

   `validation/display_gates.yaml` lists them neither as gated dimensions nor as editorial fields. The explorer **shows them**, labelled "agent draft, evidence S, unreviewed". View 1 and the HR views would otherwise have no time shares at all. If CA or IO rules that they are gated, the explorer will hide them (fail closed). Pages then fall back to task lists without shares and to "assessment pending" for targets.
5. **DP: The module rule in HR views (ADR-0018).** The explorer reads "modules stay out of default HR views" as applying to **competency content**. In the Federal Series Profile and State Class View, a duty, knowledge item or target whose competency is a module record, or is not `established`, moves into a collapsed section labelled "not part of the default HR view". The rule is **not** applied to module-homed roles themselves. For example, R14 Forester is homed in `forest`. Hiding the role would empty the 0460 profile. Please confirm, or rule that module-homed roles also leave the default view.
6. **Ruling to confirm: WP-08's task-level "reshaping claims" are not rendered.** `docs/build/WP-08/generated/change_view/*.json` carries per-task `change[]` claims (kind, drivers, note) and role-level notes. These are agent judgments of how work is changing, made without a multi-rater study. Under the display gate, agent values never render. The explorer therefore shows "assessment pending" for every task. At role level it shows only release records: linked instruments with their dated status, and watch signals. If these claims should be visible, they need to enter as `ExposureAssessment` records with `raterType llm`, where they stay gated. `externalContext` in the same files is never shown, because its records are third-party licensed and excluded from release outputs (ADR-0029 §9.6).

### C. Consistency fixes for other lanes (no ruling needed)

7. **Credential gates.** SPEC §10.5 rule 8 says verified facts need sources and are not shown without them. The explorer shows a credential gate only when the credential's `issuerVerified.verified` is true, which is 19 of 93 register rows today. It shows "n not shown until the issuer is verified" for the rest. WP-08's `evidenceNotice` text says gates are "shown only as drafts", which contradicts the SPEC; FH may want to reword it.
8. **v1 Task 13 codes in WP-07 `formation_provisions.csv`** (`v1_prior_design_prompt`) are never read by the explorer (WP-07 note).

## Consequences if not accepted

- The explorer keeps working from the stop-gap sources and labels them as such.
- The federal applicability and HR pages depend on scripts outside the release gate. The explorer's ID re-check is the only guard.
- Items 4 and 5 stay at the explorer's current reading until ruled.
