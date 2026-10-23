# EMST v1 data audit

**Role:** Data Engineer & Repository Steward (DE) · **Phase:** 1 (audit) · **Date:** 2026-10-23
**Scope:** the five v1 database workbooks, the three exposure side-workbooks, the source competency text, and
the per-domain exposure working records, all under `legacy/v1/`.
**Reproduce:** `python scripts/extract_v1.py && python scripts/diff_v1_versions.py && python scripts/audit_v1.py`
then `python -m pytest -q tests/test_v1_baseline.py` (47 tests, all passing at time of writing). Every number below
comes from `data/v1_baseline/` (mainly `qa/metrics.json` and `qa/*.csv`). If a number here and a file disagree,
the file is right.

Evidence labels follow the team brief: **[E]** evidence (with a source ID from
`docs/research/data-engineering/sources.csv`; DE-001…DE-021 are v1 artifacts, DE-022+ external), **[J]** my
judgment and its basis, **[S]** speculation and what would settle it.

---

## 0. Summary for the Chief Taxonomy Architect

1. **Baseline = `20260223_SkillsTaxonomy_Core_V3_reconciled` copyB.** It is the only version that has all 222
   competencies, Domain 7, Pre-Task 15A and the Domain 6 reconciliation. Its data are identical to copyA; only the
   Data Dictionary sheet differs (+25 rows). The file v1 calls authoritative (`skills_taxonomy_workforce_v1_updated.xlsx`)
   has only 215 competencies, so it cannot represent the "222 × 7 × 45" state that the v1 task sequence describes. [E: DE-001–DE-005, DE-012]
2. **The v1 import from the source text lost or corrupted a third of the assessment content.**
   - 2,104 of 6,484 source indicators (32.4%) are missing, because the import capped indicators at 6 per level.
   - All 30 Domain 5 competencies lost Knowledge and Application in every level (120 levels).
   - Their 360 "indicators" are mis-parsed `Knowledge*:` / `Application*:` / `Indicators*:` lines, so Domain 5
     has no real indicators at all.
   - All of this is recoverable from the source text. The parsed and reconciled copy is in `data/v1_baseline/source_text/`. [E: DE-001, DE-011]
3. **Exposure codes are not reliably attached to the task text they were assigned against.**
   - Domain 1's and Domain 3's working records classified paraphrased or invented task statements. Text similarity
     to the database task was below 0.8 for 82/120 D1 tasks and 98/105 D3 tasks. D1 is not flagged anywhere in v1.
     For D3 the record marks 98 tasks "[source-inferred]"; v1 docs say "~76%".
   - The database then paired those codes with the verbatim source task text.
   - Domain 2's database values disagree with the D2 working records on 68 of 105 tasks, including confirmed anchor
     calls and two confirmed CLD signals that the database drops. [E: DE-014–DE-016, qa/exposure_source_alignment.csv]
4. **Derived fields are not reproducible from their inputs.**
   - Stored "modal" automation type differs from the T1–T3 majority in 63 of 222 competencies.
   - No single priority rule explains the stored values.
   - CLD flags break the documented rule in 11 competencies.
   - All 7 Domain 7 rows overstate their Supporting-family count.
   - The 5 documented dual-primary stage exceptions are absent. Their second stages exist only in the Task 10 record. [E: DE-001, DE-020; qa/consistency_checks.csv]
5. **Proficiency levels are written as templates, not observable behaviour.**
   - The first word of the Knowledge statement is fixed by level: "Understands" 88.5%, "Applies" 94.3%, "Expert in" 98.4%, "Shapes" 98.4%.
   - 670 of 1,536 Knowledge/Application statements (43.6%) start with a cognitive-state or status/influence verb that can't be observed.
   - At Expert level, 298 of 384 (77.6%) are status/influence claims.
   - Indicators are much better: 14.1% / 1.1% / 0.6% / 26.3% non-observable by level. [E: qa/proficiency_genericity.csv] [J on the heuristic]
