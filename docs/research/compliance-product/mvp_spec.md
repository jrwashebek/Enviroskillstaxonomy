# MVP Specification: EMST Role Change & Development Planner (NGO pilot release 1.0)

**Role:** CP · **Date:** 2026-10-23 · **Status:** proposal for CA; coordinate with IA (entity model), DE (build), CM (pathways), IO (proficiency), LC (learning), AS (pilot cohort), FH and SL (state and federal variants)

**Labels:**
- **[E]** cites a source I read (IDs in `sources.csv`).
- **[J]** marks my judgment.
- **[S]** marks speculation.

**Where requirement IDs come from:** `CR-xx` refers to rows in `compliance_matrix.csv`; `P-CP-xx` refers to proposals in `product_strategy.md`.

> Note: `report.md`, which the coordinator saves from my returned text, summarizes the architecture and the **answers to CA's architecture questions**. This file holds the full detail: architecture and compliance in §2, the answers in §6.

---

## 1. Scope for the NGO pilot

**Goal.** Let a pilot training or program lead (persona U1 in `product_strategy.md`), working with supervisors (U3) and early-career staff (U2), do three things for a real role on their team:
1. see how the role is changing;
2. diagnose development gaps for a person or team;
3. see where the role can lead across NGO, state and federal employers.

They should be able to turn that into a development plan they actually use. [J]

### In scope (1.0)

