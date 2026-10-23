# Codebook: craft ratings and craft-related task attributes

**WP-11 output 2a** · Codebook ID `emst-craft-codebook@1.0.0-draft` · Owner: IO (A8), with definitions owned by the FC, DC and SC leads · Status: draft. Not yet calibrated with human raters; **the 0/1/2 scale is provisional until `protocol_craft_scale_pilot.md` reports** (ADR-0005) · Date: 2026-10-23
**Decision basis:** ADR-0005; ADR-0003 G-7; SPEC §7; `vocab/crafts.yaml` (definitions and tests are quoted from there in substance; that file governs if they differ).
**Used by:** `protocol_reliability_study.md` block A, `protocol_craft_scale_pilot.md`, `spec_gold_sets.md`, and any production rating of `CraftRating` records.
**Labels:** [E] evidence, [J] expert judgment, [S] speculation. Every anchored example below is a **synthetic task written for calibration**. Its key is a provisional IO key [J], to be ratified by the three-person key panel before use (`protocol_reliability_study.md` §5).

---

## 1. What you are rating

You rate **one task statement at a time**. For each of the three crafts you say how much a competent performer of *this task* must bring of that craft:

| Value | Label | Meaning |
|---|---|---|
| **0** | none | The craft contributes nothing a competent performer must bring to this task. |
| **1** | supporting | The craft catches errors or improves quality, but someone without it can still perform the task to an intermediate standard. |
| **2** | defining | Remove the craft's contribution and the task collapses: it fails the craft's defining test (§3). |

Rate the three crafts **independently**. They do not need to sum to anything. Several crafts may be 2. A task may have **no** craft at 2: that is "general professional practice" and is a legitimate answer (ADR-0003 G-7).

You also record (§5): `fieldDependency`, `formationDependency` and the reproduction-regime attributes. Record a confidence for each rating (1 = guess … 5 = certain). Use "cannot code" (§7) when the text does not let you decide.

## 2. Blind-coding rules (XR-01; ADR-0005 §6)

1. You see only the task statement and, where present, its stated condition or purpose. You do **not** see its competency, domain, module, v1 code, v1 craft label, any other rater's rating or any machine suggestion. If you recognize a task's v1 origin, rate the text in front of you, not what you remember.
2. Rate the **task as written**, in the work condition it names. If a tool class is named ("validate AI detections", "supervise an automated aircraft"), rate the human contribution in that condition.
3. Do not rate the person, the job title or the organization. "Forester" or "data scientist" tells you nothing; the deliverable does.
4. Do not reason from the expected distribution. v1 told raters to expect FC 25–30% / DC 35–40% / SC 30–35% [E: `legacy/v1/docs/craft_assignment_criteria.md`]. That instruction is withdrawn because it is circular.

## 3. The three defining tests

Start by naming the task's **deliverable**: what exists when the task is done well (a sample, a decision on the ground, a dataset, a validated model, a permit, an agreement, a budget that holds). Then apply each test.

### 3.1 Field craft (FC)

*Definition (vocab/crafts.yaml):* perceiving, measuring, acting and staying safe in a specific place: reading land, water, air, living systems and the engineered systems that hold, treat or move them, and producing ground truth and physical interventions other work depends on.

**FC = 2 if PRESENCE and at least one of PHYSICAL CONSEQUENCE or GROUND-TRUTH AUTHORITY:**
- **Presence:** competent performance needs the performer's senses or body in the place, at the time. "Place" includes an engineered system: a plant floor, a sewer line, a sampling station or a laboratory bench where the sample is measured.
- **Physical consequence:** the performer manages consequences in the physical world in real time (safety, irreversible intervention, go/no-go).
- **Ground-truth authority:** the output is the reference against which other data are judged (a field plot, a delineation, a calibrated measurement, an inspection finding of fact).

