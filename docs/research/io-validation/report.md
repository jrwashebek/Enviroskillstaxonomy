# IO Report: Making EMST v2 Valid, Measurable and Defensible

**Role:** Industrial-Organizational Psychologist, Job Analysis & Validation (IO) · **Phase 2** · **Date:** 2026-10-23
**Folder:** `docs/research/io-validation/`
**Deliverables:**
- `proficiency_model_v2.md`
- `indicator_writing_rules.md`
- `exemplar_rewrites.csv` (14 competencies, 85 indicators)
- `validation_protocol.md`
- `v1_assessment.csv` (30 verdicts)
- `candidate_competencies.csv` (3)
- `ecosystem.csv` (25)
- `sources.csv` (82)
- `v1_observability_ratings.csv` (1,354 manually coded statements)
- `v1_observability_population_rulecoded.csv` (6,268 statements)
- `analysis/` (reproducible scripts, rating files, `observability_summary.json`)

**Evidence labels.** **[E]** marks evidence read or computed in this session from v1 data and documents on disk. **[E-u]** marks evidence from a published source I know but **could not re-retrieve this session**. **[J]** is expert judgment. **[S]** is speculation.

**Evidence limit, stated up front.** The team-wide WebSearch budget was exhausted before my first search, and WebFetch requests to `ecfr.gov` and `opm.gov` were blocked pending approval. I could not verify the *current* (October 2026) status of any law, regulation, standard or program. All external sources carry `status = unverified` in `sources.csv`, and `[E-u]` maps to `E` in the CSVs. My knowledge runs to about mid-2026. Anything that may have changed since (OPM implementation of the Chance to Compete Act, EEOC actions, state AI laws, revision of the AERA/APA/NCME Standards, SIOP editions, NWCG modernization) is flagged for FH, SL or CP to verify. The v1 appraisal (§3) does not depend on the web: it is computed from the repo.

---

## 1. Summary

**Verdict on v1 measurement.** v1 is a strong *descriptive* taxonomy. In its current form it can't carry hiring, promotion or qualification decisions. Five findings drive that:

1. **Proficiency levels are tenure bands** (0–2, 3–5, 6–10, 10+ years). Years of experience predict job performance weakly, and minimum-years thresholds carry adverse-impact and age risk [E-u: IO-046, IO-049].
2. **Observability falls as stakes rise.** In a blind, stratified sample of 1,165 statements from 43 competencies (all 7 domains, all 3 crafts, 38 skill areas), 29.9% are directly observable, 41.7% need specification, 13.0% are inferred mental states and 15.4% cannot be assessed as individual performance. Direct observability falls from 56% at Foundational to 5% at Expert. Not individually assessable rises from 0% to 61% [E: IO-010].
3. **Levels are templates.** 211/222 Expert Knowledge statements start "Shapes…". 217/222 Advanced Knowledge statements start "Expert in…". On average, 81% of each competency's Expert-level statements match a few boilerplate frames [E: IO-010].
4. **Measurement content is missing.** Domain 5 has zero indicators in every database version (a parse defect), and 2,104 of the 6,484 source-text indicators (32%) never reached the database [E: IO-002].
5. **No tag has any reliability evidence.** v1 explicitly decided that an AI-augmented single analyst needed none [E: IO-009]. Even deterministic rules were misapplied: 11/222 career-ladder-destruction (CLD) flags contradict their own rule [E: IO-001].

**v2 proficiency model in brief.**
- Five responsibility-anchored levels (L1 Supervised · L2 Independent · L3 Senior · L4 Lead/Expert · L5 Strategic), plus an "Awareness" knowledge bundle that is not a level.
- Levels are defined on seven generic attributes. Five parallel SFIA and the federal Factor Evaluation System (FES): autonomy, guidelines and judgment, complexity, scope and influence, knowledge. Two are new: augmented practice and formation of others.
- Each competency is defined only within its **level span**, using 2–5 behavioral indicators per level written to a condition/standard/evidence pattern.
- Knowledge, credentials and tools move to separate layers. Years become descriptive data only.
- Performing *with* AI is part of the standard: every indicator carries an `augmentation_mode` (unaided / assisted / supervisory), with verification behavior built into the standard and AI-off/AI-on assessment where career-ladder formation is at risk.
- Levels relate to grades and pay bands through **position profiles**, never equivalence tables.

