# MOD-03 Air quality — module brief (`air`)

**Status:** editorial section authored centrally for wave 1 (ADR-0018; ADR-0009). It is not a stewarded module: no Module Stewardship Agreement exists and no partner is committed. Every record here is an agent draft (`validationStatus: draft`, `reviewStatus: unreviewed`; content evidence label J, ratings S). Nothing here is SME agreement, Delphi retention or job-analysis confirmation.

## Scope

**Subsectors:** P01 Air quality management.

**In scope:** Ambient monitoring and data quality, emissions inventories and modelling for attainment planning, stationary-source permitting and inspection (as enactments of core competencies), and smoke management for prescribed and managed fire.

**Out of scope:** Mobile-source engineering; greenhouse gas markets (MOD-10, wave 3); climate mitigation planning (MOD-08, wave 2).

**Module competencies (home here):**

- `seed:DB-C13` Operate ambient air monitoring networks to regulatory quality-assurance criteria (P01)
- `seed:DB-C14` Build emissions inventories and air quality models for attainment planning (P01, C01)
- `seed:DB-C15` Plan smoke management for prescribed and managed fire within air quality requirements (P01, L07)

**Competencies enacted here:**

- `seed:v1-6.7.1` Environmental health risk assessment [core] — enactment `seed:ena-6.7.1-air`
- `seed:DB-C03` Supervise automated and AI-assisted process control in environmental operations [core] — enactment `seed:ena-db-c03-air`
- `seed:DB-C25` Target inspections and verify compliance using monitoring data and analytics [core] — enactment `seed:ena-db-c25-air`
- `seed:DB-C26` Manage a regulated facility's environmental compliance system and obligations calendar [core] — enactment `seed:ena-db-c26-air`
- `seed:DB-C52` Analyze cumulative burdens and distributional effects of environmental decisions [core] — enactment `seed:ena-db-c52-air`
- `seed:DC-CAND-03` Design monitoring and sampling for valid environmental inference [core] — enactment `seed:ena-dc-cand-03-air`
- `seed:DC-CAND-04` Engineer environmental sensor-network and streaming data pipelines [core] — enactment `seed:ena-dc-cand-04-air`
- `seed:DC-CAND-12` Build, run and validate environmental forecast and scenario systems [core] — enactment `seed:ena-dc-cand-12-air`
- `seed:FC-C01` Deploy, maintain and verify field sensor networks [core] — enactment `seed:ena-fc-c01-air`
- `seed:FC-C24` Manage field sample custody and field quality control [core] — enactment `seed:ena-fc-c24-air`
- `seed:PS-C09` (planned; not yet authored) [core] — enactment `seed:ena-ps-c09-air`
- `seed:SC-C12` Track regulatory change and translate it into operating guidance [core] — enactment `seed:ena-sc-c12-air`
- `seed:SC-C14` Operate within, or oversee, delegated and assumed regulatory programs [core] — enactment `seed:ena-sc-c14-air`
- `seed:SL-C02` Issue environmental permits and resource-use authorizations as the deciding authority [core] — enactment `seed:ena-sl-c02-air`
- `seed:SL-C03` Conduct regulatory compliance inspections [core] — enactment `seed:ena-sl-c03-air`
- `seed:SL-C04` Develop and resolve environmental enforcement cases [core] — enactment `seed:ena-sl-c04-air`
- `seed:SL-C10` Provide compliance and technical assistance to regulated entities and local governments [core] — enactment `seed:ena-sl-c10-air`

**Roles served (`docs/decisions/mvp_role_set.csv`):** R28 Air quality specialist; R03 Monitoring and data technician; R07 Fuels and prescribed fire specialist; R11 Environmental permit writer; R12 Environmental compliance inspector; R37 Facility environmental compliance specialist.

## Licensure and credential gates

Gates are Credential records on tasks and role variants, never proficiency levels (ADR-0003 T-8). Register records are WP-07's (`data/v2/registers/credentials/`).

| Gate | Issuer | Verification |
|---|---|---|
| Visible-emissions observer certification (reference opacity method), renewed every six months | Accredited smoke schools | unverified [J: DB-CR-019] |
| Qualified source testing individual / observer | Stack testing accreditation body (to verify) | unverified [J: DB-CR-020] |
| Accredited greenhouse gas verifier (state programme) | State air agency (e.g. California) | unverified [J: DB-CR-021] |
| Professional Engineer for some permits | State engineering boards | unverified [J] |

## Candidate advisory partners (*candidate*, not committed)

Partners below are **candidates** from DB and AS research (`vocab/modules.yaml`; `docs/research/domain-bench/module_steward_candidates.csv`). None is committed; the commitment register (`data/v2/registers/commitments.csv`) is the only source of committed status. Readiness is DB's [J] rating.

*Candidate:* NACAA; AAPCA; A&WMA; EPA Air Pollution Training Institute curricula as a federal partner, whose 2025-26 operating status could not be confirmed [E: DB-ECO-012, not-found]. Readiness: Moderate [J].

## Demand corpus to build (ADR-0018 §8; P-DB-17)

State and local air agency postings and class specifications; operating and construction permit conditions; state implementation plan submittals; monitoring network plans.

## Open issues

- v1 6.7.5 was split here; its three task seeds were moved from `core/` to `modules/air/` with their successors (DB-C13, DB-C14).
- The federal greenhouse gas reporting programme is under reconsideration (L5 `seed:ins/ghgrp-reconsideration`); facility-reporting content is regime-neutral.

*Generated by `docs/build/WP-06/build_briefs.py` from the records; record lists are computed, not typed. Licence: CC BY 4.0 (narrative, ADR-0013).*
