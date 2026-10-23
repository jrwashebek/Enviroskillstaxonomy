# ADR-0005: Crafts — v2 definitions, task-level 0/1/2 ratings, field and formation dependency, reproduction regimes

- **Decision point:** DP-5 (craft representation and elicitation)
- **Status:** accepted for the representation and definitions; **provisional** on the scale (0/1/2 ordinal) until IO's craft-rating pilot reports (6–8 weeks into Phase 4)
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** FC, DC, SC, IO, DB, CM, LC, FS, PS, LM
- **Related:** ADR-0003, ADR-0008 (field dependency split from H), ADR-0023 (mobility), `vocab/crafts.yaml`

## Context

v1 stored one primary and up to two secondary crafts per competency. Craft is collinear with domain (V = 0.82; D2 35/35 DC, D4 35/35 FC), cannot show blends, and the "predicted distribution" used as calibration was circular [E: audit §5]. FC showed that identical tools got different crafts depending on their domain (2.3.2 vs 4.5.4) and that v1's "H arises only from FC/SC" is mostly a coding artifact: field-type tasks under FC parents were coded H 46% of the time, under DC parents 6% [E: FC-029, `scripts/h_artifact_check.py`]. The charter's theory of change is about **blends in people and roles**, which a label cannot carry.

## Decision

### Definitions (v2, L0)

- **Field craft** (FC, P-FC-01, broadened per P-DB-12): *the capacity to perceive, measure, act and stay safe in a specific place — reading land, water, air, living systems and the engineered systems that hold, treat or move them, and producing the ground truth and physical interventions that other environmental work depends on. It is formed through repeated, supervised exposure to real conditions and is evidenced by performance in the field, wherever the practitioner later applies it.* Seven components FC-a…FC-g (perceptual expertise; measurement and sampling integrity; situated judgment and intervention; physical and operational skill; risk management in uncontrolled environments; place knowledge and temporal depth; working with people on the land).
- **Data craft** (DC, P-DC-01): *the disciplined capacity to turn observations of environmental systems into warranted evidence, models and decision support — designing what gets measured, stewarding data so it stays fit for use and properly governed, analysing and modelling with honest uncertainty, and putting results before decision-makers in a form they can act on — including specifying, validating, supervising and answering for AI-generated analysis.* Irreducible contribution: **warrant**. Five functions: Acquire, Steward, Analyze & Model, Integrate & Communicate, Assure & Govern.
- **Statecraft** (SC, P-SC-01): *the learnable capacity to turn knowledge and public purpose into decisions that are authorized, legitimate, resourced and durable, working through law and administrative procedure, institutions, budgets and relationships across jurisdictions and sectors.* Defining deliverable: **a commitment that holds**. Nine components SC1–SC9 are an L0 vocabulary, not nine competencies.

### Tests (rater rubric, `vocab/crafts.yaml`)

- **FC = 2 (defining)** if *presence* (senses or body in the place at the time) **and** at least one of *physical consequence* or *ground-truth authority* hold; **1 (supporting)** where field knowledge catches errors but intermediate performance is possible without it (P-FC-03).
- **DC = 2** if the deliverable is an evidence product, judged by its warrant, and performing it requires choosing or checking methods rather than operating a tool (DC §2.4).
- **SC = 2** if the deliverable is a commitment needing authority, legitimacy or agreement from another institution or the public that must hold over time (SC §2.1).
- A task may have **no craft at 2** ("general professional practice", ADR-0003 G-7). Several crafts may be 2 at once (blend zones: monitoring design, validation of remote/AI outputs, inspection, burn boss vs burn plan approval).

### Representation (stored per rater, per task, as attributed assessments)

