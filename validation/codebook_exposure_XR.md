# Codebook: exposure and change instrument v2, rules XR-01 … XR-07

**WP-11 output 2c** · Codebook ID `emst-exposure-codebook@2.0.0-draft` (implements instrument `emst-exposure@2.0`) · Owner: IO (A8) for rating procedure; instrument stewards CA with LM, FS, FC, DC · Status: draft, not yet calibrated · Date: 2026-10-23
**Decision basis:** ADR-0008 (§1–§5); SPEC §5.12, §11; `vocab/exposure_instrument_v2.yaml` (governs if wording differs); ADR-0007 (governed data); ADR-0028 (signals).
**Used by:** `protocol_reliability_study.md` block D; `spec_gold_sets.md`; `protocol_llm_coder_gate.md`; every `ExposureAssessment` with `raterType ∈ {expert-panel, sme, analyst, llm}`.
**Labels:** [E] evidence, [J] judgment, [S] speculation. Examples are **synthetic** tasks with provisional IO keys [J], dated **2026-10-23**. Exposure values are dated by design, so keys must be re-ratified at each calibration.

---

## 1. What is rated, and what is never rated together

Three constructs are recorded **separately and never fused into one code** (ADR-0008 §2):

| Construct | Unit | Fields | Rated by |
|---|---|---|---|
| **(a) Technical exposure** | task | per vector (`llm-cognitive`, `robotics`, `sensing`, `convergent`): level E0–E3 | raters, blind (pass 2) |
| **(b) Deployment mode** | task × sector actor | `deploymentMode`, `deploymentStage`, `deploymentEvidence[]`, optional `strategy` | raters with evidence (pass 3) |
| **(c) Outcome** | role variant or organization (staffing); task × scenario (only eligible tasks) | `staffingOutcome`; `scenario`, `demandDirection`, `reproductionRisk` | panels (pass 4) |
| Supporting | task | `tacitExperienceRequirement` (Hi/Med/Lo), `accountabilityConstraint` (+ basis), `shouldRemainHumanReason`, `governedData`, `noDeployedToolPerformsCore` | pass 1 (tacit) and pass 3 |

**Rating passes are separated in time and form.** v1's tacit density nearly determined its automation type [E: audit §10, via ADR-0008 Context], so:
- tacit/experience requirement is rated in **pass 1**, in a separate session from technical exposure and deployment mode, with the task order re-randomized;
- deployment mode is rated in **pass 3**, after technical exposure, with the evidence packet (§5.3).

A rater may not revise an earlier pass's rating after seeing a later pass.

## 2. The seven rules

### XR-01@2.0 Blind coding

**Rule.** Code blind to the parent competency, domain, craft and any prior label, including v1's A/Ac/H/S/V codes, tacit density, career-ladder position and any LLM suggestion.
**What raters see:**
- the task statement;
- its stated condition or purpose;
- for construct (b), the sector-actor context and the deployment evidence packet (§5.3).
Nothing else.
**Why.** v1's standing rule R1 built its "FC/DC structural property" into the codes; field-type tasks under FC parents were coded H 46% of the time, under DC parents 6% [E: FC-029, via ADR-0005 Context].
**Machine check (DE).** Every `ExposureAssessment` with a human or LLM rater records `method` including `blind: true` and the interface version. An LLM prompt containing a v1 code, competency title or craft label fails CI (prompt hash on record).
**Edge case.** Task text that itself names a craft or a v1 code: route it to the author for rewriting before rating.

### XR-02@2.0 Descriptive and normative fields are separate

**Rule.** Record what **is** in descriptive fields and what **should be** only in `shouldRemainHumanReason`.
- **Descriptive** fields: technical exposure; deployment mode; `noDeployedToolPerformsCore`; `accountabilityConstraint` (a legal fact with its basis, e.g. a licensure rule requiring a human in responsible charge).
- **Normative** field: `shouldRemainHumanReason` (e.g. accountability, legitimacy, formation, safety).

