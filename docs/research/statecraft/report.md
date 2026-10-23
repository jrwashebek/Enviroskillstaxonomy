# Statecraft Lead (SC): Phase 2 Report

**Role:** Statecraft Lead (SC) · **Date:** 2026-10-23 · **Folder:** `docs/research/statecraft/`
**Evidence labels:** [E] evidence I read (source IDs in `sources.csv`); [J] my judgment, with its basis stated; [S] speculation, with what would confirm or refute it.

---

## 0. Summary

**Definition.** Statecraft is the learnable capacity to turn knowledge and public purpose into decisions that are *authorized, legitimate, resourced and durable*. It works through law and administrative procedure, institutions, budgets and relationships across jurisdictions and sectors. Its defining deliverable is **a commitment that holds**: a review, permit, rule, agreement, budget or coalition that survives challenge, staff turnover and implementation. Like any other professional competency, it can be observed in work products, simulations and outcomes.

**Key findings.**

1. **The ground moved more in 2025–26 than in any period since NEPA's 1978 regulations** [J]. Government-wide NEPA regulations no longer exist (final removal 2026-01-08) [E: SC-011]. Each department now runs its own procedures, some of them in handbooks that change faster than rules [E: SC-014, SC-040]. Courts owe agencies "substantial deference" [E: SC-012]. Sponsors can pay for an EA in 180 days or an EIS in a year [E: SC-013]. Public involvement for CEs and EAs is now discretionary under DOI's procedures [E: SC-038]. The workforce effect is a shift **from rule-following to judgment that must be justified in a record**.
2. **Federal substantive scope is contracting while partnership authority is expanding.** On the contracting side: the ESA "harm" definition is rescinded [E: SC-018], the GHG endangerment finding is rescinded [E: SC-024], WOTUS is proposed narrower [E: SC-023], and GHGRP cuts are proposed [E: SC-026]. On the expanding side: there were 540 Good Neighbor agreements in FY2025, counties and Tribes now retain revenue, and recreation GNAs are new [E: SC-030]; states are legislating their own capacity [E: SC-034]. Statecraft demand moves toward **state, local, Tribal and corporate venues, and toward agreement-making**.
3. **AI is already doing statecraft's entry-level work.** PNNL's comment-analysis and search services are in production, drafting tools are in beta, and a drafting benchmark estimates 1–5 hours saved per EIS subsection [E: SC-009]. All four of v1's "Substitution" calls fall on statecraft entry tasks (legal comparison, compliance checklists, policy literature review, comment theme analysis) [E: SC-004]. The largest statecraft risk is not that the craft disappears; it is that **the apprenticeship that produces it disappears**.
4. **Statecraft is teachable and assessable, but the field has codified it more than it has assessed it.** The UK Policy Profession Standards set three levels for Working with Ministers, Parliament and Law, Finance, Multilevel Government and Participation [E: SC-042], but they specify no assessment method [E: SC-041]. I found no validation studies of environmental statecraft assessment. That is a finding, not a gap to paper over.
5. **v1's reform flags are already stale, and its workflow model is too NEPA-centric.** They should be replaced by a dated policy-instrument layer and a durable mechanism vocabulary (`policy_landscape_2026.csv`, 34 instruments; `driver_mechanisms.csv`, 16 mechanisms). The workflow facet needs "Make rules & policy" and "Resource & finance" functions, and Review must stay separable from Authorize (§8).

---

## 1. Method, sources and limits

**What I read.** For v1 I used the craft criteria, workflow-stage definitions, Task 10 record, Task 13 synthesis, D4–D6 Sections 9–10 and Structural Conditions [E: SC-001–SC-007], plus the normalized v1 baseline [E: SC-004]. Before the coordinator's on-disk copies arrived I read the same documents through past-conversation retrieval; the texts matched. I also read the CA's architecture hypotheses and audit, and the OpenLMP sister repo's 2026-10-21 permitting-standards note [E: SC-009].

**External sources.** I ran about 21 targeted web searches and successfully read about 30 sources. I preferred primary legal and government sources (Federal Register, Supreme Court opinion, CRS, agency releases, state legislative record, UK GOV.UK standards) and fell back to current law-firm analyses where primary text was not reachable. The reasons for each choice are in `sources.csv`.

**Limits, stated plainly.**
- The **shared web-search budget ran out** partway through the session. After that I could only fetch URLs already surfaced.
- Several primary URLs were **blocked**: EPA NPDES Permit Writers' Course, IAF CPF, IAP2, NASPAA, OPM ECQs, UK i.AI Consult, PNNL PermitAI pages, DOIs for the negotiation and collaborative-governance literature. They are recorded as `unverified` in `sources.csv`. Claims that rest on them are labeled [J].
- **Not verified this session:** CEQA 2025 reforms; other state SEPAs; NHPA §106/ACHP changes; CWA §401; federal FY2026–27 appropriations; Fix Our Forests enactment after Nov 2025; JSO 3403 status; Udall Foundation conflict-resolution program status; federal NEPA staffing levels. These are marked as placeholders in the CSVs.
- For **PNNL PermitAI** I relied on the sister repo's [V-src] verification from two days earlier [E: SC-009], because I could not reopen those pages myself.

---

## 2. Statecraft for v2: definition and components

### 2.1 The refined test

v1 defined statecraft as "institutional navigation, policy, stakeholder engagement, and governance". Its irreducible value was "enabling decisions across competing interests … that translates technical capacity into authorized action" [E: SC-001]. The second half is right; I keep it. The first half lists *activities*, and that is why statecraft became a residual category in v1 (§6.1).

**v2 test (proposed).** A competency is Statecraft-primary when its defining deliverable is a **commitment that requires authority, legitimacy or agreement from another institution or the public, and must hold over time**. Removing the procedural, relational or fiscal work would leave a technically sound product that is unauthorized, illegitimate, unfunded or reversible. [J, extends SC-001]

Four properties define the deliverable:
- **Authorized**: within someone's legal power, by correct procedure.
- **Legitimate**: the right parties were heard and could see their effect.
- **Resourced**: funded and staffed.
- **Durable**: survives litigation, turnover and administration change.

These four properties make the competency assessable, because each leaves evidence: a record, an engagement trail, a budget, a track record.

### 2.2 Nine components

