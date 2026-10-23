# Codebook: work functions, cross-cutting modes and authority position

**WP-11 output 2b** · Codebook ID `emst-function-authority-codebook@1.0.0-draft` · Owner: IO (A8); vocabulary stewards CA with SC, DB, SL, PS · Status: draft, not yet calibrated · Date: 2026-10-23
**Decision basis:** ADR-0017 (status: "IO tests rater agreement on function and position tags in Phase 4; values with α < .667 are not shown"); SPEC §6.1, §6.5; `vocab/work_functions.yaml`, `vocab/authority_positions.yaml`. Those files govern if wording differs.
**Used by:** `protocol_reliability_study.md` blocks B and C; `spec_gold_sets.md`; production `FunctionRating` records; X5 state-class mapping review (SL).
**Labels:** [E] evidence, [J] judgment, [S] speculation. All examples are **synthetic** and carry provisional IO keys [J] for ratification by the key panel (FH, SL and PS nominees plus one SC nominee).

---

## Part A — Work function (one primary per task) and modes

### A1. What you are rating

For each **task statement**, choose:
1. **one primary work function** (13 options);
2. its **sub-function** where one applies;
3. whether either **cross-cutting mode** applies (MODE-ENGAGE, with a relationship type; MODE-RESOLVE).

Code blind: you see the task text only. You do not see its competency, role, module or any prior code (XR-01 applies by analogy). Record confidence 1–5.

### A2. The functions (vocab/work_functions.yaml, paraphrased for raters)

| Code | Function | The task's deliverable is… |
|---|---|---|
| `WF-ASSESS` | Assess and sense | a characterization of current conditions: inventory, survey, sample, observation, research data collection |
| `WF-PLAN` | Plan and design | a plan, design, strategy, or a monitoring or sampling design; mitigation planning |
| `WF-REVIEW` | Review consequences | an analysis of the consequences of a **proposed** action: effects, cumulative impacts, alternatives, historic-property effects |
| `WF-RULE` | Make rules and policy | a binding or general instrument: rule, code, standard, legislation, policy |
| `WF-AUTHORIZE` | Authorize | a permit, licence, approval or use authorization issued, applied for or administered (authority position says which side) |
| `WF-RESOURCE` | Resource and finance | money or value that arrives on workable terms: budget, appropriation, rate, fee, grant, loan, credit or easement transaction |
| `WF-BUILD` | Build and implement | a one-time project or treatment carried out: restoration, construction, remediation installation, fuels treatment |
| `WF-OPERATE` | Operate and maintain | continuous operation or maintenance of a plant, network, lab, facility or asset; process control |
| `WF-MONITOR` | Monitor and verify | repeated measurement against a baseline, standard or requirement; QA/QC; validation of data or models |
| `WF-ENFORCE` | Inspect, enforce and assure | a compliance inspection finding, an enforcement case or its resolution, or assurance |
| `WF-RESPOND` | Respond and recover | action in an incident or emergency, typically under incident command; recovery; post-disaster assessment |
| `WF-LEARN` | Learn and adapt | an adaptive-management decision, an evaluation, preserved institutional knowledge, or the formation of others |
| `WF-MANAGE` | Lead and manage organizations | supervision, programme or project management, workforce planning, administration |

**Sub-functions** (code only when the parent is chosen):
- `WF-AUTHORIZE.delegated`: operating a programme under delegated, primacy or assumed authority, or overseeing delegated delivery;
- `WF-MONITOR.attest`: preparing or certifying a report that carries legal attestation;
- `WF-ENFORCE.assist`: compliance or technical assistance to regulated entities;
- `WF-ENFORCE.assure`: independent third-party verification or assurance.

### A3. Decision rules

1. **Code the function of the deliverable, not of the programme the task sits in.** A sampling task inside a permitting programme is `WF-MONITOR` or `WF-ASSESS`, not `WF-AUTHORIZE`.
2. **One primary.** If two deliverables are named, the task is compound: choose "cannot code: compound" (ADR-0003 G-2).
3. **Engagement is never the function.** Communicating, consulting and facilitating are **modes** on the function they serve. "Hold a public meeting on the draft plan" → `WF-PLAN` + MODE-ENGAGE (public).
4. **Use the pair rules below** for the frequent confusions. They are listed most frequent first.

