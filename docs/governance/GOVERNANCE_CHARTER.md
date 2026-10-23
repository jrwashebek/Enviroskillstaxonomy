# EMST Governance Charter — version 0.9 (for adoption)

- **Work package:** WP-13 · **Author:** A10b (AS, with CM; Tribal gate procedures with TN as gate reviewer) · **Date:** 2026-10-23
- **Status:** **draft for adoption by the project lead**, with a one-year review (`questions_for_project_lead.md` Q8 recommendation). Not yet adopted. Licence: CC BY 4.0 (narrative publication, ADR-0013 §2).
- **Builds:** ADR-0007, ADR-0009, ADR-0012, ADR-0013, ADR-0014, ADR-0015, ADR-0016, ADR-0023, ADR-0024, ADR-0027, ADR-0028; `docs/standard/SPEC.md` §10, §12, §16, §18; AS Phase 2 `governance_charter_draft.md` (v0.1, Articles 1–11), which this version supersedes.
- **Companion documents:** `CONTRIBUTING.md` (change requests), `LICENSING.md`, `module_stewardship_agreement_template.md`, `tribal_gate_procedures.md`, `docs/adoption/COMMITMENT_REGISTER.md`.

> **Provisional status carried from the decisions.** This charter inherits the status of the ADRs it implements:
> - **ADR-0009** is *accepted* for the governance model, federation phasing and cadence, but **needs the project lead** for the host and for constituting any body with external members. Every body below is therefore described as it will work once constituted; Annex A states what exists today.
> - **ADR-0007** is *accepted* for the five vetoes and the content hold, but **needs the project lead** for the Tribal Advisory Council's binding authority and the charter carve-out, and **needs real consultation** for any Tribal-related content. Article 4.5 is an AI-drafted proposal; no Tribal nation has reviewed it.
> - **ADR-0013** is *accepted*, **conditional on the lead's written CC0 dedication** of v1-derived content (Q2).
> - **ADR-0014** is **provisional-pending-verification**; its dates are re-checked at each stage gate.
>
> Every place where a pending answer from the project lead would change the text is marked `<!-- PENDING Qn -->`. Until an answer arrives, the text follows that question's stated **default**.

> **Simulated voices.** The Tribal Nations advisor (TN) and the Workforce Voice panel were played by AI agents in Phases 1–4. Nothing in this charter speaks for any Tribal nation, practitioner or community. Provisions marked *AI-drafted; requires Tribal review* become usable only as set out in `tribal_gate_procedures.md`.

---

## Article 1. Purpose and scope

1.1 The Environmental Management Skills Taxonomy (EMST) is an open, versioned, vendor-neutral standard describing environmental work — tasks, competencies, proficiency indicators, role profiles and variants, crafts, change signals and crosswalks — so that the sector can see how its jobs are changing and people, skills and knowledge can move between federal, state, local, Tribal, NGO, private and academic institutions (charter vision; SPEC §1.1).

1.2 This charter governs the EMST **core**, its **modules**, its **fast layers** (L4 tools, L5 signals and events), its **crosswalks and registers** (L6), its releases, and the bodies that decide them (SPEC §3).

1.3 It does **not** govern the standards EMST maps to (O*NET, SOC, ESCO, OPM classification and qualification standards, NWCG qualifications, the USWFS–USFS federal qualification standards, state class plans, accreditor criteria or credential-body requirements). EMST proposes changes upstream to their owners and never forks them.

1.4 It does not govern Indigenous knowledge, which is a distinct body of environmental expertise held and governed by Indigenous nations and is **out of scope by design** (ADR-0007 §C; SPEC §16.1).

## Article 2. Principles

2.1 **Open by default.** Data, the standard, decisions and their history are public (Article 10; `LICENSING.md`).

2.2 **Evidence-labelled.** Every substantive record carries an E/J/S label, sources and provenance (SPEC §13). Agent output is draft evidence, never validation (`PHASE4_BUILD_PLAN.md` §1 rule 2).

2.3 **Stability for adopters.** Published IDs are permanent and never reused; change follows Article 7 (SPEC §12).

2.4 **Function over institution.** Content describes work, not organization charts; every competency is named by the work performed, uniformly (ADR-0016 §2).

2.5 **Sovereignty and consent.** Tribal nations' authority over their data and knowledge is respected under the CARE Principles; until a Tribal Advisory Council exists and approves, nothing Tribal-related is published (ADR-0007 §D).

2.6 **No personal data, development use only.** The Steward holds no person-level data about workers, applicants, raters, panelists or pilot participants (ADR-0012 I-1). EMST never ranks, scores, screens or selects people; exports carry "not a selection instrument / not a classification basis / not for RIF, adverse action or performance ratings" (ADR-0012 I-2).

2.7 **No single owner.** No organization, including the Steward, holds a majority of votes on any body.

2.8 **Nonpartisan posture.** EMST supplies no essay content and gives no help with political designations (ADR-0016 §6). Applicability of content to a jurisdiction is computed from the instrument registry, not asserted (ADR-0016 §3). <!-- PENDING Q4: federal default views exclude items whose only basis is a rescinded or inactive federal instrument once the lead confirms; until then federal default views show computed applicability with an explanatory note and no exclusions. -->

2.9 **Commitments are records, not adjectives.** No organization is described as committed, a partner, a steward or an adopter in any EMST document without a dated entry in the commitment register (Article 12).

## Article 3. Bodies at a glance

