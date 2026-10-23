# EMST v2 Indicator-Writing Rules

**Role:** IO (Industrial-Organizational Psychologist, Job Analysis & Validation) · **Status:** proposal for CA decision · **Date:** 2026-10-23
**Companion files:** `proficiency_model_v2.md` (the level model these indicators sit in), `exemplar_rewrites.csv` (15 v1 competencies rewritten to this standard), `validation_protocol.md` (how indicators are validated), `report.md` §3 (why v1 indicators fail).

Evidence labels follow TEAM_BRIEF §3: **[E]** cited evidence, **[J]** expert judgment, **[S]** speculation. Source IDs resolve to `sources.csv`. **[E-u]** marks evidence from a published source the author knows but could not re-retrieve in this session (web search budget exhausted, fetches blocked). It maps to `E` in the CSVs, with `status = unverified` in `sources.csv`. **[E]** without the suffix means evidence read or computed in this session from v1 data and documents on disk.

---

## 1. Why rules are needed

An indicator is the smallest unit the EMST asks a hiring manager, assessor, trainer or learner to *see*. If it can't be observed, it can't be scored reliably. If it can't be scored reliably, it can't support a content-validity argument. Without that argument it can't legally carry weight in selection.

- Under the Uniform Guidelines, content validity has to be shown against observable work behaviors. A procedure based on inferences about mental processes "cannot be supported solely or primarily on the basis of content validity" (29 CFR 1607.14C(1)) [E: IO-020].
- Job-analysis ratings of observable, specific descriptors are more reliable than ratings of abstract or trait-like descriptors [E: IO-044, IO-045].
- Competency-level ratings inflate more than task-level ratings [E: IO-043].

In v1 the problem is measurable. In a blind, stratified sample of 1,165 statements from 43 competencies, only **29.9%** were directly observable. **15.4%** could not be assessed as individual performance at all, and that share rose to **61.4%** at the Expert level [E: IO-010; `report.md` §3]. These rules exist so v2 does not repeat that.

## 2. The observability acceptance test (OBS-4)

Every v2 indicator is scored with this rubric before release. The same rubric produced the v1 figures, so v1 and v2 can be compared directly.

| Code | Meaning | Test question for the reviewer | Example (v1 text) |
|---|---|---|---|
| **3 Direct** | A specific action on a defined object, producing a performance or product a trained assessor could verify against a standard (stated or professionally implicit) | "Could two trained assessors watching this person, or reading this product, agree on whether it was done to standard?" | "Calculates material balances identifying losses and waste" |
| **2 Needs specification** | Observable, but the object, scope or standard is too broad to assess consistently without more detail; usually needs a portfolio or extended work sample | "I can see that something was done, but not whether it was done *well enough*." | "Designs and implements monitoring programs" |
| **1 Inferred state** | Knowledge, understanding, awareness, familiarity, attitude or 'expertise' stated as a condition of the person, with no behavioral referent | "Is this something the person *is* rather than something they *do*?" | "Understands natural disturbance regimes" |
| **0 Not individually assessable** | Reputation, influence, field-level impact, status, tenure, or an outcome mostly controlled by others; or empty | "Would the score depend on other people's opinions, opportunities or decisions more than on this person's performance?" | "Shapes understanding of ecosystem theory"; "Achieves recognition for…" |

**Flags** (record in addition to the code):

| Flag | Meaning | Consequence |
|---|---|---|
| **P** Proxy | Uses a credential, publication, training completion, award or years of experience as the indicator | Move it to the *qualification gate* or *evidence source* layer. Never score it as performance. |
| **C** Compound | Two or more distinct performances in one statement | Split it |
| **O** Opportunity-dependent | Can only be shown by people who already hold a role, authority, budget or scale (e.g., "leads national initiatives") | Rewrite to a performance demonstrable at the person's scale. If it can't be rewritten, mark `use_class = develop` or `promote-with-history`, never `select` |
| **T** Tool-locked | Names a vendor, product, model or fast-moving technology as part of the competency | Move the tool to the tool layer. The indicator names the *function* |

**Release thresholds** (proposed; CA to ratify) [J: based on IO-020 §14C and IO-045]:
- An indicator with `use_class` including **select** or **promote** must score **3**, with no P, C, O or T flags.
- An indicator with `use_class = develop` may score **2** if it carries an explicit evidence plan (what product, which rubric).
- Codes **1** and **0** are never released as performance indicators. A code-1 statement can be reworded as an *enabling knowledge element* (§6), assessed by knowledge test.

