
The full protocol covers per-use validity claims (§0), pre-registration (§2), sampling with composition correction (§3), the job-analysis survey (§4), Delphi (§5), linkage (§6), tagging reliability, LLM gates and the craft pilot (§7), assessment and criterion evidence (§8), fairness (§9), documentation (§10), maintenance (§11), timeline (§12) and responsibilities (§13). Key numbers, computed this session:

| Number | Value |
|---|---|
| Exact Lawshe critical values (one-tailed α = .05) | N = 15 needs 12 "essential" (CVR .60); N = 20 needs 15 (CVR .50); N = 25 needs 18 (CVR .44). **With v1's planned 3–5 reviewers per competency [E: IO-008], CVR significance is impossible at 3 and requires unanimity at 5** |
| Survey precision | n = 30 gives a ±0.36 CI on a 1–5 importance mean; n = 50 gives ±0.28 |
| Criterion studies | n ≈ 194 to detect r = .20 (power .80, two-tailed); 154 one-tailed. Few single agencies have that many incumbents in one job family, so consortium and transportability designs are needed |
| Reliability study size | With 40 units, α's 95% sampling range is about ±0.15, too wide to separate .667 from .80. 120–200 units × 6 raters narrows it to about ±0.04–0.07 |
| Effect of coarsening | A 3-level ordinal coarsening lowers α (latent .80 → about .68). CA's ordinal fallback is not automatically more reliable |

**NGO pilot vs. federal/state rollout.**
- **The NGO pilot (months 2–7) can:** calibrate instruments, codebooks and the LLM pipeline; estimate reliability; and support *describe* and *develop* uses inside pilot organizations.
- **It cannot:** support selection or generalize to federal or state jobs.
- **Federal/state content validation (months 6–15)** and **assessment plus criterion evidence (months 12–24)** follow with FH/SL partner agencies.

## 7. Candidate competencies

`candidate_competencies.csv` proposes three assessable competencies my analysis shows are missing:
- **IO-C01:** evaluate and certify others' task performance against position standards. Task-book evaluator quality is what training-use validity depends on.
- **IO-C02:** serve as a subject-matter expert in merit-based hiring assessments. SME-QA and the Chance to Compete Act put practitioners into rating applicants.
- **IO-C03:** elicit and document tacit expertise from experienced practitioners. It counters the contraction-driven knowledge loss v1 itself projected, and it supplies the critical incidents BARS need.

## 8. Answers to CA architecture questions (CA §6, IO)

### Q1. Which spine (competency vs. task statement) can be validated to a defensible standard first? (DP-1)

**Answer: the task statement, clearly. Competencies validate second, by linkage.** [E-u + E + J]

- **Reliability.** Task-level job-analysis ratings are more reliable than ratings of abstract work descriptors [E-u: IO-044]. Specificity and observability raise reliability [E-u: IO-045]. Competency ratings inflate more than task ratings under self-presentation [E-u: IO-043]. Competency inferences improve when raters have task information [E-u: IO-041].
- **Law.** UGESP content validity is built on work behaviors and explicitly limits inferences about mental processes [E-u: IO-020]. A competency is defensible in selection only through its link to validated, critical tasks.
- **v1 material.** v1's tasks are closer to assessable form (verb-led, concrete) than its competency-level statements (85.5% of Knowledge statements scored 0 or 1) [E: IO-010]. v1's tasks still need incumbent validation, standards and more depth per function.
- **Recommendation:** validate the task layer first, through the job-analysis survey (importance, frequency, consequence of error, needed at entry, AI mode). Then validate competencies as **curated clusters with an established link to at least one critical task** (`validation_protocol.md` §6), plus Delphi CVR for inclusion and level placement. This supports CA's hybrid lean: a task-graph spine, competency packaging and federated coverage.
- **One caution to CA:** a task inventory large enough to cover the sector is expensive to validate. Use **matrix sampling** (each respondent rates no more than about 80 tasks), validate **3–5 priority function clusters first**, and let unvalidated tasks exist with `validation_status = draft` rather than holding the release for them [J].

### Q2. Can raters reliably produce craft weights? Pilot design and agreement statistic. (DP-5)

