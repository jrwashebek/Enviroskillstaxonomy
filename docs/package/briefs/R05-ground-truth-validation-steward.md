# How this role is changing: Ground-truth and validation steward (emerging role)

*EMST v2 role-change brief · `seed:R05-ground-truth-validation-steward` · corridor COR-1 · lifecycle **emerging**, review by 2027-10-23 · as of 2026-10-23 · CC BY 4.0 · WP-15 first pass (2026-10-23): cleared for internal and NGO-pilot preview use; external release awaits AS co-signature and the rc.1 re-check of moving facts*

> **Read this first.** The task list, time shares, flags, target levels and change claims below are **agent drafts** (evidence S). No job analysis or SME panel has reviewed them. No task has a multi-rater v2 change assessment, so every change below is **assessment pending**. No change indicator has moved: every linked signal is at *watch*. Use this brief to describe and develop the role. It is not a classification basis or a job analysis, and it is not for selection, RIF or rating decisions. [How to read these briefs](README.md).

## Who does this work

This is a role EMST sees **forming**, not one that is established. Ground-truth and validation stewards design and look after the field reference data and validation samples that remote, modelled and AI-generated products are tested against. They code the field causes of mismatch, calibrate observers, and state whether a product is fit for a stated use. Today the work is usually spread across technicians, analysts and programme scientists rather than held by one post.

| | |
|---|---|
| **Sector actors** (editorial) | **Federal:** science agencies (advisor or researcher). **State:** resource manager. **NGO and academic:** advisor or researcher (academic variant adds data release packages). **Private:** Earth-observation and monitoring-technology firms and carbon measurement services (service provider). |
| **Typical titles** | Validation lead; reference data steward; field validation specialist |
| **Federal series** | No dedicated series (X4 `NoTermFound` for the role as a whole). Loosely related (`relatedMatch`, active): 0401, 0404, 1560. Indicative band: GS-9 to GS-11 journey; GS-12 to GS-13 senior. This is not a classification criterion. |
| **State class examples** | None found in the pilot jurisdictions or in SL's state classification sample. |

## The work today (agent draft)

| Task | Share of time | Flags |
|---|---|---|
| Record reference observations at validation points, blind to the product's prediction | 9.9% | C E F |
| Design a field validation sample (strata, size, access limits) with an analyst | 6.8% | C E |
| Code the field cause of each product–field mismatch (timing, mixed pixels, hidden understory, location error) | 6.8% | C E |
| Plan a regional network of reference plots and labelled samples (senior) | 6.8% | C |
| Collect labelled field samples with the metadata models and validators need | 6.8% | C E F |
| Decide from field evidence whether a product is fit for a stated use, documenting its limits (senior) | 3.4% | C |

## What is changing

| Work | Change (agent draft) | Driver | Evidence status |
|---|---|---|---|
| **The role itself** | **New role forming:** validating remote and AI products is becoming a distinct responsibility, and no dedicated federal series exists | AI, sensing tech | Context only: BLS projects +7% for environmental science and protection technicians over 2025–35 [BLS-02]. No posting baseline exists yet to test whether the role is appearing (`CHANGE_SIGNALS.md` §5.5). |
| Blind reference collection | Emerging: grows with product use | AI, sensing tech | Assessment pending |
| **Plan regional reference networks for Earth-observation models** | **New** | AI | Assessment pending |
| **Label reference sets without seeing tool outputs** | **New** | AI | Assessment pending |
| Review classifier-labelled camera, acoustic or genetic detections | Transforming, compressing manual screening: review queues replace it | AI | Assessment pending |

**Counter-signal, recorded in the role set:** validation could be absorbed into vendor services, leaving agencies with no field calibration of their own (`docs/decisions/mvp_role_set.csv`). If that happens, the role may not form inside public employers. The role is under lifecycle review by 2027-10-23 and lapses without new evidence (ADR-0015).

## What stays human, and why

This describes where the work sits today. The role exists because an automated product cannot validate itself. Someone has to stand at an independent point, observe without seeing the prediction, and explain the disagreement in field terms. The draft codes most tasks as needing field-formed identification and measurement skill, and names "reject automated detections that are implausible for the place, season or habitat, stating the ecological reason" as work that rests on knowing the place. The fitness-for-use decision is a judgment about a decision, not a statistic.

