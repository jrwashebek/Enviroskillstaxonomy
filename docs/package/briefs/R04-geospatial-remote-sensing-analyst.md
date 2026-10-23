# How this role is changing: Geospatial and remote sensing analyst

*EMST v2 role-change brief · `seed:R04-geospatial-remote-sensing-analyst` · corridor COR-1 · as of 2026-10-23 · CC BY 4.0 · draft awaiting WP-15 sign-off*

> **Read this first.** The task list, time shares, flags, target levels and change claims below are **agent drafts** (evidence S). No job analysis or SME panel has reviewed them. No task has a multi-rater v2 change assessment, so every change below is **assessment pending**. No change indicator has moved: every linked signal is at *watch*. Use this brief to describe and develop the role. It is not a classification basis or a job analysis, and it is not for selection, RIF or rating decisions. [How to read these briefs](README.md).

## Who does this work

Geospatial and remote sensing analysts map and monitor environmental conditions from imagery and spatial data. They build and validate detection and spatial models, design maps for decisions, and state accuracy and uncertainty. In the draft's words, pretrained Earth-observation models "change the method layer", while validation, transfer testing and fitness-for-purpose judgments grow.

| | |
|---|---|
| **Sector actors** (editorial) | **Federal, state, local:** resource manager (county and municipal planning GIS units at local level). **NGO and academic:** advisor or researcher with no decision authority (academic variant adds data release packages). **Private:** consulting service provider, adding scoping and quality review at senior and lead levels. |
| **Typical titles** | GIS analyst; remote sensing analyst; geospatial specialist |
| **Federal series** | Mapped only loosely (`relatedMatch`, all active): 1370 Cartography, 0150 Geography, 0401 General Natural Resources Management and Biological Sciences, 1560 Data Science. No series is a close fit. Indicative band: GS-9 to GS-11 journey; GS-12 to GS-13 senior; GS-13 to GS-14 lead. This is not a classification criterion. |
| **State class examples** | Washington Natural Resource Scientist 2 (`relatedMatch`). No local class is mapped in the pilot jurisdictions. |

## The work today (agent draft)

| Task | Share of time | Flags |
|---|---|---|
| Interpret satellite and aerial imagery to detect change between two dates | 8.3% | C E |
| Classify multispectral imagery into land cover from documented training data | 8.2% | C E F |
| Preprocess imagery: geometry, radiometry, cloud and shadow, documented | 5.5% | E |
| Assess map accuracy against independent field reference data, by class and condition | 5.5% | C E |
| Run spatial queries and overlays with consistent reference systems and scales | 5.5% | E |
| Analyse terrain, connectivity or resource distribution, stating the limits | 5.5% | E |
| Build a predictive spatial model, validated against independent locations | 5.5% | |
| Design a map for a stated audience and decision | 5.5% | E |

## What is changing

| Work | Change (agent draft) | Driver | Evidence status |
|---|---|---|---|
| Classify imagery into land cover | Transforming, compressing production: pretrained Earth-observation models and embeddings compress classification, and the analyst's time moves to training data, transfer tests and accuracy assessment | AI | Assessment pending. Watch: federal environmental bureaus' registered AI remote-sensing, imagery and LiDAR use cases, 2025 inventory (reliability A) [V4-15; OMB-01] |
| Assess map accuracy | Transforming, growing: accuracy assessment grows as products multiply | AI, sensing tech | Assessment pending |
| Design maps | Transforming: generative tools draft maps and graphics, but design for the decision stays | AI | Assessment pending |
| **Check that a product's training data and validation reference are independent** | **New** | AI | Assessment pending |
| **Test a pretrained model's transfer to the local ecosystem before use** (senior, lead) | **New** | AI | Assessment pending |
| **Review AI-generated analysis code line by line, testing on known answers** | **New** | AI | Assessment pending |

Context: openly licensed pretrained Earth-observation models exist. NASA and IBM released Prithvi-EO-2.0 in December 2024, and Clay is open source under Apache-2.0 [V4-16]. Their availability is not evidence that agencies have adopted them for a given task.

## What stays human, and why

This describes where the work sits today. The draft moves the analyst from producing classifications to answering whether a product can be trusted for this decision, in this place, at this time. That means designing independent reference samples, catching circular validation, diagnosing why a model fails at a new site or season, checking that a use falls inside a model's intended purpose and data period, and stating uncertainty in a form users read correctly. These judgments depend on knowing the decision and the ground. The exploratory pathway into this role keeps a field calibration practicum at 20–30% of its time, under the principle "no pixel without plot".