**Answer: unknown. No v1 evidence exists either way, and the literature doesn't settle this particular judgment.** Craft irreducibility is an inferential classification closer to an abstract descriptor than to a task-frequency rating, and v1's own records show persistent boundary disputes (2.3.2 drone operation; LCA producer vs. consumer; 7.2.3) [E: IO-006]. My prior is that task-level "defining craft" will reach α in the .60–.75 range and that constant-sum weights will be lower unless averaged over ≥ 3 raters [S; the pilot will confirm or refute it]. The pilot design is in full in `validation_protocol.md` §7.3:

| Design element | Specification |
|---|---|
| Units | **150 tasks**, stratified by v1 primary craft (50 each), ≥ 40% beyond public lands and forestry, ≥ 20% known boundary cases, ≥ 20% inferred D3 tasks. **Plus 40 competencies** as a competency-level comparison arm, which directly tests CA §7's "move toward Option A" condition |
| Raters | **12 humans** in two fully crossed groups of 6 (trained taxonomy raters; practitioner SMEs balanced by craft and ≥ 4 sector actors), after frame-of-reference training [E-u: IO-042]. **Plus an LLM arm:** frozen model, 3 runs |
| Formats | Within-subject, counterbalanced, ≥ 10 days apart. **F1 constant-sum** (100 points across FC/DC/SC, anchored on the irreducibility test). **F2 ordinal** (none / supporting / defining per craft). Derived **defining craft** (nominal). Confidence ratings |
| Statistics | Per craft: ICC(2,1) and ICC(2,k), absolute agreement, and interval Krippendorff's α for F1; ordinal α for F2; nominal α for defining craft. All with bootstrap 95% CIs; **decisions on the lower bound**. Spearman–Brown gives the operational number of raters. LLM: agreement with the human mean, run-to-run α, and a non-inferiority margin of .05 against the average single human |
| Precision | 150 × 6 gives about ±0.05 on α near .8 [E: simulation] |
| Decision rules (pre-registered) | (1) Weights if ICC(2,3) lower bound ≥ .80 and ≥ ordinal. (2) Else ordinal if its lower bound ≥ .667, labelled tentative. (3) Else defining craft only. (4) If competency-level ratings beat task-level by ≥ .10 α, report to CA as evidence for Option A. (5) LLM becomes first coder only if it passes the §7.2 gate |
| Cost and time | About 3–4 rater-hours per format; 6–8 weeks; feasible in the NGO pilot |

**An architectural note for DP-5 [E: simulation; J].** Coarsening a continuous judgment to a 3-level ordinal *reduces* α (latent .80 → about .68). The ordinal fallback is only better if raters disagree about magnitude more than about rank, and only the head-to-head comparison can show that. **Design the schema so craft representation is a swappable attribute** (weights, ordinal or nominal) carrying a confidence value and rater count, so DP-5 can be reversed without migration.

### Q3. Generic levels of responsibility plus anchors, or competency-specific levels only where practised? How many levels? (DP-4)

**Answer: both, combined.** Generic responsibility levels (L1–L5) are defined once on seven attributes, and competency-specific behavioral indicators are written **only at the levels where the competency is practised** (level spans). **Five levels, plus an Awareness knowledge bundle that is not a level.** [J; grounded in IO-061, IO-058, IO-004, IO-010]

- **Why not competency-specific scales alone.**
  - Levels would not be comparable across competencies (an "L3" in statistics would mean something different from an "L3" in negotiation). That breaks role profiles, mobility comparisons (CM) and FES-aligned crosswalks (FH).
  - Rater training would multiply.
- **Why not generic descriptors alone.** They are too abstract to assess: v1's generic-feeling level text is exactly what failed OBS-4.
- **Why five.**
  - v1's Expert level conflated deep technical authority (L4) with organization- or sector-level strategy (L5). Splitting them lets most competencies stop at L4 and confines L5 to the roughly 15–25 governance competencies where SMEs confirm it.
  - Five levels map naturally onto OPM's existing five-point competency proficiency conventions [J; FH to confirm].
  - The cost is one more level to validate, and level spans contain it.
- **Fit to CA's layers.** The level scale and attributes sit in L0 reference vocabularies. Indicators attach to L1 competencies but are built from and linked to L2 tasks. Role profiles (L3) carry required levels per competency. The entrustment scale serves the training views.

### Q4. Minimum validity evidence for a v2.0 release used in training vs. one used in selection

