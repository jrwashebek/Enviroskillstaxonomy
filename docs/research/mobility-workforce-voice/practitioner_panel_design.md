# Workforce Voice & Cross-Sector Practitioner Panel: Design for the Real Panel

**Role:** CM · **Date:** 2026-10-23 · **Status:** proposal for CA and AS decision; budget figures are [J] placeholders for AS.

**Why this document exists.** During Phase 2 an AI agent simulates the Workforce Voice panel. It may synthesise published
evidence and design protocols. It must never claim to speak for practitioners (CM-002 §3). This is the design for the
**real** panel that replaces the simulation, and for how its judgement binds the project. The charter is explicit:
practitioners' answer to "does this help me?" outweighs internal elegance (CM-001). The design makes that answer a
**decision right**, not a consultation courtesy.

---

## 1. Purpose and decision rights

The panel has four jobs:
1. **Test the theory of change against real careers.** Supply career histories that validate or refute pathway predictions (metric M-03) and expose frictions (M-02).
2. **Judge usefulness.** Run and score the "does this help me?" tests (M-06, M-07).
3. **Hold the gates.** Ratify or block expansion gates G1 and G2 (M-28).
4. **Guard against misuse.** Run a standing channel for misuse reports (M-11) and red-team new features.

**Binding mechanisms** [J]:
- **Usefulness veto at G1.** If any stratum's M-06 pass rate is below threshold, G1 cannot close. CA may override only with a written decision-log entry that answers the panel's objection point by point. That entry is published to the panel and requires a second panel vote; a failed vote escalates to the project lead.
- **Stratum quorum.** Gate votes need a majority *within every stratum* (§2), so a well-represented group cannot outvote early-career, seasonal or corps members.
- **Practitioner objection.** Any five members, or any one stratum, can file an objection to a design decision. CA must respond in writing within 15 working days, and the objection and response are recorded in `docs/decisions/`.
- **Co-signed thresholds.** The panel co-signs the numeric thresholds in `metrics_framework.csv` before the pilot starts. This prevents moving the goalposts later.
- **Delphi seats.** The panel holds reserved seats in IO's Delphi (§5.4), and their ratings are reported separately as well as pooled.

---

## 2. Composition and representation targets

**Size.** 28 standing members plus up to 8 rotating subsector seats (DB's modules). [J: large enough for ≥3 per stratum and
for stratum-level voting; small enough to meet as one group.]

| Stratum | Standing seats | Who | Notes |
|---|---|---|---|
| S-A Cross-actor movers | 5 | People who moved at least once between federal, state, local, Tribal, NGO, private or academic employers in the last 10 years | At least one move in each direction across the public/private line. At least one move *into* a field-craft role (the hardest direction; report §3.3) |
| S-B Federal and state staff in transition | 5 | Displaced, reassigned, deferred-resignation, RIF-affected or reorganized staff (2025–26), including at least 2 from field roles and 1 from fire | The 2025–26 displacement is the largest evidenced mobility event (CM-028) |
| S-C Early-career (≤5 years) | 4 | Recent graduates, technicians, people who never got a first job | Include at least 1 without a 4-year degree and 1 who left the field |
| S-D Conservation corps alumni | 3 | Alumni of state, local and national corps, at least 1 from a term cut in 2025 | Recruit via The Corps Network and member corps (CM-031) |
| S-E Seasonal and wildland fire workforce | 3 | Seasonal technicians, wildland firefighters (federal, state, contract), collateral-duty red-card holders | Recruit via firefighter advocacy organisations and unions |
| S-F Employee organisations | 3 | Union and employee-association representatives (federal and state) | Speak for organisations, not as individuals. Recorded separately |
| S-G HR, training and curriculum intermediaries | 3 | State HR classification analyst, federal training officer, corps or community-college programme lead | They decide whether the tool reaches workers |
| S-H Tribal natural-resource professionals | 2 (reserved) | Filled **only** through TN's protocol | Seats stay empty rather than be filled outside the protocol. Tribal members may decline any agenda item |

**Cross-cutting targets** (across all strata) [J]:
- **Sector actors.** At least 2 members currently employed by each of federal, state, local, NGO, private and academic employers. Tribal participation follows TN's protocol.
- **Subsector.** No more than 40% from forestry, fire and public lands combined. At least 30% from water/wastewater, air, waste and remediation, energy and utilities, environmental health, ESG or climate (DB's modules).
- **Geography.** At least 40% rural or duty-station-bound members. At least 3 census regions.
- **Demography.** Aim to reflect or exceed the sector's diversity benchmarks (Green 2.0's data could not be accessed this session, CM-061). Report composition annually.
- **Without a 4-year degree.** At least 5 members overall.
- **Veterans.** At least 2 members, because veterans' preference is a live friction and 27.9% of federal staff are veterans (CM-028).

---

## 3. Recruitment

