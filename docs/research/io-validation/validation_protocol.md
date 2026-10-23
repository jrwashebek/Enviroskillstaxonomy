# EMST v2 Validation Protocol

**Role:** IO · **Status:** draft protocol for CA approval. Pre-register before first data collection (§2) · **Date:** 2026-10-23
Labels: **[E]** evidence read or computed this session · **[E-u]** published evidence not re-retrieved this session (`unverified` in `sources.csv`) · **[J]** expert judgment · **[S]** speculation.
Companion files: `proficiency_model_v2.md`, `indicator_writing_rules.md`, `exemplar_rewrites.csv`, `analysis/` (scripts and computed values cited here).

---

## 0. What "validated" means here

Validity is a property of **interpretations of scores for a use**, not of a taxonomy in the abstract [E-u: IO-025, IO-094, IO-095]. So EMST v2 can't be "validated" once and then used for anything. This protocol builds a **validity argument per use** and says what evidence each use needs:

| Use | Claim being made | Minimum evidence (summary; full table in `report.md` §8, answer to CA Q4) |
|---|---|---|
| **Describe and plan** (workforce strategy, gap analysis, curriculum mapping) | "These tasks, competencies and levels represent the work in this function across sector actors." | Content evidence (§4–§6) + tagging reliability (§7) + provenance |
| **Develop** (training, task books, self-assessment, IDPs) | "Performing these indicators at this level shows readiness for less supervision." | Above + assessor agreement on the training instrument (§8.2) + response-process evidence (§4.6) |
| **Select and promote** | "Scores on this assessment predict, or are representative of, performance in *this* job." | Above + **job-specific** job analysis and linkage (§4, §6) + assessment reliability + standard-setting + adverse-impact analysis (§9) + criterion-related or transportability evidence where content validity is insufficient (§8.3) + UGESP documentation (§10) |

**Hard rule [J; IO-020, IO-022, IO-031]:** no EMST release is "validated for selection" in itself. An employer's selection use is defensible only after that employer's job analysis has confirmed the EMST content for the job. EMST's job is to make that confirmation fast, cheap and well documented.

## 1. Principles

1. **Tasks first, competencies by linkage.** Task statements are rated more reliably and inflate less than abstract descriptors [E-u: IO-043, IO-044, IO-045]. UGESP content validity is built on work behaviors [E-u: IO-020]. Competency validity is therefore *derived*: a competency is job-related for a job family when it is essential to at least one critical task validated for that family (§6).
2. **Pre-register everything that decides an outcome:** thresholds, rounds, stopping rules, exclusion rules, weighting, analysis plans (§2).
3. **Sample to correct, not to convenience.** v1's own scenario analysis warned that under workforce contraction, "public-agency practitioners (core fieldcraft and statecraft holders) may have reduced slack to engage in Delphi processes, while private-sector datacraft practitioners may become overrepresented in validation—biasing the taxonomy toward codifiable competencies" [E: IO-003]. §3 builds the correction in.
4. **Measure the reliability of every tag anyone will see.** v1 decided a single AI-augmented analyst needed no inter-rater reliability provisions [E: IO-009]. That decision is reversed here (§7).
5. **LLMs are coders to be validated, not oracles.** An LLM-assisted tag is published only with measured LLM–human agreement on held-out data, plus an automation-bias guard (§7.2).
6. **Document for an adversary.** Every step produces records a reviewer, an auditor or opposing counsel could inspect (§10).

## 2. Pre-registration and governance

- **Registry:** OSF Registries (or the repo plus a timestamped release tag, if CA prefers repo-only) before the first data collection in each phase [J].
- **Registered fields:** study aims and uses supported; sampling frame and quotas; instruments (frozen versions with hashes); consensus thresholds (§5.4); stopping rules; exclusion rules (§4.5); weighting scheme (§3.4); reliability targets (§7); analysis code (repo path and commit); deviations log.
- **Steering group:** IO (method owner), CA (decisions), FH/SL (federal/state requirements), DE (data and provenance), IA (LLM pipeline), TN (anything touching Tribal content; real consultation required, §3.5). The steering group may not vote in Delphi panels.
- **Ethics and approvals [J; CP lane to confirm]:**
  - Human-subjects review through an academic partner's IRB, if publication is intended.
  - Agency survey approval, and union notification or bargaining where federal or state employee participation affects working conditions.
  - The **Paperwork Reduction Act** applies if a federal agency sponsors or conducts a survey of ten or more members of the public (NGO, private, academic respondents). Federal employees responding within the scope of their employment are generally outside it. Choose the conducting entity deliberately.
  - Privacy: collect no direct identifiers in survey data; keep panel rosters separately.