v1's "H" decomposes into `fieldDependency` + `deploymentMode = human-executes` + `shouldRemainHumanReason`.
**Decision rules.**
1. Never lower a technical-exposure level because you think a task *should* stay human.
2. Never code `human-executes` because a human *must sign*. A human may sign a document drafted with AI: that is `assisted` or `compressive` with `accountabilityConstraint = true`.
3. The normative field is optional and never gates any display value.
**Example.** "Seal and sign the final design drawings for a culvert replacement" → technical exposure llm-cognitive E0 (the act of sealing is not performable by technology). The *drafting* is a different task. `accountabilityConstraint = true` (basis: state engineering licensure). `shouldRemainHumanReason = accountability`.

### XR-03@2.0 Compressive means time compression, never headcount

**Rule.** `compressive` is a **task-level** rating: substantial time compression, with the human reviewing and certifying the output. Headcount effects are **never** a task property. They are recorded only as `staffingOutcome` on a role variant or organization (construct c).
**Decision rule.** Code `compressive` when, in the deployed setting, the system produces a draft or result and the human's work becomes review, correction and certification, and the time for the task falls substantially (guide: by half or more). "Fewer analysts needed" in the evidence does not change the task code.
**Machine check (DE).** A task-level rationale containing headcount language ("FTE", "positions eliminated", "staff reduction", "headcount") raises a warning for review. A `staffingOutcome` on a Task record is invalid.

### XR-04@2.0 Deployment claims need deployment evidence

**Rule.** `supervises-system`, `system-executes`, and any deployment stage beyond `none` need **deployment evidence** in `deploymentEvidence[]`; otherwise code `compressive` with `sWatch = true`. v1's four S calls migrate this way, with the original call kept as a v1 assessment.
**What counts as deployment evidence** [J; aligned with LM P-LM-04]:
- (i) a registered deployment, such as an entry in the federal AI use-case inventory at a deployed stage, or a state equivalent;
- (ii) observed directive use: an SOP, programme directive or contract that requires the system in the task's workflow;
- (iii) a documented operating programme (agency or utility report naming the system in routine production).
Not sufficient on its own: vendor marketing, press releases, pilots described as plans, conference talks, research prototypes.
**Stage definitions:**
- `pilot`: time-limited trial with evaluation;
- `deployed-limited`: production use in some units or sites;
- `deployed-scaled`: production use as the standard method across the actor's programme.
**Machine check (DE).** `deploymentMode ∈ {supervises-system, system-executes}`, or `deploymentStage ≠ none`, with empty `deploymentEvidence[]` → invalid record. Evidence items must resolve to Source IDs.

### XR-05@2.0 Governed data

**Rule.** A task handling confidential Tribal information or Indigenous knowledge carries `governedData = tribal`. Its mode may be `assisted` or `compressive` only where the Tribe authorizes AI use; otherwise `human-executes`.
**Procedure in this codebook.** Such tasks are **held content** (ADR-0007). They are excluded from every rating frame, gold set and LLM prompt. Non-Tribal raters never rate them. The re-codes ADR-0008 names (v1 6.5.1 T3, 5.3.2 T3, 5.3.3 T2) are carried out only under Tribal approval, on Tribal terms.
**Other governed data** (`personal`, `confidential-business`): rate normally; the flag is descriptive and used by CP's privacy review.
**Rater action.** If a task you are rating appears to involve Tribal data or Indigenous knowledge, choose "cannot code: held content" and stop.

### XR-06@2.0 Aggregate external matches; show dispersion

