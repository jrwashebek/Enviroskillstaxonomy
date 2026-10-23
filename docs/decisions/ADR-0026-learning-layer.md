# ADR-0026: The learning layer — competency-level outcomes inside L1, credential bundles as computed views, pathways from role deltas, formation rules

- **Decision point:** DP-25 (new; CA) — LC's open questions on CLOs, bundles, levels, credential alignment, accreditor recognition
- **Status:** accepted (formation rules R6–R7 are normative but provisional until the pilot measures time-to-proficiency and unassisted performance)
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** LC, IO, FC, SC, DC, IA, CM, FH, SL, TN, PS
- **Related:** ADR-0004, ADR-0015 (protect), ADR-0022 (X6, X10), ADR-0023 (bridge paths), ADR-0025 (TX-D)

## Context

Learners and instructors need one competency at one level written as observable outcomes with conditions and criteria; accreditors already work at that grain (SAF: "knowledge of / understanding of / ability to"; I/R/E course mapping) [E: LC-001]. In v1, 63% of knowledge statements start with unobservable verbs, only 5.8% of indicators state a criterion, and 82% of competencies with parsed expert indicators include "Publishes…" [E: LC-031]. The credential market already holds 1,850,034 credentials, 1,022,028 of them badges [E: LC-016, LC-017]. Workforce Pell programmes run 150–599 clock hours over 8 to < 15 weeks and are approved by governors working with state workforce boards [E: V3-03].

## Decision

1. **CLOs are inside the standard (L1)** (answers LC open Q1): for each competency × defined level, the published **assessment anchors** are 2–5 indicators with condition and criterion, each with a persistent IRI (IND IDs) for credential alignment. **Instructional examples** are a separate, unvalidated, labelled layer that can change faster (LC disagreement 3 resolution).
2. **Levels for learning:** L1–L3 are course- and work-based-learning targets; L4–L5 are recognized through evidence (portfolio, peer review), never taught as a course (answers LC open Q3 within ADR-0004).
3. **Credential bundles are computed, versioned views** (answers LC open Q2): 3–8 CLOs forming one work function, computed from role profiles and the CLO layer, with stable BND IDs; credentials align to every CLO IRI and the EMST release via Open Badges 3.0 / CLR 2.0, with evidence type and assessment context; **currency** (refresh interval) follows computed change velocity and lifecycle state (e.g. emerging 2 years, established 5 years) (P-LC-06).
4. **Pathway registry** (P-LC-03): `Pathway` records (PTH IDs, mapped from LC-PW-NN) pinned to EMST versions, built from **role-profile deltas** (R1: teach only the gap), with LC's template fields and rules; the six worked pathways are the pilot set; **LC-PW-06** (three-tier AI and data-practice baseline) and **LC-PW-01** (state environmental-scientist onboarding) come first, followed by CM's two bridge paths: field → statecraft "collaboration bridge kit" and statecraft → field immersion (P-CM-06).
5. **Learning-design attributes** (P-LC-04): assessment-context code; recommended modes; typical hours per level step; prerequisite edges; typical level per task — stored on competencies and tasks; the **formation flag is computed** (P-level task with tacit/experience requirement Hi or Med for that role).
6. **Formation rules** (P-LC-05; normative, provisional): **R6 craft balance** — no pixel without plot (every data- or AI-heavy pathway includes a field ground-truth component, 20–30% field time for remote-sensing reskilling), no model without a decision owner (a statecraft accountability component); **R7 formation protection** — human-essential formation tasks delivered through observed work-based learning, augmented formation tasks assessed with a validation drill, compressive/supervised/substituted formation tasks require a **by-hand quota** of unaided products before review-and-certify credit, and every pathway with formation tasks requires a supervisor formation plan and a mentor. The CLD indicator (ADR-0008) is adjusted when a pathway records a credible **alternative formation route**; pathways report **formation coverage**.
7. **Evidence-equivalence register** (X10) supports recognition of prior learning per CLO (P-LC-07).
8. **Accreditation:** maintain versioned crosswalks to SAF (all four standards), ABET EAC/ETAC, EHAC and NAAEE's 2025 guidelines (P-LC-08); **seek SAF EPRC recognition as an optional mapping framework only after v2.1**, once the annual MINOR cadence has run once (answers LC open Q5 — recognition commits EMST to stable versioning on accreditors' cycles).
9. **Programme-mapping service** (P-LC-14) is a Tier 2 kit with human review and gold-set evaluation; learner records (CLR/LER) stay in adopters' systems (ADR-0012).
10. **Tribal colleges and universities:** curriculum alignment with TCUs is TCU-led (TN issue), under the Tribal gate.

## Rationale

A pathway is the gap between a verified current profile and a target role profile, not a family profile: a forester lacks 23 of the data-science family's core competencies, but a reskilling pathway into a remote-sensing role needs about 8 at specific levels [E: LC-037; J]. Stacking short credentials shows modest positive returns, not environment-specific [E: LC-018]; bundle grain avoids adding noise to a saturated credential market.

## Dissent and trade-offs

- **Efficiency vs formation** (LC's biggest trade-off): formation rules lengthen pathways and consume scarce mentor time; pay the cost for formation tasks only, measure it, and relax quotas where pilot data show no loss of unassisted performance.
- **FC vs LC on simulation and VR:** simulation is right for rare events; it does not replace graduated field exposure for perceptual and situated skills.
- **DC/PS vs tools layer:** learners and employers hire on tool names; tool modules are first-class *learning* objects with expiry dates and tool-agnostic competency credit (LC disagreement 4).
- **Granularity vs usability:** CLOs are many (≈ competencies × trainable levels); bundles carry usability as computed views rather than a new stored level.

## Amendments

- **2026-10-23 — CR-LC-001 / ADR-0030 §1.5 (CA).**
  - **§1:** the CLO is the indicators listed in `Competency.levels[Lx].indicators`. It is craft-neutral. Enactment indicator variants extend it only inside the enactment, and each CLO has a derived IRI (SPEC §12.3).
  - **§4:** pathways are pinned with `emstRelease`. **LC-PW-06** (AI and data-practice baseline) is the first computed **Bundle** (TX-A floor CLOs at L1, plus TX-D formation design for supervisors), not a Pathway. **LC-PW-01** is `seed:lc-pw-cor3-compliance-inspector-onboarding` (state inspector variant).
  - **§6 R7:** formation provisions are typed (`formationProvisions[]` with `responses[]` from `vocab/friction_types.yaml#formation_responses`), and `formationCoverage` is computed from them.
