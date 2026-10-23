# Strategic Foresight Report: Building EMST v2 for Futures, Not Only the Present

**Role:** Futurist / Strategic Foresight Lead (FS) · **Date:** 2026-10-23 · **Phase:** 2 (research) · **For:** Chief Taxonomy Architect (CA) and team

**Labels:**
- **[E]** evidence from a source I read (IDs resolve to `sources.csv`)
- **[J]** expert judgment (basis stated)
- **[S]** speculation (what would confirm or refute it)

**Files in this folder**

| File | Contents |
|---|---|
| `drivers.csv` | 38 STEEP+V drivers |
| `weak_signals.csv` | 44 dated signals |
| `scenarios.md` | v1 assessment; new scenario set; wind-tunnel; Futures Wheel; backcasting; signposts; stress-test method |
| `role_signals.csv` | 27 role signals |
| `candidate_competencies.csv` | 18 candidates |
| `horizon_scanning_protocol.md` | Cadence, intake, coding, triage, release flow, sentinel design, facilitator guide |
| `v1_assessment.csv` | 20 verdicts |
| `ecosystem.csv` | 23 entities |
| `sources.csv` | 60 sources |
| `scenario_stress_test.py` + `scenario_stress_test_v1.csv` | Heuristic stress test of all 222 v1 competencies |
| `scripts/build_*.py` | Reproducible generators for every CSV (run with `python3 -I`) |

---

## 1. Summary of findings

### 1.1 Money and capacity have decoupled, so v1's main scenario axis is mis-specified

- Congress enacted FY2026 Interior–Environment funding at $42.56 bn. That is −1.9% year on year, and about $15.7 bn above the President's request. [E: FS-019]
- Over the same period:
  - EPA fell to 12,849 staff (−24%). [E: FS-003]
  - USFS lost 5,325 net (−13%), and NRCS about −24%. [E: FS-042]
  - Interior lost about 10,000 staff. [E: FS-020]
- The operative uncertainty is **public stewardship capacity**: people, authority, coordination and entry pipelines across federal, state, Tribal and local actors. It is not "investment".

### 1.2 Knowledge loss is a double squeeze, at both ends of the ladder

- **At the top:** departing EPA staff had a median 30.3 years of service. Those remaining have 10.8. [E: FS-003]
- **At the bottom:**
  - Conservation postings fell 29.4% year on year (March–September 2025). Paid internships fell 43.8% and AmeriCorps postings 42%. [E: FS-026]
  - $400 m of AmeriCorps cuts hit conservation corps. [E: FS-046]
- **In the middle,** AI is compressing the entry analytical tasks that v1 had already flagged for career-ladder destruction (CLD). [E: FS-055, FS-008]
- Fieldcraft and statecraft are losing their apprenticeship substrate from both sides at once. [J]

### 1.3 AI is being trained on environmental work now, but its reliability and legitimacy in high-stakes decisions are unsettled

- In June 2026 an AI-data vendor was paying experts about $1,150–1,450 per task to build training environments for environmental agents. Applicants needed 3+ years at an agency or major consultancy. [E: FS-038]
- Reasons for doubt:
  - Enterprise agentic projects are failure-prone. An analyst forecast, cited second-hand, has over 40% cancelled by 2027. [E: FS-054]
  - Earth-observation (EO) foundation models degrade off-distribution: 80-class accuracy fell to about 42–48% in held-out regions. [E: FS-012]
  - No court has yet ruled on an AI-assisted environmental record. [J: none found; search budget limited]
- This uncertainty is the second scenario axis.

### 1.4 Devolution has moved from rhetoric to budget structure

- The USFS FY27 budget shifts some management to states, Tribes and permittees under "state-based leadership models". [E: FS-039]
- Tribal nations are asserting governmental roles. In the Roadless record, 19 of 38 Tribal submitters sought authority beyond consultation. [E: FS-040]
- Co-stewardship is slowing for lack of staff. [E: FS-020]
- Mobility across sector actors, the charter's theory of change, is becoming the operating model by necessity. [J]

### 1.5 Public environmental functions are moving to refugia and platforms

- NOAA's billion-dollar disaster database now runs at Climate Central. [E: FS-037]
- Space-based fire detection is philanthropy-led. FireSat became operational in July 2026, with early-adopter data from Q4 2026. [E: FS-011]
- Carbon registries are pairing with dMRV platforms. [E: FS-043]
- Agencies increasingly need "intelligent customer" competencies: procurement, data rights, model audit. v1 barely covers these. [J]

### 1.6 New scenario set

The axes are capacity (rebuilt & coordinated vs thin & fragmented) × AI (trusted & assured vs brittle & contested):
- **SC1 Assured Augmentation**
- **SC2 Human Premium**
- **SC3 Platform Stewardship**
- **SC4 Patchwork Retreat**

v1's augmentation/substitution choice becomes a strategy to wind-tunnel. Only **augmentation-for-formation** fails in no scenario. [J; `scenarios.md` §6] It combines:
- AI that frees senior time for mentorship
- a protected learning substrate
- cross-actor rotations
- ground truth treated as infrastructure

