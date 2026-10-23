# ADR-0002: Top-level organization — orthogonal facets replace the seven v1 domains

- **Decision point:** DP-2 (top-level organization)
- **Status:** accepted
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** DB, SC, FC, DC, IO, LC, IA, CP, FH, SL
- **Related:** ADR-0003 (competency types), ADR-0017 (work-function facet), ADR-0018 (subsectors and modules), ADR-0021 (entities)

## Context

v1's seven domains mix classifying principles (a knowledge tradition, a technology modality, a management function, a field setting, a communication mode, a policy function and a cross-cutting meta-category) and are collinear with craft (Cramér's V = 0.82) [E: CA-001, audit §3, §5]. They scatter every non-land subsector: water already sits in 1.2, 4.1, 4.7, 6.1 and 6.3, and air sits in 6.7 under "health & justice" [E: DB-003; `v1_keyword_scan_output.csv`]. Adding subsectors as new domains would mix two kinds of grouping; adding them as tags cannot hold subsector-specific competencies (DB §8 options A/B).

## Options considered

1. **Keep a single hierarchy** (domains → skill areas → competencies), adding subsector domains. Simple to explain; duplicates cross-cutting content and gives no steward unit.
2. **Subsector as tag only.** Cheap; cannot hold module-specific depth (operator process control) without bloating the core.
3. **Orthogonal facets plus modules (chosen).**

## Decision

1. **Retire the v1 domain and skill-area layer as the top level.** Keep them as a frozen legacy facet (`v1_domain`, `v1_skill_area`) on migrated records, for provenance, crosswalk and navigation by long-time users. No new content is placed in a v1 domain.
2. **Organize content by orthogonal facets, each an L0 controlled vocabulary**, applied to tasks and rolled up (computed) to competencies and roles:

   | Facet | Applies to | Vocabulary | Decided in |
   |---|---|---|---|
   | Work function (with sub-functions and cross-cutting modes) | tasks (primary), roles (computed) | `vocab/work_functions.yaml` | ADR-0017 |
   | Subsector (44, in 9 clusters; polyhierarchical) | tasks, competencies, roles | `vocab/subsectors.yaml` | ADR-0018 |
   | Competency type | competencies | `vocab/competency_types.yaml` | ADR-0003 |
   | Reusability level (transversal / cross-subsector / subsector-specific / role-specific) | competencies (computed from links, reviewed) | `vocab/competency_types.yaml#reusability` | ADR-0003 |
   | Craft weights + field and formation dependency | tasks | `vocab/crafts.yaml` | ADR-0005 |
   | Workflow profile (named sequences of work functions) | tasks, roles | `vocab/workflow_profiles.yaml` | ADR-0017 |
   | Authority position; sector actor; industry; ownership; delivery model | role variants | `vocab/authority_positions.yaml`, `vocab/sector_actors.yaml` | ADR-0007, ADR-0017 |
3. **Modules are the stewardship unit, not a facet.** A module is a namespaced bundle of subsectors with a steward and release line (ADR-0009, ADR-0018). The core holds transversal practice and cross-subsector competencies; the X cluster (review, inspection and enforcement, EJ and community programs, education, research, data) is core practice, enacted in modules (DB §7 Q1).
4. **Navigation for users is by role family and work function**, not by facet tree. Job families are groupings of role profiles (ADR-0006). The full faceted model is downloadable and queryable.

## Rationale and evidence

- DB tested CA's work-function draft against all 44 subsectors and found it "mostly holds" with specific changes (ADR-0017); DB recommends "orthogonal facets. Retire the v1 domain as the top level and keep it as an alias facet for provenance" (P-DB-03) [J resting on E: DB-003].
- DE's near-duplicate screen shows the knowledge-vs-field-operations split is a v1 architecture artifact: 16 cross-area pairs ≥ 0.25 cosine, 10 across domains (drones 2.3.2/4.5.4; water quality 1.2.4/4.1.3; erosion 1.2.5/4.2.4) [E: data-audit §11]. FC independently lists the same duplicates (P-FC-05).
- Facets are the shape ESCO, ASC and the Singapore framework use to separate kinds of capability from areas of work [E: CA-016, CA-034, CA-036, CA-037].
- CP and LC both need role-first entry with 10–20 relevant competencies, depth one click down (CP §10; LC §8) — facet trees are a back-end structure, not navigation.

## Consequences

- Every v1 competency gets new facet values in migration (ADR-0011, `v1_disposition.csv`); v1 domain values become legacy aliases.
- More facets mean more tagging and more inter-rater reliability work (IO); polyhierarchical subsectors complicate counts (CP). Mitigation: tag tasks once; compute roll-ups; only facets shown to users must pass the α gate (ADR-0024).
- Dashboards and "counts by domain" are retired; counts by work function, subsector and module are generated in CI.

## Dissent and trade-offs

- **No role opposed retiring domains as top level.** LC and FH asked that legacy navigation remain available for the companion research project and existing GitBook readers — granted via the legacy facet.
- **Trade-off named:** expressive, stewardable structure versus the simplicity of one tree. Resolved by keeping the facets internal and the views simple (CA principle 6).
