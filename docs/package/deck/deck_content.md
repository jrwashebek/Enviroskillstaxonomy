# Briefing deck content: How environmental jobs are changing, and what workforce leaders can do in 2027

*EMST v2 sector-facing package (WP-14) · audience: federal, state and NGO workforce leaders (HR directors, chief human capital and training officers, programme executives, workforce boards, educators) · 18 slides · as of 2026-10-23 · licence CC BY 4.0*

*Status: WP-15 first pass (2026-10-23, `docs/methods/WP15_SIGNOFF.md`) cleared this content for internal drafts and the NGO-pilot preview only. Before any external briefing, AS must co-sign and the moving facts marked ⟳ must be re-checked on the dates in §3 of the sign-off note. Statements marked **[pending WP-15]** are sourced but not yet entered in `docs/methods/claims_register.csv`.*

**How to use this file.** Each slide has a **headline** (the argument in one sentence), **body** (2–5 short points or a chart reference) and **speaker notes** with sources. Charts use the flagship report's datasets in `docs/package/report/figures/` (F01–F10; chart forms in `figures_index.csv`). Every chart carries its evidence label, its denominator and a table version; no information may be shown by hover or colour alone. Source IDs: `V…` = verified key facts (`docs/research/_verification/ALL_key_facts.csv`); other IDs = claims register rows. Agent-drafted EMST values are always labelled "agent draft" on screen.

**Mandate frame.** Every section answers one of three mandates leaders already carry. **Merit and skills-based hiring:** job-analysis-based assessment, crediting real experience. **Mission readiness:** delivering statutory work with the people you have. **Knowledge retention:** keeping judgment when people leave and when tools change.

---

## Part 1. Why now

### Slide 1. Title

**Headline:** In 2026, budgets and rules changed environmental work faster than software did. The entry rungs that form judgment are what is now at risk.

**Body:**
- EMST v2: an open, task-level description of environmental work for hiring, development and workforce planning
- Built for three mandates: merit and skills-based hiring, mission readiness, knowledge retention
- What follows separates verified external evidence from EMST's own drafts, which are not yet validated

**Speaker notes:** This briefing has two kinds of content and we keep them apart. External facts were verified on October 23, 2026 against primary or traceable sources, and each has a source ID. EMST's descriptions of roles and tasks are drafts written by AI agents. No job analysis or expert panel has reviewed them yet, and we say so on every slide that uses them. EMST is nonpartisan. It records the status of rules and programmes and takes no position on them (ADR-0016 §6). Licence: this deck CC BY 4.0; EMST data CC0 1.0.

### Slide 2. Three mandates converge in 2026–27

**Headline:** Skills-based merit hiring, mission readiness after a 12% workforce drop, and knowledge walking out of the door now share one prerequisite: a credible description of the work.

**Body:**
- **Merit hiring:** since September 30, 2025, self-assessment questionnaires may set minimum qualifications only. They may not rate and rank. In FY2025, 91.23% of delegated-examining announcements relied solely on them [V1-09; FED-02]
- **Technical assessments:** Natural Resources Management is Tier 2 under the Chance to Compete Act plan, with no Tier 2 date. FY2028 is the governmentwide target [V1-17; FED-03]
- **Mission readiness:** the federal civilian workforce fell from 2,313,216 to 2,035,344 between September 2024 and January 2026, a drop of about 12% [V1-01; WF-01]
- **Knowledge retention:** about 2,000 EPA staff who left at the end of 2025 had a median of 30.3 years of service, against 10.8 years for those who stayed [V1-03; WF-03]

**Speaker notes:** Job analysis is still the legal anchor. 5 CFR 300.103 requires job analysis and a rational relationship to performance, even after OPM's July 31, 2026 interim final rule removed UGESP references [SEL-02]. EMST never describes itself as "UGESP compliance" [SEL-01–03]. OPM is building series-level competency models. It issued competency-based standards for 2210 on April 13, 2026, and its target of 300+ series by the end of FY2026 appears unmet [V1-11; FED-08]. EMST is designed to feed that work, not compete with it. OPM's September–October 2026 CHCO memos include time-to-hire guidance under the Merit Hiring Plan and "Building a Mission-Ready Federal Workforce Through Strategic Recruitment" (October 15, 2026). We read titles and dates only and do not characterize their content [FED-10]. Federal vacancies now need Strategic Hiring Committee approval and annual staffing plans under EO 14356. The order sets no hiring ratio [V1-08; FED-01]. The ~317,000 figure for 2025 departures is the OPM Director's own tally, not a PPS figure. Do not mix the two counts [WF-01].