### 1.7 Eight no-regret moves for federal and state workforce strategy, 2026–2029

1. **NR-1** Protect an entry cohort, and redesign entry work for AI.
2. **NR-2** Run a sprint to capture tacit knowledge.
3. **NR-3** Make AI validation and assurance cross-cutting.
4. **NR-4** Treat ground truth as infrastructure.
5. **NR-5** Build skills-based mobility channels.
6. **NR-6** Build intelligent-customer capacity.
7. **NR-7** Fund agreement craft alongside devolution.
8. **NR-8** Start horizon scanning at v2.0.

A further seven moves are held until named triggers fire. [J; `scenarios.md` §8]

### 1.8 The taxonomy needs an architecture for emergence

- Lifecycle states: watch → proposed → emerging → established → declining → withdrawn.
- Evidence thresholds and review-by dates for each state.
- Scenario-conditioned impact assessments.
- A **protect** overlay, so a fall in public demand is never read as licence to let a safety- or trust-critical capability lapse.
- Emerging content informs training and planning, never selection, until it is established.

[J; aligns with and extends CA audit §11]

### 1.9 A heuristic stress test of v1 shows where it is fragile

- Of 222 competencies: 74 robust, 109 contingent, 39 fragile. 59 get the protect flag.
- Fragility concentrates in two places:
  - field operations and public-family field science
  - CLD-flagged entry work in communication and policy
- Nine scenario-critical gaps become candidates FS-C02 to FS-C14.

[J heuristic]

---

## 2. Scope, method and limits

### Scope

- Drivers 2026–2040
- Weak signals
- v1 scenario assessment and a new scenario set
- Backcasting to no-regret and contingent moves
- Roles that don't yet exist
- An architecture for emergence
- A recurring horizon-scanning system

Labour-market measurement and critique of AI-exposure indices belong to LM. I reference them and do not duplicate them.

### Methods, and why each was chosen

The full table is in `scenarios.md` §1.

| Method | Why |
|---|---|
| STEEP+V drivers | So values are not dropped: legitimacy, sovereignty, speed versus precaution |
| Dated weak signals | Postings lag change by 2–5 years |
| Intuitive-logics 2×2 | Usable with sector actors |
| Wind-tunnelling | Tests strategies instead of assuming them |
| Futures Wheel | Traces consequences of AI-drafted reviews |
| Three Horizons; causal layered analysis | Facilitation |
| Backcasting | Works back from the charter's 2035 vision |

### Sources

- About 37 targeted searches and about 45 deep reads, preferring primary and recent sources: CRS, GAO, NIFC, CEQ, OPM-based analyses, agency plans, court and legislative records, and law-firm alerts for current regulatory status.
- v1 documents, read from `legacy/v1/docs/`.
- `sources.csv` records why each source was chosen and its status. For example:
  - Verra dMRV terms of reference (2022): **outdated**.
  - 2025 FireSat news: **superseded** by July 2026 operations.
  - Carbon-market sizing: **unverified** (paywalled; lead paragraph only).

### Limits

1. **Search budget.** The team's shared web-search budget ran out partway through. After that I fetched only URLs returned by earlier searches. Evidence is therefore thinner than it should be on:
   - eDNA program scale
   - state climate-policy budgets (for example, California cap-and-invest)
   - ECOS and state agency capacity
   - Good Neighbor Authority volumes
   - current Pathways and entry-hiring authorities
2. **One blocked source.** A CPR article (January 2026) on USWFS funding was blocked by a permission prompt and not read. GovExec and CWSF covered the same facts. [E: FS-006, FS-049]
3. **Projects tool.** It was unavailable. Until the coordinator exported the v1 docs, I worked from the prompt that generated the v1 scenarios, retrieved from past conversations. All assessments here use the exported document. [E: FS-051]
4. **Thin sector evidence.** Evidence specific to the environmental sector on AI adoption outcomes is thin. Most AI-in-review evidence describes pilots and tools, not measured workforce effects. This is a finding, not a failure.
5. **Tribal content.** It draws only on published Tribal records (FS-040) and GAO findings (FS-020). It does not speak for Tribal nations. A Tribal channel or Tribal content needs TN's protocol and real participation.

---

## 3. Drivers (STEEP+V): what matters most

Full list: `drivers.csv`. The ten drivers below matter most for the federal/state first audience.