**Validation protocol essentials.**
- **Tasks first.** Competencies earn job-relatedness by linkage to critical tasks.
- **Composition correction for contraction bias.** Over-recruit thinned public field and statecraft strata, include recently separated incumbents, cap any sector actor at 30% of a Delphi panel, and rake and test the weights.
- **Pre-registered modified Delphi.** 15–25 members per panel, exact Lawshe critical values, 75% agreement, level placement at ≥70% modal with IQR ≤ 1, a ≤15%-change stability rule, a hard stop after Round 3, and CREDES/ACCORD reporting.
- **Krippendorff's α gates for every tag,** decided on the lower bound of the confidence interval (≥.80 production; .667–.80 tentative).
- **LLM-assisted tagging only behind gates.** Held-out gold sets; a non-inferiority gate; a blind audit stream that measures anchoring; seeded errors; abstention.
- **Linkage studies, criterion and transportability evidence, adverse-impact monitoring, and an 11-part documentation package.**

**Biggest trade-off.** Defensibility against speed and coverage. Doing this properly shrinks v2.0 to the competencies that pass the gates, with selection-use content arriving 12–24 months later than a "publish everything" release would claim. I recommend the smaller, honest release (§9).

## 2. Standards, law and practice: what binds EMST v2 (and current status)

### 2.1 Uniform Guidelines on Employee Selection Procedures (UGESP)

**What it requires.** UGESP (29 CFR 1607, adopted jointly by EEOC, DOL, DOJ and the predecessor of OPM) governs any "selection procedure" used for hiring, promotion or referral, including training-and-experience screens [E-u: IO-020, IO-021]. Three provisions bear directly on EMST:

- **§1607.14C (content validity):**
  - requires a job analysis of important work behaviors;
  - requires knowledge, skills and abilities to be operationally defined and used in observable work behaviors;
  - states that a procedure based on inferences about mental processes cannot be supported solely or primarily on content validity [E-u: IO-020].

  v1 statements such as "Understands…", "Expert in…" and "Shapes understanding of…" fail that test directly.
- **§1607.4D (adverse impact):** the four-fifths rule, plus significance testing, which practitioners pair with it [E-u: IO-098].
- **§1607.7–8 (transportability and cooperative studies):** they let agencies share validity evidence when jobs are shown to be similar. EMST task profiles could supply that job-similarity evidence (§8.3 of the protocol) [J].

**Status [J; verify].** To my knowledge UGESP is still in force; OPM incorporates it for federal employment through 5 CFR 300.103(c) [E-u: IO-022]. What changed in 2025 is *enforcement posture*, not the rule text, as far as I know:
- EO 14281 directed agencies to deprioritize disparate-impact enforcement [E-u: IO-026];
- EO 14173 revoked EO 11246, ending OFCCP affirmative-action enforcement and putting the DOL copy of UGESP (41 CFR 60-3) in question [E-u: IO-028].

Title VII's statutory disparate-impact provision (42 U.S.C. 2000e-2(k)) is unaffected, as are private suits and state anti-discrimination law [E-u: IO-029]. **Implication:** EMST should design to the UGESP standard regardless of federal enforcement, for three reasons:
1. it remains the legal benchmark in litigation;
2. state law and private plaintiffs remain;
3. a mobility tool that screens out non-traditional movers defeats the theory of change.

### 2.2 SIOP Principles and SIOP guidance on AI-based assessments

- The **SIOP Principles (5th ed., 2018)** are the professional standard for validation strategies, job analysis, fairness and documentation [E-u: IO-023]. I know of no 6th edition, but CP or FH should check.
- **SIOP's AI-assessment recommendations (January 2023)** apply the same validity and fairness logic when AI scores or screens candidates, and add documentation and monitoring expectations [E-u: IO-024].

