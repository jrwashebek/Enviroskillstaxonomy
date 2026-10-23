# Protocol: Cognitive interviews for response-process evidence (CIV)

**WP-11 output 5** · Owner: IO (A8); CM recruits movers and workforce-voice participants; CP owns display-label design and accessibility · Status: draft protocol for CA approval; runs with people in Stage 1 · Date: 2026-10-23
**Decision basis:** ADR-0024 §3 ("response-process evidence (n ≈ 10–15 cognitive interviews)"); ADR-0027 §2 (the v1 evidence drawer is "hidden entirely if comprehension testing fails"); `docs/research/io-validation/validation_protocol.md` §4.6 (revise wherever ≥ 3 respondents misread).
**Framing:** response processes are one of the sources of validity evidence in the AERA/APA/NCME *Standards* (2014 edition, current; a revision is under way, Joint Committee named 2024 [E: IO-025; IO-110]).
**Labels:** [E] evidence, [J] judgment, [S] speculation.

---

## 1. Purpose

To find out whether the people who will read, rate or act on EMST materials interpret them as intended, **before** those materials collect data or reach users. Six material sets are tested:

| Set | Material | Who reads it | What could go wrong |
|---|---|---|---|
| M1 | Level descriptors L1–L5 and the Awareness bundle (`vocab/proficiency_levels.yaml`) | incumbents, supervisors, HR | level read as years or grade; "Lead/Expert" read as a title |
| M2 | Sample indicators (≈ 12, spanning levels, modes and crafts) | assessors, trainers, learners | condition or standard missed; assisted-mode verification step not seen as required |
| M3 | Job-analysis survey items and anchors (`instrument_job_analysis_survey.md`) | incumbents, supervisors | frequency and importance confused; "needed at entry" read as "nice to have"; AI-mode item misread |
| M4 | Delphi item formats (`protocol_modified_delphi.md` §4) | SME panelists | "essential" read as "important"; placement scale misread |
| M5 | Codebook decision rules (craft, function and authority, exposure) | prospective raters | defining tests applied to the job rather than the task; E1/E2 confused; normative judgments leak into descriptive fields |
| M6 | Display labels and disclaimers (`display_gates.yaml#labels`; "not a classification basis / not a job analysis / not for RIF or rating decisions"; use-tier labels; the "Tentative" badge; the v1 evidence-drawer label) | HR specialists, training officers, early-career workers | tentative value read as final; v1 prior read as validated; indicative grade read as a classification criterion |

## 2. Sample (n ≈ 10–15 per release cycle)

| Attribute | Target across the cycle |
|---|---|
| Sector actors | ≥ 4 of federal, state, local, NGO, private, academic; ≥ 2 non-federal |
| Craft background | FC-, DC- and SC-primary roles each ≥ 2 |
| User type | ≥ 3 HR or classification specialists; ≥ 3 training officers or programme leads; ≥ 3 incumbents including ≥ 2 early-career; ≥ 2 movers between sector actors (CM) |
| Accessibility | ≥ 2 participants who use assistive technology (screen reader, magnification), for M6 (CP; WCAG 2.2 AA) |
| Tribal participants | only through Tribal research approval, on Tribal time (ADR-0024 §7). No Tribal-related material is tested in non-Tribal interviews (held content) |
| Exclusions | authors of the materials; steering-group members |

**Rounds.**
- **Round A:** 6–8 interviews on the frozen materials.
- **Revision.**
- **Round B:** 5–7 interviews on the revised materials, with new participants.
- **Round C (optional):** only if §5 requires it.
Each participant sees M1, M2 and M6, plus one rotating module (M3, M4 or M5). This keeps each interview ≤ 60 minutes.

Compensation is a stipend, or on-duty time for public employees. Participants get plain-language information and give consent. A study host holds recordings.

## 3. Method

**Concurrent think-aloud** on a short practice item, then **scripted verbal probes**. Retrospective probes follow each module. Interviewers are trained, and use the same script for every participant. They do not explain or correct during the interview.

### 3.1 Probe bank (scripted; interviewers may add spontaneous probes, which are logged)

| Target | Probe |
|---|---|
| Comprehension | "In your own words, what is this asking / describing?" "What does '[term]' mean to you here?" |
| Paraphrase (indicators) | "Describe what someone would actually do to meet this." "What would they hand you or show you?" |
| Standard | "How would you know it had been done well enough?" |
| Level | "Which of these levels does this sound like, and why?" (M1, M2) "Is this about how long someone has worked?" (correct: no) |
| Retrieval (survey) | "How did you work out how often you do this?" "What period were you thinking about?" |
| Judgment (survey) | "What made this 'very important' rather than 'important'?" |
| Response mapping | "Was there an option that fitted what you wanted to say?" |
| Codebook (M5) | "Apply the rule to this task out loud." Then: "Did you think about the job or about this task?" |
| Labels (M6), with a-priori answers | see §3.2 |

