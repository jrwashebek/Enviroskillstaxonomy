# Protocol: Admitting LLM-assisted coding (the LLM-coder gate, LLM)

**WP-11 output 9** · Owner: IO (A8), with IA (pipeline, gold-set tooling, drift) and DE (provenance, CI) · Status: draft protocol for CA approval · Date: 2026-10-23
**Decision basis:** ADR-0024 §5 (P-IO-11); SPEC §13.1–13.2 (`toolVersion`, `promptVersion`; LLM-assisted content passes IO's gate before it can carry a selection-relevant value); `vocab/evidence_labels.yaml#rater_types` (`llm`: "frozen LLM coder behind IO's gate; never sole coder of selection-relevant values"); ADR-0019 (linker gold sets); PHASE4_BUILD_PLAN §1 rule 2.
**Companion files:** `validation/spec_gold_sets.md`, `validation/display_gates.yaml#value_rules.agent_values`, `validation/reliability.py`.
**Labels:** [E] evidence, [J] judgment, [S] speculation.

---

## 1. Principle

An LLM is a **coder to be validated, not an oracle**. It may code an EMST dimension only after it has been measured against humans on held-out data under this protocol, for:
- a specific dimension;
- a specific codebook version;
- a frozen model version and prompt.
Its output stays **draft evidence** (`raterType = llm`, `validationStatus = draft`, evidence label **S**) until a human verifies it. It never becomes "human agreement".

v1 shows why. It decided that an AI-augmented single analyst needed no reliability provisions, and its own record noted that the AI "will confidently resolve ambiguous cases without flagging them as ambiguous" [E: IO-009]. In Phase 2, a rule-based coder written while looking at the sample agreed with manual codes at κ = .79 in sample, but κ = .69 on held-out statements [E: `docs/research/io-validation/analysis/observability_summary.json`]. Agreement measured on tuning data overstates real performance.

### 1.1 What Phase 4 agent output is, and is not

Phase 4 WPs produce craft ratings "from three independent agent passes recorded as `llm` raters", plus draft tags and draft indicators. Under this protocol:
- Three passes of agents built on one model family are **one rater type**. Their agreement is **run-to-run consistency**. No document may call it inter-rater reliability, SME agreement, Delphi retention or job-analysis confirmation.
- The passes may serve as **pre-fills** and **sampling strata** for human studies. They are never shown to human raters during a reliability study (XR-01), and are never pooled into any gate statistic.
- They do not enter gold sets as labels.

## 2. Gate levels

| Level | Permission | Conditions (all must hold) |
|---|---|---|
| **G0 Not admitted** | LLM output may be stored as draft evidence only; never rendered; never a pre-fill shown to raters during studies | default |
| **G1 First coder with human verification** | LLM codes first; a qualified human verifies every value before it counts as a human value (decision path recorded) | §4.1 non-inferiority **and** α(LLM, gold) lower bound ≥ .667 **and** run-to-run α ≥ .80 **and** calibration acceptable (§4.3) **and** automation-bias safeguards in force (§5) |
| **G2 Sole coder for a descriptive dimension** | LLM value may stand without per-value human verification, for **descriptive, non-selection** dimensions only, and still renders only if the dimension's human α passes the display gate | G1 conditions **and** α(LLM, gold) lower bound ≥ .80 **and** blind audit stream shows no drift for two consecutive audit cycles **and** CA approval recorded |
| **Never** | LLM as sole coder of any value that feeds selection, promotion, qualification, a published workforce statistic, a protect decision, or anything touching held content | always (ADR-0024 §5) |

Dimensions that can **never** reach G2:
- indicator OBS-4 coding for `useClass = select`;
- level placement;
- relevance ratings used in role profiles marked `criticalForSelection`;
- task criticality and needed-at-entry flags;
- staffing outcomes;
- anything with `governedData = tribal`.

## 3. Pre-conditions (freeze and log)

1. **Frozen configuration.** The following are hashed and stored with every LLM-produced value (DE/IA; SPEC §13.1 `toolVersion`, `promptVersion`):
   - model identifier and version;
   - system prompt and codebook text;
   - decoding settings (temperature, sampling);
   - retrieval context;
   - output schema.
   Any change creates a new configuration that must pass the gate again.
2. **Development vs evaluation separation.** Prompts are tuned **only** on the gold set's development split (`spec_gold_sets.md` §5). The held-out evaluation split is never seen by anyone who tunes prompts. It is stored outside the public repo until the evaluation is run (contamination control, §6.3).
3. **Blindness.** Prompts never contain the parent competency, domain, craft, v1 codes or other raters' values (XR-01). A CI check rejects prompt templates containing those fields.
4. **Abstention.** The output schema must allow `ambiguous`/`abstain` with a rationale, and a confidence value.

## 4. Measurement against humans (held-out gold)

### 4.1 Comparison design

- **Gold labels.** For each held-out unit: ≥ 2 independent blind human codes plus adjudication by a third human (`spec_gold_sets.md` §4).
- **Comparator humans.** ≥ 3 qualified human raters who did **not** contribute to that unit's gold label. They code the same units blind. This avoids the circularity of comparing humans with a gold they helped build.
- **Statistics** (per dimension; metric as in `display_gates.yaml#dimensions`):

| Statistic | Definition |
|---|---|
| α(LLM, gold) | Krippendorff's α between the LLM's value (majority across runs, §4.2) and the gold value, with unit-bootstrap 95% CI |
| ᾱ(H, gold) | mean over comparator humans of α(h, gold), same bootstrap |
| Δ | α(LLM, gold) − ᾱ(H, gold); paired unit bootstrap (same resampled units for both terms) |
| α(H, H) | human–human α among comparators (for context) |
| α(H ∪ LLM) vs α(H) | does adding the LLM as a coder lower group agreement? A diagnostic only; never a gate statistic and never reported as human agreement |
| per-category precision and recall | LLM vs gold, by category |

- **Non-inferiority (G1).** The lower bound of the 95% CI of Δ must be **> −.05** (the margin set in ADR-0024 §5), **and** α(LLM, gold) lower bound ≥ .667.
- **Sample.** ≥ 120 held-out units per dimension (≥ 10 per category, oversampling rare categories). Smaller evaluations can only yield G0.

### 4.2 Run-to-run consistency

- ≥ 3 independent runs per unit with the frozen configuration (temperature > 0 if the configuration uses sampling; otherwise 3 runs with different unit orderings).
- Report α across runs.
- **Gate: ≥ .80.** Units where runs disagree are routed to two-human coding regardless of gate level.

### 4.3 Calibration and abstention

- **Calibration.** Bin the LLM's stated confidence and report accuracy against gold per bin (reliability diagram, expected calibration error).
  - **Acceptable:** accuracy is non-decreasing with confidence, and the top bin's accuracy is ≥ .85 [J].
  - If confidence is uninformative, it may not be used to route units (every unit is verified).
- **Abstention.** Report the abstention rate, and accuracy on non-abstained units. All abstentions go to two-human coding.

### 4.4 Decision rules (pre-registered per dimension)

| Result | Gate level |
|---|---|
| any of: non-inferiority fails; α(LLM, gold) LB < .667; run-to-run α < .80 | G0 |
| non-inferiority holds; α LB ≥ .667; run-to-run ≥ .80; calibration acceptable | G1 |
| G1 and α LB ≥ .80 and two clean audit cycles (§5.1) and CA approval; descriptive dimension only | G2 |

## 5. Automation-bias safeguards (required at G1 and G2)

Human verifiers anchor on suggestions. Pre-annotation shifts annotator choices, and complacency grows with monotonous verification [E-u: IO-070, IO-071, IO-072]. The design measures and limits this.

### 5.1 Blind audit stream

- A random **20%** of units in production are coded by humans **without** seeing the LLM output (commit-then-reveal: a verifier codes blind, then sees the suggestion and may revise, with both values logged).
- **Anchoring index** = humans' agreement with the LLM when shown its output, minus their agreement on blind-stream units.
  - If the index exceeds **10 percentage points** without a matching gain in accuracy against gold, anchoring is present. Then: raise the blind share to 40%, retrain verifiers, cut throughput, and report.
- An **audit cycle** is 500 production units or one quarter, whichever comes first.

### 5.2 Seeded errors

- **5–10%** of displayed suggestions are deliberately wrong. They are drawn from plausible confusions in the codebook's pair rules, logged, and reversed after the verifier's decision.
- **Catch-rate target ≥ 80%** per verifier per cycle. Below it, the verifier pauses and retrains. A pool-wide catch rate below 80% returns the dimension to G0.

### 5.3 Verification design

- Verifiers are qualified human raters for the dimension (same qualification as `protocol_reliability_study.md` §4).
- **Accept requires an affirmative act.** There is no pre-checked "accept". For selection-adjacent dimensions, accepting a value in a high-consequence category (e.g. `system-executes`, FC = 2 on a formation task) requires a one-line reason.
- **Workload limits:** ≤ 120 units per verifier-hour, ≤ 3 hours per day on one dimension, and rotation across dimensions.
- The decision path is recorded per value: `llm-accepted`, `llm-overridden`, `human-only` (blind stream), `abstained → human`.

### 5.4 Provenance per value

Each value records:
- coder types;
- configuration hash;
- decision path;
- pseudonymous verifier ID;
- timestamp;
- whether the unit was in the blind stream or seeded.
These are stored on the L5 rating record (SPEC §13.1) and never on L1–L3 records.

## 6. Drift, contamination and change control

1. **Drift.** Re-run the held-out evaluation on any model, prompt, retrieval or codebook change, and at least every 6 months. An α(LLM, gold) drop > **.05**, or a seeded-error catch rate < 80%, **holds the pipeline** (CI blocks new LLM-first values for that dimension) until re-evaluated.
2. **Upstream model retirement.** A vendor retiring or silently updating a model counts as a configuration change. Model identifiers must be pinned; unpinnable endpoints cannot pass G1.
3. **Contamination control.** Held-out gold labels stay outside the public CC0 repo until after each evaluation, then publish with the release and are rotated (≥ 20% new held-out units each release). Canary strings are embedded in held-out files. A probe checks whether the model reproduces gold labels from unit IDs alone; a positive probe voids that held-out split.
4. **Vendor independence.** EMST is built with an AI vendor's model (ADR-0008 §4 disclosure). Where feasible, the gate evaluation is run on ≥ 2 model families, and a G2 dimension must not depend on a single vendor's model without CA's recorded acceptance of that dependency.

## 7. Disclosure

Every release states, per dimension:
- gate level;
- configuration hash;
- the share of values that were LLM-first and human-verified;
- the share overridden;
- α(LLM, gold) and ᾱ(H, gold) with CIs;
- the anchoring index;
- the seeded-error catch rate.
All are computed by the build. CP's evidence drawer shows "coded first by a validated AI coder and verified by a person" or "coded by people". It never shows "validated" for an LLM-only value.

## 8. Stop rules

| Trigger | Action |
|---|---|
| Held-out split exposed to anyone tuning prompts | void the evaluation; build a new held-out split |
| Anchoring index > 10 pp for two consecutive cycles despite retraining | dimension returns to G0 |
| Pool catch rate < 80% in a cycle | dimension returns to G0 until a new evaluation |
| Drift > .05 | pipeline held (§6.1) |
| Any LLM value found rendered without verification at G1, or any LLM value in a selection-relevant field without a second human | incident: values withdrawn from views; root-cause note in the deviations log; CA informed |
| Held content in a prompt or output | stop; purge from logs; notify TN (G-TN) |

## 9. Pre-registration fields

All `preregistration_core.yaml#core_required` fields, plus:

| Field | Content |
|---|---|
| `dimension_and_codebook` | dimension ID; codebook version and SHA-256 |
| `configuration` | model ID and version, prompt and template hashes, decoding settings, retrieval context, output schema |
| `gold_split` | held-out split ID, size, strata, storage location (non-public until evaluation), canary IDs |
| `comparators` | number and qualification of comparator humans; independence from gold |
| `statistics` | §4 table; bootstrap B and seed; non-inferiority margin −.05 |
| `gate_rules` | §4.4 |
| `safeguards` | blind share, seeded-error rate and generation method, workload caps |
| `drift_and_change_control` | §6 |
| `disclosure` | §7 fields |

## 10. Outputs

- Gate decision record per dimension and configuration (`validation/studies/LLM-nn/decision.yaml`, generated): level, statistics, date, configuration hash, approver.
- SCORES.md rows (`spec_gold_sets.md` §7).
- CI rule (DE): an LLM-first value is accepted into `data/v2/assessments/` only if a passing decision record exists for its dimension and configuration hash, and its decision path shows human verification (G1) or G2 approval.
