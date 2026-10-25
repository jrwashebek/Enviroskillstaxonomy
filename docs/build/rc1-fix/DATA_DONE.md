# D-DATA lane done (rc.1 fix pass, 2026-10-25)

D-DATA (AI agent holding the IO, LM, IA and CA codes) has finished findings M2–M10, m5–m10, m13 and the data parts of
m14 of `docs/review/data_method_review.md`, as `docs/review/DATA_FIX_BRIEF.md` decides. Decisions and the
conservative choices are in `docs/decisions/ADR-0032-rc1-recut-data-method-fixes.md` and `CR-CA-001`; the work
is logged in `WORKLOG_DATA.md`. Nothing was committed or tagged. No human has reviewed any of it.

## Summary

- **Status:** `python3 scripts/validate_v2.py`: 0 errors; `--strict`: 0 errors, 128 warnings;
  `python3 -m pytest -q tests`: 472 tests, all pass; `scripts/migrate_v1.py --check` and `scripts/build_schema.py --check`:
  OK and current. Reviewer checks c4–c8 confirm the fixes in the source tree. The only open item is the 147 positive
  NoTermFound rows that the build's redaction writes into the released X1 (REQUESTS_FOR_BUILD R-04).
- **Schema** (`schema/src/`, regenerated with your unchanged generator; SPEC 2.0.0-draft.4): `LifecycleBasis` and
  `lifecycleBasis`; `Indicator.obs4` nullable plus `obs4Draft`; `Competency.levelSpanBasis`; rating base
  `validationStatus` (required), `passIndex`, `sessionId`, `sampleFrame`, and fixed v1-analyst provenance values;
  v1-analyst ExposureAssessments may not carry v2 construct fields, and `mappingRule` is gone; ChangeSignal
  `sourceGrade` (was `reliability`), `upstreamSource`, `processingChain`, `observationId`, `independenceKey`
  (required, `$ref v_independenceKey`), `measure.difference`, `measure.nullReason`.
- **Rules:** change-indicator@1.1.0, effective-use-tier@1.1.0, role-change@0.2.0, federal-series-profile@0.2.0,
  state-class-view@0.2.0 and counts@1.2.0 are active; the versions they replace are superseded and kept.
- **Your requests:** R1 n/a, R2 done, R3 done, R4 done, R5 declined (keep your overlay), R6 done
  (`REQUESTS_FOR_DATA.md`). **Mine:** R-03 to R-08 (`REQUESTS_FOR_BUILD.md`).

## Changed record types and fields

| Type | Records | Fields |
|---|---|---|
| ChangeSignal | 110 | `reliability` → `sourceGrade`; new `upstreamSource`, `processingChain`, `observationId` (70 distinct, 68 released); `measure.difference` (10 OpenLMP signals); `measure.nullReason`; `direction` (incl. `indeterminate`) and `directionConfidence` on 55 (`generated/signal_direction_changes.csv`); `changeNote` |
| ExposureAssessment, v1-analyst | all | `deploymentMode`, `sWatch`, `tacitExperienceRequirement`, `mappingRule` removed; `evidenceLabel` J → S; `provenance.method` llm-assisted, `toolVersion`, `promptVersion`; `validationStatus` |
| ExposureAssessment, emst-exposure@2.0 | 171 | `sampleFrame`; `raterId`, `passIndex`, `sessionId`, `method`, `provenance.agent`; `validationStatus` |
| CraftRating, FunctionRating, RelevanceRating | all | `validationStatus`; llm passes: `raterId` (8 IDs, one per model and prompt family), `passIndex`, `sessionId`, `method`, `provenance.agent`; v1: `evidenceLabel` S and provenance as above |
| Competency | 224 | `levelSpanBasis` (all); `levelSpan.max` L5 → L4 (CMP-0HTAC6Q, -3WFPTJ9, -7JXTB4F, -DFBQTY4, -WZ4CQR1); `derivedFrom` (CMP-3WFPTJ9, -CZZ31P2, -8QWCQ3R, -5NFAM97); lifecycle (26, below) |
| Indicator | 1,706 | `obs4` → null, `obs4Draft` added (all); lifecycle (201) |
| Task | 147 + 8 new | lifecycle (147); 8 new review tasks (below) |
| RoleProfile, RoleVariant, Enactment, Pathway | 8, 44, 3, 11 | `lifecycleState` → watch, `lifecycleBasis`, `reviewBy`, `changeNote` |
| StateClassRecord | 38 | `workDescriptionText`, `mqText`: `storage` url-only, `sha256` removed |
| Held (Tribal hold) | 41 | 3 routed + 38 by inheritance (29 ratings, 7 indicators, 2 tasks): `indigenousDataFlag`, `approvalStatus` pending-tribal-review, `sensitivity` restricted-governed, `aiUsePermitted` false; listed in `data/v2/governance/tn_review_queue.yaml` (new) |
| Mapping sets (SSSOM) | 9 sets | `predicate_modifier: Not` on 220 NoTermFound rows; X1 justification and `other`; X2 `review_status` (198) and set `other` (κ, numbers); `held_variants` removed (129); hold-neutral metadata |

