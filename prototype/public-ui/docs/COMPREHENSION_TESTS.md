# EMST public interface: comprehension tests CT-0 to CT-5

**Owner:** content designer (an AI agent on the HCD team). **Date:** 30 October 2026. **Release:** `2.0.0-rc.1`.
**Source of the method, questions, answers, harmful misreadings and pass rules:** `docs/research/R3_standards_trust.md` §11 (CT-0 to CT-5) [E]. My additions are marked **[J]**.
**Wording under test:** `app/assets/js/content.js`. Variant A or B of each test is the shipped wording, as marked.

**Status:** ready to run. **Nothing here has been run, and no real person has seen these stimuli.** Recruitment needs the EMST project lead's approval. The brief bars contacting anyone without it [E: R3 §11 "Ethics"; team brief].

---

## 1. How to run the tests

### Ethics and consent (from R3 §11; must be done before any session)
- **Recruitment:** the EMST project lead must approve it.
- **Consent:** get written or recorded consent. Say plainly that the site is a draft prototype, and that we are testing the wording, not the person.
- **No data on the EMST site:** run every session on a prototype copy. Store notes off-site, and anonymize verbatim quotes.
- **CT-5 participants:** **do not recruit Tribal participants for CT-5** until the project lead decides how ADR-0007 applies.
- **Held content:** never show draft Tribal content to anyone. The CT-5 screens show only the policy text and the count.
- **Personal data:** collect only the literacy band, the segment, and what the participant says about the screens. Collect no names in the data set.

### Samples (R3 §11)

| Stage | Who | Size | Stop or pass rule |
|---|---|---|---|
| **A: formative** (moderated think-aloud, then probes) | 3 segments:<br>• learners and job seekers (U2, U8);<br>• supervisors, training and HR staff (U3–U6);<br>• data users (U7) | 5–8 per segment per round | Iterate until a round of 8 shows no critical confusion |
| **B: summative** | General sample; about 28% at or below PIAAC Level 1, identified with a validated screener | **n = 80** per notice | Pass if **≥ 72 of 80 correct** (lower bound of the two-sided 95% Clopper–Pearson interval above 0.80) **and ≤ 2 of 80 critical misreadings** (upper bound below 0.10) |
| **B-HR: directional** | HR or classification staff (U5) | n = 20–30 | Report only, never pass or fail. At n = 30, even 28 correct shows only a lower bound above 0.75. |

**Basis:**
- FDA label-comprehension guidance: targets set in advance; open questions before closed ones; "I don't know" always offered; no leading questions; scenario questions.
- ANSI Z535.3 critical-confusion practice.
- A round of 8 detects a problem that affects 20% of people with probability 0.83. [E: R3 §11]

### A/B design [J]
- **Stage A:** each participant sees one variant first, assigned in alternation and balanced by segment. They answer every question on it. Then they see the other variant and are asked "Which says it more clearly, and why?". Code only answers to the first variant for comprehension. The second view is for preference only.
- **Stage B:** run the variant that Stage A favors, at n = 80. If Stage A does not separate the variants, run both at n = 80 each, between subjects.
- **Order of tests:** CT-0 first, because it is a 5-second test and must come before anything else is seen. Rotate the order of CT-1 to CT-5 across participants.
- **Presentation:**
  - show each screen at phone width (390 × 844) to half the sample, and at desktop width to the other half;
  - print one stimulus per participant in Stage A, to check the printed status line.

### Session opening (every test, from R3)
Start each test with the open question **"What does this tell you?"** Ask it on the real screen, before any probe. Do not define any term before or during the questions. Accept "I don't know" without pressing.

### Coding
Code each answer in one of four ways:
- **Correct:** matches the answer key; paraphrase is fine.
- **Incorrect:** wrong, but not harmful.
- **Critical:** one of the harmful misreadings listed for that test.
- **Don't know.**

A second coder codes 20% of answers blind. Report their agreement [J].

**Report for each test** [E: R3 §11 "Reporting"]:
- the number correct, with its 95% confidence interval;
- the critical-misreading counts;
- anonymized verbatim misreadings;
- every result broken down by literacy band and segment.

**If a notice fails:** reword it, run it through Stage A again, then repeat Stage B.

---

## 2. CT-0: Who runs this site? ("Not a government website")

**Screen:** the home page.
- **Above the fold:** wordmark, search, status ribbon and H1.
- **In the footer:** the statement under test.
- Show it for 5 seconds, hide it, then probe. Then show it again for the follow-up questions.

| | Statement under test (header or footer) |
|---|---|
| **A (shipped: `COPY.site.notGov`)** | An independent open project. Not a government website. |
| **B** | Independent and open. No government agency runs or endorses this site. |