For EMST, the professional standard matters more than the enforcement climate. It is what an expert witness would apply, and what agency assessment psychologists will check.

### 2.3 AERA/APA/NCME Standards for Educational and Psychological Testing

The 2014 edition is current to my knowledge. A revision has been discussed and may be under way; status unverified [E-u: IO-025]. Its central principle, that **validity attaches to interpretations of scores for specific uses**, drives the protocol's per-use validity argument [E-u: IO-025, IO-094, IO-095]. EMST should never describe itself as "a validated taxonomy" without naming the use.

### 2.4 Federal hiring under the Merit Hiring Plan and the Chance to Compete Act

- **Chance to Compete Act (Pub. L. 118-188, December 2024):** codifies job-analysis-based "technical assessments" for competitive hiring and supports sharing assessment results across agencies [E-u: IO-031].
- **OPM Merit Hiring Plan (May 2025):** pushes agencies toward technical assessments (SME-QA résumé review, structured interviews, work samples, written tests), away from relying on self-assessment questionnaires, and toward faster hiring [E-u: IO-030].
- Implementing regulations, later revisions and agency uptake are **unverified** (FH).

**What it means for EMST [J].**
1. Federal agencies *need* job-analysis content per series and position family. EMST can be the shared, documented bank that speeds that work up: task inventories, linkage-ready competencies, L-level indicators and BARS (`proficiency_model_v2.md` §8).
2. SME-QA puts line practitioners into rating applicants. That is an assessable competency v1 lacks (candidate **IO-C02**).
3. The Merit Hiring Plan's essay questions were controversial because of concerns about job-relatedness and political content [J; unverified]. That is a reminder that **every item EMST supplies must be traceable to a job-analysis link.** The integrity exemplar (7.1.3) is written so that it can't become a loyalty test: it assesses only work products and knowledge of procedures.

### 2.5 State and local merit systems

State civil-service systems vary in constitutional and statutory bases, examination rules, union contracts and how minimum qualifications are written (often still in years). For state and local agencies administering covered federal grant programs, 5 CFR 900 Subpart F sets a merit-system floor. Whether it reaches environmental programs is for SL to determine [E-u: IO-032; J].

**Implication [J].** EMST must work as content a state can adopt *through its own merit-system processes*, not as a federal overlay:
- demonstrated-competency substitution language for years-based minimums;
- position profiles that map to class specifications;
- job-analysis records a state examiner can incorporate.

### 2.6 EEOC posture on AI in selection (2025–26)

- In January 2025 the EEOC removed its AI-related selection technical assistance [E-u: IO-027].
- Enforcement priorities moved away from disparate-impact theories under EO 14281 [E-u: IO-026]. Later actions, including any after quorum changes, are unverified.
- Meanwhile **state and local AI-in-employment rules expanded**:
  - NYC Local Law 144 bias audits [E-u: IO-033];
  - Illinois HB 3773, effective January 2026 [E-u: IO-035];
  - California automated-decision-system regulations, effective October 2025 [E-u: IO-036];
  - Colorado's AI Act, with its effective date delayed [E-u: IO-034].

  Federal efforts to pre-empt state AI laws were reported in late 2025 [S; verify, CP].

**Implication [J].** Any LLM-assisted screening built on EMST must meet the strictest applicable jurisdiction. EMST's own LLM-assisted *tagging* is not a selection procedure, but it feeds content that may become one, which is why the protocol puts gates on it (§7.2).

### 2.7 Skills-based hiring outcomes

- The Burning Glass Institute / Harvard Business School study (Fuller, Langer, Sigelman, February 2024) found that announced removals of degree requirements changed actual hiring far less than the announcements implied [E-u: IO-037]. I could not check later updates.
- The lesson for EMST: **publishing skills language doesn't change who gets hired. Assessments that measure the skills, used at the decision point, do** [J]. That is why the CM outcome metric should be hires and promotions of cross-sector and non-traditional candidates through EMST-based assessments, not adoption of EMST vocabulary.