**Rule.** Never attach a single external match label. Aggregate across matched O*NET tasks weighted by match type and similarity, and report dispersion and a no-external-analogue flag.
**This is an ingest rule (LM, WP-10), not a rater rule.** Raters never see external-index values (XR-01).
**Pre-registered aggregation parameters** [J; LM to confirm in WP-10]:
- *Eligible matches:* rows of a **reviewed** X2 SSSOM set (two independent human coders; ADR-0022) with predicate `skos:exactMatch`, `skos:closeMatch`, `skos:narrowMatch` or `skos:broadMatch`. `relatedMatch` and `NoTermFound` are excluded.
- *Weight:* match-type weight × calibrated confidence. Match-type weights are exact 1.0, close 0.75, narrow or broad 0.5.
- *Output:* the weighted mean or weighted distribution of the external value; weighted SD, min–max and the number of matches.
- *Flag:* `noExternalAnalogue = true` when no exact or close match exists.
**Display.** External context only, never an EMST tag (`display_gates.yaml#value_rules.external_index`). No change indicator rests on a single vendor's data (ADR-0008 §4).
**Machine check (DE).** An `ExposureAssessment` with `raterType = external-index` and `externalSource.matchedOnetTasks` of length 1 and no `aggregation` field is invalid.

### XR-07@2.0 Module tasks before sector-wide conclusions

**Rule.** Exposure is assessed on module tasks, including robotics-exposed subsectors, before any sector-wide exposure conclusion is published.
**Operational rule** [J]. A sector-wide statement ("x% of environmental tasks…") may be published only when:
- (a) every wave-1 module (`water`, `waterq`, `air`, `waste`, `envhealth`, `hazards`, `forest`, `wildlife`, `parks`) has ≥ 15 tasks with gated v2 values (`display_gates.yaml`), and
- (b) the robotics-exposed subsectors ADR-0008 names (materials-recovery sorting, process control, laboratory automation, pipe inspection, continuous emissions monitoring) are represented in the sample.
The statement must also report module coverage and the denominator.
**Sampling consequence.** The reliability study and gold sets stratify by home module (`spec_gold_sets.md` §3); a module stratum with ≥ 30 units gets its own gate (`display_gates.yaml#strata`).

## 3. Construct (a): technical exposure by vector

### 3.1 Vectors

| Vector | Rate it when… |
|---|---|
| `llm-cognitive` | language and reasoning models acting on text, code, images or documents could perform or speed the task |
| `robotics` | physical automation or robotic systems could perform the task's manipulation or locomotion |
| `sensing` | instruments, imagery, acoustic arrays, camera traps, eDNA or sensor networks could replace in-person observation |
| `convergent` | only an operationally inseparable combination of the above could do it (e.g. an autonomous vehicle that senses, decides and acts). Do not use `convergent` when the vectors could be deployed separately |

Rate **every** vector for every task (E0 is a valid answer). The comparison base is the task as performed today **without** the technology.

### 3.2 Levels

| Level | Definition (vocab) | Decision rule |
|---|---|---|
| **E0** | No meaningful reduction in time at equal quality | the technology cannot do the core of the task, or cannot meet the task's standard |
| **E1** | Time cut by at least half at equal quality **with the technology alone** (aligns with Eloundou E1) | a performer with commonly available technology of this vector, used directly, does the task in half the time or less, to the same standard |
| **E2** | Time cut by at least half **only with complementary software or system integration** built on the technology | the halving needs purpose-built tools, data pipelines or integration that exist but are not the bare technology |
| **E3** | Technology can perform the full task end to end at equal quality under current conditions | no human step is needed for the task's core to meet its standard (whether or not deployed; that is construct b) |

- **"Current technology"** means commercially available or documented in production use as of the assessment date. Research prototypes and announced products are not current.
- **"Equal quality"** is judged against the task's own standard (protocol, accuracy, legal sufficiency). It is not judged against "good enough".
- **Ordinal order for agreement statistics.** By intensity of exposure, E1 (halving with the technology alone) is more exposed than E2 (halving only with integration). For Krippendorff's ordinal α, **this codebook therefore orders E0 < E2 < E1 < E3.** The vocabulary lists E0–E3 in numeric order. CR-IO-003 asks CA to record the ordinal order in `vocab/exposure_instrument_v2.yaml` (and to resolve the scenario-eligibility wording "E2+"). Until then the ordinal metric uses this codebook's order, and a nominal α is reported alongside.

### 3.3 Decision procedure

