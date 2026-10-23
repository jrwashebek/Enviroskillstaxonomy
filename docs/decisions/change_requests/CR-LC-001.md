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
