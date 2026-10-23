# How this role is changing: Monitoring and data technician

*EMST v2 role-change brief · `seed:R03-monitoring-data-technician` · corridor COR-1 · as of 2026-10-23 · CC BY 4.0 · draft awaiting WP-15 sign-off*

> **Read this first.** The task list, time shares, flags, target levels and change claims below are **agent drafts** (evidence S). No job analysis or SME panel has reviewed them. No task has a multi-rater v2 change assessment, so every change below is **assessment pending**. No change indicator has moved: every linked signal is at *watch*. Use this brief to describe and develop the role. It is not a classification basis or a job analysis, and it is not for selection, RIF or rating decisions. [How to read these briefs](README.md).

## Who does this work

Monitoring and data technicians install, service and verify sensor networks, collect samples under custody and quality-assure monitoring data from collection to release. The draft describes a role whose work is moving from manual collection to verifying automated data streams and adjudicating automated flags.

| | |
|---|---|
| **Sector actors** (editorial) | **Federal:** hydrologic and physical science technicians in science centres (advisor or researcher, no decision authority). **State:** ambient monitoring units producing data for regulatory programmes (regulator). **Local:** utility and stormwater monitoring for permit compliance (regulated party). **Private:** consulting and laboratory field services (service provider; adds hazardous-site decontamination). **Tribal:** variant held (ADR-0007). |
| **Typical titles** | Environmental monitoring technician; field data technician; hydrologic technician |
| **Federal series** | 1316 Hydrologic Technician and 1311 Physical Science Technician (`narrowMatch`, active); 0404 Biological Science Technician (`relatedMatch`). 0029 Environmental Protection Assistant (`relatedMatch`) is active under its current code and **proposed** for realignment to 0303. The proposal is not final [V1-10; FED-04]. Indicative band: GS-3 to GS-5 entry; GS-6 to GS-7 journey; GS-8 to GS-9 senior. This is not a classification criterion. |
| **State class examples** | No class is mapped yet in the pilot jurisdictions (PA, TX, WA; one county environmental health department; one municipal utility). The role's targets are what a jurisdiction would crosswalk its own class against. |

## The work today (agent draft)

| Task | Share of time | Flags |
|---|---|---|
| Service deployed sensors on schedule: clean, recalibrate, replace, log | 8.7% | C E F |
| Install soil moisture, temperature and weather sensors, recording siting conditions | 5.9% | E F |
| Run side-by-side checks between sensors and a reference instrument, recording offsets | 5.9% | C E F |
| Collect representative grab water samples under custody | 5.9% | C E F |
| Measure water-quality parameters in place with calibrated meters | 5.9% | E F |
| Apply range, consistency and completeness checks to incoming records | 5.9% | C E |
| Review automated flags against field and instrument records | 5.9% | C |

## What is changing

| Work | Change (agent draft) | Driver | Evidence status |
|---|---|---|---|
| Service deployed sensors | Transforming: networked sensors multiply, and field time moves from manual collection to servicing and verifying instruments | sensing tech | Assessment pending. Watch: federal environmental bureaus' registered AI use cases in water and hydrology, 2025 inventory (reliability A) [V4-15; OMB-01] |
| Review automated flags | Transforming, compressing first-pass QC: automated checks apply the first flags, and the technician adjudicates them against field and instrument records | AI, automation | Assessment pending |
| **Audit automated flags: measure false-flag and missed-error rates** | **Emerging** | AI | Assessment pending |
| **Configure automated QC on streaming feeds** (senior) | **Emerging:** moves to senior technicians | sensing tech | Assessment pending |
| Manual data entry | **Declining:** telemetry and mobile capture reduce it | sensing tech, automation | Assessment pending |
| Grab sampling under custody | Stable: not compressed, and kept as a formation task | none | Assessment pending |

Context, not evidence of skill change: BLS projects +7% for environmental science and protection technicians over 2025–35, against +3.5% for all occupations [BLS-01; BLS-02]. Hydrologic technician projections have not yet been read (`CHANGE_SIGNALS.md` §5.4).

## What stays human, and why

This describes where the work sits today. Automated QC can flag a value, but the draft gives three judgments to the technician: whether a flag is a real fault or a real event, read against field and instrument records; when telemetry and field cues justify an unscheduled visit or a manual sample; and when siting bias (shading, sediment burial, animal disturbance) means a sensor must move. Each of these needs knowledge of the site and the instrument. Manual grab samples and meter readings stay in routine practice as the reference every sensor is checked against.

## Competencies to build next

Targets (agent draft): entry / journey / senior.