| Driver | Direction / uncertainty | Why it matters for competencies |
|---|---|---|
| D-P01 Federal contraction | Down; possible stabilization | Capacity loss concentrated in experts and entry cohorts. [E: FS-003, FS-042] |
| D-S02 Entry-pathway collapse | Down | The field-craft apprenticeship substrate is breaking. [E: FS-026, FS-046] |
| D-S01 Tenure cliff | Predetermined | Expert-level tacit knowledge is leaving now. [E: FS-003, FS-029] |
| D-T01/T02 Generative and agentic AI | Up; adoption and legality uncertain | Compresses S2/S3 entry tasks. Value moves to specification, validation and sign-off. [E: FS-008, FS-038] |
| D-T03 EO foundation models | Up | Mapping becomes cheap. Labels, field plots and regional validation become the binding constraints. [E: FS-012] |
| D-T04 Continuous fire detection | Up | 24/7 fire-intelligence roles across federal, state, utility and Tribal programs. [E: FS-011, FS-053] |
| D-P02 NEPA narrowing | Up; Senate uncertain | SPEED Act (passed the House 18 Dec 2025): 150-day statute of limitations; remand without vacatur. Scoping judgment and record quality become the competence. [E: FS-001] |
| D-P04 Devolution | Up | States and partners need federal-equivalent competencies without federal training pipelines. [E: FS-039, FS-004] |
| D-P08 Congressional counterweight | Stabilizing | "Maintain staffing levels" directives and a proposed RIF moratorium are the main lever toward SC1/SC2. [E: FS-019, FS-049, FS-048] |
| D-N01 Fire regime | Up; predetermined | 2026 year to date: 9.0 m acres, 145% of the 10-year average. Fire demand rises in every scenario. [E: FS-034] |

### Second-tier drivers that still matter

- **D-E01 Disclosure regimes.** Scope is narrowing while standardization rises:
  - Omnibus I limits CSRD to companies with more than 1,000 employees and more than €450 m turnover, with 61% fewer datapoints. (FS-013)
  - California SB 253 first reports are due 10 Nov 2026. (FS-015)
- **D-E03 Nature metrics are fragile.** Assessor variability alone can produce England's required 10% BNG uplift. (FS-047)
- **D-V04 Public data versus privatized intelligence.**
- **D-T06 Drones.** The FAA Part 108 rule is the gate. (FS-022)

### The most dangerous loop for the vision

Four drivers interact. [J]
1. Federal contraction (D-P01) cuts entry hiring.
2. AI drafting (D-T01) removes the entry tasks that remain.
3. Retirements (D-S01) remove the mentors.
4. Devolution (D-P04) moves the work to employers with no pipeline.

AI alone does not break this loop. Three moves do: protecting the learning substrate (NR-1), capturing tacit knowledge (NR-2) and building mobility channels (NR-5).

---

## 4. Weak signals: what is already visible at the edge

Full list: `weak_signals.csv` (44 signals, December 2024 to October 2026). They fall into six clusters:

1. **AI enters the environmental-review value chain from the private side first.**
   - Consulting tools that sort public comments (WS-13)
   - PermitAI and NEPATEC (WS-05, WS-11)
   - AI-agent training on agency workflows (WS-29)
   - An AI-readiness credential (WS-26)
2. **Data and intelligence functions move outside government.**
   - FireSat (WS-02, WS-31)
   - Climate Central's database (WS-08)
   - dMRV registries (WS-01)
3. **Capacity contracts, and Congress pushes back.**
   - Contraction: WS-10, WS-21, WS-15, WS-33
   - Countermoves: WS-19, WS-39
4. **Devolution and sovereignty:** WS-06, WS-27, WS-03, WS-20, WS-35.
5. **Regulatory oscillation and divergence between states:** WS-09, WS-17, WS-23, WS-16, WS-37, WS-38.
6. **Measurement credibility.**
   - BNG assessor variability (WS-28)
   - EO model degradation (WS-41)
   - Vendor capability claims not yet verified (WS-31)

**A missing signal.** I found no court decision on an AI-assisted environmental record. [J] This is the key signpost for Axis 2. Its absence keeps both SC1 and SC2 open.

---

## 5. Scenarios (summary; full treatment in `scenarios.md`)

### Verdict on v1: change

- **Carry forward:** career ladders, reproduction regimes, refugia, the ~2028 decision window, and the sentinel-bias insight.
- **Replace the axes.** They are mis-specified and federal-centric, and they treat a strategy as an uncertainty.
- **Add:** an "AI disappoints" world, signposts and wildcards.

[E/J: `scenarios.md` §2; `v1_assessment.csv`]

| | AI trusted & assured | AI brittle & contested |
|---|---|---|
| **Capacity rebuilt & coordinated** | **SC1 Assured Augmentation.** Headcount near 2024 levels but recomposed toward validators, ground-truth crews, intelligence analysts and product owners. Fieldcraft is the bottleneck. *Risk:* validation without formation. | **SC2 Human Premium.** AI is confined to low-stakes uses. Senior reviewers, consultation leads, field leaders and fire leaders command a premium. Throughput falls and backlogs grow. *Risk:* "capacity without speed" invites a political swing. |
| **Capacity thin & fragmented** | **SC3 Platform Stewardship.** Vendors, platforms and philanthropy deliver; agencies become intelligent customers. Strong private demand in GHG accounting, MRV and utilities. *Risk:* a hollow state, data-rights lock-in, a broken field ladder. | **SC4 Patchwork Retreat.** Juniors are cut and AI under-delivers. Fire absorbs capacity. Refugia carry the sector: Tribal programs, statutory state agencies, extension, endowed NGOs, data nonprofits. *Risk:* irreversible loss of fire leadership, place-based judgment, taxonomic skills and Tribal–federal relationships. |

### Predetermined in all four scenarios

- Rising fire and hazard workload
- Expert retirements
- Regulatory oscillation
- Tribal assertion of governmental roles
- Continuing private GHG-accounting demand

