# ADR-0029: Phase 4 integration rulings on the S0–S1 build change requests

- **Decision point:** DP-28 (new; CA as Phase 4 integrator): schema and vocabulary corrections found while implementing the SPEC
- **Status:** accepted
- **Date:** 2026-10-23 · **Decider:** CA
- **Change requests ruled:** CR-DE-001, CR-DE-002, CR-DE-003 (DE, WP-01/02); CR-IO-001, CR-IO-002, CR-IO-003 (IO, WP-11); CR-LM-001, CR-LM-002, CR-LM-003 (LM with FS, WP-10); CR-IA-001, CR-IA-002 (IA, WP-09; these arrived during the session). Each full ruling is in its CR file under "CA ruling".
- **Amends:** ADR-0004, ADR-0007 (status only), ADR-0008, ADR-0010, ADR-0011, ADR-0013, ADR-0017, ADR-0021, ADR-0022, ADR-0024, ADR-0027, ADR-0028, the Phase 4 build plan (WP-09 acceptance, WP-10 lane), `mvp_role_set.csv` (errata), SPEC (now 2.0.0-draft.2) and `vocab/` (13 of 19 files, plus the new `vocab/rules/`)
- **Implementation:** DE, as listed in `change_requests/RULINGS_FOR_DE.md`. IO and LM changes are listed in their CR rulings.

## Context

Implementing SPEC 2.0.0-draft.1 as a closed JSON Schema exposed five kinds of problem:
- field-name clashes and unstated paths;
- code lists that lived only in the schema;
- a conflict inside ADR-0011;
- publication and display rules that could not yet be checked by machine;
- fields that the ADR-0028 evidence rule and the external-index ingest need.

The build agents chose reversible interim encodings and filed CRs, as ADR-0009 and the build plan (§1.1) require. No persistent ID has been minted, so every correction is still a schema rebuild, not a MAJOR change.

## Decision

