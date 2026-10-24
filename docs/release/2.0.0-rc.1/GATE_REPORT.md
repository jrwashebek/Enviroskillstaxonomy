# EMST 2.0.0-rc.1: release gate report

- **Prepared by:** CA, holding the DE code for the build (AI agent roles, not people), WP-16. Run on 2026-10-23 against the tree as it stands; nothing has been committed or tagged.
- **Gate:** `docs/decisions/PHASE4_BUILD_PLAN.md` §5, items 1–8. The rulings behind this build are in ADR-0031.
- **Numbers.** Every number below comes from a command named in this report or from `docs/build/WP-16/generated/gate_evidence.json`, which `docs/build/WP-16/gate_evidence.py` generates from `dist/2.0.0-rc.1/`. None is typed from memory.
- **Authorship.** AI agents researched and drafted this release. No human subject-matter expert has validated anything in it.

## Summary

| § 5 item | Result |
|---|---|
| 1. CI green | **pass** (one non-gating report needs an IO fix) |
| 2. Core size within G-9 | **pass** |
| 3. Use tiers; nothing `select`; α gate | **pass** |
| 4. Wave-1 present; wave 2–3 absent except named early drafts | **pass** |
| 5. 37 roles at tier depth; FSP and SCV for P1–P2 federal and state variants | **conditional** |
| 6. Crosswalks X1 complete; X2 for P1 tasks; X3, X4, X5, X7, X12 at reviewed-subset level | **fail** |
| 7. WP-15 sign-off on every external claim; ACR and security packet attached | **fail** |
| 8. Q1–Q2 recorded | **pass** |

**Overall.** rc.1 builds reproducibly and is internally consistent, and it may be tagged as a release candidate for the NGO-pilot preview and the design partners. It is **not cleared for external publication**:
- item 7 fails until AS co-signs and the moving facts are re-checked on or after their dates;
- item 6 fails until humans review a subset of each crosswalk.

**Determinism** (WP-16 output). Two consecutive builds were made: `python scripts/build_release.py --profile release --version 2.0.0-rc.1`, then the same with `--out dist/2.0.0-rc.1-b --no-validate`. `diff -r` found them **byte-identical**. The SHA-256 of `SHA256SUMS` is in `BUILD.md` in this folder. A build made after the orchestrator commits carries that commit in its build line, so its hashes will differ.

---

## 1. CI green on schema, cross-record rules, typing and indicator lint, Tribal hold, personal data, computed-field and v1-completeness checks

**Result: pass.** One non-gating report needs a fix in IO's lane.

**Evidence** (same commands as `.github/workflows/ci.yml` and `release.yml`):

| Command | Output |
|---|---|
| `python scripts/extract_v1.py --check` | v1 baseline is up to date |
| `python scripts/build_schema.py --check` | schema and context are current with vocab/ |
| `python scripts/validate_v2.py --registry-base <empty base>` | **0 errors**, 156 warnings |
| `python scripts/validate_v2.py --strict --no-git-base` | **0 errors**, 156 warnings: W-REF-DEFERRED 19, W-X1-DEFERRED 12, W-INDEPENDENCE-KEY-UNLISTED 74, W-LINT-* 48, W-SUPERSEDED-TARGET 3 |
| `python scripts/migrate_v1.py --check` | 0 generated files differ |
| `python scripts/convert_instrument_links.py --check` | 0 links to convert |
| `python scripts/mint_id.py verify` | OK: 10472 registry rows |
| `python scripts/update_readme_status.py --check` | README status block is current |
| `python -m pytest -q` | **371 passed**, 0 failed, 0 skipped (exit 0) |
| `cd site && npm test` | checker self-test OK (21 seeded violations, 4 near-misses); output check OK, 765 pages, **0 problems**; browser checks OK, 71 pages, 0 axe violations, 0 external requests, 0 reflow failures |

- **Checks that run inside `validate_v2.py`, all at 0 errors in both modes:**
  - **Tribal hold:** E-TRIBAL-HOLD, E-TRIBAL-LEAK, E-TRIBAL-INHERIT, E-ORG-TARGET-TRIBAL, E-COORDS-CULTURAL, E-CONFIDENTIAL.
  - **Personal data:** E-PERSONAL-DATA.
  - **Computed fields:** E-COMPUTED-FIELD.
  - **v1 completeness:** E-X1-INCOMPLETE, E-X1-DECISION, E-X1-DUPLICATE, E-X1-STALE, E-V1KEY-UNRESOLVED, E-V1-WORKBOOK-HASH.