| # | Component | What it delivers | Typical work products (observable) | Candidate competencies |
|---|---|---|---|---|
| SC1 | **Legal-procedural fluency** | The right authority, procedure and level of review, applied correctly | Authority maps, CE/EA/EIS determinations, procedure-version notes | SC-C01, SC-C03, SC-C12, SC-C17 |
| SC2 | **Institutional navigation and intergovernmental coordination** | Multi-agency and multi-level action on a shared schedule | Coordination plans, joint schedules, cooperating-agency decisions, oversight correspondence | SC-C09, SC-C14 |
| SC3 | **Coalition, partnership and agreement building** | Shared implementation across boundaries | GNA and co-stewardship agreements, MOUs, partnership charters | SC-C08 |
| SC4 | **Negotiation and conflict resolution** | Agreed terms where interests conflict | Negotiated conditions, mitigation, settlements, mediated agreements | SC-C07 |
| SC5 | **Public engagement and legitimacy** | Decisions the affected public and governments can accept as fair | Engagement plans, what-we-heard reports, response-to-comments, a separate G2G consultation record | SC-C06, SC-C13 |
| SC6 | **Fiscal and appropriations craft** | Money that arrives, on terms that work | Budget justifications, CR plans, fee and cost-recovery designs, retained-revenue ledgers | SC-C10 |
| SC7 | **Political judgment and timing** | Choices that survive changes of administration and litigation | Durability and reversal-risk memos, decision-window calendars, briefings | SC-C11, SC-C18 |
| SC8 | **Accountability and integrity** | A record that shows why the decision was reasonable, and honest dealing | Administrative record, AI-provenance logs, disclosures | SC-C02, SC-C05, SC-C15 |
| SC9 | **Instrument design and drafting** | Binding text that can be enforced and implemented | Permit conditions, agreement terms, policy language, decision documents | SC-C16, SC-C04 |