### 2.8 Competency modeling best practice

- Campion et al. (2011) give the canonical checklist: rigorous job analysis, defined proficiency levels with behavioral descriptors, appropriate granularity, linkage to outcomes, and keeping models current [E-u: IO-038].
- Earlier work documented the rigor gap between competency modeling and job analysis [E-u: IO-039, IO-040].
- **Competency inferences are more reliable when raters work from task information** [E-u: IO-041] **and receive frame-of-reference training** [E-u: IO-042].
- **Competency ratings inflate more than task ratings** [E-u: IO-043].
- Specific, observable descriptors are rated more reliably than abstract ones [E-u: IO-044, IO-045].

Together these give the empirical spine of my answer to CA Q1 (§8).

### 2.9 Assessment methods

The most current validity benchmarks (Sackett et al., 2022) put structured interviews and job-knowledge tests near the top and years of experience near the bottom [E-u: IO-049, IO-046].

| Method | What it is good for | Caveat |
|---|---|---|
| **BARS** (Smith & Kendall 1963 retranslation) | Scoring structured interviews and performance ratings [E-u: IO-051, IO-050] | Needs careful anchor development |
| **SJTs** | Judgment-heavy constructs, e.g., statecraft judgment and integrity procedures [E-u: IO-052] | Validity varies by construct |
| **Work samples** | Field and data craft performance [E-u: IO-053] | Subgroup differences can be larger than once assumed [E-u: IO-054] |
| **Assessment centers** | L4–L5 promotion decisions [E-u: IO-055] | Costly |

**Sector-native and analog models:**
- **NWCG Position Task Books** under PMS 310-1 are a working performance-based qualification system inside the environmental sector. They are the obvious template for EMST's training-use instrument [E-u: IO-056, IO-057].
- **ACGME Milestones 2.0** and **entrustable professional activities (EPAs)** show how to make developmental levels and entrustment decisions defensible through committee judgment over multiple observations [E-u: IO-058, IO-059, IO-060].
- **SFIA 9** shows responsibility levels with skills defined only where practised [E-u: IO-061]. v1's own methodology research recommended the same [E: IO-004].

### 2.10 Delphi and consensus reporting

- **CREDES** (2017) and the newer **ACCORD** guideline (2024) define reporting expectations [E-u: IO-062, IO-063].
- A systematic review found the median Delphi consensus threshold was 75%, often not pre-specified [E-u: IO-064].
- Lawshe's CVR (1975) is the canonical content-validity statistic. Its original critical-value table should be replaced by exact binomial values (Ayre & Scally 2014), which I computed (`analysis/`) [E-u: IO-065, IO-066; E: computed].

## 3. Appraisal of v1 measurement design

### 3.1 Method

- **Sample.** Stratified random draw of 43 of 222 competencies: 6 per Domain 1–6, all 7 of Domain 7, all three crafts, 38 skill areas, seeded for reproducibility. Every Knowledge, Application and indicator statement at all four levels was included: **1,165 statements** (Domain 5 contributes Knowledge/Application only, because of the parse defect).
- **Rubric.** OBS-4, as documented in `indicator_writing_rules.md` §2:
  - 3 = direct;
  - 2 = needs specification;
  - 1 = inferred state;
  - 0 = not individually assessable;
  - plus flags: P proxy, C compound, O opportunity-dependent, T tool-locked.
- **Rater.** I rated blind and alone. **I am an LLM agent, so this is a single-rater measurement subject to the critique I make of v1.** The figures are good enough to justify redesign but not to publish. Two trained humans should re-code `v1_observability_ratings.csv` (validation protocol, Phase 1).
- **Population check.** A rule-based coder written after the sample, then frozen, coded all 6,268 statements. A 6-competency holdout (189 statements), rated afterwards, measures its honest agreement: κ = .69 (quadratic-weighted .83), against κ = .79 in sample. That gap is itself a finding about tuning-set optimism (§3.6).

### 3.2 Results

