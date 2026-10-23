# EMST v2 User Research Plan (NGO pilot → federal and state)

**Role:** CP (Product & UX Lead) · **Date:** 2026-10-23 · **Status:** proposal

**Coordinate with:**
- AS: pilot cohort, recruitment, agreements.
- CM: personas, workforce voice, outcome evaluation.
- IO: practitioner validation of role profiles and indicators.
- FH and SL: federal and state participants.
- TN: any Tribal participation.

**Labels:**
- **[E]** cites a source I read (IDs in `sources.csv`).
- **[J]** marks my judgment.

---

## 1. Purpose

The research has two equal goals:
1. Make the three MVP views usable and trustworthy for the first users (`mvp_spec.md`).
2. **Generate evidence that changes the taxonomy itself**: role profiles, tasks, competency wording, proficiency indicators, exposure judgments, pathways and frictions.

The second goal is the reason research sits inside the build. Every confusion or disagreement from a real user is data about whether the taxonomy matches real work. [J]

**Simulated voices are not research.** CM's Workforce Voice panel and the TN advisor are simulated [E: CP-002]. The CP draft personas are hypotheses [E: product_strategy §2.1]. Only sessions with real people count as findings in this plan.

---

## 2. Research questions

| # | Question | Informs |
|---|---|---|
| RQ1 | How do pilot leads, supervisors and early-career staff *currently* plan development and talk about role change? What artifacts do they use (PDs, IDP templates, training calendars), and how long does it take? | Baseline; MVP fit |
| RQ2 | What words do people use for their roles and tasks? Do the 12–15 MVP role profiles match roles they recognize? | Alternative titles; role grain (DP-6) |
| RQ3 | Can users find their role, read what is changing, and act on it without help? | View 1; IA |
| RQ4 | Do users interpret evidence tiers, agreement and "contested" markers correctly? Do they over-rely on single-analyst labels? | Uncertainty standard; DP-8 display policy |
| RQ5 | Can people rate themselves against the indicators? Do self and supervisor ratings diverge in useful ways? | IO's DP-4; gap check |
| RQ6 | Do the suggested pathways and frictions match people's real experience of moving between NGO, state and federal jobs? Which frictions are missing? | CM's similarity basis and friction attributes |
| RQ7 | Do outputs (IDP, role-change brief, PD skeleton) get used in real decisions? What blocks use? | Success metrics; 1.1 scope |
| RQ8 | What do federal and state HR, training and IT staff need before they can use the tool at work (procurement, security, accessibility, records)? | Compliance packet; 1.1 |

---

## 3. Participants and recruitment

### 3.1 Segments and numbers

| Segment | Who | Rounds | Target n (total across rounds) | Recruited via |
|---|---|---|---|---|
| S-A | Pilot program and training leads (U1) | 0–3 | 8–12 (2–3 per organization, 3–5 organizations) | AS pilot agreements |
| S-B | Supervisors and crew leads (U3) | 0–3 | 8–10 | Pilot organizations |
| S-C | Early-career staff and corps members (U2) | 0–3 | 10–15 | Pilot organizations; corps alumni networks (CM) |
| S-D | People who have moved between sector actors (NGO↔state↔federal) | 0, 3 | 6–8 | CM; professional societies |
| S-E | State training officers, curriculum leads, HR or classification staff (U4, U5) | 4 | 6–8 | SL; pilot states |
| S-F | Federal HR specialists, training officers, workforce planners (U5, U6) | 4 | 6–10 | FH |
| S-G | Assistive-technology users (screen reader, magnification, keyboard-only, voice control) drawn from any segment | 1–4 | ≥2 per round | Pilot organizations; disability-led organizations if needed |
| S-H | Practitioners validating role profiles (IO protocol) | 1–3 | ≥3 per profile | Pilot organizations, FH, SL |

### 3.2 Recruitment rules

**Sampling.**
- Purposive sampling across sector actor, craft emphasis (field, data, statecraft-heavy roles), career stage, geography (at least 2 states) and organization size.
- Rural and seasonal workers are hard to reach, so plan phone or offline options and sessions outside field season. [J]

