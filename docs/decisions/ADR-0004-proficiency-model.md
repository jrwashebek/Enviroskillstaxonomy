# ADR-0004: Proficiency — five responsibility levels on seven attributes, defined only where practised

- **Decision point:** DP-4 (proficiency model; number of levels)
- **Status:** accepted (L5 publication provisional on job-analysis evidence; attribute wording provisional on FH/FWCI check)
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** IO, FH, LC, DC, SC, FC, DB, SL, PS, CP
- **Related:** ADR-0003, ADR-0005, ADR-0006 (role levels), ADR-0024 (use tiers and validation), ADR-0026 (learning layer)

## Context

v1 levels are tenure bands (0–2, 3–5, 6–10, 10+ years) with templated text: Advanced Knowledge begins "Expert in…" in 98.4% of cases and Expert begins "Shapes…"; directly observable statements fall from 56% at Foundational to 5% at Expert [E: data-audit §8; IO-010]. Every competency is forced onto every level. The roles converged on responsibility-based levels but differed on the count and on Awareness:

| Role | Proposal |
|---|---|
| IO (P-IO-01/02) | L1 Supervised · L2 Independent · L3 Senior · L4 Lead/Expert · L5 Strategic; seven attributes incl. **augmented practice** and **formation of others**; Awareness = knowledge bundle, *not* a level; level spans |
| FH (P-FH-04) | 1 Awareness · 2 Developmental · 3 Full performance · 4 Advanced · 5 Expert, with indicative GS bands |
| LC (P-LC-02) | Three trainable levels plus a recognized (not taught) Expert level |
| DC (P-DC-10), SC (§8 Q3), FC (§5.3) | Four scope-of-accountability levels; anchor drafts written at four levels |
| DB (P-DB-08), SL (P-SL-10), PS (§9) | Map licensure grades, position qualifications and sign-off authority onto the core scale; levels by supervisory status and autonomy, years second; add "accountable for revenue or sign-off" |

## Decision

1. **One generic scale, L1–L5, defined once in L0** (`vocab/proficiency_levels.yaml`) on IO's **seven attributes**: autonomy; guidelines and judgment; complexity; scope and influence; knowledge application; **augmented practice** (tools and AI); **formation of others**. Labels: L1 Supervised, L2 Independent, L3 Senior, L4 Lead/Expert, L5 Strategic.
2. **Awareness (A) is not a level.** It is a bundle of knowledge statements tagged `A`, assessed only by knowledge checks, never a selection criterion beyond a minimum-knowledge screen.
3. **Level spans.** Each competency declares `level_min`/`level_max`; anchored indicators exist only at levels that pass IO's four publication rules (existence in job-analysis data, distinctness on a named attribute, assessability, Delphi consensus). An empty level is information, not a gap. Default spans by competency type follow `proficiency_model_v2.md` §5.
4. **L5 is defined only for competencies where SME panels confirm strategic demand** (expected ~15–25 governance, policy and portfolio competencies). L5 anchors are provisional until the first job-analysis survey (IO open Q2).
5. **Indicators** are 2–5 per defined level, written to IO's sentence pattern (observable verb + object + condition + standard, ≤ 30 words) and metadata: `augmentation_mode` (unaided / assisted / supervisory), `assessment_methods[]`, `use_class` (describe / develop / select), `validation_status`, `obs4` code, `jurisdiction_variable`, provenance (P-IO-04, P-IO-05). The **competency-level outcome (CLO)** LC asks for *is* the set of indicators at one level; it is published inside L1 (ADR-0026).
6. **Three anchoring resolutions:** generic descriptors for classifying positions; BARS built from indicators for selection and promotion; an entrustment-supervision scale on task-book tasks for training and qualification (IO model §6).
7. **Years are descriptive only** (`typical_time_to_level`, from job-analysis data). No years appear in any level definition, indicator or role requirement.
8. **Crosswalks to other scales live in L6, never as equivalences in L0:**
   - **OPM five-point scales that start at Awareness:** EMST A → OPM 1, L1 → 2, L2 → 3, L3 → 4, L4/L5 → 5 (handled in the OPM crosswalk; IO disagreement 5).
   - **Grades and pay bands:** federal and state role variants carry an *indicative* grade or pay band derived from position profiles, labelled "not a classification criterion" (P-IO-06, FH §6.2). No "L3 = GS-12" table is published.
   - **Licensure grades, NWCG/NIMS position qualifications and sign-off authority:** module-specific level anchors map onto L1–L5 (P-DB-08); the credential itself is a gate (ADR-0003 T-8), so holding a Grade IV operator licence does not *equal* L4.
   - **Four-level anchor drafts from DC, SC and FC** migrate as L1–L4; DC's "enterprise" level 4 and SC's "builds systems others use / sought out by other organizations" content is re-sorted between L4 and L5 by IO's attribute test.
   - **LC's training view:** L1–L3 are course- and work-based-learning targets; L4–L5 are recognized through evidence (portfolio, peer review), never taught as a course (LC template §2).