6. **Summaries and documentation have drifted from the data.**
   - The Workforce Signals dashboard is in the 215-competency state; 19 of its 27 headline metrics differ from the baseline.
   - The change log's Task 13 distribution (A 368, H 136, Ac 92, V 31, S 9 over 636 tasks) no longer matches
     the baseline (A 389, H 125, Ac 101, V 26, S 4 over D1–D6's 645 tasks).
   - Eleven analytical columns have no Data Dictionary entry. [E: DE-001, DE-009]
7. **What is sound:**
   - Task text in D1–D6 is a verbatim copy of the source (645/645).
   - Sector notes match the source (1,075/1,075) once artifacts are removed.
   - Reform-flag counts, Core counts, Zero-Core flags and the stability-tier rule are internally consistent.
   - Lexical near-duplication is low: no competency pair reaches cosine 0.5.
   - Every one of the 666 tasks has at least one working-record classification, and most have a written rationale. [E]

---

## 1. Which version is the v1 baseline

### 1.1 Lineage (by content, from `scripts/diff_v1_versions.py`)

| Step | Workbook | Content change (cells; see `data/v1_baseline/version_summary.csv`) |
|---|---|---|
| v1 | `skills_taxonomy_workforce_v1.xlsx` [DE-005] | 215 competencies, 43 skill areas; Dimension Tags has 45 columns (no exposure); Proficiency Indicators 860 rows |
| → v1u | `skills_taxonomy_workforce_v1_updated.xlsx` [DE-004] | **+25 Task 13 exposure columns** (T1–T3 × 5 dimensions, CLD, S-trajectory, 7 "modal" fields, provenance); Workforce Signals gains a D1 block; Data Dictionary +8 rows. **0** existing cells changed. |
| → v3 | `20260223_SkillsTaxonomy_Core_V3.xlsx` [DE-003] | **+7 Domain 7 competencies** (7.1.1–7.1.4, 7.2.1–7.2.3; +28 proficiency rows; +2 skill areas); **+CLD Severity** column; **Stability Tier changed for 37 competencies** (Stable→Transition: "Ac tasks now trigger Transition"); Data Dictionary +10 rows. No other cell changed. |
| → v3rA | `…_reconciled__copyA_995a86e4.xlsx` [DE-002] | **482 cells in the 40 Domain 6 rows**: per-task exposure re-applied (469 changed, 13 filled). Provenance becomes "D6 exposure file, reconciled March 2026" (30 rows) or "D6 Ac retrospective, Task Pre-15A" (10 rows). Booleans in those rows are rewritten as `Yes`/`No`. Two undocumented CLD severities appear (`Highest` ×4, `Ungraded` ×4). |
| → v3rB | `…_reconciled__copyB_aaf34c8c.xlsx` [DE-001] | **Data identical to copyA.** Only the Data Dictionary differs: +25 rows ("Ethical lens columns: population status", lens definitions, R10 rule). |

[E] Competency text (title, description, tasks, proficiency, sector notes) is identical across all five versions
for the competencies each contains (0 differing cells). The versions differ only in analytical layers, Domain 7 and
documentation. The "three competing database versions" in the team brief are a single linear lineage, not a fork.
The only real choice is whether to accept the March 2026 Domain 6 reconciliation (§1.3).

### 1.2 Decision and rationale

**Baseline: copyB (`20260223_SkillsTaxonomy_Core_V3_reconciled__copyB_aaf34c8c.xlsx`).**

- [E] It is the only version that has all 222 competencies with tags, CLD Severity, Pre-Task 15A, and the most
  complete Data Dictionary. It is also the latest upload (legacy MANIFEST, DE-021).
- [E] v1's own designation of `skills_taxonomy_workforce_v1_updated.xlsx` as authoritative (task sequence v7
  header and change log header; DE-012, DE-009) is internally inconsistent. The same documents say the current
  state is 222 competencies, and v1u holds 215. Pre-Task 15A's completion check is written against v1u, which never
  received it.
- [J] Choosing copyB does not discard anything. Every earlier value is kept in `version_diffs.csv`, so a v2
  decision to reverse the D6 reconciliation can be made from data.

### 1.3 Was Pre-Task 15A applied?

**Yes, in copyA/copyB only, and not cleanly.** [E: DE-006, `exposure_sources.csv`, tests `test_exposure_record_alignment_pinned`]

- All 12 A→Ac reclassifications (SA 6.3: 5, SA 6.8: 7) are present, and all 10 competencies in 6.3/6.8 carry the
  Pre-15A provenance label, so completion checks 1–3 pass.
- 24 of 30 reviewed tasks match the Pre-15A tuple exactly. The other 6 are hybrids:
  - three keep the D6 exposure file's automation type (6.3.3 T2 = H, 6.3.4 T3 = H, 6.8.5 T2 = Ac, where Pre-15A says A);
  - three mix Pre-15A tacit/career values with the D6 file's horizon (6.8.2 T1, 6.8.3 T2, 6.8.4 T2).
  No rule for this merge is documented.
- Completion check 4 ("no rows outside SA 6.3 and 6.8 modified") **fails** in the reconciled workbook. The same
  step rewrote the other 30 Domain 6 competencies from `domain6_task13_exposure_classification.xlsx`. Those rows
  match that file exactly on all 90 tasks, so the change is traceable, but it is a second, unlogged change.
- Pre-15A's "Prev" column claims all 30 tasks were A beforehand. That is untrue of both possible prior states: 9 of
  the 30 were not A in V3, and 12 were not A in the D6 exposure file. [E] The Pre-15A summary's "D6 distribution
  change" (A 64→52, Ac 0→12…) describes a third, pre-instrument stress-test state that is not in any surviving
  workbook. [J] Treat Pre-15A's before/after statistics as unreliable. Its per-task notes are still usable rationale.
- The project change log (CL-001…CL-014) has **no entry** for Pre-15A's completion or the D6 reconciliation, even
  though Pre-15A's own workbook contains a draft entry. [E: DE-009, DE-006]

### 1.4 Are Domain 7's tags complete?

**Mostly. Three defects.** [E: DE-001, DE-019]

- Complete for all 7: craft, primary and secondary stage, reform flags, stability tier, family assignments,
  and all 21 task exposure tuples (all H/Hi/–/none/N, matching the D7 tagging record 21/21).
- **Supporting Family Count is overstated in every D7 row,** by 2 (7.1.1, 7.1.2, 7.2.3) or 1 (the other four).
  [S] The D7 record suggests why: it notes "F15 is Supporting per database" for 7.2.3, yet the 7.2.3 F15 cell is
  blank. So family cells may have been lost after the counts were typed. An SME re-read of the D7 record would
  settle it.