| # | Item | Notes |
|---|---|---|
| 1 | **Role-change view** (workflow a) | One page per role variant |
| 2 | **Gap check** (workflow c) | Individual, runs locally; team grid built from shared files |
| 3 | **Pathway view** (workflow b, per role) | 3–6 destinations with gaps and frictions |
| 4 | **Exports** | IDP (DOCX, PDF, CSV); role-change brief (PDF); PD skeleton (DOCX), marked draft |
| 5 | **Competency pages, task pages, evidence and method pages, downloads, citation** | |
| 6 | **Content** | 12–15 role profiles defined by function × level, about 30–40 sector-actor variants, on three corridors (§6.3). Only the competencies and tasks those roles reference (an estimated 120–200 competencies) [S: depends on CA's DP-3 grain] |
| 7 | **Accessibility** | WCAG 2.2 AA; ACR; accessibility statement, privacy notice, security policy |

### Out of scope (1.0), with the reason

| Item | Reason |
|---|---|
| Accounts, cloud saving, sharing links that carry ratings | Compliance: CR-01, CR-08, CR-13, CR-14 |
| Skills inference from résumés or free text about a person | CR-35; deferred, P-CP-20 |
| Full PD builder | Ships in 1.1 for federal and state users; FH/LC disagreement noted |
| Training-program redesign view | 1.1 |
| Full corridor network map | 1.2 |
| Curriculum alignment | 1.2, LC |
| Domain or skill-area browsing as the primary navigation | Facet only |
| Analytics scripts | P-CP-14 |
| Tribal-specific content | Only through TN's protocol |
| Private-sector and academic variants | 2.x |

---

## 2. Architecture and compliance constraints

### 2.1 What changed in 2025–26 that the design rests on

| Topic | Status in October 2026 | Source |
|---|---|---|
| FedRAMP scope (OMB M-24-15 §III) | Covers cloud services that "create, collect, process, store, or maintain Federal information on behalf of a Federal agency". Excluded: "widely available services that provide commercially available information to agencies, but do not collect Federal information" and negligible-risk ancillary services. The agency decides. | [E: CP-016, CP-015] |
| FedRAMP Consolidated Rules 2026 (CR26) and 20x | Launched June 24, 2026. Effective for new 20x certifications from July 4, 2026; mandatory January 1, 2027. New Rev5 certifications end June 11, 2027. Classes A–D (Class A presumed adequate for processing public information). A Program path that needs no agency sponsor. "Authorized" becomes "Certified". | [E: CP-016, CP-018] |
| Secure software | **M-26-05** (January 23, 2026) rescinds M-22-18 and M-23-16. Agencies now set risk-based policies. The CISA attestation form is optional. An SBOM can be required on request. SSDF is a reference. | [E: CP-014] |
| AI | **M-25-21**: employment access is a presumed high-impact area with 7 minimum practices. **M-25-22**: acquisition data rights and anti-lock-in. **M-26-04**: LLM transparency terms in agency procurements. **OPM, August 27, 2026**: AI-drafted PDs are generally not high-impact if officials review, revise and adopt them; 5 CFR 300.103 still applies; applicant data stays in authorized tools. | [E: CP-023, CP-021, CP-022] |
| Accessibility | Section 508 = WCAG 2.0 AA. WCAG 2.2 = ISO/IEC 40500:2025; no WCAG 2.3; WCAG 3 years away. **ADA Title II** dates moved to April 26, 2027 and April 26, 2028 (WCAG 2.1 AA). HHS Section 504 deadline May 11, 2026, not extended. | [E: CP-026, CP-025, CP-012, CP-013] |
| Paperwork Reduction Act (PRA) | Identical questions to 10 or more persons need OMB clearance. Federal employees acting in their role are exempt. Direct observation is generally not "information". | [E: CP-029, CP-033] |

### 2.2 Four tiers

```
TIER 0  OPEN CORE (no personal data, ever)                  owner: DE, IA
  GitHub repo = single source of truth: CSV/JSON/JSON-LD (SKOS), schemas, validators
  Signed, versioned releases + DOI + SBOM + provenance attestation + delta file
  License: CC0 data/vocabularies, Apache-2.0 code; third-party license register
                 |  build in CI from a tagged release
                 v
TIER 1  PUBLIC EXPLORER (this MVP: static, local-first)     owner: CP
  Pre-rendered HTML: roles, competencies, tasks, pathways, evidence
  No server, no accounts, no cookies, no third-party requests, no analytics
  Gap check runs in the browser; answers stay on the device; save/load as a file
  USWDS 3 tokens/components; WCAG 2.2 AA; Pagefind client-side search
  Rehostable unchanged on .gov (DAP added via one include)
                 |  download kits; import release files
                 v
TIER 2  RUN-IT-YOURSELF KITS (adopter-operated)             owner: IA (+CP docs)
  Skills-library import files for HCM/LMS (CASE/CTDL/RSD/HR Open per IA)
  Team gap-analysis workbook/notebook (aggregates, min cell size 5)
  PD drafting kit (templates; optional prompts for the agency's approved LLM)
  Later: skills-inference pipeline with person confirmation + evaluation set
  Each kit: PTA/PIA starter, data-element inventory for SORN check,
            AI system card + impact-assessment inputs, ACR for any UI, SBOM

TIER 3  HOSTED PERSONNEL-DATA SERVICE                       NOT ON ROADMAP
  Would trigger FedRAMP (Class B/C), agency ATOs, SORNs, PIAs, GovRAMP,
  M-25-21 high-impact review, state AI-employment laws. If ever needed:
  partner with an already-certified platform; never build bespoke.
```

### 2.3 When an ATO, FedRAMP, SORN or PIA is needed

| Adoption pattern | FedRAMP | Agency ATO | SORN / PIA |
|---|---|---|---|
| Staff read the public site or download a release | No: it is an information provider that collects no Federal information [E: CP-015, CP-016] | No new ATO; ordinary web-use policy [J] | No |
| An agency loads release files into its HCM or LMS | No | A change within the HCM's existing ATO, plus software and data inventory under M-26-05 [E: CP-014; J] | Covered by the HCM's existing SORN [J] |
| An agency rehosts the static site on .gov | No | Under the hosting platform's ATO, usually a light assessment [J] | A PTA showing no PII [J]; federal website rules apply [J: CP-052, CP-053] |
| An agency runs a Tier 2 kit in its own environment | Only through components it already uses | Inside an existing authorized environment | PTA; PIA if PII; SORN coverage check; AI inventory and impact assessment if AI [E: CP-024; J] |
| An NGO hosts a SaaS where agency staff build profiles | **Yes** | **Yes** | **Yes**, at every agency; plus GovRAMP for states [E: CP-016; J: CP-048] |

**Consequence for the MVP.** The explorer must not collect Federal information:
- no uploads;
- no accounts;
- no server-side processing of input;
- no logs of what users searched or rated.

A "paste your PD" feature would be safe only if parsing ran entirely in the browser. I defer it [J]. Give each pilot state's CISO and each federal unit a one-page applicability statement that maps Tiers 0–1 to M-24-15 exclusions 4 and 5 (P-CP-03).

### 2.4 Standing rules (P-CP-02)

1. **The EMST steward holds no personal data.** Ratings, profiles, uploaded documents and query logs are never collected. A newsletter contact list, if one ever exists, is separate from the product.
2. **Person-level computation happens on the device.** Ratings live in memory. Users choose to save them to a local `.emst.json` file. An optional `localStorage` draft can be cleared with one button. [J]
3. **No user input in URLs.** Shareable links carry only role and competency IDs. [J: CR-13]
4. **No third-party requests at runtime.** Fonts, scripts and icons are self-hosted. There are no embeds. [J: CR-27; the OpenLMP dashboard's Google Fonts call, CP-011, is the pattern to avoid]
5. **Provenance on every judgment.** Every judgment shows its tier, rater type, date and method version. [E: CP-003 principle 7]
6. **Development use only.** Nothing ranks, scores or screens people. Builders produce drafts that a person adopts. [E: CP-022; J: CR-19]

### 2.5 Privacy constraints if person-level data is ever touched (PC-1 to PC-8)

| # | Constraint | Basis |
|---|---|---|
| PC-1 | EMST-operated services never receive person-level data. The EMST team never accepts agency personnel data, including for pilots. | CR-08, CR-10 |
| PC-2 | Person-level computation runs on the person's device (Tier 1) or inside the adopter's authorized system (Tier 2). | CR-01, CR-03 |
| PC-3 | Team views show aggregates with a minimum cell size of 5. Individual ratings stay with the individual unless they choose to share their file. | CR-28, CR-36 |
| PC-4 | Role profiles and signals describe work, not workers. Ingestion strips incumbent names, position numbers and contact details; stores derived signals plus source hashes. | CR-34 |
| PC-5 | Skills inference from documents about an individual is deferred. If it is ever built: Tier 2 only; the person confirms each inferred skill; the evidence span is shown; nothing is stored by default; published error rates, including by subgroup where the data allow. | CR-35 |
| PC-6 | AI-assisted builders produce drafts. A named human adopts them. Exports record that AI assisted and which release IDs were used. | CR-16, CR-11 |
| PC-7 | Every output carries "For development and planning; not a selection instrument." | CR-19 |
| PC-8 | Content governed by Tribal nations follows TN's protocol and the CARE principles. It is excluded from open builds unless consent is recorded. | CR-33 |

---

## 3. Information architecture

```
EMST Explorer  (header: search by role title | Roles | Pathways | Gap check | Evidence | Download)
│
├── Home
│     "Start with a role" search (synonyms, alt titles)  ·  3 task cards  ·  roles covered list
│     Release banner: "Release 2.0.0-pilot.1 · Most judgments are unvalidated v1 analyst assessments"
│
├── Roles
│     ├── Role (function × level), variant switch: NGO | State | Federal
│     │     ├── How this role is changing      ← View 1 (default tab)
│     │     ├── Where it can lead              ← View 3
│     │     ├── Competencies for this role     → links to Gap check (prefilled)
│     │     └── Export: role-change brief (PDF) · PD skeleton (DOCX, draft)
│     └── Roles index (filter: corridor, sector actor, level, craft blend)
│
├── Gap check                                  ← View 2
│     ├── Individual (choose role + level → rate → priorities → export IDP / save file)
│     └── Team grid (load shared files → aggregate grid; min cell 5)
│
├── Pathways (corridor pages: 3 corridors, each a list of roles in order with variants)
│
├── Competencies (A–Z + facets: type, craft, domain/function, roles using it)
│     └── Competency (definition · levels + indicators · tasks · roles · crosswalks · evidence)
├── Tasks (reached from roles/competencies; not in main nav)
│
├── Evidence & method
│     ├── How to read the evidence (tiers, agreement, dates, what would change a judgment)
│     ├── Release notes & what changed · How to challenge a judgment
│     └── Methods (links to repo docs)
│
├── Download & cite (release files, DOI, licence, SBOM, security packet, ACR)
└── Footer: Accessibility statement · Privacy ("what we don't collect") · Security · Licence · Release ID
```

**Labelling.** Titles follow the words practitioners use. Round 0 card sorting and the synonym collection test them (`user_research_plan.md`). The domain and skill-area hierarchy from v1 appears only as a facet on competency lists. [J]

---

## 4. Key screens (wireframe descriptions)

All screens use a single-column layout below 640 px with a 16 px gutter. Every chart has a heading that states its message, a visible text summary, and a "Show as table" control. [E: CP-027; J]

### S1: Role page, "How this role is changing" (View 1; flagship, generated from the forester prototype pattern [E: CP-006])

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Roles › Field → data corridor                                            │
│ Monitoring & Data Technician · Journey level      [NGO] [State] [Federal]│
│ Also called: field data technician, monitoring tech, data collector      │
│                                                                          │
│ IN SHORT  Field collection is shifting toward sensor and drone data;     │
│ the human work moves to calibration, quality control and judging when    │
│ the data are wrong. (Evidence: mostly unvalidated v1 analyst judgments.) │
│                                                                          │
│ HOW THE WORK IS SHIFTING (share of time, by change type)   [Show table]  │
│  Augmented ▒▒▒▒▒▒▒▒▒▒ 45%   Compressed ░░░░░░ 25%   Human-essential ███ 20% │
│  No assessment yet ···· 10%     ← patterns + labels, not color alone     │
│  Evidence mix: 90% v1 analyst (unvalidated) · 10% none                   │
│                                                                          │
│ TASKS, BY WORK FUNCTION                              [Expand all]        │
│ ▸ Collect field data (time share ~30%)                                   │
│   Change: COMPRESSED  - AI/sensors do first pass; human reviews          │
│   Evidence: v1 analyst · Feb 2026 · 1 assessment · ⚑ contested           │
│   Demand signal: postings mentioning drone/sensor QA ↑ (few postings,    │
│   n=14, 2 states) · What would change this? ›  · Challenge this ›        │
│ ▸ Calibrate and ground-truth remote data (~15%)  NEW/EMERGING            │
│ ▸ Enter and QA data (~25%) ...                                           │
│                                                                          │
│ WHAT STAYS HUMAN            │ EMERGING IN THIS ROLE                      │
│ • Judging site conditions   │ • Ground-truth protocol design             │
│ • Safety decisions in field │ • Evaluating AI-classified imagery         │
│                                                                          │
│ NEXT STEPS  [Check gaps for this role]  [Where can it lead?]             │
│ Export: [Role-change brief PDF]  [PD skeleton DOCX - draft]              │
│ Release 2.0.0-pilot.1 · DOI … · For development and planning; not a      │
│ selection instrument.                                                    │
└──────────────────────────────────────────────────────────────────────────┘
```

**Interaction notes.**
- Task rows are native `<details>` disclosures, so they work with a keyboard and without JavaScript.
- The variant switch is a link to the variant's own page, not client-side state, so URLs stay shareable and carry no input.
- "Challenge this" opens a page explaining two routes: a GitHub issue template, or an email address. The page warns that GitHub is a third party. [J: CR-38]

### S2: Gap check, individual (View 2)

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Gap check · Monitoring & Data Technician · Journey   [change role/level] │
│ 🔒 Your answers stay on this device. Nothing is sent anywhere.           │
│    [Save to file] [Open saved file] [Clear everything]                   │
│                                                                          │
│ 1 of 14  Data quality control                   Core for this role       │
│   Target for this level: PROFICIENT                                      │
│   What proficient looks like (observable):                               │
│    • Flags out-of-range values against protocol before submission        │
│    • Documents corrections with reason and source                        │
│   Where are you now?  ( ) Not yet ( ) Developing (•) Proficient          │
│                       ( ) Advanced ( ) Not sure                          │
│   Optional: supervisor view ( ) … (•) Developing   Note: [__________]    │
│   Linked to a changing task ✓ (Collect field data - COMPRESSED)          │
│                         [◂ Previous]  [Next ▸]  [See summary]            │
└──────────────────────────────────────────────────────────────────────────┘
SUMMARY: "Start with these 3" (largest gap × tied to changing tasks ×
core), "Strengths", "Where self and supervisor differ" (talk about these),
export [IDP DOCX] [IDP PDF] [CSV]; each item links to "how people
typically build this" (LC stub) and to the competency page.
```

**Rules.**
- Radio buttons have targets of at least 24×24 px (WCAG 2.5.8).
- "Not sure" is always offered.
- The summary ranks competencies, never the person.
- No score or percentage of readiness is shown. The output is a prioritized list. [J: CR-19, PC-7]
- The saved file contains `release_id`, `role_variant_id`, `level`, `ratings[]` and `schema_version`. There are no names unless the user types one into the note.

### S3: Team grid

The lead loads 5 or more saved files shared by team members, through the organization's own drive or email, with consent (PC-3).

| Competency | Not yet | Developing | Proficient | Advanced | Target |
|---|---|---|---|---|---|
| Data quality control | 1 | 3 | 2 | 0 | Proficient |
| … | | | | | |

- Columns are counts. Names are hidden by default.
- If fewer than 5 files are loaded, the grid shows only "fewer than 5 people; showing individual files is up to you".
- Export as CSV or PDF.
- Nothing leaves the device. [J]

### S4: Pathway view, "Where this role can lead" (View 3)

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Where Monitoring & Data Technician (NGO, journey) can lead               │
│ List view (default) | Diagram view                                       │
│                                                                          │
│ ▸ GIS / Remote-Sensing Analyst · State · journey                         │
│   Shares 9 of 14 core competencies.  Build: spatial analysis, scripting, │
│   metadata standards.   Frictions: state civil-service exam; class       │
│   series [state class code, dated].  Evidence: computed from role        │
│   profiles (not yet observed in real career moves)                       │
│   [Check my gaps for this role]                                          │
│ ▸ Physical Science Technician-type role · Federal · journey              │
│   Crosswalk: OPM series [code, as of 2026-10] · O*NET-SOC [code]         │
│   Frictions: US citizenship; seasonal→permanent conversion rules …       │
│ ▸ Monitoring Program Coordinator · NGO · lead  …                         │
└──────────────────────────────────────────────────────────────────────────┘
```

- The list is the accessible primary view. The diagram view is an enhancement that has keyboard focus order and the same information in text (WCAG 2.5.7: no drag needed).
- "Shares N of M core competencies" is used in place of a similarity score, because an absolute count is easier to understand and harder to over-read. [J]

### S5: Competency page

Contents:
- type (CA DP-3), definition, durable-capability note (no tool names);
- levels with 3–5 observable indicators each (IO);
- tasks it serves, with their change status;
- roles that require it, with target levels;
- tools layer links (dated);
- crosswalks;
- an evidence panel;
- "how people typically build this" (LC);
- `"Download this record (JSON)"`.

### S6: Evidence & method

Covers tiers, agreement, how dates and horizons work, calibrated words, what "contested" means, how to challenge a judgment, a release diff, and known gaps. A worked example walks one task row through every element of S1.

### S7: Exports

| Export | What it contains |
|---|---|
| **Role-change brief** (PDF, tagged and accessible) | S1 content as one to two pages, with the evidence tier on every claim |
| **IDP** (DOCX, PDF, CSV) | Priorities, indicators, a notes column |
| **PD skeleton** (DOCX) | Duties grouped by work function, with time shares, linked competencies, and task IDs for traceability. Watermarked "DRAFT generated from EMST release X; review, revise and adopt", matching the human-adoption condition in OPM's AUG 2026 memo [E: CP-022] |

Every export shows the release ID, DOI and the development-use statement (PC-6, PC-7).

---

## 5. Data needed from the v2 model

This aligns with CA's layers L0–L6 [E: CP-003] and with IA's entity model, which was not yet published when I wrote this. IA owns the formats; this table gives the product's needs. "MVP" means required for 1.0.

| Entity / field | Needed by | MVP | Notes / owner |
|---|---|---|---|
| **Role profile** (L3): id, title, alt_titles[], function, level (entry, journey, lead), summary_plain (≤60 words), lifecycle_status | S1, S4, search | ✓ | FH, SL, PS, CM; plain summaries written and reviewed by CP |
| **Role variant**: id, role_id, sector_actor (+ subtype), jurisdiction (optional), crosswalks[] (OPM series and quals, state class, O*NET-SOC, each with as_of date and match type), frictions[] | S1 switch, S4 | ✓ | FH, SL, IA |
| **Role–task link**: importance, time_share (range allowed), source, confidence | S1 shares, PD skeleton | ✓ | FH, SL, practitioners; time share can start as ordinal bands |
| **Task** (L2): id, statement, work_function, craft (weights or ordinal), competency_ids[], v1_alias | S1, S5 | ✓ | FC, DC, SC, DB |
| **Exposure assessment** (L5): assessment_id, task_id, (role_id), dimension values (type A, Ac, H, S, V; tacit; vector; horizon), rater_type, rater_id (pseudonymous), method_version, codebook_version, date, confidence, evidence_ids, contested flag, scenario_id | S1 change labels, agreement, tier | ✓ | LM, IA; v1 values migrated with rater_type "v1-analyst" [E: CP-003] |
| **Change signal** (L5): id, type (postings, PD, plan requirement, policy event), target (task or role), period, direction, magnitude **with interval or n**, coverage_note, source_ids, date | S1 demand line | Partial | LM, IA; must allow "no signal yet" |
| **Emerging item**: competency or task with lifecycle_status "emerging" plus evidence | S1 "Emerging" | ✓ | CA, FS, DC |
| **"Stays human" rationale**: a short text per task where H applies, with the assessment it comes from | S1 | ✓ | FC; must be descriptive, not normative (CA's critique of D7) [E: CP-003] |
| **Competency** (L1): id, type, title, definition, levels[] with indicators[] (observable), tasks[], tools[] (L4, dated) | S2, S5 | ✓ | IO, LC, craft leads |
| **Role–competency link**: target level per role level, criticality (core or supporting), served_task_ids[] | S2 priorities | ✓ | IO, FH |
| **Pathway edge** (computed): origin_variant, dest_variant, shared_core_count, dest_core_count, gap_competency_ids[], similarity metrics, basis (computed or observed), observed_count (aggregate, minimum 5) | S4 | ✓ computed; observed later | CM [E: CP-010] |
| **Friction attribute**: id, actor pair or destination, type (exam, citizenship, credential, pay system, conversion rule), text, jurisdiction, as_of, source | S4 | ✓ for MVP corridors | SL, FH, CM |
| **Learning hook**: competency × level → resource type or curricula (optional) | S2 summary | Stub | LC |
| **Release metadata**: release_id, DOI, date, evidence-tier legend, licence, delta | Every page and export | ✓ | DE |
| **Governance flag**: CARE or TN consent status per record; open_build boolean | Build filter | ✓ | TN, DE |

**Build-time computations** (DE; matches CA's computed-not-stored list [E: CP-003]):
- role change-mix bars (time share by change type);
- evidence-tier mix;
- agreement summaries;
- pathway edges and shared counts;
- gap-priority weights (gap × criticality × link to changing tasks);
- search index (Pagefind).

Each page also gets a JSON "record" download. [J]

---

## 6. Answers to CA architecture questions

These answer `chief-architect/architecture_hypotheses.md` §6 (CP) and DP-6.

### 6.1 Q1: Which three views does the first user need, and what does each require of the data model?

From a product standpoint I support CA's hybrid lean: a task-and-role spine underneath, with competencies as the user-facing packaging (§4 of the hypotheses). All three views are anchored on roles and computed from tasks. A competency hub without the task layer could produce none of them. [J]

**View 1: "How is this role changing?"** (role-change view; S1)

This is v1's forester prototype [E: CP-006], generated from data.

- **Data model requirements:**
  - L3 role profiles with variants, alternative titles and plain summaries.
  - Role–task links with **time share** (this drives "how much of the job"; the prototype used duty percentages).
  - L2 tasks with work function and craft.
  - **Several L5 exposure assessments per task**, each with rater type, date, method version, confidence and contested flag, so the view can show agreement and tier.
  - L5 change signals that carry an **interval or sample size** and a coverage note.
  - Emerging competencies and tasks with lifecycle status.
  - A descriptive "stays human" rationale.
  - Build-time computed role summaries.
- **Minimum for 1.0:** 12–15 role profiles. v1 assessments are migrated as "v1 single analyst". The view must render "no signal yet" honestly.

**View 2: "Where are the gaps?"** (gap check, individual or team; S2 and S3)

This runs locally.

- **Data model requirements:**
  - Role–competency links with target level per role level, criticality, and **served_task_ids** (so the view can say "this gap matters because the task is changing").
  - L1 levels with **3–5 observable, anchored indicators** per level. IO's DP-4 decides the scale. The generic statements in v1 cannot be self-rated [E: CP-003 §4.3].
  - Optional learning hooks (LC).
  - No person entity in the model. Ratings exist only as a versioned client-side file format.

**View 3: "Where can this role lead?"** (pathway view; S4)

- **Data model requirements:**
  - Computed pathway edges between role variants, using CM's similarity basis (CM's question 1), with an asymmetric gap list. CM's `dest_core_absent_in_origin` already does this at family level [E: CP-010].
  - A flag showing whether each edge is computed or **observed** (observed only as an aggregate with a minimum count of 5).
  - First-class **friction attributes**, dated and sourced.
  - **Dated crosswalks** on destination variants, because OPM consolidates series through September 2027 [E: CP-003].

**Cross-cutting rule:** every number on screen traces to stored, attributed records in a tagged release and is computed at build time. Nothing is hand-typed into a page. [J; E: CP-003]

### 6.2 Q2: What privacy constraints apply if role profiles or signals ever touch person-level data?

PC-1 to PC-8 in §2.5 apply. In architectural terms:

1. The EMST schema contains **no person entity**. Person-level structures exist only as client-side file formats (Tier 1) or kit schemas (Tier 2) that adopters instantiate in their own authorized systems.
2. Signals from documents that can name people (PDs, postings, plans) are **de-identified at ingestion**. Only derived signals and source hashes are stored.
3. **Observed career transitions** come only from consented research cohorts or from aggregates that agencies compute internally. They are stored as aggregate edges with a minimum count of 5, never as individual histories.
4. If any person-level processing ever runs on EMST infrastructure, the full regime applies: FedRAMP, ATO, SORN, PIA, GovRAMP, M-25-21 review and state AI-employment law (§2.3, last row). That is the reason to keep it off.

[J; CR-01, CR-08, CR-10, CR-28, CR-34, CR-35]

### 6.3 DP-6: role grain and first role set

**Grain.** Use **function × level of responsibility** (entry, journey, lead) with **sector-actor variants**. Do not use OPM series × grade:
- series are being consolidated and are federal-only;
- grade is a pay construct that state class levels do not match.

Each variant carries dated crosswalks to series, state class and SOC. [J; E on consolidation: CP-003]

**Size.** 12–15 profiles, about 30–40 variants. That is enough to cover three corridors end to end, and small enough for practitioners to validate each profile in one 60-minute session. [J]

**Candidate corridors.** These are hypotheses. AS confirms them against the cohort's actual roles; FH and SL confirm the destinations.

1. **Field → data:** field or crew technician → monitoring or data technician → GIS / remote-sensing analyst.
2. **Field → statecraft:** crew lead or restoration project lead → environmental review / permitting specialist → program manager.
3. **Corps → career:** conservation corps member → seasonal technician (state or federal) → permanent technician or specialist. Add fire roles (fuels technician → fuels / prescribed-fire specialist) or water-quality roles if the cohort's employers need them.

The corridors cross all three crafts on purpose, so the pilot tests the theory of change rather than a single craft. [J; v1 pilot framing E: CP-009]

---

## 7. Data visualization and uncertainty display standard (P-CP-13)

### 7.1 General rules

These follow USWDS data-visualization guidance [E: CP-027]:

- Use common chart types: horizontal bars, dot ranges and lists.
- State the message in the heading.
- Give every chart a visible text summary and a "Show as table" control. Charts are SVG with `aria-hidden="true"`, paired with a real `<table>`.
- Never make information available only on hover.
- Never use color alone. Pair the palette with patterns and direct labels.
- Do not use red–green pairs.
- Meet 3:1 non-text contrast for marks and 4.5:1 for text.

[E: CP-027; J]

### 7.2 Evidence tiers

Three tiers, using CA's terms [E: CP-003]. Each appears as a text badge:

| Tier | Badge text |
|---|---|
| T-v1 | "v1 single analyst (LLM-assisted), unvalidated" |
| T-panel | "Practitioner panel, n raters, agreement x of n" |
| T-bench | "Panel + external benchmark agree" |

The badge is always text first, with an icon second.

### 7.3 Showing agreement, confidence and quantities

- **Agreement:** show counts in plain language, for example "2 of 3 assessments: Augmented; 1: Compressed". Do not show κ or percentages. Mark a row "Contested" when assessments disagree or v1 flagged it. v1 flagged 33 competencies [E: CP-007].
- **Calibrated words.** Use a fixed vocabulary for confidence: *low / medium / high*. Confidence is derived from the amount of evidence and the level of agreement. This is modelled on the IPCC uncertainty guidance [J: CP-072]. Use the words, never invented precision.
- **Quantities.**
  - Show direction plus range plus n, for example "↑ rising; 2023→2026; 14 postings in 2 states (few)".
  - Below n=30, show counts, not percentages.
  - Below n=10, show "too few to say".
  - Never draw a trend line without the underlying points. [J; quantile-dotplot and uncertainty-viz literature, CP-071]
- **Time.** Label every judgment with its date ("assessed Feb 2026"). Show horizons as ranges labelled "projection: 1–3 years".

### 7.4 Rules for aggregation and explanation

- **Aggregation rule.** The only roll-up is the role-level time-share bar. It always carries an evidence-mix line beneath it. **No headline percentages** across the taxonomy from single-rater data. That was the failure in v1's Flourish story [E: CP-004, CP-003].
- **"What would change this?"** Every exposure label has one sentence describing the evidence that would move it, for example "Panel ratings from field supervisors in 2+ states".
- **Comprehension is a release gate.** If Round 2 users misread tiers more than 20% of the time, revise the display or hide T-v1 values (`user_research_plan.md` §5).

### 7.5 Palette

Use the USWDS color tokens with a colorblind-safe set of 4 categorical hues for change types:
- Augmented, Compressed, Human-essential and Substitution, each with a distinct pattern;
- a neutral grey with a dotted pattern for "No assessment".

Retire v1's green/amber/red severity scheme [E: CP-004]. Validate the palette with a CVD simulator and in Round 1. [J]

---

## 8. Technology recommendation (P-CP-11)

### 8.1 Criteria

1. Static output and no runtime third parties (CR-01, CR-27).
2. Full control of markup for WCAG 2.2 AA (CR-20, CR-21).
3. Pages generated from release JSON (generated, never hand-authored).
4. A small dependency tree, which keeps the SBOM short and the patch burden low (CR-05, CR-06).
5. Maintainable by a very small team. v1's model was "a single analyst position augmented by AI" [E: CP-009].
6. Rehostable on .gov with USWDS (CR-22).
7. Longevity and how widely the tool is used.

### 8.2 Options appraised

| Option | Status (Oct 2026) | Fit | Verdict |
|---|---|---|---|
| **Eleventy (11ty) 3 + USWDS 3 + Pagefind** | 11ty 3.1.7 (Oct 15, 2026); USWDS 3.14.0 (Aug 2026); Pagefind 1.5.2 (Apr 2026) [E: CP-028] | Data-driven pages from JSON; ships zero client JavaScript by default; small dependency tree; full markup control; USWDS is plain CSS and JS | **Recommended** [J] |
| **Astro 7 (+ Starlight for docs)** | astro 7.4.2 (Oct 21, 2026); Starlight 0.42.6 [E: CP-028] | Strong island architecture; Starlight has good accessibility defaults and built-in Pagefind; larger dependency tree and faster major-version churn | **Equal alternative** if DE prefers it [J] |
| **Python generator (Jinja templates) in DE's pipeline** | Same pattern as the OpenLMP single-page dashboard [E: CP-011] | One language for the pipeline and the site; very small footprint; more custom code to maintain | Acceptable if DE wants a single toolchain [J] |
| **Zensical** (successor to Material for MkDocs) | 0.0.71 (Oct 16, 2026), pre-1.0 [E: CP-035]; FedRAMP's own documentation site uses it [E: CP-020] | Excellent for documentation and methods pages; built for documents, so a poor fit for computed role views; pre-1.0 risk | Use for a methods and docs sub-site **only if** DE wants Python; not for the explorer [J] |
| **Material for MkDocs** | 9.7.7 (Jul 2026) [E: CP-035] | Same as Zensical, and its maintainers have moved on to Zensical | Not recommended for new work [J] |
| **Observable Framework** | 1.13.4; last modified Apr 2026 [E: CP-028] | Excellent data visualization; heavier client side; release cadence has slowed | Not for the MVP; possible for research notebooks [J] |
| **GitBook** (v1 plan) | Hosted SaaS [J: CP-067] | Third-party hosting and scripts; limited control over accessibility conformance and computed views; navigation starts from domains | **Retire** for the product [J] |
| **Airtable** (v1 plan) | Hosted SaaS [J: CP-068] | Not a publishing tool. As source of truth it conflicts with the decision that GitHub is the source of truth; the free plan lacked scripting [E: CP-009] | **Retire** as source of truth [E: CP-003] |
| **Flourish** (v1 plan) | Canva SaaS [J: CP-069] | Third-party embeds; publicly published data; no control over accessibility; claims that are hard to version | **Retire** from the product; one-off stories only, built from tagged releases [J] |

### 8.3 Hosting and domain

- Host on **GitHub Pages**, built by GitHub Actions from tagged releases.
- Use a custom domain owned by the steward (AS).
- HTTPS is enforced.
- GitHub Pages cannot set response headers. Add CSP through a `<meta http-equiv>` tag. If HSTS preload or a full header-based CSP is required, DE chooses a static host that supports headers and records it as a new third party. [J: CP-080]
- If an agency adopts, it mirrors the built site under .gov on its own authorized platform and adds DAP through one include (CR-13, CR-22).

### 8.4 Client-side JavaScript budget

- Around 30 KB compressed for the gap check and team grid. Vanilla JS or small web components; no framework.
- Everything else works without JavaScript.
- Saved files are plain JSON with a `schema_version` for forward compatibility.

[J]

---

## 9. Security packet and release gates

**Release gates.** A release is blocked unless all of the following hold:
1. Schema validation passes (DE).
2. Automated accessibility checks show zero violations on all page templates, and the manual keyboard and screen-reader pass on S1–S4 is complete.
3. The SBOM is generated, dependencies have no critical vulnerabilities, and the Scorecard run is complete.
4. Every displayed value has a tier, and the claims checklist is done (P-CP-09).
5. The release ID and DOI are stamped on pages and exports.
6. The ACR is updated for major releases.

**Security packet** (P-CP-03), published under `/download/security/`. [E: CP-014, CP-016, CP-034]
- applicability statement;
- data-flow diagram;
- SBOM;
- checksums;
- SSDF mapping;
- voluntary CISA attestation form;
- Scorecard report;
- SECURITY.md and disclosure policy.

---

## 10. Analytics without tracking PII (P-CP-14)

**1.0 has no analytics script** and sets no cookies. Instead:
1. **Research instrumentation.** Task success, time and comprehension are measured in moderated sessions and the field trial (`user_research_plan.md`).
2. **Release download counts** from GitHub release assets, which are aggregate and anonymous.
3. **Opt-in feedback.** A "Was this useful?" link opens a short form hosted by the NGO steward. It is never embedded and never automatic, and it carries a notice.
4. **Self-reported artifact use** in field-trial check-ins.

If aggregate page counts are later required:
- use a self-hosted, cookieless counter that does not store IP addresses or user agents, documented in the privacy notice;
- or, on a federal mirror, use DAP (no PII, IP anonymization [E: CP-032]).

Never send role selections or ratings to any analytics endpoint. [J: CR-13]

---

## 11. Success metrics for the pilot

These must be coordinated with CM's expansion metrics. All targets are [J] and should be revisited after Round 0 baselines.

| Metric | Target by the end of the pilot | Measured by |
|---|---|---|
| Core task success (5 tasks, unassisted) | ≥ 80% (Round 3); ≥ 70% gate at Round 1 | Moderated tests |
| UMUX-Lite (2 items; maps to SUS) | Equivalent to SUS ≥ 70 [J: CP-070] | End of session |
| Uncertainty comprehension | ≥ 80% correct on 4 probes; over-reliance < 20% (would act on a contested label without checking) | Probes (`user_research_plan.md` §5) |
| Time to produce a role-change brief or IDP | ≤ 20 minutes, and faster than the Round 0 baseline method | Timed task and field trial |
| Real use | ≥ 60% of pilot organizations use an EMST output in a real development or planning decision; ≥ 1 artifact per organization | Field-trial check-ins |
| Repeat use | ≥ 50% of field-trial participants use the tool in 2 or more separate weeks | Diary (self-report) |
| Taxonomy yield | ≥ 30 change requests from research; CA accepts or adapts ≥ 1/3; every MVP role profile reviewed by ≥ 3 practitioners | Change-request log |
| Accessibility | 0 open WCAG A failures; ≤ 5 minor AA issues with dates for fixes; assistive-technology users complete the core tasks | ACR; sessions |
| Procurement readiness | One pilot-state CISO and one federal unit confirm in writing that Tier 1 needs no new ATO or FedRAMP, or name exactly what it does need | Security packet review |

---

## 12. Release plan

| Weeks (pilot clock) | Deliverable | Research |
|---|---|---|
| 1–4 | Role set confirmed (AS, FH, SL); data contract with IA and DE; low-fidelity prototypes of S1, S2, S4 for 3 roles | Round 0 discovery; card sort; baseline task timing |
| 5–8 | Clickable prototype on real v1-migrated data for 4–6 roles; uncertainty display variants | Round 1 usability and comprehension (A/B of two tier displays) |
| 9–12 | 1.0 beta: all 12–15 roles; exports; security packet; ACR draft | Round 2 usability, including assistive-technology users |
| 13–20 | 1.0 in use: field trial at pilot organizations; fixes; taxonomy change requests to CA | Field trial (diary, check-ins), Round 3 summative |
| 21–26 | 1.1 scoping with federal and state users (PD builder, training-program view) | Federal and state rounds (PRA-aware) |