| § | CR | Ruling | Effect |
|---|---|---|---|
| 1 | CR-DE-001 | accept with changes | `signalStatus`/`seriesStatus`/`sourceStatus`; `prefLabel` not `title`; base-array `notation` on VocabularyTerm; `mint_id.py` the one writer; instrument registry path; `definition` MUST on authored L0/L1/L3 records; seed-v1 exemption, with no `candidate` while seed-v1; `Task.tools[]` **and `Competency.enactments[]`** become computed inverses (the second is a change from DE's proposal); schema-local enumerations move into the **existing** vocabulary files; DE's extra fields are **ratified** (`v1Seed` stripped from every release; `v1Values`; `sWatch`; `tacitExperienceRequirement`; v1-only competency-subject ratings; IO indicator metadata; `transversalCluster`; `reviewBy`; `/` in seed keys) |
| 2 | CR-DE-002 | accept 1–4, reject 5 | ID prefixes `WCH`, `SER`, `SCR`; X12 registered; `'yes'`/`'no'` quoted; machine values for `supervisory_status` and `appointment_route`; no "recovered" flag (provenance already records it) |
| 3 | CR-DE-003 (1) | accept | **The v1 stability tier is not migrated.** ADR-0011 rule 4 drops it and rule 5 names it. It is a pure function of migrated inputs (zero violations, C05), so storing it would store a summary. The competency-level CLD flag, R9 severity and S-trajectory flag do migrate, as prior evidence only: the v1 CLD flag contradicts its own rule in 11 of 222 competencies, so it carries analyst judgment, which is the context of the R9 severity prior |
| 4 | CR-DE-003 (2) | accept | `vocab/rules/<rule-id>@<version>.yaml` is the only home for computed-view rules (`schema/rules/` rejected). The CA registered `counts`, `inverse-links` (1.0.0, 1.1.0), `assessment-staleness`, `effective-use-tier` (0.1.0 interim, 1.0.0 target), `change-indicator@1.0.0` and `display-gate@1.0.0`. Code stays in `scripts/` and `validation/`; parameters may live in a stewarded file pinned by path and SHA-256 |
| 5 | CR-IO-001 | accept with changes | publication-rule checks are `pass \| fail \| pending \| not-applicable`; evidence MUST accompany `pass` on PR-1 and PR-4 (PUB-14); `distinguishingAttribute` is required above the lowest level that has indicators; IO's tier mapping is **ratified**, so rc.1 levels are describe-grade until a Delphi runs; waiver register at `data/v2/governance/lint_waivers.csv` |
| 6 | CR-IO-002 | confirm 1–7 with clarifications | unmeasured = "Assessment pending"; admissible-study definition (human raters; ≥ 3 raters is a floor, 6 remains the target); editorial-field list extended by three definitional fields; **Task.workFunction is gated**, so views navigate by the editorial role function until a study reports; strata, weak-category, production and select rules confirmed |
| 7 | CR-IO-003 | accept | `ordinal_order: [E0, E2, E1, E3]`, codes kept; scenario rows apply at E1, E2 or E3 |
| 8 | CR-LM-001 | accept with changes | typed `signalFamily` (`counts_toward`; policy counts for role-change only; projection and workload never count), `independenceKey` (a slug, with a provider table in `vocab/change_types.yaml`; must be listed once a signal is active), `registeredDeployment`, `impact`, signposts `SP-01…SP-12` (SP-12 Tribal Council only), `pointsToward`, measure baseline and sensitivity; `EMST-*` notation entries forbidden from `candidate` on; **no occupation target** (attach through X3); **organization target** for government employers only, never Tribal; `statusAfter`, `submitted-for-review`, `agency-order` added; evidence rule ported to `scripts/` and `tests/` |
| 9 | CR-LM-002 | accept with changes | external-index records at occupation→role grain, with role target and crosswalk path; `levelDistribution` with `basis`, or index values only; partial dates; licence held out of every bundle until the index's terms are verified; context-only display, with broad-match values in the evidence drawer only |
| 10 | CR-LM-003 | accept | WP-10 lane ratified (signals, instruments, events, watch items, external assessments, `docs/methods/`); the builder stays an LM authoring tool that CI never runs |
| 11 | CR-IA-001 | accept with one wording change | role seed keys `seed:<role_key>`, variant seed keys `seed:<role_key>/<sector_actor>[/<slice>]`; `mvp_role_set.csv` errata applied, checked against V1-10 (0408, 0482 and 0486 are **not** proposed for realignment; 0410 is; R19 is O*NET 19-1031.00) |
| 12 | CR-IA-002 | accept; item 4 optional | SSSOM 1.0 plus the 1.1 justification `semapv:LLMBasedMatching` as a declared extension for unreviewed agent rows; reviewed rows take `MappingReview` and keep `original_justification` in `other`; an optional strict-1.0 export rendering |

### Rules that bind every lane from now on

1. **Vocabulary writers quote `yes`/`no`/`on`/`off`/`y`/`n` codes.** All 19 files were checked with a YAML 1.1 loader.
2. **No stored inverse links:** `Task.tools[]` and `Competency.enactments[]` are forbidden in source records, alongside the existing computed fields.
3. **A rule change is a change record.** Views stamp `ruleId`/`ruleVersion`; CI fails on a stamp with no rule file.
4. **Authoring tools stay in their owner's lane and are never invoked by CI or the release build.** Code that CI or the build runs lives in `scripts/` with tests in `tests/`.

## Rationale

- Each ruling follows the SPEC wherever the SPEC was implementable. It corrects the SPEC where implementing it exposed a defect, such as a name clash, a second copy of a link, or an untestable rule.
- Where a CR's proposal would have left two places for one fact (stored inverse enactments, a "recovered" flag) or broken an invariant (new vocab files would break the generator rule that every vocab file generates an enumeration), the CA chose the single-place alternative.
- The stability-tier and CLD rulings rest on a reproducibility test. A v1 value that its documented rule fully determines is a summary and does not migrate. A v1 value that departs from its rule carries judgment and migrates as prior evidence.

## Consequences

- SPEC 2.0.0-draft.2. Schema 2.0.0-draft.2 after DE's rebuild. `python3 scripts/build_schema.py --check` reports STALE (`EmstId`, `StateClassFields`, `v_idTypePrefix`, `v_mappingSetId`) until DE regenerates and wires the new vocabulary keys. Data validation is unaffected meanwhile.
- No record changes meaning. LM migrates its interim notation encodings and re-targets organization signals; IO moves its waiver default path and adds PUB-14.
- Q11 (a lead-signed invitation to inter-Tribal organizations to help form a Tribal Advisory Council) is added to `questions_for_project_lead.md`. Its safe default is that no invitation is drafted for sending.

## Dissent and trade-offs

- **DE:** an enumeration in an existing file is less discoverable than a dedicated `l5_registry.yaml`. Accepted cost: each list carries a comment naming its schema field, and moving lists into new files can be revisited at the next schema MINOR together with the generator test.
- **IO:** gating Task.workFunction thins View 1 until the first reliability study. The CA accepts that over showing an unmeasured classification as fact (ADR-0017).
- **LM:** listing every active independence key is extra stewardship. It is the only way "no single vendor" can be enforced rather than assumed.