Both variants keep the same ribbon: "Draft release 2.0.0-rc.1 · Drafted by AI agents, not yet reviewed by people · What this means".

**Questions** [E: R3 CT-0]
1. "Who runs this website?"
2. "Is it a government site?"
3. "Who wrote the task lists?"

**Diagnostic** [J: R3 §6 notes that "Federal Series Profile" pages raise this risk]: show the OPM series page for 0460 (Forestry) and ask "Who made this page?"

**Correct answers**
1. An independent or open project, not the government. "A volunteer or research project" is also correct.
2. No.
3. AI agents drafted them, and people have not reviewed them yet.

**Harmful misreadings** [E: R3]: "OPM"; "a federal agency"; "experts wrote it". In the diagnostic, "OPM made this page" is critical.

**Pass:** at least 72 of 80 answer "not government" or "an independent project" to questions 1 and 2. No more than 2 of 80 give a critical answer.

---

## 3. CT-1: "Drafted by AI, not yet reviewed by people"

**Screen:** the role page for *Field resource technician* (`emst:core/ROL-ZJFCC09`): the page header, the status line, and the first 8 of 35 tasks. Only the AI line differs between variants. The use line reads the same in both: "Use for describing work and planning. Not for decisions about people."

| | AI line under test |
|---|---|
| **A (names the human role and the review path)** | Drafted by AI agents, working to rules set by the EMST project lead. Not yet reviewed by people. Next step: review by practitioners. |
| **B (shipped: `COPY.ai.line`; does not name them)** | Drafted by AI agents. Not yet reviewed by people. |

In both variants, "About this record" holds `COPY.ai.detail`:

> AI agents wrote this record from sources and checked it with automated tests, following rules set by the EMST project lead. No one who does this work has reviewed it, and no study has tested it. Next on the review path: review by practitioners.

**Questions** [E: R3 CT-1]
1. "Who wrote this task list?"
2. "Has anyone who does this job checked it? How do you know?"
3. Scenario: "Your supervisor wants these tasks pasted into a position description today. What do you do?"
4. "What must happen before you could rely on it?"

**Correct answers**
1. AI agents, working to rules set by a person (the project lead). "AI" alone is correct.
2. No. The page says "not yet reviewed by people".
3. Use the tasks only as a starting draft. HR or the responsible official must review, change and adopt any wording, and the job's own experts should check it. Do not paste it in as final. [J: from `core.text.hrDisclaimer` and the OPM memo of 27 August 2026, R3 §4]
4. People who do the work review it, and a study tests it. Any job use also needs the employer's own review.

**Harmful misreadings** [E: R3]:
- "reviewed by experts or the government";
- "AI means it is false".

**Also record, not scored** [J]: answers to question 3 that paste the text in unchanged as final.

**Pass:** at least 72 of 80 say "AI-drafted, not reviewed by people" (questions 1 and 2). No more than 2 of 80 give a critical answer.

**Diagnostics:**
- **[E: R3]** Run a variant without the site-level explanation, with the "What this means" link and About pages removed, to measure the "full automation" assumption.
- **[J: R2 unknown 1, Altay & Gilardi 2024 via R3 §4]** Ask "How much would you trust this task list, from 1 to 5?" and "Would you use it for [the participant's own work]?". Compare A and B on these answers and on the "AI means it is false" count. If A lowers the harmful misreadings without raising over-reliance (question 3), ship A's wording as `ai.line`.

---

## 4. CT-2: "Assessment pending"

**Screen:** the role page for *Field resource technician*, "The work" section (35 tasks). Show the first 8 tasks, grouped by competency.

**Variant A (shipped: `COPY.pending`, shown once at the end of the section):**

> **Assessment pending**
> 0 of 35 tasks assessed so far. Not shown yet: importance, share of work time, whether it is critical, whether it is needed on day one.
> No group of practitioners has rated these yet. We show nothing rather than a guess, so the order of this list says nothing about importance.
> These values will appear after a study with practitioners checks them. No study has reported yet.

