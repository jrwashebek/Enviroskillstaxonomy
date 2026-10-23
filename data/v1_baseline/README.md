# EMST v1 baseline (normalized)

A tidy, reproducible extract of the **v1 Environmental Management Skills Taxonomy database**, made so v2 can be
built from data rather than from spreadsheets. It is a **provenance baseline**: values are v1's own, including
its mistakes, with known defects flagged and not fixed. Where v1 is wrong, use the `qa_flags` and `source_text/`
tables to see what it should have said. For the findings, see [`docs/audit/data-audit.md`](../../docs/audit/data-audit.md).

- **Baseline workbook:** `legacy/v1/data/20260223_SkillsTaxonomy_Core_V3_reconciled__copyB_aaf34c8c.xlsx`
  (why this one: audit §1). Hashes of every input are in `BUILD_INFO.json`.
- **Regenerate:** `python scripts/extract_v1.py` (needs `openpyxl`); `python scripts/diff_v1_versions.py`;
  `python scripts/audit_v1.py` (needs `scikit-learn`). Check: `python scripts/extract_v1.py --check`;
  `python -m pytest -q tests/test_v1_baseline.py`.
- **Do not edit by hand.** The tests compare each output with the SHA-256 in `BUILD_INFO.json`.
- **Keys are v1 provenance keys, not v2 IDs:** `v1:1.1.1` competency, `v1:1.1` skill area, `v1:1` domain,
  `v1:1.1.1:T2` task, `v1:1.1.1:foundational` proficiency level, `v1:1.1.1:foundational:I3` indicator,
  `v1:1.1.1:F5` family assignment, `v1:1.1.1:L2` ethical lens, `v1:1.1.1:sector:ngos` sector note.

## Tables

| File | Rows | One row per | Notes |
|---|---|---|---|
| `structure.csv` | 52 | domain (7) or skill area (45) | checked against the Structure Summary sheet |
| `competencies.csv` | 222 | competency | title and description, plus `suggested_title`/`suggested_description` where v1 merged them (19); `qa_flags` |
| `tasks.csv` | 666 | job task (222 × 3) | text plus the five Task 13 exposure dimensions and their provenance |
| `proficiency.csv` | 888 | competency × level (4) | Knowledge, Application, indicator counts, `qa_flags` |
| `indicators.csv` | 4,852 | indicator | `qa_flag` marks the 360 Domain 5 rows that are mis-parsed K/A lines, not indicators |
| `craft_stage_reform.csv` | 222 | competency | craft, workflow stage, six reform flags, stability tier, family counts |
| `family_assignments.csv` | 1,002 | competency × family with a value | Core / Supporting (blank cells omitted) |
| `ethical_lenses.csv` | 20 | competency × lens with a value | only 7.1.1–7.1.4 are populated in v1 |
| `exposure_summary.csv` | 222 | competency | CLD, S-trajectory, the stored "modal" fields, provenance |
| `exposure_sources.csv` | 786 | task × working record | every per-task classification found in v1 working records and side workbooks, with rationale, confidence codes and agreement with the baseline |
| `sector_applications.csv` | 1,110 | competency × sector (5) | |
| `labor_market_crosswalk.csv` | 15 | profession family | family → SOC (2018 assumed; see audit §14 for suspect codes) |
| `workforce_signals.csv` | 102 | dashboard cell | the v1 dashboard sheet in long form; **stale** (215-competency state) |
| `data_dictionary.csv` | 69 | dictionary entry | the v1 Data Dictionary sheet |
| `vocabularies.csv` | 84 | code | controlled vocabularies used for validation; `status` = documented / observed_undocumented |
| `normalization_log.csv` | 455 | changed cell | every per-cell change the extractor made (marker stripping, residue removal, Yes/No booleans) |
| `version_diffs.csv`, `version_summary.csv` | 1,311 / 101 | difference | cell-level diff of the five v1 database workbooks (`scripts/diff_v1_versions.py`) |
| `source_text/*.csv` | | | the source competency text (`legacy/v1/docs/20251202_SkillsTaxonomy_Core_V2 (1).txt`) parsed and compared with the database: 6,484 source indicators (2,104 not in the database), Domain 5 Knowledge/Application, task and sector text checks |
| `qa/*.csv`, `qa/metrics.json` | | | audit outputs (`scripts/audit_v1.py`) |
| `v1_baseline.json` | | | all of the above, nested one object per competency |

## Global value maps (applied silently, listed here)

- Booleans `TRUE/FALSE`, `True/False`, `Y/N`, `Yes/No` → `true`/`false`. (`Yes`/`No` occurs only in the 40
  reconciled Domain 6 rows and is logged per cell.)
- Vector em dash `—` → `none`.
- Craft secondary `DC-sec` → `DC`. The column name carries the role.
- Skill-area code is taken from the competency code (`1.1`), never from the Excel float.
- Exposure provenance labels → snake_case codes; the raw label is kept in `exposure_provenance_raw`.
- Whitespace trimmed and collapsed.

Per-cell changes go to `normalization_log.csv`. They are: trailing `*` (264 sector notes) and `#` (30 Domain 5
descriptions). Both are import artifacts: the next line's bullet or the `#Job Tasks:` heading bled into the cell.
They are moved to `source_marker` columns. Two source-document headings that bled into Academia notes (2.7.5,
6.4.5, plus 6.8.5) are removed, and the raw value is kept in the log.

## Licence

Proposed: CC0-1.0 for this derived data, matching the LMPs split (see
`docs/research/data-engineering/report.md`). v1 content is the project lead's own work. Confirm before release.