- **Ethical lenses:** 7.1.1–7.1.4 are populated (20 cells). The 15 cells for 7.2.1–7.2.3 are blank, although the
  D7 record gives their values (7.2.1 and 7.2.3: L3=I, L5=I; 7.2.2: L5=I; rest A). Change log CL-008 already flags this.
- No per-task rationale table. The rationale is prose, one block per competency.

### 1.5 Are L1–L5 empty everywhere?

**Empty for 218 of 222 competencies (1,090 of 1,110 cells).** The only populated cells are the 20 for 7.1.1–7.1.4.
[E] The copyB Data Dictionary says classification of all 222 is "complete in session working records (Tasks 15
and 14)". But no Task 15 record exists in `legacy/v1/docs/`, and task sequence v7 lists Task 15 as PENDING
(DE-012). [J] Treat L1–L5 for Domains 1–6 as **not done**. The Data Dictionary statement is unverifiable.

### 1.6 Are the "modal" exposure fields consistent with the per-task values?

**No.**

| Dimension | Cells where stored "modal" differs from the T1–T3 majority |
|---|---|
| automation type | 63 of 222 |
| vector | 35 |
| horizon | 22 |
| tacit density | 3 |
| career ladder | 0 |
| **All dimensions** | **123 of 1,110 cells, in 79 competencies** |

[E: qa/modal_consistency.csv]

- **Domains 1, 6 and 7 use majority throughout** (87/87). Domains 2–5 do not: majority holds for 22/35, 12/35,
  20/35 and 18/30.
- **In all 63 automation-type mismatches the stored "modal" is the minority non-A type:**

  | T1–T3 pattern | Stored modal | Cases |
  |---|---|---|
  | A/A/Ac | Ac | 27 |
  | A/A/H | H | 20 |
  | A/A/V | V | 13 |
  | Ac/Ac/H | H | 2 |
  | Ac/Ac/V | V | 1 |

- No fixed priority order reproduces the stored values. The best one, V > S > H > Ac > A, explains 189/222.
- "Modal Contested" is undefined in v1. It is TRUE for 3 competencies whose automation types do have a majority
  (1.3.4, 1.4.4, 1.7.1: H/A/A).

[J] The modal fields were assigned by hand with a "most distinctive call" instinct in some sessions and a
majority rule in others. In v2 they should not be stored: compute them on read from the task values with one
published rule, or drop them.

---

## 2. What the normalized baseline contains

`data/v1_baseline/` (documented in its `README.md`):

- **Core tables:** `structure` (52), `competencies` (222), `tasks` (666), `proficiency` (888), `indicators` (4,852),
  `craft_stage_reform` (222), `family_assignments` (1,002), `ethical_lenses` (20), `exposure_summary` (222),
  `sector_applications` (1,110), `labor_market_crosswalk` (15), `workforce_signals` (102), `data_dictionary` (69).
- **Provenance tables:** `exposure_sources` (786 per-task classifications from 9 v1 working records and side
  workbooks), `normalization_log` (455), `version_diffs` (1,311), `vocabularies` (84).
- **Other:** `source_text/` (the parsed source and the reconciliation), `qa/`, and `v1_baseline.json` (everything nested).

Keys are provisional v1 provenance keys (`v1:1.1.1`, `v1:1.1.1:T2`, `v1:1.1.1:foundational:I3`…).
`BUILD_INFO.json` records the SHA-256 of all 13 inputs and every output. The build is deterministic; a test
re-runs it and compares byte for byte.

---

## 3. Completeness profile

Full per-column table: `qa/completeness.csv`. Material gaps [E: DE-001]:

| Field | Filled | Note |
|---|---|---|
| Description | 203 / 222 | the 19 blanks are **merged into the title** by the import (e.g. 3.1.1 "Project planning and scheduling Breaking down complex conservation work…"); `suggested_title`/`suggested_description` split them |
| Knowledge / Application | 768 / 888 levels | all 120 missing are Domain 5 (§6) |
| Indicators (valid) | 4,492 | 4,852 rows minus 360 mis-parsed D5 rows; see §9 for truncation |
| Craft Secondary | 168 / 222 | blank = "no secondary warranted" per Data Dictionary; not a gap |
| Stage Secondary 1 | 203 / 222 | 19 blank, undocumented whether intentional |
| Stage Primary 2 | **0 / 222** | 5 dual-primary exceptions documented (§5, C13) |
| Stage Secondary 2 | 0 / 222 | column never used |
| Dual Primary Exception | 0 TRUE / 222 | Data Dictionary and Task 10 record list 5 |
| L1–L5 lenses | 20 / 1,110 | §1.5 |
| T13 per-task dimensions | 666 / 666 tasks × 5 | complete |
| CLD Severity | 62 / 62 CLD-flagged | complete where applicable, but with undocumented values (§4) |
| Labor Market Crosswalk secondary SOC | 14 / 15 | F9 has none (intentional per note) |

---

## 4. Vocabulary validity

All coded values validate against `vocabularies.csv`. That table separates documented values (from the v1 Data
Dictionary) from values seen in the data but defined nowhere. The tests fail if a new undocumented value appears.
[E: DE-001]

