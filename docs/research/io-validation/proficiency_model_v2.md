# EMST v2 Proficiency Model: Responsibility-Anchored, Behaviorally Evidenced Levels

**Role:** IO · **Status:** proposal (P-IO-01 to P-IO-05 in `report.md`) for CA decision; FH, SL and LC input requested where marked · **Date:** 2026-10-23
Labels: **[E]** evidence read or computed this session · **[E-u]** published evidence not re-retrieved this session (`unverified` in `sources.csv`) · **[J]** expert judgment · **[S]** speculation.

---

## 1. Decision in one paragraph

Retire v1's four **years-based** levels (Foundational 0–2 y, Intermediate 3–5 y, Advanced 6–10 y, Expert 10+ y). Replace them with **five responsibility-anchored levels (L1–L5)**, each defined by **seven generic attributes**: autonomy; guidelines and judgment; complexity; scope and influence; knowledge application; augmented practice (tools and AI); and formation of others. Each competency is defined **only at the levels where the work actually exists**, its "level span". At each defined level it carries 2–5 **behavioral performance indicators**, written to `indicator_writing_rules.md` and assessed by named methods. Knowledge, credentials and tools move to separate layers. Years of experience become, at most, descriptive data (time typically taken to reach a level), never a criterion. Levels inform federal grades and state pay bands through **position profiles**, not equivalence tables.

## 2. Why the v1 levels can't carry selection, promotion or training decisions

1. **Years are a weak and legally exposed proxy.**
   - Meta-analytic evidence puts the validity of prehire experience for job performance near zero (ρ ≈ .06) [E-u: IO-046]. Earlier syntheses show that experience predicts performance only when measured by *what was done* and *at what level*, not by elapsed time [E-u: IO-047, IO-048]. Experience in years also ranks near the bottom of current validity estimates for selection procedures [E-u: IO-049].
   - Minimum-years thresholds are a classic source of adverse impact on people with interrupted careers (caregiving, military service, seasonal and term appointments, RIFs) and raise age-related issues when used as caps [J]. Under UGESP, a training-and-experience requirement with adverse impact needs validity evidence [E-u: IO-020, IO-021].
   - Federal hiring already has its own experience rules (specialized experience and time-in-grade in OPM qualification standards), and the Chance to Compete Act and Merit Hiring Plan push agencies *away* from self-reported experience screens toward technical assessments [E-u: IO-030, IO-031]. A parallel years scale in EMST would at best be redundant and at worst invite misuse [J].
   - Environmental careers are discontinuous across sector actors (seasonal fire crews, term NGO grants, Tribal program cycles, academic postdocs). Years-based levels systematically disadvantage the cross-sector movers the theory of change depends on [J; CHARTER].
2. **The level content is template text, not behavior.** Across all 222 competencies:
   - 211 Expert Knowledge statements begin "Shapes…".
   - 217 Advanced Knowledge statements begin "Expert in…", so the *Advanced* level is defined by the word "expert".
   - 209 Foundational Knowledge statements begin "Understands / Familiar / Aware".
   - On average, 81% of each competency's Expert-level statements match a handful of boilerplate frames ("influences", "publishes", "recognized", "provides leadership").

   In the blind 43-competency sample, only **1 of 43** Expert levels contained a single directly observable, non-proxy statement [E: IO-010].
3. **Every competency has every level, whether or not the work exists.** "Collaborative document management" (2.5.2) has an Expert level that "Advances document management in environmental sector". v1's own methodology research recommended the opposite: SFIA-style responsibility levels that "avoid forcing every skill into every level" (`Skills Taxonomy Architecture and Methodology…md`, §Proficiency scaling) [E: IO-004].
4. **Observability falls exactly where the stakes rise.** Directly observable statements fall from 56% (Foundational) to 42% (Intermediate), 15% (Advanced) and 5% (Expert). Opportunity-dependent statements rise from 0% to 21% (Advanced) and 39% (Expert) [E: IO-010]. Senior selection and promotion, the highest-stakes uses, rest on the least assessable content.