**FC = 1** when field-formed knowledge catches errors or improves quality, but an intermediate performer could do the task without it (fitting a growth model; reviewing imagery of a familiar ecosystem; drafting a burn plan's fire-behaviour section).
**FC = 0** when neither presence nor field-formed knowledge matters (reconciling a budget; drafting a public notice).

### 3.2 Data craft (DC)

*Definition:* turning observations into **warranted** evidence, models and decision support, including specifying, validating, supervising and answering for AI-generated analysis.

**DC = 2 if all three hold:**
1. the deliverable is an **evidence product** (dataset, analysis, model, validation, risk determination, evidence-bearing design);
2. its quality is judged by its **warrant** (provenance, method, uncertainty, fitness for a stated decision);
3. doing it well needs **choosing or checking methods**, not just operating a tool.

**DC = 1** when data skill improves the product but the deliverable is something else (a field form; a permit that cites an analysis; an inspection report with a table).
**DC = 0** when there is no evidence product (felling a tree; facilitating a meeting).
**Not DC-defining:** an observation made in place (FC); an authorization or institutional commitment (SC); disciplinary knowledge every craft draws on (a knowledge area, not a task property).

### 3.3 Statecraft (SC)

*Definition:* turning knowledge and public purpose into decisions that are **authorized, legitimate, resourced and durable**. The defining deliverable is a **commitment that holds**.

**SC = 2 if** the deliverable is a commitment that needs authority, legitimacy or agreement from **another institution or the public**, and must hold over time. Remove the procedural, relational or fiscal work and you are left with a technically sound product that is unauthorized, illegitimate, unfunded or reversible.
**SC = 1** when institutional awareness improves the work but the deliverable is not itself a commitment (briefing a landowner on findings; preparing the technical section of a permit application someone else negotiates).
**SC = 0** otherwise.
**Not statecraft:**
- general management (scheduling, facilities, supervision);
- general communication;
- internal coordination that produces no authorization or legitimacy (ADR-0003 G-7; ADR-0017 `WF-MANAGE`).

## 4. Decision procedure (use it in this order)

1. **Name the deliverable** in five words or fewer. If you cannot, the task may be compound or vague: see §7.
2. **FC test.** Presence? If no → FC is 0 or 1. If yes → physical consequence or ground-truth authority? If yes → FC = 2; if no → FC = 1.
3. **DC test.** Evidence product judged by warrant, needing method choice or checking? All three → DC = 2. Data skill helps but the deliverable is something else → 1. Otherwise 0.
4. **SC test.** A commitment needing another institution's or the public's authority, legitimacy or agreement, and lasting? → SC = 2. Institutional awareness helps → 1. Otherwise 0.
5. **Check the common errors (§6)** before you submit.
6. **No 2 anywhere?** That is allowed. Do not raise a 1 to a 2 to avoid it.

## 5. Task attributes recorded with the craft rating

These are **not** craft weights (ADR-0005 §Representation 2–3). Rate them separately.

| Attribute | Values (vocab/crafts.yaml) | Decision rule | Anchor |
|---|---|---|---|
| `fieldDependency` (ordinal) | `on-site-required` · `on-site-preferred` · `remote-capable` · `remote` | Where must the work happen? Required: physical action, sampling, in-person inspection or real-time field decision. Preferred: usually on site but parts can be done remotely with tools. Remote-capable: fully off site, though visits sometimes improve it. Remote: no field component | required: collect a water sample; preferred: service a sensor station with telemetry pre-checks; remote-capable: review flagged camera-trap images; remote: prepare a budget justification |
| `formationDependency` (ordinal) | `yes` · `partial` · `no` | Must the performer's expertise have been formed through supervised field or institutional exposure, even if this task is done on a screen? Yes: competent performance relies on judgment only field or institutional formation builds. Partial: formation helps with hard cases; routine cases can be learned at a desk or in simulation. No: study, desk practice or simulation suffice | yes: adjudicate AI species identifications; partial: classify land cover from imagery in a familiar ecosystem; no: write a metadata record |
| `mentorshipDependence` (ordinal) | `L` · `M` · `H` | Supervised in-place repetitions needed to reach independent performance: L = few or none beyond instruction; M = a season's supervised practice; H = repeated supervised practice across conditions | H: fell hazard trees; M: point-count surveys; L: run a standard meter |
| `cycleDependence` (ordinal) | `none` · `seasonal` · `multi-year-or-rare-event` | How many natural or operating cycles must a learner see? Rare-event skills need simulation | rare-event: respond to an escaped prescribed fire; seasonal: phenology-dependent plant identification |
| `placeBoundness` (nominal) | `general` · `ecosystem-type` · `site-specific` · `system-specific` | How portable is the knowledge? General: across regions and actors; ecosystem-type: relearned across regions; site-specific: lost when people leave the site; system-specific: bound to one engineered system's configuration | system-specific: operate one plant's process-control loops; site-specific: know where a creek floods first |
| `currencyDecay` (ordinal) | `L` · `M` · `H` | How fast does unpractised skill decay? | H: aerial ignition; L: soil description |
| `credentialGate` | `none` · `internal-qualification` · `external-certificate` · `licence` | **Not rated.** It is a verified fact recorded from the Credential register with a source (display_gates.yaml#not_alpha_gated). If you believe a gate applies, write it in the note | — |

## 6. Common errors and edge cases (decision rules)

| # | Situation | Rule |
|---|---|---|
| E1 | **Operating a tool vs. producing warrant.** Running a model, entering data, operating a GIS interface | Operating is not DC 2 (T-2: evidence only by operating an interface is L4 fluency). DC 2 only if the task requires choosing or checking methods and the product is judged by warrant |
| E2 | **Same tool, different task.** Flying a drone near crews vs. processing the imagery | Rate the task, not the tool. Flying near crews: FC 2 (presence + physical consequence), DC 1, SC 1 (airspace or crew coordination). Processing: DC 2, FC 1, remote-capable, formation yes [J; FC worked example, FC report §4] |
| E3 | **Remote review that needs field formation.** Checking AI species identifications against recordings or images | FC is 1 (no presence) unless the task requires going to the site. Record `formationDependency = yes`. Do **not** raise FC to 2 because field formation matters: formation is an attribute, not a weight (ADR-0005). If the task says "against field observations made by the performer", presence holds and FC can be 2 |
| E4 | **Inspection** | Typically FC 2 (presence + ground-truth authority for findings of fact) **and** SC 2 (the finding supports an enforceable determination that must withstand challenge). Both may be 2 (ADR-0005 Consequences) |
| E5 | **General management, supervision, scheduling** | SC 0 unless the task produces authorization, legitimacy, resourcing or a durable cross-institution commitment. Supervising a crew: SC 0, FC per presence |
| E6 | **Budgets and money** | Internal tracking: SC 0–1. Securing appropriations, writing a grant agreement's terms or setting a fee schedule that must survive review: SC 2 |
| E7 | **Communication** | Writing or presenting is not a craft by itself. A public meeting is SC 2 only when it confers legitimacy on a pending decision (a hearing, a consultation step). An outreach talk is SC 0–1 |
| E8 | **Design of monitoring or sampling** | DC 2 (a design for inference). FC 1 if done at a desk; FC 2 only if the design is made in place (siting plots on the ground). Formation usually yes. DC and FC may both be high (ADR-0005 dissent) |
| E9 | **Engineered systems and laboratories** | The DB broadening counts presence at a plant, network or lab bench. Operating a treatment process in real time: FC 2 (presence + physical consequence), `placeBoundness = system-specific`. Bench analysis whose result is the reference value: FC 2 (presence + ground-truth authority). Record confidence; FC may contest this boundary (ADR-0005 dissent) |
| E10 | **Permits, rules, agreements** | Drafting conditions that bind another party: SC 2. The technical basis (an effluent-limit calculation) may be DC 2 in a separate task. If the task bundles both, rate both and flag "possible compound" in the note |
| E11 | **Tasks naming AI or automation** | Rate the human contribution in that condition. "Supervise an automated sorting line": FC 2 if in place with physical consequence; DC per whether the performer checks system outputs against warrant |
| E12 | **Knowledge-only statements** ("Know the hydrologic cycle") | Not a task. Choose "cannot code: not a task" |
| E13 | **Compound tasks** ("Develop and maintain…") | Choose "cannot code: compound". The author must split it (ADR-0003 G-2) |
| E14 | **Tribal-related tasks** (government-to-government relations, Tribal data or Indigenous knowledge) | Held. They are not in any rating frame. If one appears, choose "cannot code: held content" and do not rate it (ADR-0007) |
| E15 | **Complexity-dependent cases** (simple vs. complex riparian buffers; v1 integration point 9) | Rate the task as written. If the text does not say which case, rate the modal case it describes and lower your confidence. Do not average two imagined tasks |

## 7. Cannot code

Choose "cannot code" with a reason in any of these cases:
- `not a task`;
- `compound`;
- `missing information` (the text does not say what is produced);
- `held content`;
- `two readings` (the text supports two different deliverables).

These answers are data. A dimension with > 10% cannot-code is a codebook or text defect (`protocol_reliability_study.md` §7.3).

## 8. Anchored calibration examples (synthetic; provisional keys [J])

The calibration set uses FC's four worked examples [J: FC report §4, from FC-029]. It also uses tasks written to represent nine of v1's ten craft integration points [E: `legacy/v1/docs/craft_assignment_criteria.md` "Ten Integration Points"]. **Integration point 2 (Traditional Ecological Knowledge integration) is excluded** under the Tribal hold (ADR-0007): Indigenous knowledge is out of scope by design. The tasks are re-written as v2 task statements, because v1 rated competencies.

| # | Task statement (synthetic) | FC | DC | SC | fieldDep. | formation | Why (rule) |
|---|---|---|---|---|---|---|---|
| C1 | Plan and fly a UAS survey mission near active crews, holding the flight when crew positions conflict with the flight path | 2 | 1 | 1 | on-site-required | yes | presence + physical consequence; airspace and crew coordination is supporting (E2) |
| C2 | Process survey imagery into an orthomosaic and report its positional accuracy against ground control points | 1 | 2 | 0 | remote-capable | yes | evidence product judged by warrant; ground-control judgment is field-formed (E2) |
| C3 | Conduct a field inspection of a permitted facility and document findings of fact against permit conditions | 2 | 0 | 2 | on-site-required | yes | ground-truth authority + enforceable finding (E4) |
| C4 | Evaluate AI-generated species identifications against recordings, accepting, correcting or rejecting each | 1 | 1 | 0 | remote-capable | yes | no presence → FC 1; formation is the attribute (E3). DC 1: checking outputs, not designing the validation |
| C5 | Interpret satellite imagery to map landscape-scale vegetation change for a forest plan | 1 | 2 | 0 | remote-capable | partial | v1 point 1: DC defining, field grounding supporting |
| C6 | Write the prescription and contingency section of a prescribed-burn plan for a unit | 1 | 1 | 1 | remote-capable | yes | v1 point 3 as a planning task; no presence; the commitment (approval) is a separate task |
| C7 | Make the go/no-go decision on a prescribed burn from on-site weather and fuel observations | 2 | 0 | 1 | on-site-required | yes | presence + physical consequence; authorization was made earlier |
| C8 | Map stakeholder interests and influence for a contested water allocation decision, using network analysis of meeting records | 0 | 1 | 2 | remote | partial | v1 point 4: the deliverable serves a durable decision; DC is the method |
| C9 | Synthesize population and threat evidence into a species status assessment for a listing decision | 0 | 2 | 1 | remote | partial | v1 point 5: warrant of the synthesis is defining; regulatory framing supporting |
| C10 | Design decision triggers and response protocols for an adaptive management agreement among three agencies | 0 | 1 | 2 | remote | partial | v1 point 6: institutional learning architecture binds partners |
| C11 | Recommend source populations and exchange rates for a genetic rescue, stating uncertainty in viability gains | 0 | 2 | 0 | remote | partial | v1 point 7: analytical judgment is the deliverable |
| C12 | Screen a proposed project's area for cumulative environmental burdens and document the screening basis for the record | 0 | 2 | 2 | remote | partial | v1 point 8: co-equal; both 2 is allowed |
| C13 | Lay out riparian buffer widths on the ground for a harvest unit, adjusting for observed channel and slope conditions | 2 | 0 | 0 | on-site-required | yes | v1 point 9 (simple case): presence + irreversible intervention |
| C14 | Calculate mitigation credits for a wetland bank under the applicable crediting requirements | 0 | 1 | 2 | remote | partial | v1 point 10: value set by the regulatory system |
| C15 | Reconcile monthly programme expenditures against the approved budget | 0 | 0 | 0 | remote | no | general professional practice (G-7); no craft at 2 |
| C16 | Run a jar test and adjust coagulant dose on a treatment train during a turbidity spike | 2 | 1 | 0 | on-site-required | yes | engineered system: presence + physical consequence (E9); system-specific |

Keys C5–C14 are IO's reading of v1's integration-point rationales applied to task text. **Expect disagreement on C6, C9, C12 and C14** (v1 itself flagged them as contested). Disagreement on them is information for the key panel, not rater error.

## 9. Alternative scales (pilot only; ADR-0005 §4, §7)

- **F1 constant-sum:** distribute 100 points across FC, DC and SC by how much each is irreducible to doing the task. A task with no defining craft may give its points to "general practice" (the fourth bucket). Raters see the same definitions (§3).
- **F2 ordinal:** this codebook's 0/1/2.
- **Nominal-defining (derived):** the set of crafts at 2 (F2), or at ≥ 40 points (F1). Empty set = general practice.

## 10. One-page rater checklist

1. Read the task. Name the deliverable.
2. FC: presence? then consequence or ground truth? → 2 / 1 / 0.
3. DC: evidence product + warrant + method choice? → 2 / 1 / 0.
4. SC: a commitment from another institution or the public that must hold? → 2 / 1 / 0.
5. No craft at 2 is allowed.
6. Field dependency, formation dependency, reproduction attributes. Do not let them change the craft ratings.
7. Confidence 1–5. Cannot code if needed, with a reason.
8. Never look up the task's competency or v1 code.

## 11. Version control

- Changes to definitions, tests, decision rules or the value set are a MINOR codebook version. They invalidate agreement results for gating (`display_gates.yaml#admissibility.invalidated_by`).
- Wording clarifications that leave decisions unchanged are a PATCH, attested by the key panel.
- The definitions belong to `vocab/crafts.yaml`. A conflict between this codebook and that file is resolved in the vocabulary by CA.