**Variant B (R3's screen, like the current explorer):** a task table with an **Importance** column, sorted by that column, with "Assessment pending" in every row. The line above the table reads: **0 of 35 assessed**.

**Questions** [E: R3 CT-2]
1. "Which task is most important?"
2. "What does 'Assessment pending' mean?"
3. "Why is this task first?"
4. "When will this change?"

**Correct answers**
1. The page doesn't say yet.
2. No one has rated this value yet, so it is not shown. It does not mean zero or unimportant.
3. Not because it is important. The order says nothing about importance (A: grouped by competency; B: no values to sort by).
4. After a study with practitioners. No date has been set.

**Harmful misreadings** [E: R3]:
- pending read as zero, low or "not important";
- importance inferred from row order;
- a believed date.

**Pass:** at least 72 of 80 correct on questions 1 and 2. No more than 2 of 80 give a critical answer.

**Diagnostic** [E: R3]: repeat the questions on a chart version, with a bar chart of "importance" that has empty bars. The prototype never draws this chart [E: DESIGN_SPEC §2.5]. The diagnostic shows how big the risk it avoids is.

---

## 5. CT-3: What you can use this for (use tiers)

**Screen:** the status line of *Field resource technician* (describe use). The use statement differs by variant. Also show the "How to read EMST" sections for "Train and develop" and "Job analysis input", which are not reached in this release.

**Variant A (shipped: `COPY.use.describe`, with its link to the key):**

> **Describe and plan.** Use for describing work and planning. Not for decisions about people.
> **You can:** Describe the work of a role in a workforce plan or grant report. · Map a course or training program to the tasks a role does. · Find task wording to start a job or position description. Your HR office must then review and change it.
> **You can't:** Screen, score or rank people who apply for a job. · Set a job's series, grade or pay (classification). · Rate how well an employee does their job. · Choose which jobs or people to cut in a reduction in force.

On the key page, under "Train and develop" and "Job analysis input": **Not reached in this release**, followed by `COPY.use.develop.notReached` and `COPY.use.select.notReached`.

**Variant B (verbal label only, as in the current explorer: `core.labels.useTierText`):**

> Use tier: Describe: workforce analytics, planning, curriculum mapping

On the key page: the four tier names and definitions from `core.labels.useTier`, with develop and select marked "not reached".

**Format** [E: R3 CT-3]: for each scenario, the participant answers **Yes**, **No**, **Not yet** or **Don't know**, then says why.

| | Scenario | Correct answer [E: R3] |
|---|---|---|
| a | Explore what a prescribed-fire course might cover. | Yes |
| b | Describe skill areas in a regional workforce plan. | Yes, with limits |
| c | Write a crew member's individual development plan. | Not yet: no record reaches *develop* |
| d | Screen or rank applicants. | No |
| e | Choose positions to cut in a reduction in force. | No |
| f | Rate an employee's performance. | No |
| g | Start an agency job analysis. | Only as input to the agency's own analysis with SMEs; nothing reaches *select* yet |

**Scoring note for (a)** [J]: the role shown is "describe", which covers (a). If the participant reasons from an exploratory record instead, "Yes" is still correct.

**Harmful misreadings** [E: R3]:
- "Yes" to (d), (e) or (f), each allowed no more than 2 of 80 times;
- in the U5 sample, report every "Yes" to (d), (e) or (f), by count and verbatim.

**Pass:** at least 72 of 80 correct on each of (a), (b) and (c).

**Diagnostic** [E: R3]: do the empty *develop* and *select* rungs read as "coming soon"? Ask: "Will EMST be usable for (c) soon? When?"
- Correct: the page gives no date, and says what would have to happen first.
- Record any answer that names a date or "soon".

---

## 6. CT-4: Crosswalk match strength

**Screen:** *Fisheries and aquatic biologist* (`emst:wildlife/ROL-DXYAYRQ`), section "Connections". Add one "more specific" row from *Field resource technician*, as a second card, so that all four match types appear [J].
- The rows are real rc.1 crosswalk rows.
- The O\*NET-SOC title is shown for test realism, from O\*NET's public occupation list. The release carries the code only [E: DATA.md "Labels"].

**Variant A (shipped: `COPY.match`, no numbers):**

| Linked item | Match |
|---|---|
| OPM series 0482 Fish Biology | Close fit, not the same · AI-suggested, not reviewed |
| O\*NET-SOC 19-1023.00 Zoologists and Wildlife Biologists | Broader term · AI-suggested, not reviewed |
| OPM series 0401 General Natural Resources Management and Biological Sciences | Related in part · AI-suggested, not reviewed |
| OPM series 0404 Biological Science Technician | Related in part · AI-suggested, not reviewed |
| *(Field resource technician)* OPM series 0462 Forestry Technician | More specific series · AI-suggested, not reviewed |

Under the table:

> AI agents suggested these links to help you find related items. No person has checked them. They do not mean EMST matches O\*NET, ESCO, OPM or any state system, and EMST makes no such claim until people review them.

**Variant B (R3's variant):** the same rows and note, plus each row's agent confidence, as rc.1 records it.
- Label each value exactly as the explorer did: "agent confidence (uncalibrated)" [E: `core.text.agentConfidence`].
- R3's illustrative value was 0.6. The real values are:
  - 0482, 0.8;
  - 19-1023.00, 0.65;
  - 0401, 0.35;
  - 0404, 0.3;
  - 0462, 0.7.
  [E: `app/data/role-rol-dxyayrq.js`, `role-rol-zjfcc09.js`, field `conf`]

**Questions** [E: R3 CT-4]
1. "Is the EMST item the same as the O\*NET or OPM item?" (R3 wrote "O\*NET or ESCO". ESCO rows carry no labels in rc.1, so OPM rows are used.)
2. "Which link is strongest?"
3. "Has a person checked these links?"
4. "Could you tell a funder your course is 'aligned with O\*NET'?"
5. *(Variant B only)* "What does 0.8 mean?" (R3 asked about 0.6. This uses the real value on the top row.)

**Correct answers**
1. No.
2. "Close fit" is the closest. None of them means "the same", and none has been checked. (Not used for pass or fail.)
3. No.
4. No.
5. The AI agent's own rough number. It is not a probability and not calibrated.

**Harmful misreadings** [E: R3]:
- "the same" or "equivalent";
- "aligned" or "approved";
- "80% (or any percent) chance it's right" (R3: "60% chance it's right"). **If more than 2 of 80 give this answer, hide the number in default views.** Variant A already hides it.

**Pass:** at least 72 of 80 correct on questions 1, 3 and 4. No more than 2 of 80 give a critical answer.

---

## 7. CT-5: Held-records notice

**Screens** [E: R3 CT-5]:
- the held-records page (`#/about/held`), reached from the footer link;
- the search result for "Tribal", which leads to the same page.

Only the text differs between variants.

**Variant A (shipped: `COPY.about.held`, which is all the brief allows):**

> **Held records**
> Content under the project's Tribal content hold is excluded from every build until a Tribal Advisory Council approves it. These pages neither show nor describe it; the release notes give only a count of held records.
> Held records in release 2.0.0-rc.1: 163
> Governance documents on GitHub

**Variant B (A plus the explorer's own verbatim statement, `core.release.indigenousStatement`, placed first):**

> **Held records**
> Indigenous knowledge is a distinct body of environmental expertise held and governed by Indigenous nations. It is out of scope of EMST by design.
> Content under the project's Tribal content hold is excluded from every build until a Tribal Advisory Council approves it. These pages neither show nor describe it; the release notes give only a count of held records.
> Held records in release 2.0.0-rc.1: 163
> Governance documents on GitHub

**Why test B** [J]:
- R3 IG-02 requires the notice to say that Indigenous knowledge is out of scope by design, and CT-5 question 3 tests it.
- Variant A's policy text does not say it.
- B uses only existing verbatim policy text, and adds no new wording.
- **Shipping B is a decision for the project lead.**

**Questions** [E: R3 CT-5]
1. "What is this telling you?"
2. "Why aren't these records shown?"
3. "Does EMST describe Indigenous knowledge?"
4. "Can anyone see the records now?"
5. "How does the notice come across?" Ask for a tone rating and a comment.

**Correct answers**
2. They are waiting for approval from a Tribal Advisory Council, and EMST won't publish them without it.
   - **Scoring note** [J]: R3's answer key says "a council formed by Tribal governments". Neither variant's text says how the council is formed, so accept approval or consent by a Tribal Advisory Council.
3. No. It is out of scope by design. Expect variant A to score lower here.
4. No.

**Harmful misreadings** [E: R3]:
- "Tribes refused", or "are hiding something";
- "EMST deleted Tribal work";
- "insiders can see them";
- "coming on a date".

**Pass:** at least 72 of 80 correct on questions 2–4. No more than 2 of 80 give a critical answer.

**Tone (question 5):**
- Report it descriptively only.
- Once a Tribal Advisory Council exists, its members, not this team, should set the tone criteria [E: R3].
- **Do not recruit Tribal participants** for this test until the project lead decides how ADR-0007 applies [E: R3 §11].

---

## 8. Summary of variants

| Test | A | B | Shipped now |
|---|---|---|---|
| CT-0 not a government website | "An independent open project. Not a government website." | "Independent and open. No government agency runs or endorses this site." | A |
| CT-1 AI line | names the human role and the review path | "Drafted by AI agents. Not yet reviewed by people." | B (plus A-like detail in "About this record") |
| CT-2 pending | one summary per section, with a count, the reason and what changes it | an importance column of "Assessment pending" with "0 of 35 assessed" | A |
| CT-3 use tier | "You can / You can't" with concrete examples | verbal tier label only | A |
| CT-4 match types | plain match types, no numbers | the same, plus agent confidence | A |
| CT-5 held notice | verbatim policy, count and link | adds the explorer's verbatim out-of-scope statement | A (B needs the project lead's decision) |