9. **Role levels** (entry, journey, senior, lead, strategic) used in L3 are bands of these levels, not a separate scale (ADR-0006).

## Rationale and evidence

- Tenure is a weak, legally exposed proxy: prehire experience validity ρ ≈ .06; minimum-years thresholds carry adverse-impact and age risk [E-u: IO-046, IO-049]; OPM itself says tenure is a weak proxy and federal qualifications rest on specialized experience [E: FH-001].
- Generic levels make competencies comparable across role profiles, mobility comparisons (CM) and FES-aligned crosswalks (FH); competency-specific scales alone would not (IO §8 Q3). Generic descriptors alone are what failed in v1.
- Five rather than four: v1's Expert conflated deep technical authority with organization-level strategy; splitting lets most competencies stop at L4 [J: IO]. Four-level drafts lose nothing because they map into L1–L4.
- The augmented-practice and formation-of-others attributes put v1's career-ladder-destruction finding into the definition of level itself (IO §4), and they implement SC's "protect the statecraft apprenticeship" (P-SC-06) and FC's formation proposals (P-FC-08).
- Private ladders advance by scope of accountability — task → task budget → project/client → practice/revenue (PS §9) — which the scope-and-influence attribute carries; "accountable for revenue or sign-off" becomes an L3/L4 descriptor example, not a new level.

## Consequences

- All v1 Knowledge/Application statements and Expert "Publishes…/Shapes…" indicators are retired as level content; usable indicators are migrated as **draft seeds** (`validation_status = seed-v1`), with the 2,104 truncated source indicators recovered first (P-DE-12, P-IO-15).
- CP's gap view and LC's pathways use per-competency profiles, not a single person-level number; CP designs a profile visualization (IO disagreement 2).
- Federal views must label grade bands indicative; SL's state view maps levels by supervisory status and autonomy first (P-SL-10).

## Dissent and trade-offs

- **FH** preferred Awareness as level 1 to match OPM conventions: accepted in the crosswalk, not in the model (one-level offset).
- **LC** argued three trainable levels suffice: preserved as a training view (L1–L3 trainable).
- **DC, SC, FC** wrote four-level anchors: they map without loss; DC said a split of L3 would be the natural extension — the five-level scale provides it at the top instead.
- **Trade-off named:** comparability and defensibility versus the legibility of one uniform four-by-N grid; and one more level to validate, contained by level spans.

## Amendments

- **2026-10-23 — CR-IO-001 / ADR-0029 §5 (CA).**
  - **Publication-rule results.** Each result is `pass | fail | pending | not-applicable`. Evidence is required when PR-1 or PR-4 is `pass`, and CI rejects either `pass` without `job-analysis-confirmed` or `panel-retained` indicators respectively (PUB-14).
  - **PR-2 field.** PR-2 is recorded in `Indicator.distinguishingAttribute` (an `ATT-*` attribute). It is required above the lowest level that has indicators once a record is `candidate`.
  - **Tier mapping.** IO's mapping is ratified: indicators are published at a level when the rules required by the record's use tier pass. Untested rules show "level placement pending validation".
  - **Consequence for rc.1.** Until a Delphi runs, no level is develop-grade.
  - **Waivers.** They live in `data/v2/governance/lint_waivers.csv`.