## Competencies to build next

Targets (agent draft): journey / senior / lead.

| Competency | Targets | Why now |
|---|---|---|
| Evaluate model fitness-for-purpose and validate against independent evidence *(distinguishing)* | L2 / L3 / L4 | Transfer tests, circularity checks, envelope checks |
| Analyse remotely sensed data to map and monitor environmental conditions *(distinguishing)* | L2 / L3 / L4 | The core, with production compressed |
| Conduct reproducible, auditable environmental analysis, including AI-assisted code | L2 / L3 / L3 | Line-by-line review of generated code |
| Quantify and communicate uncertainty for environmental decisions | L2 / L3 / L3 | Uncertainty kept in every summary |
| Validate AI-generated work products before professional use *(emerging)* | L2 / L3 / L3 | Data and AI floor, at a higher level for this role |
| Ground-truth remote-sensed, modelled and AI-generated outputs in the field *(emerging)* | L1 / L2 / L3 | Field reference data |
| Design and steward field reference data for Earth-observation and AI models *(emerging)* | – / L2 / L3 | Reference design at senior level |

## Entry paths and formation

The draft flags one formation task at journey level: writing a script that reproduces a manual processing result. The WP-07 provisions add **by-hand quotas**. One processing step is done by hand before it is scripted, and **two reference tiles are interpreted and digitized by hand** before automated classification is credited. Only then does the learner name the classifier's characteristic confusions. The risk is analysts who validate model output without ever having made a map by hand or stood on a reference plot. FS names this "validation without formation" as the quiet risk in its most AI-favourable scenario (`scenarios.md` §4, SC1 [J]).

## Pathways in and out (exploratory, not recommended)

- **In, field resource technician (R02) → this role (reskill):** five steps, covering spatial analysis and scripting, image analysis with by-hand quotas, a field calibration practicum, validation at volume with a seeded-error batch, and a capstone calibration report defended to the accountable official. About 320 hours over 9 months [J]. A community-college certificate may fit Workforce Pell where a governor-approved programme exists [V3-03; SKL-02]. The pathway notes it "must not be used to stop hiring field entrants".
- **Out:** the role links onward to the ground-truth and validation steward (R05). WP-07 has not yet authored that pathway.

None of these has been tested against observed moves (ADR-0023 §5).

## What you can do now

- **Supervisor.** Require a transfer test and an independent reference before any pretrained-model output is used for a local decision, and record both. Make line-by-line review of AI-generated code, with tests on known answers, a standing rule. Ask for uncertainty in every summary.
- **Training officer.** Build by-hand quotas into onboarding (hand-digitized tiles, one manual processing step) and seeded-error validation drills. Tag modules on specific tools with an expiry date, because the method layer is moving fastest here.
- **HR specialist.** No federal series fits closely, so read the four related Federal Series Profiles as context for writing duties, subject to classification review. For state and local positions, crosswalk your class against the role's targets. Any selection use needs your own job analysis [SEL-02].

## Sources

- EMST records: `data/v2/core/roles/seed-R04-geospatial-remote-sensing-analyst.yaml`; `data/v2/core/variants/seed-R04-*`; `docs/build/WP-08/generated/change_view/R04-geospatial-remote-sensing-analyst.json`; `docs/build/WP-08/generated/federal-series/{1370,0150,0401,1560}.md`; `docs/build/WP-08/generated/state-class/variants/seed-R04-*`; `docs/build/WP-07/staging/pathways/seed-lc-pw-cor1-field-technician-to-geospatial-analyst.yaml`; `docs/research/strategic-foresight/scenarios.md`. Explorer: `site/_site/roles/r04-geospatial-remote-sensing-analyst/`.
- [V3-03; SKL-02] ACTE, Workforce Pell final rule, 2026-05-18, https://www.acteonline.org/blog/cte-policy-watch/ed-releases-final-rule-on-workforce-pell/
- [V4-15; OMB-01] OMB 2025 Federal Agency AI Use Case Inventory, https://github.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory
- [V4-16] NASA-IMPACT/IBM, Prithvi-EO-2.0 repository, https://github.com/NASA-IMPACT/Prithvi-EO-2.0; Clay Foundation Model repository, https://github.com/Clay-foundation/model
- [SEL-02] 5 CFR part 300, https://www.ecfr.gov/current/title-5/chapter-I/subchapter-B/part-300
