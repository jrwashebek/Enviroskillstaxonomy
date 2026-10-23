# ADR-0016: Representing DEI- and EJ-labelled content for federal adopters — name by the work, keep the content, filter by instrument

- **Decision point:** DP-15 (DEI/EJ-labelled content)
- **Status:** accepted (mechanism); the **publication stance** of the federal default views is confirmed by the project lead (`questions_for_project_lead.md` Q4)
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** FH, AS, SC, TN, SL, CP, DB, LC, CM
- **Related:** ADR-0003 (naming rule), ADR-0007 (Tribal containers), ADR-0028 (instrument registry)

## Context

- OPM guidance pages carry a banner rescinding DEI- and gender-related guidance; SAF renamed diversity-titled programmes to protect accreditation work [E: AS-008, AS-042]. FH: 5.3.4 "Diversity, equity, and inclusion practices" and possibly 6.7.2 (EJ screening) cannot be federal requirements in 2026 [E: FH-011 for DEI; J for EJ].
- **FH (P-FH open Q4):** applicability flags; keep these items out of federal default profiles.
- **AS (disagreement 8):** keep the content and **name it by the work performed**; leaving the labels risks federal rejection of whole kits; some will read renaming as capitulation.
- **SC (issue 1):** EJ, climate and co-stewardship competencies are federally contested; if federal adopters can filter by venue or instrument, content need not be deleted to remain adoptable.
- **TN:** Tribal relations sit beside DEI in v1 skill area 5.3; Tribal status is political, not demographic, and that placement exposed Tribal programmes to cuts (P-TN-08).
- Deleting the content would misrepresent state, NGO, local and Tribal practice (e.g. state cumulative-impact laws, DB-060; community engagement work) (FH disagreement 6).

## Decision

1. **Keep the content in the core where it meets the evidence standard.** No competency is deleted because its subject is federally disfavoured; none is retained because it is favoured. The evidence rule (two independent sources incl. a demand signal) applies equally.
2. **Name every competency by the work performed — as a uniform rule, not a targeted relabelling.** ADR-0003's naming rule (verb + object + context; no programme or ideology label in titles) applies to all 222 v1 items and every candidate. Examples: v1 6.7.2 "Environmental justice screening and assessment" → "Analyze cumulative burdens and distributional effects of environmental decisions" (merging DB-C52); v1 5.3.4 "DEI practices" → split into "Design accessible, inclusive public engagement and services" (with SC-C06) and "Apply merit-based, job-related practices in recruitment and team management" (with FH-C13, IO-C02); v1 5.3.5 → "Build working partnerships with communities affected by environmental decisions". Programme names (EJ, DEI, Justice40) become **search aliases** (`altLabel`) and L5 instrument links, so users can still find them.
3. **Applicability is computed from instruments, not asserted by flag.** Each competency or task that depends on a contested policy instrument carries a sensitivity edge to that **Instrument** in the L5 registry (e.g. EO revocations, state cumulative-impact statutes, CEQ guidance status). Views compute `venueApplicability` per sector actor and jurisdiction from instrument status. The **federal default profiles** therefore exclude items whose only basis is a rescinded or inactive federal instrument, while state, local, NGO and private views keep them where their own instruments apply.
4. **FH's applicability flag survives as a computed, dated field** (`federalApplicability ∈ {required-basis, permitted, no-current-basis}` with `asOf`), not a stored editorial judgement — so it changes when instruments change, in either direction.
5. **Tribal content is never in a DEI or EJ container.** Skill area 5.3 is split: Tribal government-to-government content moves to Statecraft obligations owed to Tribal nations (ADR-0007, held); cross-cultural communication is reframed as observable cultural humility, separate from DEI and EJ (P-TN-08).
6. **Nonpartisan posture:** EMST supplies no essay content and gives no help with political designations (Schedule Policy/Career) (FH issue for AS and CA).

## Rationale

- Function-based naming is already the general rule for durability (DC-R1) and portability; applying it uniformly removes the reading that renaming is capitulation, because every competency is renamed by the same rule.
- Instrument-based applicability keeps EMST accurate across administrations: the 2025–26 landscape oscillates (rescissions, reconsiderations, injunctions) [E: SC policy_landscape_2026; V2-05, V2-06, V2-07], and a stored flag would go stale as fast as v1's reform flags did.
- Federal adopters get default profiles that a classifier can use tomorrow without rejecting a whole kit; non-federal users lose nothing.

## Consequences

- SC and DE seed the instrument registry with the relevant federal and state instruments; CP's federal views use the computed applicability.
- The companion research project should use the new titles and note the alias mapping (carry-over flag).

## Dissent and trade-offs

- **AS** and others note renaming can be read as capitulation; mitigated by the uniform rule and visible aliases.
- **FH** preferred stored applicability flags; adopted as a computed field instead (stays correct when instruments change).
- **Trade-off named:** federal adoptability and sector completeness are both kept, at the cost of an instrument registry that must be maintained quarterly (P-SC-14).