- **The release build's own self-check passed.** It finds no held key, no withheld key and no unminted `seed:` reference in the bundle.
- **The 31 strict errors of the baseline are resolved by rule** (ADR-0031 §5 item 5). They are now W-REF-DEFERRED, because no releasable record names those targets. A test asserts that a minted candidate naming the same target is still an error.
- **Indicator lint, three runs:**
  - **The release gate's lint (inside `validate_v2.py`):** 0 errors. All 48 W-LINT warnings are on unauthored v1 seeds, which are not released.
  - **IO's linter in `--mode release` on the 3,294 released Indicator, Competency, Task and KnowledgeStatement records:** **0 failing** (411 A03 info).
  - **IO's whole-tree report** (`lint_indicators.py data/v2`; the CI step is `continue-on-error`): exit 1. Its loader reads every CSV row and every typeless YAML document as an Indicator, so it reports "required metadata missing" on ID, migration, crosswalk and governance files. Minting added the `ids/` files to that list.
- **Tests.** Four tests encoded the pre-mint state ("nothing is a candidate yet") and three acceptance tests had started skipping silently. All were updated to the post-mint rules, and a test was added for the State Class View file names (ADR-0031 §9).

**What is missing**
- IO: make `validation/lint_indicators.py` skip `data/v2/ids/` and `data/v2/migration/` and require `type` on YAML documents, so the whole-tree report means something.
- The 2,088 I-STALE-ASSESSMENT notices are information, not errors: ratings whose task text changed since rating. They need re-rating before any study uses them.

## 2. Core size within the G-9 range of 120–180 (held included)

**Result: pass.**

**Evidence.** The release notes, generated by `counts@1.1.0`, read: "Core competencies: 164 released + held core reported as a count (11); range 120-180". That makes 175. `validate_v2.py` reports `I-CORE-SIZE core competencies 164 + held 11 = 175 (G-9 range 120-180)`.

**What is missing:** nothing. Headroom to 180 is 5, so a net-new core competency still needs an offsetting merge approved by the CA.

## 3. Every published element shows its use tier; nothing is `select`; every displayed tag meets the α gate or is hidden

**Result: pass.**

**Evidence** (`views/effective_use_tier.json`, `views/display_gate.json`, `gate_evidence.json` item3):
- **Use tiers.** 3,742 elements carry a computed effective use tier: describe 1,891, exploratory 1,851. They are every released competency, task, indicator, enactment, role profile, role variant, knowledge statement and pathway. No element type is missing from the view.
- **`select` appears 0 times**, whether as a declared tier, a use class or an effective tier.
- **Display gate.** `display-gate@1.1.0` made 8,262 decisions: pending 3,977, editorial 3,093, hidden 1,192. **No α-gated value is shown**, because no reliability study exists yet.
- **Explorer.** The output check counts 1,073 figures with badges and 0 problems.

**What is missing:** nothing for rc.1. No tag can show until the first reliability study reports, and the views say so.

## 4. All wave-1 module sections present; wave-2 and wave-3 content absent except the early drafts named in the dispositions

**Result: pass.**

**Evidence** (`gate_evidence.json` item4; released records by module):
- **The nine wave-1 modules are present:** air 147, envhealth 127, forest 468, hazards 122, parks 99, waste 304, water 189, waterq 177, wildlife 174.
- **The only other modules are the two named early drafts:**
  - extract (5 records: IA-CC-05, "Administer mineral and energy authorizations and reclamation", with its indicators);
  - worklands (28 records: FH-C03, "Develop conservation plans with private landowners …", and role R19, Soil conservationist, with its variants, tasks, indicators and ratings).
- `select_promotions.py` refuses any other wave-2 draft (it stops on a stray).
- Planned targets in waves 2 and 3 are not released. They are counted by area in the release notes ("Held and deferred").

**What is missing:** nothing.

## 5. 37 role profiles at their tier depth; Federal Series Profile and State Class View for every federal and state variant in P1–P2

**Result: conditional.**

**Evidence** (`gate_evidence.json` item5; `views/federal_series_profiles/`, `views/state_class_views/`):