### Slide 3. The capacity shock is fiscal and policy-driven

**Headline:** The 2025–26 contraction of public environmental capacity came from budgets and policy, not from AI. That is a different problem with different remedies.

**Body:** Chart **F01** (`f01_public_capacity_change.csv`): dot plot of percentage change by unit, each row with its own period and base.
- USFS and NPS each lost more than a quarter of their employees, and federal park rangers fell 34.1% (Sep 2024–Jan 2026) [V1-02; WF-02]
- EPA had 12,849 employees at the end of January 2026, down 24% in a year [V1-03; WF-03]
- FY2026 Interior-Environment appropriations: $42.56bn, down 1.9% from FY2025, against a $26.85bn request [V1-15; WF-09]

**Speaker notes:** Bases differ by row and must not be read as one series (F01 source note). The USFS and NPS rows are lower bounds, because the source says "more than a quarter". These are federal figures only. They do not describe state, local, NGO or private workforces, and they say nothing about Tribal workforces, which EMST does not measure. None of the verified sources attributes these declines to AI. LM's reading in `docs/methods/CHANGE_SIGNALS.md` §7.1 is that the driver is fiscal and policy. That matters because remedies for a budget shock (protecting entry cohorts, mobility, knowledge capture) differ from remedies for automation.

---

## Part 2. What the evidence says

### Slide 4. Most environmental AI is science work, and most of it is not deployed

**Headline:** Federal environmental AI is mostly machine learning for science pipelines. Of the 347 use cases that report a stage, 61 are deployed. None of the five review and permitting use cases is in production.

**Body:** Charts **F02** (`f02_federal_env_ai_use_cases_type_by_stage.csv`) and **F03** (`f03_federal_env_ai_use_cases_by_function.csv`).
- The leading functions are species detection, remote sensing, water and fire
- NEPA, environmental review and permitting: 5 use cases, 0 deployed [OMB-02]
- Governmentwide, the 2025 inventory lists 3,611 use cases, 445 of them high-impact [V4-15; OMB-01]

**Speaker notes:** Source: OMB 2025 Federal Agency AI Use Case Inventory (README as of April 13, 2026), environmental bureaus of USDA, DOI, DOC (NOAA) and EPA, as extracted by EMST LM. "Deployed" means `development_stage = deployed` only, while OMB's README pools deployed and piloted, so do not mix the two [OMB-02 do-not-say]. Entries are agency self-reports: registration is not use, and NOAA reported no stages. The 2026 inventory is expected around the turn of the year and is a signpost to watch.

### Slide 5. Drafting tools are everywhere, and that is not the same as automation

**Headline:** Drafting tools are now available to tens of thousands of federal environmental staff. Availability is not use, and no EMST change indicator has yet passed its evidence test.

**Body:** Table **F04** (`f04_commercial_genai_drafting_tools_at_scale.csv`): licence bands by department and use category; product names omitted.
- Commercial AI drafting, summarizing and search tools are licensed at 10,000+ users in USDA, DOI and EPA (agency estimates)
- EMST moves a change indicator only when two independent evidence families agree, the change persists or is deployed, the match is close, the driver matches and a named person has reviewed it (ADR-0028)
- **No indicator has moved for any of the 13 priority roles** (F10)

**Speaker notes:** Language rules we hold ourselves to. The Anthropic Economic Index's "77% of API transcripts show automation patterns" describes how API traffic uses a model. It is not job or task automation [AEI-02]. BLS's new AI exposure categories are four relative levels, built partly from the same Eloundou, Anthropic and Microsoft data. They are not forecasts and do not separate automation from augmentation [BLS-03]. EMST is built with an Anthropic model and treats Anthropic usage data as one family among several. No indicator may rest on it alone (`CHANGE_SIGNALS.md` §3). Occupation-level exposure index values are kept out of this deck and the release until their licence terms are verified (WP-15 §2.5).

### Slide 6. Rules moved faster than technology

