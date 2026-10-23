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

## CA ruling

- **Ruling:** **accept** (item 1 as DE's interim, now an ADR-0011 amendment; item 2 with `vocab/rules/` as the only home) · **Date:** 2026-10-23 · **Decider:** CA · **Recorded in:** ADR-0011 (amended rules 4–5), ADR-0021 (amendment), ADR-0029 §3–§4, SPEC §14.3, DECISION_LOG `CR-DE-003`

### 1. Stability tier and CLD: the rule 4/5 conflict is resolved

- **The v1 stability tier is not migrated.** ADR-0011 rule 4 is amended to drop "stability tier", and rule 5 now names it. The tier is a stored summary: a documented rule assigns it from the reform flags and Ac tasks, with zero violations (data-audit C05). It can therefore be recomputed from inputs that do migrate, so migrating it would store a summary. It stays readable in `data/v1_baseline/craft_stage_reform.csv` as v1 history. The computed robustness class replaces it (ADR-0008 §6; SPEC §11.7). The WP-02 criterion "no stored summary field migrated" holds.
- **Reform flags migrate as prior evidence**, as rule 4 says, and seed the frozen historical driver events (ADR-0028 §3).
- **The competency-level CLD flag, R9 severity and the S-trajectory flag do migrate as prior evidence** (`data/v2/assessments/emst-v1-cld/`). The reason for treating them differently from the tier: the v1 CLD flag contradicts its own rule in 11 of 222 competencies (data-audit). It is therefore not a pure function of migrated inputs. It records the analyst's judgment, and that judgment is the context of the R9 severity prior the codebook keeps ("v1 R9 severity as expert overlay prior"). It is never a v2 value, never displayed, and never an input to the computed CLD, which is recomputed at role and pathway level (ADR-0008 §6).

### 2. Computed-view rules: `vocab/rules/` is the one home

- **Accepted: `vocab/rules/<rule-id>@<version>.yaml`** (SPEC §14.3, ADR-0021). `schema/rules/` is **rejected**. A computed-view rule is a reviewed definition of what EMST publishes, not schema structure. Each rule change is a change record the CA (later the TSC) reviews, and the rule files sit in the same reviewed lane as the vocabularies they compute over.
- **The CA has created the rule files.** Their text was read from `scripts/build_release.py` and the CRs.

| File | Status |
|---|---|
| `counts@1.0.0` | as implemented |
| `inverse-links@1.0.0` | as implemented; superseded by 1.1.0 |
| `inverse-links@1.1.0` | adds `Task.tools` and `Competency.enactments` (CR-DE-001 #8–9) |
| `assessment-staleness@1.0.0` | as implemented, plus the competency-level hash case |
| `effective-use-tier@0.1.0` | interim, as implemented |
| `effective-use-tier@1.0.0` | target: evidence cap and level-rule cap (CR-IO-001) |
| `change-indicator@1.0.0` | ported from LM's `evidence_rule.py` (CR-LM-001 #3) |
| `display-gate@1.0.0` | CR-IO-002; parameters in `validation/display_gates.yaml`, pinned by path and SHA-256 |

- **Division of work.** The rule file is the normative definition. The code stays in `scripts/` (DE lane), and IO's display gate stays in `validation/` (IO lane). A rule file may delegate thresholds to a stewarded parameter file pinned by path and SHA-256. DE proposes rule text or new versions through a CR or a PR touching only `vocab/rules/`, and the CA merges it. CI checks two things: every `ruleId`/`ruleVersion` stamped in a view has a rule file, and every rule file's `implementation` path exists.
