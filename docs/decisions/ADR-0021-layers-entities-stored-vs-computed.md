# ADR-0021: Layers L0–L6, the entity catalogue, and "store atoms, compute summaries"

- **Decision point:** DP-20 (new; CA) — layer model, entity catalogue, stored vs computed
- **Status:** accepted
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** DE, IA, FS, LM, CM, LC, CP, SL, PS, DB, TN
- **Related:** ADR-0001, ADR-0003, ADR-0010; SPEC §3–§6, §12

## Context

v1 stored conclusions and threw away the observations behind them; every stored summary drifted (modal exposure differs from the T1–T3 majority in 63 of 222 competencies; CLD breaks its own rule in 11; D7 Supporting-family counts wrong in 7 of 7; the Workforce Signals sheet differs from the data in 19 of 27 headline numbers) [E: data-audit §1.6, §5, §13]. FS asked for scenario definitions in L0 rather than L5 and lifecycle on L1–L4 (FS §10); SC asked where the instrument registry lives (SC open Q2).

## Decision

### Layers

| Layer | Contents | Cadence | Stored entities |
|---|---|---|---|
| **L0 Reference vocabularies** | crafts (definitions, components, rubric, reproduction-regime attributes); proficiency levels and attributes; sector actors and subtypes; industry, ownership, delivery model; authority positions; sign-off types; work functions, modes, workflow profiles; subsectors, clusters, modules; competency types; reusability; lifecycle states; editorial statuses; use tiers; evidence labels; exposure codebook; **scenario set**; change types; mapping predicates; driver mechanisms; jurisdictional context | annual or slower (MAJOR to change meaning) | `VocabularyTerm` (SKOS concept schemes in `vocab/`) |
| **L1 Competencies** | practice competencies, knowledge areas, transversal practice; indicators by level (CLOs); enactments | annual MINOR | `Competency`, `Indicator`, `Enactment` |
| **L2 Tasks and knowledge** | task statements; knowledge statements (incl. Awareness bundles) | semi-annual within the annual MINOR | `Task`, `KnowledgeStatement` |
| **L3 Roles** | role profiles, role variants, job families (computed groupings with stable IDs), pathways | semi-annual within MINOR | `RoleProfile`, `RoleVariant`, `JobFamily`, `Pathway` |
| **L4 Tools, methods and technical standards** | software, platforms, models, instrument classes, protocols, technical standards, reporting frameworks | dated snapshots; quarterly review for short half-life | `Tool` |
| **L5 Change and evidence** | exposure and craft assessments; change signals; **instrument registry** and dated driver events; watch items; scenario-conditioned rows; friction records | continuous, reviewed; snapshots pinned per release | `ExposureAssessment`, `CraftRating`, `RelevanceRating`, `ChangeSignal`, `WatchItem`, `Instrument`, `DriverEvent`, `FrictionRecord` |
| **L6 Crosswalks and reference registers** | SSSOM mapping sets (O*NET-SOC and tasks/DWAs, SOC 2018, ESCO, OPM series register, state class records, CIP, private reference job architecture, v1→v2); credential register | track upstream; ≥ quarterly | `Mapping`, `MappingSet`, `Credential`, `StateClassRecord`, `SeriesRecord` |
| **Learning (cross-layer)** | learning resources, credential bundles (computed views with stable IDs) | MINOR | `LearningResource`, `Bundle` |
| **Provenance** | sources, change records, decision records, ID registry | every change | `Source`, `ChangeRecord`, ADRs, registry |

- **Scenario definitions are L0** (versioned reference vocabulary, 3-year refresh); **scenario-conditioned assessments are L5** (FS §10 Q1).
- **The instrument registry** is reference data with an L0-like identity discipline but lives in **L5**, because instrument *status* changes continuously through dated `DriverEvent`s; tasks link to durable **mechanisms** (L0, SC's 16 driver mechanisms) and instruments link to mechanisms, so sensitivity is computed and nothing on a competency goes stale (P-SC-02; answers SC open Q2).
- **Credentials** are reference entities registered in L6 (CTDL-ready), linked as gates from L2/L3 (ADR-0022).

### Stored vs computed (P-DE-04, adopted in full)

- **Stored:** authored text; atomic ratings per rater (exposure, craft, relevance, lens triggers, functions and positions where rated) with instrument version, date, rationale, text hash and confidence; links (task → competency `supports` with strength; role → task with importance, time share, criticality, needed-at-entry; role → competency targets; task → tool; task → mechanism; enactments); dated events and signals; mappings; credentials; change records; decisions; the ID registry; **protect** decisions; lifecycle-state decisions.
- **Computed at build by versioned rules** (`vocab/rules/<id>@<version>.yaml`; each view row records `ruleId`, `ruleVersion`, `buildCommit`; CI recomputes and compares): competency and role exposure distributions; consensus values per task; craft blends; dominant craft; competency work-function and subsector roll-ups; reusability suggestions; family relevance and breadth (v1 "Zero-Core"); job-family membership; CLD (task, role, pathway) with driver attribution; entry-path health; robustness class and scenario sensitivity; reform/instrument sensitivity; venue applicability; federal series and state class views; pathway edges, directional coverage and pathway scores; bundles' contents; effective use tier; agreement statistics; all dashboard, README and documentation counts; the data dictionary; inverse links.
- **The schema forbids** computed fields in source records (`additionalProperties: false`); release CSVs include all computed views so spreadsheet users never need the source.

## Rationale

The single defect behind v1's drift was hand-maintained summaries next to data [J: DE §2]. LMPs already generates its README status and validates every record [E: DE-022].

## Consequences

DE implements `scripts/build_views.py` and the rule registry in Phase 4 WP-01; CP's views read only from `dist/views/`.

## Dissent and trade-offs

**DE** names the cost: source files are less self-contained; mitigated by shipping computed views with every release (DE disagreement 3).

## Amendments

- **2026-10-23 — CR-DE-003, CR-DE-001 / ADR-0029 §1, §4 (CA).**
  - **Rule registry home.** `vocab/rules/<rule-id>@<version>.yaml` is the only home for computed-view rules; `schema/rules/` was rejected. Registered so far: `counts@1.0.0`, `inverse-links@1.0.0` and `@1.1.0`, `assessment-staleness@1.0.0`, `effective-use-tier@0.1.0` (interim) and `@1.0.0`, `change-indicator@1.0.0`, and `display-gate@1.0.0`.
  - **Rules versus code.** The code lives in `scripts/` (DE) and `validation/` (IO); the views are built by `scripts/build_release.py` today, which is where the "`scripts/build_views.py`" named above currently lives.
  - **Inverse links.** `Task.tools[]` and `Competency.enactments[]` are inverse links: computed in bundles, forbidden in source.
