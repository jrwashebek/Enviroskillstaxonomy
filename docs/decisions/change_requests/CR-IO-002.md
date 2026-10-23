# CR-IO-002: Display-gate semantics: unmeasured values, admissible studies, editorial fields and strata

- **From:** IO (A8), WP-11 · **To:** CA (decider); CP (WP-12) and DE (WP-01) as implementers · **Date:** 2026-10-23 · **Type:** C/X (clarifies ADR-0024 §4, ADR-0017 status line, SPEC §10.5) · **SemVer impact:** patch (clarification) unless CA changes a threshold
- **Affects:** `validation/display_gates.yaml`, `validation/display_gate.py`; SPEC §10.5; `vocab/lifecycle_states.yaml#reliability_gate`
- **Evidence label:** J

## Questions the ADRs leave open, and IO's encoded answers (for confirmation)

1. **Unmeasured equals not shown.** SPEC §10.5 says tags shown need α lower bound ≥ .667; ADR-0017 says values with α < .667 are not shown. Neither says what happens before any study.
   - *Encoded:* no admissible study → not rendered, label "Assessment pending". This matches ADR-0027's "assessment pending" rule for View 1.
2. **What counts as a study.** *Encoded:*
   - human rater types only (`expert-panel`, `sme`, `analyst`);
   - ≥ 120 units (ADR-0024 §4 study size for decisions);
   - ≥ 3 distinct raters, ≥ 2 pairable values per counted unit;
   - unit bootstrap with ≥ 10,000 resamples, decided on the 2.5th percentile;
   - pre-registered, blind (XR-01);
   - same codebook version as the values;
   - lapses after 36 months.
   - Any `llm`, `external-index` or `v1-analyst` rater in the counted set makes the result inadmissible.
3. **Editorial definitions are not ratings.** *Encoded:* these are not α-gated, but are labelled "editorial":
   - RoleProfile.primaryWorkFunction;
   - RoleVariant.sectorActor;
   - RoleVariant.authorityPosition;
   - Competency.homeModule;
   - Competency.competencyType;
   - Task.supports.
   What is gated is the assignment of *external units* (postings, PDs, state classes) to authority positions, and all task-level ratings, including Task.workFunction.
   - Verified facts (credential gates, sign-off authority, accountability constraint) need sources, not α.
   - IO asks CA to confirm this list. Without it, hiding the work function of every role would empty View 1.
4. **Strata.** *Encoded:* a module or sector-actor stratum with ≥ 30 study units needs its own lower bound ≥ .667 for values in that stratum to render (XR-07 intent).
5. **Weak categories.** *Encoded:* a category whose one-vs-rest point α < .50 (≥ 10 units) caps its values at `tentative`.
6. **Production values** need a ≥ 3-human-rater consensus; tentative values need ≥ 2 agreeing human codes or an adjudication.
7. **Select views** admit production-marked tags only.

## Request

Confirm or amend items 1–7 and record the decision in DECISION_LOG. Then:
- CP renders only through `display_gate.decide()` (or an equivalent that passes `validation/tests/test_display_gates.py`);
- DE emits agreement results in `display_gates.yaml#agreement_result_schema` to `dist/views/agreement/`.

## CA ruling

- **Ruling:** **confirm items 1–7, with three clarifications** · **Date:** 2026-10-23 · **Decider:** CA · **Recorded in:** ADR-0024 and ADR-0017 (amendments), ADR-0029 §6, SPEC §10.5, `vocab/rules/display-gate@1.0.0.yaml`, DECISION_LOG `CR-IO-002`

1. **Unmeasured means not shown: confirmed.** With no admissible study, a value is not rendered and the view shows "Assessment pending". This is ADR-0027's rule for View 1.
2. **Admissible study: confirmed** as encoded:
   - human rater types only;
   - ≥ 120 units;
   - ≥ 3 distinct raters;
   - ≥ 2 pairable values per counted unit;
   - unit bootstrap of ≥ 10,000 resamples, decided on the 2.5th percentile;
   - pre-registered and blind;
   - same codebook version as the values;
   - lapses after 36 months.

   *Clarifications:* (a) ≥ 3 raters is the admissibility floor. The design target stays 120–200 units × 6 raters (ADR-0024 §4), and deciding on the lower bound already penalizes thin studies. (b) An `llm`, `external-index` or `v1-analyst` rater in the counted set makes the study inadmissible. An LLM coder can become admissible only after it passes `validation/protocol_llm_coder_gate.md` **and** a reviewed change record amends `display_gates.yaml`. It is never admissible by default and never for `select` values (ADR-0024 §5).
3. **Editorial fields: confirmed, with additions and one consequence made explicit.**
   - Editorial: RoleProfile.primaryWorkFunction, RoleVariant.sectorActor, RoleVariant.authorityPosition, Competency.homeModule, Competency.competencyType and Task.supports are labelled "editorial" and not α-gated. The CA adds three equally definitional fields: RoleVariant.sectorActorSubtype, Enactment.actorType and Competency.transversalCluster.
   - Gated: the assignment of external units (postings, PDs, state classes) to authority positions, and every task-level rating, **including Task.workFunction**. ADR-0017's status line ("values with α < .667 are not shown") governs it.
   - Consequence: until a study reports, views navigate by the editorial RoleProfile.primaryWorkFunction and show task work function as "Assessment pending". The value stays in the source records and in the release bundle with its `validationStatus`, because a data download is not a display. IO puts work function first in the first reliability study.
   - Verified facts (credential gates, sign-off authority, accountability constraint) need E-labelled sources, not α. Without a source they are not shown.
4. **Strata: confirmed.** A module or sector-actor stratum with ≥ 30 study units needs its own lower bound ≥ .667 before its values render.
5. **Weak categories: confirmed.** A category with one-vs-rest point α < .50 (on ≥ 10 units) caps its values at `tentative`.
6. **Production and tentative values: confirmed.** Production needs a consensus of ≥ 3 human raters. Tentative needs ≥ 2 agreeing human codes or an adjudication (consistent with SPEC §7.2).
7. **Select views: confirmed.** They admit production-marked tags only.

**Then (both accepted):**
- CP renders gated values only through `validation/display_gate.py::decide()`, or an equivalent that passes `validation/tests/test_display_gates.py`.
- DE emits agreement results in `display_gates.yaml#agreement_result_schema` to `dist/views/agreement/`.
- The gate is registered as `vocab/rules/display-gate@1.0.0.yaml`, with its parameters pinned to `validation/display_gates.yaml` by path and SHA-256. Changing any threshold is a change record (type X) the CA reviews.