### 3.2 Comprehension items for labels (M6), with pre-registered correct answers

| Label shown in context | Question | Counted correct if the participant says, in substance… |
|---|---|---|
| "Tentative: rater agreement α = … (95% CI …)" | "What does this tell you about the value?" | raters agreed only moderately; the value may change; use with care |
| "Assessment pending" | "Can you tell how exposed this task is?" | no, it has not been assessed yet (not "it is low") |
| v1 evidence drawer: "v1 single-analyst prior, LLM-assisted, unvalidated — not for decisions" | "Could you use this in a decision about a position or a training plan?" | no, it is an unvalidated earlier estimate |
| "Indicative grade band — not a classification criterion" | "Could you use this to set the grade of a position?" | no, the classification standard decides |
| Use tier "develop" on a competency | "Could you use this to screen job applicants?" | no, it is for training and development |
| "External context: [index] (…), aggregated over n matched tasks; dispersion …" | "Is this EMST's assessment?" | no, it comes from an outside index, matched approximately |
| "Pathway (exploratory)" | "Is this route recommended?" | no, it is exploratory |

## 4. Coding and analysis

1. **Interview summaries.** Within 48 hours, the interviewer writes a structured summary per item: verbatim key quotes (de-identified), the problem observed and the probe that revealed it. Recordings stay with the study host and are deleted after coding (per approval terms). They never enter the repo.
2. **Problem codes** (assigned per item per participant):
   - `COMP` comprehension of a term;
   - `REF` wrong referent (job instead of task; organization instead of person);
   - `LEVEL` level read as tenure or grade;
   - `STD` standard missed or invented;
   - `MAP` no fitting response option;
   - `CALC` retrieval or estimation burden;
   - `SENS` sensitive or uncomfortable;
   - `ASSUME` assumes knowledge the reader lacks;
   - `ACCESS` an accessibility barrier;
   - `CRIT` critical misreading (§5).
3. **Double coding.** Two analysts code all summaries independently, and disagreements are resolved by discussion. Agreement is reported descriptively (percent agreement). With n ≈ 10–15 it is not a reliability estimate and gates nothing.
4. **Problem matrix.** Items × problem codes × participants, with counts by round. Counts are computed and never typed into reports.

## 5. Decision and stop rules (pre-registered)

| Rule | Trigger | Action |
|---|---|---|
| **Revise (pattern)** | ≥ 3 participants in a round show the same problem code on an item | revise the item, then retest it in the next round |
| **Revise (critical)** | any single `CRIT`: a reading that would reverse a decision or lead to a prohibited use (e.g. a tentative value read as final, a v1 prior read as validated, an indicative grade read as a classification criterion, an "exploratory" pathway read as recommended, an assisted-mode indicator read as allowing acceptance of AI output without checking) | revise, then retest in the next round |
| **Label pass** | in the **final** round, ≥ 80% of participants answer each §3.2 question correctly | label approved for release |
| **v1 drawer** | the v1 evidence-drawer label fails the label-pass rule in the final round | v1 values are **hidden entirely** in that release (ADR-0027 §2) |
| **Stop (success)** | after Round B: no new problem code with ≥ 3 occurrences, no `CRIT`, and every label passes | stop |
| **Stop (limit)** | after Round C (maximum three rounds per release cycle) | items still failing are withdrawn from the release or redesigned by their owner (CP for labels, IO for instruments). They are not shipped with a known misreading |
| **Accessibility** | any `ACCESS` problem on M6 | CP fixes it before release, whatever the count (WCAG 2.2 AA is a release gate, ADR-0027 §4) |

## 6. Pre-registration fields

All `preregistration_core.yaml#core_required` fields, plus:
- `materials` (frozen M1–M6 with SHA-256);
- `module_rotation`;
- `sample_targets` (§2);
- `probe_bank` (§3.1) and `label_items_with_correct_answers` (§3.2);
- `interviewer_training`;
- `problem_codes` (§4);
- `decision_and_stop_rules` (§5);
- `recording_retention`.

## 7. Outputs

- Report `validation/studies/CIV-nn/report.md` (generated). It contains:
  - the sample by attribute (aggregate only);
  - the problem matrix;
  - each revision with before-and-after text;
  - label comprehension rates by round;
  - decisions.
- Revised materials, versioned. A revised survey or codebook gets a new version. A revised display label is a CP change, recorded with the study ID.
- A flag to CA if any `CRIT` traces to an ADR-level design choice rather than wording.