## 3. Anatomy of a v2 indicator

An indicator is **one sentence** plus **structured metadata**. The sentence carries the performance. The metadata carries everything an assessor, HR system or curriculum designer needs.

**Sentence pattern:** `<Observable verb> <specific object/work product> [<condition>] [<standard>]`. No more than 30 words, in plain language, with the actor implied.

| Element | Question it answers | Good | Bad |
|---|---|---|---|
| **Verb** | What does the person *do*? | measures, classifies, drafts, verifies, negotiates, approves | understands, supports, leverages, ensures |
| **Object** | On what, producing what? | "a stream-reach macroinvertebrate sample", "a scope of work", "a fuels prescription" | "issues", "programs", "the field" |
| **Condition** | Given what inputs, tools, AI assistance, supervision or situation? | "from field plot data and an AI-generated draft", "under the direction of a qualified evaluator", "when site conditions differ from the plan" | (none stated, so level is ambiguous) |
| **Standard** | How good is good enough? | "so that results meet the program's QA/QC acceptance criteria", "within the agreement's stated tolerances", "with each conclusion traceable to cited evidence" | "effectively", "appropriately", "comprehensive" |
| **Evidence** *(metadata, not in the sentence)* | How would an assessor see it? | work product, direct observation, structured interview, simulation/SJT, knowledge test, record or task-book sign-off, multi-source feedback | n/a |

### Required metadata fields (for DE/IA schema)

`indicator_id` (stable) · `competency_id` · `level` (L1–L5) · `text` · `verb` · `object` · `condition` · `standard` · `evidence_types` (pipe list: `work-product|observation|interview|simulation|sjt|knowledge-test|record|task-book|msf`) · `assessment_methods` · `augmentation_mode` (`unaided|assisted|supervisory`; §5) · `use_class` (pipe list: `select|promote|develop|self-assess`) · `jurisdiction_variable` (true if the standard depends on federal, state, Tribal or local rules; then it links to a jurisdiction overlay instead of naming a rule) · `safety_or_legal_critical` (true/false) · `obs4_code` · `obs4_flags` · `validation_status` (`draft|sme-reviewed|delphi-retained|job-analysis-confirmed|criterion-supported`) · `provenance` (v1 key(s), source documents, authoring agent or person, and whether LLM-assisted) · `version`.

## 4. Verb guidance

**The verb does not set the level. The conditions and standard do.** A common failure in competency frameworks, v1 included, is the verb ladder (identify → apply → analyze → design → shape), where level comes from verb choice alone and the object and standard stay vague. v2 sets level through the seven generic attributes in `proficiency_model_v2.md` §4: autonomy, guidelines, complexity, scope, knowledge, augmented practice and formation of others. The lists below are *typical*, not mandatory [J].

