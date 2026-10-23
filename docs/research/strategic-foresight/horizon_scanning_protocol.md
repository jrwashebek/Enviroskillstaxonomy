# EMST Horizon-Scanning and Sentinel Network Protocol (v0.1)

**Role:** Futurist / Strategic Foresight Lead (FS) · **Date:** 2026-10-23 · **Status:** Proposal for Chief Taxonomy Architect (CA) decision. It redesigns v1 Task 22 ("Sentinel Network Design → Living System Launch").

**Labels:** [E] evidence (source IDs in `sources.csv`) · [J] judgment · [S] speculation.

---

## 1. Purpose, and what changes from v1 Task 22

**Purpose.** Detect, early and systematically, changes in environmental work and in the forces acting on it: new roles, task shifts, tools, policy and legal events, funding and market shifts, data discontinuities. Code them so they can be compared. Turn them into dated L5 change-signal records that move lifecycle states in the taxonomy, inform workforce strategy, and say which scenario (SC1–SC4 in `scenarios.md`) is arriving.

### v1 Task 22 as planned [E: FS-052; v1 task sequence v6/v7]

- Five outputs:
  - a sentinel protocol (governance, survey instrument, update triggers, version propagation)
  - named fire nodes: NWCG, PFTC, state forestry associations, Tribal fire programs
  - named permitting nodes: federal review agencies, state programs, consulting firms
  - an annual survey scoped by `fire_context` and `permitting_context`
  - a first-survey launch plan
- v7 added the Wildfire Intelligence Center (WFIC) as a priority channel, with nodes at NIFC Predictive Services, USFS FAM intelligence, NOAA fire weather, state fire-intelligence programs and Tribal fire programs.
- Task 22 was sequenced *last*, after Delphi and publication.

### What is carried