**Headline:** In 2025–26, dated policy changes reshaped review, authorization, hiring and disclosure work faster than any tool did, and more are scheduled for 2027.

**Body:** Chart **F09** (`f09_policy_instrument_timeline_2025_2027.csv`): timeline by domain; recorded, scheduled and pending items marked in text.
- **Review:** CEQ's NEPA regulations removed (final, effective January 8, 2026), so agencies follow their own procedures [NEPA-01]. *Seven County* (8–0 judgment) requires substantial deference to agency scope choices [NEPA-04]
- **Pending, not law ⟳:** the SPEED Act passed the House and has had no Senate action [NEPA-05]. A separate bipartisan Senate bill, S. 5653, was unveiled September 30, 2026 [NEPA-10]
- **Hiring and selection:** OFCCP's rescission of the EO 11246 regulations takes effect October 26, 2026 [SEL-01] ⟳. Colorado's SB 26-189 takes effect January 1, 2027, and the AG issued draft rules on October 6, 2026 [AIGOV-02; AIGOV-03] ⟳
- **Fire:** the January 2027 standards align USWFS and USFS federal qualifications. NWCG separately updated PMS 310-1 in January 2026 [WF-10]

**Speaker notes:** Other verified items on the timeline: the ESA "harm" definition rescission took effect September 14, 2026 and is litigated [ESA-01]. The Section 106 rewrite is at OIRA and unpublished ⟳ [NHPA-01]. The USFS project-level objection rule was published October 13, 2026 and takes effect November 12 [FOR-01]. OPM's April 24, 2026 list of 115 series is **proposed** for realignment. Never say "realigned" ⟳ [FED-04]. There is no final WOTUS rule ⟳ [CWA-01]. FAA Part 108 (drone BVLOS) is at OIRA and unpublished. That status rests partly on trade press ⟳ [UAS-01]. California SB 253 first reports are due November 10, 2026 [DISC-01]. Unverified registry items are excluded from this deck, among them the Fix Our Forests Act, the ePermit Act and IRA rescission amounts (WP-15 §2.1). Re-check every ⟳ item before presenting.

### Slide 7. Demand is moving toward monitoring, evaluation and validation

**Headline:** The durable demand signal is for monitoring design, evaluation and verified data, not less environmental work. Official projections show analytical and technician occupations growing faster than average.

**Body:** Charts **F05** (`f05_plan_monitoring_share_by_rule.csv`) and **F07** (`f07_bls_projections_2025_35.csv`).
- Forest plans written under the 2012 rule devote about 31% of components to monitoring, against about 3% under the 1982 rule (each plan weighted equally) [PLAN-01]
- BLS 2025–35: environmental science and protection technicians +7%, environmental engineers +6.3%, environmental scientists +6%, against +3.5% for all occupations [BLS-01; BLS-02]
- Slower or declining: foresters +2.2%, forest and conservation workers −2%, water and wastewater operators −6% [BLS-02]

**Speaker notes:** The plan data are a cross-era comparison of different plans, not a time series. About 95% of components come from USFS plans in western states, so do not generalize beyond them [PLAN-01]. The claim that coordination "tripled" is a weighting artifact. Under plan-equal weighting only partnership touchpoints rise, and weakly [PLAN-02]. Projections are context, not evidence of skill change, and BLS does not attribute these occupation projections to AI. Wildland firefighters are not counted separately in the +4% firefighter projection [BLS-02].

---

## Part 3. How roles are changing

### Slide 8. Thirteen priority roles on three corridors

**Headline:** EMST v2's first 13 role profiles sit on three corridors. Each starts in field or NGO work, crosses field, data and statecraft, and ends in state and federal roles.

**Body:** Chart **F10** (`f10_p1_corridors_and_roles.csv`): three swimlanes; emerging roles outlined dashed; footer "change indicator: none active".
- **COR-1:** corps member → field technician → monitoring and data technician, geospatial analyst, ground-truth and validation steward (emerging)
- **COR-2:** fire operations → fuels and prescribed fire specialist, fire intelligence analyst (emerging)
- **COR-3:** restoration project lead → environmental review, permit writing, compliance inspection → programme manager
- Each role has a two-page brief: `docs/package/briefs/`

