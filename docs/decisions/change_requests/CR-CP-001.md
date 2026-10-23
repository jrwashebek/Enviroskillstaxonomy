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

## CA ruling

- **Ruling:** **accept A1–A3; decide B4–B6; confirm C7–C8** · **Date:** 2026-10-23 · **Decider:** CA · **Recorded in:** ADR-0030 §1.8 and §6, SPEC §10.5 (draft.3), `vocab/rules/role-change@0.1.0.yaml`, `vocab/rules/pathway-edges@0.1.0.yaml`, `vocab/rules/display-gate@1.1.0.yaml` (draft), DECISION_LOG `CR-CP-001`
- **Note:** this CR arrived during the CA's S1-close session and is ruled with the batch.
- **Implementation:** DE per `RULINGS_FOR_DE.md` §19; IO for the display-gate parameters.

**A. Views from the release**
1. **`views/venue_applicability.json`: accepted.** `venue-applicability@1.0.0` is registered (CR-SC-001 ruling, item 4). Until DE ships it, the explorer may keep the labelled prototype stop-gap but MUST NOT show a `required-basis` value. The prototype over-reads rescissions, which is the defect CR-SC-001 fixes. Show "basis not yet linked" instead.
2. **Federal Series Profile and State Class View in the release: accepted** (CR-FH-001 ruling, item 1). The release applies its own gate; the explorer's ID re-check stays as a second guard.
3. **Rules registered** (`interim`, ported by DE):
   - `pathway-edges@0.1.0` as proposed.
   - CP's `role-change-summary` is folded into FH's change-view rule as **`role-change@0.1.0`**, because one view should have one rule. Following B4, its summary counts tasks by assessment status per role level. It does **not** use time shares.

**B. Rulings**

4. **Role-profile bundle values: split into editorial design values and gated job-analysis values.**
   - **Editorial design values**, shown labelled "editorial draft (agent-drafted, unreviewed)" at describe tier and never in a `select` context:
     - which tasks and competencies a role bundles, and its `roleLevels`;
     - `taskBundle[].formationTask` (protective, derived from `formationDependency`);
     - `competencyTargets[].targetLevel`.
     The gap check (View 2) and pathway edges (View 3) need target levels. A target level is a role-design statement that the Delphi validates later. It is not a measured rating.
   - **Gated job-analysis values**, which render as "Assessment pending (job analysis)" until a named human review:
     - `taskBundle[].importance`, `timeShare`, `critical` and `neededAtEntry`;
     - `competencyTargets[].importance`, `distinguishing` and `criticalForSelection`.
     These are what a job analysis measures, and WP-03's rule already forbids an LLM as sole coder of `critical` and `neededAtEntry`. They render from `validationStatus ≥ reviewed` with a `pid:` reviewer, labelled with that status. In the Federal Series Profile and State Class View, `timeShare` and `importance` render only from `job-analysis-confirmed`: percentage of time is a classification factor, and those views say "not a classification basis".
   - **Consequences:**
     - The FSP lists major duties without percentages ("% time: set by the supervisor; EMST supplies none before job analysis").
     - View 1 uses task counts, not shares.
     - `job-family-membership@0.1.0` weights targets by `importance` only once they are job-analysis-confirmed, and otherwise weights them equally.
     - The values stay in the records and the bundle with their `validationStatus` (data download ungated).
   - The CA has registered `display-gate@1.1.0` as `draft` with these lists. IO adds them to `validation/display_gates.yaml` and `decide()`, then sets 1.1.0 active and 1.0.0 superseded.
5. **Module rule in HR views: CP's reading confirmed, with one precision.** "Modules stay out of default HR views" (ADR-0018 consequences) governs cross-role default navigation: catalogue browse, job-family lists, and competency lists not scoped to a role. Those show core content only.
   - In a role-scoped view (FSP, SCV, role page), the competencies of the role's or variant's **home module**, and the module enactments of core competencies in that module, render in the main section. Each carries its module label and the Q8 note "editorial section, not a stewarded module".
   - Content from other modules, and items that are not `established`, go to the collapsed "not part of the default HR view" section.
   - Module-homed roles stay in the default HR views (R14 Forester's 0460 profile is not emptied).
6. **Task-level reshaping claims: confirmed not rendered.** Agent change judgments render as "assessment pending". At role level the view shows release records only: linked instruments with dated status, through typed links and sensitivity edges, and watch signals. They become records under CR-FH-001 item 2 and stay gated there. `externalContext` is never shown (licence; ADR-0029 §9.6).

**C. Confirmations**
7. **Credential gates: confirmed.** A gate renders only when its Credential has `issuerVerified.verified = true` with sources (SPEC §10.5 rule 8), with "n not shown until the issuer is verified" for the rest. FH rewords WP-08's `evidenceNotice` to match. LM (WP-15) and LC prioritize issuer verification for gates on P1 tasks.
8. **v1 Task 13 codes:** confirmed never read or shown.

## Implementation note (CP, WP-12, 2026-10-23)

- **A1.** The explorer computes the federal-applicability view with DE's registered `scripts/rules/venue_applicability.py#compute` over the release bundle (`site/tools/venue_view.py`). It is labelled "rule venue-applicability@1.0.0 applied to the release records, not yet emitted by the release build". The WP-05 prototype remains only as a fallback, and the explorer never shows "required-basis" from it. The explorer switches to `views/venue_applicability.json` automatically when the release emits it.
- **A3.** The reference implementations are in `site/lib/model.mjs`:
  - `levelCounts` implements `role-change@0.1.0`;
  - the "pathway-edges@0.1.0" block compares the origin's highest role level with the destination's first role level.
- **B4.** Job-analysis values are gated by `jaGate()` in `site/lib/model.mjs` until IO activates `display-gate@1.1.0`.
- **B5 and B6.** Implemented as ruled.
- **C7.** Implemented as ruled, with one addition from the coordinator: a gate whose issuer is verified reads "may be involved (agent-drafted link, not a verified requirement)", never as a requirement.
- **WP-15 sign-off.** Records tied to unverified register rows render as "Unverified — not for citation" (`site/claims/register_map.yaml`). `site/tools/check-output.mjs` section E fails the build on any `do_not_say` wrong form.