| Typical at | Preferred observable verbs | Notes |
|---|---|---|
| L1 Supervised | collects, measures, records, labels, identifies (from a defined set), follows (a named procedure class), operates, calibrates (per procedure), checks (against a checklist), reports, prepares (a draft), enters, maintains (equipment or files) | Condition usually names the supervision and the procedure |
| L2 Independent | conducts, selects (from established methods), analyzes, interprets, drafts (for issue), verifies, troubleshoots, documents (rationale), schedules, applies (a named method or criteria set), explains (to a named audience) | Condition usually is "routine cases without step-by-step direction"; standard is the program's accepted method |
| L3 Senior | adapts, designs (a project-level plan or study), evaluates, reviews (others' work products), resolves (non-routine cases), negotiates, prioritizes, justifies, trains (others in a defined task), escalates (with documented basis) | Condition usually names the *non-routine* or *conflicting-evidence* situation |
| L4 Lead/Expert | develops (methods, criteria or standards for a program), sets (technical acceptance criteria), arbitrates, approves, audits, certifies (others' qualification), leads (a defined multi-party or high-consequence effort), designs (program-level systems) | Standard usually references defensibility under external review |
| L5 Strategic | establishes (organization-wide or cross-jurisdiction standards or policy), governs, allocates (resources across programs), sponsors (multi-organization efforts) with a defined decision record | Use sparingly; L5 indicators are almost always O-flag risks (§2) |

**Verbs to use with care** (each needs an explicit object and standard): *manages, coordinates, leads, develops, implements, integrates, evaluates*. These are fine with a concrete object ("coordinates a multi-agency field schedule for a prescribed burn window"). They fail without one ("coordinates partnerships").

## 5. Representing AI-augmented performance

v2 writes the standard for the work **as it is actually performed**, which increasingly includes AI and automation. It does so without letting the tool's output stand in for the person's competence [J; grounded in IO-075, IO-076, IO-077, IO-024].

1. **Every indicator declares an `augmentation_mode`:**
   - `unaided`: performed without AI or automated decision support. Use this when (a) the task is formation-critical (it builds the judgment needed to check AI later, per v1's career-ladder-destruction finding), (b) it is safety-critical or must be done where tools fail (field, incident, no connectivity), or (c) the law requires a human determination.
   - `assisted`: AI or automation is permitted or expected. **The standard must include the person's verification behavior** (what was checked, against what independent evidence, and how acceptance, qualification or rejection was documented).
   - `supervisory`: the performance *is* configuring, monitoring, validating and overriding an automated system (e.g., an autonomous sensor network or automated classification pipeline).
2. **Assess process, not just output, in assisted mode.** Field evidence shows generative AI narrows output differences between novices and experts on tasks inside the tool's competence, and can degrade performance outside it [E-u: IO-075, IO-076]. Output-only scoring then stops discriminating levels. Assisted-mode assessments should include **seeded-error items**, where the AI draft contains a planted error and the score is whether the candidate catches it, plus a **documented accept/qualify/reject rationale**.
3. **Dual-condition assessment where formation matters.** For competencies whose L1–L2 tasks v1 tagged as compressed or substituted *and* career-ladder-sensitive (CLD flag), assess one component AI-off and one AI-on. Evidence from clinical AI suggests unaided skill can decline after routine AI use [E-u: IO-077], so AI-on performance alone can hide a deficit.
4. **Name the function, never the product.** Write "an AI-generated species classification" or "a large-language-model draft", not a vendor or model name (T flag).
5. **Accountability stays with the person.** Assisted-mode standards end with a traceable human decision: "…and records the basis for accepting or rejecting each flagged output."

## 6. What is *not* an indicator (and where it goes instead)

| Content type | v1 example | v2 home | Assessed by |
|---|---|---|---|
| Enabling knowledge | "Understands dose-response relationships" | **Knowledge element** linked to the competency (and optionally a level), written as a testable proposition: "Dose-response relationships: threshold vs. non-threshold models; reference dose; slope factor" | Knowledge test, oral exam, or the explanation component of a work sample |
| Credentials and legal qualifications | "Completes OSHA HAZWOPER Technician (40-hour) training" | **Qualification gate**: a requirement attached to *positions*, not a level of competence | Record check |
| Tool fluency | "Uses Tableau, Power BI…" | **Tool layer** (faster-moving, versioned separately; DC lane) | Practical check if required by the position |
| Scholarly output, awards, reputation | "Publishes influential research" | **Evidence source** an assessor *may* consult for a performance indicator (e.g., a published method as a work product), never an indicator in itself | n/a |
| Values and dispositions | "Values local and traditional knowledge" | **Conduct expectation** in a code of practice, or rewritten as behavior ("records and cites knowledge-holder input and its permitted uses before…") | Behavior only |
| Sector application notes | "Natural capital accounting…" | **Context examples** (descriptive) | Not assessed |

## 7. Banned constructions (indicator lint)

These patterns are rejected automatically. The regular expressions are a starting specification for an automated linter (IA/DE lane), and every hit routes the indicator to human revision. In v1 they account for most code-0 and code-1 statements [E: IO-010].

| # | Construction | Lint pattern (case-insensitive, start of sentence unless noted) | Why | Fix |
|---|---|---|---|---|
| B1 | Internal-state verbs | `^(understands|knows|is aware|aware of|familiar with|appreciates|comprehends|grasps|has knowledge)` | Not observable (OBS-4 = 1); UGESP 14C(1) | Move to knowledge element, or use *explains / identifies / distinguishes* + object |
| B2 | Level labels as content | `^(expert in|proficient in|skilled in|deep understanding|comprehensive expertise)` | Circular: uses the level to define the level | State the performance |
| B3 | Reputation, influence, status | `^(shapes|influences|advances|transforms)|recogni[sz]ed (as|expert|authority|leader)|thought leader|achieves recognition|influential|adopted (widely|sector-wide)|field-wide|nationally|internationally` | OBS-4 = 0; opportunity-dependent; scored by others' opinions | Describe the work product the influence came from (a method, standard or decision record) |
| B4 | Proxies | `^(publishes|presents at|holds|completes .*training|has \d+ years)|years of experience|certified|licensed` | Criterion contamination; adverse-impact risk (§8) | Move to qualification gate or evidence source |
| B5 | Outcome guarantees | `^(ensures|guarantees|achieves|demonstrates significant)` | Outcome is shared with others or the environment | State the controlling behavior and its check |
| B6 | Empty verbs | `^(supports|assists with|contributes to|participates in|is involved in|handles|addresses|leverages|utilizes|works effectively)` | No object or standard; OBS-4 ≤ 2 | Name the specific contribution and its product |
| B7 | Compound performances | `\b(and|or)\b` joining two verbs (e.g., `designs and implements`) | Can't score partial performance | Split into two indicators |
| B8 | Adjective-only gradation | `\b(basic|simple|complex|sophisticated|comprehensive|advanced|major)\b` when it is the *only* change from the adjacent level | Levels not distinguishable (§9) | Change autonomy, condition or standard explicitly |
| B9 | Vendor, tool or model names | product names, or `AI-powered|machine learning|blockchain|digital twin` used as the competency rather than the function | Obsolescence; vendor lock-in | Name the function; move the tool to the tool layer |
| B10 | Hard-coded jurisdiction rules | named regulation or rule as the standard (e.g., "SEC climate disclosure rule", "2012 Planning Rule") | Rules change; v1 already contains outdated references [J] | "applicable federal/state/Tribal/local requirements" + `jurisdiction_variable = true` |
| B11 | Trait or attitude | `respectful|passionate|values|committed to|demonstrates integrity` | Not job behavior; legally weak | Describe the behavior |
| B12 | Non-job-related access | owns a vehicle, unlimited availability, physical requirements not tied to essential functions | ADA / Section 501 risk | Tie to an essential function or delete |

## 8. Fairness rules for indicators used in selection

1. **No tenure in indicators.** Years of experience have weak criterion validity (meta-analytic ρ ≈ .06 for prehire experience and job performance) [E-u: IO-046]. Their predictive value comes from the *content* of experience, not its duration [E-u: IO-047, IO-048]. Minimum-years rules also risk disparate impact on people with interrupted careers and age-related claims [J]. Indicators describe performance; time is recorded descriptively at most (`proficiency_model_v2.md` §3).
2. **No opportunity-gated indicators at selection levels** (O flag, §2). People from under-resourced organizations, rural duty stations, Tribal programs or small NGOs often never get to "lead national initiatives". Requiring it measures access, not competence [J].
3. **Use the least adverse alternative of equal validity.** When two indicator formulations or assessment methods are similarly job-related, prefer the one with smaller expected subgroup differences. Work samples, for example, can show larger Black–White differences than once assumed [E-u: IO-054], and UGESP 1607.3B expects alternatives to be considered [E-u: IO-020].
4. **Reasonable accommodation, including for AI-assisted tasks.** If an indicator is in assisted mode, the assessment must give equal access to the tool and accommodate its use [J; IO-024, IO-081].

## 9. Level-differentiation rule (for authors and Delphi panels)

Adjacent-level indicators for the same competency must differ on **at least one named generic attribute** (autonomy, guidelines and judgment, complexity, scope and influence, knowledge, augmented practice, formation of others). The author records which attribute changed in the `notes` field [J; IO-061 design principle].

Example (wildlife survey):
- **L1:** "Records detections on a standardized datasheet **under a qualified observer's direction**, so that species codes, counts and locations pass the program's QA check." *(autonomy: supervised)*
- **L2:** "Conducts a point-count or transect survey **independently on an assigned route**, so that detections, distances and effort meet the protocol's data standard." *(autonomy: independent)*
- **L3:** "**Adapts** the survey protocol **when site conditions prevent standard execution**, and documents the deviation and its effect on detectability." *(complexity: non-routine; guidelines: adapting rather than following)*

Counter-example (v1, 2.7.3 Digital twins): "Develops simple digital twins" → "Develops comprehensive digital twins" → "Develops sophisticated digital twin systems". Only adjectives change (B8).

## 10. Behaviorally anchored rating scales (BARS)

Indicators define *what* is assessed. BARS define *how well* it was done, when a rating scale is needed: structured-interview scoring, supervisor ratings used as criteria, assessment-center exercises [E-u: IO-050, IO-051, IO-055]. Build them as follows:

1. Collect critical incidents from SMEs, at least 10 per competency, spanning ineffective to highly effective performance.
2. Have a second, independent SME group **retranslate** the incidents: assign each incident to a competency and rate its effectiveness. Retain incidents with high assignment agreement and low dispersion in effectiveness ratings. Criteria such as ≥60% assignment agreement and SD ≤ 1.5 on a 7-point scale are common; pre-register the exact criteria (`validation_protocol.md` §5) [J].
3. Scale anchors at three to five points per indicator cluster. Anchors describe behavior and its consequence ("Accepted the model's classification without checking the two plots it flagged as low-confidence; one was misclassified").
4. Train raters with frame-of-reference training. It improves the accuracy and agreement of competency inferences [E-u: IO-042].

## 11. Worked examples (v1 → v2)

The full set is in `exemplar_rewrites.csv`. These show the rules at work.

| v1 statement (code) | Problem | v2 indicator | Level · mode · evidence |
|---|---|---|---|
| "Understands basic statistics (mean, variance, correlation, hypothesis testing)" (1) | B1 | *Knowledge element:* descriptive statistics; sampling distributions; Type I/II error. *Indicator:* "Calculates descriptive statistics and a two-group comparison for a monitoring dataset, stating the test's assumptions and whether the data meet them." | L1 · assisted (software) · work product + knowledge test |
| "Shapes statistical practice in environmental field" (0) | B3 | Deleted. If the role needs L4: "Sets the statistical acceptance criteria (power, effect size, error rates) for a monitoring program and documents their basis so that external reviewers can reproduce the design decision." | L4 · assisted · work product + structured interview |
| "Completes OSHA HAZWOPER Technician (40-hour) training" (3P) | B4; also mixes emergency-response levels with site-worker training hours [J] | Qualification gate on the *position*: "current HAZWOPER training at the level the position's hazard assessment requires". *Indicator:* "Establishes an isolation zone and access control for a suspected release, using the responder guidebook, before any containment is attempted." | L2 · unaided · simulation/drill observation |
| "Provides leadership on decision science" (0) | B3, B6 | "Leads a structured decision analysis for a contested management choice, so that objectives, alternatives, consequences and trade-offs are documented and each stakeholder group's objectives appear in the record." | L3 · assisted · work product + interview |
| "Questions AI recommendations and maintains ethical awareness" (2C) | B7, B11 | "Rejects or qualifies an AI-generated recommendation when it conflicts with independent field or regulatory evidence, and records the conflicting evidence and decision." | L2 · assisted · seeded-error simulation + record |
| "Uses sustainability reporting software (e.g., Workiva, Diligent ESG)" (3T) | B9 | Tool layer. *Indicator:* "Traces each reported sustainability metric to its source data and calculation method, so that an assurance provider can re-perform the calculation." | L2 · assisted · work product |
| "Recognizes that assisted migration remains controversial" (1) | B1 | "Summarizes the principal scientific and governance arguments for and against a proposed translocation, citing sources for each, for a decision-maker briefing." | L2 · assisted · work product |
| "Leads major forest health initiatives" (2O) | O flag | "Develops a forest-health monitoring and response plan for an administrative unit, specifying detection thresholds, response triggers and responsible parties." | L4 · assisted · work product |

## 12. Process for authors (checklist)

1. Start from a **task**, not a competency name. Each indicator must link to at least one validated task (`validation_protocol.md` §6).
2. Write the sentence (§3). Run the lint (§7).
3. Fill in the metadata (§3), especially `augmentation_mode` and `use_class`.
4. Score OBS-4 yourself. A second author scores it blind. Disagreements go to an adjudicator.
5. Confirm the level-differentiation rule (§9) against adjacent levels.
6. Send to an SME panel. Record the panel outcome in `validation_status`.
7. If the indicator was LLM-drafted, record that in `provenance`, along with the human who accepted it (`validation_protocol.md` §7).
