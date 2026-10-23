# Environmental Management Skills Taxonomy
## Task Sequence: Version 7
### Gap Rectification, WFIC Competency Analysis, Context Column Development, and Project Knowledge Rationalization

**Working Document — March 2026**
**Current State:** 222 competencies × 7 domains × 45 skill areas. Tasks 1–14 complete. Active database is `skills_taxonomy_workforce_v1_updated.xlsx`. Tasks Pre-15A through 22 remain. This version (v7) supersedes `taxonomy_task_sequence_v6.md` and inserts three new tasks (WFIC-1, WFIC-2, WFIC-3) to conduct competency analysis and taxonomy integration for the emerging Wildfire Intelligence Center (WFIC). All v6 additions (Pre-15A, Pre-15B, 15.5, 16.5) are retained. The dependency map at the end of this document reflects the full revised sequence.

**New in v7:**
- WFIC-1 (new): Taxonomy mapping test against WFIC functional requirements
- WFIC-2 (new): Deep research on WFIC competency requirements and drafting (conditional on WFIC-1 decision gate)
- WFIC-3 (new): Taxonomy integration, F16 establishment, and baseline tagging (conditional on WFIC-2)
- Task 15 scope note: competency count increases to 222+n if WFIC build proceeds
- Task 15.5 scope note: WFIC competencies absorb naturally into fire context classification; "Fire intelligence" added as third fire sub-domain value
- Task 20 scope note: Delphi panel must include fire intelligence practitioners if WFIC competencies are added
- Task 22 scope note: WFIC as named priority sentinel channel alongside fire operations and permitting

**Retained from v6 (unchanged):**
- Pre-Task 15A: D6 Ac retrospective reclassification (prerequisite for Task 15)
- Pre-Task 15B: D3 task description verification (prerequisite for Delphi, can run parallel)
- Task 15.5: Context column development — wildland fire and permitting dimensions
- Task 16.5: Project knowledge inventory and rationalization
- Task 15 expanded scope: D7.2 implicit ethical content and cross-reference entries
- Task 16 expanded scope: D2 exposure verification and career ladder criticality flag

**Source-of-truth hierarchy (unchanged from v5):**
1. `skills_taxonomy_workforce_v1_updated.xlsx` — database is authoritative for all tag values
2. `20251202_SkillsTaxonomy_Core_V2__1_.txt` — source text is authoritative for competency content
3. Framework definition documents — authoritative for classification criteria
4. This document — authoritative for task sequence and scope

---

## How to Use This Document

At the start of every session, read this document to confirm the current task, its prerequisites, and its expected outputs. Do not proceed without confirming prerequisites are met.

**Session opening convention:**
*"I'm continuing work on the taxonomy. The primary database is `skills_taxonomy_workforce_v1_updated.xlsx`. The task sequence is `taxonomy_task_sequence_v7.md`. I'm on Task [X]."*

---

## Pre-Task 15A: D6 Ac Retrospective Reclassification

**Status: PENDING — must complete before Task 15 and WFIC-1**
**Prerequisites:** Task 13 complete ✓
**Estimated scope:** 10–20 tasks in skill areas 6.3 and 6.8

> **SESSION PROTOCOL: START A NEW CHAT**
> This is a focused reclassification task with bounded scope (SA 6.3 and 6.8 only). Starting fresh eliminates context contamination from prior sessions and ensures the Ac criterion is read directly from `domain4_task12_working_record.md` Section 1.2 rather than reconstructed from memory. The task should complete within a single session.
>
> **Opening message for new chat:**
> *"I'm continuing work on the Environmental Management Skills Taxonomy. Active database: `skills_taxonomy_workforce_v1_updated.xlsx`. Task sequence: `taxonomy_task_sequence_v7.md`. I'm on Pre-Task 15A: D6 Ac Retrospective Reclassification. Please read the task sequence and `domain4_task12_working_record.md` Section 1.2 before we begin."*

