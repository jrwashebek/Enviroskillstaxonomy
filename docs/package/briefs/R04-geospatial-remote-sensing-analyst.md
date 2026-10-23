# How this role is changing: Geospatial and remote sensing analyst

*EMST v2 role-change brief · field and data corridor · as of 23 October 2026 · CC BY 4.0*

> **Status: draft for NGO-pilot preview (2026-10-23).** AI agents checked facts against sources, and some claims await
> register rows. Not yet reviewed by independent human experts. Date-sensitive statements will be re-checked before
> external release.
>
> **A first draft for your staff to correct:** written by AI agents and not yet checked by practitioners. Nothing here is
> a measurement, and nothing here is for classifying positions or for selecting, rating or removing anyone.
> [How to read these briefs](README.md).

## Who does this work

Geospatial and remote sensing analysts map and monitor environmental conditions from imagery and spatial data. They
build and validate detection and spatial models, design maps for decisions, and state accuracy and uncertainty. The
draft expects pretrained Earth-observation models to change the methods of the work, while validation, transfer testing
and fitness-for-purpose judgments grow.

| | |
|---|---|
| **Employer types** | **Federal, state, local:** resource manager (county and municipal planning GIS units at local level). **NGO and academic:** advisor or researcher with no decision authority (the academic variant adds data release packages). **Private:** consulting service provider, adding scoping and quality review at senior and lead levels. |
| **Typical titles** | GIS analyst; remote sensing analyst; geospatial specialist |
| **Federal series** | Mapped only loosely (partial fit; all active): 1370 Cartography, 0150 Geography, 0401 General Natural Resources Management and Biological Sciences, 1560 Data Science. No series is a close fit. Indicative band: GS-9 to GS-11 journey; GS-12 to GS-13 senior; GS-13 to GS-14 lead. This is not a classification criterion. |
| **State class examples** | Washington Natural Resource Scientist 2 (partial fit). No local class is mapped in the jurisdictions whose public class plans EMST read; no agency has been involved. |

## The work today (agent draft)

Main tasks, in rough work order. This is a selection; EMST shows no time shares.

| Task | Formation task |
|---|---|
| Preprocess imagery (geometry, radiometry, cloud and shadow), documenting each step | |
| Run spatial queries and overlays with consistent reference systems and scales | |
| Classify multispectral imagery into land cover from documented training data | yes |
| Interpret satellite and aerial imagery to detect change between two dates | |
| Analyze terrain, connectivity or resource distribution, stating the limits | |
| Build a predictive spatial model, validated against independent locations | |
| Assess map accuracy against independent field reference data, by class and condition | |
| Design a map for a stated audience and decision | |

## What is expected to change

| Work | Expected change (agent draft) | Driver | Outside signal (every task change: assessment pending) |
|---|---|---|---|
| Classify imagery into land cover | Transforming, compressing production: pretrained Earth-observation models and embeddings could compress classification, moving the analyst's time to training data, transfer tests and accuracy assessment | AI | Remote sensing, imagery and lidar: 63 registered AI use cases in eleven federal environmental units, 11 deployed (2025 inventory, EMST keyword classification; reliability A) [1] |
| Assess map accuracy | Transforming, growing: accuracy assessment would grow as products multiply | AI, sensing technology | none yet |
| Design maps | Transforming: generative tools can draft maps and graphics, but design for the decision stays | AI | none yet |
| **Check that a product's training data and validation reference are independent** | **New** | AI | none yet |
| **Test a pretrained model's transfer to the local ecosystem before use** (senior, lead) | **New** | AI | none yet |
| **Review AI-generated analysis code line by line, testing it on known answers** | **New** | AI | none yet |

Of the role's 32 draft tasks, the other 26 carry no drafted change claim. Context: openly licensed pretrained
Earth-observation models exist. NASA and IBM released Prithvi-EO-2.0 in December 2024, and Clay is open source under
Apache-2.0 [2]. Both are available for research and pilot use; their availability is not evidence that agencies have
adopted them for any task.

## What stays with people, and why

This describes where the work sits today. The draft moves the analyst from producing classifications toward answering
whether a product can be trusted for this decision, in this place, at this time. That means designing independent
reference samples, catching circular validation, diagnosing why a model fails at a new site or season, checking that a
use falls inside a model's intended purpose and data period, and stating uncertainty in a form users read correctly.
These judgments depend on knowing the decision and the ground. The role draws mainly on data craft, anchored in field
reference work: the exploratory pathway into it keeps a field calibration practicum at 20–30% of its time, under the
principle "no pixel without plot".

## Competencies to build next

Draft targets by level, journey / senior / lead (agent draft; design statements to test, not findings).