**Incentives** [J; confirm with AS counsel and agency ethics offices]:
- NGO and early-career participants: compensated (gift card or stipend), funded by the NGO or coalition.
- Federal employees participating in their official capacity: generally not compensated.
- State employees: state gift and ethics rules vary.

**Scheduling.** Sessions are remote by default, with low-bandwidth options and a phone fallback. In-person contextual visits are used for Round 0 where possible.

**Tribal participation.** Only under TN's protocol and with the nation's or organization's agreement. Results are not published without consent. [E: CP-002; J: CP-073]

---

## 4. Ethics, privacy and the Paperwork Reduction Act

**Sponsorship.** Pilot research is conducted by the NGO steward or coalition, **not on behalf of a federal agency**. That keeps PRA clearance out of the critical path. [J, applying CP-029, CP-033]

**If a federal agency co-sponsors a round** (likely in Round 4) [E: CP-029, CP-033]:
- Prefer **direct observation** (usability tasks) and **semi-structured interviews**. Neither is generally "information" under PRA.
- Give **standardized questionnaires** (SEQ, UMUX-Lite, SUS, comprehension probes) only to federal employees acting in their role, who are exempt, or to fewer than 10 non-federal respondents within 12 months.
- Otherwise, use the agency's **generic clearance**.
- Count every response toward the 10, including declines.
- State employees count as "persons".

**Consent.**
- Written or recorded verbal consent covers purpose, voluntariness, recording, retention, use of quotes, and withdrawal.
- A separate opt-in covers quoting by role title.
- Federal sessions include a Privacy Act statement where an agency collects anything. [E: CP-033; J]

**Data handling.**
- Each participant gets an ID.
- Recordings are stored in NGO-controlled storage, never in the GitHub repo, and deleted 90 days after synthesis.
- Notes are de-identified at synthesis.
- Only synthesized, de-identified findings go into the repo (`docs/research/…/insights/`).
- Artifacts collected (PDs, IDP templates) must be public or redacted by the participant's organization. **No personnel records are accepted** (PC-1). [J: CR-10]

**IRB.** Usability research for product improvement is kept separate from outcome evaluation. If CM's theory-of-change evaluation or any publication uses pilot data, obtain an IRB determination through an academic partner before collecting that data. [J: CP-074]

**Gap-check data in sessions.** Participants may rate fictional personas instead of themselves. If they rate themselves, their files stay on their own device and are never collected. [J: PC-2]

---

## 5. Methods by round

| Round (pilot weeks) | Methods | n | Main outputs |
|---|---|---|---|
| **R0 Discovery** (1–4) | Contextual interviews, 60 min, with artifact walk-throughs; baseline task timing ("show me how you'd plan development for this role today"); **open card sort** of role titles and task statements (moderated, small groups; <10 per structured instrument if federally co-sponsored); synonym collection for role titles | 10–14 interviews; 12–20 card-sort participants | Validated or revised personas (with CM); role list and alternative titles (DP-6); baseline times; first taxonomy change requests |
| **R1 Prototype** (5–8) | Moderated usability tests on clickable prototypes (real v1-migrated data, 4–6 roles); **A/B comparison of two uncertainty displays** (between-subjects with probes, plus a within-subject preference at the end); tree test of the IA | 8–10 usability; 15–25 tree test | Gate: task success ≥70% and comprehension ≥70% (`mvp_spec.md` §11); display choice; IA fixes |
| **R2 Beta** (9–12) | Moderated usability on 1.0 beta (all roles, exports); **accessibility sessions with assistive-technology users**; practitioner validation sessions for role profiles (IO protocol: review tasks, time shares, indicators, "stays human" rationale) | 8–10 usability incl. ≥2 assistive-technology users; ≥3 practitioners per profile | ACR evidence; content and structure change requests; profile revisions |
| **R3 Field trial + summative** (13–20) | Real use at 4–6 organizations; weekly 5-minute diary check-ins (what you used it for, what you produced, what blocked you); collection of artifacts produced, with permission; exit interviews; summative usability on core tasks; SUS at exit | 15–25 trial participants; 8–10 summative | Success metrics; evidence of use in real decisions; repeat use; final pilot change requests |
| **R4 Federal and state** (21–26) | Contextual interviews with HR, training and workforce staff; usability of 1.1 concepts (PD builder, training-program view); **procurement walkthrough** with a state CISO or ADA coordinator and a federal ISSO or privacy officer, using the security packet | 6–10 federal; 6–8 state; 2–4 IT, security and accessibility reviewers | 1.1 requirements; written confirmation of ATO/FedRAMP applicability (or the gap); federal and state variant corrections |