> **COMPLETION CHECK — verifiable in a separate chat:**
> Load `skills_taxonomy_workforce_v1_updated.xlsx` Dimension Tags sheet. Filter to Domain 6 (codes 6.x.x), skill areas 6.3 and 6.8.
> 1. Col 70 (provenance): all reviewed rows show "D6 Ac retrospective, Task Pre-15A" — not "Reconstructed (D6)"
> 2. Automation Type column: at least some rows in SA 6.3 and 6.8 show Ac (not all A); if every row remained A, the reclassification criterion was not applied
> 3. A written list of newly identified CLD signals exists in the session record or as a standalone document
> 4. No rows outside SA 6.3 and 6.8 have been modified (scope containment check)
> **Task is complete when all four checks pass.**

**Background:** During Task 12 instrument development, a flag was placed on Domain 6 documentation-heavy tasks: competencies in 6.3 (Resource Economics) and 6.8 (Climate Finance & Investment) where practitioners primarily produce regulatory and policy documentation were classified A (Augmentation) but may meet the Ac (Compressive Augmentation) criterion — AI tools substantially reduce time and cognitive investment such that headcount compression is plausible even without full substitution, with the human role shifting to review-and-certify rather than primary execution.

**Work:**
Review all D6 tasks in skill areas 6.3 and 6.8 against the Ac criterion from `domain4_task12_working_record.md` Section 1.2. Apply the headcount-compression test: would AI-assisted document production in this task plausibly reduce FTEs even though full substitution hasn't occurred? Reclassify A→Ac where criterion is met. Document each reclassification decision with a provenance note in col 70 ("D6 Ac retrospective, Task Pre-15A").

**Reclassification must precede Task 15** because any reclassified competency carrying a P-position Ac call becomes a new CLD signal, which affects both the stability tier cross-validation (Task 16) and the ethical lens analysis (Task 15) — specifically L5 (Professional Integrity) considerations where AI-compressed documentation work raises questions about practitioner independence from automated outputs.

**Output:** Revised D6 automation type values in Dimension Tags sheet; updated provenance flags in col 70; list of newly identified CLD signals from D6 reclassification

---

## Pre-Task 15B: D3 Task Description Verification

**Status: PENDING — must complete before Delphi instrument finalization (can run parallel to Pre-15A and WFIC tasks)**
**Prerequisites:** Task 13 complete ✓
**Estimated scope:** ~76% of Domain 3 task descriptions (~80 tasks)

> **SESSION PROTOCOL: START A NEW CHAT**
> This task requires repeated close reading of the source taxonomy text (`20251202_SkillsTaxonomy_Core_V2__1_.txt`) against database entries. Starting fresh keeps the context window clean for source text comparisons and prevents interference from prior analytical sessions. The task is text-verification work, not classification, and should complete within one session.
>
> **Opening message for new chat:**
> *"I'm continuing work on the Environmental Management Skills Taxonomy. Active database: `skills_taxonomy_workforce_v1_updated.xlsx`. Task sequence: `taxonomy_task_sequence_v7.md`. I'm on Pre-Task 15B: D3 Task Description Verification. Please read the task sequence before we begin."*

> **COMPLETION CHECK — verifiable in a separate chat:**
> Load `skills_taxonomy_workforce_v1_updated.xlsx` Competencies sheet. Filter to Domain 3 (codes 3.x.x).
> 1. Col 70 (provenance): all D3 rows show "D3-verified" — no rows remain flagged "source-inferred"
> 2. A Substantive discrepancy list exists as a documented output, even if empty
> 3. Any Substantive discrepancies show revised task descriptions AND revised exposure classifications in the Dimension Tags sheet
> **Task is complete when all three checks pass.**

**Background:** Approximately 76% of Domain 3 task descriptions were inferred from competency names and context during Task 13 rather than transcribed verbatim from `20251202_SkillsTaxonomy_Core_V2__1_.txt`. If any source task framing differs materially from the inferred description, the exposure classification may require revision. This verification must precede Delphi instrument finalization because Delphi reviewers will assess classifications against source task descriptions.

**Work:**
For each D3 competency, open `20251202_SkillsTaxonomy_Core_V2__1_.txt` and confirm whether the three task descriptions in the database match the source text. Flag discrepancies using a two-level system: Minor (framing difference only, classification unaffected) and Substantive (task scope materially different, classification requires review). Revise task descriptions and classifications where Substantive discrepancies are found. Add provenance code "D3-verified" in col 70 for each confirmed row.

