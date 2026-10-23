# Stage 1a — NGO Pilot Design (v1.0 for Phase 4)

- **Work package:** WP-13 · **Author:** A10b (AS, with CM for metrics and gates) · **Date:** 2026-10-23 · **Licence:** CC BY 4.0
- **Supersedes:** AS Phase 2 `docs/research/adoption-stewardship/ngo_pilot_design.md` (draft), updated to the ADRs and corrected facts.
- **Builds:** ADR-0014 (rollout; **provisional-pending-verification** — dates re-checked at each stage gate), ADR-0006 (corridors COR-1…COR-3), ADR-0012 (no personal data), ADR-0023 (theory of change, gates), ADR-0024 (use tiers; describe/develop only), ADR-0027 (v2.0 product, claims hygiene), ADR-0007 (Tribal hold); `gate_metrics_G1_G2.csv`; `pilot_mou_template.md`.
- **Project lead decisions applied (2026-10-23, `docs/decisions/PROJECT_LEAD_DECISIONS.md`):** Q1 accepted (TAC binding consent authority; the Tribal gate nevertheless stays closed until compensation is funded and a TAC exists); Q5 accepted (Stage 1a and Stage 1b run in parallel, Stage 1b co-producing artifacts from 2027); Q7 (v1 figures only as methodology history; this design cites none).
- **Pending answers that change this text:** Q3 (signatory), Q4 (federal default views), Q6 (theory of change wording), Q9 (funding). Each place is marked.

> **No organization named in this document has committed to the pilot.** Names are recruitment channels or illustrative candidates. An organization becomes a pilot member only when a signed MOU is entered in the commitment register (charter Art. 12).

---

## 1. What the pilot is for

The pilot is the first test of the operating theory of change under real conditions, not a demo: *blends made visible in gate instruments, plus reduced frictions on demand-backed pathways, increase cross-actor movement and knowledge retention* (ADR-0023 §1) <!-- PENDING Q6: internal wording; external pilot materials quote the charter sentence only ("if those blends are visible and portable, mobility follows") until the lead adopts the restated version -->. It runs the v2.0 **Role Change & Development Planner** and kits with NGO programme and training leads (pilot user U1), whose job "contains the state training officer's job, with different role variants" (ADR-0027 §1).

It must answer five questions:

| # | Question | Measured by |
|---|---|---|
| 1 | **Value.** Does the tool help NGO programme and training leads do something they needed to do? | M-06, M-07 |
| 2 | **Embedding.** Do EMST IDs get into real gate artifacts (postings, JDs, IDPs, training plans, grant reports) within six months? | M-08 |
| 3 | **Portability.** Do corridors that start in NGO roles end in recognizable state and federal role variants that shadow users accept? | M-01, M-02, shadow-user review |
| 4 | **Coverage.** Which roles and competencies does the cohort need that EMST lacks? | "request a role" log → backlog |
| 5 | **Adoption economics.** What support does an organization need to keep using EMST after the stipend ends? | AS-G1a–d |

**Use is describe/develop only.** Nothing in the pilot ranks, screens, selects or removes anyone; selection-grade content does not exist in v2.0 (ADR-0024 §1; SPEC §19.1).

## 2. Corridors

The pilot uses the three P1 corridors fixed in ADR-0006. Every corridor ends in a state or federal role variant, so the pilot can say something about federal and state rollout (CM assumption A10).

| Corridor | Roles (mvp_role_set) | NGO entry points | State and federal destination variants | Why now |
|---|---|---|---|---|
| **COR-1** corps and field entry → technician → monitoring/data → geospatial | R01–R05 | corps crew member, crew lead, individual placement; NGO monitoring technician | state parks, forestry or fish-and-wildlife technician; federal biological science technician (0404) and forestry technician (0462); monitoring technician; geospatial analyst | largest entry pathway; AmeriCorps terminations of ~$400M were largely reinstated in plaintiff jurisdictions, but the Sep 11 2026 settlement covers **FY2026 only** and litigation is stayed to Feb 1 2027 [E: V1-05], so corps supply is fragile and portable competency records matter |
| **COR-2** fire operations → fuels and prescribed fire → fire intelligence | R06–R08 | NGO burn crew, prescribed-fire training exchange participant, fire-adapted-community coordinator | state fire or forestry fuels staff; USWFS or USFS fuels and fire-intelligence positions | **USWFS–USFS aligned federal qualification standards take effect Jan 2027; NWCG is not a party** to that alignment and updated PMS 310-1 on Jan 23 2026 [E: V3-13]; EMST links to these qualification systems and never competes with them |
| **COR-3** restoration and land stewardship → environmental review, permitting, compliance → programme management | R09–R13 | land trust stewardship or monitoring staff; watershed council project manager; community air or water monitoring lead | state water-quality, permitting or compliance staff; federal 0401 and 0028 variants | permitting and compliance capacity is moving to states; Pennsylvania counts federal experience as equivalent and reports 1,350 hires with federal experience by Aug 2026 [E: SL-031, SL-080] |