**Speaker notes:** The corridors are a CA decision (ADR-0006), chosen because they cross all three crafts (field, data and statecraft) and end in recognizable state and federal positions. Role content is an agent draft: tasks, time shares and target levels have not been reviewed by people. Tribal variants are held under ADR-0007 and not shown. No craft-blend or exposure ratings are charted, because all are agent drafts awaiting multi-rater assessment (report NOT-BUILT-2).

### Slide 9. The new work is checking

**Headline:** EMST's draft role views show one pattern across all three corridors, for the pilot to test: the newly required work is checking AI identifications, AI-drafted permits and analyses, automated flags and detections. That work needs people with formed judgment.

**Body (agent drafts; every row "assessment pending"):**

| Role | Being compressed | Newly required |
|---|---|---|
| Field resource technician | Detection effort moves to stations and classifiers | Accept, correct or reject AI-suggested identifications; field-check AI condition maps |
| Geospatial analyst | Classification production | Transfer-test pretrained models locally; catch circular validation; review AI-written code line by line |
| Environmental review specialist | Drafting of analysis sections | Verify AI-drafted sections against the record; batch-review automated exclusion screening |
| Permit writer | First drafts of permits and fact sheets | Review AI-drafted permits; confirm or override automated completeness checks |
| Compliance inspector | Inspection report drafting | Confirm or dismiss automated anomaly flags before referral |
| Fire intelligence analyst | Continuous spread modelling | Adjudicate automated detections before resources are ordered |

**Speaker notes:** Source: WP-08 role-change views (`docs/build/WP-08/generated/change_view/`), which are agent drafts with evidence label S. They are hypotheses for the pilot and the job-analysis survey to test, not findings. The external evidence fits them: drafting tools are available at scale (F04), but review and permitting AI is not deployed (F03), so checking work is where change will show first if it comes. The briefs give the time share of each task and the drivers behind each change.

### Slide 10. What stays human is accountable judgment

**Headline:** In the draft role views, what stays with people is the judgment someone answers for, on the ground and on the record.

**Body (descriptive, from the agent-drafted role views; not a claim that this cannot change):**
- **On the ground:** reading a restoration site's response; the go/no-go decision from a test fire; findings of fact in an inspection; confirming an invasive detection
- **On the record:** deriving permit limits from standards; the significance determination; the reasoned explanation linking evidence to each choice; frank written advice
- **Over the tools:** deciding when a model is fit for a use, and when to restrict or retire it

**Speaker notes:** ADR-0027 requires the "stays human" rationale to be descriptive, not normative. These are the tasks the agent-drafted views keep with people and the reasons the drafts give. The fit with law matters for HR. OPM's August 27, 2026 memo treats AI drafting of position descriptions as generally not high-impact when the responsible official independently reviews and adopts the draft, while rating and ranking are presumed high-impact [V1-13; FED-05]. Deference doctrine after *Seven County* rewards documented agency reasoning [NEPA-04].

### Slide 11. The entry-path problem (a hypothesis)

**Headline:** Hypothesis: the tasks through which juniors form judgment are being cut by budgets and compressed by tools at the same time. If so, tomorrow's seniors will not be able to tell when AI is wrong.

**Body:** Table **F08** (`f08_entry_path_indicators.csv`): one row per indicator, each with its own unit and scope.
- The USFS hired no non-fire seasonal staff in 2025 and committed to 2,000 seasonals for 2026 [V1-04; WF-04]
- Paid conservation internship postings fell 43.8% on one board (Mar–Sep 2025), and AmeriCorps postings fell 42% [V1-14; WF-05]
- Under-30 share of the federal civilian workforce: 8.9% → 7.9% (Sep 2024–Jan 2026) [V1-02; WF-02]
- **Mechanism:** the same entry tasks (identification, plot work, first drafts, comment coding) are where tools compress repetition. **Evidence status:** hypothesis; untested in environmental work