## 3. Sampling frame and composition correction

### 3.1 Strata

**Sector actor** (federal · state · local · Tribal · NGO · private · academic) × **function cluster** (CA's work functions, or interim: FC-, DC-, SC-primary clusters) × **career stage** (early < 5 years in the field; mid; senior) × **region** (4 Census regions + Alaska/Pacific).
Career stage is used *only* for sampling and analysis, never for proficiency levels (`proficiency_model_v2.md` §2) [J].

### 3.2 Population benchmarks for weighting (owners in brackets)

- Federal: OPM workforce data by occupational series (0028, 0401, 0404, 0408, 0454, 0455, 0460, 0462, 0486, 0819, 1301, others) [FH].
- State and local: BLS OEWS by ownership and SOC, plus state classification-plan headcounts where obtainable [SL].
- Private: OEWS private-ownership SOC/NAICS [PS].
- NGO: partner rosters plus nonprofit-sector registries for environmental organizations [AS].
- Academic: faculty and staff counts in relevant CIP families [LC].
- Tribal: **no benchmark is assumed.** Participation and any counts follow TN's protocol and the nations' own decisions [TN; CARE].

### 3.3 Quotas (minimum completes)

| Study | Cell definition | Minimum per cell | Notes |
|---|---|---|---|
| Job-analysis survey, federal/state rollout | sector actor (fed, state) × function cluster | 30 incumbents + 10 supervisors | n = 30 gives a 95% CI half-width of ±0.36 on a 1–5 importance mean (SD ≈ 1) [E: computed, `analysis/`] |
| Job-analysis survey, other actors | sector actor × function cluster | 15 | Descriptive and comparative only until n ≥ 30 |
| NGO pilot survey | function cluster | 10 | Feasibility, not estimation |
| Delphi panels | per panel | 15–25 completing all rounds | §5.2 |

### 3.4 Correcting for contraction-driven composition bias [J, building on IO-003]

1. **Over-recruit the strata the contraction thins.** Public-agency field and statecraft roles (fed, state, local, Tribal), field-season staff, and early-career and term employees get recruitment targets at **1.5×** their quota.
2. **Include recently separated incumbents.** People who left a relevant position within the past 24 months (RIFs, deferred resignation, retirement, term expiry) form a *recent-incumbent* sub-stratum. They hold the knowledge most at risk, and they are free of current-employer constraints. Analyze them separately and pooled.
3. **Remove participation costs that fall unevenly.**
   - Request authorization for on-duty participation for public employees.
   - Offer stipends for NGO and Tribal participants and for separated incumbents.
   - Provide offline, phone and interviewer-administered modes for field staff.
   - Schedule field-role collection outside peak field and fire season.
4. **Cap over-representation in panels.** No sector actor above 30% of any Delphi panel. Private-sector datacraft practitioners no higher than their population share in the federal/state release panels. At least one-third of each panel's members must have **current or recent field- or statecraft-primary roles**.
5. **Weight and test.** Rake survey weights to the benchmarks in §3.2 (sector actor × occupation cluster; region; career stage) and trim weights at 5× the median. Report weighted and unweighted results, the design effect, and a **sensitivity analysis** that drops the most over-represented stratum. If a retention decision flips between weighted and unweighted results, the item goes to Delphi as contested.
6. **Monitor during fielding.** Track response by stratum weekly; follow up stratum-targeted; run a nonresponse-bias check (early vs. late responders; respondents vs. frame).

### 3.5 Tribal participation

Tribal nations participate as sovereign governments and employers, on their terms. This protocol does **not** authorize collecting Tribal workforce data or Indigenous knowledge. That requires TN's protocol and real consultation with the nations involved. Until then, Tribal-specific content is flagged `requires-consultation` and is not validated by non-Tribal panels [J; CHARTER; TEAM_BRIEF §3].

## 4. Job-analysis survey

### 4.1 Instrument content

**Task section.** Tasks for the respondent's function cluster, with matrix sampling so that each respondent rates no more than about 80 tasks and the survey stays under 40 minutes [J]. The scales follow practice-analysis conventions for frequency, importance and criticality [E-u: IO-084].

| Scale | Response format (anchored) |
|---|---|
| Performed in current/most recent position | Yes / No |
| Frequency | 1 less than yearly · 2 yearly · 3 monthly · 4 weekly · 5 daily |
| Importance to effective job performance | 1 not important · 2 minor · 3 important · 4 very important · 5 critical |
| Consequence of error | 1 negligible · 2 minor rework · 3 significant cost, delay or legal exposure · 4 serious harm to people, environment or legal standing · 5 severe or irreversible harm |
| Needed at entry | Must be performed without further training on day one: Yes / No |
| AI or automation in how this task is done now | none · assisted · largely automated with my review · I supervise an automated system (feeds `augmentation_mode` and L5 change signals) |
| Changed materially in past 12 months? | Yes / No (sentinel item; §11) |

**Competency section** (≤ 25 competencies linked to the cluster): importance; **required level for full performance** (A, L1–L5, shown with the generic descriptors); level **needed at entry**; and optionally typical time to reach that level, to populate the descriptive `typical_time_to_level` (`proficiency_model_v2.md` §3).

**Background:** sector actor, series or class or job family, supervisory status, region, career stage, whether the respondent has moved across sector actors (CM lane). No names; no exact duty station.

### 4.2 Respondents

Incumbents rate their own positions. Supervisors rate the positions they supervise. Comparing the two is an inflation check: competency and ability ratings inflate under self-presentation pressure, task ratings less so [E-u: IO-043, IO-087].

### 4.3 Retention rules (pre-register; illustrative values) [J]

- **Task retained for a function cluster** if (a) at least 25% of the cluster's incumbents perform it, **and** (b) weighted mean importance ≥ 3.0, **or** mean consequence of error ≥ 4.0 (low-frequency, high-consequence tasks such as hazmat response must not drop out on frequency).
- **Critical task** (eligible to support selection): retained, *and* criticality index (importance × consequence, pre-registered formula) in the top tercile for the cluster.
- **Needed at entry:** at least 50% of incumbents *and* supervisors say "yes". Otherwise the task is a development target, not an entry selection criterion.
- **Actor-variant task:** retention differs by ≥ 25 percentage points between sector actors with n ≥ 15 each. These feed CA's enactment-note and role-variant hypothesis.

### 4.4 Reliability of job-analysis ratings

- ICC(2,k) of mean importance per task within a function cluster: target ≥ .80. Within-group agreement r_wg(j) is reported alongside. ICC form and interpretation follow standard reporting guidance [E-u: IO-085].
- The number of raters needed follows from single-rater ICC by Spearman–Brown. A single-rater ICC of .30 needs about 10 raters for ICC(k) ≥ .80; .40 needs about 7 [E: computed, `analysis/`]. Meta-analytic job-analysis reliabilities are higher for task data than for generalized work activities [E-u: IO-044].

### 4.5 Data-quality exclusions (pre-register)

- 2–3 **bogus tasks** per form, plausible but nonexistent. Respondents endorsing them as performed are excluded or down-weighted [E-u: IO-078].
- Two instructed-response items; straight-lining (identical responses across ≥ 90% of a page).
- Completion time under one-third of the median.

### 4.6 Response-process evidence

Cognitive interviews (n ≈ 10–15 per release, spread across sector actors and crafts) on scale anchors, the level descriptors and a sample of indicators. Revise wherever 3 or more respondents misread [J].

## 5. SME panels and modified Delphi

### 5.1 Structure

1. **Round 0, SME workshops** (DACUM-style, 6–10 SMEs per function cluster): critique task and competency drafts; generate critical incidents (≥ 10 per competency) for BARS; propose level spans.
2. **Delphi Rounds 1–3**, online and anonymous: one panel per function cluster plus one cross-cutting panel (transversal and Domain 7 content).
3. **Retranslation panel** for BARS (independent SMEs; `indicator_writing_rules.md` §10).

### 5.2 Panel size and composition

- Recruit 25 per panel, expecting about 20% attrition, for 15–25 completing all rounds.
- With N = 15, an item needs 12 "essential" ratings (exact CVR ≥ .60); N = 20 needs 15 (CVR ≥ .50); N = 25 needs 18 (CVR ≥ .44) [E: computed by exact one-tailed binomial, α = .05, per IO-066's method; `analysis/observability_summary.json`].
- **The v1 Delphi design (about 30 panelists, 3–5 reviewers per competency) cannot support CVR decisions.** With 5 reviewers every one must rate "essential"; with 3, no result reaches significance [E: computed].
- Composition: the §3.4 caps, plus at least 20% early-career members, at least 20% members who have moved between sector actors (CM), and representation from both federal and state agencies in every panel for the federal/state release.
- SME qualification criteria are documented per member: current or recent performance of the work, supervision of it, or training others in it. Conflicts of interest are recorded.

### 5.3 Items and rating formats per round

| Item type | Rating(s) |
|---|---|
| Competency (title + definition) | Essential / useful but not essential / not necessary (Lawshe) for the function cluster; clarity 1–4 |
| Level span | Lowest and highest level at which the work exists (A, L1–L5) |
| Indicator | Level placement (A, L1–L5, or "not a real performance"); observability (directly / with specification / not observable); essential-useful-not necessary |
| v1 Delphi flags (contested tag decisions) | Structured choice plus rationale |

Required comments: any "not necessary" or "unclear" rating, and any placement two or more levels from the round median.

### 5.4 Consensus thresholds and stopping rules (to be pre-registered) [J; anchored in IO-062, IO-063, IO-064, IO-065, IO-066, IO-069]

| Decision | Rule |
|---|---|
| **Retain** | CVR ≥ the exact critical value for the responding N (one-tailed α = .05) **and** ≥ 75% "essential" or "useful" |
| **Exclude** | ≥ 75% "not necessary", or, in the final round, < 50% "essential" or "useful" |
| **Revise** | Neither retain nor exclude. One wording revision is allowed; the revised item re-enters the next round |
| **Clarity** | ≥ 80% rate 3–4; otherwise the wording is revised |
| **Level placement** | ≥ 70% of panelists at the modal level **and** IQR ≤ 1 level |
| **Selection-use designation** (indicator) | Retained **and** ≥ 75% "directly observable" **and** OBS-4 = 3 by two independent coders |
| **Stability** (item stops) | Consensus reached, **or** ≤ 15% of panelists change category between rounds (no significant shift on a Wilcoxon signed-rank test) |
| **Hard stop** | After Round 3. Items without consensus are published as "no consensus" with their distributions, never forced |
| **Actor divergence** | If overall consensus is reached but a sector-actor subgroup (n ≥ 5) differs by ≥ 25 pp on essential+useful, flag `actor-variant` for CA |
| **Attrition** | Report per round; flag any panel with < 70% retention; compare dropouts with completers by sector actor and craft |

Common Delphi practice uses about 75% agreement, but many studies don't pre-specify it. That gap is exactly what reviewers attack [E-u: IO-064].

The content validity index (I-CVI ≥ .78) was considered as an alternative to CVR [E-u: IO-086]. CVR is kept as primary because the decision being made is *essentiality* for the job, which is what Lawshe's item asks. CVI may be reported alongside it for relevance ratings.

### 5.5 Feedback between rounds

Each panelist sees:
- distribution, median and IQR;
- CVR;
- anonymized verbatim comments;
- their own previous rating.

Show subgroup breakdowns only when the divergence rule fires, to limit conformity pressure [J; IO-069]. If an LLM summarizes free-text comments, a human checks the summary against the verbatim comments, the verbatim comments stay available, and the use is disclosed in the report (ACCORD) [J; IO-063].

### 5.6 Reporting

Report against **CREDES** and **ACCORD**. Include:
- rationale for the method and panel selection;
- consensus definitions set a priori;
- number of rounds and the feedback given;
- response and attrition by round;
- handling of non-consensus;
- steering-group roles and conflicts;
- any AI use in item drafting or synthesis [E-u: IO-062, IO-063].

## 6. Linkage studies

1. **Task ↔ competency.** SMEs (≥ 7 per cluster, not the same people as the Delphi panel where avoidable) rate each retained task × candidate competency: 0 not needed · 1 helpful · 2 essential. A link is **established** if mean ≥ 1.5 or ≥ 60% rate 2. A competency is **job-related for a function cluster** only if it has an established link to at least one *critical* task (§4.3). Competencies with no such link stay in the taxonomy for description and development but may not be used for selection in that cluster [J; IO-020 §14C; IO-079].
2. **Indicator ↔ task.** Each indicator cites the task(s) it evidences (`indicator_writing_rules.md` §12).
3. **Assessment ↔ indicator (blueprint).** Every assessment component maps to indicators. Report coverage: the share of critical tasks and essential competencies the assessment samples.
4. **Knowledge element ↔ indicator.** Each knowledge element links to the indicator(s) it enables. Knowledge tests sample only linked elements.
5. Linkage reliability: ICC(2,k) of linkage means, target ≥ .75 [J].

## 7. Tagging reliability, including LLM-assisted tagging

### 7.1 Human reliability (all published tags)

| Item | Specification |
|---|---|
| **Dimensions** | Craft (§7.3); work function or stage; actor relevance; exposure dimensions (automation type, tacit density, career-ladder position, vector, horizon); ethical lenses (if retained); indicator level placement; OBS-4 codes. Profession-family Core/Supporting should be **replaced by job-analysis survey importance data** (§4), not re-tagged by analysts [J] |
| **Codebook** | Definitions, decision rules, worked examples, and boundary cases taken from v1's Delphi flags (e.g., 2.3.2 drone operation; LCA producer vs. consumer; 7.2.3 S5/S6). Coders receive frame-of-reference training, which improves the accuracy and agreement of competency inferences [E-u: IO-042] |
| **Design** | Gold set of **≥ 150 tasks and ≥ 60 competencies per dimension**, stratified by domain, actor and v1 value, with ≥ 10 units per category (merge rare categories, or oversample them). Two independent human coders per unit (three for craft); a third adjudicates |
| **Statistic** | Krippendorff's α with the metric suited to each dimension (nominal: automation type, vector, stage; ordinal: tacit density, horizon, level; interval: craft weights), with bootstrap 95% CIs (≥ 1,000 resamples), confusion matrices and per-category agreement [E-u: IO-067, IO-068] |
| **Decision rule (pre-register; apply to the lower CI bound)** | ≥ .800 → production. .667–.800 → publish aggregates only, labelled "tentative", with two-coder consensus behind every published value. < .667 → revise the codebook or collapse categories and re-test; after two failed iterations, drop the dimension or demote it to descriptive notes [E-u: IO-067] |

**Why the CI matters:** with 40 units, α's 95% sampling range is about ±0.15, too wide to separate .667 from .800. With 120–200 units and 6 raters it narrows to about ±0.04–0.07 [E: simulation, `analysis/alpha_precision_simulation.py`].

**v1 baseline:** v1 tags have no inter-rater evidence.
- Same-rater, version-to-version agreement on D6 exposure codes was 95% (automation type), 93% (tacit density) and 89% (career-ladder position).
- 11 of 222 CLD flags (5%) contradict v1's own deterministic rule.
- Out-of-vocabulary codes (Yes/No, Y/N, "Highest", "Ungraded") appear [E: IO-001, IO-002, `analysis/observability_summary.json`].

Those are consistency checks, not reliability evidence. They are not a substitute for it.

### 7.2 LLM-assisted tagging with human verification

The aim is to use LLMs where they are measurably as good as humans, and never to let them silently set consequential values. The protocol responds to the failure mode v1 itself identified: the AI "will confidently resolve ambiguous cases without flagging them as ambiguous" [E: IO-009]. It also draws on the automation-bias and pre-annotation literature [E-u: IO-070, IO-071, IO-072] and LLM-annotation validation practice [E-u: IO-073, IO-074].

1. **Freeze and log.** Model identifier and version, system prompt, codebook version, decoding settings and retrieval context are hashed and stored with every LLM-produced tag (DE/IA).
2. **Separate development from evaluation.** Prompts and rules are tuned only on a development set. The gold evaluation set is **held out and never seen by whoever tunes prompts**.

   This session shows why it matters. A rule-based coder written while looking at the 43-competency sample agreed with manual codes at κ = .79 (quadratic-weighted .91) *in sample*. On a held-out set of 6 competencies (189 statements) it fell to κ = .69 (QWK .83) [E: `analysis/observability_summary.json`]. Agreement measured on tuning data overstates real performance.
3. **Metrics** (per dimension):
   - α(LLM, adjudicated gold);
   - α among human coders;
   - α of the pooled coder set with and without the LLM (does adding the LLM lower group agreement?);
   - per-category precision and recall;
   - **calibration** of the LLM's stated confidence (does confidence predict correctness?);
   - **run-to-run consistency** (≥ 3 runs; α across runs).
4. **Acceptance gates:**
   - The LLM may serve as **first coder** for a dimension if α(LLM, gold) is no more than .05 below the human–human α (non-inferiority margin) **and** its lower CI bound is ≥ .667.
   - It may serve as **sole coder** for a *descriptive* dimension only if α ≥ .80 and the audit stream (step 5) shows no drift.
   - It is **never sole coder** for any value that feeds selection, promotion, qualification or published workforce statistics [J].
5. **Human-verification design to detect and limit automation bias:**
   - **Blind audit stream:** a random 20% of units is coded by humans *without* seeing the LLM output.
   - **Anchoring index** = humans' agreement with the LLM when shown its output, minus their agreement when blind. If it exceeds 10 pp without a matching gain in accuracy against gold, anchoring is present: raise the blind share, retrain verifiers, and slow throughput.
   - **Seeded errors:** 5–10% of displayed LLM suggestions are deliberately wrong (logged and reversed afterwards). Verifier catch-rate target ≥ 80%; below that, pause and retrain.
   - **Abstention:** the LLM must be allowed to answer "ambiguous" or abstain, and must give a rationale. Abstentions, low-confidence outputs and LLM–human disagreements go to two-human coding.
   - **Workload limits:** cap items per verifier-hour and rotate dimensions, because vigilance and complacency effects grow with monotonous verification [E-u: IO-071].
   - **Provenance per tag:** coder types; decision path (LLM-accepted / LLM-overridden / human-only); verifier ID (pseudonymous); timestamp.
6. **Drift.** Re-run the evaluation set on any model or prompt change, and at least every 6 months. An α drop > .05 holds the pipeline.
7. **Disclosure.** Every release states, per dimension, the share of values that were LLM-first and human-verified, and the measured agreement.

### 7.3 Craft-weight reliability pilot (answers CA Q2; decides DP-5)

**Question:** can raters reliably produce task-level craft weights, and are they more reliable than (a) a 3-level ordinal per craft or (b) competency-level craft ratings?

| Design element | Specification [J unless marked] |
|---|---|
| **Units** | **150 tasks**, stratified: 50 per v1 primary craft; ≥ 40% from subsectors beyond public lands and forestry (DB); ≥ 20% known boundary cases (v1 Delphi flags); ≥ 20% from Domain 3 tasks that v1 inferred rather than transcribed. Plus **40 competencies** for the competency-level comparison arm |
| **Raters** | **12 humans** in two groups of 6: (a) trained taxonomy raters; (b) practitioner SMEs balanced across FC/DC/SC backgrounds and ≥ 4 sector actors. Fully crossed within group (every rater rates every unit). Plus an **LLM arm**: one frozen model, 3 independent runs |
| **Formats** (within-subject, counterbalanced) | **F1 constant-sum:** distribute 100 points across FC/DC/SC by how much each is *irreducible* to doing the task (v1 irreducibility test as the anchor). **F2 ordinal:** for each craft, none / supporting / defining. A derived "defining craft" (nominal) comes from both. Each rating carries confidence (1–5). Half the raters do F1 first. The second format comes after ≥ 10 days, with task order re-randomized |
| **Training** | 60-minute frame-of-reference session; 10 practice tasks with feedback, excluded from analysis [E-u: IO-042] |
| **Burden** | About 60–90 s per task per format: roughly 3–4 hours per rater per format, paid or on-duty |
| **Statistics** | Per craft: ICC(2,1) and ICC(2,k), absolute agreement, and interval α for F1; ordinal α for F2; nominal α for defining craft. Bootstrap 95% CIs. Spearman–Brown projection of the raters needed for ICC ≥ .80. LLM: ICC between LLM mean and human panel mean; run-to-run α; non-inferiority versus the average single human. Group (a) vs. (b) difference |
| **Precision** | 150 units × 6 raters gives a 95% sampling range of about ±0.05 for α ≈ .8 (interval) and about ±0.06 for a 3-level ordinal [E: simulation] |
| **Caution** | Collapsing a continuous judgment into 3 ordinal categories *lowers* α: latent single-rater reliability .80 becomes ordinal α ≈ .68 in simulation [E: simulation]. The ordinal fallback is not automatically "more reliable"; only the head-to-head comparison settles it |
| **Decision rules (pre-register)** | (1) If F1 per-craft ICC(2,k=3) has a lower CI bound ≥ .80 and is ≥ F2: **adopt weights**, with 3 raters per task in production. (2) Else if F2 ordinal α(k=3 consensus) has a lower bound ≥ .667: **adopt ordinal**, labelled tentative. (3) Else if defining-craft nominal α ≥ .667 but weights and ordinal fail: store **defining craft only** at task level. (4) If competency-level ratings beat task-level ratings by ≥ .10 α: report to CA as evidence for §7 "move toward Option A". (5) LLM arm passes the gate → LLM as first coder with human verification (§7.2) |
| **Timeline and cost** | 6–8 weeks, including recruitment. Feasible in the NGO pilot phase |

## 8. Assessment development and criterion-related evidence

### 8.1 Methods by use

[E-u: IO-049, IO-050, IO-052, IO-053, IO-055]

| Use | Preferred methods | Notes |
|---|---|---|
| Selection (federal and state) | Structured interviews with BARS; work samples and job simulations; job-knowledge tests built from knowledge elements; SJTs for judgment-heavy competencies; SME-QA résumé review against L-level indicators | Structured interviews and job-knowledge tests have among the highest current validity estimates. Years of experience have among the lowest [E-u: IO-049, IO-046] |
| Promotion | Work-product portfolios scored with rubrics; assessment centers for L4–L5 governance competencies; structured interviews | Follow assessment-center guidelines (dimensions defined by behavior, multiple exercises, trained assessors) [E-u: IO-055] |
| Training and qualification | Task books with entrustment-supervision ratings; observed practice; AI-off/AI-on paired tasks; seeded-error validation exercises | NWCG task books provide a working, sector-native model [E-u: IO-056, IO-057] |

### 8.2 Reliability of assessment scores

- Structured-interview and work-sample scoring: inter-rater ICC(2,k) ≥ .80 for operational decisions, ≥ .70 for development use [J].
- Task-book entrustment ratings: target ≥ .70 agreement between two evaluators on the same trainee, sampled in at least 10% of sign-offs.
- Knowledge tests: internal consistency ≥ .80 and item analysis; differential item functioning (DIF) review when subgroup n allows.

### 8.3 Criterion-related evidence

**When it is required [J; IO-020, IO-023]:**
- (a) high-volume selection use across agencies;
- (b) constructs that content validity can't carry (judgment, collaboration, integrity);
- (c) adverse impact is found and alternatives must be compared.

**Design:**
- Concurrent study with incumbents first, then predictive where feasible.
- Criteria collected **for research only**: BARS performance ratings by supervisors trained for the study; objective indicators (QA error rates, inspection-report quality scored blind, task-book completion time).
- Sample size: n ≈ 194 to detect r = .20 at α = .05 (two-tailed), power .80; 154 one-tailed; 124 for r = .25 [E: computed]. Few single agencies have that many incumbents in one job family, so plan **consortium studies** (UGESP cooperative studies) and **transportability** across agencies and states [E-u: IO-020, IO-089].
- **EMST's distinctive contribution:** validated task profiles are exactly the job-similarity evidence that transportability and validity-generalization arguments need. A state agency can show its environmental specialist job matches the task profile on which an assessment was validated elsewhere [J].

### 8.4 Standard-setting

Cut scores are set by an SME panel using a documented method (modified Angoff for knowledge tests; body-of-work or contrasting-groups for work samples), anchored to the minimally acceptable performance at the required level, with an adverse-impact review before adoption [J].

## 9. Fairness and adverse-impact monitoring

1. **Content stage:** a bias and sensitivity review panel (diverse; includes accessibility review and TN advice on Indigenous-related content) screens every indicator for B11/B12 constructions (`indicator_writing_rules.md` §7), for opportunity-gating (O flag), and for cultural or linguistic loading.
2. **Assessment stage:** collect voluntary applicant self-identification where lawful. At each hurdle compute impact ratios (four-fifths), a significance test (Fisher exact or two-proportion Z) and a practical-significance measure (shortfall), plus age 40+, and intersectional analysis where n permits [E-u: IO-020, IO-098].
3. **Triggers:** an impact ratio < .80 with p < .05, or < .80 for two consecutive cycles, prompts a search for less discriminatory alternatives of comparable validity, with the review documented.
4. **AI in assessment:** where AI scores or screens, apply SIOP's AI-assessment recommendations [E-u: IO-024]. Check the jurisdiction's requirements: NYC Local Law 144 bias audits; Illinois's 2026 AI-in-employment amendments; Colorado's AI Act, if in force; California's automated-decision-system regulations (effective October 2025) [E-u: IO-033 to IO-036; status unverified, CP to confirm].
5. **Legal context [J; status to verify, FH/CP]:**
   - Federal enforcement priorities shifted away from disparate-impact theories in 2025 (EO 14281) [E-u: IO-026].
   - EEOC removed its AI-selection technical assistance in January 2025 [E-u: IO-027].
   - Executive Order 11246 was revoked (EO 14173), ending OFCCP affirmative-action enforcement [E-u: IO-028].
   - **None of this removes** Title VII's statutory disparate-impact provision, private rights of action, state anti-discrimination law, or the federal requirement that employment practices rest on job analysis and comply with UGESP [E-u: IO-020, IO-022, IO-029].

   Monitoring is both legal protection and a test of the theory of change: a tool meant to open mobility that screens out non-traditional movers has failed on its own terms.

## 10. Documentation package for legal defensibility

| # | Record | Owner | Keep |
|---|---|---|---|
| D1 | Job-analysis report: methods, frame, weights, instruments, response, ratings, reliability, retention decisions | IO / DE | Life of use + 5 y [J] |
| D2 | SME rosters with qualifications, demographics (aggregate), conflicts | IO | same |
| D3 | Pre-registration, deviations log, Delphi round data, CVR tables, comments | IO / DE | same |
| D4 | Linkage matrices (task–competency, indicator–task, assessment blueprint) | IO | same |
| D5 | Assessment development: item and exercise writing, BARS retranslation, pilot statistics, scoring keys | IO / employer | same |
| D6 | Standard-setting record | employer + IO | same |
| D7 | Validity evidence (content, criterion, transportability) per use | IO / employer | same |
| D8 | Adverse-impact analyses, alternatives considered, decisions | employer | per UGESP 1607.15 and record-keeping rules; California ADS rules require 4 years for covered systems [E-u: IO-020, IO-036] |
| D9 | Accommodation procedures and counts | employer | same |
| D10 | AI documentation: model and version, prompts, evaluation results, drift checks, disclosure | IA / DE | same |
| D11 | Version and provenance: every indicator and tag traceable to source, author type, validation status | DE | permanent (repo) |

## 11. Maintenance and revalidation (replaces v1's single-analyst sentinel design)

- **Annual sentinel survey:** a short form, with the §4.1 "changed in past 12 months" and "AI/automation in workflow" items for the 20–30 highest-exposure tasks per cluster. It goes to a standing panel recruited under the §3.4 caps. Coding follows §7.2, never single-analyst-only.
- **Revalidation triggers:**
  - ≥ 20% of a cluster's respondents report material change in a task;
  - a regulatory change affecting a jurisdiction-variable standard (SC/FH/SL);
  - a tool-frontier shift flagged by FS/LM;
  - an adverse-impact trigger.

  Any trigger leads to a targeted re-rating of level placement and augmentation mode for affected competencies.
- **Full job-analysis refresh** at least every 5 years per function cluster, in line with certification-industry practice-analysis expectations [J; IO-106].

## 12. Sample sizes and timeline; NGO pilot vs. federal/state rollout

| Phase | Months | Activities | Sizes | What it can support |
|---|---|---|---|---|
| **0 Setup** | 0–2 | Pre-registration; codebooks; instrument build; approvals (§2); recover v1 truncated and D5 indicators (DE) | n/a | n/a |
| **1 NGO pilot** | 2–7 | Craft-weight pilot (§7.3); OBS-4 double-coding of v1 sample (2 humans; 1,354 statements already single-coded in `v1_observability_ratings.csv`); LLM-tagging gate test on 2 dimensions; 1–2 Delphi panels (cross-cutting + one function cluster); pilot survey; cognitive interviews; task-book pilot with entrustment ratings in 2–3 organizations | 150 tasks × 12 raters; Delphi 15–25 per panel; survey 100–200; interviews 10–15 | **Describe** and **develop** uses within pilot organizations; method calibration; **no selection use** |
| **2 Federal/state content validation** | 6–15 | Job-analysis survey for 3–5 priority function clusters with FH/SL partner agencies; Delphi for those clusters; linkage studies; BARS development | ≥ 30 incumbents + 10 supervisors per actor × cluster cell (about 400–1,000 per cluster); Delphi 6–8 panels | Describe, develop, and **content-valid selection content** for agencies whose own job analysis confirms it |
| **3 Assessment and criterion evidence** | 12–24 | Build assessments for 2–3 priority roles; concurrent validation (consortium); standard-setting; baseline adverse-impact analysis | n ≥ 150–200 per job family (consortium) | Selection and promotion use, with documented validity |
| **4 Maintenance** | ongoing | Annual sentinel; triggered revalidation; 5-year refresh | standing panel 60–100 | Change signals; currency |

**What the NGO pilot can and cannot do [J].**
- **Can:** test instruments, codebooks and the LLM pipeline; estimate reliability; refine indicators; and validate content for *development* use in pilot organizations.
- **Cannot:** generalize to federal or state jobs (different work, authorities and legal requirements), support selection, or stand in for agency job analysis. NGO results should be labelled "pilot evidence, NGO context".

## 13. Responsibilities

| Area | Lead | Contributing roles |
|---|---|---|
| Method, instruments, analysis | IO | n/a |
| Federal partner agencies, OPM alignment, SME-QA integration | FH | n/a |
| State partners and merit-system rules | SL | n/a |
| Tribal participation protocol | TN | real consultation required |
| LLM pipeline, gold-set tooling, drift | IA | n/a |
| Data, provenance, registry, release | DE | n/a |
| Task books, entrustment, learning-use evidence | LC (with IO) | n/a |
| Mover sub-sample, workforce-voice cognitive interviews | CM | n/a |
| Approvals, privacy, accessibility, PRA | CP | n/a |
| Steward and partner recruitment | AS | n/a |
| Decisions on thresholds and dispositions | CA | n/a |