**Pre-registration (ADR-0023 §1).** Before kickoff, CM pre-registers 10–15 pathways across the three corridors (each with origin variant, destination variant, comparison units and the friction records expected), the failure condition (logic model §5: no documented artifact chain on any pathway **and** M-06 below threshold after 12 months ⇒ pathway features stop at the pilot; EMST continues as a role-change and training resource), and the G1 thresholds co-signed by the Workforce Voice Panel. Pre-registration is mirrored as a timestamped repository release.

## 3. Cohort

**Size:** 12 organizations (range 10–14). Enough for strata to show in the "every stratum" tests; supportable by one coordinator [J].

**Geography:** two or three states where state design partners are sought (ADR-0014 §1), plus two national or multi-state organizations, so corridors end in real state classes that SL can crosswalk [J].

| Slot | Organization type | Count | Recruitment channel (candidate; none contacted) | Notes |
|---|---|---|---|---|
| A | Conservation corps — one state-run, one nonprofit, one individual-placement programme | 3 | The Corps Network (represents 140 member organizations engaging 22,000+ young people a year [E: V3-05]) as **candidate anchor partner** | The Resource Assistants Program page does not show 2025–26 activity or scale; check before citing RAP as a live pathway [E: V3-05 note] |
| B | Land trusts — one accredited mid-size, one small or rural | 2 | Land Trust Alliance (candidate channel) [J] | easement monitoring, stewardship, transactions |
| C | Watershed council or river organization | 2 | River Network; state watershed council networks (candidate channels) [J] | restoration project management, monitoring, grant reporting |
| D | Prescribed-fire or fire-adapted-communities NGO | 1 | prescribed-fire training exchange and learning-network partners (candidate channel) [J] | COR-2 entry |
| E | Community environmental health or environmental-justice organization | 1 | regional networks (candidate channel) [J] | community monitoring; permitting participation from the community side |
| F | Tribal-serving NGO | **0** | **none: the Tribal outreach gate is closed** (`docs/governance/tribal_gate_procedures.md`) | Q1 is accepted, but the slot stays at 0 until compensation is funded and a TAC exists, and then only by invitation through the TAC's process; never a quota (M-25). <!-- DECIDED Q1 (2026-10-23, PROJECT_LEAD_DECISIONS.md): TAC binding consent authority accepted; the content hold continues until a TAC exists --> <!-- PENDING Q9 --> |
| G | Statewide intermediary (e.g. state association of conservation districts or land trust coalition) | 1 | national associations (candidate channel) [J] | tests whether an intermediary can carry EMST to members |
| H | Data-heavy conservation science or restoration NGO | 1 | practitioner networks (candidate channel) [J] | tests Data craft and human-AI practice content |
| — | Reserve (fills from B, C or G if F stays empty) | 1 | — | keeps the cohort at 12 |

**Shadow users (not cohort members).** Two or three state HR or training staff and one or two federal classification or training staff review NGO-produced artifacts and corridor endpoints. They give the pilot its state and federal validity check. They are drawn from the agencies co-producing artifacts in the parallel Stage 1b design-partner track (`stage1b_design_partner_packages.md`), and their reviews are recorded under those agencies' design-partner letters. <!-- DECIDED Q5 (2026-10-23, PROJECT_LEAD_DECISIONS.md): parallel tracks accepted; Stage 1b co-produces artifacts from 2027 --> Federal shadow-user feedback is collected with Paperwork Reduction Act-aware design (no identical questions to ten or more members of the public without clearance; CP).

## 4. Selection

A three-person panel scores each applicant 1–5 per criterion: the pilot coordinator (AS successor role), the product lead (CP successor role) and **one member of the real Workforce Voice Panel** (not a simulated voice). <!-- PENDING Q9: the real panel must be recruited and paid first; if it is not, an external evaluator takes the third seat and the departure is recorded. -->

| # | Criterion | Weight | Evidence asked for |
|---|---|---|---|
| 1 | **A real artifact in the next six months** (hire, reorganization, season plan, grant report, training redesign) where EMST could be used | 25% | named artifact and date |
| 2 | **Corridor fit**: roles on COR-1, -2 or -3, placing people toward state or federal roles | 20% | placement or partnership examples (aggregate, no names) |
| 3 | **Named lead with time**: about 0.1 FTE for 10 months (role, not person, recorded in the register) | 15% | executive director's letter |
| 4 | **Willingness to share de-identified artifacts** under the MOU and to take part in research sessions | 15% | signed intent |
| 5 | **Cohort balance**: size, rurality, type, state; small organizations favoured | 15% | cohort-level balancing |
| 6 | **Reach**: an intermediary or network role that can spread use | 10% | membership or network |