**Role profiles: 37** (P1 13, P2 17, P3 6, P4 1).
- **P1:** 22–35 tasks per role. Every role has 16 or more competency targets.
- **P2:** 26–35 tasks per role, with 14 or more targets.
- **P3:** all six carry a lifecycle state, `reviewBy` 2027-10-23 and a named counter-signal.
- **P4:** a draft.

**Federal Series Profiles: 36 series files.** 27 of the 28 P1–P2 federal variants appear in one.
- The exception is R01, Conservation corps member. Its X4 rows are `NoTermFound` for the role itself. Series appear only as destinations after the corps hiring authority, and the port excludes those by design (feeder rule).

**State Class Views: 37 class files.** All 30 P1–P2 state variants are in the index.
- 17 have at least one class view in the pilot jurisdictions (TX, WA, PA; Lewis County WA; Philadelphia Water).
- 13 are mapped to no pilot class, and the index says so.

**What is missing**
1. **"Critical competencies" cannot be counted.** The depth rule asks for 6–12 critical competencies (P1) and 6–10 (P2) with target levels. Every P1 and P2 role has more targets than that. Which targets are *critical* is a job-analysis value, and the gate renders it "Assessment pending" until job analysis. WP-16's rule-based additions (ADR-0031 §5 item 3) raised some counts, for example R13 to 31.
2. **Importance, time share and critical and needed-at-entry flags** exist only as agent drafts. They are hidden by design.
3. **R01:** a decision that a federal corps member has no series profile, recorded as not applicable rather than as a gap. FH should confirm.
4. **The 13 state variants without a pilot class need either a class mapping (SL) or a recorded "not in the pilot jurisdictions" status.**
5. **Every series and class mapping behind these views is an unreviewed agent candidate** (item 6).

## 6. X1 complete; X2 for P1 tasks; X3, X4, X5 (pilot states), X7 and X12 at reviewed-subset level

**Result: fail.** X1 and the coverage of X2 pass. No other crosswalk has a human-reviewed subset.

**Evidence** (`gate_evidence.json` item6; mapping rows in `emst.bundle.jsonld` and `sssom/`):

| Crosswalk | Rows | Review state | Human reviewer |
|---|---|---|---|
| X1 v1 → v2 | 926 | complete: all 888 v1 keys (222 competencies, 666 tasks); validator X1 checks 0 errors | n/a (manual curation by DE) |
| X2 task → O*NET task | 316 | all 316 P1 tasks have rows; 198 `two-coder-agreed-target`, 118 `needs-adjudication`; both coders are LLM agents | 0 |
| X3 variant → O*NET-SOC / SOC | 197 | candidate | 0 |
| X4 variant → OPM series | 333 | candidate | 0 |
| X5 variant → state and local classes | 58 | candidate | 0 |
| X7 competency → ESCO | 338 | llm-reviewed-candidate | 0 |
| X12 → DOL AI Literacy | 49 | candidate | 0 |

**What is missing**
- For each of X2–X12, a subset reviewed by a named human (`pid:`).
- For X2 specifically, two coders with κ ≥ 0.6 on match type (ADR-0022), plus adjudication of the 118 open rows.
- Owners per ADR-0022: LM and IA (X2), IA, FH and LM (X3), FH (X4), SL (X5), IA (X7), DC and LC (X12).
- The agents cannot supply this.

## 7. WP-15 sign-off on every external claim; ACR and security packet attached

**Result: fail.**

**Evidence**

**`docs/methods/WP15_SIGNOFF.md` after the fix passes.** It reads: "Owner: LM (A9) · Co-signer: AS (pending) · … Status: first pass plus a flagship-report check". Its sign-off clears internal drafts and the NGO-pilot preview only, and it says plainly that nothing is cleared for external publication until AS co-signs and the moving facts are re-checked.
- **AS co-signature: not given.** It is a separate sign-off. The CA may not provide it and has not.

**Claims register** (`docs/methods/claims_register.csv`, counted by `gate_evidence.py`): 124 rows.
- **By status:** verified 70, corrected 19, verified-partial 13, unverified 14, derived 6, held 1, illustrative-unverified 1.
- **Changes since the fix passes:**
  - RPT-27 is `derived`.
  - OMB-02 and RPT-04 read "nine agencies and bureaus".
  - PLAN-01 and OMB-02 are single-quoted, and the explorer enforces them.