## 3. Architecture: four layers, one level scale

| Layer | What it holds | Leveled? | Changes how often | Assessed by |
|---|---|---|---|---|
| **A. Performance indicators** | What a person does at a level, to standard (`indicator_writing_rules.md`) | Yes (L1–L5, within the competency's span) | Slow (version per release) | Observation, work product, simulation, structured interview, task book |
| **B. Knowledge elements** | Testable propositions the performance depends on (former v1 "Knowledge" statements, rewritten) | Optional (tag the lowest level that needs it) | Slow-medium | Knowledge tests, oral exam, explanation component of work samples |
| **C. Qualification gates** | Licenses, legally required training, safety qualifications (HAZWOPER, PE, RPF, NWCG position quals, CDL…) | No; attached to *positions* and jurisdictions | Set by external bodies | Record check |
| **D. Tool layer** | Named software, models, platforms, AI products (DC lane) | Optional (tool proficiency) | Fast (quarterly-annual) | Practical check |

**Years** live outside all four layers, as an optional *descriptive* field per competency and level, `typical_time_to_level`. It comes from job-analysis data (`validation_protocol.md` §4) and is shown to learners and planners as information only [J].

## 4. Generic level descriptors (L1–L5) on seven attributes

The attributes deliberately parallel SFIA's levels of responsibility (autonomy, influence, complexity, knowledge, business skills/behavioral factors) [E-u: IO-061]. They are also *conceptually* aligned with the federal Factor Evaluation System factors (knowledge required; supervisory controls; guidelines; complexity; scope and effect; contacts) [E-u: IO-080]. That alignment makes PD language translate without equating levels to grades (§8; FH to confirm) [J].

| Attribute | **L1 Supervised** | **L2 Independent** | **L3 Senior** | **L4 Lead / Expert** | **L5 Strategic** |
|---|---|---|---|---|---|
| **Autonomy** (≈FES supervisory controls) | Works under direct or close direction; work is checked | Completes standard assignments without step-by-step direction; reviewed for results | Plans own approach to non-routine work; review is for policy fit, not method | Sets the technical approach for a program or team; work is accepted as technically authoritative | Sets direction across programs or organizations; accountable to executives, boards or elected officials |
| **Guidelines and judgment** (≈FES guidelines) | Follows written procedures; refers deviations | Selects among established methods; interprets guidance for routine cases | Adapts methods where guidance is incomplete or conflicting; documents deviations | Creates methods, criteria or guidance where none exist; resolves conflicts between guidelines | Establishes policy or standards others' guidance is based on |
| **Complexity** (≈FES complexity) | Defined, repetitive tasks; few variables | Varied routine cases; recognizes non-routine and escalates | Non-routine cases with multiple interacting variables, uncertain or conflicting data | Novel, high-consequence or contested problems with no precedent | Systemic problems spanning institutions, jurisdictions or long horizons |
| **Scope and influence** (≈FES scope/effect, contacts) | Own tasks; contacts within the work unit | Own assignments; routine contacts with partners and public | Project or site; persuades and negotiates with external parties on technical matters | Program or landscape; represents the organization in technical disputes and negotiations | Organization or sector; negotiates commitments between governments or organizations |
| **Knowledge application** (≈FES knowledge) | Applies procedural knowledge of a defined task | Applies the body of standard methods in the specialty | Integrates knowledge across specialties for a case | Recognized technical depth that others rely on; extends methods | Integrates technical, legal, fiscal and political knowledge for strategic choices |
| **Augmented practice** (tools and AI; new) | Uses approved tools under prescribed checks; reports anomalies | Selects tools for routine work; verifies outputs against independent evidence; documents acceptance or rejection | Calibrates trust in specific tools across conditions; decides when not to use them; reviews others' AI-assisted products | Designs verified human-AI workflows and acceptance criteria for a program; audits for drift and misuse | Sets organizational governance for AI and automation, including formation and accountability safeguards |
| **Formation of others** (new; responds to v1 CLD finding) | Learns through supervised performance | Shows peers routine tasks | Coaches trainees; evaluates task performance against standards (task-book evaluator) | Certifies others' qualification; designs developmental experiences, including protected unaided practice | Sets formation pathways and protects entry cohorts organization-wide |

**Optional "Awareness" descriptor (A).** Some cross-cutting competencies need everyone to have *awareness*: knowing the issue exists, recognizing when it applies, and knowing whom to call (e.g., Indigenous data sovereignty, hazmat recognition). This is recorded as a **knowledge-element bundle tagged A**, assessed only by knowledge checks. It is **not** a proficiency level and may not be used as a selection criterion beyond a minimum-knowledge screen [J].

**Why five levels and not four.** v1's Expert level mixed two different things: deep technical authority (L4) and organization-level strategy (L5). Splitting them lets most competencies stop at L4. L5 is used only for genuinely strategic competencies (policy, governance, program portfolio), and the number of levels maps more naturally onto OPM's existing five-point competency proficiency scales [J; FH to confirm]. The cost is one more level to validate; §6 limits it.

## 5. Level spans: not every competency needs every level

Each competency declares `level_min` and `level_max`. Proposed defaults by competency type (to be confirmed per competency by SME panel and job-analysis data) [J]:

| Competency type | Typical span | Examples (v1 codes) |
|---|---|---|
| Field technique / operational procedure | L1–L3 | wildlife observation (4.1.2), water sampling (4.1.3), fuels treatment implementation (4.3.3 part) |
| Analytical method | L1–L4 | statistics (2.2.2), risk assessment (6.7.1), MFA (3.7.5) |
| Program or system design | L2–L4 | monitoring program design, decision-support systems (2.4.3) |
| Governance, policy, negotiation | L2–L5 | planning (6.2.3), Tribal data sovereignty agreements (7.1.1), AI governance (7.1.4) |
| Cross-cutting professional practice | A + L1–L4 | AI output validation (7.2.1), regulatory integrity (7.1.3) |
| Strategic only | L4–L5 | vision and mission (3.2.2), enterprise portfolio budgeting |

**Rules for defining a level** [J; consistent with IO-061 and IO-058 practice]:
1. **Existence:** job-analysis data show the performance is required in real positions at that responsibility level. Proposed threshold: at least 20% of incumbents whose position profile is at that level rate the competency "important" or above (`validation_protocol.md` §4).
2. **Distinctness:** indicators differ from the adjacent level on at least one named attribute (§4; `indicator_writing_rules.md` §9).
3. **Assessability:** at least two indicators at the level pass OBS-4 = 3 for its `use_class`.
4. **Consensus:** the Delphi panel places the indicators at that level under the pre-registered placement criterion (`validation_protocol.md` §5).

A level that fails any rule is **not published**. An empty level is information, not a gap.

## 6. Behavioral anchoring at three resolutions

| Use | Anchor type | How it's built | Score |
|---|---|---|---|
| **Classification of a position** (what level does this job require?) | Generic descriptors (§4) + indicator list | SME judgment against descriptors; job-analysis survey | Required level per competency (position profile) |
| **Selection and promotion** (does this person perform at L*n*?) | Indicators converted into exercise-specific **BARS** | Critical incidents → retranslation → anchors (`indicator_writing_rules.md` §10) | Rating per indicator cluster; cut score set by SME standard-setting (`validation_protocol.md` §8) |
| **Training and qualification** (is this trainee ready to perform unsupervised?) | **Entrustment-supervision scale** applied to task-book tasks | NWCG task-book model plus EPA/entrustment practice [E-u: IO-056, IO-057, IO-059, IO-060] | 1 = assessor performed it; 2 = step-by-step direction; 3 = assessor present for correction; 4 = available on call; 5 = no supervision needed. L1 → L2 readiness = consistent 4–5 across required tasks |

Medical education's experience is directly relevant. ACGME Milestones 2.0 treats levels as developmental *descriptions*, judged by a committee from multiple observations. It explicitly does not require every learner to reach the top level, and it expects the graduation target to sit below it [E-u: IO-058]. EMST should copy that stance: "L4" is not an aspiration for every worker, and an L2 position profile is not a deficit [J].

## 7. AI-augmented performance is part of the standard

Principles [J; grounded in IO-024, IO-075, IO-076, IO-077, and v1 7.2.x content]:

1. **Write standards for the work as performed.** Where AI or automation is normal in the job, the indicator describes performance *with* it (`augmentation_mode = assisted` or `supervisory`), and the standard includes verification and accountable decision.
2. **Level is about judgment, not tool use.** Using an AI tool never raises a person's level. Calibrating, auditing, governing and deciding when not to use it is what the "augmented practice" attribute scales.
3. **Protect the unaided core.** Some L1–L2 indicators should stay `unaided` where (a) v1 flagged career-ladder destruction (CLD = true, 62 competencies), (b) safety or legal accountability requires it, or (c) field conditions make tools unreliable. Without those, the experience that builds the judgment needed to check AI disappears (v1 Task 13 finding; Structural Conditions report) [E: IO-003].
4. **Assess both conditions where it matters.** Dual-condition (AI-off and AI-on) assessment for CLD-flagged competencies; seeded-error tasks for assisted-mode indicators (`indicator_writing_rules.md` §5).
5. **Re-validate when the tool frontier moves.** A change in tool capability can move tasks between levels: what was L2 analysis becomes L1 supervised review of an automated output. The horizon-scanning cycle (FS, LM) should trigger a targeted re-rating of level placement for affected competencies (`validation_protocol.md` §11).

Example, competency 4.1.2 (wildlife observation), level L2:
- *unaided:* "Identifies to species the birds detected by sight and sound on a point-count route, with an error rate within the program's observer-certification threshold."
- *assisted:* "Reviews automated species classifications from an acoustic recorder deployment, verifying a random sample and all low-confidence detections against the recordings, and records accepted, corrected and rejected detections."

## 8. Relation to federal grades and state pay bands, without equating them

**Principle:** a grade or band is a property of a **position**, set by classification standards from the duties *and* their difficulty and responsibility. EMST levels are properties of **performance on a competency**. A position has a *profile*: required level per competency, from its PD and job analysis. The profile informs, but does not determine, grade [J; FES logic in IO-080; FH and SL to own the operational rules].

**How the link works:**
1. **Position profile:** for each position (or PD family), list the 5–12 competencies that matter, each with a required level and its use class (needed at entry vs. developed on the job).
2. **Classification support:** because the generic attributes parallel FES factors (§4), a classifier can read an EMST profile as *evidence* about factor levels (e.g., an L3 "autonomy" profile supports, but does not decide, a supervisory-controls factor level). The classification standard still decides the grade.
3. **Qualifications and assessment:** "specialized experience" statements and technical assessments (SME-QA, structured interview, work sample) can be written from the profile's L-level indicators. Under the Chance to Compete Act and Merit Hiring Plan, those assessments must rest on job analysis. EMST supplies the task, competency and indicator bank that speeds up the job analysis; it does not replace it [E-u: IO-030, IO-031; IO-022].
4. **State classes:** the same profile logic applies to state classification plans (e.g., Technician / Specialist I–III / Senior / Supervisor series). Minimum qualifications in many state plans are still written in years. EMST profiles can supply **demonstrated-competency substitution language** for those minimums, subject to each state's merit-system rules (SL lane) [J].
5. **Other sector actors:** private career-level frameworks, NGO job levels and Tribal classification systems map the same way. The profile is the portable object, and mobility comes from comparing profiles, not grades (CM lane) [J].

**Illustrative only** (not a crosswalk; FH and SL to validate against real PDs): many 0400-series full-performance positions at GS-11/12 would likely profile at L2–L3 on core technical competencies and L1–L2 on supporting ones. A GS-13/14 program lead would profile L3–L4 on core and L4 on governance competencies. Any single level will appear across several grades [S: test with a sample of 30–50 PDs per series].

**What must not happen:** publishing "L3 = GS-12" or "L3 = Band 4" tables. That would import EMST into classification decisions it was never validated for. It would also invite grade-based adverse-impact challenges and break across 50 state systems [J].

## 9. Migration from v1

| v1 element | v2 destination | Rule |
|---|---|---|
| Level label (years) | Retired; optional descriptive `typical_time_to_level` from data | No carry-over of year bands |
| Foundational K/A + indicators | Mostly L1 indicators (rewrite) + knowledge elements | 56% already directly observable in the sample; rewrite the rest [E: IO-010] |
| Intermediate | Mostly L2 | 42% direct, 50% need specification; add conditions and standards |
| Advanced | L3 or L4 (decide per indicator) | Only 15% direct; heavy rewrite |
| Expert | L4/L5 only where the work exists; otherwise delete | 61% not assessable; boilerplate; do not migrate "Shapes/Influences/Publishes/Recognized" |
| "Knowledge" statements (888) | Knowledge elements (layer B) | 85.5% scored 0 or 1 as performance statements |
| Credentials in indicators (e.g., HAZWOPER) | Qualification gates (layer C) | Correct content errors on the way (see 4.4.4 exemplar) |
| Tool names in indicators | Tool layer (D) | DC lane |
| Domain 5 indicators (missing in DB) | Recover from source text (706 indicators), then rewrite | DE lane for recovery |
| Indicators truncated at the six-per-level import cap (2,104 source indicators absent from the DB overall) | Recover from source text before rewrite | DE lane |

Each migrated indicator keeps `provenance = v1:<code>:<level>:<n>`, and its `validation_status` resets to `draft` [J].

## 10. Data model additions (for DE and IA)

`competency.level_min`, `competency.level_max`, `competency.awareness_bundle` (bool) · `level_descriptor` (L1–L5 × 7 attributes, versioned) · `indicator` (fields in `indicator_writing_rules.md` §3) · `knowledge_element` (id, text, competency_id, min_level, assessment) · `qualification_gate` (id, issuing body, jurisdiction, renewal, linked positions) · `position_profile` (position or PD id, competency_id, required_level, needed_at_entry, use_class, source) · `typical_time_to_level` (competency_id, level, median_years, IQR, n, source survey, date).

## 11. Trade-offs and open questions

- **Comparability vs. accuracy.** Five levels with spans make EMST harder to summarize ("what level is this person?") than a uniform four-level grid. That's deliberate: a person has a profile, not a level [J]. Product and UX (CP) will need a profile visualization.
- **Generic descriptors vs. competency-specific indicators.** Generic descriptors keep levels consistent across 200+ competencies but are too abstract to assess on their own. Indicators are assessable but costly to write and validate. v2 needs both; only indicators are scored [J].
- **AI mode drift.** As tools improve, `assisted` indicators may need yearly re-review. Validation can't be one-off (`validation_protocol.md` §11) [J].
- **For CA:** should L5 exist at all in the first federal and state release, or be deferred until job-analysis data show enough strategic-competency demand? IO recommends defining L5 only for the about 15–25 governance competencies where SME panels confirm it [J].
- **For FH and SL:** confirm whether the FES-parallel attribute wording helps or hurts classifier adoption, and test the profile approach on a pilot set of PDs (0401, 0408, 0460, 0819, a state environmental specialist series).
- **For LC:** the entrustment-supervision scale and task-book design (§6) are shared ground between assessment and curriculum. Propose a joint specification.