| Competency | Targets | Why now |
|---|---|---|
| Deploy, maintain and verify field sensor networks *(emerging; distinguishing)* | L1 / L2 / L3 | Most field time goes to instruments |
| Assure the quality of environmental data from collection to release *(distinguishing)* | L1 / L2 / L3 | Flag adjudication and audits |
| Engineer environmental sensor-network and streaming data pipelines | – / L2 / L3 | Streaming QC configuration |
| Validate AI-generated work products before professional use *(emerging)* | L1 / L2 / L2 | Data and AI floor (ADR-0025) |
| Record provenance and AI involvement in work products | L1 / L2 / L2 | Raw, flagged and corrected data versioned separately |
| Collect trace-level and genetic samples without contamination *(emerging)* | L1 / L2 / L3 | Emerging-contaminant and eDNA work |
| Calibrate field observers and run field measurement QA | senior L3 | Hot checks alongside crews |

## Entry paths and formation

People reach this role from field technician work, and the formation still happens in the field: installing sensors, taking grab samples under custody, and making side-by-side checks against reference instruments. The risk the WP-07 provisions guard against is a technician who adjudicates automated flags without ever having found the errors by hand. In the upskilling pathway, **one month of automated flags is reviewed by hand**, with false-flag and missed-error rates reported, before automated flagging is credited. **Manual meter readings at every service visit** stay in place as the reference. Fewer field entry openings upstream (see the R02 brief) also mean fewer people arriving with that grounding [V1-04; V1-14].

## Pathways in and out (exploratory, not recommended)

- **In, field resource technician (R02) → this role (upskill):** three observed sensor installations; manual meter readings at each service visit; one month of flags reviewed by hand; five observed grab-sampling events with zero custody defects; the data and AI floor. About 160 hours over 6 months, and state-approved continuing-education hours may count [J].
- **Out:** the role profile links onward to the ground-truth and validation steward (R05) and the environmental compliance inspector (R12). WP-07 has not yet authored a pathway for these links. R12's inspector onboarding pathway includes grab sampling and a manual audit of a facility's monitoring reports that transfer directly.

None of these has been tested against observed moves (ADR-0023 §5).

## What you can do now

- **Supervisor.** Require a hand review of a sample of automated flags each quarter and report false-flag and missed-error rates. Keep raw, flagged and corrected data as separate versions. Make the decision to send someone for an unscheduled visit explicit and record the trigger.
- **Training officer.** Sequence training as installation, then servicing, then flag review, then QC configuration. Hold automated-QC credit until the by-hand review is done. Use seeded-error batches as drills.
- **HR specialist.** For federal positions, compare duties with the 1316 and 1311 Federal Series Profiles. Treat 0029 as its current series, because realignment to 0303 is proposed, not decided [V1-10]. For state and local positions, crosswalk your class specification against the role's targets, since no pilot-state class is mapped yet. Any selection use needs your own job analysis [SEL-02].

## Sources

- EMST records: `data/v2/core/roles/seed-R03-monitoring-data-technician.yaml`; `data/v2/core/variants/seed-R03-*`; `docs/build/WP-08/generated/change_view/R03-monitoring-data-technician.json`; `docs/build/WP-08/generated/federal-series/{1316,1311,0404,0029}.md`; `docs/build/WP-08/generated/state-class/variants/seed-R03-*`; `docs/build/WP-07/staging/pathways/seed-lc-pw-cor1-field-technician-to-monitoring-data-technician.yaml`. Explorer: `site/_site/roles/r03-monitoring-data-technician/`.
- [V1-04; WF-04] Office of Rep. Joe Neguse, 2026-03-23, https://neguse.house.gov/media/press-releases/neguse-huffman-press-us-forest-service-answers-staffing-levels-ahead-summer
- [V1-10; FED-04] OPM CHCO memo (proposed realignment), 2026-04-24, https://www.opm.gov/chcoc/latest-memos/modernization-and-consolidation-of-occupational-series.pdf
- [V1-14; WF-05] National Parks Traveler, 2025-11-10, https://www.nationalparkstraveler.org/2025/11/analysis-conservation-job-postings-shows-significant-decrease-during-2025
- [V4-15; OMB-01] OMB 2025 Federal Agency AI Use Case Inventory, https://github.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory
- [BLS-01; BLS-02] BLS Employment Projections 2025–35 (2026-08-27), https://www.bls.gov/news.release/ecopro.nr0.htm; OOH, Environmental Science and Protection Technicians, https://www.bls.gov/ooh/life-physical-and-social-science/environmental-science-and-protection-technicians.htm
- [SEL-02] 5 CFR part 300, https://www.ecfr.gov/current/title-5/chapter-I/subchapter-B/part-300