**How the 15 unverified or held rows reach rc.1:**
- NEPA-09, ESA-02, ESA-03, CWA-02, DISC-03 and REG-01 to REG-07: their records are **withheld** (31 records, `data/v2/governance/release_withheld.yaml`; ADR-0031 §8).
- REG-08 (J-dated days) and REG-09 (base instruments without events): released, with the J label stated and no status asserted.
- TRB-01: held.

**Explorer checks after the rebuild.** The output check reports 0 problems on 765 pages. `grep -rl` for "IRA conservation", "monitoring requirements", "nine environmental bureaus", "intelligent customer", "EXPLORE Act amendments" and "NWCG is not a party" finds no file. No page contains a `seed:` key.

**ACR (`site/ACR.md`) and security packet (`site/SECURITY_PACKET.md`).** Both exist and both are attached. CP (an AI agent) prepared both, and no human reviewer has checked either. Both describe the explorer built from `2.0.0-dev` in the preview profile:
- **ACR:** it reports 0 axe violations on 71 sampled pages. The rc.1 build reproduces that: 71 pages, 0 violations. It lists screen-reader, voice-control and magnification testing as not yet done, so four criteria are "Partially supports".
- **Security packet:** its point 7 still says that instruments tied to unverified rows render as "Unverified — not for citation". In rc.1 those records are withheld.

**Moving facts and re-check dates** (`WP15_SIGNOFF.md` §3; the register's `recheck_by`). None falls on or before 2026-10-23, so **none has been re-signed for the rc.1 build** as §3 requires:

| Re-check on or after | Fact |
|---|---|
| 2026-10-27 | Colorado SB 26-189: AG comments and hearing |
| 2026-10-27 | OFCCP rescission effective date |
| 2026-11-12 | Section 106 NPRM, after the ACHP meeting |
| 2026-11-13 | USFS objection rule effective date |
| 2026-11-15 | SPEED Act / S. 5653 Senate floor |
| 2026-11-30 | FAA Part 108 |
| 2026-12-15 | every other `recheck_by` in the register (49 rows on that date) |
| 2027-01-23 to 2027-08-15 | later rows (64), plus 3 "on next OpenLMP release" |

The Federal Register and Congress.gov must be read directly at the re-check; both were unreachable from the WP-15 session. Census BTOS and the Yale tracker are re-read at rc.1, as the sign-off's §4 says.

**What is missing**
1. **AS co-signature** of WP-15.
2. **The re-checks.** LM re-checks each moving fact on or after its date and re-signs, then the build is re-run.
3. **CP re-issues the ACR and the security packet for the tagged rc.1 build.** That means the version evaluated and the point-7 wording. CP should also add assistive-technology testing when Round 2 runs. Both files are CP's; WP-16 did not edit them.
4. **Package lane:** the flagship report's five required corrections (WP-15 §4) and the CR-FIX-A-001 sentence.

## 8. The lead's answers to Q1–Q2 recorded

**Result: pass.**

**Evidence.** `docs/decisions/PROJECT_LEAD_DECISIONS.md`, both dated 2026-10-23:
- **Q1** (Tribal Advisory Council binding consent authority, charter carve-out, compensation budgeted before first contact): accepted, all three.
- **Q2** (CC0 for the v1 text): accepted.
- **The build reflects Q2.** It excludes no record as "v1-derived text pending CC0 dedication", and `tests/test_build_release.py` asserts that. **The Tribal hold stays in force:** 122 held records are reported only as a count.

**What is missing:** nothing for this item. Q3, Q4, Q6 and Q8–Q11 remain open with their defaults in force.

---

## Decisions for the project lead

1. **Approve external publication** of rc.1, or of a later rc, once items 6 and 7 clear. The comment-window plan (`COMMENT_WINDOW_PLAN.md`) waits on this decision.
2. **CR-FIX-A-001.** The career-ladder hypothesis is published as a finding only after named human reviewers, a qualified industrial-organizational psychologist and a labor economist, validate it. It is then co-published with a nonpartisan partner. This binds the lead's publications.
3. **CR-FIX-B-002.** Decide whether role profiles fitted to each organization are part of the pilot offer, and set a reply-by date and eligibility.
4. **Recruit the human reviewers** for the crosswalk subsets (item 6) and for the AS co-signature path (item 7).
5. **Open questions with defaults in force:** Q3, Q4, Q6, Q8–Q11. Also NH11, the CTA account.