1. Name the task's core: the part that must be done for the deliverable to exist.
2. For each vector: could that technology, now, do the core end to end at equal quality? Yes → E3. No → could it halve the time used directly? → E1. Only with integration? → E2. Otherwise → E0.
3. Confidence 1–5 per vector. "Cannot code" if the task's standard is not stated well enough to judge "equal quality".

## 4. Supporting attributes (pass 1 and pass 3)

| Attribute | Values | Decision rule |
|---|---|---|
| `tacitExperienceRequirement` (pass 1) | Hi · Med · Lo | **Hi:** performance to standard relies on judgment built through extended supervised practice across varied conditions; procedures cannot fully specify it. **Med:** procedures cover routine cases; non-routine cases need experienced judgment. **Lo:** a newcomer can meet the standard from written procedure after brief instruction. Rated before, and separately from, any exposure judgment. Used as a predictor, never inferred from mode |
| `accountabilityConstraint` (pass 3) | true/false + basis | true only with a cited legal or licensure basis requiring a human in responsible charge |
| `noDeployedToolPerformsCore` (pass 3) | true/false | descriptive: no deployed tool performs any part of the core task in this sector actor's context |
| `shouldRemainHumanReason` (optional, pass 3) | free text from a short list: accountability · legitimacy · formation · safety · governed-data · other | normative. Never affects other fields (XR-02) |

## 5. Construct (b): deployment mode (task × sector actor)

### 5.1 Modes (ordinal order for α: human-executes < assisted < compressive < supervises-system < system-executes)

| Mode | Rule |
|---|---|
| `human-executes` | no deployed tool performs any part of the core task in this actor's context |
| `assisted` | the human performs the task with tools that support it; the human produces the core output |
| `compressive` | the system produces the draft or result; the human reviews, corrects and certifies; task time falls substantially (XR-03) |
| `supervises-system` | the system executes; the human monitors and intervenes; **evidence required** (XR-04) |
| `system-executes` | the system executes without routine human review; **evidence required** (XR-04) |

### 5.2 Strategy tag (optional)

Code it only if the deployment evidence states the adopter's design intent:
- `substitution`: removes human performance of the task;
- `augmentation`: keeps human performance and speeds it;
- `augmentation-for-formation`: also frees senior time for mentoring and protects the learning substrate.
Otherwise leave it blank. Never infer strategy from mode.

### 5.3 Evidence packet

Per task × actor, DE and LM assemble an evidence packet from L5 signals and Source records:
- registry entries;
- programme reports;
- SOPs;
- dated postings that name the system in duties.
The packet excludes external-index values, v1 values and agent opinions. A rater codes from the packet plus their own documented knowledge, citing any added source.

## 6. Construct (c): outcomes

- **`staffingOutcome`** (role variant or organization only): `grow` · `stable` · `compress` · `decline` · `insufficient-evidence`. Each value carries driver tags (AI, sensing, automation, fiscal, policy, demographic…). Fiscal or policy contraction must not be coded as automation (ADR-0008 Rationale). `insufficient-evidence` is the default.
- **Scenario rows** (task × SC1–SC4): `demandDirection` ∈ up · flat · reshape · external · down; `reproductionRisk` ∈ L · M · H. Rated only for **eligible tasks**:
  - vocab: E2+ on any vector, or deployment mode compressive or higher;
  - or flagged formation tasks.
  IO reads "E2+" as intended to include E1 (directly exposed) and asks CA to confirm in CR-IO-003. Until then, eligibility includes E1, E2 and E3. Rated by a pre-registered panel with the scenario narratives in `vocab/scenarios.yaml`.

## 7. Anchored examples (synthetic; keys [J] as of 2026-10-23; to be re-ratified)

