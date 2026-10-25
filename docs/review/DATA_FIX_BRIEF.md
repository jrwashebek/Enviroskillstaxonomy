# rc.1 data and method fix pass — shared brief (2026-10-25)

An independent data and methods review of 2.0.0-rc.1 is in `docs/review/data_method_review.md`. It found 1 blocker, 11 major and 15 minor findings, each with evidence and an exact fix. Read the whole review before you start.

rc.1 has **not** been tagged or distributed. This pass fixes the findings and re-cuts `2.0.0-rc.1` from a clean commit. Record the re-cut in ADR-0032. Every rc.1 ID is still `candidate`. Any ID that must change follows ADR-0010: deprecate it, never reuse it.

## Decisions that bind this pass

These are orchestrator decisions under the rule "hide rather than show; defer rather than invent".

1. **M1 (agent drafts in the bundle and CSVs).**
   - In the JSON-LD bundle, move every display-gated value into a sub-object named `agentDraft`. This covers role `taskBundle[]` importance, timeShare, critical and neededAtEntry; `competencyTargets[].importance`; and any other value that `validation/display_gates.yaml` gates. The sub-object carries `raterType`, `validationStatus` and the display-gate label.
   - In every CSV and HCM export, leave these values out altogether.
   - Remove `work_function`, `field_dependency` and `formation_dependency` from `csv/tasks.csv`, or replace each with a `*_status` column that holds only the gate label.
   - Rename `use_class` to `use_class_declared`, and set `obs4` to null until humans double-code it, as m8 asks.
   - Add `effective_use_tier`.
   - Name all of this in the Release manifest notice.
2. **M2.** Relabel every `v1-analyst` rating to `evidenceLabel: S`, with `provenance.method: llm-assisted`, `toolVersion: unknown (v1 sessions)` and `promptVersion: legacy/v1 working records`. Add `validationStatus` to the rating base in the schema and set it on every rating.
3. **M4.** Passes by one model with one prompt are **one rater**. Use a single `raterId` per model and prompt family, plus `passIndex` (1–3) and `sessionId`. Every rating's `method` text must say "run-to-run consistency of one model; not independent raters; not reliability". Replace "independent" with "repeated" in AUTHORING_GUIDE §4, PHASE4_BUILD_PLAN §WP-03 and S1_AUTHORING_BRIEF.
4. **M7 (lifecycle).** Lifecycle describes the *work* in the sector. `validationStatus` describes the *record*.
   - Redefine `established` in `vocab/lifecycle_states.yaml`, through a change record, as "long-standing work in the sector; EMST content validation is tracked separately in `validationStatus`".
   - Remove lifecycle's cap on use tier. Use tier is capped by `validationStatus` and the display gate.
   - Roles and competencies marked `proposed` or `emerging` that do not meet the vocabulary's entry thresholds become `watch`. Store a `lifecycleBasis` with the evidence and the threshold test, and make the validator check it.
   - List every role whose state changes, so the package can be updated. For example, the ground-truth and validation steward brief says "(emerging)".
5. **M10.** Federal Series Profiles and State Class Views exclude rows below `skos:closeMatch`, or show them only in a section labelled "unreviewed agent candidates (not an alignment)". Rename `confidence` to `agentConfidence (uncalibrated)`.
6. **M8.** Keep v1 exposure values only in `v1Values`. Drop the v1-mapped `deploymentMode` and `tacitExperienceRequirement` from `v1-analyst` records, or rename them `v1Mapped*`. Mark stale v1 assessments (task-text hash mismatch) `stale: true`. Add `sampleFrame` to the 2.0 batch, and `intensityRank` to the E-levels.
7. **M5 and M6.**
   - The independence key becomes an enumeration generated from `vocab/change_types.yaml`. The validator rejects unlisted keys at every status.
   - Add `upstreamSource` and `processingChain`, and make ER-1 require disjointness on all three.
   - One observation is one record, attached to several targets by `targetIds[]`. Alternatively give each record an `observationId`; in that case counts must report distinct observations.
   - Add the direction `indeterminate`, and apply it wherever the difference interval includes 0 or a sensitivity check erases the effect.
   - Cap projection-family confidence at `low` when the crosswalk is broader than closeMatch.
8. **M3 and M9 (crosswalks).**
   - X1 uses `semapv:LLMBasedMatching` with its decision source.
   - The X2 status becomes `two-llm-coders-agreed-target`, with κ recorded on the set.
   - NoTermFound rows use one documented convention: `predicate_modifier: Not`, or no positive predicate.
   - Gate statements give the honest numbers.