1. `craft_rating{FC, DC, SC}` on each **L2 task** as a three-value ordinal **0 / 1 / 2** per craft (FC's recommended first choice), with `confidence` and rater metadata.
2. Two task attributes that are **not** craft weights:
   - `field_dependency` ∈ {on-site-required, on-site-preferred, remote-capable, remote} — must the work happen in place?
   - `formation_dependency` ∈ {yes, partial, no} — must the expertise have been formed through field (or institutional) exposure, even if the task is now done on a screen?
3. **Reproduction-regime attributes** on tasks (P-FC-04): mentorship dependence (L/M/H), cycle dependence (none / seasonal / multi-year or rare-event), place-boundness (general / ecosystem-type / site-specific / **system-specific** for engineered systems, DB), credential gate (none / internal qualification / external certificate / licence), currency decay (L/M/H); **entry-path dependence is computed** from role profiles.
4. **Swappable representation.** The schema's `CraftRating` accepts `scale ∈ {ordinal-0-2, constant-sum-100, nominal-defining}` so the IO pilot outcome can be applied without migration (P-IO-12).
5. **Computed, never stored:** competency blend = mean of linked task ratings weighted by link strength; role blend = task ratings weighted by importance × time share; "dominant craft" is a derived display field only. v1 Craft Primary/Secondary migrate as `prior_evidence` assessments by `v1-analyst-01`.
6. **Elicitation protocol:** raters code **blind to parent competency, domain and v1 craft** (FC §8 Q1, the artifact test); calibrate on v1's ten integration points plus FC's four worked examples; ≥ 3 raters per task for production values; Krippendorff's ordinal α with bootstrap CI, decision on the lower bound (ADR-0024).
7. **Pilot (decides the scale):** IO §7.3 design — 150 tasks (50 per v1 primary craft, ≥ 40% beyond public lands, ≥ 20% boundary cases, ≥ 20% inferred D3) plus 40 competencies, 12 human raters in two crossed groups, frozen LLM arm × 3 runs, formats F1 constant-sum and F2 ordinal ≥ 10 days apart. Pre-registered rules: weights if ICC(2,3) LB ≥ .80 and ≥ ordinal; else ordinal if LB ≥ .667 (tentative); else defining-craft only; competency-level ≥ .10 better → report as evidence for Option A.
8. **Uses:** craft blends **describe** roles and **design** pathways (what kind of learning a gap needs). They are **not** the mobility similarity measure (ADR-0023; P-CM-04) and are not shown about individuals until IO's M-04 reliability threshold is met.

## Rationale and evidence

- Craft varies by task and context within one competency (1.1.5 site vs landscape; riparian buffers; prescribed fire "a defensible 50/50") [E: CA-010, CA-023]; UAS ignition changes the firing task, not the whole prescribed-fire competency [E: FC-002].
- Without `formation_dependency`, screen-based work that depends on field-formed expertise drifts to DC and field craft appears to decline when it is being exercised remotely (FC §8 Q1, disagreement 1). This attribute resolves the FC–DC ownership dispute over AI species verification, ground-truth design and drone processing by moving it "from labels to attributes" — both crafts can be rated 2.
- Coarsening a continuous judgment to three levels lowers α (latent .80 → about .68) [E: IO simulation], so the ordinal is a usability choice (raters can defend "defining vs supporting", not 0.6 vs 0.7) that the pilot must confirm, not a reliability guarantee.
- CM computed that three-dimensional blends cannot separate destinations (31% of family pairs have blend cosine ≥ .95) [E: CM §7 Q1].

## Consequences

- DB's broadening adds engineered-system field judgment (operators, inspectors, lab analysts) to FC; the `system-specific` place-boundness value keeps the outdoor, place-bound sense visible (DB disagreement 1 mitigation).
- Inspection (FC-C04) and work with landowners (FC-C21) can be FC 2 and SC 2 together, ending the FC–SC ownership dispute.
- v1's statistic "Statecraft plurality (42%)" will fall; the Delphi packet must explain why (SC disagreement 7).

## Dissent and trade-offs

- **IO:** the ordinal is not inherently more reliable; only the head-to-head pilot decides (IO disagreement 4). Accepted: status provisional, schema swappable.
- **FC vs DB** on broadening FC to engineered systems: FC's concern is dilution of "judgment earned outdoors"; mitigated by place- vs system-boundness. FC may contest the wording in Phase 4 review.
- **DC:** monitoring design (DC-CAND-03) is DC-primary because the deliverable is a design for inference; FC may rate FC 2 too — the representation allows both.
- **Trade-off named:** rater burden (three ratings plus attributes per task) versus a blend that is real. Mitigation: pre-fill from v1 as prior, re-rate contested tasks and integration points first.
