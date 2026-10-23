# ADR-0017: The work-function facet, cross-cutting modes, workflow profiles, authority position and sign-off authority

- **Decision point:** DP-16 (work-function facet; SC generalization; DB's Operate & maintain and Respond & recover; regulatory-posture facet; PS posture and sign-off authority)
- **Status:** accepted (IO tests rater agreement on function and position tags in Phase 4; values with α < .667 are not shown to users)
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** SC, DB, SL, PS, FC, DC, FH, IO, TN, LM
- **Related:** ADR-0002, ADR-0006, ADR-0007, ADR-0022 (credentials); `vocab/work_functions.yaml`, `vocab/workflow_profiles.yaml`, `vocab/authority_positions.yaml`, `vocab/authority_positions.yaml#sign_off_authority`

## Context

v1's six stages are a public-lands project and authorization lifecycle; S1 is primary for 111 of 222 competencies and S6 for 4; enforcement had to be tagged S2; sustainability reporting carried "digital permitting" flags; air quality carried "NEPA timeline" [E: audit §8; DB §3.1, §3.9]. CA's draft facet (Assess & sense → Plan & design → Authorize & regulate → Implement & operate → Monitor & verify → Enforce & assure → Learn & adapt → Engage & communicate) was tested by DB against 44 subsectors and by SC against seven governance contexts; both found it "mostly holds" with specific changes. Three roles independently found a missing axis: which side of the regulatory relationship a role sits on (SL "authority position", DB "regulatory position", PS "posture"), plus PS's **sign-off authority**.

## Decision

### 1. Work functions (primary facet on L2 tasks; role and competency values computed)

| Code | Function | Includes | Source of change |
|---|---|---|---|
| `WF-ASSESS` | Assess & sense | inventory, survey, sampling, characterization, observation, environmental research data collection | CA draft |
| `WF-PLAN` | Plan & design | plans, designs, strategies, monitoring and sampling designs, mitigation planning | CA draft |
| `WF-REVIEW` | Review consequences | NEPA and state EPA review, EHP review, effects analysis, cumulative-impact analysis | **SC**: split from Authorize (§112 accelerates NEPA but not ESA/NHPA [E: SC-039]) |
| `WF-RULE` | Make rules & policy | rulemaking, legislation, codes, standards, policy instruments | **SC** (APA distinguishes rulemaking from adjudication) |
| `WF-AUTHORIZE` | Authorize | permits, licences, approvals, special uses, grazing and mineral authorizations; sub-function `WF-AUTHORIZE.delegated` = administer or oversee delegated/assumed programmes | CA draft; **SL** (oversee delegated delivery) |
| `WF-RESOURCE` | Resource & finance | budgets, appropriations, rates, fees, grants and financial assistance (SRF), credit and easement transactions, green finance | **SC**, **SL** (fund/assist), DB ("Finance & transact") |
| `WF-BUILD` | Build & implement | restoration, treatments, construction, remediation installs, one-time projects | **DB**: split from Implement & operate |
| `WF-OPERATE` | Operate & maintain | continuous operation of plants, networks, labs, facilities and assets; vegetation and asset maintenance | **DB**, **SL** |
| `WF-MONITOR` | Monitor & verify | monitoring, measurement, QA/QC, validation; sub-function `WF-MONITOR.attest` = **Report & attest** (DMRs, TRI, GHGRP, CCRs, corporate disclosures) | CA draft; **DB** |
| `WF-ENFORCE` | Inspect, enforce & assure | compliance inspection, enforcement cases, compliance and technical assistance (`.assist`), third-party verification and assurance (`.assure`) | CA draft; **SL** (inspect, enforce) |
| `WF-RESPOND` | Respond & recover | incident and emergency response under ICS, recovery, post-disaster assessment | **DB** |
| `WF-LEARN` | Learn & adapt | adaptive management, evaluation, knowledge continuity, developing people (formation of others) | CA draft |
| `WF-MANAGE` | Lead & manage organizations | supervision, programme and project management, workforce planning, administration | **CA addition** (keeps general management out of Statecraft, P-SC-07) |

### 2. Cross-cutting modes (multi-valued, optional, on tasks)

- `MODE-ENGAGE` **Engage & communicate**, with `relationshipType ∈ {public, stakeholder, client, intergovernmental, government-to-government}`. **Government-to-government relations with Tribal nations are a distinct relationship type, never "engagement" in the public-participation sense** (SC §8 Q2; TN), and tasks carrying it fall under ADR-0007's gate.
- `MODE-RESOLVE` **Resolve & defend**: objections, appeals, hearings, litigation, mediation and negotiation of disputes — windows that sit across review and authorization (SC).

### 3. Workflow profiles (named sequences over work functions)

`WP-PROJECT` project-and-authorization lifecycle (**v1 S1–S6, kept**: S1→PLAN, S2→REVIEW, S3→AUTHORIZE, S4→BUILD/OPERATE, S5→MONITOR, S6→LEARN; the S2/S3 separation for permitting-reform analysis is preserved); `WP-REGPROGRAM` regulatory-programme cycle; `WP-OPERATIONS` operations cycle; `WP-COMPLIANCE` compliance and enforcement cycle; `WP-DISCLOSURE` disclosure cycle; `WP-INCIDENT` incident cycle; `WP-RULEMAKING` rulemaking cycle; `WP-CAPITAL` utility capital-and-compliance cycle; `WP-AGREEMENT` stewardship-agreement cycle; `WP-RESEARCH` research cycle (P-DB-05, P-SC-03).

### 4. Authority position (required attribute on every role variant; orthogonal to sector actor)

| Code | Position | Example |
|---|---|---|
| `regulator` | issues authorizations, inspects, enforces over others | state NPDES permit writer; county EH inspector |
| `resource-manager` | decides over resources it holds or manages | USFS district ranger; state forester; land trust steward |
| `regulated-party` | applicant, permittee, operator in responsible charge, reporting entity | utility operator; facility EHS manager; developer |
| `service-provider` | prepares or delivers for another party under contract | environmental consultant; contract crew |
| `independent-verifier` | third-party verification, assurance, certification | GHG verifier; certification-scheme auditor |
| `funder` | grants, loans, financial assistance | SRF programme manager; foundation |
| `advocate` | influence without authority; watchdog | NGO policy advocate |
| `advisor-researcher` | epistemic authority; advisory | academic advisor; agency research scientist |

One employer can hold several positions (a city regulates as a health department and is regulated as a POTW); position belongs to the **variant**, not the employer. Mirror roles (permit writer ↔ permittee compliance manager ↔ consultant preparer) share tasks with inverted posture and are linked for mobility (P-DB-06, P-SL-02, P-PS-01).

### 5. Sign-off authority (attribute on tasks and role variants)

`signOffAuthority ∈ {licensure (PE, PG, RPF, certified operator in responsible charge), legal-signatory (certifying official), regulatory-definition (ASTM/AAI "Environmental Professional", SOI-qualified), accreditation (accredited verifier), position-qualification (NWCG/NIMS position)}`, each linked to Credential records (ADR-0022). A task that requires sign-off records it; a role variant that holds it records it. Mobility computations treat missing sign-off as a **blocking friction**, not a skill gap (P-PS-02; DB §3.5).

### 6. Industry, ownership and delivery model

Facets on variants (ADR-0007): industry (PS's 14 employer types), ownership, delivery model.

## Rationale and evidence

- DB: "Authorize & regulate works for both permit writers and applicants, *provided* a regulatory-position facet tells which side the role is on"; merging Build and Operate "recreates the v1 S4 problem"; incidents run at a tempo and under a command structure unlike deliberative functions (DB §7 Q2).
- SL: in 70 sampled state and local classes, the most-mapped v1 competencies are 6.1.2 (29 classes) and 6.1.3 (18), both written from the regulated party's side; the state jobs are permit writers, inspectors, enforcement case managers and primacy staff [E: SL-088, SL-079, SL-072, SL-071, SL-050].
- PS: private employers hire on sign-off authority, entry-gate credentials, named regulatory-programme experience and, at senior levels, business practice [E: PS-016, PS-026]; mirror roles share tasks but invert posture (PS §6).

## Consequences

- Each v1 task gets a work-function value in migration from its stage tags as prior evidence, then re-rated.
- Fifteen values (13 functions + 2 modes) is longer than CA's draft of eight. Users see function names on roles and filters, not the whole list.

## Dissent and trade-offs

- **SC vs CA draft:** "Engage & communicate" moved from a stage to a mode, and Authorize split — accepted; the facet is less simple, but utilities, air districts and counties now fit (SC disagreement 4).
- **SL** wanted authority position as a facet on role variants rather than an L0 term applied to tasks (SL open Q1) — adopted on variants; tasks inherit it only through the variant.
- **DB** considered "Finance & transact" orphaned under Plan & design — given its own home in `WF-RESOURCE`.
- **Trade-off named:** a richer facet that more raters must agree on versus misclassifying two of the largest job families (operators and emergency responders) and most state regulatory work.

## Amendments

- **2026-10-23 — CR-IO-002 / ADR-0029 §6 (CA).**
  - **Unmeasured equals not shown.** The status line ("values with α < .667 are not shown") applies to Task.workFunction and to the assignment of external units to authority positions. Before any admissible study, views show "Assessment pending".
  - **Editorial fields.** RoleProfile.primaryWorkFunction, RoleVariant.sectorActor, sectorActorSubtype and authorityPosition are definitional and are labelled "editorial", not α-gated. Views navigate by the editorial role function until the work-function study reports.