- **Channels.** Corps networks (The Corps Network, state corps; CM-031); federal and state employee unions and associations;
  firefighter advocacy organisations; professional societies (forestry, wildlife, fisheries, water, environmental health,
  planning); early-career and diverse-professional networks; community colleges and land-grant extension; state workforce
  boards (SL's lane); and, for Tribal seats, only through TN.
- **Open call plus targeted outreach.** The open call alone over-recruits the already-networked [J].
- **Selection.** A stratified selection from applicants by a selection committee (CM, AS, one external evaluator). Stratum targets
  are filled first. Ties are broken by lottery to reduce network bias [J].
- **Accessibility.** Phone and mobile participation. No requirement for video or a work email. Materials meet Section 508 (CP).
  Sessions are scheduled around field seasons: fire and field strata are **not** asked to meet June–September except
  asynchronously [J].

## 4. Compensation and constraints

- **Pay everyone for their time** at a professional rate, with an annual stipend plus per-session payments. Tie it to time, not
  outcomes [J; AS to budget].
- **Federal and state employees.** Accepting payment or serving in an official capacity may be restricted by ethics rules. Members
  may need to participate in a personal capacity, on personal time, or with supervisor approval. CP must clear the arrangement
  before recruitment [J; flagged as an issue outside my area]. Offer non-cash alternatives (donation, training credit) where pay is
  barred.
- **Employee-organization reps** sit as organisational representatives. Their organisation decides about payment.
- **Cover costs.** Travel, connectivity and childcare for any in-person session.

## 5. Methods and cadence

| Method | What it answers | Cadence | Linked metric |
|---|---|---|---|
| 5.1 Career-history interviews (critical-incident technique on each move: trigger, search, barriers, what was recognised, what was lost) | A2, A4, A5; observed transitions for validation; friction register | All members in year 1; new members on joining | M-02, M-03 |
| 5.2 Diary studies (4–6 weeks during a real job search, reskilling or work transfer) | Whether the tool is used at the moment of decision; trust; articulation gain | Twice a year, 8–12 volunteers | M-09, M-12 |
| 5.3 Moderated usability sessions with think-aloud on persona tasks (`personas.md`) | "Does this help me?" pass/fail by stratum | Every release candidate | M-06, M-07 |
| 5.4 Delphi seats (IO's design) | Validity of role profiles, craft weights and pathway plausibility from lived experience | Per Delphi round | IO metrics; M-04 context |
| 5.5 Card sorts and language tests (craft names, role titles, competency wording across actors) | Whether the shared language is understood by people outside the project | Before views are designed | — |
| 5.6 Sensemaking workshops on metrics and gate evidence | Panel judgement on G1/G2 | Before each gate | M-28 |
| 5.7 Misuse red-teaming | A11 risks; policy wording | Before any person-level feature ships; annually | M-11 |
| 5.8 Institutional-knowledge capture pilot (structured handover interviews with departing or transferred staff, co-designed with S-B and S-F) | Knowledge continuity; tests the candidate competency CC-CM-01 | Year 1 with 2–3 partner units | M-22 |

**Standing cadence.** One plenary per quarter (virtual, 2 hours). Monthly asynchronous rounds. One in-person convening per year
outside fire season.

## 6. Conflict of interest, anonymity and protection

- **Disclosures.** Each member discloses their employer, vendor relationships, consulting work, and any stake in workforce
  products. Members recuse from votes on features where they have a commercial stake.
- **Anonymity by default.** Members choose whether to be named publicly. Anything published from their testimony is
  de-identified. Quotes appear only with explicit, revocable consent. No employer receives individual-level data.
- **Protection from retaliation.** Federal and state staff in transition may fear consequences. Sessions are not recorded unless
  every participant consents. Notes are pseudonymised. Members can submit anonymous written input through a channel CM does not
  control (e.g. a third-party evaluator) [J].
- **Human-subjects review.** Career-history interviews and diary studies are human-subjects research if results are published.
  Run them under an IRB or equivalent review with informed consent and data-retention limits. Use trauma-informed interviewing,
  because displacement is distressing [J].
- **Data minimisation.** Career histories used for pathway validation are stored at the minimum grain needed (role, actor,
  dates, location bucket), separately from identity, with deletion on request (CP to specify).

## 7. Handover from the simulated panel

1. The real panel's first task is to **review and rewrite `personas.md`**: discard composites that ring false and add missing
   ones.
2. The second is to **co-sign or change** the gate thresholds in `metrics_framework.csv`.
3. Every simulated-voice claim in CM's Phase 2 outputs carries a label. The panel marks each one *confirmed*, *corrected* or
   *rejected*. Rejected claims are withdrawn from the repo with a decision-log entry.

## 8. Budget sketch (for AS) [J]

Roughly 28 members × (annual stipend + ~10 sessions), plus diary-study incentives, a facilitator, an external evaluator, IRB
fees and one convening. AS should cost this against the evaluation budget. A practitioner panel is cheaper than a failed
federal rollout.
