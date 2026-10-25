# EMST 2.0.0-rc.1 — release notes (generated)

- Released: 2026-10-25 · schema 2.0.0-draft.4 · build be7760153baa688366b83f5d0bdfc6a722029c53+recut-pending-commit · profile `release`
- **Publication status: not cleared for external publication; items 6 and 7 fail** (release gate, `docs/decisions/PHASE4_BUILD_PLAN.md` §5; `docs/release/2.0.0-rc.1/GATE_REPORT.md`). External publication is signed by the EMST project lead, after at least one named human subject-matter reviewer has read the report and briefs (project lead decision Q13, 2026-10-24). AI agent checks, including the adoption-lead role, are advisory.
- **Authorship.** This release was researched and drafted by a team of AI agents (Anthropic's Claude), each given a specialist role, working to a charter set by the EMST project lead. AI agents checked the facts against sources in October 2026. No independent human expert has reviewed the release yet. Role names such as "Chief Taxonomy Architect" are AI agent roles, not people.
- **Not validated.** Nothing in this release has been validated by human subject-matter experts. No Delphi panel, reliability study or job analysis has been run. Every rating and tag is an AI agent's draft (raterType llm, label S; or v1-analyst, LLM-assisted, prior evidence). Repeated passes of one model are one rater: their agreement is run-to-run consistency, not reliability. The display gate shows none of them as findings, and every published element is at describe or develop tier at most, never select.
- **IDs.** IDs are candidate; they become stable from 2.0.0 (SPEC §10.1: IDs are stable from `published`). The registry rows are `candidate`; an adopter that imports them into an HCM system should expect them to be confirmed, or deprecated with a successor (ADR-0010), at 2.0.0.
- **Agent drafts.** Agent-drafted values that the display gate does not show sit only in an `agentDraft` sub-object, with their raterType, validationStatus and display-gate label: role task-bundle importance, time share, critical and needed-at-entry flags; competency-target importance, distinguishing and critical-for-selection flags; task work function, field and formation dependency, work modes, relationship types and reproduction-regime codes; indicator OBS-4. They are AI drafts, not job-analysis results. The CSV and HCM files leave them out (csv/tasks.csv gives only their gate status in *_status columns; csv/indicators.csv names the agents' declared use class use_class_declared). Values moved into `agentDraft` in this bundle: 13820.
- Licence: CC0-1.0 for data and standard text (ADR-0013). EMST describes work; it is not a selection instrument, not a classification basis, not a job analysis and not for RIF, adverse action or performance-rating decisions (ADR-0012 I-2; ADR-0024).
- Indigenous knowledge is a distinct body of environmental expertise held and governed by Indigenous nations. It is out of scope of EMST by design (ADR-0007; SPEC §16.1).

## Contents (counted by the build)

| Entity | Records |
|---|---|
| ChangeSignal | 107 |
| Competency | 223 |
| CraftRating | 4013 |
| Credential | 96 |
| DriverEvent | 78 |
| Enactment | 260 |
| ExposureAssessment | 1358 |
| FunctionRating | 89 |
| Indicator | 1699 |
| Instrument | 87 |
| JobFamily | 17 |
| KnowledgeStatement | 51 |
| Pathway | 11 |
| RelevanceRating | 635 |
| RoleProfile | 37 |
| RoleVariant | 140 |
| SeriesRecord | 79 |
| StateClassRecord | 38 |
| Task | 1317 |
| Tool | 99 |
| WatchItem | 2 |

### Ratings by rater type and distinct units (counts@1.2.0)

Several passes of one model with one prompt family are one rater (one `raterId`); their agreement is run-to-run consistency, not reliability.

| Rating type | Rater type | Records | Distinct units rated | Distinct raterIds |
|---|---|---|---|---|
| CraftRating | llm | 3924 | 1308 | 7 |
| CraftRating | v1-analyst | 89 | 89 | 1 |
| ExposureAssessment | llm | 171 | 57 | 1 |
| ExposureAssessment | v1-analyst | 1187 | 550 | 1 |
| FunctionRating | v1-analyst | 89 | 89 | 1 |
| RelevanceRating | v1-analyst | 635 | 635 | 1 |

ChangeSignal: 107 records, 68 distinct observations (by `observationId`).

### Competencies by kind

| Kind | Records |
|---|---|
| knowledge-area | 9 |
| practice | 196 |
| transversal | 18 |

### Competencies by module

| Module | Records |
|---|---|
| air | 3 |
| core | 163 |
| envhealth | 3 |
| extract | 1 |
| forest | 16 |
| hazards | 4 |
| parks | 4 |
| waste | 10 |
| water | 6 |
| waterq | 6 |
| wildlife | 6 |
| worklands | 1 |

### Competencies by module and kind

| Module | knowledge-area | practice | transversal |
|---|---|---|---|
| air | 0 | 3 | 0 |
| core | 9 | 136 | 18 |
| envhealth | 0 | 3 | 0 |
| extract | 0 | 1 | 0 |
| forest | 0 | 16 | 0 |
| hazards | 0 | 4 | 0 |
| parks | 0 | 4 | 0 |
| waste | 0 | 10 | 0 |
| water | 0 | 6 | 0 |
| waterq | 0 | 6 | 0 |
| wildlife | 0 | 6 | 0 |
| worklands | 0 | 1 | 0 |

### Competencies by lifecycle state

| Lifecycle state | Records |
|---|---|
| established | 197 |
| watch | 26 |

### Roles by tier (MVP role set)

| Tier | Records |
|---|---|
| P1 | 13 |
| P2 | 17 |
| P3 | 6 |
| P4 | 1 |

### Role variants by sector actor

| Sector actor | Records |
|---|---|
| academic | 6 |
| federal | 34 |
| local | 25 |
| ngo | 15 |
| private | 25 |
| state | 35 |

### Held and deferred

- Held Tribal-related records (ADR-0007 §D), reported only as a count: 163.
- Planned v2.0 targets not in this release (deferred to rc.2 or a later wave), by area: built 3, climate 1, culture 1, ehs 2, energy 5, extract 4, lab 1, marine 1, markets 14, worklands 6.

## Excluded by the release gate

| Reason | Records |
|---|---|
| draft (not in a release) | 1372 |
| held (Tribal content hold, ADR-0007 §D) | 163 |
| held back: removing references to records not in this release would empty a required field (B1) | 3 |
| no minted ID | 130 |
| third-party index-derived licence (ADR-0013; ADR-0029 §9.6) | 102 |
| withheld: claim rests on an unverified claims-register row (WP-15 §2.1; ADR-0031 §8) | 31 |

References removed from released records because their target is not released (by reason): held 3, not in this release 1, withheld 33.

Records held back because removing those references would leave a required field empty: 3 (never shipped with an emptied required field; review B1).

Actor enactments that lost a requires, enables or constrains link to an instrument not in this release: 19; their venue values read “indeterminate (basis withheld)” (review m4).

## How the crosswalks, lifecycle states and change indicators were made (computed from this release)

- **X1 v1 → v2:** 926 rows; justification semapv:LLMBasedMatching 926; decisions from docs/decisions/v1_disposition.csv (CA agent); human reviewer: none (AI agent).
- **X2 task → O*NET task:** 316 rows; justification semapv:LLMBasedMatching 316; human reviewer: none (AI agent).
- **X3 variant → O*NET-SOC / SOC:** 197 rows; justification semapv:LLMBasedMatching 175, semapv:MappingChaining 22; human reviewer: none (AI agent).
- **X4 federal variant → OPM series:** 113 rows; justification semapv:LLMBasedMatching 113; human reviewer: none (AI agent).
- **X5 variant → state and local classes:** 58 rows; justification semapv:LLMBasedMatching 58; human reviewer: none (AI agent).
- **X7 competency → ESCO:** 338 rows; justification semapv:LLMBasedMatching 338; human reviewer: none (AI agent).
- **X12 → DOL AI Literacy:** 49 rows; justification semapv:LLMBasedMatching 49; human reviewer: none (AI agent).
- **X2 coverage:** 316 rows; 202 name an O*NET task; 153 agreed by two LLM coders, 16 of them at closeMatch or better; 114 no term found; κ on match type 0.465 (95% CI 0.388-0.541) below the ADR-0022 target 0.6, so the X2 gate fails. Two LLM coders agreeing is LLM-vs-LLM agreement, not human inter-coder reliability.
- **Lifecycle** (competencies, tasks and roles): established 1396, watch 181. None is proposed or emerging: records whose signals do not meet the vocabulary's entry thresholds are `watch`, with the test stored in `lifecycleBasis`. Lifecycle describes the work, not the record, and does not cap the use tier (effective-use-tier@1.1.0).
- **Change indicators** (change-indicator@1.1.0): 210 rows: watch 210. Only active, human-reviewed signals can move one.

## Not in this release (SPEC §12.5, §17.2)

rc.1 ships: JSON-LD bundle, CSV + Frictionless data package (with the HCM skills-library file and the delta feed), SKOS Turtle, SSSOM (with SSSOM 1.0-strict renderings), computed views, delta files and SHA256SUMS. It does not ship these artifacts that the SPEC says each release carries:

- SPEC §12.5: "does this affect me?" notice.
- SPEC §12.5: DOI.
- SPEC §12.5: SBOM of the data release.
- SPEC §12.5: signed artifacts.
- SPEC §12.5: accessibility conformance report for the data release (the explorer's is site/ACR.md).
- SPEC §17.2: CTDL-ASN (the primary public linked-data channel; nothing is registered in the Credential Registry, so the `ctid` values in csv/hcm_skills_library.csv are derived UUIDv5 values, SPEC §12.3, registered nowhere).
- SPEC §17.2: CASE 1.1.
- SPEC §17.2: RSD.
- SPEC §17.2: Open Badges 3.0 alignment targets.

## Lint waivers applied (data/v2/governance/lint_waivers.csv)

| Rule | Waived hits |
|---|---|
| (none) | 0 |

## Three-module recurrence (CR-DB-001; for the Editorial Board, not a gate)

Core practice competencies recurring in fewer than three modules: 93 of 136.

## Core size (G-9)

Core competencies: 163 released + held core reported as a count (12); range 120-180 (counts@1.2.0).

## Computed-view rules

| Rule | Version |
|---|---|
| assessment-staleness | 1.0.0 |
| change-indicator | 1.1.0 |
| counts | 1.2.0 |
| display-gate | 1.1.0 |
| effective-use-tier | 1.1.0 |
| federal-series-profile | 0.2.0 |
| inverse-links | 1.2.0 |
| job-family-membership | 0.1.0 |
| mirror-links | 0.1.0 |
| pathway-edges | 0.1.0 |
| role-change | 0.2.0 |
| state-class-view | 0.2.0 |
| venue-applicability | 1.0.0 |

Held Tribal-related items are reported only as a count (ADR-0007 §D); nothing Tribal-related is published before a Tribal Advisory Council approves.

## Delta

Against the previous release (none given): added 10436 · changed 0 · superseded 0 · withdrawn 0 (delta.json).

Against the v1 baseline (delta_v1.json; v1 had no persistent IDs, so every ID is added):

| v1 key kind and outcome | v1 keys |
|---|---|
| competency: no successor in this release | 29 |
| competency: retired | 1 |
| competency: successor in this release | 192 |
| task: no successor in this release | 110 |
| task: retired | 3 |
| task: successor in this release | 553 |