| Body | Role in one line | Constituted when | Decides |
|---|---|---|---|
| **Steward** (host institution) | Operates the programme; holds marks in trust; signs agreements; no editorial veto | Host Agreement signed (target Jan 2028); until then the project lead acts <!-- PENDING Q3 --> | operations, budget, contracts within Advisory Council policy |
| **Editorial Board (EB)** | Decides content and releases | Interim EB named at rc.1 (recommended); default: project lead acts as interim EB <!-- PENDING Q8 --> | content (S, D), lifecycle, protect, MINOR and PATCH releases |
| **Technical Steering Committee (TSC)** | Owns schema, IDs, namespaces, release engineering, crosswalk method, CI | Interim TSC named at rc.1 (recommended); default: DE and IA roles act as interim TSC <!-- PENDING Q8 --> | schema, IDs, namespaces, build, conformance checks, crosswalk method |
| **Advisory Council (AC)** and its **Executive Group** | Sector-actor seats; ratifies MAJOR releases; appoints EB; hears appeals; selects successor host | By gate G1, March 2028 (recommended) <!-- PENDING Q8 --> | ratification, appointments, appeals (final except Tribal category), succession |
| **Tribal Advisory Council (TAC)** | Binding consent over Tribal-related content (proposed) | Only when constituted by Tribal governments and inter-Tribal organizations, after reviewer compensation is funded <!-- PENDING Q1 --> | inclusion, wording and release of Tribal-related content |
| **Workforce Voice Panel (WVP)** | Real practitioners; usefulness veto at G1 | Recruited before the pilot (Q9 funding) <!-- PENDING Q9 --> | G1 usefulness veto; co-signs gate thresholds |
| **Module Stewards** | Partners holding a Module Stewardship Agreement | Not before v2.2 (2029), after a signed agreement and two on-time cycles | content within their module, within core rules |
| **Validation Panels** | SME, Delphi and job-analysis panels under IO protocols | First panels with Stage 1 design partners (2027); Delphi by G1 | pre-registered panel outcomes (retention, level placement) |
| **Sentinel Network** and **Triage Panel** | Paid, stratified practitioners reporting change; quarterly triage | At v2.0; size per funding <!-- PENDING Q9 --> | routing of signals; proposals to the EB |

Terms of reference for each body follow in Article 4. Annex A states what exists on 2026-10-23 and what acts in each body's place until it is constituted.

## Article 4. Terms of reference

Each body's terms of reference use the same headings: purpose; composition; appointment; term; decision rights; quorum and decision rule; appeal path; cadence and records; support; status.

### 4.1 Steward (host institution)

| Heading | Terms |
|---|---|
| **Purpose** | Operate the EMST programme: employ staff, manage funds, run infrastructure, sign agreements, hold the EMST name and marks **in trust** for the Consortium (Art. 11). |
| **Composition** | An institution bound by a five-year Host Agreement (Art. 13). Accountable officers: the centre director and the Managing Editor. Recommended host path: EPIC incubates through December 2027; an open call in Q2 2027 selects a university-based EMST Stewardship Center to operate from January 2028, governed by an independent EMST Consortium (ADR-0009 §8). <!-- PENDING Q3: (a) EPIC incubation, (b) open call, (c) signatory. Default: the project lead is signatory for Stage 1 documents; the host call is drafted but not issued. --> |
| **Appointment** | Selected by the Advisory Council (or, before it exists, the project lead) through the open call criteria in AS `sustainability_model.md` §4. |
| **Term** | Five years, renewable; ≥ 12 months' notice of withdrawal. |
| **Decision rights** | **Decides:** staffing, contracts, budget execution within the annual plan the AC reviews; fee schedules and waivers (published); signature of MOUs, DUAs, design-partner letters and Module Stewardship Agreements after the relevant body approves their terms; the accessibility conformance report signature after Phase 4 (ADR-0027 §4). **Recommends:** the annual plan and budget. **Has no vote or veto** on content, releases or Tribal-related decisions. |
| **Quorum and decision rule** | Institutional decisions follow the host's own delegation of authority; the Host Agreement names who may sign for EMST. |
| **Appeal path** | A body or member who believes a Steward decision breaches this charter (e.g. a fee arrangement that buys content influence) refers it to the AC Executive Group; Host Agreement disputes follow that agreement. |
| **Cadence and records** | Annual plan and budget to the AC; quarterly adopter bulletin; every agreement it signs is entered in the commitment register within 10 business days. |
| **Support** | Maintains the published maintenance floor (~3 FTE, ~$0.62M a year) before cutting anything else (Art. 13.4). |
| **Status (2026-10-23)** | No host. The project lead signs for the project <!-- PENDING Q3 -->. |

### 4.2 Editorial Board (EB)

