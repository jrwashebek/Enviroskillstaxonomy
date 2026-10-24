# EMST 2.0.0-rc.1 — release notes (generated)

- Released: 2026-10-23 · schema 2.0.0-draft.3 · build f68e5af41e43c8faacae789462a71fcf06ac85c0+uncommitted · profile `release`
- **Authorship.** This release was researched and drafted by a team of AI agents (Anthropic's Claude), each given a specialist role, working to a charter set by the EMST project lead. AI agents checked the facts against sources in October 2026. No independent human expert has reviewed the release yet. Role names such as "Chief Taxonomy Architect" are AI agent roles, not people.
- **Not validated.** Nothing in this release has been validated by human subject-matter experts. No Delphi panel, reliability study or job analysis has been run. Every rating and tag is an AI agent's draft (raterType llm, evidence label S) or v1 prior evidence; the display gate shows none of them as findings, and every published element is at describe or develop tier at most, never select.
- Licence: CC0-1.0 for data and standard text (ADR-0013). EMST describes work; it is not a selection instrument, not a classification basis, not a job analysis and not for RIF, adverse action or performance-rating decisions (ADR-0012 I-2; ADR-0024).
- Indigenous knowledge is a distinct body of environmental expertise held and governed by Indigenous nations. It is out of scope of EMST by design (ADR-0007; SPEC §16.1).

## Contents (counted by the build)

| Entity | Records |
|---|---|
| ChangeSignal | 107 |
| Competency | 224 |
| CraftRating | 4026 |
| Credential | 96 |
| DriverEvent | 78 |
| Enactment | 260 |
| ExposureAssessment | 1367 |
| FunctionRating | 90 |
| Indicator | 1706 |
| Instrument | 87 |
| JobFamily | 17 |
| KnowledgeStatement | 51 |
| Pathway | 11 |
| RelevanceRating | 641 |
| RoleProfile | 37 |
| RoleVariant | 140 |
| SeriesRecord | 79 |
| StateClassRecord | 38 |
| Task | 1313 |
| Tool | 101 |
| WatchItem | 3 |

### Competencies by kind

| Kind | Records |
|---|---|
| knowledge-area | 9 |
| practice | 197 |
| transversal | 18 |

### Competencies by module

| Module | Records |
|---|---|
| air | 3 |
| core | 164 |
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
| core | 9 | 137 | 18 |
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
| emerging | 26 |
| established | 198 |

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

- Held Tribal-related records (ADR-0007 §D), reported only as a count: 122.
- Planned v2.0 targets not in this release (deferred to rc.2 or a later wave), by area: built 3, climate 1, culture 1, ehs 2, energy 5, extract 4, lab 1, marine 1, markets 14, worklands 6.

## Excluded by the release gate

| Reason | Records |
|---|---|
| draft (not in a release) | 1372 |
| held (Tribal content hold, ADR-0007 §D) | 122 |
| no minted ID | 130 |
| third-party index-derived licence (ADR-0013; ADR-0029 §9.6) | 102 |
| withheld: claim rests on an unverified claims-register row (WP-15 §2.1; ADR-0031 §8) | 31 |

References removed from released records because their target is not released (by reason): not in this release 3, withheld 34.

## Lint waivers applied (data/v2/governance/lint_waivers.csv)

| Rule | Waived hits |
|---|---|
| (none) | 0 |

## Three-module recurrence (CR-DB-001; for the Editorial Board, not a gate)

Core practice competencies recurring in fewer than three modules: 94 of 137.

## Core size (G-9)

Core competencies: 164 released + held core reported as a count (11); range 120-180 (counts@1.1.0).

## Computed-view rules

| Rule | Version |
|---|---|
| assessment-staleness | 1.0.0 |
| change-indicator | 1.0.0 |
| counts | 1.1.0 |
| display-gate | 1.1.0 |
| effective-use-tier | 1.0.0 |
| federal-series-profile | 0.1.0 |
| inverse-links | 1.2.0 |
| job-family-membership | 0.1.0 |
| mirror-links | 0.1.0 |
| pathway-edges | 0.1.0 |
| role-change | 0.1.0 |
| state-class-view | 0.1.0 |
| venue-applicability | 1.0.0 |

Held Tribal-related items are reported only as a count (ADR-0007 §D); nothing Tribal-related is published before a Tribal Advisory Council approves.

## Delta

Against the previous release (none given): added 10472 · changed 0 · superseded 0 · withdrawn 0 (delta.json).

Against the v1 baseline (delta_v1.json; v1 had no persistent IDs, so every ID is added):

| v1 key kind and outcome | v1 keys |
|---|---|
| competency: no successor in this release | 28 |
| competency: retired | 1 |
| competency: successor in this release | 193 |
| task: no successor in this release | 107 |
| task: retired | 3 |
| task: successor in this release | 556 |