**Exclusions:** organizations that sell competing workforce products (conflict of interest; charter Art. 9.6); any organization that would need to share identifiable personnel records to take part; Tribal governments (not NGOs; governed by the Tribal gate, not this pilot).

## 5. What pilot organizations do: use cases

Each organization picks **at least two** use cases; at least one must produce a gate artifact (UC2, UC3 or UC4).

| ID | Use case | v2.0 dependency (ADR-0027 §1) | Output | Metrics |
|---|---|---|---|---|
| UC1 | **How is this role changing?** Review task-level change for one or two roles, with uncertainty, tier and "assessment pending" shown; decide what to train, keep or redesign | View 1 Role Change | short role-change note | M-06, M-07 |
| UC2 | **Rewrite a posting or job description with EMST IDs**; a human adopts or edits the draft | PD/JD skeleton export (v2.0; full builder in v2.1) | live posting or JD citing EMST IDs and release | **M-08** |
| UC3 | **Corps member or seasonal transition portfolio**: member and supervisor map season experience to competencies and levels; gap view against a state or federal destination | View 2 Gap check (**local-first**: ratings stay in a file on the member's device) | portfolio or IDP **owned by the member**; optional Open Badges | M-08, M-09 |
| UC4 | **Season training plan or curriculum**: map the plan; find gaps against corridor destinations | kits and data files (works before the explorer) | revised training plan | M-08 |
| UC5 | **Grant proposal or funder report**: describe workforce outcomes in EMST terms | data files | proposal or report section | AS-G1b |
| UC6 | **AI-readiness review of team tasks**: which tasks AI may augment or compress; plan human-AI practice training and protect formation tasks | View 1; View 4 What's coming (exploratory) | team note | M-06 |

**Fallback if the product slips:** UC2, UC4 and UC5 run on data files and kits alone; the pilot start (Mar 2027) holds even if the explorer lands late (ADR-0014 consequences). View 3 Pathways is shown only as **exploratory**; no pathway is labelled "recommended" (ADR-0023 §5).

## 6. Support model

| Component | What | Who |
|---|---|---|
| Pilot coordinator | 1.0 FTE for 12 months; single point of contact; keeps the commitment register current | Steward (AS successor role) |
| Kickoff | 1.5-day regional workshop; travel paid for small organizations | coordinator, product lead, CM |
| Monthly cohort calls | 60 minutes; peer show-and-tell; release changes | coordinator |
| Weekly office hours | drop-in help | coordinator + rotating expert |
| Research sessions | moderated usability rounds at weeks 1–8 and 9–20; think-aloud on persona tasks | product lead, CM; IRB-reviewed where results are published |
| Peer pairs | each organization paired with one of a different slot type | coordinator |
| Midpoint workshop | month 6; contribution-story check (logic model step 4) | CM, coordinator |
| "Request a role" path | requests enter the backlog with status shown | product lead, EB |
| Misuse channel | reports of ranking, screening or removal use go to the Workforce Voice Panel channel and the Steward; any incident pauses expansion (M-11) | Steward, WVP |
| Stipend | tiered payment for staff time (§10) | Steward |

## 7. Data and privacy (summary; full terms in `pilot_mou_template.md` Schedule B)

1. **No personal data reaches the Steward** (ADR-0012 I-1). The default exchange is organization-level artifacts with names and identifiers removed (postings, JDs, training plans, grant-report sections).
2. **Gap checks and portfolios stay local.** Ratings live in a client-side file the member or organization holds; nothing about an individual is sent to EMST (ADR-0012 tiers 1–2).
3. **Research with people** (usability sessions, diary studies, career-history interviews) runs under IRB review with informed consent. Any person-level research records are held by an **IRB-governed research partner, never by the Steward**; EMST receives only aggregates, with cells below n = 5 suppressed (ADR-0012 I-1 §3–4).
4. **Development use only.** Pilot outputs may not be used to rank, select or remove staff; any such use is a misuse incident (M-11).
5. **Tribal data and knowledge are excluded.** Artifacts are screened at intake for site locations, cultural-resource information and anything Tribal-confidential; such material is returned or destroyed, not stored (ADR-0007 V2).
6. **No third-party AI processing** of shared artifacts unless the organization opts in in writing.
7. **Withdrawal** at any time; withdrawn artifacts deleted from working sets within 30 days; published aggregates remain.
8. **Retention** three years, then deletion unless re-consented.

## 8. Timeline

Dates follow ADR-0014 and are re-checked at each stage gate.

| Period | Activity | Depends on |
|---|---|---|
| Nov 2026 – Jan 2027 | Pilot funding secured; WVP recruited; open call (4 weeks); selection; anchor-partner MOU offered | Q9 funding <!-- PENDING Q9 -->; Q3 signatory <!-- PENDING Q3 --> |
| Feb 2027 | MOUs signed and registered; baseline (artifacts, roles, posting language; aggregate HR baselines from partners); pre-registration released | `2.0.0-rc.1` data available (SPEC §19.1) |
| Mar 2027 | Kickoff; onboarding | — |
| Apr – May 2027 (weeks 1–8) | UC4/UC5 on data files; research round 1 on rc.1 views | — |
| Jun – Aug 2027 (weeks 9–20) | UC1–UC3; research round 2; first artifacts | explorer views (WP-12) |
| Sep 2027 | Midpoint workshop; contribution story v1 | — |
| Sep – Dec 2027 | Embedding: second artifacts; repeat use; shadow-user reviews | Stage 1b design-partner letters signed and registered <!-- DECIDED Q5 (2026-10-23, PROJECT_LEAD_DECISIONS.md): parallel tracks accepted; Stage 1b co-produces artifacts from 2027 --> |
| Jan – Feb 2028 | Close-out; evidence pack; adoption-economics interviews | — |
| **Mar 2028** | **Gate G1 decision** (EB, or CA/lead if the EB is not constituted), with the WVP's binding usefulness veto | `gate_metrics_G1_G2.csv`; charter Art. 4.6 |

## 9. Success, gate and stop rules

- **Gate G1** uses the definitions in `gate_metrics_G1_G2.csv` and `gate_metrics_G1_G2.md` verbatim; this design does not restate thresholds, to avoid two versions.
- **Stop or redesign triggers:** any misuse incident (M-11); M-06 fails in any stratum after one redesign round; fewer than three organizations have produced a gate artifact by month 6 (M-08 trajectory); the anchor partner withdraws; a data incident involving personal or Tribal-confidential information.
- A stop means redesign, not abandonment: kits and data stay useful to design partners. Negative findings are published (pre-registered evaluation).

## 10. Budget (pilot-specific; [J] planning estimates, not quotes)

| Line | Low | High | Notes |
|---|---|---|---|
| Stipends (12 organizations, tiered $8k–$20k; small organizations at the top tier) | $96k | $240k | pass-through; no indirect |
| Pilot coordinator (1.0 FTE, 12 months, loaded) | $130k | $185k | |
| Convenings and travel support | $40k | $90k | |
| External evaluation (contribution analysis, reviewer) | $30k | $80k | |
| Accessible and translated materials (Spanish at minimum where needed) | $5k | $15k | |
| Contingency (10%) | $30k | $61k | |
| **Total** | **≈ $331k** | **≈ $671k** | **planning figure ≈ $0.5M** |

The Phase 2 line for Tribal-serving participation ($10k–$30k) is removed while the Tribal gate is closed (Q1 accepted; compensation not yet funded) <!-- DECIDED Q1 (2026-10-23, PROJECT_LEAD_DECISIONS.md): TAC binding consent authority accepted; the content hold continues until a TAC exists --> <!-- PENDING Q9 -->. WVP compensation is budgeted in the evaluation and governance lines of the sustainability model, not here.

**Funding sources** are candidates only; V3 found active environment programmes at Moore, Walton and Doris Duke and AI programmes at Bezos Earth Fund, Google.org and Schmidt Sciences, but **none runs a programme dedicated to environmental workforce skills** [E: V3-10]. Pilot funders will be asked to accept EMST-described workforce outcomes in grantee reporting (the first grant-condition lever).

## 11. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Corps funding disruption after the FY2026 settlement period and the Feb 1 2027 end of the litigation stay [E: V1-05] | Medium | recruit one state-run corps; UC3 portfolios are member-owned and survive programme loss |
| Product slips | Medium | UC2/UC4/UC5 on kits and data files; shift research rounds |
| NGO needs pull the product away from federal and state needs | Medium | corridors end in state and federal variants; shadow-user reviews |
| Small organizations lack capacity | High | tiered stipends; peer pairs; office hours; two-use-case minimum |
| Sensitive data shared by mistake (site locations, personnel details) | Low–Medium | intake checklist; return-or-destroy rule; no third-party AI by default |
| Pilot read as endorsement of a product | Medium | pre-registered evaluation; publish negative findings; no organization described as a "partner" without a register entry |
| Framing risk in federal shadow reviews (DEI/EJ-labelled content) | Medium | uniform function-based naming and computed applicability (ADR-0016) <!-- PENDING Q4 --> |