| Heading | Terms |
|---|---|
| **Purpose** | Decide substantive content changes, lifecycle and protect decisions, and releases, so the core, modules and views read as one system. |
| **Composition** | 7–9 voting members: Managing Editor (chair; votes only to break ties); three craft editors (Field craft, Data craft, Statecraft); a methods editor (job analysis and validation); an interoperability editor; a sector-balance editor (state, local, NGO or private); the **TAC liaison (voting)** once a TAC exists <!-- PENDING Q1 -->; one rotating module representative once any module is stewarded (v2.2+). **Rules:** ≤ 1 member per organization; ≥ 3 sector actors represented; no vendor or consultancy seat (Art. 9.4). |
| **Appointment** | Appointed by the AC from public nominations; the interim EB at rc.1 is named by the project lead <!-- PENDING Q8 -->. |
| **Term** | Two years, staggered; at most two consecutive terms. |
| **Decision rights** | **Decides:** change requests of type S (substantive) and D (deprecate) and their adjudication; editorial status transitions to `published`, `deprecated`, `superseded`, `withdrawn`; lifecycle changes in L1–L4 (ADR-0028 §5); `protect` decisions and any withdrawal of a protected record, after sector consultation (ADR-0015 §3); PATCH and MINOR releases; the dispute-resolution role from the close of Phase 4 (ADR-0009 §6). **Jointly decides** X (structural) changes with the TSC. **Recommends** MAJOR releases to the AC. **Cannot:** decide Tribal-related content (Art. 4.5); override pre-registered Validation Panel outcomes (Art. 4.8); override the Workforce Voice Panel's G1 veto except by the procedure in Art. 4.6. |
| **Quorum and decision rule** | Quorum: two-thirds of voting seats, including members from ≥ 3 sector actors. Rough consensus; if it fails, a two-thirds vote of members present. The chair records objections and how they were addressed. MAJOR recommendation: two-thirds of all voting seats. Recusal under Art. 9. |
| **Appeal path** | A proposer, a body or any 10 community members may appeal an EB decision to the **AC Executive Group** within 30 days, on grounds of process (charter not followed), evidence (decision contradicts the evidence standard) or conflict of interest. The Executive Group's decision is final, except in the Tribal category, which never reaches it (Art. 8). Before the AC exists, appeals go to the project lead <!-- PENDING Q8 -->. |
| **Cadence and records** | At least monthly during build years, quarterly thereafter; decisions and rationale in `docs/decisions/` within 14 days (ADR-0009 §6). |
| **Support** | Managing Editor and editorial staff of the Steward. Members' time compensated where their employer permits; public employees participate under their agency's ethics rules. |
| **Status (2026-10-23)** | Not constituted. The CA resolves disputes through Phase 4; the CA decision log continues. Default after Phase 4: the project lead acts as interim EB <!-- PENDING Q8 -->. |

### 4.3 Technical Steering Committee (TSC)

| Heading | Terms |
|---|---|
| **Purpose** | Keep EMST machine-readable, reproducible and interoperable: schema, ID policy and the ID registry, namespaces, the build and CI, release engineering and signing, crosswalk method, conformance checks. |
| **Composition** | 3–5 members: the Data Steward (DE successor role), the Interoperability / Skills-Intelligence lead (IA successor role), ≥ 1 external maintainer from an adopter, and up to two further members with standards or security expertise. ≤ 1 member per organization outside the Steward's staff. |
| **Appointment** | Appointed by the EB; interim TSC named at rc.1 <!-- PENDING Q8 -->. |
| **Term** | Two years, renewable. |
| **Decision rights** | **Decides:** schema SemVer, field additions (MINOR) and removals (MAJOR, with EB and AC); ID minting rules and namespace registration (`vocab/identifiers.yaml`); CI rules and release engineering; SSSOM method and upstream re-pinning; conformance checks for modules, forks and "EMST-conformant"/"EMST-mapped" claims (SPEC §18); type C (crosswalk) change requests and type E (errata) for data plumbing. **Jointly decides** type X with the EB. **Cannot:** change content meaning; relax Tribal-hold or personal-data CI checks (those checks change only with TAC consent and EB approval respectively). |
| **Quorum and decision rule** | Quorum: a majority including ≥ 1 member not employed by the Steward. Lazy consensus over 7 days for routine technical changes; otherwise majority vote. |
| **Appeal path** | To the EB; then to the AC Executive Group. |
| **Cadence and records** | Fortnightly during build; monthly thereafter; decisions as ADRs or change records. |
| **Support** | Steward staff; CI infrastructure; credentials held by two people at two organizations (Art. 13.3). |
| **Status (2026-10-23)** | Not constituted. DE and IA act as interim TSC (steward field in `vocab/identifiers.yaml`) <!-- PENDING Q8 -->. |

### 4.4 Advisory Council (AC) and Executive Group

| Heading | Terms |
|---|---|
| **Purpose** | Give the sector actors whose legitimacy EMST borrows a formal voice; ratify what affects adopters most; appoint and hold the EB to account; hear appeals; keep EMST alive if the host fails. |
| **Composition** | 17–21 voting seats: federal (2), state (2), local (1), Tribal (2, appointed by the TAC; **seats stay empty until a TAC exists**) <!-- PENDING Q1 -->, NGO (2), private employers (2), academia and accreditors (2), professional societies (2), workforce voice and employee organizations (2, one nominated by the WVP), labor-market data and research (1), plus up to two at-large seats for balance. **Funders sit as non-voting observers.** Vendors and consultancies hold at most two seats in total (Art. 9.4). |
| **Executive Group** | Chair, vice-chair and three members elected by the AC from at least three sector actors. |
| **Appointment** | First AC appointed by the project lead (or Steward) from public nominations by gate G1 (recommended) <!-- PENDING Q8 -->; thereafter seats are filled by nomination from the constituency each seat represents, confirmed by the AC. |
| **Term** | Three years, staggered; at most two consecutive terms. |
| **Decision rights** | **Decides:** ratification of MAJOR releases (two-thirds of votes cast); EB appointments; appeals (Executive Group; final except Tribal category); successor host selection (Art. 13.2); the Steward's annual plan review; charter amendments (with EB; Art. 14); review of the fee-for-service portfolio. **Advises** on priorities, modules, waves and the annual plan. **Cannot:** decide content directly; override the TAC. |
| **Quorum and decision rule** | Quorum: a majority of filled voting seats, with ≥ 4 seat categories present. Ratification and amendments: two-thirds of votes cast. Appointments: simple majority. Executive Group: quorum 3 of 5 non-recused members; majority decision; members who took part in the decision under appeal are recused. |
| **Appeal path** | Executive Group decisions on appeals are final. A challenge to an AC decision itself on conflict-of-interest grounds goes to the Executive Group with the conflicted members recused; on Tribal-related matters the TAC's position governs (Art. 8.4). |
| **Cadence and records** | At least twice a year; Executive Group as needed (appeals heard within 45 days of filing). Minutes public, with confidential personnel matters redacted. |
| **Support** | Travel and honoraria for members whose organizations cannot pay; Steward staff support. |
| **Status (2026-10-23)** | Not constituted. Until it exists, its appeal and ratification functions rest with the project lead <!-- PENDING Q8 -->. |