Vocabularies: `change_types.yaml`, `lifecycle_states.yaml`, `exposure_instrument_v2.yaml`, `mapping_predicates.yaml`.

## Lifecycle changes (the package must be updated for these)

No record met an entry test, so no record is `proposed` or `emerging` any more. 440 records moved to `watch`
(`generated/lifecycle_changes.csv`).

**Roles (8):**

| ID | Role | Before |
|---|---|---|
| `emst:core/ROL-7DTPX8B` | Ground-truth and validation steward | emerging |
| `emst:core/ROL-8V0NKZ4` | Permitting technology product owner | emerging |
| `emst:core/ROL-AC7DRZ6` | AI-assisted environmental review lead | emerging |
| `emst:core/ROL-ETRR81A` | Knowledge continuity lead | proposed |
| `emst:core/ROL-RTNR722` | Environmental AI assurance officer | proposed |
| `emst:core/ROL-XVN70QT` | GHG and nature data controller | emerging |
| `emst:forest/ROL-FSCZ00K` | Fire intelligence analyst (continuous operations) | emerging |
| `emst:forest/ROL-G90XCWY` | Intergovernmental stewardship agreement manager | emerging |

**Competencies (26, all previously emerging):** core CMP-0AES3WF, -0ET1TVQ, -1TY9TQH, -6EYD4G1, -7JGQFKZ, -AJ2N74N,
-AY1JPJR, -BEN7KNR, -BQRDVKJ, -F6ZC95V, -G675QW3, -KEHNFZ7, -KXG302R, -MH34DHE, -MS40XXX, -N3V5JCP, -PKREZ0G,
-PYFVWSR, -QSAV0HJ, -VMK86P6, -WJ60RG0, -X2Y7C07; envhealth CMP-HDA7HQX; forest CMP-PE8PB46; hazards CMP-S73NCC7;
waste CMP-1HZYAB0. Titles are in the csv.

Also moved: 44 role variants, 147 tasks, 201 indicators, 3 enactments, 11 pathways.

**For the content owners (not changed here):** under the new meaning, some of these competencies describe work that
is long-standing in parts of the sector (for example post-disaster field assessment, sensor networks, trace and
genetic sampling, emerging contaminants). They may be `established`; that is a content decision with evidence, so it
is left to the owners.

## New records that need IDs minted

Eight draft review tasks (m7; `add_review_tasks.py`), each `status: draft`, `validationStatus: draft`, evidence S:

| Seed key | Module | Supports |
|---|---|---|
| `seed:rc1-m7-adaptation-analysis-review` | core | `emst:core/CMP-94MWBXW` |
| `seed:rc1-m7-biodiversity-analysis-audit` | core | `emst:core/CMP-PYQADZP` |
| `seed:rc1-m7-carbon-estimate-verify` | core | `emst:core/CMP-H55Y4NM` |
| `seed:rc1-m7-compliance-guidance-review` | core | `emst:core/CMP-BR5Q9TJ` |
| `seed:rc1-m7-ecosystem-service-estimate-verify` | core | `emst:core/CMP-G0WT56E` |
| `seed:rc1-m7-legislative-product-verify` | core | `emst:core/CMP-7JXTB4F` |
| `seed:rc1-m7-wilderness-analysis-review` | parks | `emst:parks/CMP-YS52BS8` |
| `seed:rc1-m7-agreement-report-verify` | wildlife | `emst:wildlife/CMP-6S8JA64` |

No other new record. 41 already-minted records are now held, so their IDs must not appear in any release file (R-06).

## Package edits needed (not made; `docs/package/` is outside this lane)

1. Re-run `docs/package/report/figures/build_figures.py` (m13). F05/F06 now label rows by the difference interval
   and add difference columns; the captions change.
2. Remove "emerging" or "proposed" from the eight role briefs and any competency text above. For example, the
   ground-truth and validation steward brief says "(emerging)". Describe them as watch: hypothesized work.
3. Lifecycle wording: "established" means long-standing work, not validated; lifecycle no longer caps the use tier.
4. Signal counts: 110 signals, 70 distinct observations (68 released); five OpenLMP readings, SIG-84J3FBK and
   SIG-VFA30PA are indeterminate; 43 projection readings are low confidence.
5. X2 statement: 202 of 316 name an O*NET task; 16 agreed at closeMatch or better; κ 0.465, gate fail.
6. Rater statement: repeated passes of one model are one rater; agreement is run-to-run consistency.
7. v1 tags: single-analyst, LLM-assisted, evidence S.
8. HR views: rows below closeMatch are excluded; confidence is the agent's, uncalibrated.
9. Counts that come from the build (effective tiers, FSP and SCV files, held and released totals): take them from
   the re-cut's `counts.json`.