- The idea of a sentinel network
- Fire, permitting and fire-intelligence as named channels
- An annual practitioner survey
- Version propagation [J; CA's register also carries this, FS-055/CA]

### What changes, and why [J]

1. **Scanning starts at v2.0, not after it.**
   - The v1 sequence left the taxonomy blind for the period of fastest change (2025–27).
   - Signals in `weak_signals.csv` show material shifts at roughly monthly frequency, for example: FireSat operational in July 2026 (FS-011), Part 108 in White House review (FS-022), CAREP launched (FS-027), the Roadless proposal (FS-040), SB 253 regulations final (FS-015).
2. **The annual survey is necessary but not sufficient.** v2 adds:
   - continuous machine intake (IA's engine)
   - monthly human scanning
   - a quarterly triage panel
   - event-triggered reviews
3. **Channels expand beyond fire and permitting** to every subsector in v2's scope, and to all seven sector actors.
4. **Sentinel recruitment is stratified, and sentinels are compensated.** This corrects the austerity bias v1 itself predicted: under contraction, public field and statecraft holders have the least slack to participate (FS-051).
5. **Every signal is coded to a shared schema** (§6) and becomes an L5 record. Survey answers alone cannot be audited or compared over time.
6. **The scenario signpost link is explicit.** Each signal can mark which scenario it points toward. This turns scanning into strategy input, not just taxonomy maintenance.

---

## 2. Design principles

1. **Leading over lagging.** Pilots, procurements, credentials, court decisions and first-of-kind postings come before occupational statistics. Weight them accordingly, and confirm them with lagging data later.
2. **Disconfirmation is built in.** For every promoted trend, someone is assigned to look for counter-signals (§8.3).
3. **Balanced voices.** No single sector actor, craft or career stage may provide more than 30% of sentinel inputs in a cycle (§5.3).
4. **Two-speed governance.** Watch-layer items move quarterly and are non-normative. Core content moves annually, with validation (IO). This protects HR users from churn.
5. **Sovereignty and privacy by design.** Tribal-sourced signals follow TN's protocol and CARE principles. Person-level data is never stored in L5 (CP).
6. **Cheap enough to survive year five.** The minimum viable configuration (§12) must be fundable by one host organization (AS).

---

## 3. Cadence

| Cycle | What happens | Who | Output |
|---|---|---|---|
| **Continuous** | Automated intake: postings, PDs, land-plan requirements (OpenLMP), Federal Register, procurement, dockets, preprints, news. LLM pre-coding with confidence scores | IA engine; FS sets the queries | Candidate signal records (status `machine-coded`) |
| **Event-triggered (within 10 working days)** | Rapid review when a pre-registered trigger fires: e.g., SPEED Act enacted; Part 108 final; appellate ruling on an AI-assisted record; USFS fire merger; major dataset discontinued; catastrophic hazard event | FS lead plus the relevant channel lead | Rapid note; possible interim watch items |
| **Monthly** | Human scan of priority sources (§4); validate machine codes; sentinel submissions reviewed | FS scanners (rotating DB members) | Monthly digest (2 pages): top 10 signals, signposts moved |
| **Quarterly** | **Triage panel**: score and route signals, promote or lapse watch items, update the signpost dashboard | Panel: FS lead (chair), IA, one craft lead in rotation (FC/DC/SC), one DB subsector expert, one sentinel representative, TN when Tribal signals are on the agenda, CM for workforce-voice items | Watch-list update; RFCs to CA; scenario-signpost update |
| **Annual** | **Signals Review and sentinel survey**: synthesize the year; survey sentinels; review watch to emerging to established promotions; retrospective on missed signals; publish a "State of Environmental Work" brief | FS plus CA; IO validates promotions to established | Inputs to the minor release; annual brief |
| **Every 3 years (or after a wildcard)** | Scenario refresh: re-run drivers, re-check axes, re-run the stress test | FS with a sector-actor foresight session (§13) | Revised `scenarios.md`; stress-test report |

---

## 4. Intake: sources by STEEP+V, with owners

The listed sources are a starting set, not a boundary. Scanners add sources and record why (Charter).

| Category | Priority sources (examples) | Signal types | Intake mode | Owner |
|---|---|---|---|---|
| Technological | Agency AI use case inventories (FS-031); CEQ Permitting Innovation Center (FS-007); PNNL PermitAI and NEPATEC (FS-008, FS-044); EFA/FireSat (FS-011); NASA ESTO digital twins (FS-030); FAA BVLOS and DFR (FS-022); arXiv/EarthArXiv; registry dMRV programs (FS-024, FS-043) | pilot, tool-adoption, capability | Machine plus monthly | IA, DC |
| Environmental | NIFC IMSR and Predictive Services (FS-034); drought and flood monitors; Climate Central disaster database (FS-037); IPBES/IPCC outputs (FS-033) | demand pressure, data discontinuity | Machine plus seasonal | FS, FC |
| Economic | SAM.gov and state procurement; USAspending; carbon and nature market reports (FS-025); disclosure regulators (CARB, EFRAG; FS-015, FS-050); philanthropic grants | funding-event, market-event | Machine plus quarterly | PS, FS |
| Political | Federal Register; Congress.gov; CRS (FS-001, FS-019); GAO (FS-020, FS-029); state legislatures (e.g., NCSL trackers); court dockets (D.C. Circuit, Ninth Circuit) | policy-event, legal-decision | Machine plus monthly | SC, FH, SL |
| Social and workforce | OPM workforce data (data.opm.gov); USAJOBS and state job boards; Conservation Job Board (FS-026); corps networks; professional societies (SAF, TWS, AFS, NAEP, AWWA, WEF, NEHA); credential launches (FS-027); AI expert-task marketplaces (FS-038) | new-role, entry-path, credential | Machine plus monthly | IA, LM, LC, CM |
| Values | Tribal organizations and published Tribal records (FS-040), **only via TN protocol**; public-comment records; EJ organizations; polling | legitimacy, sovereignty | Monthly (human only) | TN, CM |
| Demand signals | OpenLMP plan components (desired conditions, monitoring requirements, coordination touchpoints) | requirement-shift | Machine, per plan revision | IA |

---

## 5. Who scans

### 5.1 Core team [J]

- **FS lead.** About 0.3 FTE in steady state; owns the protocol, triage and scenarios.
- **IA engine.** Automated intake and pre-coding; reports uncertainty and never smooths it over (charter).
- **Rotating scanners.** Two or three DB subsector experts per quarter, about 4 hours each per month.

### 5.2 Institutional channels (nodes)

Each channel has a named lead organization or person and a quarterly check-in.

| Channel | Example nodes (to be confirmed by AS/SL/FH/TN) | Scope selector |
|---|---|---|
| Fire operations and fire intelligence (v1 + WFIC) | NIFC Predictive Services; USFS FAM and USWFS staff; NWS IMET program; CAL FIRE Office of Wildfire Technology R&D; Colorado Center of Excellence; Tribal fire programs (via TN); utility situational-awareness centres | fire work function and subsector tags |
| Environmental review and permitting (v1) | Federal review agencies; Permitting Council; state environmental review programs; consulting firms; NAEP | Work function "Authorize & regulate" plus the S1–S6 profile |
| Water and wastewater | State drinking-water and clean-water programs; utilities (AWWA/WEF networks) | water modules |
| Air quality and environmental health | State and local air agencies; county environmental health (NEHA network) | air and EH modules |
| Corporate disclosure and environmental markets | CARB disclosure program; assurance providers; registries; corporate sustainability teams | ESG and markets modules |
| State and local government | ECOS-type state networks; state forestry associations (CWSF; FS-049); NACo | sector actor = state/local |
| Tribal channel (governed by TN) | Inter-Tribal organizations and Tribal natural resource programs that **choose** to participate | Tribal sector actor; CARE governance |
| Workforce pipeline | Conservation corps networks; university programs (SAF/ABET-accredited); credential providers (e.g., CAREP) | entry-path, credential |

### 5.3 Practitioner sentinels (stratified panel)

- **Size.** 60–90 sentinels on two-year staggered terms. [J: enough for at least three per actor-by-craft cell in the main cells.]
- **Stratification quotas:**
  - Sector actor: federal, state, local, Tribal, NGO, private, academic. Each ≥8%, none >30%.
  - Primary craft: FC, DC, SC. Each ≥25%.
  - Career stage: early (0–5 years) ≥25%, mid ≥30%, senior ≥25%.
  - Subsector coverage matched to v2 modules.
  - Include people who have moved between actors (CM) and people displaced in 2025–26.
- **Compensation.** Honoraria, or employer-recognized professional development time. Volunteer-only panels skew toward the well-resourced. [J; FS-051 austerity-bias argument]
- **Asks:**
  - A quarterly two-minute "What changed in your work?" pulse (§9)
  - Ad hoc signal submissions
  - The annual survey
  - An optional foresight session each year
- **Protection.** Submissions can be anonymous to the public record. Identities are held separately under CP's privacy rules.

---

## 6. Signal coding scheme (L5 signal record)

All signals, whether machine, scanner or sentinel, use one schema. Controlled vocabularies are versioned in L0.

| Field | Values / notes |
|---|---|
| `signal_id` | Persistent ID (IA scheme) |
| `captured_date`, `event_date` | ISO dates; `event_date` may be approximate (`2025`, `2025-05`) |
| `title`, `summary` | One line; ≤60 words |
| `source_ids` | Resolve to the project sources registry |
| `steepv_category` | Social · Technological · Economic · Environmental · Political · Values |
| `driver_ids` | From `drivers.csv` (versioned driver list) |
| `signal_type` | new-role · role-change · task-shift · tool-adoption · pilot · procurement · credential · policy-event · legal-decision · funding-event · market-event · data-discontinuity · incident · requirement-shift · counter-signal |
| `sector_actors` | federal · state · local · tribal · ngo · private · academic (pipe list) |
| `subsector`, `geography` | Module code; jurisdiction |
| `crafts_affected` | FC · DC · SC (pipe list) |
| `linked_entities` | v2 IDs of tasks, competencies, roles or tools affected (or `none-yet`, which flags a candidate new entity) |
| `novelty` | 1 known pattern · 2 new instance of an emerging pattern · 3 first-of-kind |
| `source_reliability` | A primary or authoritative · B reputable secondary · C partisan or vendor · D unverified |
| `corroboration` | 1 single source · 2 two independent sources · 3 multiple source types (e.g., pilot plus postings plus policy) |
| `impact` | 1 local or niche · 2 affects a role or subsector · 3 affects multiple actors or crafts, or a pathway |
| `horizon` | now · 1-3y · 3-5y · 5-10y · 10y+ |
| `scenario_signpost` | SC1 · SC2 · SC3 · SC4 · none (pipe list allowed) |
| `evidence_label` | E · J · S |
| `proposed_action` | log · watch · deep-dive · RFC · alert |
| `coder_type`, `coder_id`, `confidence` | human / llm / sentinel; 0–1 |
| `care_flag` | true if Tribal or Indigenous data, which routes to TN review before any publication |
| `personal_data_flag` | must be false for storage in L5 |
| `review_status` | machine-coded · human-validated · triaged · closed |

### Priority score

**Priority = impact × reliability weight × (novelty + corroboration)**

- Reliability weights: A = 1.0, B = 0.8, C = 0.5, D = 0.25. The range is 0.5 to 18.
- Routing:
  - ≥9 → deep-dive
  - ≥12 with linked_entities = `none-yet` → candidate entity (watch)
  - Any legal decision or statute with an effective date → RFC regardless of score

[J: the thresholds are starting values; recalibrate after two quarters against panel decisions.]

**Coder reliability.** Each quarter, double-code a 10% sample (human against human, and human against LLM). Target Cohen's κ ≥ 0.6 on `signal_type`, `impact` and `scenario_signpost`. Report results in the annual review (IO to confirm the statistic).

---

## 7. Triage and routing

| Route | Criteria | Next step | Time limit |
|---|---|---|---|
| **Log** | Low priority, or a duplicate | Stored in L5; counted toward corroboration | Monthly |
| **Watch** | Plausible change, insufficient evidence; or a candidate new entity | Creates or updates a **watch item** (lifecycle state `watch`) with review-by date = +12 months | Quarterly panel |
| **Deep-dive** | Priority ≥9, or a cluster of ≥3 related signals | Assigned analyst writes a 2–4 page note; may propose an RFC | Next quarter |
| **RFC** | Evidence meets a lifecycle promotion threshold, or a statute, regulation or legal decision with an effective date | Change request to CA, with evidence pack | CA decision within one release cycle |
| **Alert** | A wildcard or trigger in `scenarios.md` §8.4 fires | Rapid note to CA, AS and pilot adopters; signpost dashboard updated | 10 working days |

---

## 8. How signals become taxonomy versions

### 8.1 Lifecycle states (summary; full rules in `report.md` §6)

The states run: `watch` (L5 only) → `proposed` → `emerging` → `established` → `declining` → `withdrawn`. Two side states and one overlay apply:

- `lapsed`: a watch item expired with no new evidence.
- `merged`: absorbed into another entity.
- `protect` (overlay): a capability is kept even when demand declines.

States apply to L1 competencies, L2 tasks, L3 role profiles and L4 tools alike. They align with the CA's proposed lifecycle status (`docs/audit/architecture-audit.md` §11) and add a pre-content `watch` state and the `protect` overlay.

### 8.2 Promotion evidence thresholds (starting values) [J]

- **Watch → proposed.** At least three independent signals of at least two signal types from at least two sector actors. Alternatively, one authoritative mandate (statute, regulation, standard) with an effective date. Plus a draft definition linked to existing L2 tasks.
- **Proposed → emerging.** Observable in work: at least 10 postings or PDs (IA engine) across at least two actor types in 12 months, or a named program operating it. A provisional task bundle and feeder roles are identified.
- **Emerging → established.** Sustained demand (at least 30 postings or PDs across at least three actor types over 12 months, or one major employer's classification or PD standard). SME validation meets IO's agreement standard. Assessable indicators are defined (IO). **Only established content is eligible for selection uses** (IO lane).
- **Established → declining.** Demand share down at least 30% over 24 months, or substitution confirmed using v1's S-confirmation checklist (full task performance, scoping bracket, modal deployment; FS-056). A `protect` check is mandatory.
- **Declining → withdrawn.** Below threshold for 36 months, no `protect` flag, and CA approval. A withdrawn entity keeps its ID and crosswalks (never deleted).

### 8.3 Counter-signal duty

Every proposed promotion to `established`, and every move to `declining`, must include a short counter-signal search: evidence the trend is stalling, reversing or confined to one actor. Example: agentic AI cancellations (FS-054) against agentic AI training markets (FS-038).

### 8.4 Release mapping (with DE and IA)

| Release type | Content |
|---|---|
| Patch (x.y.**z**) | Wording fixes; signpost dashboard updates; new L5 records |
| Minor (x.**y**.0) | Lifecycle promotions and demotions; new proposed or emerging entities; tool-layer additions (L4 may also run monthly as its own versioned layer) |
| Major (**x**.0) | Structural changes (families, work functions, level model), decided by CA |

Every release publishes a **Signals appendix** listing the signals and decisions behind each lifecycle change. This is the provenance chain from signal to decision to version.

---

## 9. Instruments

### 9.1 Quarterly sentinel pulse (about 2 minutes)

1. In the last three months, has any task in your work been done differently because of a new tool, AI, a policy or law, funding, or staffing change? (yes/no; which driver?)
2. Describe the change in one or two sentences.
3. Did a task you used to do as a beginner disappear, shrink, or move to someone else or to a tool? (CLD probe)
4. Have you seen a job title, posting or role you had not seen before? (title, employer type, link)
5. Which of these feels closest to where your part of the sector is heading? Four one-line scenario descriptions, plus "none".

### 9.2 Annual sentinel survey (about 20 minutes)

This extends the v1 annual survey; context scoping uses v2 work functions and subsectors, not only `fire_context` and `permitting_context`.

- **A. Role and context:** sector actor; subsector; work function; career stage; craft self-profile.
- **B. Task change:** for 8–12 tasks drawn from the respondent's role profile (L3), rate change over the past year. Scale: none, tools only, method changed, task moved to AI or a tool, task moved to another role or organization, task new.
- **C. Learning substrate:** "Where do beginners in your unit now learn X?" for that role's CLD-flagged tasks.
- **D. Emerging roles:** confirm or reject current watch-list roles from your vantage point.
- **E. Barriers:** pay, housing, classification, credential, culture (v1 barrier taxonomy; FS-051).
- **F. Scenario signposts:** which indicators do you see locally?
- **G. Open:** what is the taxonomy missing?

---

## 10. Bias controls and quality

- **Austerity correction.** Apply the quotas in §5.3. Weight responses by cell if a cell under-responds. Report the cell response rates each year. [J; FS-051]
- **Vendor-signal discount.** Reliability C applies to vendor capability claims (e.g., FireSat detection size; FS-009, FS-011) until they are independently corroborated.
- **Missed-signal retrospective.** Each year, list changes that surprised the team and trace whether signals existed and why they were not routed. This is the main learning loop.
- **Inter-coder reliability.** See §6.
- **Echo-chamber check.** At least 20% of monthly scanning time goes to sources outside environmental management: adjacent professions (law, accounting, radiology) and other sectors' foresight units (FS-032).

---

## 11. Data governance

- **Tribal and Indigenous data.** Signals involving Tribal programs, knowledge or communities get `care_flag = true`. They are not published or linked to entities until TN's protocol review is complete. Published Tribal records (e.g., FS-040) may be cited as sources; their content is not converted into taxonomy content without consent. [J; CARE; TN lane]
- **Personal data.** L5 holds no person-level data. Sentinel identities are stored separately, with access controls (CP).
- **Licensing.** Store link, summary and coding for copyrighted or paywalled sources, not their text.
- **Machine coding.** LLM-coded records carry `coder_type = llm` and a confidence score, and stay `machine-coded` until a human validates them (IA lane).

---

## 12. Resourcing and ownership (for AS: who maintains this in year five?)

| Configuration | People | Notes |
|---|---|---|
| **Minimum viable (year 5 floor)** | FS lead 0.3 FTE; IA engine maintenance 0.2 FTE; 30 sentinels; quarterly triage; annual review | Keeps signposts and the watch list alive under SC3/SC4 conditions |
| **Standard** | FS 0.5 FTE; IA 0.3 FTE; 2–3 rotating scanners; 60–90 sentinels with honoraria; one sector-actor foresight session a year | Recommended for v2.0–v2.3 |
| **Enhanced** | Plus channel leads funded in fire, permitting and water; partner foresight units | If a host institution funds it |

[J: FTE figures are planning estimates, not costed.]

---

## 13. First-year launch plan (proposed)

| Month (from v2.0 approval) | Milestone | Responsible |
|---|---|---|
| 0–1 | CA approves protocol; L5 signal schema implemented | CA, DE, IA |
| 1–2 | Seed L5 with `weak_signals.csv` (44 signals) and `role_signals.csv` (27) as `human-validated` records; watch list created | FS, DE |
| 1–3 | Channel leads confirmed for fire/WFIC, permitting and one non-forestry subsector (water recommended) | AS, SL, FH, DB |
| 2–4 | Sentinel recruitment (first 30, quota-checked); TN protocol for a Tribal channel drafted with real Tribal partners, or the channel is deferred | FS, CM, TN |
| 3 | First quarterly triage panel | FS (chair) |
| 4 | First sector-actor foresight session (NGO pilot cohort plus one federal and one state agency) | FS, AS |
| 6 | Second triage; first coder-reliability check | FS, IA, IO |
| 9 | Third triage; sentinel panel expanded toward 60 | FS |
| 12 | First annual Signals Review and survey; first missed-signal retrospective; Signals appendix in the minor release | FS, CA, IO |

---

## 14. Facilitator guide: a 2¾-hour foresight session with sector actors

**Purpose.** Help a mixed group (federal, state, Tribal where invited, NGO, private, academic, early-career and senior) see how their work may change, test current workforce plans and EMST content against the four scenarios, and produce coded signals and no-regret moves.

**Group.** 16–32 people in four tables of 4–8. Mix actors and crafts at each table. Have at least one early-career person per table.

**Roles.**

- Lead facilitator
- One table host per table, who keeps time and captures notes on templates
- A note-taker who codes signals live, if possible

**Materials.**

- One-page scenario cards (SC1–SC4, from `scenarios.md` §4)
- 20–30 signal cards drawn from `weak_signals.csv`, mixed across categories and including two counter-signals
- Role cards (from `role_signals.csv`)
- Three Horizons wall template
- Wind-tunnel grid
- No-regret and trigger template
- Signal submission forms (schema in §6, simplified)

**Ground rules.**

- Scenarios are not predictions.
- Every scenario is someone's best case and someone's worst case.
- Speak from your own experience; no one speaks for a community they do not represent.
- Indigenous knowledge is shared only if, and as, the holder chooses, and it is not recorded without consent.

### Agenda

| Time | Segment | What happens | Output |
|---|---|---|---|
| 0:00–0:10 | **Opening** | Purpose; ground rules; one-sentence introductions ("one change in my work this year") | Warm-up signals |
| 0:10–0:40 | **Three Horizons on one function** (e.g., environmental review, or field monitoring) | Wall exercise. H1: what is fading? H3: what future practice is already visible in pockets? H2: which innovations bridge (H2+) and which get captured (H2−)? | Horizons map; candidate H3 practices |
| 0:40–1:00 | **Signal gallery** | Participants walk the signal cards, dot the three that surprise them most and the one they doubt most, and add their own on blank cards | Ranked signals; new signals (coded later) |
| 1:00–1:10 | Break | | |
| 1:10–1:45 | **Scenario immersion** | Each table takes one scenario and writes a "day in the life, 2033" for two roles: an early-career worker and a supervisor, in a named sector actor. Prompts: What does the person do before lunch? What did they learn in their first two years, and from whom? Which tasks does AI or a vendor do? What would break if it failed? | Four role narratives; role signals |
| 1:45–2:10 | **Wind-tunnel** | Tables test (a) their organization's current workforce plan, or three draft EMST competencies or roles, and (b) the three strategies (ST-S, ST-A, ST-M) against their scenario. Rate each item works, partial or fails, with one reason | Completed grids |
| 2:10–2:35 | **Backcast to moves** | Plenary. Each table names moves that worked in its scenario. The group sorts them into **no-regret** (works in ≥3 scenarios) and **contingent** (name the trigger). Compare with NR-1 to NR-8 | No-regret list; triggers |
| 2:35–2:45 | **Close** | Commitments (who will try what in 90 days); invitation to join the sentinel panel; how outputs will be used and credited | Commitments; sentinel sign-ups |

### Adaptations

- **Two-hour version:** drop Three Horizons, shorten immersion to 25 minutes.
- **Virtual:** use a shared whiteboard, breakout rooms and pre-read scenario cards.
- **Tribal-convened session:** design and facilitation are led or co-led by the Tribal host. The agenda and recording follow the host's rules. EMST staff attend as guests (TN).
- **Single-agency session:** replace the actor mix with a craft and career-stage mix; wind-tunnel the agency's own workforce plan.

### Facilitator tips [J]

- Watch for "SC3 is just efficiency" and "SC4 can't happen here". Ask what evidence would change the speaker's mind, and point to the signposts.
- Keep early-career voices central in the immersion segment. Their answers to "where did you learn this?" are the CLD evidence.
- Code signals the same day and send participants the coded list within two weeks, so they see their input used.

### After the session

1. Within two weeks, enter new signals in L5 and add role signals to the watch list.
2. Send participants a two-page summary.
3. Report wind-tunnel failures on EMST content to CA as RFCs.