- **Undocumented values in use:**
  - CLD Severity `Highest` (4) and `Ungraded` (4). Both come from the D6 reconciliation; the Data Dictionary
    allows High | Moderate | Low.
  - Two exposure-provenance labels, "D6 exposure file, reconciled March 2026" (30) and "D6 Ac retrospective, Task
    Pre-15A" (10). The dictionary lists Session-direct | Reconstructed (D2) | Reconstructed (D6).
- **Spelling drift:**
  - The 40 reconciled D6 rows write CLD Flag, S-Trajectory, CLD (modal) and Modal Contested as `Yes`/`No`; the
    other 182 rows use `TRUE`/`FALSE` or `Y`/`N`. That is 160 cells, normalized and logged.
  - The vector "none" value is an em dash (`—`).
  - Skill-area codes are stored as Excel floats (1.1). That would break at a tenth skill area (1.10 = 1.1). The
    extractor derives them from the competency code instead.
- **Columns with no Data Dictionary entry (11):** Stage Secondary 1/2, Core Family Count, Supporting Family Count,
  and the seven T13 "modal" fields (Auto Type, Tacit Density, Career Ladder, Vector, Horizon, CLD Flag, Modal
  Contested). None of the text columns (Description, Job Tasks, Knowledge/Application, sector notes) is defined
  either. [J] The undefined modal fields are the root of §1.6.

---

## 5. Internal consistency checks

From `qa/consistency_checks.csv`; each check is re-run by `scripts/audit_v1.py`. [E: DE-001; rule sources DE-001 Data Dictionary, DE-020]

| ID | Check | Violations |
|---|---|---|
| C01 | Reform Flag Count = number of TRUE reform flags | 0 / 222 |
| C02 | Core Family Count = Core assignments | 0 / 222 |
| C03 | Supporting Family Count = Supporting assignments | **7 / 222** (all Domain 7) |
| C04 | Zero Core = (Core count = 0) | 0 / 222 |
| C05 | Stability Tier follows the documented (Feb 2026) rule | 0 / 222 |
| C06 | stored modal = T1–T3 majority (auto / tacit / career / vector / horizon) | **63 / 3 / 0 / 35 / 22** |
| C07 | Modal Contested TRUE exactly when automation types have no majority | **3** |
| C08 | CLD Flag TRUE exactly when a P-position task is Ac/S/V | **11** |
| C09 | CLD Flag (modal) = CLD Flag | 0 |
| C10 | CLD Severity filled if and only if CLD Flag TRUE | 0 |
| C11 | H tasks, and only H tasks, have vector none and horizon N | **3** (4.4.2 T2, 4.6.1 T2, 4.7.2 T3 are H with AI/2) |
| C12 | S-trajectory TRUE only where an Ac task exists | **4** (2.3.2, 2.4.2, 5.4.4, 5.5.2) |
| C13 | 5 documented dual-primary exceptions present | **5 missing** |

**C08 in detail.** Eight competencies have a P-position Ac/V task but CLD = FALSE: 2.1.1, 2.1.2, 2.1.3, 2.1.5,
2.2.3, 2.6.2, 2.6.4 (all "Reconstructed (D2)") and 4.1.3. Three have CLD = TRUE with no P-position Ac/S/V task:
4.4.1, 4.4.5, 4.6.3.

The D2 cases matter. The D2 working record marks **2.1.1 T1 (CLD-Moderate) and 2.1.5 T2 (CLD-Low) as
confirmed in the session transcript ([C])**, but the database has CLD = FALSE for both. In 2.1.1 the Ac call has
moved from T1 to T3. [E: DE-015]

**C13 in detail.** The second primary stages are recoverable from `taxonomy_task10_working_record.md`
(Dual-Primary Exception Register):

| Competency | Stages |
|---|---|
| 1.5.5 | S1+S5 |
| 1.6.3 | S1+S5 |
| 2.1.1 | S1+S5 |
| 2.7.3 | S1+S5 |
| 4.3.2 | S4+S1 |

[E: DE-020]

---

## 6. Import fidelity: database vs source competency text

v1 ranks the source text as authoritative for competency content (DE-012). The source was parsed with
`scripts/v1_source_text.py`: 215/215 competencies, 645/645 tasks, 860/860 levels, 1,075/1,075 sector notes, 0
parse problems. The reconciliation is in `data/v1_baseline/source_text/`. [E: DE-011, DE-001]