**Speaker notes:** This is the career-ladder finding, presented as ADR-0027 and WP-14 require: a hypothesis with its mechanism and evidence status, not a result. The closest external benchmark is descriptive and not environmental. Employment of 22–25-year-olds in the most AI-exposed occupations was about 19% below the trend for less-exposed occupations as of June 2026, working through reduced hiring, and ADP data under-cover government [V4-03; IDX-02]. Do not cite it as causal or use the earlier 13% figure. The entry-rung signals above have fiscal and policy drivers. EMST's design response is formation provisions in its exploratory pathways: unaided work before AI assistance is credited. Examples are 50 identifications checked by an experienced observer, two effects sections drafted unaided, and one comment set of 200+ coded by hand (`docs/build/WP-07/formation_provisions.csv`; quotas are LC judgment for pilot calibration [J]). The pilot pre-registers the test.

---

## Part 4. Four futures and the moves that hold in all of them

### Slide 12. Four plausible futures

**Headline:** EMST's scenarios cross two uncertainties: whether public capacity is rebuilt, and whether AI earns trust in environmental decisions. The four results call for different bets but share one set of moves.

**Body (2×2):**

| | AI trusted and assured | AI brittle and contested |
|---|---|---|
| **Capacity rebuilt and coordinated** | **Assured Augmentation:** fewer document producers, more reviewers and ground-truth staff; quiet risk of "validation without formation" | **Human Premium:** larger human teams, wage premium for experienced reviewers and field leads, backlogs |
| **Capacity thin and fragmented** | **Platform Stewardship:** agencies become intelligent customers of vendors and platforms | **Patchwork Retreat:** capacity survives in state, university and NGO refugia; outcomes diverge by state |

**Speaker notes:** Source: FS, `docs/research/strategic-foresight/scenarios.md` §3–4. All narrative content is FS judgment [J]. Scenarios are not forecasts. Predetermined in all four: more fire and climate-hazard workload, expert retirements, and regulatory oscillation between administrations. One verified workload marker: as of October 11, 2026, the season had reached 63,884 fires and 9.0 million acres, 133% and 145% of the 2016–2025 average [FIRE-01]. No court has yet remanded an AI-assisted environmental record, so the Human Premium trigger events are speculative [S].

### Slide 13. Eight no-regret moves

**Headline:** Eight moves pay off in all four scenarios. They are options agencies can test now.

**Body:**
1. Protect a minimum entry cohort and redesign entry work so juniors still produce, field-check and defend their own work
2. Run a tacit-knowledge capture and succession sprint for high-risk, place-bound functions
3. Make AI validation a cross-cutting requirement for anyone who uses AI output, with a small model-risk function
4. Treat ground truth (reference plots, labelled data, calibrated observers) as infrastructure
5. Build skills-based mobility channels: translate federal experience into state and NGO terms; use details and IPAs
6. Strengthen intelligent-customer capacity: public data rights, auditability and exit clauses in AI and data contracts
7. Invest in intergovernmental agreement craft and fund partner capacity alongside any devolution
8. Stand up horizon scanning and a sentinel network linked to workforce plans

**Speaker notes:** FS `scenarios.md` §8.3 (NR-1 to NR-8), adopted for publication as guidance in View 4 (ADR-0027 §1). Contingent moves wait for their triggers (§8.4). Examples: scale AI-assisted review teams only after appellate decisions uphold AI-assisted records *and* headcount stabilizes (CM-1). Train drone BVLOS programme leads only once FAA Part 108 is published (CM-2). Fund fire-intelligence cohorts once agencies ingest new detection data on known access terms (CM-3). Acting too early has stated risks. FH and AS have not yet confirmed that adopters can act on every move, so present them as options [J].

---

## Part 5. What EMST v2 is and how to use it

### Slide 14. What EMST v2 is

**Headline:** EMST v2 is an open, versioned description of environmental work at task level. It is built to go into the documents that gate hiring and development, not to sit on a shelf.

**Body:**
- **Roles and variants** by employer type (federal, state, local, NGO, private, academic), with tasks, time shares, competencies and target levels, all labelled agent drafts until validated
- **Generated HR views:** a Federal Series Profile per OPM series and a State Class View per mapped class, each labelled "not a classification basis / not a job analysis / not for RIF or rating decisions"
- **Change and pathway views:** what is changing, with evidence status, and exploratory pathways with formation provisions
- **Open and private by design:** CC0 data, a static local-first explorer that stores no personal data, an accessibility target of WCAG 2.2 AA