**Principle.** Validity belongs to a use, not to the taxonomy [E-u: IO-025, IO-094]. v2.0 should ship with **use-labels on every element** (`validation_status`, `use_class`). No release is "validated for selection" in itself: an employer's selection use is defensible only after its own job analysis confirms the content [E-u: IO-020, IO-022, IO-031]. Labels:
- **Describe / plan:** workforce analytics and curriculum mapping.
- **Develop:** training, task books, IDPs, self-assessment.
- **Select / promote.**

**Minimum evidence by use:**

| Evidence | Describe / plan | Develop (training) | Select / promote |
|---|---|---|---|
| Documented provenance and versioning of every element | Required | Required | Required |
| SME content review across ≥ 3 sector actors and all relevant crafts (Delphi-retained: CVR ≥ exact critical value, ≥ 75% essential or useful) | Required for published competencies | Required | Required |
| Tag reliability reported (α with CI) for every tag shown to users; values with α < .667 not shown | Required | Required | Required |
| Indicators lint-clean with OBS-4 ≥ 2 and an evidence plan | Recommended | **Required** | OBS-4 = 3, no flags, double-coded |
| Level placement consensus (≥ 70% modal, IQR ≤ 1) | n/a | Required | Required |
| Response-process evidence (cognitive interviews, n ≈ 10–15) | Recommended | Required | Required |
| Bias and sensitivity review of content (incl. accessibility; TN on Indigenous content) | Recommended | Required | Required |
| Assessor agreement on the training instrument (two-evaluator agreement ≥ .70 on a ≥ 10% sample) | n/a | **Required** where sign-offs confer qualification | Required (inter-rater ≥ .80 operational) |
| Job-analysis survey confirmation for the function cluster (importance, frequency, consequence, needed at entry; ICC(k) ≥ .80; composition-corrected sample) | Recommended | Recommended (required for qualification-conferring task books) | **Required, for the specific job or position family, by or with the employer** |
| Linkage: competency/indicator ↔ critical task; assessment blueprint ↔ indicators | n/a | Recommended | **Required** |
| Standardized administration, scoring keys or BARS, and standard-setting record | n/a | Recommended | **Required** |
| Adverse-impact analysis plan; alternatives considered; accommodations | n/a | Monitor completion and outcomes by group | **Required** (four-fifths + significance + practical) |
| Criterion-related, transportability or validity-generalization evidence | n/a | n/a | **Required** where content validity is insufficient (judgment, integrity, collaboration constructs), for high-volume multi-agency use, or where adverse impact appears |
| UGESP-style documentation package (D1–D11) | Partial (D1–D4, D11) | Partial (D1–D5, D11) | **Complete** |
| AI documentation, if any AI scores or screens | n/a | If AI scores | **Required**, plus jurisdiction checks (NYC, IL, CA, CO) |

**Practical consequence for v2.0 [J].** A v2.0 released about 7–9 months into the work can credibly be **describe/develop-grade**, for the pilot and the first federal and state training uses. **Selection-ready content** for named function clusters follows as each cluster completes job analysis and linkage, roughly months 12–15. Criterion evidence follows at months 18–24.

### What this means for CA §7 ("what would change my mind")

- I have **no evidence** that competency-level ratings are more reliable than task-level ones. The literature points the other way for importance and frequency judgments [E-u: IO-043, IO-044].
- For *craft* judgments specifically, the question is open, and the §7.3 pilot tests it head-to-head.
- Until the pilot reports, IO's evidence supports CA's provisional lean: **task-graph spine, competency packaging.**

## Proposals