| Content | Agreement | Defect |
|---|---|---|
| Task text (D1–D6) | **645 / 645 verbatim** | none |
| Sector notes | 1,075 / 1,075 | after removing artifacts: trailing `*` on 264 notes (the next line's bullet), and three source headings appended to Academia notes. One is a 7,278-character Domain 3 overview inside 2.7.5's Academia note. |
| Titles | 215 / 215 | 19 titles carry their description (the source puts both on one line for these) |
| Knowledge / Application | 740 / 860 | **all 120 Domain 5 levels missing** (the source formats D5 as `*Knowledge*:`; the import did not recognize it) |
| Indicators | 4,380 / 6,484 present | **2,104 missing (32.4%)**: import cap of 6 per level truncated 585 of 740 non-D5 levels; all 120 D5 levels lost every indicator |
| Domain 5 "indicators" | 0 / 360 valid | Indicator 1–3 hold `Knowledge*: …`, `Application*: …` and `Indicators*:` |
| Descriptions (D5) | 30 | trailing `#` (from `#Job Tasks:`) |

[E] Indicators per level in the source are 6.50 / 8.44 / 8.98 / 6.24 (Foundational→Expert; maxima 9 / 11 / 12 / 10;
215 competencies). The database means are 5.06 / 5.13 / 5.13 / 4.92 (222 competencies; D5 counts zero valid, D7 four).

[J] Consequences:
- Any v1 analysis that counted or read indicators, including Task 9's family tagging and Task 13's X-position
  adjudications, which read "Expert proficiency indicators" (DE-015), worked from a truncated and, for D5,
  corrupted record.
- v2 should take proficiency content from the source text, not the database.

[E] The source also contains content the database never captured:
- per-domain example position lists;
- career pathway tables with their own year bands ("Entry 0-3, Mid 3-7, Senior 7-15, Expert 15+"), which
  conflict with the proficiency bands "0-2 / 3-5 / 6-10 / 10+";
- representative job-role profiles with credentials and salary ranges.

These narrative sections cite skill areas under an older numbering. Examples: "1.6 (Climate Adaptation)", where
1.6 is now Biotechnology & Genetics; "1.9 (Sustainable Agriculture & Food Systems)"; "1.9.2: Advanced (soil
carbon)"; and "This domain encompasses nine skill areas" for a domain that has eight. [J] If v2 mines these
profiles (they are useful role-signal material for CM/FH), every code reference must be re-resolved by hand.

---

## 7. Exposure (Task 12/13/14) provenance

`exposure_sources.csv` puts every per-task classification found in v1 into one table, from 6 working records and
3 side workbooks:
- D1, D3, D5 Task 13 records;
- D4 Task 12 record;
- five D2 skill-area files (with [C]onfirmed / [R]econstructed / [I]nferred codes);
- D7 tagging record;
- D5 and D6 exposure workbooks;
- Pre-15A workbook.

Each row is compared with the baseline. [E: DE-006–DE-008, DE-014–DE-019; qa/exposure_source_alignment.csv]

| Record | Tasks | Values = baseline | Auto type = baseline | Text verbatim | Text similarity < 0.8 | Note |
|---|---|---|---|---|---|---|
| D1 record | 120 | 120 | 120 | 24 | **82** | not flagged as inferred anywhere |
| D2 records (5 files) | 105 | **37** | 77 | 48 | 29 | confidence: C 12, C★ 8, C-auto/R-other 15, R 48, I 22 |
| D3 record | 105 | 105 | 105 | 7 | **98** | 98 marked "[source-inferred]" |
| D4 record | 105 | 105 | 105 | 101 | 1 | |
| D5 record / D5 xlsx | 90 / 90 | 89 / 90 | 89 / 90 | 81 / 85 | 4 / 1 | |
| D6 xlsx | 120 | 102 | 114 | 120 | 0 | equal to baseline outside 6.3/6.8 |
| Pre-15A xlsx | 30 | 24 | 27 | 5 | 11 | abbreviated text |
| D7 record | 21 | 21 | 21 | 0 | 11 | abbreviated text |

Findings:

1. **D3 is worse than v1 thinks, and D1 has the same problem unreported.**
   - [E] The D3 record classified invented task statements for 98/105 tasks. Example 3.1.3 T2: record "Develop
     risk mitigation strategies and assign risk owners"; source/database "Create contingency plans and mitigation
     strategies for critical risks".
   - [E] The D1 record paraphrases 82 of 120. Example 1.1.5 T2: record "Analyze habitat data to identify limiting
     factors"; database "Evaluate habitat suitability using GIS-based landscape analysis".
   - Yet the database pairs those codes with the verbatim source text. [J] Pre-Task 15B (D3 verification) should
     be widened to D1. More fundamentally, v2 exposure must be re-derived against the v2 task text it will be shown
     with. Re-checking 187 tasks against new text costs about as much as reclassifying them under v2's method.
2. **D2's database values are a different reconstruction from the D2 working files.**
   - [E] Agreement is 37/105 on all five dimensions and 77/105 on automation type, including 7 of the 12 "[C]
     confirmed anchor call" rows (all 8 star-confirmed rows in SA 2.4–2.7 agree).
   - [E] The database labels all of D2 "Reconstructed (D2)", and two confirmed CLD signals are lost (§5).
   - [J] Neither source is the "true" Task 13 D2 state; the session transcript is not in the project. Both should
     go to v2 as low-confidence prior evidence, not as carried-forward tags.
3. **Rationale coverage is better than v1 says.**
   - [E] Every one of the 666 tasks has at least one classification record. All D1–D6 tasks (645) have a written
     per-task rationale. D7 has rationale as per-competency prose.
   - The "D6 exposure source document confirmed missing" gap (CL-012) is partly closed: the D6 workbook carries a
     rationale note for all 120 tasks. But it is a self-described *re-application* of the instrument, not the
     original stress-test record.
4. **Distribution claims in v1 documents are stale.**
   - [E] CL-007 / task13 synthesis report A 368, H 136, Ac 92, V 31, S 9 (636 tasks, a "9-task arithmetic residual").
   - The baseline's D1–D6 tasks give A 389, H 125, Ac 101, V 26, S 4 (645). With D7: H 146 (666).
   - Headline narrative claims such as "9 confirmed S calls, all D6" are therefore out of date: the baseline has 4.
   - [J] v2 documentation should generate every count from data (§13).

