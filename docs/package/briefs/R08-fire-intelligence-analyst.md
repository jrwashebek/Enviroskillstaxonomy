# How this role is changing: Fire intelligence analyst (continuous operations, emerging role)

*EMST v2 role-change brief · `seed:R08-fire-intelligence-analyst` (forest module) · corridor COR-2 · lifecycle **emerging**, review by 2027-10-23 · as of 2026-10-23 · CC BY 4.0 · draft awaiting WP-15 sign-off*

> **Read this first.** The task list, time shares, flags, target levels and change claims below are **agent drafts** (evidence S). No job analysis or SME panel has reviewed them. No task has a multi-rater v2 change assessment, so every change below is **assessment pending**. No change indicator has moved: every linked signal is at *watch*. Use this brief to describe and develop the role. It is not a classification basis or a job analysis, and it is not for selection, RIF or rating decisions. [How to read these briefs](README.md).

## Who does this work

This is an **emerging year-round role**. Fire intelligence analysts fuse satellite, camera, sensor, weather and resource data into operational fire intelligence. They adjudicate automated detections, predict spread with stated confidence, track forecast skill, and brief duty officers and incident leaders so that resources are ordered on evidence. Much of this work is done today inside incident positions such as fire behaviour and long-term analysts, and in predictive services.

| | |
|---|---|
| **Sector actors** (editorial) | **Federal and state:** resource manager. No local, NGO or private variant is drafted. |
| **Typical titles** | Fire behaviour analyst; predictive services analyst; fire intelligence specialist |
| **Federal series** | Spread across series with no close fit (`relatedMatch`, all active): 1340 Meteorology, 0401, 1560 Data Science, 0462 Forestry Technician, 2210 IT Management, 0132 Intelligence. Indicative band: GS-9 to GS-11 journey; GS-12 to GS-13 senior; GS-13 to GS-14 lead. This is not a classification criterion. |
| **State class examples** | None mapped in the pilot jurisdictions. |

## The work today (agent draft)

| Task | Share of time | Flags |
|---|---|---|
| Integrate satellite detections, camera feeds, weather and resource status into a continuously updated situation summary for dispatch | 18.2% | C E |
| Adjudicate an automated fire detection against cameras, public reports and other sensors before resources are ordered | 9.0% | C E F |
| Brief duty officers and incident commanders on activity, predicted growth and resource needs | 9.0% | C |
| Predict spread, intensity and spotting for an operational period, stating assumptions | 9.0% | C E F |
| Track the accuracy of detections and spread predictions against outcomes | 4.5% | |
| Brief leaders on the confidence of projections, updating when observations diverge | 4.5% | C |

## What is changing

| Work | Change (agent draft) | Driver | Evidence status |
|---|---|---|---|
| **The role itself** | **New role forming:** year-round fire intelligence is taking shape as detection networks come online and federal fire is reorganized under the U.S. Wildland Fire Service (Secretarial Order 3448, January 12, 2026) [V1-06; WF-07] | sensing tech, AI, policy | A satellite-deployment signal is linked but not yet verified, so it is not quoted here (FIRE-02, awaiting WP-15) |
| **Continuous multi-source fusion for dispatch** | **New** | AI, sensing tech | Assessment pending |
| **Adjudicate automated detections before ordering** | **New** | AI, sensing tech | Assessment pending. Watch: federal environmental bureaus' registered AI fire and smoke use cases, 2025 inventory (reliability A) [V4-15; OMB-01] |
| **Track forecast skill against observed outcomes** (senior, lead) | **New** | AI | Assessment pending |
| Predict fire spread and intensity | Transforming: spread models run continuously, and hand-worked predictions are kept as a formation check | AI | Assessment pending |

**Counter-signal, recorded in the role set:** the function may stay inside incident positions with no year-round staffing (`docs/decisions/mvp_role_set.csv`). FS lists funding fire-intelligence cohorts as a *contingent* move (CM-3). It holds until agencies ingest new satellite-class detection data with known access terms, because acting earlier risks lock-in to a data product whose licensing is unknown (`scenarios.md` §8.4, [J]).

## What stays human, and why

