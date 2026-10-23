# WP-03 authoring prompt (frozen) — `wp03-authoring@1`

Owner: FC (A3) · Model: `claude-opus-5-5` · Frozen: 2026-10-23 · Licence: CC0-1.0

This is the instruction set the FC agent followed when drafting WP-03 competency, task, indicator and enactment
records. Records cite it as `provenance.promptVersion: wp03-authoring@1`.

1. Build from the decisions: ADR-0003 (T-1..T-8, G-1..G-9), ADR-0004, ADR-0005, ADR-0025, `vocab/crafts.yaml`,
   `vocab/proficiency_levels.yaml`, `vocab/work_functions.yaml`, `docs/standard/AUTHORING_GUIDE.md`, the WP-03
   section of `docs/decisions/PHASE4_BUILD_PLAN.md`, and FC Phase 2 research (`docs/research/field-craft/`).
2. Competencies: function-based title (verb + object + context), no product, platform, vendor or named instrument;
   SKOS definition stating what is covered and excluded; statement of at most 60 words; level span limited to the
   levels where the practice is performed (default L1-L3 for field technique; L4 only where the work sets methods,
   certifies others or designs programmes; L5 never asserted without SME confirmation).
3. Tasks: one imperative verb, object, condition or purpose; 8-30 words; no compound verbs. Split execution to
   protocol from adaptation in place, and production from specification, review and defence, wherever both exist
   (G-2). Record workFunction, fieldDependency, formationDependency and the reproduction-regime attributes as the
   author's draft judgment. Credentials are gates, never proficiency (T-8).
4. Indicators: 2-5 per published level; one sentence of at most 30 words; observable verb + object + condition +
   standard; none of the twelve banned constructions; augmentationMode, assessmentMethods, useClass (describe or
   develop, never select), obs4, jurisdictionVariable, distinguishingAttribute (level above L1 or above span min).
   Reward justified refusal and correct expressions of uncertainty; test outcomes against an independent reference
   where one exists (FC report §5.2).
5. Everything is draft evidence: status draft, validationStatus draft, provenance.method llm-assisted, reviewStatus
   unreviewed, evidence label J (basis in editorialNote) unless sources are cited.
6. No Tribal content outside the hold; actor-neutral text; no personal data; synthetic examples only.