---

## 8. Proficiency statements: how much is generic or non-observable

### 8.1 Heuristic (documented in `scripts/audit_v1.py`)

Each Knowledge, Application and indicator statement is classified by its opening words (first match wins):

| Class | Opening words | Observable? |
|---|---|---|
| status_influence | shapes, transforms, leads transformative, advances, influences, is recognized / recognized as, provides strategic/expert leadership, sets direction, pioneers, champions | No: describes reputation or impact, not behaviour |
| cognitive_state | understands, knows, is aware, familiar, appreciates, has knowledge/understanding, comprehends, expert in, deep understanding, knowledgeable, recognizes the importance… | No: an internal state that can only be inferred |
| vague_action | applies, supports, assists, participates, contributes, helps, engages, works with, demonstrates, manages, leads, oversees, directs, provides, handles, follows, uses | Observable in principle, but without a specified product or standard |
| observable_action | anything else (conducts, collects, designs, calculates, maps, writes, presents…) | Yes, verb-led |

Non-observable = status_influence + cognitive_state. A second signal, **templated**, marks statements whose
wording, after the competency's own title words are masked, recurs in at least 5 different competencies.

[J] Limits:
- Lead-word rules are a screening tool; they over-penalize Foundational "Understands X" (sometimes the honest
  content of entry-level knowledge) and under-penalize "Conducts…" with no standard.
- The IO role should replace this with a behavioural-anchor review. It is good enough to rank where rewriting
  effort should go.

### 8.2 Results [E: qa/proficiency_genericity.csv, metrics.json → genericity]

**Opening word is fixed by level** (Knowledge statements, 192 per level, D1–D4, D6–D7):

| Level | Dominant first word | Share |
|---|---|---|
| Foundational | "Understands" | 88.5% |
| Intermediate | "Applies" | 94.3% |
| Advanced | "Expert in" | 98.4% |
| Expert | "Shapes" | 98.4% |

Application statements:

| Level | Most common first words |
|---|---|
| Foundational | supports 20.8%, uses 10.9% |
| Advanced | leads 53.6% |
| Expert | provides 49.5%, leads 21.4%, influences 16.1% |

**Non-observable share** (status_influence + cognitive_state):

| Level | Knowledge | Application | Indicators |
|---|---|---|---|
| Foundational | 92.7% | 0.0% | 14.1% |
| Intermediate | 2.1% | 0.0% | 1.1% |
| Advanced | 98.4% | 0.5% | 0.6% |
| Expert | **100%** | **55.2%** | **26.3%** |

- Overall: 670 of 1,536 Knowledge/Application statements (43.6%) are non-observable.
- Expert-level Knowledge/Application: 298 of 384 (77.6%) are status/influence claims ("Shapes…", "Transforms…",
  "Leads transformative…").
- By domain, non-observable Knowledge/Application runs from 39.3% (D3) to 49.1% (D6). Domain 5 cannot be scored
  in the database: its statements are missing (§6).
- **Expert indicators are the most templated content in v1** [E]. Templates and the number of competencies they
  recur in:
  - "Publishes influential ⟨X⟩ research": 43 competencies
  - "Develops innovative ⟨X⟩ approaches": 42
  - "Leads major ⟨X⟩ initiatives": 20
  - "Provides expert ⟨X⟩ consultation": 16
  - "Influences ⟨X⟩ standards": 12
  - Overall, 21.3% of Expert indicators are templated.
  - "Publishes influential research" appears verbatim in 11 competencies (1.6.5, 1.7.1–1.8.5).
  - 41 indicator texts are exact duplicates across competencies (93 rows; `qa/duplicate_indicators.csv`).

[J] What this means for v2:
- The Knowledge/Application pair carries almost no level-specific information beyond the level name. The
  indicators carry the assessable content, and a third of them were dropped by the import.