| ID | Proposal | Type | Basis |
|---|---|---|---|
| **P-IO-01** | Retire years-based levels. Adopt L1–L5 responsibility-anchored levels on seven attributes (incl. augmented practice and formation of others) plus an Awareness bundle | change | §3.3, `proficiency_model_v2.md` [E/E-u/J] |
| **P-IO-02** | Adopt **level spans**; publish a level only if it passes the existence, distinctness, assessability and consensus rules | change | §4 [J] |
| **P-IO-03** | Split v1 level content into four layers: performance indicators, knowledge elements, qualification gates, tools | change | §3.2, §4 [E] |
| **P-IO-04** | Make `indicator_writing_rules.md` the authoring standard, including the OBS-4 release thresholds and a CI lint for the 12 banned constructions (IA/DE build) | add | §5 [E/J] |
| **P-IO-05** | Represent AI-augmented performance with `augmentation_mode` on every indicator, verification-in-the-standard, seeded-error scoring, and AI-off/AI-on assessment for CLD-flagged competencies | add | §4 [E-u/J] |
| **P-IO-06** | Link levels to grades and bands through **position profiles** only; ban grade-equivalence tables; align attribute wording with FES concepts (FH to confirm) | change | §2.4, §4 [J] |
| **P-IO-07** | **Task spine first.** Validate tasks through a composition-corrected job-analysis survey; competencies are job-related only via linkage to critical tasks | change | §8 Q1 [E-u/J] |
| **P-IO-08** | Replace the v1 Delphi plan with the pre-registered modified Delphi: 15–25 per panel, exact CVR, published thresholds and stopping rules, sector-actor caps, CREDES/ACCORD | change | §6 [E/E-u] |
| **P-IO-09** | Build the contraction-bias correction into every sample: over-recruitment, recently separated incumbents, removing participation costs, caps, raking and sensitivity tests | add | §6; IO-003 [E/J] |
| **P-IO-10** | Reverse v1's "no inter-rater reliability" decision. Every published tag carries Krippendorff's α with CI; ≥ .80 production, .667–.80 tentative, < .667 not shown | change | §3.5 [E] |
| **P-IO-11** | Allow LLM-assisted tagging only through the §7.2 gate: frozen versions, held-out gold set, non-inferiority, blind audit stream with anchoring index, seeded errors, abstention, drift checks, disclosure. Never sole coder for selection-relevant values | add | §3.6, `validation_protocol.md` §7.2 [E/E-u] |
| **P-IO-12** | Run the **craft-weight pilot** (150 tasks + 40 competencies × 12 raters + LLM arm) before deciding DP-5. Make craft representation a swappable attribute | add | §8 Q2 [E/S] |
| **P-IO-13** | Ship v2.0 with **use-labels** (`use_class`, `validation_status`) on every element, and the minimum-evidence table in §8 Q4 as release criteria | add | §8 Q4 [J] |
| **P-IO-14** | Treat v1 exposure, craft, stage, family and lens tags as **analyst priors**, labelled as such, until validated. Replace profession-family Core/Supporting with survey importance data | change | §3.5 [E] |
| **P-IO-15** | DE to recover the 2,104 truncated source indicators (incl. all 706 Domain 5) and fix the 19 merged titles *before* rewriting; CA to run a near-duplicate screen (e.g., 1.4.2 / 4.1.2) | add | §3, `v1_assessment.csv` [E] |
| **P-IO-16** | Add candidate competencies IO-C01 (evaluate and certify performance), IO-C02 (SME in merit-based hiring), IO-C03 (elicit tacit expertise) | add | §7 [J/E-u] |
| **P-IO-17** | Position EMST task profiles as **job-similarity evidence** for transportability and consortium validation across agencies and states, a distinct value proposition for small agencies (FH/SL/AS) | add | `validation_protocol.md` §8.3 [J] |
| **P-IO-18** | Commission human double-coding of `v1_observability_ratings.csv` (2 coders, α target ≥ .80) before any v1-observability figure goes into publications | add | §3.1 [J] |

## Disagreements and trade-offs

1. **With v1: single-analyst AI coding without inter-rater reliability.** v1 treated consistency of application as sufficient [E: IO-009]. I disagree. Consistency with oneself is not agreement among qualified raters, and v1 broke even its own deterministic rules (CLD). **Trade-off:** the protocol needs about 2–3× the coding labor for gold sets and audit streams. The LLM gate can recover most of that once passed.
2. **With v1: four universal levels.** v1 valued a uniform grid that is easy to display. I'd give that up for level spans. **Trade-off:** profiles are harder to summarize in one number, so CP will need profile visualizations. I judge the uniform grid's legibility to be false precision.
3. **With a likely product pressure: publish all ~250 competencies at v2.0.** I recommend use-labels and a smaller describe/develop-grade release, with selection-grade content arriving cluster by cluster. **Trade-off:** coverage and adoption momentum versus defensibility. CA decides. I recommend defensibility for anything federal or state HR will touch.
4. **With CA's ordinal fallback for craft (§4).** The ordinal is not inherently more reliable: coarsening lowers α. Only the head-to-head pilot should decide. **Trade-off:** 6–8 weeks before DP-5 can close.
5. **With the "Awareness as level 1" convention common in competency frameworks** (including, I believe, some OPM proficiency scales; FH to confirm). I keep Awareness outside the performance levels so that L1 is always a *performance*. **Trade-off:** a one-level offset when crosswalking to frameworks that count Awareness as level 1. Handle it in the crosswalk (IA), not in the model.
6. **Fairness versus validity in method choice.** Work samples are highly job-related but can show larger subgroup differences [E-u: IO-054]. Structured interviews with BARS and job-knowledge tests are strong on both, but don't capture field craft directly. **Trade-off:** use multi-method assessment with documented consideration of alternatives, never a single high-impact hurdle [J].
7. **Opportunity-dependent senior indicators.** Removing "leads national initiatives" from selection levels may frustrate senior practitioners who earned those roles. **Trade-off:** I keep such evidence for *promotion with work history*, but not as a selection criterion that excludes equally capable people from small organizations [J].