**Output:** Verified D3 task descriptions in Competencies sheet; list of Substantive discrepancies with revised classifications; col 70 provenance update

---

## WFIC-1: Taxonomy Mapping Test Against Wildfire Intelligence Center Requirements

**Status: PENDING**
**Prerequisites:** Pre-Task 15A complete
**Estimated scope:** 1–2 sessions

> **SESSION PROTOCOL: START A NEW CHAT**
> This is an analytical exercise requiring both taxonomy database familiarity and external policy research. A fresh chat ensures the analysis is conducted against the current database state (post-gap-rectification) and draws WFIC functional requirements from primary sources rather than prior conversation summaries.
>
> **Opening message:**
> *"I'm continuing work on the Environmental Management Skills Taxonomy. Active database: `skills_taxonomy_workforce_v1_updated.xlsx`. Task sequence: `taxonomy_task_sequence_v7.md`. I'm on WFIC-1: Taxonomy Mapping Test against Wildfire Intelligence Center requirements. Please read the task sequence, `Wildland_Fire_Workforce_Skills_and_Near-Term_Technology_Disruptions.md`, and `profession_family_definitions.md` (F12 entry) before we begin."*

> **COMPLETION CHECK:**
> 1. A WFIC functional requirements inventory exists, organized by functional area, with source citations for each requirement
> 2. A coverage matrix exists mapping each WFIC functional requirement to existing taxonomy competencies with ratings: Full Coverage, Partial Coverage, No Coverage
> 3. A gap assessment document exists identifying: (a) functional areas with No Coverage, (b) functional areas with Partial Coverage and a description of what is missing, (c) an estimated count of new competencies needed
> 4. A decision recommendation exists: proceed to WFIC-2/3 (significant gaps), adjust Task 15.5 scope only (minor gaps), or no action needed (full coverage)
> **Task is complete when all four outputs exist as a single WFIC mapping document.**

**Background:** Executive Order 14308 (June 2025) directed the consolidation of wildland fire prediction and research entities into a national Fire Intelligence Center. The WFIC would serve as a joint USDA/DOI/Commerce hub for wildfire intelligence, prediction, coordination, and response, modeled on the National Weather Service. The establishment of the U.S. Wildland Fire Service (January 2026) and subsequent USDA/DOI secretarial orders initiated implementation. The WFIC's workforce competency requirements have not been systematically mapped.

The EMST provides an outside-in competency analysis to inform WFIC workforce design — identifying what professional competencies the intelligence function requires, which are already captured in existing environmental management professional standards, and where gaps exist. The intended audience is those actively designing the WFIC's workforce; the analysis is outside-in with room for refinement based on institutional context in subsequent engagements.

**Work — Part A: Infer WFIC functional requirements**

Construct a functional requirements inventory for the WFIC organized by operational area. Sources:
1. **Institutional mandate documents:** EO 14308; USDA and DOI secretarial orders; USWFS establishment documentation
2. **Existing capability standards:** NWCG PMS 310-1; NIFC Predictive Services program documentation; DOI Wildland Fire Dispatch Competency Model
3. **Institutional analog:** National Weather Service organizational structure and workforce composition as the named model for WFIC design
4. **Technology and systems documentation:** USFS Enterprise Geospatial Portal (EGP) modernization; Wildland Fire Assessment System (WFAS); BlueSky smoke modeling; emerging AI/ML fire detection and behavior prediction tools; OGC Generative AI in Wildland Fire Engineering Report
5. **Project knowledge:** `Wildland_Fire_Workforce_Skills_and_Near-Term_Technology_Disruptions.md`; `deep-research-report__8_.md`

Expected functional areas (provisional — refine from source analysis):
- Fire weather prediction and forecasting
- Fire behavior modeling and prediction
- Remote sensing and geospatial fire intelligence
- AI/ML model development, deployment, and validation for fire applications
- Multi-source data fusion and intelligence synthesis
- Decision-support system operation and maintenance
- Interagency coordination and intelligence dissemination
- Technology transition and integration (pilot-to-operational pathway management)
- Data governance, quality assurance, and archival
- Post-fire damage assessment and recovery intelligence