- Expert level as written measures standing (publishing, influencing, leading) rather than capability. That is a
  defensibility problem for hiring and promotion uses (IO's lane) and an equity problem for practitioners in roles
  that do not publish (Tribal, state, local, private field staff).
- Recommend:
  - rebuild proficiency from indicators upward;
  - drop the four fixed-verb Knowledge stems;
  - require every Expert indicator to name an observable work product or decision.

---

## 9. Indicators

| Level | Database valid (mean) | Levels at the 6-cap | Source total (mean, max) | Levels truncated |
|---|---|---|---|---|
| Foundational | 1,123 (5.06) | 170 | 1,397 (6.50, 9) | 175 |
| Intermediate | 1,138 (5.13) | 185 | 1,814 (8.44, 11) | 209 |
| Advanced | 1,138 (5.13) | 185 | 1,931 (8.98, 12) | 213 |
| Expert | 1,093 (4.92) | 144 | 1,342 (6.24, 10) | 108 |

[E: DE-001, DE-011]

- Indicator numbering has no gaps (888/888 levels).
- Domain 7 has exactly 4 indicators per level.
- **Tool names:** 43 indicators and 6 tasks name a specific tool or product.
  - In indicators: LiDAR 7, R 7, Python 6, SQL 3, Survey123 3, Fulcrum 3, Unity 3, MS Project 2, Smartsheet 2,
    Unreal 2, FARSITE 2, plus single mentions (ArcGIS, QGIS, TensorFlow, PyTorch, FVS, SWAT, Program MARK…).
  - In tasks: Python, R, Survey123, iNaturalist, Asana, Gantt, LiDAR, InVEST, ARIES.
  - Lexicon in `scripts/audit_v1.py`, so this is a lower bound.
  - [J] That is low for tasks and modest for indicators. The tool layer the brief asks for (durable competency vs fast-moving tool fluency) can be separated
  by extracting these mentions into a linked tool table rather than rewriting competencies.

---

## 10. Task statements

[E: qa/task_quality.csv]

- **Verb first:** 666 / 666 tasks start with an imperative verb (145 distinct verbs; most common: use 54,
  develop 47, conduct 28, evaluate 27, monitor 26).
- **Purpose or condition:** 468 of 666 (70.3%) carry a purpose or condition clause (to / for / using / based on /
  within / by…).
- **Outcome:** 361 of 666 (54.2%) carry an outcome clause (to / for / so that / ensuring / that).
- **Verb-object only:** 198 tasks (29.7%) have neither, e.g. "Design and implement biodiversity monitoring
  protocols" (1.1.2 T1) or "Diagnose biotic and abiotic stressors impacting tree health" (1.3.4 T2).
- **Compound verbs:** 54 tasks open with a compound verb ("Develop and maintain…", "Download, process, and
  interpret…"). These are two tasks in one, which complicates single-code exposure classification.
- **Length:** median 10 words (range 5–33).

[J] The tasks are workable raw material. Against O*NET-style task statements (action + object + purpose or
context), about 30% lack the purpose element and 8% are compound. The bigger structural issue is the fixed three
tasks per competency. It forces breadth into three slots, and the T1→T3 order is only weakly a career
progression: P-position falls from 89 (T1) to 41 (T3), but C-position dominates every slot and only 11 T3 tasks
are X-position. v2 should allow a variable number of tasks per competency.

---

## 11. Near-duplicate competencies and tasks

**Method.** TF-IDF (unigrams and bigrams, English stop words, sublinear tf) with cosine similarity, at three
granularities:
1. competency title + description;
2. task text;
3. a "rich" competency document: title + description + tasks + valid indicators.

**Threshold justification.** I read pairs in rank order. For the rich documents, every pair at or above 0.25 is a
plausible overlap an SME should adjudicate. Below about 0.23 the pairs become "related aspects within one skill
area" (e.g. 3.6.2 reporting vs 3.6.5 KPIs). Rich-document similarity is 0.091 at the 99th percentile and 0.209
at the 99.9th, so 0.25 selects about the top 0.07% of 24,531 pairs. [J]

**Results.** [E: qa/near_duplicate_*.csv]
- Lexical duplication is low:
  - title + description: maximum cosine 0.439, no pair ≥ 0.5;
  - tasks: maximum 0.60, 4 pairs ≥ 0.5, none ≥ 0.7.
- **Conceptual overlap is real and structured.** 16 rich-document pairs reach ≥ 0.25: 13 across skill areas and
  10 across domains. The pattern is the same subject split between a "knowledge" domain and the "field operations"
  domain, or between two finance skill areas:
  - drone operation: 2.3.2 vs 4.5.4 (0.44)
  - green bonds: 6.6.5 vs 6.8.2 (0.41)
  - water quality: 1.2.4 vs 4.1.3
  - prescribed fire: 4.2.3 vs 4.3.2
  - erosion: 1.2.5 vs 4.2.4
  - field data systems: 2.3.3 vs 4.1.5
  - carbon markets: 6.3.5 vs 6.8.3
  - climate vs adaptation finance: 6.8.1 vs 6.8.4
  - community-based participatory research: 5.6.5 vs 6.7.3
  - soil: 1.2.1 vs 4.1.4
  - conservation finance: 3.4.2 vs 6.6.4
  - wildlife survey: 1.4.2 vs 4.1.2
  - project-management software vs planning: 2.5.3 vs 3.1.1
- [J] TF-IDF misses paraphrase, so this is a lower bound. IA's semantic-matching work should re-run this with
  embeddings and SME review. The knowledge-vs-field-operations split is a v1 architecture choice (domains as
  knowledge types). The CA should decide whether v2 keeps both halves as separate competencies or as proficiency
  facets of one.

---

## 12. Distributions

[E: metrics.json → distributions]

**Craft primary:** SC 94, DC 79, FC 49. Craft is close to a proxy for domain:

| Domain | Craft primary |
|---|---|
| D2 | 100% DC (35/35) |
| D4 | 100% FC (35/35) |
| D1 | DC 26, FC 14 |
| D3 | SC 28, DC 7 |
| D5 | SC 28, DC 2 |
| D6 | SC 33, DC 7 |
| D7 | SC 5, DC 2 |

FC occurs only in D1 and D4. Craft secondary: DC 91, SC 49, FC 28, none 54.
[J] If v2 reorganizes around functions, crafts will become an independent signal for the first time. Any v1
"craft blend" finding is largely a domain finding.

**Workflow stage (primary):**

| S1 | S4 | S5 | S2 | S3 | S6 |
|---|---|---|---|---|---|
| 111 (50%) | 45 | 35 | 16 | 11 | 4 |

**Stability tier:** Transition 150, Stable 53, Emergent 19. The Feb 2026 rule moved 37 Stable to Transition.

**Families:**
- Core per family runs from F7 Data Science (40), F5 Conservation Science (30) and F8 Policy (30) down to 10
  (F4, F11, F12).
- Core assignments per competency: 0 for 43, 1 for 133, 2 for 34, 3 or more for 12.
- 43 Zero-Core; 30 flagged Foundational Professional Prep.

**Reform sensitivity:** 129 competencies (58.1%) carry at least one flag, 184 flag instances. That matches the
Data Dictionary's 122 / 174 for 215 plus D7's 7 / 10, so it is consistent, just never updated.

**Exposure, all 666 tasks:**

| Dimension | Values |
|---|---|
| Automation type | A 389, H 146, Ac 101, V 26, S 4 |
| Tacit density | Hi 277, Med 275, Lo 114 |
| Career ladder | C 467, P 184, X 15 |
| Vector | AI 516, none 143, Cv 6, Ro 1 |
| Horizon | 1: 394, 2: 129, N: 143 (no horizon 3 anywhere) |

CLD flagged in 62 competencies (severity Moderate 31, Low 16, High 7, Highest 4, Ungraded 4); S-trajectory in 15.

---

## 13. Stale summaries and documentation drift

- **Workforce Signals sheet:** still reports the 215-competency state ("across all 215 competencies"). 19 of its
  27 headline numbers differ from the baseline (e.g. Stable 90 vs 53, Transition 110 vs 150, SC 89 vs 94, F7 Core
  34 vs 40), and the exposure block covers D1 only. [E: qa/workforce_signals_vs_baseline.csv] It is kept in the
  baseline as a historical artifact. **Do not cite it.**
- **Change log:** ends at CL-014. It has no entries for Pre-15A, the D6 reconciliation, CLD Severity or the
  37-tier change. Its header still names v1u as authoritative. [E: DE-009]
- **Data Dictionary:** in copyB it asserts lens classification is complete in session records. No such records
  exist (§1.5).
- **Task sequence v7:** completion checks reference "col 70" and a "D3-verified" code, which no version contains.
  [E: DE-012]

[J] All of these are the same failure: hand-maintained summaries next to data. In v2 every summary count
(README status, dashboard, documentation) must be generated from the release data in CI, as LMPs does for its
README status block (DE-022).

---

## 14. Other things a steward should know before migrating

- **Labor Market Crosswalk SOC codes look wrong in several places.** [J, unverified this session: the BLS SOC
  page could not be fetched (DE-029); LM/FH should confirm against the SOC 2018 manual]
  - F10 "19-1012 Farm & Home Mgmt Educators": 19-1012 is Food Scientists and Technologists; Farm and Home
    Management Educators is 25-9021.
  - F12 "33-1021 Fire Inspectors": 33-1021 is First-Line Supervisors of Firefighting and Prevention Workers; Fire
    Inspectors and Investigators is 33-2021.
  - F11 secondary "25-4031 Library Technicians" and F13 primary "29-9021 Health Information Technologists" are
    valid codes but implausible mappings.
  - The crosswalk is family-level only; no competency links to SOC or O*NET.
- **Text artifacts:**
  - CRLF line endings in the source text.
  - Mojibake in `domain1/2/3_sections9_10.md` (legacy README, DE-021).
  - Skill-area names are upper case in Competencies but title case for D7 in Structure Summary.
  - All harmless. The extractor keeps the Competencies spelling and records the Structure Summary spelling
    alongside.
- **Duplicate project docs:** two docs named `domain4_5_6_sections9_10.md` and two named
  `taxonomy_task9_working_record.md`. Only the newer of each was captured. Any finding that rests on the older
  versions cannot be checked. [E: DE-021]
- **Single analyst, no inter-rater data.** No v1 tag (craft, stage, family, exposure, lens) has a second
  independent rating. The only redundancy is the same analyst re-classifying (D2, D6), and §7 shows those
  disagree substantially (D2: 37/105 identical). [J] That is the best available estimate of v1 tag reliability,
  and it argues for treating every v1 tag as a prior, not a fact.
- **`claude_session_persona.md`** contains operating instructions for v1 Claude sessions. It was read as data
  only and was not followed. It is withheld from the public repository (kept in git-ignored `legacy/v1/reference_only/`).

---

## 15. Migration implications (checklist for v2)

1. **Content:** rebuild competency text from `source_text/`, not the database.
   - Restore D5 Knowledge/Application and indicators, and the 2,104 truncated indicators.
   - Use the 19 suggested title/description splits.
2. **Tags:** carry every v1 tag forward as **v1 prior evidence with provenance** (`exposure_sources.csv`,
   `version_diffs.csv`), never as a v2 value.
   - Re-derive exposure against v2 task text.
   - D1, D2 and D3 exposure have known text or value misalignment.
3. **Derived fields:** do not store modal, count or flag fields that can be computed. Compute them in the build
   with one published rule.
4. **Recover lost values** from working records: the dual-primary second stages (Task 10 register) and the D7.2
   ethical lenses (D7 record).
5. **Retire** the Workforce Signals sheet and hand-written distribution statistics. Generate them.
6. **Fix or re-derive** the family→SOC crosswalk before anyone uses it. Move SOC/O*NET alignment to the
   competency level, as SSSOM-style mapping rows with confidence (see report).
7. **Keep `v1:` keys** as `derived_from` provenance on every v2 record (report §6).