Signposts and triggers are in `scenarios.md` §8.4–8.5.

---

## 6. Architecture for emergence (Task 5)

### 6.1 Principles [J]

1. **Two speeds.** A fast, non-normative watch layer sits beside a slow, validated core. HR users should never see churn in what they hire against, and foresight users should never wait a year to see a new role.
2. **Compose, don't invent.** Emerging roles and competencies are built from existing or provisional L2 tasks. Their mobility, feeder roles and exposure can then be computed from day one.
3. **Every claim about the future carries a date and an expiry.** No future-facing tag goes in without `review_by`.
4. **Demand is not supply.** Record reproduction risk separately from the direction of demand, and protect capabilities whose loss would be irreversible.
5. **Scenario-condition only what is scenario-sensitive.** Do not quadruple every assessment.

### 6.2 Lifecycle states

These apply to L1 competencies, L2 tasks, L3 role profiles and L4 tools.

| State | Lives in | Meaning | Allowed uses | Review by | Entry threshold (starting values) |
|---|---|---|---|---|---|
| `watch` | L5 only (a watch item is a signal cluster plus a hypothesized entity) | Something may be forming | Foresight; "what's coming" view | +12 months; lapses if no new evidence | ≥2 signals, or one high-priority signal (protocol §6) |
| `proposed` | L1–L4, persistent ID, flagged non-normative | A draft definition exists | Foresight; curriculum exploration | +12 months | ≥3 independent signals of ≥2 types from ≥2 sector actors, **or** one mandate with an effective date. Linked to L2 tasks. |
| `emerging` | L1–L4 | Observable in work | Training, development, workforce planning. **Not selection.** | +24 months | ≥10 postings or PDs across ≥2 actor types in 12 months, **or** a named operating program. Feeder roles identified. |
| `established` | L1–L4 | Validated and stable | All uses, including selection where IO standards are met | +36 months | ≥30 postings or PDs across ≥3 actor types over 12 months, **or** a major employer's classification or PD standard. Plus SME validation to IO's standard and assessable indicators. |
| `declining` | L1–L4 | Demand falling, or the task substituted | All uses, flagged; development investment de-prioritized | +24 months | Demand share down ≥30% over 24 months, **or** v1's S-confirmation checklist met (FS-056). **Protect check mandatory.** |
| `withdrawn` | L1–L4 (ID and crosswalks kept, never reused) | No longer current | History; crosswalk | none | Below threshold for 36 months, no protect flag, and CA approval |
| `lapsed` / `merged` | L5 / L1–L4 | Watch expired / absorbed into another ID | none / redirect | none | Automatic, or CA decision |

### The `protect` overlay

It is stored as a governance decision, not computed.
- **Criteria.** At least two of these hold:
  - Failure would be severe: life safety, legal duty, irreversible ecological harm, or broken trust.
  - Reproducing the capability takes 5 years or more.
  - Supply is fragile in two or more scenarios.
- **Effects:**
  - The item cannot move to `withdrawn` without CA approval plus sector consultation.
  - It gets priority for knowledge capture (NR-2).
- **Candidates from the stress test:** 59 v1 competencies. Examples:
  - 4.2.3 prescribed burning
  - 1.3.2 forest mensuration and inventory
  - 1.4.3 species identification
  - 4.1.3 water-quality surveys
  - 6.5.1 Tribal consultation (TN decides how this is framed)

[J; `scenario_stress_test_v1.csv`]

### Relation to CA's audit

CA's audit (`docs/audit/architecture-audit.md` §11) proposes:
- lifecycle statuses: proposed, emerging, established, declining, withdrawn
- retiring the stored stability tier

I concur, and add:
- a pre-content `watch` state in L5
- the `lapsed` and `merged` states
- the `protect` overlay
- explicit evidence thresholds and review-by dates
- extension to L2 tasks and L4 tools

### 6.3 Scenario tags and scenario-conditioned assessment (L5)

Changes to tasks are recorded in three parts:

1. **Technical performability.** Dated and attributed. It does not vary by scenario at the time of assessment. LM chooses which external measures to ingest.
2. **Adoption pathway.** A *strategy* tag on the assessment: substitution, augmentation, or augmentation-for-formation.
3. **Realized impact and reproduction risk.** *Scenario-conditioned* (SC1–SC4). Each row records:
   - demand direction: up, flat, reshape, external, or down
   - reproduction risk: L, M or H

**Burden control.** Only tasks above an exposure threshold, or with a CLD flag, get scenario-conditioned rows. All L1 competencies and L3 roles get computed roll-ups.

**Computed views:**
- robustness class (robust / contingent / fragile), replacing the stability tier
- scenario-sensitivity profile
- suggested protect flags (for a governance decision)

### 6.4 Stress-testing the taxonomy

The procedure is in `scenarios.md` §9. For each major release:
1. Write role cards for each scenario.
2. Test coverage, and list scenario-critical gaps.
3. Compute sensitivity and robustness.
4. Wind-tunnel the architecture decisions themselves.

   Example: does a crosswalk centred on federal job series still serve users in SC3/SC4, when most delivery roles are state, NGO or private? I think not, which supports CA's role-variant approach.