The nine components are a reference vocabulary (L0 in the CA's layering), not nine competencies. Competencies combine them. SC9 is the medium most of the others are performed in, and it is the one AI touches most [J].

### 2.3 Teachable, not a trait

The common belief is that some people are "naturally political". That belief is not harmless. If statecraft is a trait, nobody designs the pipeline that produces it, and AI can quietly remove that pipeline (§5.4) [J].

My claim is that each layer of statecraft has a known learning mechanism and a known assessment method.

| Layer | Examples | How it is learned | How it is assessed | Evidence |
|---|---|---|---|---|
| **Knowledge** | Which authority applies; how a CE is documented; how appropriations lapse | Courses, procedure briefings, case files | Knowledge tests, seeded-case screening | [E] Agencies retrain staff on procedure explicitly: Reclamation's 2026 deck walks staff through the new DOI handbook, CE consolidation, the Responsible Official role, and the duties that remain (ESA, §106, G2G) [SC-038] |
| **Skill** | Negotiating conditions; facilitating a contested meeting; drafting enforceable terms | Simulations with structured feedback, comparing cases, drafting clinics | Standardized role-plays scored on behaviorally anchored scales (BARS); work samples | [J] There is experimental and review evidence that negotiation is trainable and that comparing cases improves transfer [SC-050, SC-052], and collaborative competencies have been identified among federal managers [SC-051]. I could not re-read these sources this session. |
| **Judgment** | When to engage beyond the legal minimum; how durable an instrument is; where to draw the scope boundary | Supervised exposure, debriefs, rotations across actors, case method | Structured "what-if" interviews, situational judgment tests, prediction logs reviewed for calibration | [E] The UK standard codifies judgment-level outcomes, e.g., Level 3 "Trusted and able to provide free and frank advice"; "how and when to react in unexpected situations" [SC-042]. [J] Prediction logs make judgment observable over time. |
| **Relationships** | Trust with cooperating agencies, Tribal staff, regulators | Sustained joint work; agreements built to survive turnover | Counterpart (360) feedback; agreement durability | [E] Co-stewardship agreements are "institutionalized to survive agency turnover and preserve institutional memory" [SC-036]. [E] Wildland fire's Position Task Books show that a sector can standardize performance documentation for consequential, judgment-heavy work [SC-007, secondary]. |

**Where the evidence is thin.**
- The strongest public-sector precedent, the UK standards, is *developmental*. Its descriptors are mostly "Understands …" and "Champions …", and it specifies no assessment [E: SC-041, SC-042]. That is the same weakness as v1's "Manages … independently" [E: SC-004].
- I found **no published validation study** of a statecraft assessment in environmental agencies.
- `statecraft_proficiency_anchors.csv` proposes 40 behaviorally anchored indicators with named assessment methods. They are [J] until IO pilots them.

### 2.4 What statecraft is not

- **Not general management.** Scheduling, facilities, equipment and supervision are organizational management. They produce internal outputs, not commitments that cross institutional boundaries [J].
- **Not communication in general.** Writing and speaking are enabling skills. They become statecraft when they produce authorization or legitimacy (a briefing that leads to a decision; a response-to-comments that closes the record) [J].
- **Not Datacraft with a policy topic.** An economic impact analysis is DC. Choosing how that analysis is used, defended and documented in a decision is SC [J, consistent with SC-001's budgeting split].

---

## 3. Statecraft across sector actors

### 3.1 Eight roles compared

| Role | Authority basis | Principals and accountability | Characteristic instruments | Distinctive statecraft |
|---|---|---|---|---|
| **Federal NEPA lead / IDT leader** | NEPA as amended 2023; the department's own procedures (DOI handbook 516 DM 1; USDA 7 CFR 1b) [E: SC-014, SC-009] | Responsible Official; courts under "substantial deference" [E: SC-012]; IG; Congress | CE determinations, EA/FONSI, EIS/ROD, cooperating-agency decisions, Sec. 112 fee schedules | Choosing the level of review and scope boundaries; managing page and time limits; evaluating applicant-prepared documents; building a reasoned record; deciding when to engage beyond minimums [E: SC-038] |
| **State permit writer** (NPDES, Title V, assumed 404) | State law plus federally delegated or assumed authority | Agency director; EPA oversight; permit appeal boards; courts | Permits, fact sheets, conditions, compliance schedules | Writing conditions that are enforceable and defensible; managing the federal oversight relationship; carrying reversion risk (Florida's 404 authority reverted to the Corps in 2026) [E: SC-021] |
| **County planner** | Police power; state planning and SEPA/CEQA law (state law not verified this session) | Planning commission and elected board (direct political principals); quasi-judicial hearing rules | Comprehensive plans, zoning codes, staff reports, conditional-use permits | Briefing elected bodies; running quasi-judicial hearings; acting as a cooperating agency on federal actions [E: SC-014; SPEED would expand this, SC-010] |
| **Tribal environmental / natural resources director** | Inherent sovereignty; treaties; federal program authorities (TAS, 638/ISDEAA, TFPA); GNA partner since 2018, revenue retention since 2025 [E: SC-030, SC-036] | Tribal council and community; government-to-government relations with federal and state governments | Tribal codes and permits, GNA and co-stewardship agreements, consultation positions | Acting as regulator, rights-holder and partner at once; protecting knowledge and data on Tribal terms. **TN must lead here**; I flag only the structural difference. |
| **NGO policy advocate** | None formal; influence through comment, litigation, coalitions and legislative engagement | Board, members, funders; courts as venue | Comments, notices of intent to sue, coalition letters, model legislation | Strategic comment drafting (would gate standing if SPEED is enacted) [E: SC-010]; choosing venues as NEPA litigation leverage falls [E: SC-012]; using statutes outside NEPA [E: SC-022] |
| **Corporate regulatory affairs manager** | None; obligations as a regulated entity | Executives, board, investors; regulators in several jurisdictions | Permit applications, applicant-prepared EAs/EISs, Sec. 112 fee requests, disclosures (CA SB 253 from 2026-11-10; EU CSRD) [E: SC-027, SC-028] | Managing a portfolio of authorizations; strategy across divergent regimes; regulator relationships; making the business case for engagement |
| **Consultant** | Contract with an agency or sponsor | Client; agency adequacy review; professional ethics | Draft environmental documents, technical reports, comment analyses | Independence and quality under the sponsor-pays model; AI-assisted production [E: SC-009]; translating between agency and applicant |
| **Academic advisor** | Epistemic authority; advisory committees | Peers, institution, advisory bodies | Testimony, science syntheses, peer review, advisory reports | Being an "honest broker"; translating science to decisions courts will defer to; staying relevant when agencies need reasoned explanations more than exhaustive analysis [J] |

### 3.2 What transfers and what does not

**Transfers well** [J, based on the comparison above]:
- Negotiation (SC4)
- Engagement design (SC5, except G2G consultation)
- Record-keeping and integrity discipline (SC8)
- Drafting (SC9)
- Durability judgment (SC7)

These are the portable core. A state permit writer who moves to a consultancy, or a federal NEPA lead who moves to a county, brings them intact.

**Transfers with translation:**
- Legal-procedural fluency (SC1) transfers as a *method* (map the authority; find the procedure version; document the reasoning). It does not transfer as *content*, because each jurisdiction's authorities differ.
- Fiscal craft (SC6) transfers between public actors (appropriations, CRs, fees) but changes in kind for NGOs (grants) and firms (capital budgets).

**Does not transfer without new learning:**
- **The authority basis and the principals.** A federal employee's political principals are distant and insulated by civil service; a county planner's sit on the dais [J].
- **Sovereignty.** Practitioners trained to treat Tribes as "stakeholders" carry a frame that is wrong and harmful [J; TN to validate].
- **Delegated-program constraints.** Working inside a delegated program is a different discipline from working in a federal agency [E: SC-021].

### 3.3 Implication for the model

Most statecraft should be **one competency with structured enactments by actor**. A few competencies should be actor-specific because the deliverable differs in kind (§8, Q1).

v1's five sector notes have no Tribal or local-government column and merge federal, state and local into "Public Agencies" [E: SC-004]. They should be replaced by an **authority-context** record: authority basis, principal, accountability venue, characteristic instruments, transfer frictions.

---

## 4. The legal and policy landscape, October 2026

All 34 instruments, with status, workforce implications, affected v1 codes and sources, are in `policy_landscape_2026.csv`. The patterns:

### 4.1 Six shifts

1. **From rules to procedures (discretion rises).**
   - CEQ removed 40 CFR 1500–1508. The interim rule was effective 2025-04-11 and the final rule took effect 2026-01-08. CEQ said that after EO 14154 "the agency lacks authority to maintain its NEPA implementing regulations" [E: SC-011].
   - Of 108,385 submissions on that rule, about 457 were unique [E: SC-011]. That ratio matters for AI comment analysis (§5).
   - DOI moved most procedures into a handbook that "can be updated more easily than regulations" [E: SC-014].
   - Practitioners warn that guidance-based procedures are "more susceptible to changes in administration" [E: SC-040] and that "Guidance can be changed quickly, raising the risk of mid-review shifts" [E: SC-039].
   - *Workforce:* knowing which procedure, and which version, governs a decision is now a skill in its own right [J].
2. **Deference and remedy recalibrated.**
   - *Seven County* (2025-05-29): "Courts should afford substantial deference"; NEPA is "a purely procedural statute"; a deficient EIS "does not necessarily require vacating" an approval [E: SC-012].
   - The SPEED Act passed the House on 2025-12-18 [E: SC-010]. It would add a 150-day limitations period, remand without vacatur, and standing only for those who filed a "substantive and unique comment". It is pending in the Senate, where S. 3224 differs [E: SC-010].
3. **Speed bought with money and technology.**
   - NEPA §112 (P.L. 119-21, 2025-07-04) lets sponsors pay 125% of document cost for an EA in 180 days or an EIS in one year [E: SC-013]. It does not speed ESA or §106 [E: SC-039]. For context, the median EIS took 2.8 years over 2019–2024 [E: SC-013, citing CEQ].
   - The Presidential Memorandum of 2025-04-15, the CEQ Action Plan (2025-05-30) and data standard v1.2 (2025-08-18) set up federal digital permitting [E: SC-037, SC-009].
   - The ePermit Act passed the House unanimously on 2025-12-09 and has a Senate companion [E: SC-017, SC-015].
4. **Federal substantive scope contracts.**
   - ESA: the "harm" definition was rescinded (effective 2026-09-12; habitat modification alone is no longer take) [E: SC-018]; the blanket 4(d) rule was eliminated and the 4(b)(2) exclusions rule finalized (effective 2026-08-20) [E: SC-019]; section 4 and 7 rules are proposed [E: SC-020].
   - CAA: the endangerment finding is rescinded and vehicle GHG standards repealed. Challenges include one by the Bay Area AQMD [E: SC-024, SC-025].
   - CWA: WOTUS is proposed, with a supplemental proposal and no final rule [E: SC-023].
   - GHGRP: cuts proposed (46 categories; subpart W suspended to RY2034) [E: SC-026].
   - Each change is being litigated [E: SC-022, SC-025]. *Workforce:* federal practice may reverse again; durability judgment (SC7) and state, local and Tribal capacity matter more [J].
5. **Devolution through partnership instruments.**
   - In FY2025 the Forest Service held 540 GNAs: 426 with 39 states, 50 with counties, 45 with Tribes [E: SC-030].
   - The EXPLORE Act lets counties and Tribes retain revenue through FY2028 and created recreation GNAs (first FS agreement January 2026) [E: SC-030, SC-031].
   - Colorado extended state GNA authority to DOI agencies (signed 2026-04-13) [E: SC-034]. A bill would allow 20-year agreements [E: SC-032].
   - Tribal co-stewardship persists in roughly 150 DOI and 121 USFS agreements, but EO 14112 was rescinded and agreements are "not self-funding" [E: SC-035, SC-036].
6. **Disclosure fragments.**
   - The SEC proposed rescinding its climate rule on 2026-05-29 [E: SC-029].
   - California's SB 253 reports are due 2026-11-10; SB 261 is enjoined [E: SC-027].
   - EU Omnibus I narrowed CSRD to companies with more than 1,000 employees and €450m turnover [E: SC-028].

### 4.2 Top five changes since early 2025, with workforce implications

| # | Change | Workforce implication |
|---|---|---|
| 1 | **CEQ regulations removed; agency-specific procedures** (DOI final 2026-02-24; USDA final 2026-04-03; DOT final 2026-09-01; EPA proposed 2026-06-25) [E: SC-011, SC-014, SC-009] | NEPA staff must work to divergent, versioned procedures. Public involvement becomes a judgment call. A single "NEPA regulations" curriculum is obsolete. |
| 2 | ***Seven County* deference, plus the pending SPEED Act** [E: SC-012, SC-010] | The reasoned record becomes the main defense. NGO advocacy shifts upstream and to other venues. Comment craft and comment analysis may gate standing. |
| 3 | **Paid acceleration and digital permitting** (§112 fee; PM, Action Plan, data standard; PermitAI in production; ePermit passed the House) [E: SC-013, SC-037, SC-009, SC-017] | New roles: permitting product owner and data steward. Entry-level drafting and comment triage are automated. ESA and §106 specialists become the critical path. |
| 4 | **Federal substantive rollback, litigated** (ESA harm, 4(d), 4(b)(2); endangerment finding; WOTUS; GHGRP) [E: SC-018, SC-019, SC-024, SC-023, SC-026] | Consultation, wetland and air practice reshapes. States, air districts and NGOs move into litigation and their own programs. Practitioners must work under two possible legal futures. |
| 5 | **Partnership authority expands to counties and Tribes** (GNA revenue retention; recreation GNA; state statutes) [E: SC-030, SC-034] | Agreement design and administration (SC3, SC6, SC9) become core jobs in state forestry, counties and Tribal programs. Federal staff become agreement managers. |

A sixth runner-up: the **fragmentation of corporate disclosure**, which splits the corporate regulatory-affairs role [E: SC-027, SC-028, SC-029].

### 4.3 Does this landscape change what statecraft *is*?

No. It changes the **weights**. Judgment under discretion (SC7), record integrity (SC8), agreement-making (SC3) and fiscal craft (SC6) go up. Rote procedure knowledge (part of SC1) goes down, both because it changes too fast to memorize and because AI retrieves it [J]. This is why the taxonomy should hold durable components in the core and the instruments in a dated layer (P-SC-02).

---

## 5. AI and digital permitting

### 5.1 Real deployments (not pilots on paper)

- **PNNL PermitAI** (funded by DOE Office of Policy and the Permitting Council) [E: SC-009]:
  - SearchNEPA and CommentNEPA are listed as **production**; WriteNEPA and EngageNEPA as production/beta.
  - NEPATEC 3.0 (August 2026) holds 81,347 projects and about 10.2 million pages.
  - PermitTEC v0.1 links 761 NEPA court cases to projects, with each field tagged as LLM-extracted and manually validated, manually corrected, or unreviewed.
  - DraftNEPABench (102 EIS-section tasks across 19 agencies), built with OpenAI, estimated 1–5 hours saved per subsection, up to about 15%.
- **CEQ Action Plan** [E: SC-037, SC-009]:
  - Service delivery standards include "Workflow Automation" (e.g., routine CE review) and "Digital-First Documents" that "deliver structured and readily usable data".
  - Minimum functional requirements include automated project screening and administrative record management.
  - Agencies using AI are pointed to OMB M-25-21.
- **Docket scale:** 371,657 comments on the 2026 Roadless proposal [E: SC-009]; more than 220,000 on WOTUS [E: SC-023]; 108,385 submissions with about 457 unique on CEQ's removal rule [E: SC-011]. At this scale, human-only comment reading is no longer realistic [J].

I could not reach the UK i.AI "Consult" evaluation [unverified: SC-059], so I have no non-US comparator. There is no peer-reviewed evaluation of production comment-analysis accuracy in US environmental review in what I read. **The deployment evidence is real; the evidence on accuracy and legal adequacy is thin** [J].

### 5.2 What changes in the work

| Task | Before | Now / near term | Evidence |
|---|---|---|---|
| First-draft resource sections | Junior analyst | AI draft; human specifies, checks and owns | [E: SC-009] |
| Comment binning and summaries | Junior coder | AI bins; human samples, finds unique substantive comments, writes responses | [E: SC-009, SC-011] |
| CE screening | Specialist checklist | Rules-based screening plus GIS overlays; human decides extraordinary circumstances | [E: SC-037, SC-009] |
| Legislative and regulatory tracking | Analyst | Automated monitoring; human translates changes into operations | [E: SC-004 (v1 V call), SC-038] |
| Record assembly | Clerk and specialist | Structured data and provenance by design; human writes the reasoned explanation | [E: SC-037, SC-012] |

### 5.3 What stays human, and why it is not sentiment

1. **The decision and its reasoned explanation.** A named Responsible Official decides [E: SC-038], and courts defer to the agency's reasoning [E: SC-012]. Deference attaches to an accountable official's reasoning; a tool cannot carry that accountability [J].
2. **Legitimacy.** Whether the right people were heard, and could see their effect, is judged by those people. When participation is optional [E: SC-038], someone must choose to offer it and defend that choice [J].
3. **Relationships.** Government-to-government consultation, cooperating-agency trust and negotiation depend on parties who know each other and remember. v1 coded these H (5.2.4 T1–T3; 6.5.1 T1–T2) [E: SC-004], and nothing I found contradicts that [J].
4. **Judgment where rules have become discretion.** Scope boundaries, extraordinary circumstances, engagement beyond the minimum, instrument choice. These grew in 2025–26 precisely because rules were withdrawn [E: SC-014, SC-039].

### 5.4 Risks the taxonomy should name

- **Losing the comment that matters.** When only about 0.4% of submissions are unique [E: SC-011], a model that merges one unique, substantive comment into a campaign bin can drop the comment that matters legally. If SPEED's standing rule passes, that error would also affect who may sue [E: SC-010; J on consequence]. → SC-C05.
- **Provenance.** Unlabeled AI text in a record invites challenges to the integrity of the record and its reasoning. PermitTEC's three-state provenance tags are a workable pattern [E: SC-009; J]. → SC-C02.
- **Apprenticeship collapse.** All four v1 S calls fall on statecraft entry tasks [E: SC-004]. Those tasks were how juniors absorbed law and agency culture [J]. Redesign entry work as supervised validation, record audits, mock hearings and drafting clinics, and track the risk as a CLD signal (P-SC-06). [S: it would be confirmed if agency NEPA entry-level hiring and consultant junior headcounts fall while senior demand holds; LM to test.]
- **Metric gaming.** Structured process data (dashboards, case events) makes timeliness visible but not legitimacy. Expect pressure to optimize what is measured [S].

---

## 6. Review of v1

Full verdicts (35 rows) are in `v1_assessment.csv`. The main points:

### 6.1 The craft definition and the residual problem

v1 tags 94 of 222 competencies SC-primary (42%): D3 28, D5 28, D6 33, D7 5 [E: SC-004]. Some of these produce no boundary-crossing commitment: 3.3.3 Facilities operations, 3.3.2 Equipment and asset management, 3.1.1 Scheduling, 5.5.1 Visitor information, 5.4.3 Volunteer program management. Statecraft absorbed whatever was neither field nor data work [J].

The CA audit found that the criteria document predicted craft by domain and then treated agreement with the prediction as calibration [E: CA audit §5]. I agree, and add that the definitional phrase "stakeholder engagement" made the residual easy. **Verdict: change** (P-SC-07).

### 6.2 Domain 6

- **6.1.4 NEPA process implementation.** Its job task "in accordance with NEPA regulations" refers to rules that no longer exist [E: SC-011]. Rewrite it around level-of-review selection, limits, applicant-document oversight, discretionary engagement and the record (SC-C02–C04, C06).
- **6.1.3 Permitting procedures** is too coarse. Split it into durable pathway competencies and put permit-program specifics in the instrument layer. A March 2026 v1 permitting review found the same lack of permit-type granularity [J].
- **6.5.x Intergovernmental relations** should be carried but updated for cooperating-agency practice, delegated-program reversion and agreement instruments [E: SC-014, SC-021, SC-030].
- **6.7.2 EJ screening** and the v1 D6 narrative assume EJ becoming "embedded in regulatory frameworks at federal and state levels" [E: SC-005]. That is outdated at the federal level: DOI's procedures dropped EJ references [E: SC-014]. Make it venue-aware and tool-agnostic.
- **6.7.5 Air quality management** sits under Environmental Health & Justice, but air districts run regulatory programs and litigate [E: SC-025]. DB should restructure it.
- **Proficiency text** ("Manages permit applications independently"; "Shapes NEPA policy and practice") cannot be observed. Replace it with anchors.
- **Stability tier:** 39 of 40 D6 competencies are "Transition" [E: SC-004], so the tier does not discriminate.

### 6.3 Domain 5 (engagement)

D5 is the relational core and mostly H [E: SC-004], so carry it. Add SC-C06 for engagement under discretion. 6.4.4 T2 (comment themes) should move from **S to Ac**: the work changes rather than disappears, because substantive comments still require reasoned responses and SPEED would raise their legal stakes [E: SC-009, SC-010].

v1's Task 13 says relational-institutional legitimacy shows "no trajectory toward S or V in any domain" [E: SC-006]. That holds for relational *tasks*, but V calls already sit inside statecraft competencies (6.4.5 T1, 5.5.2 T1/T3, 6.7.2 T1) [E: SC-004]. The claim should be scoped to tasks.

### 6.4 Domain 3

3.1.2 Budget development covers only project budgets. Split it, and add public fiscal and appropriations craft (SC-C10). The UK standards make Finance one of eleven core policy standards [E: SC-042], and 2025 brought new fiscal instruments with direct workforce effects (§112 fees, GNA revenue retention) [E: SC-013, SC-030].

### 6.5 The six reform flags: retire as columns, replace with a dated layer

The flags sit on 129 of 222 competencies (184 instances in the database). The stored counts disagree with the Task 10 record (e.g., digital-permitting 66 vs 39) [E: SC-004, SC-003]. More fundamentally, they encode one moment's federal agenda:

- **"One-federal-decision"** names an executive policy. Its durable content (one document, lead agency, schedules) is now statute: NEPA §107 as amended in 2023, plus FAST-41 [E: SC-010].
- **"S2-S3-boundary"** is a property of the workflow model, not a reform.
- **"Consultation-reform"** lumps sovereign consultation together with ESA process rules.
- **Missing entirely:** judicial review, review scope, jurisdiction scope, substantive standards, delegation, agreements, disclosure and fiscal mechanisms.

**Proposal (P-SC-02).** Three linked parts that do not go stale:
- **Instruments** (`policy_landscape_2026.csv`): dated, sourced, with status.
- **Mechanisms** (`driver_mechanisms.csv`): 16 durable codes, each mapped to the v1 flag it replaces.
- **Sensitivity edges**: task or competency × mechanism, asserted once with evidence.

A competency's current exposure is *computed*: the mechanisms it depends on, joined to instruments whose status changed within a window. New events are appended; nothing on the competency row needs editing. v1 flags are kept as a frozen historical view.

### 6.6 The S1–S6 workflow model

S1–S6 is a project-and-authorization lifecycle centered on NEPA and public lands [E: SC-002]. Symptoms:
- 6.1.5 Enforcement had to be tagged S2 (Environmental Review) [E: SC-003].
- S1 is primary for 111 of 222 competencies [E: SC-004; CA audit §8].
- There is no place for rulemaking, budgeting, compliance assurance, or utility and corporate cycles [J].

I largely agree with the CA's generalized facet, with specific changes (§8, Q2).

---

## 7. Candidate competencies, role signals and anchors

- **`candidate_competencies.csv`, 18 candidates.**
  - Nine are rewrites or substantial transformations of v1 content: C01 authority and pathway mapping, C02 administrative record, C03 level of review, C09 interagency schedule, C10 fiscal craft, C12 regulatory change translation, C14 delegated programs, C15 multi-regime disclosure, C17 litigation and remand resilience.
  - Six are new or emerging: C04 applicant-document oversight, C05 AI supervision for legal defensibility, C06 discretionary engagement design, C08 stewardship agreements, C11 durability judgment, C16 drafting binding instruments.
  - Two are stable but under-specified in v1: C07 negotiation, C18 briefing principals.
  - C13 G2G consultation is a **placeholder for TN**.
- **`role_signals.csv`, 17 signals.** Highlights:
  - NEPA specialist transforming (R01).
  - Junior document writer and entry-level policy analyst: entry path at risk (R02, R14).
  - GNA program manager: a new role (R05).
  - Permitting technology product owner: a new role (R08).
  - Corporate disclosure manager: splitting (R09).
  - Air district counsel: transforming (R12).
  - Third-party neutral: direction unknown, [S] (R16).
- **`statecraft_proficiency_anchors.csv`, 40 anchors** for 10 competencies at four levels. Each names an observable behavior, the evidence of performance, and an assessment method (seeded work samples, BARS-scored simulations, mock record certification, moot defenses, prediction-log calibration, 360 input from counterparts).
- **`ecosystem.csv`, 21 entities.** The most useful integrations:
  - The CEQ data standard: its entities (comment, engagement, case_event, decision_element) can serve as both assessment evidence and demand data.
  - PermitAI benchmarks: an external reference for D6 exposure calls.
  - The Federal Register and CRS: feeds for the instrument layer.
  - The UK standards: a level benchmark.

---

## 8. Answers to CA architecture questions

### Q1. Does Statecraft need actor-specific competencies, or one competency with actor-specific enactments? (DP-7)

**Answer: one competency with structured enactments by default, plus a small set of actor-specific competencies under a stated rule.**

- **Default: enactments.** The portable core (negotiation, engagement design, record integrity, drafting, durability judgment) is performed with the same observable behaviors across actors. What differs is the authority basis, the principals, the accountability venue and the instruments [J, from the §3 comparison]. These differences belong in a **structured enactment record**, not free text, so transfer frictions can be computed. Proposed fields: `actor_type`, `authority_basis`, `principal`, `accountability_venue`, `characteristic_instruments`, `typical_frictions`. The UK standards handle multilevel government the same way, as one standard (2.4) with leveled behaviors, not separate competencies per level of government [E: SC-042].
- **Rule for an exception.** Create an actor-specific competency **only when the defining deliverable differs in kind** (a different legal duty or source of authority), not merely in procedure [J]. Applying the rule gives four exceptions:
  1. **Exercising Tribal sovereignty** (a Tribal government running its own regulatory, consultation and agreement programs). TN must write or approve it.
  2. **The duty-holder side of government-to-government consultation** (SC-C13, federal and state). It is a legal obligation owed to a sovereign, not engagement; it pairs with (1). TN decides whether it is written at all.
  3. **Operating or overseeing delegated and assumed regulatory programs** (SC-C14, state and Tribal). Authority is contingent on federal predicates and can revert [E: SC-021].
  4. **Regulated-entity compliance across divergent regimes** (SC-C15, private). The deliverable is defensible compliance for an entity without authority, across jurisdictions [E: SC-027, SC-028, SC-029].
- **NGO advocacy without authority** passes as an enactment, not a separate competency: it uses SC4, SC5, SC7 and SC9 toward influence rather than decision [J].
- **Evidence strength:** mostly [J]. The test would be IO comparing anchored ratings of the same competency across actors. If behaviors diverge beyond the enactment fields, split.

### Q2. Is the generalized work-function facet adequate, and what replaces the reform flags as dated driver events?

**The facet: adequate with four changes.** I tested the CA draft (Assess & sense → Plan & design → Authorize & regulate → Implement & operate → Monitor & verify → Enforce & assure → Learn & adapt → Engage & communicate) against seven contexts [J]:

| Context | Fit | Gap |
|---|---|---|
| Federal land project | Good | Impact review is inside "Authorize & regulate" but behaves differently (below) |
| State permit program (NPDES, Title V) | Good for issue → monitor → inspect → enforce → renew | Rulemaking (water quality standards, SIP rules) is not permitting |
| County planning | Good | Zoning codes (legislative) vs permits and variances (quasi-judicial) |
| Tribal government | Mostly | "Engage & communicate" must not absorb government-to-government relations |
| Water utility | Partial | No home for rate cases, SRF loans, bonds, capital budgets |
| Air district | Good with a rulemaking function | Litigation and dispute work |
| Corporate compliance | Good if "assure" includes disclosure and assurance | Disclosure is legally consequential output |

**Proposed changes:**
1. **Separate "Review consequences" from "Authorize"**, at least as sub-functions. The 2025–26 reforms hit them differently: §112 accelerates NEPA but "does not streamline" ESA or NHPA [E: SC-039]; Seven County changes review scope, not permit standards [E: SC-012]. Merging them would blind the change-signal layer to which work is actually being accelerated.
2. **Add "Make rules & policy"** (rulemaking, legislation, codes, standards). Administrative law distinguishes rulemaking from adjudication and permitting [J, a well-established APA distinction], and much state, local and air-district work is rulemaking.
3. **Add "Resource & finance"** (budgets, appropriations, rates, fees, grants, retained revenue). Utilities, counties and Tribes run on it, and 2025 created new fiscal instruments [E: SC-013, SC-030].
4. **Treat "Engage & communicate" and "Resolve & defend"** (objections, appeals, hearings, litigation, mediation) **as cross-cutting modes, not stages.** Engagement happens in every stage. Objection and litigation windows sit across review and authorization [E: SC-009 objection rule; SC-012]. Government-to-government relations should be a distinct relationship type within the mode, not "engagement" [J; TN].

Keep S1–S6 as the named "project and authorization lifecycle" profile, as the CA proposes. Add profiles for the regulatory-program cycle, the utility capital-and-compliance cycle, the corporate disclosure cycle and the rulemaking cycle.

**Dated driver events.** These are delivered as seed data:
- `policy_landscape_2026.csv`: 34 instruments with status as of 2026-10 and sources.
- `driver_mechanisms.csv`: 16 mechanisms, each mapped to the v1 flag it replaces.

**Proposed event schema** (aligned with the CA audit §9):
- `event_id`, `instrument_id`
- `event_type`: introduced | passed-chamber | enacted | proposed | interim | final | effective | enjoined | vacated | remanded | rescinded | decided | expired
- `event_date`, `jurisdiction`, `mechanism_ids`
- `direction`: expands | contracts | reshapes
- `status_after`, `source_ids`, `evidence_label`, `recorded_by`, `review_by`

Tasks link to **mechanisms** through durable sensitivity edges; instruments link to mechanisms; events change instrument status. Exposure is computed, so nothing on a competency row goes stale. Seed events: the six v1 flags with their provenance, plus every row of `policy_landscape_2026.csv`.

For non-US and non-federal coverage, the same schema holds state statutes (Colorado HB26-1205), EU directives (Omnibus I) and court decisions (CBD v. Zeldin) [E: SC-034, SC-028, SC-021].

### Q3. What does teachable, observable Statecraft look like at each level?

**A consistent pattern across the 10 anchored competencies** [J; it parallels the UK Level 1–3 progression, SC-042, and adds an assessment method at each level]:

| Level | Observable signature | Typical evidence | Typical assessment |
|---|---|---|---|
| **L1 Foundational** | Applies the right procedure or template to a defined case, and **knows what they don't know** (escalates rather than guesses) | Checklists and logs that pass QA; seeded cases solved | Knowledge tests; seeded-case work samples with answer keys; record QA audits |
| **L2 Intermediate** | **Independently produces work products others accept and act on** (pathway plan, CE/EA determination, engagement plan, budget justification, certified record, negotiated conditions) | Acceptance by the responsible official or partner; low rework; counterpart feedback | Portfolio review against rubrics; standardized simulations scored on BARS; inter-rater file review |
| **L3 Advanced** | **Handles contested, novel or changing situations without restarting**, and defends the reasoning to counsel, courts, principals and partners | Records that survive challenge; instrument changes absorbed; agreements kept through turnover | Structured "what-if" interviews; moot defenses; complex multi-party simulations; 360 input; prediction-log calibration |
| **L4 Expert** | **Builds systems others use** (templates, screening logic, policies, agreements, statutes) and is sought out by other organizations | Adoption metrics; laws or policies enacted; portfolio outcomes | Artifact and adoption review by a peer panel |

Two design notes:
- **Tenure bands** (0–2, 3–5, 6–10, 10+ years) should be descriptive only. The anchors are written so a three-year state permit writer can show L3 on authority mapping [J].
- **Counterpart 360 input and prediction logs** make relationships and judgment observable. Both are personnel data and need CP review for privacy and due process (§11).

---

## 9. Proposals

- **P-SC-01. Adopt the v2 definition, the four-property deliverable test (authorized, legitimate, resourced, durable) and the nine components (SC1–SC9) as the L0 Statecraft vocabulary.** *Change* (v1 definition). Why: it keeps v1's irreducibility logic but makes the deliverable observable and stops the residual drift. [J; SC-001, SC-042]
- **P-SC-02. Retire the six reform-flag columns and the Reform Flag Count. Replace them with a dated policy-instrument registry, driver events and 16 durable mechanisms, with competency and task sensitivity computed.** *Retire + add.* Seed from `policy_landscape_2026.csv` and `driver_mechanisms.csv`; keep v1 flags as a frozen view. [E: SC-003, SC-004, SC-011, SC-012]
- **P-SC-03. Accept the CA work-function facet with four changes:** split Review from Authorize; add Make rules & policy; add Resource & finance; treat Engage and Resolve & defend as cross-cutting modes. Keep S1–S6 as one profile and add four more profiles. *Change.* [J; E: SC-039, SC-012, SC-030]
- **P-SC-04. Represent sector actors through structured authority-context enactment records.** Create actor-specific statecraft competencies only when the deliverable differs in kind; four are proposed (Tribal sovereignty, owned by TN; G2G duty-holder; delegated programs; multi-regime compliance). *Change* (v1 sector notes). [J; E: SC-021, SC-027]
- **P-SC-05. Rewrite D6 skill area 6.1 around durable competencies** (SC-C01 pathway, C02 record, C03 level of review, C04 applicant-document oversight, C17 litigation and remand resilience). Move permit-program and procedure specifics (DOI 516 DM 1, 7 CFR 1b, NPDES, Title V, 404) to the instrument and tools layer. *Change.* [E: SC-011, SC-014, SC-009]
- **P-SC-06. Protect the statecraft apprenticeship.** Add a craft-level "apprenticeship at risk" signal wherever entry tasks are S or V. Pair each automated entry task with a designed developmental substitute: validation sampling, record audits, mock hearings and objection resolution, drafting clinics, cross-actor rotations. Pilot a **statecraft task book** modeled on fire's Position Task Books (LC, FH, SL). *Add.* [E: SC-004, SC-007; J]
- **P-SC-07. Tighten the SC-primary test and re-tag D3 and D5 management items** (expect roughly 15–25 changes). Ask CA whether a "no defining craft / general practice" designation is allowed. *Change.* [J; SC-004]
- **P-SC-08. Adopt the 40 anchors as the pilot proficiency content for statecraft and hand them to IO for validation.** Start with SC-C03 and SC-C05, whose seeded work samples are easiest to score reliably. *Add.* [J]
- **P-SC-09. Add SC-C05 (AI supervision for legal defensibility).** Agree the boundary with DC: DC owns general AI-output validation (7.2.1); SC owns legal adequacy, uniqueness and response sufficiency, and provenance in the record. *Add.* [E: SC-009, SC-010, SC-011]
- **P-SC-10. Add SC-C10 fiscal and appropriations craft and split v1 3.1.2.** *Add + change.* [E: SC-042, SC-030, SC-013]
- **P-SC-11. Reclassify 6.4.4 T2 from S to Ac and scope Task 13's "no trajectory toward S/V" claim to tasks.** *Change.* [E: SC-004, SC-009]
- **P-SC-12. Add the remaining candidates** (C06, C08, C09, C11, C12, C14, C15, C16, C18) and hold C13 for TN. *Add.* [mixed E/J; see CSV]
- **P-SC-13. Use the CEQ data standard and PermitAI benchmarks as external evidence for D6 tasks.** Map anchor evidence to CEQ entities. Use DraftNEPABench and NEPABench task definitions to replace single-analyst exposure calls on review tasks. Use PermitTEC to calibrate litigation-risk anchors (with IA and LM). *Add.* [E: SC-009]
- **P-SC-14. Run a quarterly instrument-layer refresh** from the Federal Register, CRS and Climate Case Chart, with a named steward and `review_by` dates on every sensitivity edge. Without an owner, P-SC-02 decays as fast as v1's flags did (AS). *Add.* [J]

---

## 10. Disagreements and trade-offs

1. **Biggest trade-off: durable competencies vs the instrument fluency employers actually hire and train for.** HR posts "NEPA specialist (516 DM 1)" or "NPDES permit writer", not "authority-pathway mapping". Putting instruments in a dated layer keeps the core from going stale and makes skills portable across actors. The cost is a second layer that must be maintained, and views that rejoin the two for users. I accept the cost, but only if P-SC-14 gets an owner. The alternative is v1's outcome: flags stale within a year [J].
2. **With v1 (6.4.4 T2: S vs Ac).** v1 treats comment analysis as substituted with the entry pathway eliminated. I read the same deployments as compressive augmentation, with the legal stakes rising [E: SC-009, SC-010]. The right task for a junior is validating the AI's work, not reading every comment.
3. **With v1 Task 13 ("relational legitimacy shows no trajectory to S/V").** Right about the relational tasks; wrong if read as protecting whole statecraft competencies or the pipeline [E: SC-004].
4. **With the CA draft facet.** I disagree on two points. "Engage & communicate" should be a cross-cutting mode, not a stage. "Authorize & regulate" merges rulemaking with adjudication and permitting, and buries impact review. Trade-off: two more functions and one more mode make the facet less simple, but without them utilities, air districts and counties do not fit [J].
5. **With DC (ownership of AI validation).** I propose splitting by consequence: DC owns methods, SC owns legal adequacy. If CA prefers one transversal "human-AI practice" competency with enactments, I can accept that, provided the legal-adequacy anchors survive.
6. **With TN.** I have written SC-C13 and the Tribal sector-actor row only as placeholders. TN may decide the G2G duty-holder competency should not be written by a non-Tribal team, or should be framed from the Tribal side. I defer.
7. **Reducing the SC count (P-SC-07) may look like downgrading governance work.** v1 presented "Statecraft plurality (42%)" as a finding about the profession [E: SC-001]. Precision should win, but the Delphi packet should say why the number fell [J].
8. **Precision vs legibility in the driver vocabulary.** Sixteen mechanisms are harder to scan than six flags. Users would see computed views ("competencies affected by changes in the last 12 months"), not the vocabulary [J].

---

## 11. Issues outside my area that affect the vision

- **Political durability of the taxonomy itself (AS, CP, CA).** Competencies on EJ, climate and co-stewardship are federally contested in 2026 [E: SC-014, SC-024, SC-035]. If federal adopters may filter by venue or instrument, content need not be deleted to remain adoptable. I recommend designing that filtering in now [J].
- **Workforce capacity shocks (FH, LM).** I could not verify federal NEPA and regulatory staffing changes. Capacity loss can look like "skill change" in posting data; that is why `driver_mechanisms.csv` includes DM-16 workforce-capacity [S].
- **State variation (SL, DB).** CEQA and other SEPA reforms were not verified this session. State procedures likely diverge as much as federal ones now do [J].
- **Tribal (TN).** SPEED would restrict judicial review of claims involving Tribal trust lands except by the affected Tribe [E: SC-010]. That is a sovereignty issue to assess, not a permitting detail.
- **Personnel data (CP).** The anchors use counterpart 360 input, prediction logs and record audits. These are personnel records; Privacy Act and state equivalents apply [J].
- **Interoperability (IA).** CEQ data standard v1.2 is CC0 with a stable entity model [E: SC-009]. Mapping anchor evidence types to it is cheap and makes EMST legible to permitting systems.
- **Curriculum (LC).** A statecraft task book and simulation library would likely be the highest-leverage training investment for a federal and state MVP [J].
- **Verification debt.** The search budget ran out. Items marked "NOT VERIFIED" in `policy_landscape_2026.csv` should be checked before any Delphi packet cites them.

---

## 12. Open questions for the Chief Taxonomy Architect

1. May a competency carry **no defining craft** (a general professional practice layer), so management items stop inflating Statecraft (P-SC-07)?
2. Where does the **instrument registry** live: as reference data (an L0-like cadence) with events in L5, or entirely in L5? I recommend a registry plus events.
3. Do you accept **Review ≠ Authorize**, plus **Make rules & policy** and **Resource & finance** as functions, with Engage and Resolve & defend as modes (P-SC-03)?
4. For **politically contested content** (EJ, climate, co-stewardship): is it core with venue tags, or modules? I lean core with venue and instrument tags [J].
5. **AI-supervision ownership:** SC-specific (SC-C05), DC (7.2.1), or one transversal competency with enactments?
6. Should **actor-specific competencies** require TN sign-off whenever they touch Tribal governments, even if written from the federal or state duty-holder side? I recommend yes.

---

## 13. Files in this folder (`/home/claude/emst/docs/research/statecraft/`)

| File | Contents |
|---|---|
| `report.md` | This report. Writing was blocked for the subagent; the orchestrator should save this text. |
| `sources.csv` | 54 sources (SC-001–SC-061); 12 marked `unverified` (blocked or not reached) |
| `policy_landscape_2026.csv` | 34 dated instruments: NEPA, permitting technology, ESA, CWA, CAA, disclosure, GNA, forestry, Tribal, state SEPA placeholders, AI governance |
| `driver_mechanisms.csv` | 16 durable driver mechanisms plus the retired S2-S3 flag, each mapped to the v1 flag it replaces and to example instruments (extra file, §6.5, §8 Q2) |
| `v1_assessment.csv` | 35 verdicts on the v1 definition, D3/D5/D6/D7 items, the flags, the stability tier, S1–S6, proficiency text and sector notes |
| `candidate_competencies.csv` | 18 candidate statecraft competencies (SC-C01–C18) |
| `role_signals.csv` | 17 role signals (SC-R01–R17) |
| `statecraft_proficiency_anchors.csv` | 40 anchors: 10 competencies × 4 levels, with evidence and assessment methods |
| `ecosystem.csv` | 21 entities (standards, programs, datasets, credentials, coalitions) and how EMST connects to each |

All CSVs were generated with Python's csv module and validated: headers match the team schemas, controlled vocabularies are respected, every cited source ID resolves to `sources.csv`, and every v1 code cited exists in `data/v1_baseline/competencies.csv`. The build scripts are in the session scratchpad (`/tmp/claude-0/-home-claude/fbbe9940-26ca-5e5a-9a05-1e06b16da4ee/scratchpad/build_*.py`).