## Issues outside my area that affect the vision

- **DE:** 32% indicator loss at import, all Domain 5 indicators missing, 19 merged titles, out-of-vocabulary tag values. Recover and fix before any rewrite. Make CLD and stability *computed* fields (CA §4 agrees).
- **TN:** v1 5.2.1 source text lists "tribes" as a stakeholder category. Tribal nations must be modelled as sovereign governments engaged by consultation. My exemplar adds an indicator to that effect; TN should review wording. The validation protocol gives non-Tribal panels no authority over Tribal-specific content (`validation_protocol.md` §3.5).
- **FC/CP:** 4.4.4 appears to pair HAZWOPER emergency-response levels with site-worker course hours. That's a safety-content error to verify against 29 CFR 1910.120.
- **SC/PS:** hard-coded rules in v1 content that 2025 changes may have overtaken (SEC climate disclosure in 3.6.2; "NEPA scientific integrity requirements" in 7.1.3). All standards should reference a jurisdiction overlay.
- **FH:** confirm OPM's current implementation of the Chance to Compete Act and Merit Hiring Plan; whether OPM's five-point proficiency conventions start at Awareness; and the FES-attribute alignment. Pilot the position-profile approach on about 30–50 PDs per priority series.
- **SL:** determine whether 5 CFR 900 Subpart F reaches environmental programs. Collect how states write minimum qualifications (years) and whether demonstrated-competency substitution is allowed.
- **CP:** Paperwork Reduction Act exposure depends on who conducts the survey; union notice for employee surveys; a state AI-employment-law matrix; privacy of panel rosters.
- **CM:** make the outcome metric *hires and promotions through EMST-based assessments*, not vocabulary adoption (§2.7). The cross-sector mover sub-sample in surveys and panels is shared work.
- **LC:** the entrustment scale and task-book design are shared ground. Co-specify them, and keep knowledge elements testable for curriculum use.
- **IA:** build the indicator linter and the gold-set and LLM-gate tooling (`validation_protocol.md` §7.2). The holdout drop I measured (κ .79 → .69) is the reason never to evaluate on tuning data.

## Open questions for the Chief Taxonomy Architect

1. **Release posture (DP-10 / release criteria):** do you accept use-labelled v2.0, describe/develop-grade first with selection-grade per cluster later, as the release model (P-IO-13)?
2. **DP-4:** do you accept five levels with spans (P-IO-01, P-IO-02)? Should L5 be deferred until job-analysis data confirm demand?
3. **DP-5:** will you hold the craft-representation decision for the §7.3 pilot (6–8 weeks) and require a swappable schema meanwhile?
4. **Priority function clusters:** which 3–5 clusters (with FH/SL) get the first job-analysis survey? My suggestion: a field monitoring cluster (FC), a regulatory compliance and permitting cluster (SC), a geospatial and data analysis cluster (DC), and one non-forestry cluster (water or air quality) to test coverage beyond public lands.
5. **Pre-registration venue:** OSF Registries or repo-only timestamped releases?
6. **Tags with poor reliability:** if v1 ethical-lens E/I/A coding fails the α gate after two codebook iterations, may IO recommend expressing ethics only through observable indicators (as in 7.1.3) and retiring the lens columns?
7. **v1 observability figures:** may they be cited externally only after human double-coding (P-IO-18)?