### 4.5 Tribal Advisory Council (TAC)

> **AI-drafted; requires Tribal review.** This section was drafted by an AI agent from TN's Phase 2 protocol (`docs/research/tribal-sovereignty/tribal_engagement_protocol.md` §5). It does not speak for any Tribal nation. The TAC, once constituted, writes its own terms of reference and may discard any part of this section. The project lead's decision on Q1 determines whether the authority below is offered.

| Heading | Terms |
|---|---|
| **Purpose** | Hold authority over Tribal-related content so that EMST respects Tribal sovereignty and control of Tribal data and knowledge (charter; ADR-0007). |
| **Composition** | Proposed 7–11 members **nominated by Tribal governments and inter-Tribal organizations, never selected by the project**; regional spread including Alaska; a separate Native Hawaiian participation track; members choose their own chair. The TAC decides its own composition. |
| **Appointment** | Through a selection process designed with the first inter-Tribal reviewers **before** any wider outreach (protocol §4). No outreach of any kind until reviewer compensation is funded and the project lead has decided Q1 (`tribal_gate_procedures.md` §2). <!-- PENDING Q1 --> |
| **Term** | Proposed two years, staggered; the TAC decides. |
| **Decision rights (proposed, per the Q1 recommendation)** | **Binding consent authority** over the inclusion, wording and release of Tribal-related content (ADR-0007 §D list: the 7.1.1 successor TN-C07; every L2 ethical-lens definition and tag; TN-C01–TN-C13; SC-C13; Tribal role variants; Tribal-flagged change signals; TN's role signals; the Tribal engagement protocol and the Indigenous data governance policy; Tribal-related protect decisions; any use of Tribal workforce data; the Tribal-related content of each release). **Default where it does not decide: withhold.** It may require removal, restriction or labels (e.g. Local Contexts Notices or Labels) at any time and may withdraw an approval. **Advises** on everything else; the project answers in writing. It appoints the EB's voting TAC liaison and the AC's Tribal seats. Consent is also required to amend Art. 4.5, Art. 8.4 or any Tribal-related provision (Art. 14.2). <!-- PENDING Q1: (a) binding consent authority; (b) no override by the CA, EB or AC; (c) compensation budgeted before first contact. Default if unanswered: the ADR-0007 §D content hold stays in force indefinitely; no Tribal outreach; TN-C01–C13, SC-C13, the v1 5.3.2, 6.5.1 and 7.1.1 successors, Tribal variants and Tribal signals remain internal drafts excluded from every release. --> |
| **Quorum and decision rule** | **Set by the TAC.** Draft suggestion only: consensus-seeking with recorded minority views. Until the TAC adopts its rules, no TAC decision can be taken and the default (withhold) applies. |
| **Appeal path** | **None against a TAC decision on Tribal-related content.** The CA (through Phase 4), the EB and the AC cannot override it (proposed charter carve-out, ADR-0007 §10). The project may ask the TAC once, in writing, to reconsider, without a deadline; if the TAC declines, the content stays withheld. The rest of a release proceeds without the withheld content. |
| **Cadence and records** | On Tribal time: draft minimum windows of 90–120 days for any matter needing a Tribal government decision, 30–45 days for staff-level review, extensions on request (protocol §10). The TAC approves its own records; deliberations are confidential unless it decides otherwise. |
| **Support** | Funded before first contact: honoraria at professional rates, travel, and a 0.5 FTE Tribal Liaison who reports to the TAC (AS sustainability model). Payment goes to the party the Tribe directs and never depends on agreement or transfers ownership. <!-- PENDING Q9: if compensation cannot be funded, the gate stays closed and no outreach occurs. --> |
| **Status (2026-10-23)** | **Does not exist. No outreach has occurred or is authorized.** The content hold applies (ADR-0007 §D; SPEC §16.1). |

### 4.6 Workforce Voice Panel (WVP)

| Heading | Terms |
|---|---|
| **Purpose** | Keep the people EMST serves at the centre: test the theory of change against real careers, judge usefulness, hold the expansion gates, guard against misuse (CM `practitioner_panel_design.md` §1; ADR-0009 §2). |
| **Composition** | 28 standing members plus up to 8 rotating subsector seats, in strata: S-A cross-actor movers (5); S-B federal and state staff in transition (5); S-C early-career (4); S-D conservation corps alumni (3); S-E seasonal and wildland fire workforce (3); S-F employee organizations (3, organizational representatives); S-G HR, training and curriculum intermediaries (3); S-H Tribal natural-resource professionals (2 reserved, **filled only through the Tribal gate; they stay empty until then**) <!-- PENDING Q1 -->. Cross-cutting targets: ≤ 40% from forestry, fire and public lands; ≥ 30% from water, air, waste, energy, environmental health, ESG or climate; ≥ 40% rural or duty-station-bound; ≥ 5 without a four-year degree; ≥ 2 veterans. |
| **Appointment** | Open call plus targeted outreach; stratified selection by a committee (CM, AS successor role, one external evaluator); stratum targets filled first; ties broken by lottery. |
| **Term** | Two years, staggered; members may serve two terms. |
| **Decision rights** | **Binding usefulness veto at G1:** if any stratum's M-06 pass rate is below threshold, G1 cannot close. The CA (Phase 4) or the EB (thereafter) may override only by (i) a written decision-log entry answering the panel's objection point by point, (ii) a second panel vote, and, if that fails, (iii) escalation to the AC Executive Group, whose decision is final (ADR-0009 §2) — before the AC exists, to the project lead <!-- PENDING Q8 -->. **Co-signs** the numeric thresholds in `docs/adoption/gate_metrics_G1_G2.csv` before the pilot starts. **Ratifies** G1 and G2 (M-28). **Files practitioner objections** (any five members or any one stratum); the EB answers in writing within 15 working days. Holds reserved, separately reported Delphi seats. |
| **Quorum and decision rule** | Gate votes need a quorum in **every** stratum that has members (≥ 2 present per stratum) and a **majority within every stratum**; strata are never averaged away. S-H is excluded from quorum while empty. |
| **Appeal path** | The panel's veto is the appeal against a gate decision; the override procedure above is the only route around it. Individual members may raise conduct concerns with the external evaluator, who reports to the AC Executive Group. |
| **Cadence and records** | Quarterly plenary (virtual); monthly asynchronous rounds; one in-person convening a year outside fire season; usability sessions at every release candidate. Minutes in `docs/decisions/` without names unless members choose to be named. |
| **Support** | Paid for time (annual stipend plus per-session payments); costs covered; public employees participate as their ethics rules allow, with non-cash alternatives where pay is barred. Career-history interviews and diary studies run under an IRB with a research partner; identifiable records are held by that partner, never by the Steward (ADR-0012 I-1 §3–4). |
| **Status (2026-10-23)** | Not recruited. The Phase 2–4 panel was simulated and its outputs carry labels for the real panel to confirm, correct or reject. Recruitment depends on Q9 funding <!-- PENDING Q9 -->. |

### 4.7 Module Stewards

| Heading | Terms |
|---|---|
| **Purpose** | Let subsector bodies with their own mandate and staff maintain depth in their module while the core stays coherent (ADR-0009 §3; ADR-0018). |
| **Phasing** | **v2.0–v2.1 (2027–2028): modules are editorial sections**, authored centrally and paid for by the core, each with a named **module advisory partner** listed as *candidate* until a commitment record exists. **v2.2+ (2029 onward):** a section becomes a **stewarded module** only after its partner signs a Module Stewardship Agreement (`module_stewardship_agreement_template.md`) **and** completes two review cycles on time. |
| **Composition** | One organization (or a named joint stewardship of two) per module, with a named contact and an SME pool. |
| **Appointment** | MSA approved by the EB (terms) and the TSC (conformance), signed by the Steward; entered in the commitment register. |
| **Term** | MSA term three years, renewable; orphan clause below. |
| **Decision rights** | **Decides** content changes inside its module namespace within core rules: core schema and vocabularies, three-module and home-module rules, the evidence standard, no redefinition of core IDs, no separate licence (SPEC §18.2). **Proposes** core changes through the ordinary process. **Cannot** decide Tribal-related content in its module (TAC), release timing (EB) or schema (TSC). |
| **Quorum and decision rule** | Per the steward's own governance, documented in the MSA, with recorded reviewer identities (pseudonymous in the repo). |
| **Appeal path** | Contributors may appeal a module steward decision to the EB; then to the AC Executive Group. A steward may appeal a TSC conformance finding to the EB. |
| **Orphan clause** | A module returns to the core if its steward misses two review cycles or withdraws. |
| **Cadence and records** | ≥ 1 review cycle a year on the core cadence; annual conformance check by the TSC. |
| **Status (2026-10-23)** | **No module is stewarded and none can be before v2.2.** No subsector body has agreed to steward a module [E: ADR-0009 context; AS-042, AS-056]. <!-- PENDING Q8: default — no module is described as stewarded. --> |

### 4.8 Validation Panels

| Heading | Terms |
|---|---|
| **Purpose** | Provide the human evidence the release criteria require: SME content review, the pre-registered modified Delphi, job-analysis surveys, reliability studies and cognitive interviews (ADR-0024). |
| **Composition** | Per IO's protocols (WP-11): Delphi panels of 15–25 members; ≤ 30% from any sector actor; ≥ 50% independent panelists where recruited through adopters; over-recruitment of thinned public field and statecraft strata and recently separated incumbents; active field practitioners in proportion to the field workforce; WVP reserved seats reported separately. Tribal participants only through Tribal research approval, on Tribal time — **none while the Tribal gate is closed** <!-- PENDING Q1 -->. |
| **Appointment** | Convened by the methods editor (IO successor role) with the Steward; recruitment channels may include adopters, subject to the composition rules. |
| **Term** | Per study. |
| **Decision rights** | **Decides** the pre-registered outcome of its study (e.g. Delphi retention at the exact Lawshe critical value, ≥ 75% essential or useful, level placement ≥ 70% modal with IQR ≤ 1). The EB **may not** record a `validationStatus` of `panel-retained` or `job-analysis-confirmed` that the panel's pre-registered result does not support; it may re-run a study under a new pre-registration. Panels **advise** on wording; the EB decides wording. |
| **Quorum and decision rule** | Per pre-registration (OSF Registries, mirrored as a timestamped repo release); hard stop after round 3. |
| **Appeal path** | Methodological challenges go to the methods editor, then to the EB; a challenge that the pre-registration was not followed goes to the AC Executive Group. Panelists' individual ratings are never overruled. |
| **Cadence and records** | Results enter the repo **only as aggregates**; rater IDs are pseudonymous and the identity map is held by the research partner outside the repo (ADR-0012 I-1 §3). |
| **Support** | Compensated; participation costs removed for thinned strata (ADR-0024 §7). <!-- PENDING Q9: default — panels are smaller and reported as such. --> |
| **Status (2026-10-23)** | Protocols being designed in WP-11. **No panel has run.** No agent rating may be reported as SME agreement, Delphi retention or job-analysis confirmation (`PHASE4_BUILD_PLAN.md` §1 rule 2). |

### 4.9 Sentinel Network and Triage Panel

| Heading | Terms |
|---|---|
| **Purpose** | Detect how environmental work is changing between releases and feed the annual Signals Review (ADR-0028 §5; P-AS-12). |
| **Composition** | **Sentinels:** 60–90 practitioners, stratified and compensated (each sector actor 8–30%; each craft ≥ 25%; early-career ≥ 25%); channels for fire and fire intelligence, permitting, water, air and environmental health, disclosure and markets, state and local, workforce pipeline; a Tribal channel only as the TAC governs it. **Triage Panel:** foresight lead (chair), skills-intelligence lead, a rotating craft lead, a module expert, a sentinel representative, the mobility lead; the TAC for Tribal-flagged signals. |
| **Appointment** | Sentinels recruited by the Steward through societies, corps and design-partner agencies; triage members appointed by the EB. |
| **Term** | Sentinels: annual cycle, renewable. Triage members: two years. |
| **Decision rights** | Sentinels **report** signals; they decide nothing about content. The Triage Panel **routes** signals and **proposes** lifecycle changes to the EB; machine-coded signals stay `machine-coded` until a human validates them; Tribal-flagged (`careFlag`/`tribalPrograms`) signals are quarantined for the TAC. |
| **Quorum and decision rule** | Triage: quorum of four including the chair; majority routing decision; 10% of signals double-coded each quarter (κ ≥ 0.6). |
| **Appeal path** | A sentinel or proposer may ask the EB to review a triage disposition. |
| **Cadence and records** | Continuous intake; event-triggered review within 10 working days; monthly digest; quarterly triage; annual Signals Review before the April MINOR. Signals describe work, not workers; `personalData = false` on every record. |
| **Support** | Honoraria; coding support. <!-- PENDING Q9: default — the network starts at the year-five floor of 30 sentinels. --> |
| **Status (2026-10-23)** | Not recruited. |

## Article 5. Decision rights matrix

D = decides · J = decides jointly · R = recommends or proposes · C = consulted · V = may veto or withhold · — = no role. "Lead (interim)" shows who acts until a body is constituted (Annex A).

| Decision | EB | TSC | AC | TAC | WVP | Module Steward | Validation Panel | Steward | Lead (interim) |
|---|---|---|---|---|---|---|---|---|---|
| Errata (E) | D | D (data plumbing) | — | V if Tribal-related | — | D in module | — | — | CA through Phase 4 |
| Crosswalk change (C) | C | D | — | V if Tribal-related | — | R | — | — | DE/IA |
| Substantive content (S) | D | C | — | V if Tribal-related | C | D in module (v2.2+) | R (evidence) | — | CA → lead |
| Deprecation (D) | D | C | C if protected | V if Tribal-related | — | R | — | — | CA → lead |
| Structural (X): schema, L0 meaning | J | J | ratifies if MAJOR | V if Tribal-related | — | C | — | — | CA |
| Tribal-related (T) | — | — | — | **D (consent; default withhold)** <!-- PENDING Q1 --> | — | — | — | — | **hold: nothing published** |
| Lifecycle change L1–L4 | D | — | — | V if Tribal-related | — | D in module | validates `established` (IO) | — | CA → lead |
| Protect / withdraw protected | D after sector consultation | — | C | D if Tribal-related | C | R | — | — | CA → lead |
| PATCH release | D | J (engineering) | — | V on Tribal content | — | — | — | signs artifacts | CA |
| MINOR release (April) | D | J | C | V on Tribal content | C (usability) | C | — | publishes | CA → lead |
| MAJOR release | R | R | **D (2/3)** | V on Tribal content | C | C | — | publishes | lead |
| Gate G1 / G2 | R | — | C | — (Tribal participation is never a target) | **V (G1 usefulness); ratifies** | — | — | R | CA (Phase 4) → EB |
| Module stewardship agreement | D (terms) | D (conformance) | C | V on Tribal terms | — | party | — | signs | lead |
| Commitments (MOUs, DUAs, letters) | C | — | C (policy) | V if Tribal | — | — | — | signs; registers | **lead signs** <!-- PENDING Q3 --> |
| Fee schedule and services portfolio | C | — | reviews | — | — | — | — | D (published) | lead |
| Host selection and succession | — | — | **D** | C | — | — | — | — | lead <!-- PENDING Q3 --> |
| Charter amendment | J (2/3) | C | J (2/3) | V on Tribal provisions | C | C | — | C | lead adopts v0.9 <!-- PENDING Q8 --> |
| EB appointments | — | — | D | appoints TAC liaison | nominates (AC seat) | — | — | — | lead names interim EB |

## Article 6. Change and contribution process (summary)

6.1 Anyone may propose a change. Change requests are pull requests (or issues that become pull requests) typed **E** errata, **C** crosswalk, **S** substantive, **D** deprecate, **X** structural, **T** Tribal-related (routed to the TAC first; while the gate is closed, T requests are held unopened beyond triage) (ADR-0009 §4). Bots may open pull requests; humans merge.

6.2 **S and X require two independent sources including at least one demand signal** (posting, PD, plan requirement, staffing plan) or SME panel data.

6.3 Service levels: triage ≤ 30 days; candidate comment 30 days (minor) or 60 days (major or X); adjudication ≤ 30 days after comment closes, each comment marked Noted / Accepted / Accepted with modification / Deferred / Rejected.

6.4 The full procedure, templates and the contributor's certificate (DCO) are in `CONTRIBUTING.md`.

## Article 7. Versioning and release cadence

| Release | Contents | Cadence | Notice |
|---|---|---|---|
| PATCH | errata; crosswalk re-pins (O*NET, ESCO, OPM register); fast-layer snapshots | as needed; crosswalks ≥ quarterly | release notes |
| MINOR | additive content; new role variants; deprecations with successors; lifecycle promotions | **once a year in April** (after the sentinel cycle, before federal budget formulation) | candidate ≥ 60 days before |
| MAJOR | breaking change: withdrawal without successor; change to the meaning of an L0 term or the level scale; schema removal | **≤ once every 3 years**, announced ≥ 12 months ahead | migration guide and crosswalk |

7.1 The prior MAJOR is supported for ≥ 24 months after its successor ships; assessment users may pin a version until their next job-analysis refresh (ADR-0009 §5).

7.2 Every release ships a "does this affect me?" notice, a machine-readable delta, a DOI, signed artifacts, SHA256SUMS, an SBOM, an accessibility conformance report (WCAG 2.2 AA) and the third-party licence register (SPEC §12.5; ADR-0027 §4; `LICENSING.md`).

7.3 Counts in release notes and documents are generated by CI, never typed (ADR-0021).

## Article 8. Disputes and appeals

8.1 **Through Phase 4,** the CA resolves disputes (team charter; ADR-0009 §6). From the close of Phase 4, the EB decides disputes, with appeal to the AC Executive Group, whose decision is final (except 8.4). Until the EB and AC are constituted, the project lead acts for both <!-- PENDING Q8 -->.

8.2 **Appeal paths by body:**

| Decision appealed | First appeal | Final appeal | Time limits |
|---|---|---|---|
| Triage rejection of a change request | Managing Editor (re-triage) | EB | file within 30 days; answer within 30 days |
| EB content, lifecycle or release decision | — | AC Executive Group | file within 30 days; heard within 45 days |
| TSC technical or conformance decision | EB | AC Executive Group | 30 / 45 days |
| Module Steward decision | EB | AC Executive Group | 30 / 45 days |
| Validation Panel methods | Methods editor → EB | AC Executive Group (pre-registration breach only) | 30 / 45 days |
| Triage Panel signal disposition | EB | — | 30 days |
| Gate decision (G1/G2) | WVP veto and override procedure (Art. 4.6) | AC Executive Group (after a failed second panel vote) | per gate calendar |
| Steward decision breaching the charter | AC Executive Group | — | 45 days |
| Conflict-of-interest finding | AC Executive Group (conflicted members recused) | — | 45 days |
| **TAC decision on Tribal-related content** | **None; one written request to reconsider, no deadline** | — | on Tribal time |

8.3 Grounds for appeal: the charter or a pre-registered procedure was not followed; the decision contradicts the evidence standard; a decision-maker had an undisclosed conflict; or new evidence not available at the time. Appeals are public, except personnel matters.

8.4 **Tribal carve-out (proposed; AI-drafted; requires Tribal review).** For Tribal-related content, no body's dispute-resolution authority overrides the TAC, and the default is withhold (ADR-0007 §10). <!-- PENDING Q1(b): charter carve-out. Default if unanswered: the content hold stays in force indefinitely, which has the same practical effect (nothing Tribal-related is published). -->

## Article 9. Conflicts of interest and the fee-for-service firewall

9.1 Every member of every body files an annual disclosure: employment, funding, consulting, vendor relationships and roles in organizations whose standards EMST crosswalks.

9.2 Members recuse from decisions in which they or their organization would gain directly (e.g. a vendor's mapping, a client's role profile, a society's credential crosswalk).

9.3 **Funders have no vote** on any body; every funding agreement includes an editorial-independence clause.

9.4 Vendors and consultancies hold at most two AC seats in total and no EB seat.

9.5 **Firewall.** Staff delivering paid services do not decide change requests arising from that engagement. Paid work never buys content changes; any content change arising from paid work goes through Article 6 like any other request.

9.6 Pilot organizations that sell competing workforce products are excluded from the pilot cohort (`docs/adoption/stage1a_ngo_pilot_design.md` §4).

9.7 Breaches go to the AC Executive Group; remedies range from recusal to removal.

## Article 10. Licensing

10.1 **CC0 1.0** for EMST-authored data and standard text; **CC BY 4.0** for narrative publications; **Apache-2.0** for code; third-party material keeps its own terms and stays out of CC0 files; Tribal-contributed content lives in its own namespace under the contributor's chosen licence (ADR-0013). Details and the path map: `LICENSING.md`.

10.2 The v1-derived text enters the CC0 data files only after the project lead's written CC0 dedication. <!-- PENDING Q2. Default: rc.1 ships with v1-derived text excluded from the CC0 data files (IDs, structure and crosswalks only); v1 wording stays in legacy/ under its current terms. -->

## Article 11. Name, marks and conformance

11.1 "EMST" and its marks are held by the Steward **in trust** for the Consortium and pass to any successor (Art. 13).

11.2 Anyone may say they "use" or "map to" EMST with a release ID.

11.3 "EMST-mapped" (an adopter artifact whose items carry EMST IDs and release) and "EMST-conformant" (a dataset or tool meeting SPEC §18.1) claims require a published conformance check by the TSC. Fees, where charged, are public and waived for small NGOs, Tribal nations and organizations, and public agencies below a size threshold.

11.4 Modified versions may not be called EMST.

11.5 An adopter using EMST content in selection must cite the release and use tier and must rely on its own job analysis (SPEC §18.3).

## Article 12. Commitments and the commitment register

12.1 Every commitment made to or by EMST — adopter, design partner, pilot organization, module advisory partner, funder, host, data provider, co-publisher — is recorded in the commitment register (`data/v2/registers/commitments.csv`; schema in `docs/adoption/COMMITMENT_REGISTER.md`) with its rung, artifact, dates, signatories and a **year-five owner** (P-AS-15; ADR-0009 §9).

12.2 **No organization may be described as committed, a partner, a pilot member, an adopter, a steward, a funder or a co-publisher** in any EMST document, view, kit or communication unless the register holds a dated entry with status `signed` or `active` supporting that description. Otherwise the organization is described as a *candidate* or *prospect*, or not named. The register is the only source of committed status (`PHASE4_BUILD_PLAN.md` §6).

12.3 Signatories: the Steward once a Host Agreement exists; until then the project lead signs Stage 1 documents <!-- PENDING Q3: or EPIC, if it confirms incubation and the lead so decides. --> Agencies and organizations sign for themselves; agents never sign or imply a signature.

12.4 Tribal nations and Tribal organizations are never entered as prospects, never listed as having been asked, and never counted toward any target (protocol §8; CM M-25).

12.5 The register feeds CM metrics M-10 (partner commitment) and M-29 (stewardship funding horizon); the Steward reviews it quarterly and publishes a summary generated from it.

## Article 13. Succession and continuity (the anti-ASC clause)

13.1 **Host Agreement:** five-year renewable term; ≥ 12 months' notice of withdrawal; obligation to transfer records, funds held for EMST, domains, accounts and marks to a successor.

13.2 **Successors:** the AC selects a successor from a standing list of ≥ 2 pre-qualified alternates, reviewed annually, including a fiscal sponsor or open-standards foundation.

13.3 **Continuity by design:** the public repository mirrored in ≥ 2 places; an archival deposit and DOI per release; a reproducible build and runbooks; credentials held by two people at two organizations.

13.4 **Maintenance floor:** about 3 FTE and $0.62M a year (Managing Editor 1.0, Data Steward 1.0, Partnerships 0.5, Tribal Liaison 0.5; quarterly crosswalk refresh; an annual release; TAC support; repository, mirrors and DOIs). If revenue falls short, cuts follow the degradation ladder with **6 months' notice** to adopters: pause new modules and role profiles; targeted panels only; biennial MINOR (crosswalk patches stay quarterly); virtual convenings; then the floor. **Below the floor the AC triggers succession, not silent decline** (ADR-0009 §7). <!-- PENDING Q9: funding of the floor and of compensation lines. -->

13.5 **Five-year public review** of the charter, the host and the funding mix.

## Article 14. Adoption, amendment and review

14.1 This charter takes effect as version 0.9 when the project lead adopts it, and is reviewed after one year <!-- PENDING Q8 -->. Until adoption, it guides Phase 4 work as a draft and the CA's decisions govern.

14.2 Amendments after adoption require a two-thirds vote of the EB **and** a two-thirds vote of the AC after a 60-day public comment period. Amendments to Art. 2.5, Art. 4.5, Art. 8.4 or any other Tribal-related provision also require TAC consent; while no TAC exists, those provisions may be made **more** protective but not less.

14.3 The ADRs govern where they and this charter disagree, until the charter is corrected by a change record (SPEC preamble).

---

## Annex A. What exists on 2026-10-23, and who acts in each body's place

| Body | Exists? | Acting in its place | Becomes real when | Pending |
|---|---|---|---|---|
| Steward | No | Project lead (signatory) | Host Agreement signed (target Jan 2028) | Q3 |
| Editorial Board | No | CA through Phase 4; then the project lead as interim EB | Lead names an interim EB at rc.1 | Q8 |
| TSC | No | DE and IA roles | Lead names an interim TSC at rc.1 | Q8 |
| Advisory Council | No | Project lead (ratification, appeals) | Constituted by G1 (Mar 2028) | Q8 |
| Tribal Advisory Council | **No; no outreach** | **Nobody.** The content hold applies; nothing Tribal-related is published | Tribal governments and inter-Tribal organizations constitute it, after compensation is funded | Q1, Q9 |
| Workforce Voice Panel | No (simulated in Phases 2–4) | Nobody may claim its voice; CM's thresholds stand as proposals until co-signed | Recruited before the pilot starts (Mar 2027) | Q9 |
| Module Stewards | No | EB with candidate advisory partners (named only as candidates) | v2.2+, after an MSA and two on-time cycles | Q8 |
| Validation Panels | No | Nobody; agent ratings stay `draft`, evidence label S | First panels with design partners in 2027 | Q9 |
| Sentinel Network | No | Nobody | At v2.0; floor of 30 if unfunded | Q9 |

## Annex B. Index of PENDING markers in this document

| Question | Where | Text follows the default |
|---|---|---|
| Q1 TAC authority, carve-out, compensation | Art. 3, 4.2, 4.4, 4.5, 4.6, 4.8, 5, 8.4 | hold indefinitely; no outreach |
| Q2 CC0 dedication of v1-derived text | Art. 10.2 | v1 text excluded from CC0 files |
| Q3 Host and signatory | Art. 3, 4.1, 5, 12.3, Annex A | project lead signs; host call drafted, not issued |
| Q4 Federal default views | Art. 2.8 | computed applicability, no exclusions |
| Q8 Constituting bodies at rc.1 | Art. 3, 4.2–4.4, 4.6, 4.7, 5, 8.1, 14.1, Annex A | lead acts as interim EB; CA log continues; no module stewarded |
| Q9 Funding the floor and compensation | Art. 3, 4.5, 4.6, 4.8, 4.9, 13.4, Annex A | degradation ladder; 30 sentinels; smaller panels; no Tribal outreach |