9. **B1 and the exports.**
   - Apply `_lang()` only where the schema types a field as Text.
   - `self_check()` validates every bundle node against the schema, minus the documented computed fields, and fails the build on any error.
   - Redaction must never leave a required field empty. Hold back the record instead, or emit `indeterminate (basis withheld)` for venue applicability (m4).
   - Add a JSON-LD round-trip test.
   - Add context terms for the dropped keys (M11).
   - Fix the frictionless `created` field (m2).
   - Refuse `+uncommitted` under `--profile release` (m1).
10. **Release notes.** The generated notes must state:
    - the gate status line: "not cleared for external publication; items 6 and 7 fail" until they pass;
    - that IDs are candidate and become stable from 2.0.0 (m11);
    - which SPEC §12.5 and §17.2 artifacts rc.1 omits (m3);
    - a breakdown by rater type and by distinct units (m12).
11. **Sign-off path (project lead decision Q13, 2026-10-24).**
    - External publication is signed by the **EMST project lead, after at least one named human subject-matter reviewer** has read the report and briefs. AI agent checks, including the adoption-lead role, are advisory.
    - Update gate item 7 in `docs/decisions/PHASE4_BUILD_PLAN.md` §5, `docs/methods/WP15_SIGNOFF.md` and the gate report to match. Do not record any human sign-off that has not happened.
12. **Tribal hold (m14).**
    - Replace the X1 comment "Successor withheld pending Tribal Advisory Council review" with "successor not in this release".
    - Drop `held_variants`.
    - Run the trigger scan over every output file and field, including Mapping, provenance, SSSOM, CSV, TTL and views.
    - Route `CMP-2VQTX8E`, `TSK-11X9525` and `TSK-5ZRM1W1` to the TN review queue with `approval_status: pending-tribal-review`. Exclude them from the release until that review happens.

## Lanes for this pass

| Agent | Owns | Findings |
|---|---|---|
| **D-DATA** (holds IO, LM, IA, CA codes) | `schema/src/`, `vocab/`, `data/v2/`, `scripts/validate_v2.py`, `scripts/rules/`, `scripts/migrate_v1.py`, `pipelines/` (x2, crosswalks, views), `validation/`, `docs/standard/` (SPEC → 2.0.0-draft.4, AUTHORING_GUIDE), the build plan and brief wording in item 3, and ADR-0032 | M2–M10, m5–m10, m13 (in `docs/package/report/figures/build_figures.py`; that one file only), and the m14 data parts |
| **D-BUILD** (holds DE, CP codes) | `scripts/build_release.py`, `scripts/build_schema.py` and the generated schema, `schema/emst.context.jsonld`, `tests/test_build_release.py` and new build tests, `site/`, `docs/release/`, `docs/methods/WP15_SIGNOFF.md`, gate item 7 text in the build plan | B1, M1, M11, m1–m4, m11, m12, m15, the m14 scan coverage; then the re-cut and the gate re-run |

**Sequence.**
1. D-DATA finishes its schema and vocabulary changes first, and writes `docs/build/rc1-fix/DATA_DONE.md` when its whole lane is done.
2. D-BUILD works on the build code and tests in parallel against the current schema.
3. When `DATA_DONE.md` exists, D-BUILD does the final work:
   - regenerates the schema;
   - mints any new IDs, using the single writer and only for new records;
   - rebuilds the release twice and confirms the two builds are byte-identical;
   - regenerates the views and the explorer, and runs `check-output.mjs`;
   - re-runs the release gate;
   - writes `docs/release/2.0.0-rc.1/GATE_REPORT.md`, `RELEASE_NOTES.md` and `counts.json` again.

**Rules.**
- Never `git commit` or `git tag`. The orchestrator commits, and tags from a clean commit after the gate re-run.
- Never edit `docs/package/` beyond m13's figure script. List any package edits needed in your final reply.
- Agent ratings stay `raterType: llm`.
- No personal data.
- If the harness refuses a write, do not work around it; return the text instead.
- Write progressively: container restarts happen.
- Keep a worklog at `docs/build/rc1-fix/WORKLOG_<DATA|BUILD>.md`.

**Final reply** (at most 250 words): each finding marked fixed, deferred or rejected, with a reason; the test, validator and gate status; and the package edits needed.