| | Direct (3) | Needs spec. (2) | Inferred (1) | Not assessable (0) |
|---|---|---|---|---|
| **All statements** (n = 1,165) | 29.9% | 41.7% | 13.0% | 15.4% |
| Foundational | 56.2 | 14.7 | 29.1 | 0.0 |
| Intermediate | 42.2 | 49.7 | 7.8 | 0.3 |
| Advanced | 15.3 | 69.0 | 14.6 | 1.0 |
| **Expert** | **5.3** | 33.0 | 0.4 | **61.4** |
| Knowledge statements | 2.3 | 12.2 | 61.0 | 24.4 |
| Application statements | 16.3 | 60.5 | 0.6 | 22.7 |
| Indicators | 38.5 | 44.0 | 5.6 | 11.9 |

[E: IO-010; `analysis/observability_summary.json`]

- **Flags.** Proxies rise from 0.7% (F) to 22.1% (E). Opportunity-dependent statements rise from 0% (F) to 21.1% (A) and 38.9% (E). Compound statements are 11–18% at F to A. Tool-locked statements are 6–9% at F to A.
- **Assessable level content.** Share of competency-levels with at least one direct, non-proxy statement: **F 88% · I 88% · A 56% · E 2%** (1 of 43).
- **Population.** The frozen coder, which under-calls direct statements and so is conservative, gives the same shape across all 222 competencies: Expert 58% not assessable, Advanced 5% direct [E: IO-010].
- **By domain and craft.** Domain 5 scores lowest (6% direct; 50% "usable", meaning code ≥ 2 and not a proxy), because only its generic Knowledge/Application lines exist. Domain 7 and Domain 2 score highest (40% and 39% direct). Statecraft-primary statements are slightly less observable (26% direct) than field craft (35%) or data craft (30%). That fits the charter's concern about treating statecraft as a trait rather than a teachable competency, but the difference is small next to the level effect [E: IO-010; J].

### 3.3 Years-based levels

The source text labels the levels "(Entry-level, 0-2 years)", "(3-5 years)", "(6-10 years)", "(10+ years)" across all 215 source competencies [E: IO-002]. Used for selection, they:
1. rest on a weak predictor [E-u: IO-046, IO-047, IO-048];
2. create disparate-impact and age exposure that would need validation under UGESP [E-u: IO-020, IO-021];
3. conflict with OPM qualification and assessment rules [E-u: IO-030, IO-031];
4. penalize the discontinuous, cross-sector careers EMST exists to support [J].

**Verdict: retire** (`v1_assessment.csv`).

### 3.4 Job tasks

v1 has 666 tasks, three per competency. They are verb-led and close to O*NET style, which is a good starting point. Problems:
- only **7.5%** state a standard or protocol;
- **31%** are compound;
- **17.9%** name AI or a specific technology;
- **8%** lead with "Use…", treating the tool as the task;
- they were written top-down from competencies;
- about 76% of Domain 3 task text was inferred [E: IO-010, IO-005].

The brief's description of T1→T3 as foundational→advanced isn't borne out by v1's own career-ladder tags. Only 89 of 222 T1 tasks are tagged primary-learning, and only 11 T3 tasks are tagged specialist [E: IO-002]. **Verdict: carry as seed items for the job-analysis task inventory; confirm by incumbent ratings.**

### 3.5 Reliability of the exposure ratings and other tags

- **No inter-rater evidence exists.** The record shows a deliberate choice: for a single analyst using AI, "you don't need inter-rater reliability provisions" [E: IO-009]. In v1, "calibration" meant tuning the instrument to the analyst's own judgment [E: IO-007].
- **What can be computed is consistency, not reliability:**
  - Same-rater version-to-version agreement on Domain 6 tasks between the D6 working file and the reconciled database: automation type 95%, tacit density 93%, career-ladder position 89% (partly deliberate reclassification) [E: IO-002].
  - CLD rule violations in 11/222 competencies [E: IO-001].
  - Out-of-vocabulary values: True/False/Yes/No/Y/N; "Highest" and "Ungraded" severity [E: IO-001].
  - Ethical lenses populated for 4/222 [E: IO-001].