**Work — Part B: Map existing taxonomy competencies to WFIC requirements**

For each WFIC functional area, query the existing 222 competencies across all domains. Produce a coverage matrix:
- **Full Coverage:** An existing competency addresses this functional requirement at adequate specificity.
- **Partial Coverage:** An existing competency addresses an aspect of this requirement but misses critical WFIC-specific dimensions.
- **No Coverage:** No existing competency addresses this functional requirement.

Cross-domain draws are expected from D1 (fire ecology/behavior science), D2 (geospatial, data science, AI/ML), D3 (program management, interagency coordination), D4 (fire operations), D5 (communication, stakeholder engagement), and D6 (policy coordination).

**Work — Part C: Gap assessment and decision recommendation**

Synthesize Part B into a structured gap assessment. Decision gate criteria:
- **Proceed to WFIC-2/3** if: 3+ functional areas have No Coverage, OR the gaps represent professional work that cannot be adequately described by combining existing competencies
- **Adjust Task 15.5 scope only** if: gaps are minor and addressable through expanded fire_context classification and Delphi notes
- **No action** if: existing competencies provide Full or adequate Partial Coverage for all WFIC functional areas

**Output:** WFIC competency mapping document with functional requirements inventory, coverage matrix, gap assessment, and decision recommendation

---

## WFIC-2: WFIC Competency Research and Drafting

**Status: CONDITIONAL — proceeds only if WFIC-1 decision gate recommends**
**Prerequisites:** WFIC-1 complete with "proceed" recommendation
**Estimated scope:** 2–3 sessions

> **SESSION PROTOCOL: START A NEW CHAT for each session**
> Session WFIC-2A focuses on research synthesis and competency architecture. Session WFIC-2B+ focuses on drafting competency descriptions.
>
> **Opening message for Session WFIC-2A (architecture):**
> *"I'm continuing work on the Environmental Management Skills Taxonomy. Task sequence: `taxonomy_task_sequence_v7.md`. I'm on WFIC-2: WFIC Competency Research and Drafting, architecture session. Please read the task sequence, the WFIC-1 mapping document, and `20251202_SkillsTaxonomy_Core_V2__1_.txt` (for competency description conventions) before we begin."*
>
> **Opening message for Session WFIC-2B (drafting):**
> *"I'm continuing work on the Environmental Management Skills Taxonomy. Task sequence: `taxonomy_task_sequence_v7.md`. I'm on WFIC-2: WFIC Competency Drafting. Please read the task sequence and the WFIC-2A architecture decisions before we begin."*

> **COMPLETION CHECK:**
> 1. Draft competency descriptions exist for all identified gap areas, following taxonomy conventions: competency name, three job tasks per competency, four proficiency levels with assessment indicators, sector-specific applications
> 2. Each new competency has a proposed domain assignment and skill area assignment with rationale
> 3. A draft F16 (Wildland Fire Intelligence & Decision Support) profession family definition exists, following the format in `profession_family_definitions.md`
> 4. A WFIC competency architecture document exists recording: total new competency count, domain distribution, relationship to existing competencies, and boundary decisions
> 5. All draft competencies have been reviewed by the user before proceeding to WFIC-3
> **Task is complete when all five checks pass.**

**Work — Part A: Research synthesis and competency architecture**

Using the gap assessment from WFIC-1, conduct targeted research. Sources include NWS workforce structure and position descriptions, NIFC Predictive Services documentation, USFS FAM position descriptions, OGC Wildland Fire AI Engineering Report, DOI Wildland Fire Dispatch Competency Model, and academic literature on fire intelligence and predictive analytics in emergency management.

Determine:
1. **Domain assignment:** Do WFIC competencies constitute a new skill area within an existing domain, or require assignment across multiple domains? Follow the taxonomy's domain logic: domains reflect knowledge traditions, not institutional homes.
2. **Skill area structure:** Group new competencies into skill areas (typically 3–7 competencies per skill area).
3. **Relationship to existing competencies:** Document prerequisites, adjacencies, and overlaps.

**Work — Part B: Draft competency descriptions**

