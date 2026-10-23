# CR-LC-001: Pathway records before role records, typed formation provisions, CLO identifiers, and an employer-mandated credential gate

- **From:** LC (A8 with IO), WP-07 · **To:** CA (decider); DE (validator, schema); FH (WP-08 role records); IO (CLO and X10 validation) · **Date:** 2026-10-23 · **Type:** X (structural; schema and vocabulary) and C (process) · **SemVer impact:** minor (new optional fields and one vocabulary term)
- **Affects:** SPEC §5.10 `Pathway`, §5.19 `Credential`, §12.3 derived identifiers; `vocab/authority_positions.yaml#closure_types`; `scripts/validate_v2.py` planned targets; ADR-0026 §1, §4, §6; ADR-0022 X10
- **Evidence label:** J (LC; each gap was found by authoring the WP-07 records against schema 2.0.0-draft.1 and the rulings in `RULINGS_FOR_DE.md`)

## Problems and what WP-07 did meanwhile

1. **Pathways cannot enter `data/v2/` before WP-08's role records.** `Pathway.fromVariant`/`toVariant` must resolve to a `RoleProfile` or `RoleVariant`; none exist until S2, so each pathway would fail `E-REF-DANGLING`. The role keys themselves are now settled (CR-IA-001 ruling: `seed:<role_key>`, `seed:<role_key>/<sector_actor>[/<slice>]`).
   *Interim:* the 11 P1-corridor pathways are written schema-valid (checked with the generated schema) to `docs/build/WP-07/staging/pathways/` by `docs/build/WP-07/scripts/build_wp07_pathways.py`, using `seed:<role_key>` RoleProfile references. Moving them is mechanical once the roles exist.
2. **Formation provisions have no typed home.** ADR-0026 R7 requires, per formation task, observed work-based learning, a validation drill, or a by-hand quota of unaided products before review-and-certify credit, plus a supervisor plan and mentor. `Pathway.sequence[]` allows only `step`, `tasks`, `outcomes`, `roleLevel`, `note`. ADR-0026 §4 also says pathways are "pinned to EMST versions", but there is no pin field.
   *Interim:* provisions are written into each step's `note` and, machine-readably, into `docs/build/WP-07/formation_provisions.csv` (35 rows, generated).
3. **CLOs have no identifier.** ADR-0026 §1 makes the CLO the set of indicators at one level, with persistent IRIs on the indicators. Credential alignment (Open Badges 3.0 / CLR 2.0), the X10 register and pathway outcomes all need to name "competency C at level Lx" as one target.
   *Interim:* X10 rows (`data/v2/crosswalks/emst-x10-evidence-equivalence/2.0.0-draft.sssom.tsv`) use the competency as `object_id` and put the level in `other` as `clo_level=Lx`; pathway `outcomes` list the indicator IDs the builder resolves at build time.
4. **Which indicators make up a CLO?** At some levels, enactment-specific indicators (for example the FC, DC and SC enactment indicators of `seed:DC-CAND-13` at L2) sit beside the generic ones and all point at the same competency and level. A pathway or bundle that takes "all indicators at L2" then requires field-craft anchors of a statecraft learner.
   *Interim:* pathways include every indicator at the level and say so; WP-12 views should filter by enactment once the rule exists.
5. **No closure type for employer- or policy-mandated credentials.** `closure_types` offers `legal-licensure`, `regulation-mandated-training` and `voluntary` ("not legally required; employer or market preference"). Wildland fire position qualifications, federal contracting-officer's-representative certification, incident-command training and many state inspector credentials are mandatory for the assignment by agency or interagency policy, but are not required by statute or regulation. Calling them `voluntary` is accurate to the definition but misleads HR users.
   *Interim:* those register rows use `voluntary` with an editorial note (`data/v2/registers/credentials/`).
6. **LC-PW-06 (AI and data-practice baseline) is not a role delta.** ADR-0026 §4 puts it first, but it has no from/to role. WP-07 did not author it as a Pathway. It is a natural first **Bundle** (computed view; TX-A floor CLOs at L1 plus TX-D formation design for supervisors).

## Proposed change

1. **Validator (DE):** treat references that match the CR-IA-001 role-key forms and whose `<role_key>` is in `docs/decisions/mvp_role_set.csv` as planned targets (`W-REF-PENDING`, error under `--strict`), so pathways can live in `data/v2/core/pathways/` from S1. If the CA prefers the staging route, WP-07 moves the files when WP-08's records land.
2. **Schema (DE/IA):** add to `Pathway`:
   - `emstRelease` (SemVer; required at `candidate`);
   - `sequence[].formationProvisions[]` = `{task (RecordRef), response ∈ {observed-wbl, supervised-repetitions, validation-drill, by-hand-quota}, quota {count (integer), unit (Text)}, releaseCriterion (Text), mentorRequired (boolean)}`, with the response values in a vocabulary (`vocab/friction_types.yaml#formation_responses`, beside `pathway_types`).
   The computed `formationCoverage` (SPEC §5.10) would then read these instead of free text.
3. **Identifiers (CA, SPEC §12.3):** define a derived CLO IRI, `<competency IRI>/levels/<Lx>` (for example `https://w3id.org/emst/core/CMP-XXXXXXX/levels/L2`), resolvable in the release bundle to the indicator set, for badge alignment and as the X10 object. Until minting, `seed:` keys keep the `other: clo_level=Lx` convention.
4. **Rule (CA with IO and DC):** decide whether enactment-specific indicators are part of the generic CLO, or belong to the enactment (`Enactment.indicatorVariants`) and are excluded from the generic CLO. LC recommends the second: the CLO is the craft-neutral anchor set, and an enactment adds its anchors only for learners in that enactment.
5. **Vocabulary (CA):** add `{notation: employer-mandated, definition: "Required for the assignment by employer, agency or interagency policy, but not by statute or regulation."}` to `closure_types`; WP-07 then re-codes the affected register rows.
6. **ADR-0026 §4 wording (CA):** record LC-PW-06 as the first computed Bundle (TX-A floor) rather than a Pathway, and LC-PW-01 as `seed:lc-pw-cor3-compliance-inspector-onboarding` (state inspector variant).