This describes where the work sits today. The role exists to put a person between an automated detection and a resource order. The draft's core judgments are whether a detection is real, whether a forecast system's skill is still good enough for the decision it serves, when to restrict or retire it, and how confident a briefing should sound. Each is a judgment about consequences and accountability. The bundle also keeps a field link: escalating AI output that conflicts with field evidence, and field-checking automated perimeters and fuels products.

## Competencies to build next

Targets (agent draft): journey / senior / lead.

| Competency | Targets | Why now |
|---|---|---|
| Fuse multi-source fire intelligence into operational decision support *(emerging; distinguishing)* | L2 / L3 / L4 | The role's core new work |
| Build, run and validate environmental forecast and scenario systems *(emerging)* | L2 / L3 / L4 | Skill tracking; restrict or retire decisions |
| Predict fire behaviour from fuels, weather and topography | L2 / L3 / L4 | Hand-worked check on models |
| Quantify and communicate uncertainty for environmental decisions | L2 / L3 / L4 | Confidence briefings |
| Validate AI-generated work products before professional use *(emerging)* | L2 / L3 / L3 | Detection adjudication |
| Ground-truth remote-sensed, modelled and AI-generated outputs in the field *(emerging)* | L2 / L2 / L3 | Field checks of automated perimeters |
| Communicate environmental and health risks under uncertainty | L2 / L3 / L3 | Public smoke advisories |

## Entry paths and formation

People arrive from fire operations (R06) or geospatial analysis (R04). The WP-07 reskilling pathway protects the judgment the role depends on. Learners make **five hand-worked spread and intensity predictions** checked against observed behaviour, and must explain their errors **before modelled outputs are credited**. They then work a seeded-error detection set in which both false alarms and misses must be caught, and field-check automated products on three incidents or burns. The formation threat is scarce detail and duty-officer slots after the 2025–26 staffing losses. The USFS and the NPS each lost more than a quarter of their employees between September 2024 and January 2026 [V1-02; WF-02].

## Pathways in and out (exploratory, not recommended)

- **In, wildland fire operations (R06) → this role (reskill):** five steps, covering behaviour prediction compared with observation, fusing and adjudicating detections, incident maps and forecast systems (tool modules expire), field checks ("no pixel without plot"), and briefing confidence to incident leaders and the public ("no model without a decision owner"). About 300 hours over 18 months, including one to two fire seasons [J]. Replayed historical incidents in simulation cover rare large-fire events.
- **In (role link, no pathway authored yet):** from geospatial and remote sensing analyst (R04).
- **Out:** none recorded. The role is too new.

None of these has been tested against observed moves (ADR-0023 §5).

## What you can do now

- **Supervisor or duty officer.** Write down who adjudicates automated detections before resources are ordered, and what they check. Track detection and spread-prediction accuracy over a season and report systematic errors. Keep hand-worked predictions as a periodic check on models.
- **Training officer.** Use the R06-to-R08 sequence to build the function from inside operations staff. Combine duty-officer shadowing in season with replayed incidents in simulation out of season. Tag forecast-system modules to expire.
- **HR specialist.** No series fits, so describe the duties within existing series positions, labelled subject to classification review, and record the gap. FS's contingent move CM-3 suggests waiting for its trigger before creating standing cohorts [J].

## Sources

- EMST records: `data/v2/modules/forest/roles/seed-R08-fire-intelligence-analyst.yaml`; `data/v2/modules/forest/variants/seed-R08-*`; `docs/build/WP-08/generated/change_view/R08-fire-intelligence-analyst.json`; `docs/build/WP-08/generated/federal-series/variants/seed-R08-fire-intelligence-analyst--federal.md`; `docs/build/WP-07/staging/pathways/seed-lc-pw-cor2-fire-operations-to-fire-intelligence.yaml`; `docs/decisions/mvp_role_set.csv`; `docs/research/strategic-foresight/scenarios.md` §8.4. Explorer: `site/_site/roles/r08-fire-intelligence-analyst/`.
- [V1-02; WF-02] Partnership for Public Service (data to Jan 2026), https://ourpublicservice.org/?p=47956
- [V1-06; WF-07] U.S. Department of the Interior, SO 3448, 2026-01-12, https://www.doi.gov/document-library/secretary-order/so-3448-establishment-us-wildland-fire-service
- [V4-15; OMB-01] OMB 2025 Federal Agency AI Use Case Inventory, https://github.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory
