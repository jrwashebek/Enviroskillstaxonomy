# How this role is changing: Monitoring and data technician

*EMST v2 role-change brief · field and data corridor · as of 23 October 2026 · CC BY 4.0*

> **Status: draft for NGO-pilot preview (2026-10-23).** AI agents checked facts against sources, and some claims await
> register rows. Not yet reviewed by independent human experts. Date-sensitive statements will be re-checked before
> external release.
>
> **A first draft for your staff to correct:** written by AI agents and not yet checked by practitioners. Nothing here is
> a measurement, and nothing here is for classifying positions or for selecting, rating or removing anyone.
> [How to read these briefs](README.md).

## Who does this work

Monitoring and data technicians install, service and verify sensor networks, collect samples under custody and
quality-assure monitoring data from collection to release. The draft describes a role whose work is expected to move
from manual collection toward verifying automated data streams and adjudicating automated flags.

| | |
|---|---|
| **Employer types** | **Federal:** hydrologic and physical science technicians in science centers (advisor or researcher, no decision authority). **State:** ambient monitoring units producing data for regulatory programs (regulator). **Local:** utility and stormwater monitoring for permit compliance (regulated party). **Private:** consulting and laboratory field services (service provider; adds hazardous-site decontamination). |
| **Typical titles** | Environmental monitoring technician; field data technician; hydrologic technician |
| **Federal series** | 1316 Hydrologic Technician and 1311 Physical Science Technician (more specific series; active); 0404 Biological Science Technician (partial fit). 0029 Environmental Protection Assistant (partial fit) is active under its current code and **proposed** for realignment to 0303; the proposal is not final [1]. Indicative band: GS-3 to GS-5 entry; GS-6 to GS-7 journey; GS-8 to GS-9 senior. This is not a classification criterion. |
| **State class examples** | No class is mapped yet in the jurisdictions whose public class plans EMST read (a sample of states, one county environmental health department and one municipal utility; no agency has been involved). The draft targets below are what a jurisdiction would compare its own class against. |

## The work today (agent draft)

Main tasks, in rough work order. This is a selection; EMST shows no time shares.

| Task | Formation task |
|---|---|
| Install soil moisture, temperature and weather sensors, recording siting conditions | yes |
| Service deployed sensors on schedule: clean, recalibrate, replace, log | yes |
| Run side-by-side checks between sensors and a reference instrument, recording offsets | yes |
| Collect representative grab water samples under custody | yes |
| Measure water-quality parameters in place with calibrated meters | yes |
| Apply range, consistency and completeness checks to incoming records | |
| Review automated flags against field and instrument records | |

## What is expected to change

| Work | Expected change (agent draft) | Driver | Outside signal (every task change: assessment pending) |
|---|---|---|---|
| Service deployed sensors | Transforming: as networked sensors multiply, field time would move from manual collection to servicing and verifying instruments | sensing technology | Water and hydrology: 36 registered AI use cases in eleven federal environmental units, 10 deployed (2025 inventory, EMST keyword classification; reliability A) [2] |
| Review automated flags | Transforming, compressing first-pass quality control: automated checks would apply the first flags, and the technician would adjudicate them against field and instrument records | AI, automation | none yet |
| **Audit automated flags: measure false-flag and missed-error rates** | **Emerging** | AI | none yet |
| **Configure automated quality control on streaming feeds** (senior) | **Emerging:** expected to move to senior technicians | sensing technology | none yet |
| Manual data entry | **Declining:** telemetry and mobile capture reduce it | sensing technology, automation | none yet |
| Grab sampling under custody | Stable: not compressed, and kept as a formation task | — | none yet |

Of the role's 32 draft tasks, the other 26 carry no drafted change claim. Context, not evidence of skill change: BLS
projects 7% growth for environmental science and protection technicians over 2025–35, against 3.5% for all occupations
[3]. EMST has not yet read the hydrologic technician projection.

## What stays with people, and why

This describes where the work sits today. Automated checks can flag a value, but the draft gives three judgments to the
technician: whether a flag is a real fault or a real event, read against field and instrument records; when telemetry
and field cues justify an unscheduled visit or a manual sample; and when siting bias (shading, sediment burial, animal
disturbance) means a sensor must move. Each needs knowledge of the site and the instrument. Manual grab samples and
meter readings stay in routine practice as the reference every sensor is checked against. The role blends field craft
and data craft.

## Competencies to build next

Draft targets by level, entry / journey / senior (agent draft; design statements to test, not findings).