| Competency | Draft targets | Why now |
|---|---|---|
| Evaluate model fitness for purpose and validate against independent evidence | Independent / Senior / Lead | Transfer tests, circularity checks, envelope checks |
| Analyze remotely sensed data to map and monitor environmental conditions | Independent / Senior / Lead | The core, with production expected to compress |
| Conduct reproducible, auditable environmental analysis, including AI-assisted code | Independent / Senior / Senior | Line-by-line review of generated code |
| Quantify and communicate uncertainty for environmental decisions | Independent / Senior / Senior | Uncertainty kept in every summary |
| Validate AI-generated work products before professional use *(emerging)* | Independent / Senior / Senior | Basic data and AI skills, at a higher level for this role |
| Ground-truth remote-sensed, modeled and AI-generated outputs in the field *(emerging)* | Supervised / Independent / Senior | Field reference data |
| Design and steward field reference data for Earth-observation and AI models *(emerging)* | — / Independent / Senior | Reference design at senior level |

## Entry paths and formation

The draft marks one formation task at journey level: writing a script that reproduces a manual processing result. The
formation provisions in EMST's draft pathways add **by-hand quotas**. One processing step is done by hand before it is
scripted, and **two reference tiles are interpreted and digitized by hand** before automated classification is
credited. Only then does the learner name the classifier's characteristic confusions. The risk is analysts who validate
model output without ever having made a map by hand or stood on a reference plot. EMST's foresight analysis (a desk
exercise by an AI agent, not yet reviewed by a human panel) names this "validation without formation" as the quiet risk
in its most AI-favorable scenario [J].

## Pathways in and out (exploratory, not recommended)

- **In, field resource technician → this role (reskill):** five steps, covering spatial analysis and scripting, image
  analysis with by-hand quotas, a field calibration practicum, validation at volume with a seeded-error batch, and a
  capstone calibration report defended to the accountable official. EMST's curriculum draft estimates about 320 hours
  over 9 months [J]. A community-college certificate may fit Workforce Pell where a governor-identified in-demand
  occupation applies [3; J]. The pathway notes that it "must not be used to stop hiring field entrants".
- **Out:** the role links onward to the ground-truth and validation steward; no pathway has been drafted for that link
  yet.

None of these has been tested against observed career moves.

## What you can do now

- **Supervisor.** Require a transfer test and an independent reference before any pretrained-model output is used for a
  local decision, and record both. Make line-by-line review of AI-generated code, with tests on known answers, a
  standing rule. Ask for uncertainty in every summary.
- **Training officer.** Build by-hand quotas into onboarding (hand-digitized tiles, one manual processing step) and
  seeded-error validation drills. Give modules on specific tools an expiry date, because methods are moving fastest
  here.
- **HR specialist.** No federal series fits closely, so read the four related Federal Series Profiles in the explorer as
  context for writing duties, subject to classification review. For state and local positions, compare your class with
  the draft targets. Any selection use needs your own job analysis under 5 CFR 300.103 [4].
- **Educator.** Put the by-hand quotas into remote-sensing courses (one processing step by hand before scripting it; two
  reference tiles digitized by hand before automated classification counts) and keep field reference work in every
  course: "no pixel without plot".

## Sources

1. Office of Management and Budget, *2025 Federal Agency AI Use Case Inventory* (README as of 13 April 2026), with EMST's
   keyword classification of the eleven environmental units' records.
   https://github.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory
2. NASA-IMPACT and IBM, Prithvi-EO-2.0 repository, https://github.com/NASA-IMPACT/Prithvi-EO-2.0; Clay Foundation Model
   repository, https://github.com/Clay-foundation/model
3. ACTE, *ED Releases Final Rule on Workforce Pell*, 18 May 2026.
   https://www.acteonline.org/blog/cte-policy-watch/ed-releases-final-rule-on-workforce-pell/
4. 5 CFR part 300 (eCFR compilation; OPM interim final rule 91 FR 48236, 31 July 2026).
   https://www.ecfr.gov/current/title-5/chapter-I/subchapter-B/part-300

---

**Who wrote this.** Researched and drafted by a team of AI agents (Anthropic's Claude), each given a specialist role,
working to a charter set by the EMST project lead. AI agents checked the facts against sources in October 2026. No
independent human expert has reviewed this brief yet. Role names such as "foresight lead" are AI agent roles, not
people.

**Comment or correct.** To comment, correct an error or ask about the pilot, open an issue at
[github.com/jrwashebek/Enviroskillstaxonomy/issues](https://github.com/jrwashebek/Enviroskillstaxonomy/issues).

*Technical note.* Role key `R04-geospatial-remote-sensing-analyst` in the EMST v2 data release. Sources behind the
numbered citations: [1] claims-register rows OMB-02, RPT-28; [2] verification record V4-16 (no claims-register row
yet); [3] SKL-02; [4] SEL-02. Pathway: the field-technician-to-geospatial-analyst record (exploratory).