| Confusion | Rule | Example → code |
|---|---|---|
| ASSESS vs MONITOR | ASSESS characterizes a condition once or for a new purpose. MONITOR repeats measurement against a baseline, threshold or requirement, or checks data and model quality | baseline vegetation survey → ASSESS; quarterly sampling at permit outfalls → MONITOR; validating a land-cover model's accuracy → MONITOR |
| PLAN vs REVIEW | REVIEW analyses the consequences of an action someone has proposed. PLAN produces the plan or design | alternatives and effects chapter → REVIEW; the management plan itself → PLAN |
| REVIEW vs AUTHORIZE | REVIEW informs a decision. AUTHORIZE grants, denies, conditions, applies for or administers an authorization | effects determination → REVIEW; drafting permit conditions → AUTHORIZE |
| AUTHORIZE vs ENFORCE | AUTHORIZE is before and at issuance. ENFORCE checks compliance afterwards and handles violations | permit renewal → AUTHORIZE; inspection of a permitted site → ENFORCE |
| ENFORCE vs MONITOR.attest | The permittee's own required reports are `WF-MONITOR.attest`; the regulator's review of them for violations is `WF-ENFORCE` | certifying a discharge monitoring report → MONITOR.attest |
| BUILD vs OPERATE | BUILD is one-time with an end (a project). OPERATE is continuous | install a remediation system → BUILD; run it → OPERATE |
| OPERATE vs RESPOND | RESPOND is an incident outside normal operations, usually under incident command | process upset handled by standard procedure → OPERATE; spill response under ICS → RESPOND |
| PLAN vs RULE | RULE produces an instrument binding on others or generally applicable. PLAN binds only the planning organization's own actions | county ordinance text → RULE; county park management plan → PLAN |
| RESOURCE vs MANAGE | RESOURCE brings money in or sets financial terms with other parties. MANAGE administers internal resources and people | appropriations request → RESOURCE; staffing plan → MANAGE |
| LEARN vs MONITOR | LEARN turns monitoring results into adaptive decisions, evaluation, knowledge capture or training others. MONITOR produces the measurements | revising treatment triggers from five years of data → LEARN |
| LEARN vs MANAGE | Formation of others (task-book evaluation, mentoring, designing developmental experiences) is LEARN. Supervising work output is MANAGE | evaluate a trainee's task-book tasks → LEARN |
| AUTHORIZE vs AUTHORIZE.delegated | Use `.delegated` only when the text names operating or overseeing a delegated, primacy or assumed programme | state review of a county's delegated septic programme → AUTHORIZE.delegated |
| ENFORCE.assure vs ENFORCE | `.assure` = an independent third party verifies assertions, credits or disclosures | verify a GHG inventory as accredited verifier → ENFORCE.assure |

### A4. Modes

| Mode | Code when | Values |
|---|---|---|
| `MODE-ENGAGE` | Communicating, consulting or engaging with people **outside the performer's work unit** is a material part of doing the task to standard | `relationshipType` ∈ public · stakeholder · client · intergovernmental · government-to-government |
| `MODE-RESOLVE` | The task involves objections, appeals, hearings, litigation, mediation or negotiating a dispute | (none) |

Relationship-type rules:
- **public**: the general public or affected publics in a participation process;
- **stakeholder**: identified interested or affected parties;
- **client**: a customer or contracting party;
- **intergovernmental**: other governments or agencies, other than Tribal nations as sovereigns;
- **government-to-government**: relations with Tribal nations as sovereigns. These are **never** public participation. Tasks carrying this type are **held content** (ADR-0007; ADR-0017 §2). They are excluded from rating frames. If one appears, choose "cannot code: held content".

### A5. Anchored examples (synthetic; provisional keys [J])