Draft each new competency following the conventions in `20251202_SkillsTaxonomy_Core_V2__1_.txt`:
- Competency name (active-verb phrase)
- Brief description (one sentence)
- Job Tasks (3): T1 = foundational execution, T2 = intermediate application/analysis, T3 = advanced synthesis/leadership
- Proficiency Levels (4): Foundational (0–2 years), Intermediate (3–5 years), Advanced (6–10 years), Expert (10+ years) with Knowledge, Application, and Assessment Indicators
- Sector-Specific Applications: Public Agencies, Private Sector, NGOs, Consulting, Academia

**Work — Part C: Draft F16 profession family definition**

Following `profession_family_definitions.md` format: Definition, Boundary criteria, Representative roles, Domain span, Overlap notes.

**Critical design principle:** Define F16 around the *function* (wildland fire intelligence and decision support) rather than the *institution* (the WFIC). The intelligence function is durable regardless of institutional reorganization.

**Output:** Draft competency descriptions; draft F16 definition; WFIC competency architecture document

---

## WFIC-3: Taxonomy Integration and Baseline Tagging

**Status: CONDITIONAL — proceeds only if WFIC-2 complete**
**Prerequisites:** WFIC-2 complete with user-reviewed competency descriptions
**Estimated scope:** 1–2 sessions

> **SESSION PROTOCOL: START A NEW CHAT**
>
> **Opening message:**
> *"I'm continuing work on the Environmental Management Skills Taxonomy. Active database: `skills_taxonomy_workforce_v1_updated.xlsx`. Task sequence: `taxonomy_task_sequence_v7.md`. I'm on WFIC-3: Taxonomy Integration. Please read the task sequence, the WFIC-2 outputs, and the framework definition documents before we begin."*

> **COMPLETION CHECK:**
> 1. Competencies sheet: new WFIC competencies present with complete descriptions, correct D.SA.N codes, and provenance "WFIC-3" in col 70
> 2. Dimension Tags sheet: new rows with profession family tags (Core/Supporting) for F16 and all applicable families
> 3. Dimension Tags sheet: new rows with workflow stage tags
> 4. Dimension Tags sheet: new rows with craft assignments (FC/SC/DC)
> 5. `profession_family_definitions.md` updated with F16 definition
> 6. F12 (Fire Management) overlap notes updated to reference F16 boundary
> 7. Competency count in this task sequence document updated from 222 to final count
> 8. Data Dictionary updated with any new codes or column modifications
> **Task is complete when all eight checks pass.**

**Work — Part A: Database integration**

Add reviewed competencies to the Competencies sheet with D.SA.N codes and "WFIC-3" provenance.

**Work — Part B: Baseline tagging (Tasks 9, 10, 11 equivalent)**

1. Profession family tagging per `profession_family_definitions.md`
2. Workflow stage tagging per `workflow_stage_definitions.md` (apply reform sensitivity flags where applicable)
3. Craft assignment per `craft_assignment_criteria.md` (expected: predominantly DC with some SC)

**Note:** Exposure classification, ethical lens, fire/permitting context, and stability tier assignments are NOT performed here — new competencies are processed alongside all others during Tasks 15, 15.5, and 16.

**Work — Part C: Update framework documents**

1. Add F16 to `profession_family_definitions.md`
2. Update F12 overlap notes
3. Update this task sequence: revise competency count throughout
4. Update Data Dictionary

**Output:** Integrated database with 222+n competencies; updated framework documents; updated task sequence

---

## Task 15: Ethical Lens Population

**Status: PENDING**
**Prerequisites:** Pre-Task 15A complete; WFIC-3 complete (or WFIC-1 decision gate indicates no new competencies needed); stable competency list
**Primary reference:** `ethical_lens_framework.md`

Session protocols, completion checks, and work specifications are as specified in v6, with the following v7 modifications:

**v7 scope adjustments:**
- Competency count is 222+n if WFIC build proceeded
- WFIC competencies assigned to existing domains are processed in their domain session
- High-priority ethical integration sites now include: WFIC competencies for L3 implications (AI-driven fire prediction affecting community safety) and L5 implications (automated intelligence products displacing professional judgment)
- For WFIC competencies, use the WFIC-2 draft descriptions as source text for E/I/A classification