**Why these methods.**
- Direct observation and semi-structured interviews give the richest evidence for a new tool, and they are also the PRA-safe methods. [E: CP-033]
- A field trial is the only way to measure whether outputs are *used*, which is the charter's real test. [J; CP-001 "does this help me?"]

---

## 6. Usability test tasks

Each scenario is written in the participant's own context where possible. A fictional organization and persona are available as a fallback. Tasks are given in plain language without interface terms.

| # | Task (scenario prompt) | Success criterion | Views tested |
|---|---|---|---|
| T1 | "One of your staff does [their real job]. Find the page that best describes that job." | Reaches the correct role variant within 3 minutes using their own words | Search, IA, alternative titles |
| T2 | "Which two parts of this job are changing most? How sure is EMST about that?" | Names 2 tasks with the highest change share **and** states the evidence tier and agreement correctly | View 1; uncertainty |
| T3 | "Your director wants to drop the field data collection training because this page says that work is being compressed. What would you tell them?" | Notes that the evidence is a single unvalidated analyst judgment or contested, or that the human review work grows; does not endorse cutting on this evidence alone | Over-reliance probe (RQ4) |
| T4 | "Do a development check for [persona] and produce a plan you could take to a one-on-one." | Completes ratings, identifies the top 3 priorities, exports the IDP | View 2; exports |
| T5 | "Where could this person go next in state or federal government? Name one thing that might stand in the way." | Names ≥1 state or federal destination and ≥1 friction correctly | View 3 |
| T6 | "Here are five saved files from your team. What is the most common gap?" | Loads files and identifies the top shared gap; respects the minimum cell-size message | Team grid |
| T7 | "You've been asked which version of EMST your plan is based on. Find out." | Finds the release ID or DOI on the export or page | Release stamping |
| T8 | "You think one of these judgments is wrong. What would you do?" | Finds the "Challenge this" route and understands both options (GitHub or email) | Feedback route |
| T9 (R4) | "Draft the duties section of a position description for this role. What would you still need to check before using it?" | Produces a skeleton; names the HR review and adopt step; recognizes the draft watermark | PD skeleton (1.1) |

---

## 7. Measures

| Measure | Instrument | When | Notes |
|---|---|---|---|
| Task success | Complete, partial or fail per task, with predefined criteria (§6) | R1–R3 | Report the rate with a 95% confidence interval, given the small n [J] |
| Time on task | Timed from prompt to criterion | R0 baseline, R1–R3 | Compare with the R0 baseline method |
| Errors and wrong paths | Observed | R1–R3 | Coded by screen |
| Single Ease Question (SEQ) | 7-point, after each task | R1–R3 | Standardized; see PRA rules in §4 |
| UMUX-Lite | 2 items, end of session | R1–R3 | Regression to an SUS-equivalent score [J: CP-070] |
| SUS | 10 items, end of field trial | R3 | For comparability with other public tools [J: CP-070] |
| **Uncertainty comprehension** | 4 probe items plus a confidence rating per item. (1) "Who made this judgment, and has anyone checked it?" (2) "Which of these two tasks is EMST more confident about?" (3) "What does 'contested' mean here?" (4) "Would you change a training budget based on this row alone? Why?" | R1–R3 | Target ≥80% correct by R3. **Over-reliance rate** = share who would act on a contested or T-v1 label without checking; target <20% (`mvp_spec.md` §7) |
| Trust calibration | 5-point "How much would you rely on this?" for rows of different tiers | R1–R2 | Reliance should rise with tier; flat reliance means the display has failed [J: CP-071] |
| Usefulness and intent to use | "How likely are you to use this in the next month, and for what?" (open) | R1–R3 | Coded for concrete use |
| Real use | Diary entries and artifacts produced | R3 | ≥60% of organizations use an output in a real decision |
| Accessibility | Issues logged by WCAG 2.2 success criterion and severity | R2–R4 | Feeds the ACR |
| Taxonomy yield | Change requests by type, and their CA disposition | R0–R4 | ≥30 requests; ≥1/3 accepted or adapted |