| # | Task (synthetic) | llm-cog. | robotics | sensing | conv. | tacit | Mode (actor context) | Notes |
|---|---|---|---|---|---|---|---|---|
| X1 | Summarize public comments on a draft plan into themes with traceable citations to each comment | E1 | E0 | E0 | E0 | Med | compressive (federal; evidence: documented production use in comment-analysis workflows) | verifying citations is the human step; XR-03: no headcount |
| X2 | Identify bird species from acoustic recorder files for a monitoring programme | E2 | E0 | E2 | E0 | Hi | assisted (state; classifier used to pre-screen, human confirms) | sensing and llm-cognitive separately E2: purpose-built classifiers needed |
| X3 | Sort mixed recyclables on a materials-recovery line | E0 | E2 | E1 | E2 (boundary) | Lo | supervises-system only with evidence; else assisted | convergent only if the sorting robot's sensing and picking are inseparable; key panel to rule (XR-07 robotics subsector) |
| X4 | Delineate a wetland boundary on site from soils, hydrology and vegetation indicators | E0 | E0 | E2 | E0 | Hi | human-executes | imagery and LiDAR pre-screens are a different (planning) task |
| X5 | Draft a categorical-exclusion documentation memo from a project description and checklist | E1 | E0 | E0 | E0 | Med | compressive with `sWatch` unless deployment evidence (XR-04) | legal sufficiency review is the human step; accountabilityConstraint false unless a rule requires a named official |
| X6 | Seal and sign final design drawings as engineer of record | E0 | E0 | E0 | E0 | Hi | human-executes | accountabilityConstraint true (licensure); normative reason: accountability (XR-02) |
| X7 | Adjust coagulant dose in response to raw-water turbidity at a treatment plant | E0 | E0 | E2 | E2 | Med | assisted (local utility; online analyzers with operator control) | convergent E2 if dose control is automated on sensor input |
| X8 | Inspect the interior of a sewer main for structural defects | E0 | E2 | E2 | E2 | Med | assisted (crawler camera, operator codes defects) | XR-07 robotics subsector |
| X9 | Negotiate the terms of a cooperative stewardship agreement between two agencies | E0 | E0 | E0 | E0 | Hi | human-executes | drafting support would be a separate task |
| X10 | Validate a machine-learning land-cover map against a stratified field sample and report accuracy | E2 | E0 | E0 | E0 | Med | assisted | the validation itself is human method choice (DC) |
| X11 | Operate continuous emissions monitoring and certify quarterly data | E0 | E0 | E3 | E0 | Med | supervises-system only with evidence (e.g. a permit requiring CEMS) | certification is attestation (accountabilityConstraint true) |
| X12 | Fell a hazard tree near a trail | E0 | E0 | E0 | E0 | Hi | human-executes | robotics E0 under current conditions in uncontrolled terrain |

X3 deliberately tests the convergent rule and is expected to split raters. The key panel's ruling is recorded in the next PATCH.

## 8. Cannot code

Use "cannot code" with one of these reasons:
- `standard not stated` (cannot judge equal quality);
- `compound task`;
- `held content`;
- `actor context missing` (construct b);
- `no evidence packet` (construct b: then `deploymentMode` defaults to the most conservative code supported, never above `compressive`).

## 9. Machine-checkable constraints (for DE's validator)

| Check | Rule | Severity |
|---|---|---|
| XR-04 | mode ∈ {supervises-system, system-executes}, or stage ≠ none, needs non-empty `deploymentEvidence[]` resolving to Source IDs | error |
| XR-03 | `staffingOutcome` on a Task-level assessment | error |
| XR-03 | headcount terms in a task-level rationale | warn |
| XR-05 | `governedData = tribal` on a record not under `approvalStatus = pending-tribal-review` or approved | error (release) |
| XR-06 | `raterType = external-index` without `externalSource.aggregation` and `dispersion` | error |
| XR-02 | `shouldRemainHumanReason` present and `technicalExposure` levels missing | warn (normative recorded without descriptive) |
| Scenario | scenario rows on a task that is not eligible (§6) | error |
| Hash | `taskTextSha256` ≠ current task hash → stale (never displayed) | computed |
| v1 | `raterType = v1-analyst` without `v1Flags[]` | error |

## 10. Version control

Same as `codebook_craft_ratings.md` §11. Exposure codebooks are also re-ratified at least every 12 months, because what counts as "current technology" moves. A re-ratification that changes any key is a MINOR version and voids gate results.