Publish the results with the release.

---

## 7. Roles that don't exist yet (or barely do)

`role_signals.csv` holds 27 signals:
- 13 new roles
- 7 transforming roles
- 3 declining roles
- 2 entry paths at risk
- 1 merging role
- 3 skill shifts

### The eight with the strongest case for v2.0

These should enter v2.0 as `proposed` or `emerging` L3 role profiles.

| Role (ID) | Horizon | Evidence | Core competencies needed | Entry paths that feed it |
|---|---|---|---|---|
| AI-assisted environmental review lead (FS-RS-01) | 1–3y | E (FS-008, FS-044, FS-027, FS-001) | FS-C01 validate AI analyses; FS-C03 provenance and record; FS-C09 product; 6.1.4 NEPA | NEPA specialists (0028/0401); consulting project managers; holders of AI-readiness credentials |
| Environmental model risk / AI assurance officer (FS-RS-02) | 1–3y | J (FS-031) | FS-C02 model risk; FS-C10 procurement and data rights; 7.1.4 | Data scientists with regulatory exposure; QA/QC leads; senior analysts displaced by drafting automation |
| Ground-truth and reference-data steward (FS-RS-04) | 1–3y | E (FS-012, FS-023) | FS-C04; FS-C08; 2.2.3; 4.1.1 | Field technicians and inventory crews. **This gives a field-craft ladder a data-craft destination.** |
| Fire intelligence analyst, continuous ops (FS-RS-05) | now | E (FS-011, FS-053, FS-034) | FS-C05; 4.3.4; 2.1.2 | Fire crews with GIS skills; incident meteorologists (IMETs); geospatial analysts; utility situational-awareness centre staff |
| Permitting-technology product owner (FS-RS-07) | 1–3y | E (FS-007, FS-044) | FS-C09 | Experienced reviewers moving into product roles; digital-service staff gaining domain depth |
| Intergovernmental stewardship agreement manager (FS-RS-11) | 1–3y | E (FS-020, FS-039, FS-040) | FS-C14; 6.5.1; 6.5.3 | Tribal liaisons; agreements specialists; state forestry staff |
| Knowledge continuity lead (FS-RS-12) | now | J (FS-003, FS-029) | FS-C12; FS-C13 | Senior practitioners; training officers; knowledge managers |
| Corporate GHG and nature data controller (FS-RS-13) | now | E (FS-015, FS-013, FS-050) | FS-C18 | Accountants; EHS and compliance staff |

### Hold in watch

- Digital-twin steward (FS-RS-09): still research-stage. [E: FS-030]
- Drone program lead (FS-RS-08): gated by the FAA Part 108 rule. [E: FS-022]
- Climate adaptation navigator (FS-RS-15): [S]. Needs posting evidence from SL/IA.
- Administrative record and AI provenance specialist (FS-RS-17): [S] until courts rule.

### Entry paths at risk

- Entry-level NEPA/policy analyst (FS-RS-18)
- Corps, internship and seasonal crews (FS-RS-19)

These are not roles to delete. They are **pathways to redesign** (NR-1, FS-C13).

### An ambivalent new role

The environmental AI evaluation expert (FS-RS-10) offers income and mobility to displaced experts. It also builds the systems that may substitute for entry-level work, which makes it H2− in Three Horizons terms. I recommend that EMST record it as `emerging` (private sector) and track it as a signpost for Axis 2 and SC3. It should not be promoted as a career destination. [J]

### Method for designing roles that don't exist yet

Each proposed role profile must carry:
1. A function statement independent of any tool or organization.
2. A provisional task bundle linked to L2, combining existing tasks and `proposed` tasks.
3. Feeder roles, with the competency delta from each.
4. At least three evidence signals, or the reason it is speculative.
5. A horizon, a scenario sensitivity and a review-by date.
6. A named counter-signal: what would show the role is not forming.

This keeps future roles computable and honest. [J]

---

## 8. Recurring horizon scanning (summary; full protocol in `horizon_scanning_protocol.md`)

### Cadence

- Continuous machine intake (IA engine).
- Event-triggered rapid reviews within 10 working days.
- A monthly human scan and 2-page digest.
- A quarterly triage panel: FS (chair), IA, a rotating craft lead, a DB expert, a sentinel representative, TN when relevant, and CM.
- An annual Signals Review and sentinel survey, feeding the minor release.
- A scenario refresh every 3 years, or after a wildcard.

### Coding

- **Shared L5 signal schema.** Each signal records:
  - STEEP+V category, driver and signal type
  - actors, crafts and linked entities
  - novelty, reliability (A–D) and corroboration
  - impact, horizon and scenario signpost
  - CARE and personal-data flags
- **Priority score** = impact × reliability × (novelty + corroboration).
- **Routes:** log, watch, deep-dive, RFC, alert.
- **Quality check:** each quarter, 10% of signals are double-coded, with a target agreement of κ ≥ 0.6.

### People

- **Practitioner sentinels.** 60–90, **stratified and compensated**:
  - each sector actor between 8% and 30% of the panel
  - each craft at least 25%
  - early-career at least 25%