All other v6 specifications (L2/L3 transposition warning, R10 rule, Parts A–E, completion checks) remain unchanged.

---

## Task 15.5: Context Column Development — Wildland Fire and Permitting

**Status: PENDING — retained from v6**
**Prerequisites:** Task 15 complete; Pre-Task 15A complete

Work, session protocols, and completion checks are as specified in v6.

**v7 addendum:** Add "Fire intelligence" as a third fire sub-domain value in `fire_context_note` alongside "Suppression" and "Prescribed fire." This segmentation captures the distinct disruption dynamics facing the intelligence workforce. Flag the three-way segmentation for Delphi review. All WFIC-specific competencies are expected to classify as Primary fire context with "Fire intelligence" sub-domain note.

---

## Task 16: Stability Tier Validation and Labor Market Layer Enrichment

**Status: PENDING — retained from v6, unchanged**

Work, session protocols, and completion checks are as specified in v6.

**v7 scope note:** WFIC competencies (if added) require stability tier assignments. Expected: Emergent or Transition tiers. Career_ladder_criticality flag unlikely to apply.

---

## Task 16.5: Project Knowledge Inventory and Rationalization

**Status: PENDING — retained from v6, scope expanded**

Work, session protocols, and completion checks are as specified in v6.

**v7 scope expansion:** Inventory must also address WFIC-1 mapping document, WFIC-2 architecture document, F16 integration status, `Wildland_Fire_Workforce_Skills_and_Near-Term_Technology_Disruptions.md` retention, and any documents produced during WFIC research.

---

## Tasks 17–22: Retained From v6 (v7 Scope Notes Added)

Session protocols, completion checks, and work specifications are as specified in v6.

**v7 scope notes:**

**Task 17 (GitBook Architecture):** Navigation must accommodate WFIC competencies. F16 appears in profession family index page.

**Task 18 (Python Export Script):** Script handles any new competencies and F16 family without structural changes if WFIC competencies follow standard conventions.

**Task 20 (Delphi Preparation):** Panel must include fire intelligence practitioners (NIFC Predictive Services, USFS geospatial fire analysts, fire weather meteorologists) if WFIC competencies are in the taxonomy.

**Task 22 (Sentinel Network Design):** WFIC itself becomes a named priority sentinel channel. Nodes: NIFC Predictive Services, USFS FAM intelligence staff, NOAA fire weather services, state fire intelligence programs (CA Office of Wildfire Technology R&D, CO Center of Excellence), tribal fire programs with intelligence capacity. `fire_context_note` "Fire intelligence" value serves as competency scope selector for WFIC-specific signal coding.

---

## Revised Dependency Map

```
Tasks 1–14 [COMPLETE]
    │
    ├── Pre-Task 15A: D6 Ac retrospective reclassification [PENDING]
    │       ⚠️ Must complete before Task 15 and WFIC-1
    │       ⚠️ Must complete before Task 16
    │
    ├── Pre-Task 15B: D3 task description verification [PENDING]
    │       Can run parallel to Pre-15A and WFIC tasks
    │       Must complete before Delphi instrument finalization
    │
    ▼
WFIC-1: Taxonomy mapping test against WFIC requirements [PENDING]
    │   Prerequisites: Pre-Task 15A complete
    │   Output: coverage matrix, gap assessment, decision recommendation
    │
    │   ══════════════════════════════════════════
    │   DECISION GATE: Proceed to WFIC-2/3?
    │   - Yes if: 3+ No Coverage areas OR genuinely new professional function
    │   - No if: minor gaps addressable through Task 15.5 scope adjustment
    │   ══════════════════════════════════════════
    │
    ├── [If YES] WFIC-2: Research and competency drafting [CONDITIONAL]
    │       │   Output: draft competencies, F16 definition, architecture document
    │       ▼
    │   WFIC-3: Taxonomy integration and baseline tagging [CONDITIONAL]
    │       Output: database updated to 222+n competencies; F16 established
    │
    ├── [If NO] Proceed directly to Task 15
    │
    ▼
Task 15: Ethical lens population [PENDING]
    │   Prerequisites: Pre-Task 15A; WFIC-3 or WFIC-1 "no action" decision
    │   Scope: all competencies (222+n) across all domains
    │
    ▼
Task 15.5: Context column development — fire and permitting [PENDING]
    │   v7: "Fire intelligence" sub-domain value in fire_context_note
    │
    ▼
Task 16: Stability tier validation + labor market enrichment [PENDING]
    │
    ▼
Task 16.5: Project knowledge inventory and rationalization [PENDING]
    │   v7: WFIC documents included in inventory scope
    │
    ▼
Task 17: GitBook architecture design
    │
    ▼
Task 18: Python export script + Markdown generation
    │
    ▼
Task 19: GitBook build and QA → Published V1
    │
    ▼
Task 20: Delphi preparation
    │   v7: fire intelligence practitioners on Delphi panel
    │   Pre-Task 15B must be complete
    │
    ▼
Task 21: Delphi execution → Published V1.1
    │
    ▼
Task 22: Sentinel network design → Living system launch
    │   v7: WFIC as named sentinel channel
```