## Consequences if not accepted

Pathways stay outside `data/v2/` until S2; formation provisions stay in free text and a sidecar file that CI cannot check; credential alignment targets an indicator list rather than one stable CLO address; HR users see policy-mandated qualifications labelled "voluntary".

## CA ruling

- **Ruling:** **accept 1–6, with changes to 2 and 3** · **Date:** 2026-10-23 · **Decider:** CA · **Recorded in:** ADR-0030 §1.5, ADR-0026 and ADR-0022 (amendments), SPEC §5.3, §5.10, §5.19, §12.3 (draft.3), `vocab/authority_positions.yaml#closure_types`, `vocab/friction_types.yaml#formation_responses`, `vocab/identifiers.yaml#form.clo_iri`, DECISION_LOG `CR-LC-001`
- **Implementation:** DE per `RULINGS_FOR_DE.md` §17; LC (A8) data moves in S2 as listed.

1. **Planned role references: accepted, with a hold condition.** A reference is a planned target (`W-REF-PENDING`; error under `--strict`) when all three hold:
   - it matches the CR-IA-001 forms `seed:<role_key>` or `seed:<role_key>/<sector_actor>[/<slice>]`;
   - `<role_key>` is in `docs/decisions/mvp_role_set.csv`;
   - `<sector_actor>` is a `vocab/sector_actors.yaml` notation.

   A planned reference to a Tribal sector actor or subtype is held: the referencing record must carry the hold flags, otherwise `E-TRIBAL-INHERIT`. The same planned-target treatment extends to `seed:<cand_id>` for `candidate_disposition.csv` rows decided `core-v2.0` or `module-v2.0` (held keys count as held), so enactments can name planned core targets such as DB-C42 and PS-C15. **LC (A8)** moves the 11 staged pathways into `data/v2/core/pathways/` in S2, once DE has landed this item and item 2. It does not wait for WP-08.
2. **Typed formation provisions: accepted, with changes.**
   - `Pathway.emstRelease` (SemVer of the release the pathway is pinned to) is required from `candidate` on.
   - `sequence[].formationProvisions[]` items are `{task, responses[], quota?, releaseCriterion, mentorRequired}`.
   - **Change:** `responses[]` is an array (minItems 1) of `vocab/friction_types.yaml#formation_responses` values (`observed-wbl`, `supervised-repetitions`, `validation-drill`, `by-hand-quota`), because four WP-07 rows combine two responses.
   - `quota {count (integer ≥ 1), unit}` is optional, and required when `responses` contains `by-hand-quota` or `supervised-repetitions`.
   - The provision's `task` must be one of the step's `tasks` (`E-PROVISION-TASK`).
   - `formationCoverage` (computed) reads these, never free text. `formation_provisions.csv` stays WP-07's generated audit copy only.
3. **CLO identifiers: accepted, with a change.**
   - The derived CLO IRI is `<competency IRI>/levels/<Lx>`, e.g. `https://w3id.org/emst/core/CMP-XXXXXXX/levels/L2`; the compact form is `emst:core/CMP-XXXXXXX/levels/L2`. An enactment's CLO is `<enactment IRI>/levels/<Lx>`.
   - It is derived like the CASE, CTID and RSD identifiers. It is never minted, never in the ID registry, and resolves in the release bundle to a node `{competency, level, indicators[]}`. Badge alignment (Open Badges 3.0 `alignment.targetUrl`, CLR 2.0) and the X10 object use it.
   - Until minting, X10 keeps `object_id = <competency seed key>` with `other: clo_level=Lx` (ratified).
   - **Change:** pathways name CLOs as `{competency, level}` in new `Pathway.cloOutcomes[]` and `sequence[].cloOutcomes[]` fields, not as lists of every indicator at a level. `outcomes[]` stays for naming specific indicators. **LC** converts the staged pathways' "all indicators at Lx" outcomes to `cloOutcomes` when moving them.
4. **CLO composition: LC's recommendation adopted.**
   - The generic CLO is the indicators listed in `Competency.levels[Lx].indicators`, which are craft-neutral.
   - Indicators listed in an `Enactment.indicatorVariants[]` are never part of the generic CLO. The enactment's CLO is the generic CLO plus its variants at that level.
   - An indicator listed in both places is `E-CLO-ENACTMENT-INDICATOR`.
   - WP-12 filters by enactment. Learners in other enactments are never asked for another enactment's anchors.
5. **`employer-mandated` closure type: accepted.** The CA has added `{notation: employer-mandated, definition: "Required for the assignment by employer, agency or interagency policy, but not by statute or regulation."}` to `closure_types`; DE regenerates `v_closureType`. **LC (A8)** re-codes the affected register rows in S2: wildland-fire position qualifications, contracting-officer's-representative certification, incident-command training and the state inspector credentials required by agency policy. Each re-coded row keeps its issuer and verification status, and its `legalBasis` names the policy.
6. **ADR-0026 §4: amended as proposed.** LC-PW-06 (AI and data-practice baseline) is the first computed **Bundle** (TX-A floor CLOs at L1, plus TX-D formation design for supervisors), not a Pathway. LC-PW-01 is `seed:lc-pw-cor3-compliance-inspector-onboarding` (state inspector variant).