---

## 8. How findings change the taxonomy (not only the UI)

**Coding.** Every observation is coded by **layer**:

| Code | Layer | Routed to |
|---|---|---|
| UI | Interface | CP |
| CON | Content wording or plain summaries | CP, then author role |
| ROLE | Role profile: missing, merged, split or mis-levelled role; time shares | FH, SL, CA |
| TASK | Missing, wrong or duplicate task statement | Craft leads, DB |
| COMP | Competency unclear, overlapping or wrongly typed | CA, IO |
| IND | Proficiency indicator not observable or not ratable | IO |
| EXP | Practitioner disagrees with an exposure or "stays human" judgment | LM, IA |
| PATH | Pathway or friction missing or wrong | CM, SL, FH |
| XW | Crosswalk code wrong or outdated | IA, FH, SL |
| COV | Subsector or role not covered | CA, DB |

**Triage rule (P-CP-15).**
- An issue raised by **3 or more participants from 2 or more organizations**, or by any single practitioner validation session (IO protocol), becomes a **change request** to CA.
- Single observations are logged and watched.
- Compliance or safety issues (privacy, accessibility, misleading claims) are fixed immediately, whatever the count. [J]

**Change request record.** Each request is filed as a GitHub issue using a template, or in the repo log. Fields:
- `cr_id`, layer, affected IDs (role, task, competency);
- observation summary (de-identified);
- count of participants and organizations;
- segment(s);
- evidence excerpt (paraphrased);
- proposed change;
- route (owner role);
- CA disposition and date;
- release in which it is resolved.

**Exposure feedback is evidence, but not a verdict.**
- When a practitioner challenges an exposure judgment, the challenge is recorded as a dated, attributed L5 assessment with rater_type `practitioner-feedback` and low weight.
- It triggers re-assessment by the panel process. It does not overwrite anything. [J: matches CA's assessment-record model, CP-003]

**Closing the loop.** Each release note has a "You said, we changed" section linking change requests to their resolutions. Pilot participants get a short summary after each round. [J]

**Examples of expected taxonomy changes** (hypotheses to test):
- alternative titles per role variant;
- time-share corrections;
- new emerging tasks (for example, ground-truthing remote-sensing products);
- indicator rewrites that make the gap check ratable;
- new friction attributes (seasonal-to-permanent conversion rules, state exam requirements);
- merges of competencies users cannot tell apart.

[J; v1's forester prototype suggests several, CP-006]

---

## 9. Cadence and operations

| Activity | Cadence |
|---|---|
| Research sessions | 2–4 per week during rounds |
| Synthesis | Weekly, 60 minutes: CP, plus the role owner for the layer under discussion |
| Change-request triage with CA | Every 2 weeks |
| Round readout | End of each round; a written insight summary in the repo (de-identified) |
| Diary check-ins (R3) | Weekly, 5 minutes, by short form or phone |
| ACR update | Each major release (R2 evidence) |
| Federal/state procurement walkthrough | Once in R4, repeated before 1.1 launch |

**Effort.** Roughly 0.5 FTE of research and design across 26 weeks, plus practitioner time: about 60 minutes per role-profile validation per practitioner. Participant incentives are funded by AS. [J]

---

## 10. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Field season limits availability | Schedule R0 and R3 around seasons; offer phone and asynchronous options [J] |
| Pilot cohort skews to forestry and public lands (v1's bias) | Purposive recruitment across water, restoration, monitoring and community roles; DB review of the role list [E: CP-003] |
| Participants rate themselves in front of supervisors | Use fictional personas in sessions; keep self-rating private; collect supervisor views separately [J] |
| Over-claiming from small samples | Report counts and intervals; label findings by segment; never generalize from fewer than 2 organizations [J] |
| Federal participation is blocked by sponsorship or PRA | Keep the NGO as sponsor; use direct observation; use federal employees acting in their role; get a generic clearance if an agency sponsors [E: CP-029, CP-033] |
| Simulated personas are mistaken for findings | Label every artifact by source type ("CP draft", "CM simulated", "participant finding") [E: CP-002] |
