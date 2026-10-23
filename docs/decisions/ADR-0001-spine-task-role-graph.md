# ADR-0001: Spine — a task-and-role graph inside, typed competencies outside

- **Decision point:** DP-1 (spine entity)
- **Status:** accepted
- **Date:** 2026-10-23 · **Decider:** Chief Taxonomy Architect (CA)
- **Roles consulted:** IO, FH, SL, CP, LC, IA, CM, LM, DE, FS, PS
- **Supersedes:** the "provisional lean" in `docs/research/chief-architect/architecture_hypotheses.md` §4
- **Related:** ADR-0003 (typing and grain), ADR-0006 (role grain), ADR-0019 (NLP target), ADR-0021 (entity catalogue), ADR-0024 (validation)

Evidence labels follow TEAM_BRIEF §3: [E] evidence with a source or proposal ID, [J] judgment, [S] speculation.

## Context

v1 had one entity, the competency, and could not describe a job, a craft blend, a sector actor, a tool or a change over time (audit §0). Phase 1 set three options: A (competency hub), B (task-and-role statement graph, NICE/O*NET pattern) and C (federated core plus modules). C is about coverage and governance and is decided in ADR-0009 and ADR-0018; this ADR decides which entity carries meaning and validity.

## Options considered

| Option | What it is | For | Against |
|---|---|---|---|
| A. Competency hub | Competencies are the central entity; tasks hang off them | Matches federal/state HR language; fastest v1 migration | Hardest unit to validate; rebuilds v1's grain problem; exposure, mobility and NLP still need tasks |
| B. Task-and-role graph only | Tasks/knowledge statements and roles; competencies are optional views | Highest analytical power; validates best | Illegible to HR, learners and instructors; very large SME burden |
| **Hybrid (chosen)** | Tasks (L2) and role profiles (L3) are the spine; typed competencies (L1) are first-class, curated, assessable packages **justified by links to critical tasks** | Validity of B, usability of A | Two things to maintain; link discipline needed |

## Decision

1. **The spine is the task-and-role graph.** L2 tasks are atomic, persistent work statements, many-to-many with competencies and roles. L3 role profiles bundle tasks with importance and time share. Exposure, craft weights, change signals and mobility attach to tasks and are computed upward.
2. **Competencies are first-class, not mere views.** Each L1 competency is a persistent, typed, named and leveled package that users hire, train and credential against. It must link to at least one task (rule C-1, SPEC §5.2), and to at least one *critical* task before it can carry `use_class = select`.
3. **Users enter through roles and competencies, never through the raw graph.** Every user-facing view (role change, gap check, pathway, federal series view, state class view, learning pathway) is generated from the graph.
4. **Links are stored once, on the many side** (task → competency `supports`; role → task bundle and competency targets). Inverses, blends, summaries and counts are computed (ADR-0021).
5. **Named sub-decision DP-18a** (ADR-0019) governs when automated text linking moves from competencies to tasks.

## Rationale and evidence

- **Validity runs through tasks.** Task-level job-analysis ratings are more reliable than ratings of abstract descriptors, and competency ratings inflate more under self-presentation [E-u: IO-043, IO-044, IO-045]. UGESP content validity rests on work behaviors, so a competency is defensible in selection only through linkage to validated critical tasks [E-u: IO-020]. IO's answer to DP-1: "the task statement, clearly. Competencies validate second, by linkage" (P-IO-07).
- **Federal and state HR use competency-shaped artifacts.** The Chance to Compete Act and the Merit Hiring Plan centre "critical competencies identified through job analysis" [E: FH-023, FH-002]; FH's grain table (role = use, competency with proficiency = assessment, task = evidence) is exactly the hybrid (FH §9 Q1). SL: the state-facing view must be "class-shaped" but the crosswalk engine needs tasks (SL disagreement 2).
- **Every product view is task-anchored.** CP's three MVP views are "role-anchored and computed from tasks, so a competency hub without a task layer could produce none of them" (CP §11 Q1).
- **Mobility, exposure and new-work detection work at task grain.** CM: importance-weighted asymmetric task overlap is the similarity basis (P-CM-04). LM: task-level exposure and observed use exist for every environmental O*NET task, and "new work can only be detected at the task level" (LM §7 Q4). The external measures worth ingesting are anchored to O*NET tasks/DWAs (P-LM-02, P-LM-03), which was CA's stated condition for strengthening the task spine (hypotheses §7).
- **Curriculum needs anchored competencies.** "A competency without level anchors is not usable by an instructor. An atomic statement graph without competency views is not usable either" (LC §8 Q1).

## Consequences

- L2 must be rebuilt richer than v1's three-per-competency layer: variable count, verb + object + condition/purpose, production split from specification/review/defence (P-FS-11), execution split from in-place adaptation (FC §8 Q1), crosswalk-first to O*NET tasks/DWAs (P-LM-02, P-IA-08).
- The SME burden concentrates on tasks. IO's mitigation is adopted: matrix sampling (≤ ~80 tasks per respondent), 3–5 priority function clusters validated first, and unvalidated tasks allowed with `validation_status = draft` (IO §8 Q1; ADR-0024).
- DE's schema must enforce the task-link rule and forbid stored inverses (ADR-0021).

## Dissent and trade-offs

- **IA (timing):** agrees with the destination but warns that v1 tasks are a worse NLP target than competencies today (dev P@1 0.43 vs 0.53) [E: IA §5.3]. Accepted; handled by ADR-0019.
- **FH:** "every federal hiring artifact is competency-shaped" — accepted as a packaging requirement, not a spine argument.
- **CM:** task-weighted role bundles multiply SME burden; proposes depth over breadth (10–15 pathways first). Accepted in ADR-0006 and ADR-0023.
- **Trade-off named:** two maintained layers (tasks and competencies) and a link discipline, in exchange for validity and usability together.

## What would change this decision

IO's craft-rating pilot arm (40 competencies vs 150 tasks) showing competency-level ratings beating task-level by ≥ .10 α (P-IO-12 decision rule 4) would move craft ratings, not the spine, toward competencies. Evidence that adopters cannot consume competency packages generated from a task graph would reopen packaging, not validity.