- **Institutional channels.**
  - Carried from v1: fire/WFIC and permitting.
  - New: water; air and environmental health; disclosure and markets; state and local; workforce pipeline.
  - A Tribal channel governed by TN.

### Release flow

Each signal moves through these steps:
1. Signal
2. Watch item
3. RFC
4. CA decision
5. Release, with a Signals appendix recording provenance

### Floor for year five

About 0.3 FTE FS, 0.2 FTE IA, 30 sentinels and quarterly triage. [J]

### Facilitator guide

A 2¾-hour session with sector actors (protocol §14):
1. Three Horizons on one function.
2. Signal gallery.
3. Scenario immersion: "a day in 2033" for an early-career worker and a supervisor.
4. Wind-tunnel of the participants' workforce plan and draft EMST content.
5. Backcast to no-regret moves and triggers.
6. Sentinel sign-up.

There are adaptations for 2-hour, virtual, Tribal-convened and single-agency sessions.

---

## 9. Turning long horizons into near-term workforce decisions

This is the main practical output for the federal/state first audience. Details are in `scenarios.md` §8.

### No-regret moves (late 2026 to 2029)

- **NR-1** Protect an entry cohort and its learning substrate.
- **NR-2** Run a tacit-knowledge sprint.
- **NR-3** Make AI validation and assurance cross-cutting.
- **NR-4** Treat ground truth as infrastructure.
- **NR-5** Build skills-based mobility channels.
- **NR-6** Build intelligent-customer capacity.
- **NR-7** Build agreement craft, with funded partner capacity.
- **NR-8** Run horizon scanning from v2.0.

### Contingent moves, with triggers

| Move | Trigger |
|---|---|
| CM-1 Scale AI review teams | Appellate validation of AI-assisted records, plus stable headcount |
| CM-2 Train BVLOS program leads | Part 108 rule is final |
| CM-3 Build fire-intelligence cohorts | Access terms for FireSat-class data are known |
| CM-4 Retain senior staff | AI-related remands |
| CM-5 Platform-oversight package | Contracts rise while FTE falls |
| CM-6 Refugia strategy | Entry hiring near zero and the RIF moratorium fails |
| CM-7 Digital-twin stewardship | First operational regulatory use of a twin |

**Decision point for CA:** whether these are published in the federal/state pilot package and the NGO kit. I recommend yes.

---

## 10. Answers to CA architecture questions (§6, FS)

### FS-Q1. What scenario structure should the change-signal layer carry, and should exposure assessments be scenario-conditioned? (DP-8)

**Answer.** Carry the four-scenario set SC1–SC4:
- Axis 1: capacity (rebuilt & coordinated vs thin & fragmented)
- Axis 2: AI reliability and legitimacy (trusted & assured vs brittle & contested)

Do **not** carry v1's investment × adoption-mode matrix as axes.

[E/J: FS-019, FS-003, FS-042 on decoupling; FS-054, FS-012, FS-008 on brittleness; `scenarios.md` §2–3]

**Placement.**
- **Scenario definitions** go in **L0**, as a versioned reference vocabulary. Each set carries:
  - `scenario_set_id`
  - version and refresh date
  - axis definitions
  - signposts

  They change on a 3-year cycle and many records refer to them. [J]
- **Scenario-conditioned assessments** go in **L5**.
- I suggest CA's table move "foresight scenarios" from L5 to L0, and keep "scenario-conditioned assessments" in L5.

**Conditioning: the three-part model (§6.3).**
1. Technical performability is scenario-invariant and dated. LM's lane ingests or assesses it.
2. Adoption pathway is a strategy tag.
3. Realized impact and reproduction risk are scenario-conditioned, but only for tasks above an exposure or CLD threshold.

Robustness class, sensitivity profile and protect suggestions are computed as roll-ups. This implements v1's "technical overlap × adoption mode × ladder fragility" (FS-051) without multiplying every assessment by four. [J]

**Strength of evidence.** Scenario conditioning is judgment by nature. These assessments must carry rater type and confidence like any other L5 assessment. CA's audit §10 already includes a `scenario_id?` field. I concur, and suggest adding `strategy_id?` next to it. [J]

### FS-Q2. How should the model represent roles that don't exist yet: "proposed" role profiles, or placeholder task bundles?

**Answer.** Both, joined. Represent them as **L3 role profiles in state `proposed` or `emerging`, composed from L2 task bundles that may include `proposed` tasks.** [J]
- Free-floating placeholder bundles without a role identity are not usable.
- Roles without task bundles cannot be compared, crosswalked or mapped for mobility.

**Fields required beyond a normal role profile:**
- Function statement, neutral as to tool and organization
- Evidence signals (L5 IDs) and evidence label
- Feeder roles and competency deltas
- Horizon
- Scenario sensitivity
- `review_by`
- A named counter-signal

**Before content.**
- A `watch` item in L5 (signal cluster plus hypothesized role) comes before anything enters L3.
- Proposed and emerging roles appear in a "what's coming" view, not in HR selection views (CP/IO).

**Seeds.** The 8 roles in §7 enter as `proposed` or `emerging`. The rest enter as `watch`.

