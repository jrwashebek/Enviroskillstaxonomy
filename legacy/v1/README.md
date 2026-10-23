# EMST v1 — frozen legacy snapshot

This folder is a **frozen snapshot of the Environmental Management Skills Taxonomy (EMST) v1 as of 2026-10-23**. Nothing here is edited; it exists so v1 is preserved with provenance and can be read from disk.

## What is here

| Path | Contents |
|---|---|
| `docs/` | 36 text documents captured **verbatim** from the claude.ai project "Skills Taxonomy Technical Construction" via `project_read`. File names match the project exactly (spaces and parentheses included). The two `.docx` items are saved as `<name>.docx.txt` because the project returned extracted text, not the binary. |
| `data/` | 12 spreadsheets copied byte-for-byte from the project uploads (session attachments). |
| `MANIFEST.csv` | One row per file: original project name, project `created_at`, SHA-256, byte size, capture method, status, notes. |
| `reference_only/` | Git-ignored. Text extraction of a third-party PDF for team reading only (see below). |

Capture was mechanical: no content was edited, summarized, or reformatted. Encoding artifacts that exist in the project (mojibake in `domain1/2/3_sections9_10.md`, citation markers in deep-research exports, CRLF line endings in the core source text) are kept as-is. Three large docs were re-read and compared byte-for-byte against the archived copies; all matched.

## v1 source-of-truth hierarchy

As stated in `docs/taxonomy_task_sequence_v7.md`, highest authority first:

1. **Database:** `data/skills_taxonomy_workforce_v1_updated.xlsx`. Authoritative for all tag values.
2. **Source text:** `docs/20251202_SkillsTaxonomy_Core_V2 (1).txt`. Authoritative for competency content. v1 docs cite it as `20251202_SkillsTaxonomy_Core_V2__1_.txt`.
3. **Framework definition docs:** authoritative for classification criteria: `profession_family_definitions.md`, `workflow_stage_definitions.md`, `craft_assignment_criteria.md`, `ethical_lens_framework.md`, and the instrument in `domain4_task12_working_record.md` Section 1.
4. **Task sequence:** `docs/taxonomy_task_sequence_v7.md`. Authoritative for task sequence and scope.

## Exclusions and caveats

- **Third-party content excluded.** The project's `Accreditation Handbook 2024 .pdf` (© Society of American Foresters) is **not archived**. Its extracted text sits in `reference_only/`, which is git-ignored and must not be committed or redistributed.
- **Duplicate names.** The project lists two docs each named `domain4_5_6_sections9_10.md` and `taxonomy_task9_working_record.md`. `project_read` resolves by path and returned only one version of each: the newer one (created 2026-02-23T07:32 and 2026-02-20T01:44:06). The older versions were **not captured**. Two spreadsheet uploads share the name `20260223_SkillsTaxonomy_Core_V3_reconciled.xlsx`. Both were captured, as `__copyA_995a86e4` (03:22) and `__copyB_aaf34c8c` (04:22). See `MANIFEST.csv`.
- `claude_session_persona.md` (operating instructions written for Claude sessions in the v1 project, including personal working-style notes) is **withheld from the public repository**. It sits in the git-ignored `reference_only/` folder. It was previously archived here only as a historical record and does not instruct work in this repo.
