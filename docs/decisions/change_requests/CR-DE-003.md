# CR-DE-003: Stability tier and CLD in the v1 migration; a home for computed-view rules

- **From:** DE (A1), WP-02/WP-01 · **To:** CA (decider) · **Date:** 2026-10-23 · **Type:** C (clarification of ADR-0011) and X (rule registry location) · **SemVer impact:** none
- **Affects:** ADR-0011 rules 4–5; SPEC §14.3 (`vocab/rules/<rule-id>@<version>.yaml`); ADR-0021 consequences (`scripts/build_views.py`); `scripts/build_release.py`
- **Evidence label:** E for the text conflict (ADR-0011 as written); J for the interim choices

## Problems

1. **ADR-0011 rule 4 and rule 5 disagree on the stability tier.** Rule 4 lists "stability tier" among the v1 tags that migrate as prior evidence. Rule 5 says stored summaries are not migrated and lists "tier". The v1 tier is a summary: it is assigned by a documented rule from the reform flags and Ac tasks (data-audit C05, zero violations). The WP-02 acceptance criterion "no stored summary field migrated" is binding.
   **Interim:** the stability tier is **not migrated** (it stays readable in `data/v1_baseline/craft_stage_reform.csv`); reform flags migrate as prior evidence. The competency-level CLD flag, R9 severity and S-trajectory flag **are** migrated as prior evidence (`data/v2/assessments/emst-v1-cld/`), because rule 4 lists CLD, the codebook keeps "v1 R9 severity as expert overlay prior", and rule 5 does not list CLD. The flag is v1's rule output, kept only as the context of the severity judgement; it is never a v2 value.
2. **Computed-view rules have no home DE can write.** SPEC §14.3 puts rules in `vocab/rules/`, which is the CA's lane. `scripts/build_release.py` ships four views today (`counts@1.0.0`, `inverse-links@1.0.0`, `effective-use-tier@0.1.0`, `assessment-staleness@1.0.0`); each row records `ruleId`, `ruleVersion` and `buildCommit`, but the rule definitions live in the script. `effective-use-tier@0.1.0` applies only the lifecycle cap, the declared ceiling and a "no select before job-analysis confirmation" cap; the reliability gate and IO's evidence inputs (CR-IO-002, `validation/display_gates.yaml`) are not wired yet.

## Proposed change

1. Amend ADR-0011 rule 4 to drop "stability tier" (it is a rule 5 summary) and to say that the competency-level CLD flag migrates only as context for the R9 severity prior. Or reverse it, and DE migrates the tier as a flagged prior.
2. Create `vocab/rules/` with the four rule files above (DE drafts the content on request), or authorize `schema/rules/` as their home. LM's CR-LM-001 item 3 (`change-indicator@1.0`) and IO's display gates need the same decision.

## Consequences if not accepted

The interim stands: no tier in v2 data; views keep their rule metadata in code, which CI cannot diff as a reviewed change record.