| # | Task statement | Function | Sub | Modes |
|---|---|---|---|---|
| W1 | Establish permanent vegetation plots and record baseline cover for a restoration site | ASSESS | — | — |
| W2 | Collect quarterly groundwater samples at compliance wells following the sampling and analysis plan | MONITOR | — | — |
| W3 | Certify the facility's monthly discharge monitoring report as the designated signatory | MONITOR | attest | — |
| W4 | Draft effluent limits and monitoring conditions for a municipal discharge permit renewal | AUTHORIZE | — | — |
| W5 | Analyse the cumulative effects of a proposed transmission line on wetland function | REVIEW | — | — |
| W6 | Present the draft travel management plan at a public open house and record comments for the record | PLAN | — | ENGAGE (public) |
| W7 | Inspect a construction site's stormwater controls and document deficiencies against permit conditions | ENFORCE | — | — |
| W8 | Explain stormwater permit requirements to small-site operators who request help | ENFORCE | assist | ENGAGE (client) |
| W9 | Negotiate the terms of a consent order resolving a facility's permit violations | ENFORCE | — | RESOLVE; ENGAGE (stakeholder) |
| W10 | Draft a county ordinance setting setback requirements for onsite wastewater systems | RULE | — | — |
| W11 | Prepare a revolving-fund loan agreement for a water system's treatment upgrade | RESOURCE | — | ENGAGE (client) |
| W12 | Carry out a mechanical fuels treatment on a 40-hectare unit to the prescription | BUILD | — | — |
| W13 | Adjust chemical feed rates at a drinking-water plant in response to raw-water turbidity | OPERATE | — | — |
| W14 | Direct containment of a diesel spill on a river as division supervisor under incident command | RESPOND | — | ENGAGE (intergovernmental) |
| W15 | Revise thinning triggers in an adaptive-management plan from five years of monitoring results | LEARN | — | — |
| W16 | Evaluate a trainee's performance on task-book tasks and record the entrustment level | LEARN | — | — |
| W17 | Prepare the annual staffing and training plan for a field programme | MANAGE | — | — |
| W18 | Audit a state's administration of its delegated air permitting programme | AUTHORIZE | delegated | ENGAGE (intergovernmental) |
| W19 | Verify a company's reported greenhouse-gas emissions as an independent accredited verifier | ENFORCE | assure | ENGAGE (client) |
| W20 | Respond to an administrative appeal of a grazing permit decision with the decision record | AUTHORIZE | — | RESOLVE |

### A6. Edge cases

- **Research.** Data collection is ASSESS. Analysis of experiments that informs management is ASSESS unless it validates a model or dataset (MONITOR) or evaluates a programme (LEARN).
- **Data stewardship.** Curating or QA-checking a dataset is MONITOR (validation). Designing a data system is PLAN.
- **AI review tasks.** Validating AI-generated outputs before use is MONITOR (validation of data or models), whatever programme it serves.
- **Training delivery.** Teaching a course is LEARN (formation of others) + ENGAGE only if outside parties attend.
- **Contract administration.** Procurement and contract terms are RESOURCE when they set financial terms with outside parties. Day-to-day oversight of a contractor's work is MANAGE.

---

## Part B — Authority position of a unit (posting, PD, state class, role-variant description)

### B1. What you are rating

For each **position document**, choose **one** authority position: the side of a regulatory or resource relationship the position sits on **in its principal duties**. A position document is a de-identified public posting, position description or state class specification, or an EMST role-variant summary. The variant's own declared position is an editorial definition and is not rated (`display_gates.yaml#not_alpha_gated`). What is gated is whether raters assign external documents to positions consistently, which is what X5 state-class mapping and automated posting classification depend on.

### B2. Positions (vocab/authority_positions.yaml)

| Code | The position… |
|---|---|
| `regulator` | issues authorizations, inspects and enforces over **others'** actions |
| `resource-manager` | decides over lands, waters, species, assets or programmes **its employer holds or manages** |
| `regulated-party` | must meet requirements as applicant, permittee, operator in responsible charge or reporting entity, **for its own employer** |
| `service-provider` | prepares or delivers work **for another party** under contract |
| `independent-verifier` | provides third-party verification, assurance or certification that must be **independent** |
| `funder` | provides grants, loans or other financial assistance to others and oversees their use |
| `advocate` | influences decisions without formal authority; monitors and challenges |
| `advisor-researcher` | holds epistemic authority; advises, researches, synthesizes |

### B3. Decision rules