- **Verdict: needs evidence** before any exposure or tag statistic is published as more than analyst judgment (`validation_protocol.md` §7).

### 3.6 Lesson for LLM-assisted work (the method, turned on myself)

My frozen rule coder agreed with my manual codes at κ = .79 on the items I had seen while writing it, and κ = .69 on items I hadn't [E: IO-010]. The same thing happens when an analyst tunes an LLM prompt on the items used to judge it. Agreement on tuning data overstates real performance. This is why the protocol requires held-out gold sets and blind audit streams (§7.2).

## 4. v2 proficiency model (summary; full text in `proficiency_model_v2.md`)

1. **Four layers:**
   - (A) leveled performance indicators;
   - (B) knowledge elements, assessed by tests;
   - (C) qualification gates on positions (HAZWOPER, NWCG quals, licenses);
   - (D) tools, versioned fast.
2. **Five levels on seven attributes.** The attributes parallel SFIA [E-u: IO-061] and the FES factors [E-u: IO-080], so PD language translates without equating levels to grades. "Augmented practice" scales from *using approved tools under prescribed checks* (L1) to *governing AI and automation, including formation safeguards* (L5). "Formation of others" scales from *learns through supervised performance* to *protects entry cohorts organization-wide*. This puts v1's career-ladder-destruction finding into the level definitions themselves [J].
3. **Level spans with four publication rules:** the work exists, levels are distinct, the level is assessable, and there is consensus. An empty level is information, not a gap [J].
4. **Three resolutions of anchoring:**
   - generic descriptors, for classifying positions;
   - BARS, for selection and promotion;
   - entrustment-supervision ratings on task-book tasks, for training. These follow the NWCG and EPA models [E-u: IO-056, IO-059, IO-060].
5. **AI-augmented performance:** each indicator declares `augmentation_mode`. Assisted-mode standards include verification and accountable decision. Process-based scoring uses seeded errors, because AI compresses output differences between novices and experts [E-u: IO-075, IO-076]. Dual-condition assessment applies to CLD-flagged competencies, given evidence that unaided skill can decline after routine AI use [E-u: IO-077].
6. **Grades and bands:** position profiles (required level per competency) inform, but do not determine, classification. No "L3 = GS-12" tables [J; FH and SL to own].

The exemplars (`exemplar_rewrites.csv`) show the model working across all seven domains and all three crafts: 5 FC, 4 DC and 5 SC competencies, 85 indicators, each with level, assessment method, mode, use class and v1 provenance. They include a merge (1.4.2 into 4.1.2), a correction of an apparent HAZWOPER content error (4.4.4), recovery of Domain 5 content from source text (5.2.1, with a sovereignty fix for TN), a reform-resilient regulatory competency (6.1.2), and an integrity competency written so it can't be scored as a trait (7.1.3).

## 5. Indicator-writing rules (summary; full text in `indicator_writing_rules.md`)

- **Sentence pattern:** one sentence of the form *observable verb + specific object + condition + standard*, at most 30 words, plus structured metadata (evidence types, assessment method, augmentation mode, use class, jurisdiction-variable flag, OBS-4 code, validation status, provenance).
- **Release thresholds:** selection or promotion use requires OBS-4 = 3 with no flags. Development use allows 2 with an evidence plan. Codes 0 and 1 are never released as performance indicators.
- **Twelve banned constructions with lint patterns,** for IA/DE to automate. Examples: internal-state verbs; level labels used as content; reputation and influence; proxies; outcome guarantees; empty verbs; compound performances; adjective-only gradation; vendor names; hard-coded jurisdiction rules; traits; non-job-related access requirements.
- **Fairness rules:** no tenure, no opportunity-gated indicators at selection levels, least-adverse alternative, accommodation for AI-permitted tasks.
- **Level-differentiation rule:** adjacent levels must differ on a *named* attribute, not on adjectives.

## 6. Validation protocol (summary; full text in `validation_protocol.md`)

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