---

## Project Knowledge Document Map (Updated for v7)

**Source-of-truth documents:**
- `skills_taxonomy_workforce_v1_updated.xlsx` — primary database
- `20251202_SkillsTaxonomy_Core_V2__1_.txt` — source taxonomy text

**Task sequence:**
- `taxonomy_task_sequence_v7.md` — this document (authoritative; supersedes v6, v5, v3)

**Framework criteria:**
- `profession_family_definitions.md` — v7: will be updated with F16 at WFIC-3
- `workflow_stage_definitions.md`
- `craft_assignment_criteria.md`
- `ethical_lens_framework.md`

**Session behavior:**
- `claude_session_persona.md`

**Exposure classification — instrument and domain records:**
- `domain4_task12_working_record.md` — instrument ratification (Section 1) + D4 pilot table
- `domain1_task13_exposure_classification.md`
- `domain3_task13_exposure_classification.md`
- `domain5_task13_exposure_classification.md`
- `d2_sa21_geospatial.txt` through `d2_sa26_sa27_ai_monitoring_immersive.txt` (5 files)
- D6 exposure: confirm source document location (see Task 16.5 gap flag)

**Cross-domain synthesis:**
- `task13_crossdomain_synthesis.md` — standing rules R1–R12, cross-domain findings
- `task14_crossdomain_synthesis.xlsx` — structured synthesis with 5 analytical sheets

**Tagging working records and structural analysis:**
- `taxonomy_task9_working_record.md`
- `taxonomy_task9_completion_summary.md` — Tier 1 essential; Delphi framing source
- `taxonomy_task10_working_record.md`
- `taxonomy_task11_working_record.md`
- `domain6_task10_workflow_stage_tagging.txt` — D6 workflow/reform data; potential D6 exposure source
- `domain7_task14_tagging_record.txt` — Domain 7 full tagging rationale

**WFIC analysis:**
- `Wildland_Fire_Workforce_Skills_and_Near-Term_Technology_Disruptions.md` — fire workforce research; WFIC primary reference
- WFIC-1 mapping document (to be produced)
- WFIC-2 architecture and competency drafts (to be produced, conditional)

**GitBook domain content:**
- `domain1_sections9_10.md`, `domain2_sections9_10.md`, `domain3_sections9_10.md`
- `domain4_5_6_sections9_10.md`

**External reference:**
- `deep-research-report__8_.md`
- `Five_Functional_Positions_Framework.docx`
- `SAF_Accreditation_Handbook_2024.pdf`
- `Structural_Conditions_of_Environmental_Management_Professions.md`

**Infrastructure:**
- `EMST_Infrastructure_Setup_Guide.docx`
- `EMST_Change_Log_v1.xlsx`

**To be produced:**
- `project_knowledge_inventory.md` (at Task 16.5)

---

*Last updated: March 2026. Supersedes taxonomy_task_sequence_v6.md.*
*v7 additions: WFIC-1, WFIC-2, WFIC-3 inserted between Pre-Task 15B and Task 15.*
*Session protocols and completion checks added for all WFIC tasks.*
*Downstream scope notes added for Tasks 15, 15.5, 16, 16.5, 17, 20, 22.*
*Next update: After WFIC-1 decision gate, update to reflect proceed/no-proceed outcome.*