1. **Principal duties decide.** Use the duties that take the most time or are listed as primary. Ignore incidental duties ("may assist with…"). Record a secondary position in the note if it takes ≥ 25% of time.
2. **Sector actor does not decide.** A municipal utility operator is a `regulated-party`. A state lab under contract to another agency is a `service-provider`. A federal research scientist is an `advisor-researcher` (ADR-0017: position is orthogonal to sector actor).
3. **Whose resource? Whose obligation?**
   - Authority over others' private actions or facilities → `regulator`.
   - Authority over uses of resources the employer manages (federal or state lands, a land trust's easements) → `resource-manager`, even when the position issues use permits.
   - Meeting one's own employer's obligations → `regulated-party`.
   - Meeting a client's obligations → `service-provider`.
4. **Independence test** for verifier vs service provider. If the deliverable is an opinion or attestation that rules or a scheme require to be independent of the party assessed → `independent-verifier`. Otherwise, preparing the party's own submission → `service-provider`.
5. **Funder vs resource-manager.** Moving money to others under assistance agreements is `funder`. Managing one's own budget is not a position (it is a function, WF-RESOURCE).
6. **Advocate vs advisor-researcher.** Seeking a particular outcome on behalf of an organization's position → `advocate`. Providing analysis or advice whose authority rests on expertise, without a stake in the outcome → `advisor-researcher`.
7. **Mixed documents.** If two positions each take about half the duties, choose "cannot code: two readings" and note both. Mixed documents become mirror-role or variant-split evidence for FH and SL; they are not forced.

### B4. Anchored examples (synthetic; provisional keys [J])

| # | Position document summary | Position | Why |
|---|---|---|---|
| P1 | State environmental agency engineer who writes and renews wastewater discharge permits | regulator | authority over others' facilities |
| P2 | National forest district staff officer who approves special-use permits for outfitters on the forest | resource-manager | authorizes uses of a resource the employer manages (rule 3) |
| P3 | City water utility chief operator in responsible charge of the treatment plant | regulated-party | own employer's compliance obligations (rule 2) |
| P4 | Consulting firm biologist who prepares species surveys and effects reports for developers' permit applications | service-provider | client's obligations |
| P5 | Accredited verifier who issues verification opinions on facilities' greenhouse-gas reports | independent-verifier | required independence (rule 4) |
| P6 | State revolving-fund project officer who manages loan agreements with local water systems | funder | money to others under agreements |
| P7 | Watershed NGO staff who review permit drafts and file comments urging stricter limits | advocate | influence without authority |
| P8 | University extension specialist who advises landowners and agencies on grazing practices | advisor-researcher | epistemic authority, no stake in the decision |
| P9 | County environmental health inspector of restaurants and onsite septic systems | regulator | others' facilities (city or county employer is irrelevant) |
| P10 | Facility EHS manager who prepares the plant's air permit applications and compliance certifications | regulated-party | own facility |
| P11 | Land trust stewardship manager who monitors and enforces easement terms on private parcels | resource-manager | the trust holds the easement interest it enforces [J: contested; some raters will say regulator; key panel to rule] |
| P12 | State forestry agency forester who writes stewardship plans for private landowners at no cost | advisor-researcher | advice without authority over the land [J: contested with service-provider; key panel to rule] |

P11 and P12 are deliberate boundary cases; the key panel's ruling is recorded in the codebook's next PATCH.

### B5. Edge cases

- **Delegated programmes.** A state running a delegated federal permit programme is `regulator`. The federal staff overseeing the state's programme are also `regulator` (oversight of delegated delivery).
- **Public enterprises.** A public utility, port or landfill authority is `regulated-party` when it is the operator subject to permits.
- **Tribal employers and programmes.** Held. Not in any rating frame (ADR-0007).
- **Contract inspectors.** A contractor performing inspections for an agency is `service-provider` (the authority stays with the agency). Code the contractor's document, not the agency's.

---

## Cannot code (both parts)

Use "cannot code" with one of these reasons:
- `compound`;
- `missing information`;
- `two readings`;
- `held content`;
- `not a task / not a position document`.

## Version control

Same as `codebook_craft_ratings.md` §11. Any change to the function list, sub-functions, modes or positions is an L0 vocabulary change decided by CA. It voids gate results for this codebook.