## Competencies to build next

Targets (agent draft): **L2 at journey, L3 at senior**.

| Competency | Why now |
|---|---|
| Design and steward field reference data for Earth-observation and AI models *(emerging; distinguishing)* | The role's core product |
| Ground-truth remote-sensed, modelled and AI-generated outputs in the field *(emerging; distinguishing)* | Blind collection and mismatch coding |
| Adjudicate automated species detections using field-formed identification expertise *(emerging)* | Review queues |
| Build task-specific evaluation sets and benchmark AI tools before adoption *(emerging)* | Reference sets labelled blind |
| Calibrate field observers and run field measurement quality assurance | Observer agreement against tolerances |
| Evaluate model fitness-for-purpose and validate against independent evidence | Fitness-for-use decisions |
| Design monitoring and sampling for valid environmental inference | Sample design |

## Entry paths and formation

No one enters this role directly. People arrive from field technician (R02), monitoring and data technician (R03) or geospatial analyst (R04) work, carrying formed identification, measurement or mapping judgment. That makes the role a **downstream test of the entry pipeline**. If seasonal and entry field openings stay scarce [V1-04; V1-14], fewer people will have the field grounding it needs. The pathway's senior step adds formation of others: evaluating observers and capturing site-specific knowledge from departing staff before it leaves. FS's no-regret move NR-4 treats ground truth as infrastructure (reference plots, labelled datasets, calibrated assessor pools) because every AI, Earth-observation and digital measurement system depends on it (`scenarios.md` §8.3, [J]).

## Pathways in and out (exploratory, not recommended)

- **In, field resource technician (R02) → this role (upskill):** five steps, covering reference-data design and collection with an analyst (one observed labelled-sample campaign), observer calibration and sampling design (one blind re-measurement of a crew sample), fitness-for-use decisions, formation of others and knowledge continuity, and briefing the accountable official on what the validation supports ("no model without a decision owner"). About 200 hours over 12 months, mostly field time and mentoring [J]. Seasonal reference-data campaigns shared across agencies might supply field exposure where single programmes lack plots [S].
- **In (role links, no pathway authored yet):** from R03 and R04.
- **Out:** none recorded. The role is too new.

None of these has been tested against observed moves (ADR-0023 §5).

## What you can do now

- **Supervisor or programme scientist.** Name who owns validation for each remote or AI product your programme relies on, and whether that person ever goes to the field. Keep a reference set that the product vendor has not seen. Ask for the field-coded causes of mismatch, not only an accuracy number.
- **Training officer.** Use the R02-to-R05 sequence to grow the function from inside a technician cohort, without creating a new post first. Include blind re-measurement and observer calibration sessions.
- **HR specialist.** Do not expect a series or class. Describe the duties in existing technician, biologist or data science positions, labelled subject to classification review. If you contract validation out, write data rights and independent field checks into the contract. This is FS's no-regret move NR-6 on intelligent-customer capacity [J].

## Sources

- EMST records: `data/v2/core/roles/seed-R05-ground-truth-validation-steward.yaml`; `data/v2/core/variants/seed-R05-*`; `docs/build/WP-08/generated/change_view/R05-ground-truth-validation-steward.json`; `docs/build/WP-08/generated/federal-series/variants/seed-R05-ground-truth-validation-steward--federal.md`; `docs/build/WP-07/staging/pathways/seed-lc-pw-cor1-field-technician-to-ground-truth-steward.yaml`; `docs/decisions/mvp_role_set.csv`; `docs/research/strategic-foresight/scenarios.md` §8.3. Explorer: `site/_site/roles/r05-ground-truth-validation-steward/`.
- [V1-04; WF-04] Office of Rep. Joe Neguse, 2026-03-23, https://neguse.house.gov/media/press-releases/neguse-huffman-press-us-forest-service-answers-staffing-levels-ahead-summer
- [V1-14; WF-05] National Parks Traveler, 2025-11-10, https://www.nationalparkstraveler.org/2025/11/analysis-conservation-job-postings-shows-significant-decrease-during-2025
- [BLS-02] BLS OOH, Environmental Science and Protection Technicians (2025–35), https://www.bls.gov/ooh/life-physical-and-social-science/environmental-science-and-protection-technicians.htm