[E for each role's evidence; J for the design]

### FS-Q3. What horizon-scanning cadence and intake should feed L5, and who reviews it?

**Answer.** See §8 and `horizon_scanning_protocol.md`.

**Cadence:**
- Continuous machine intake (IA)
- Event triggers (10 working days)
- Monthly human scanning
- **A quarterly triage panel:** FS (chair), IA, a rotating FC/DC/SC lead, a DB expert, a sentinel representative, TN for Tribal signals, and CM
- An annual Signals Review tied to the minor release
- A scenario refresh every 3 years

**Decision rights:**
- The triage panel routes signals and proposes changes.
- **CA decides** lifecycle changes in L1–L4.
- **IO validates** promotions to `established`.
- **TN clears** any signal carrying a `care_flag`.
- Machine-coded signals stay `machine-coded` until a human validates them.

[J; rationale in protocol §1–2]

### Comments on §4 (the provisional layered model)

1. **Lifecycle on all content layers.** Carry lifecycle state on L1, L2, L3 and L4, not only on L3 as the table implies. [J]
2. **Store `protect`.** Add it as a stored governance attribute on L1 and L3 (and on L2 where useful). It must not be computed away. [J]
3. **Replace "Stability."** Among the computed views, replace "Stability" with "robustness class" and "scenario sensitivity". I concur that the v1 tier should be retired. Its dashboard counts disagree with its own tags: 110/90/15 versus 150/53/19. [E: FS-055]
4. **Validate craft reproduction regimes early.** I support CA's L0 crafts with reproduction-regime attributes. These attributes drive most of the scenario-fragility signal in the stress test, so IO and FC should validate them early. [J]

---

## 11. Proposals

- **P-FS-01: Adopt the SC1–SC4 scenario frame.** [E/J]
  - Store the definitions in L0, versioned, with the first refresh in 2029.
  - Retire v1's axes as axes, and move augmentation/substitution to the strategy set.
  - *Why:* the 2026 evidence shows v1's axes are mis-specified.
- **P-FS-02: Lifecycle states on L1–L4.** Watch → proposed → emerging → established → declining → withdrawn, plus lapsed and merged, with the thresholds and review-by dates in §6.2. *Why:* the taxonomy can represent emergence without destabilizing the validated core. [J]
- **P-FS-03: A `protect` overlay**, with the criteria in §6.2. *Why:* demand falls first in public agencies under SC3/SC4. Without protection, the taxonomy would record the loss of irreversible capabilities as routine decline. [J]
- **P-FS-04: A three-part change model in L5:** performability; adoption pathway; scenario-conditioned impact and reproduction risk. A computed robustness class replaces the stability tier. [J]
- **P-FS-05: Emerging roles as L3 profiles.** [E/J]
  - Seed v2.0 with FS-RS-01, -02, -04, -05, -07, -11, -12 and -13 as `proposed` or `emerging`.
  - Put the remaining role signals in watch.
- **P-FS-06: Add FS-C01 to FS-C18 to the candidate pool.** [E/J]
  - Priority (no-regret) set: FS-C01, -C02, -C04, -C08, -C10, -C12, -C13, -C14.
  - Coordinate wording with:
    - DC: C01, C02, C04, C11
    - FC: C04, C08, C12
    - SC: C03, C09, C10, C14
    - IO: all
- **P-FS-07: Adopt `horizon_scanning_protocol.md`, and start at v2.0, not after the Delphi.** Seed L5 with `weak_signals.csv` and `role_signals.csv`. [J]
- **P-FS-08: A stratified, compensated sentinel panel of 60–90,** with the quotas in protocol §5.3. *Why:* it corrects the austerity bias v1 identified (FS-051). [J]
- **P-FS-09: Stress-test every major release** against SC1–SC4 (`scenarios.md` §9) and publish the results. After the Delphi, replace the heuristic with sensitivity ratings from SMEs. [J]
- **P-FS-10: Publish NR-1 to NR-8 and CM-1 to CM-7** in the federal/state pilot package and the NGO kit, as workforce-strategy guidance tied to EMST content. [J]
- **P-FS-11: Split L2 tasks that bundle production with specification, review and defence.**
  - Example: "draft an alternatives analysis" versus "specify, review and defend an AI-assisted alternatives analysis".
  - *Why:* exposure and CLD can then be computed at the pathway level (see the Futures Wheel). [J]
- **P-FS-12: v1 dispositions per `v1_assessment.csv`.** [J/E]
  - Retire 3.4.3 (crypto/DeFi).
  - Move 2.7.1, 2.7.2 and 2.7.4 to watch.
  - Rewrite 3.6.2 around its function.
  - Separate 6.2.5 from a new foresight competency (FS-C15).
  - Expand 7.2.1 and 7.2.2 into FS-C01 and FS-C13.
- **P-FS-13: A "What's coming" user view,** separate from the HR views, covering watch and emerging roles, signposts and no-regret moves. CP to design. [J]

---

## 12. Disagreements and trade-offs

1. **With v1: the scenario axes.**
   - v1 treated adoption mode as an uncertainty; I treat it as a strategy.
   - *Trade-off:* testability versus continuity with v1 work and with narratives on the research side (the sister Skills Taxonomy project). I favour testability.
   - The v1 quadrants map onto mine (`scenarios.md` §3.3), so some continuity is kept.
2. **With CA (minor).** These add to CA's direction rather than dispute it:
   - Scenario definitions should sit in L0, not L5.
   - Add a `watch` pre-state and a stored `protect` overlay.
   - Extend lifecycle states to L2 and L4.
3. **With IO (anticipated): uses of emerging content.**
   - I propose that `emerging` content may be used for training, development and workforce planning, but not for selection. IO may want even training uses gated by validation.
   - *Trade-off:* speed of response versus defensibility. A training officer who acts on an AI-assurance gap in 2027 cannot wait for a 2029 validation study.
   - I accept a hard bar on selection.
4. **With LM (anticipated): evidence for promotion.**
   - LM may prefer evidence from posting volume. Postings lag pilots and mandates by years.
   - I use corroboration across several signal types for the early states, and posting thresholds only for `established`.
   - *Trade-off:* false positives versus late detection. The `lapsed` state and review-by dates limit the cost of false positives.
5. **With DC: tool-defined roles.** Names like "drone program lead" or "FireSat analyst" risk becoming tool names. I define roles by function and keep tools in L4. DC should police this line.
6. **With FH: classification.** I do not propose new OPM series for emerging roles. Parenthetical titles, PD language and interdisciplinary positions should carry them. FH to confirm what is feasible under the 2026 series consolidation.
7. **Within the theory of change (CM).** Expert-task AI markets (FS-RS-10) give displaced experts income and mobility, which is good for individuals. They may also accelerate the substitution that hurts the sector's ladders. EMST should describe this honestly, neither promoting nor suppressing it.
8. **The biggest trade-off: designing for futures versus credibility with first users.**
   - An HR specialist will discount a taxonomy full of speculative roles. A taxonomy that describes only 2024 will be out of date at its first release.
   - *Resolution:* the two-speed architecture, with a clearly labelled, non-normative watch and emerging layer next to a validated core.
   - *Cost:* governance complexity, and a standing scanning budget (protocol §12).

---

## 13. Issues outside my area that affect the vision

- **DE: a fragile evidence base.** Public datasets that EMST will depend on can be discontinued; the NOAA billion-dollar database is precedent (FS-037). DE should snapshot or mirror critical external series with provenance, including:
  - OPM workforce data
  - NIFC data
  - agency AI use-case inventories
- **FH/AS: a thinned HR machinery.** OPM headcount is down 35%, and its 2023 skills-gap action plan has not been implemented (FS-029).
  - This is an opening: agencies need ready-made skills infrastructure.
  - It is also a risk: there are fewer counterparts to adopt it.
- **TN: the Tribal channel and content.**
  - GAO and the Roadless record show both capacity strain and assertion of governmental roles (FS-020, FS-040).
  - TN should decide whether and how a Tribal sentinel channel works.
  - FS will not scan Tribal community content beyond published records without that protocol.
- **CP: privacy design.** Sentinel identities and survey data need a privacy design. L5 must never hold person-level data.
- **AS: ownership in year five.** Horizon scanning only works if someone funds the year-five floor (protocol §12).
- **IA: intake and coding.**
  - Implement the L5 signal schema, with LLM pre-coding and confidence scores.
  - Add listings from AI-training marketplaces, and agency AI use-case inventories, to the intake.
- **LM: evidence for the change model.**
  - Corroborate or refute v1's CLD patterns with data on entry-level postings and position descriptions. FS-026 points the right way but is not occupation-specific.
  - Choose the performability measures for part 1 of the change model.
- **SC: NEPA reform.** If the SPEED Act passes, the S2/S3 task set changes materially: deadlines, limitations periods, and "substantive comment" rules. SC should keep L2 tasks durable across reforms, and use dated policy events instead of v1's static flags.
- **Sister Skills Taxonomy project (research side).** The scenario change (axes, SC2 and SC4) and the double-squeeze finding should be carried over for consistency with the v1 literature already published. Flagged per the project instructions.

---

## 14. Open questions for the Chief Taxonomy Architect

1. Do you adopt SC1–SC4 (capacity × AI legitimacy) as EMST's scenario frame, with the definitions in L0? (DP-8)
2. Do you accept lifecycle states on L1–L4, with the `watch` pre-state, the evidence thresholds and the `protect` overlay? (DP-10, DP-9)
3. Is the watch/emerging layer **published** in v2.0 (in a "what's coming" view), or held internally until v2.1? I recommend publishing it, clearly labelled.
4. Should the foresight competency FS-C15 sit in the L1 transversal practice layer, or as a core competency in a strategy cluster?
5. Do the eight seed emerging roles (§7) enter the federal/state MVP role set (DP-6), or only the watch view?
6. Will the v1 WFIC/F16 question be resolved in the role layer, with fire intelligence as an L3 role family with variants rather than a new profession family? I recommend the role layer.
7. Who owns horizon scanning after the pilot, and is the year-five floor (§8) acceptable to AS?
8. Will NR-1 to NR-8 be published as guidance with the pilot package? This is the named decision point in `scenarios.md` §8.4.
