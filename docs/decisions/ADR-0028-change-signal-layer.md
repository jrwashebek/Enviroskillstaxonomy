# ADR-0028: The change-signal layer — signal records, the evidence rule, the instrument registry, and horizon scanning

- **Decision point:** DP-27 (new; CA) — L5 design; what moves a role's change indicator; replacing the reform flags; scanning cadence and decision rights
- **Status:** accepted
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** LM, FS, SC, IA, SL, FH, FC, DC, DB, TN, CP, DE, AS
- **Related:** ADR-0008, ADR-0015, ADR-0016 (venue applicability), ADR-0019 (linker quality), ADR-0021

## Context

v1's six reform flags are dated, US-federal, reversible events stored as timeless Booleans on 129 of 222 competencies; three stored summaries disagree; the flags miss judicial review, scope, delegation, agreements, disclosure and fiscal mechanisms; outside NEPA they are the wrong regime entirely [E: audit §9; SC §6.5; DB §3.9]. The charter's living-system goal needs continuous intake that does not let posting noise or fiscal shocks masquerade as skill change (LM, FC).

## Decision

### 1. Signal records (`ChangeSignal`, L5)

Fields (merging LM §6.3, IA §7 and FS's coding): target type and ID (task, competency, role variant, tool, instrument); measure, value, unit, CI95, n, denominator, baseline; observed and comparison periods; geography; sector actor; source ID and release; corpus version, SHA-256 and licence; method and tool/prompt version; crosswalk path and **weakest match type**; `linkerQuality`; direction ∈ {augment, automate, new, grow, decline, stable, reshape}; direction confidence; **driver tags** ∈ {AI, sensing-tech, automation-robotics, policy-reform, fiscal, demographic, climate, market, workforce-capacity}; STEEP+V category; novelty; source reliability A–D; corroboration count; priority score = impact × reliability × (novelty + corroboration); `careFlag`/`tribalPrograms`; personal-data flag (must be false); evidence label (S until reviewed); review status; reviewer; `reviewBy`; status ∈ {watch, active, retired}.

### 2. The evidence rule — what may move a role's change indicator (P-LM-07, LM §7 Q3)

A signal moves a computed change indicator only if: (1) **two independent signal families** point the same way (families: capability, observed use, deployment, postings or PDs, headcount, plan requirements, worker report; two indices on the same data family count as one); (2) **persistence** for two consecutive periods, or one period plus a registered deployment; (3) a traceable crosswalk path with minimum match type **close** (partial matches can raise only a watch); (4) a declared base and **driver tag** (fiscal and policy shocks are tagged so they do not masquerade as AI effects); (5) **named human review**. Otherwise `status = watch`: shown in the "what's coming" view, not moving the indicator. **No indicator may rest on a single vendor's data** (ADR-0008 §4).

### 3. Instrument registry and driver events (replacing the reform flags; P-SC-02)

- **`Instrument`** (L5 registry): statute, rule, EO, OMB memo, court decision, permit programme, agreement authority, disclosure regime, state HR order; jurisdiction; status.
- **`DriverEvent`**: `eventType ∈ {introduced, passed-chamber, enacted, proposed, interim, final, effective, enjoined, stayed, vacated, remanded, rescinded, decided, expired, sunset}`, date, jurisdiction, `mechanismIds`, direction ∈ {expands, contracts, reshapes}, status after, sources, evidence label, recorded by, `reviewBy`.
- **Mechanisms** (L0; SC's 16 durable driver mechanisms incl. DM-16 workforce capacity): tasks link to mechanisms through **sensitivity edges** asserted once with evidence; instruments link to mechanisms; competency and role sensitivity is **computed** ("affected by instrument changes in the last 12 months").
- **Seeds:** v1's six flags as frozen historical seed events with provenance; SC's 34 instruments (`policy_landscape_2026.csv`), updated by V2 (CEQ NEPA rule removal final 8 Jan 2026; DOI NEPA Handbook, not "516 DM 1"; Seven County 8–0 judgment with a 5-justice majority opinion; SPEED Act passed House, pending in Senate EPW; ESA "harm" rescission final, effective 14 Sep 2026, litigated; GHG endangerment rescission final, effective 20 Apr 2026, litigated; WOTUS still proposed; CEQ data standard v1.2; Section 106 NPRM at OIRA; SB 253 first reports due 10 Nov 2026; SB 261 enjoined; Omnibus I in force 18 Mar 2026) [E: V2-01–V2-16]; TN's dated Tribal-policy events (P-TN-15) **under the Tribal gate**; FC's drone and seasonal-hiring events (P-FC-20); SL's state events (skills-based hiring orders, SEPA amendments, delegation and assumption changes; P-SL-06); FH's OPM issuances (P-FH-02); module stewards' regime events (P-DB-11).
- **State HR events count as L5 signals** (answers SL open Q5): they update friction and crosswalk records directly and count as the *policy* family toward role change indicators, but cannot alone move a skill-change indicator.
- **Quarterly instrument-registry refresh** from the Federal Register, CRS, Congress.gov, court dockets and state registers, with a named steward and `reviewBy` on every sensitivity edge (P-SC-14).

### 4. Standing demand signals

- **Plan requirements** (OpenLMP and successors; P-LM-08): monitoring questions and standards by theme and method; rule-era trend analyses; extend to BLM RMPs, state wildlife action plans, TMDLs, NPDES permits and state forest plans. **Weighting** (answers LM open Q6): headline series weight **each plan equally** (components normalized within plan); component-weighted series are published as a sensitivity check (Idaho Panhandle 2022 alone supplies 29% of monitoring components).
- **Postings and PDs** (P-LM-09): an October 2026 USAJOBS and state-board baseline snapshot for core series; quarterly duties-text diffs via IA's pipeline; federal posting *volume* treated as a policy signal.
- **Federal AI use-case inventory** (annual; P-DC-11) and **OPM Federal Workforce Data** (monthly; FWD replaced FedScope in Jan 2026 [E: V1-16]) for deployment stage, headcount, accessions, under-30 share and trainee series (entry-path health; P-FH-12).
- **Official projections** (annual): BLS Employment Projections **2025–35** (released Aug 27 2026), including BLS's new AI exposure categories, ingested as an external `ChangeSignal` source by SOC and as an external-index comparator for ADR-0008; the 2024–34 projections are superseded and are not cited as current [E: V4].
- **Data continuity:** DE snapshots and mirrors critical external series (OPM FWD, NIFC, agency AI inventories, OpenLMP releases) with provenance, because public datasets can be discontinued (FS issue).

### 5. Horizon scanning (FS protocol, P-FS-07; AS sentinel network, P-AS-12)

- **Cadence:** continuous machine intake (IA); event-triggered rapid review within 10 working days; monthly human scan and two-page digest; **quarterly triage panel** (FS chair, IA, a rotating FC/DC/SC lead, a DB expert, a sentinel representative, CM; TN or the Tribal Council for Tribal signals); **annual Signals Review** feeding the April MINOR; scenario refresh every 3 years or after a wildcard. Starts at v2.0, not after the Delphi.
- **Decision rights:** the triage panel routes signals and proposes changes; the CA (Phase 4) / Editorial Board decides lifecycle changes in L1–L4; IO validates promotions to `established`; the Tribal Council clears any `careFlag` signal; machine-coded signals stay `machine-coded` until a human validates them; 10% of signals double-coded each quarter (κ ≥ 0.6).
- **Sentinels:** 60–90 practitioners, **stratified and compensated** (each sector actor 8–30%; each craft ≥ 25%; early-career ≥ 25%); channels carried from v1 (fire and fire intelligence; permitting) plus water; air and environmental health; disclosure and markets; state and local; workforce pipeline; a Tribal channel only as the Tribal Council governs it.
- **Year-five floor:** ~0.3 FTE foresight, ~0.2 FTE skills intelligence, 30 sentinels and quarterly triage (FS §8).

## Rationale

Sixteen durable mechanisms joined to dated instruments keep competencies from going stale when instruments change, which is exactly how v1's flags failed within a year (SC disagreement 1). The two-family rule resolves LM's and FS's tension: FS's early lifecycle states use corroboration across signal types; indicator movement needs LM's stronger standard.

## Dissent and trade-offs

- **SC:** a second, maintained layer must rejoin durable competencies to the instrument fluency employers hire on (views do this); acceptable only if P-SC-14 has an owner — named in the build plan.
- **LM vs FS:** false positives vs late detection — `watch`, `lapsed` and `reviewBy` limit false-positive cost.
- **TN:** the Tribal channel exists only on Tribal terms; Tribal workforce change will be under-measured by design.

## Amendments

- **2026-10-23 — CR-LM-001, CR-LM-003 / ADR-0029 §8, §10 (CA).**
  - **Signal fields (§1).** §1 gains `signalFamily`, `independenceKey`, `registeredDeployment`, `impact`, `scenarioSignposts[]`, `pointsToward[]` and measure `baseline`/`sensitivity`; `status` is renamed `signalStatus`. `signalFamily` and a listed `independenceKey` are required for `active` signals.
  - **Policy family (§2–§3).** `policy` counts toward role-change indicators only; `projection` and `workload` never count. "Single vendor" is enforced through the provider table in `vocab/change_types.yaml#independence_keys`.
  - **Driver events (§3).** They gain `submitted-for-review`, a vocabulary for `statusAfter` (incl. `under-review`) and the instrument type `agency-order`.
  - **Targets.** An occupation is not a target type: occupation-grain signals attach through X3. Government organizations may be targets; Tribal ones never may (V3).
  - **Rule and lane.** The evidence rule is registered as `vocab/rules/change-indicator@1.0.0.yaml`. The WP-10 write lane is ratified.

- **2026-10-23 — CR-SC-001 / ADR-0030 §1.4 (CA).**
  - **§3:** a link from an enactment or role variant to an Instrument carries a role (`vocab/driver_mechanisms.yaml#instrument_link_roles`). The role belongs to the link, not to the instrument, because one rule can require one actor's work and remove another's (LM).
  - `DriverEvent.actingInstrument` names the instrument that caused an event. Revoked and revoking instruments stay separate records.
  - Tasks may carry sensitivity edges, but only task-specific ones: inherited edges are computed.