**Speaker notes:** North star (charter): "If those blends are visible and portable, mobility follows." Product strategy, from ADR-0023 §2: exports into position descriptions, class specifications, postings, assessments, development plans and learning records take priority over browse-only views, and an artifact registry records which partner documents use EMST IDs. The evidence behind that strategy is that publishing a framework rarely changes hiring by itself. Burning Glass Institute and Harvard Business School research (reported February 2024) found that only 37% of firms announcing skills-based hiring followed through, and fewer than 1 in 700 hires changed [CM-011, pending WP-15]. Colorado made about 80% of its classifications skills-based, yet non-degree hires stayed at 25% in 2024, flat on 2023 [CM-012, pending WP-15]. WCAG 2.2 AA covers the Section 508 (WCAG 2.0 AA) and ADA Title II (WCAG 2.1 AA) standards. Title II compliance dates are April 26, 2027 and April 26, 2028 [CMP-01; CMP-03]. Explorer: `site/_site/`.

### Slide 15. Federal HR: tomorrow morning

**Headline:** Federal HR teams can start job analysis and position description work from EMST task bundles instead of a blank page, without using EMST to select anyone.

**Body:**
- **0400 Kit (0401 and 0404 first):** Federal Series Profiles, competency models, PD language by grade band, and task-level crosswalks from series **proposed** for realignment [FED-04]
- **Job-Analysis Starter Pack:** a task inventory and a matrix-sampled SME survey for one Tier 2 natural-resources series, run by your talent team on 3–5 vacancies
- **Forester PD in FES format:** an example regenerated from EMST data, labelled "DRAFT — SUBJECT TO CLASSIFICATION REVIEW", with factor levels left to the classifier
- **Guardrails:** no selection use without your own job analysis [SEL-02]; never "UGESP compliance" [SEL-01–03]; series shown under current codes until OPM finalizes

**Speaker notes:** Package contents: `docs/adoption/stage1b_design_partner_packages.md` (Packages A and B). The Forester PD: `docs/package/forester_pd_fes_draft.md`. It reuses no v1 duty percentages or exposure calls. AI-assisted drafting of a PD is generally not high-impact under OPM's August 27, 2026 memo when the official reviews, revises and adopts it [V1-13; FED-05]. Self-assessment questionnaires cannot rate and rank [FED-02], so agencies need job-analysis-based technical assessments, and EMST supplies the task frame for those analyses. Collective-bargaining obligations on PD changes are anticipated (ADR-0014 consequences).

### Slide 16. States, NGOs and educators: the same task language

**Headline:** States, NGOs and educators can crosswalk, credit and train against the same task language that federal teams use, so experience can be recognized when people change employers.

**Body:**
- **States:** State Class Views for pilot classes (PA, TX, WA, a county environmental health department, a municipal utility); a federal-to-state crosswalk to be validated with Pennsylvania, which counts federal experience as equivalent and reports 1,350 hires with federal experience by August 2026 [SL-031, pending WP-15]
- **NGOs:** use cases such as a corps member's transition portfolio held on the member's own device, or a posting rewritten with EMST IDs and adopted by a person
- **Educators and trainers:** course-level outcomes at target levels, with by-hand quotas where AI compresses learning tasks; Workforce Pell programmes are approved by governors working with state workforce boards [V3-03; SKL-02]
- **AI literacy:** EMST maps to the DOL AI Literacy Framework's five content areas [SKL-01]

**Speaker notes:** State packages: `docs/adoption/stage1b_design_partner_packages.md` Package C (Pennsylvania) and the X5 class records. NGO use cases UC1–UC6: `docs/adoption/stage1a_ngo_pilot_design.md` §5. The gap check is local-first: ratings stay in a file the member holds, and nothing about an individual is sent to EMST (ADR-0012). The DOL framework areas are Understand AI Principles, Explore AI Uses, Direct AI Effectively, Evaluate AI Outputs and Use AI Responsibly (TEN 07-25, February 13, 2026) [SKL-01]. WIOA is not reauthorized; H.R. 8210 was ordered reported 19–14 with no floor vote found [SKL-03].

---

## Part 6. The offer, the limits and the ask

### Slide 17. The offer, and what EMST cannot yet claim

**Headline:** We offer a 2027 NGO pilot and a federal–state design-partner track in parallel. We are explicit about what EMST v2 cannot yet claim and how it will earn each claim.