| Competency | Draft targets | Why now |
|---|---|---|
| Deploy, maintain and verify field sensor networks *(emerging)* | Supervised / Independent / Senior | Most field time goes to instruments |
| Assure the quality of environmental data from collection to release | Supervised / Independent / Senior | Flag adjudication and audits |
| Engineer environmental sensor-network and streaming data pipelines | — / Independent / Senior | Streaming quality-control configuration |
| Validate AI-generated work products before professional use *(emerging)* | Supervised / Independent / Independent | Basic data and AI skills every EMST role includes |
| Record provenance and AI involvement in work products | Supervised / Independent / Independent | Raw, flagged and corrected data kept as separate versions |
| Collect trace-level and genetic samples without contamination *(emerging)* | Supervised / Independent / Senior | Emerging-contaminant and eDNA work |
| Calibrate field observers and run field measurement quality assurance | senior: Senior | Hot checks alongside crews |

## Entry paths and formation

People reach this role from field technician work, and the formation still happens in the field: installing sensors,
taking grab samples under custody, and making side-by-side checks against reference instruments. The formation
provisions in EMST's draft pathways guard against a technician who adjudicates automated flags without ever having found
the errors by hand. In the upskilling pathway, **one month of automated flags is reviewed by hand**, with false-flag and
missed-error rates reported, before automated flagging is credited. **Manual meter readings at every service visit**
stay in place as the reference. Fewer field entry openings upstream (see the field technician brief) also mean fewer
people arriving with that grounding.

## Pathways in and out (exploratory, not recommended)

- **In, field resource technician → this role (upskill):** three observed sensor installations; manual meter readings
  at each service visit; one month of flags reviewed by hand; five observed grab-sampling events with zero custody
  defects; the basic data and AI skills. EMST's curriculum draft estimates about 160 hours over 6 months, and
  state-approved continuing-education hours may count [J].
- **Out:** the role profile links onward to the ground-truth and validation steward and to the environmental compliance
  inspector, but no pathway has been drafted for these links yet. The inspector onboarding pathway includes grab
  sampling and a manual audit of a facility's monitoring reports, both of which transfer directly.

None of these has been tested against observed career moves.

## What you can do now

- **Supervisor.** Require a hand review of a sample of automated flags each quarter and report false-flag and
  missed-error rates. Keep raw, flagged and corrected data as separate versions. Make the decision to send someone for
  an unscheduled visit explicit, and record the trigger.
- **Training officer.** Sequence training as installation, then servicing, then flag review, then quality-control
  configuration. Hold automated-flagging credit until the by-hand review is done. Use seeded-error batches as drills.
- **HR specialist.** For federal positions, compare duties with the explorer's 1316 and 1311 Federal Series Profiles.
  Treat 0029 as its current series, because realignment to 0303 is proposed, not decided [1]. For state and local
  positions, compare your class specification with the draft targets, since no sample-state class is mapped yet. Any
  selection use needs your own job analysis under 5 CFR 300.103 [4].
- **Educator.** Make one month of hand-reviewed automated flags, with false-flag and missed-error rates reported, part
  of a monitoring course, and keep manual meter readings as the reference in every field lab.

## Sources

1. U.S. Office of Personnel Management (CHCO memo), *Modernization and Consolidation of Occupational Series* (proposed),
   24 April 2026. https://www.opm.gov/chcoc/latest-memos/modernization-and-consolidation-of-occupational-series.pdf
2. Office of Management and Budget, *2025 Federal Agency AI Use Case Inventory* (README as of 13 April 2026), with EMST's
   keyword classification of the eleven environmental units' records.
   https://github.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory
3. U.S. Bureau of Labor Statistics, *Employment Projections 2025–2035*, 27 August 2026,
   https://www.bls.gov/news.release/ecopro.nr0.htm; Occupational Outlook Handbook, Environmental Science and Protection
   Technicians, https://www.bls.gov/ooh/life-physical-and-social-science/environmental-science-and-protection-technicians.htm
4. 5 CFR part 300 (eCFR compilation; OPM interim final rule 91 FR 48236, 31 July 2026).
   https://www.ecfr.gov/current/title-5/chapter-I/subchapter-B/part-300

---

**Who wrote this.** Researched and drafted by a team of AI agents (Anthropic's Claude), each given a specialist role,
working to a charter set by the EMST project lead. AI agents checked the facts against sources in October 2026. No
independent human expert has reviewed this brief yet. Role names used in EMST's records are AI agent roles, not
people.

**Comment or correct.** To comment, correct an error or ask about the pilot, open an issue at
[github.com/jrwashebek/Enviroskillstaxonomy/issues](https://github.com/jrwashebek/Enviroskillstaxonomy/issues).

*Technical note.* Role key `R03-monitoring-data-technician` in the EMST v2 data release. Claims-register rows behind the
sources: [1] FED-04; [2] OMB-02, RPT-28; [3] BLS-01, BLS-02; [4] SEL-02. Pathway: the field-technician-to-monitoring
record (exploratory).