**Body:**
- **Stage 1a, NGO pilot (March 2027 – February 2028):** about 12 organizations (range 10–14) in two or three states, on the three corridors, for describe and develop uses only; expansion decision (gate G1) in March 2028
- **Stage 1b, design partners (January – December 2027):** co-produce the 0400 Kit, the Job-Analysis Starter Pack, the Pennsylvania crosswalk and a fire crosswalk keyed to the USWFS–USFS standards; partner staff act as shadow users of the pilot
- **Not yet claimed:** every task value is an agent draft; every change is "assessment pending"; no change indicator has moved; pathways stay exploratory until validated against observed moves (AUC ≥ 0.70 and better than naive baselines); tags with reliability α < .667 are never displayed
- **Not used:** v1 single-analyst statistics (methodology history only); occupation exposure index values (licence pending); Tribal content (held until a Tribal Advisory Council constituted by Tribal governments exists and approves)

**Speaker notes:** No organization has committed. The Corps Network and the named agencies are candidates, and an organization is a partner only when a signed record is in the commitment register (`docs/adoption/COMMITMENT_REGISTER.md`). Gate G1 includes "does this help me?" at ≥ 70% overall and ≥ 60% in every stratum, with a practitioner panel veto, and EMST IDs in a real gate artifact at ≥ 50% of pilot organizations (`docs/adoption/gate_metrics_G1_G2.md`). Reliability studies, a modified Delphi and a matrix-sampled job-analysis survey are designed now and run with people in Stage 1 (WP-11). EMST claims no alignment with O*NET, ESCO, OPM or state systems until a reviewed mapping set exists (ADR-0027 §3). No October 2026 posting baseline exists yet, so EMST makes no claim about posting volumes or content beyond the one-board figures cited (WP-15 §2.7). The Tribal outreach gate stays closed until reviewer compensation is funded and a Council exists. EMST does not contact or speak for any Tribal nation (ADR-0007).

### Slide 18. The ask

**Headline:** Three commitments in 2027 would let EMST test whether a shared description of the work helps people move and helps agencies keep what they know.

**Body:**
- **Federal agencies:** a design-partner letter (a talent team runs the Job-Analysis Starter Pack on 3–5 vacancies; classification staff review the 0400 Kit)
- **States and workforce boards:** join the federal-to-state crosswalk (Pennsylvania model) or a class-specification crosswalk, and share aggregate placement counts (n ≥ 5)
- **NGOs, corps and educators:** a pilot MOU with a named lead at about 0.1 FTE for ten months; map one curriculum or season plan
- **Everyone:** challenge the drafts. Practitioners are needed for SME panels, reliability studies and the Delphi

**Speaker notes:** Templates: `docs/adoption/pilot_mou_template.md` and the design-partner letter of intent in `stage1b_design_partner_packages.md` (Annex). First commitments sought, re-dated against verified facts (ADR-0014 §4): a federal design-partner letter by February 2027; three state forestry or environmental agencies plus one workforce board by April 2027; a pilot anchor partner plus 11 pilot MOUs by March 2027. All of these are targets, not commitments. EMST collects no personal data. Pilot outputs may not be used to rank, select or remove anyone, and any such use is a misuse incident that pauses expansion (`stage1a_ngo_pilot_design.md` §7, §9). Contact route and signatory follow the project lead's pending decision on hosting (Q3).

---

## Claims on this deck awaiting WP-15 entry or re-check

| Claim | Where | Status |
|---|---|---|
| CM-011 skills-based hiring follow-through (37%; under 1 in 700 hires) | Slide 14 notes | Sourced [E: CM-011], not in register: pending WP-15 |
| CM-012 Colorado classifications (~80%) and non-degree hires (~25%) | Slide 14 notes | Sourced [E: CM-012], not in register: pending WP-15 |
| SL-031 Pennsylvania 1,350 hires with federal experience | Slide 16 | Sourced [E: SL-031], not in register: pending WP-15 |
| ⟳ NEPA-05, NEPA-10, SEL-01, AIGOV-02/03, NHPA-01, FED-04, CWA-01, UAS-01 | Slides 6, 15 | Moving facts: re-check on the WP-15 §3 dates |
| FIRE-01 fire season figures | Slide 12 notes | Verified 2026-10-23; re-check by 2027-01-31 |
