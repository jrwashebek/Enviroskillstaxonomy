# MOD-04 Waste, materials and remediation — module brief (`waste`)

**Status:** editorial section authored centrally for wave 1 (ADR-0018; ADR-0009). It is not a stewarded module: no Module Stewardship Agreement exists and no partner is committed. Every record here is an agent draft (`validationStatus: draft`, `reviewStatus: unreviewed`; content evidence label J, ratings S). Nothing here is SME agreement, Delphi retention or job-analysis confirmation.

## Scope

**Subsectors:** P02 Solid waste, recycling & materials management; P03 Hazardous waste & materials management; P04 Contaminated sites & remediation.

**In scope:** Solid waste collection, processing and disposal; producer responsibility and materials management; hazardous waste determination and generator compliance; contaminated-site assessment, remedy selection and long-term stewardship; transaction due diligence; regulation of solid waste facilities.

**Out of scope:** Chemicals and pesticide regulation and facility-wide EHS management (MOD-05, wave 2); emergency hazardous-materials response beyond the core field-safety practice.

**Module competencies (home here):**

- `seed:DB-C16` Operate solid waste collection, processing and disposal systems to permit conditions (P02)
- `seed:DB-C17` Administer extended producer responsibility and materials-management programmes (P02, M01) — lifecycle emerging
- `seed:DB-C18` Determine hazardous waste status and manage generator compliance (P03, P06)
- `seed:DB-C19` Conduct environmental site assessment and site characterization (P04, W05)
- `seed:DB-C20` Select remedies for contaminated sites and oversee cleanup through long-term stewardship (P04)
- `seed:PS-C13` Conduct environmental due diligence for property transactions (P04)
- `seed:SL-C14` Regulate solid waste and materials management facilities (P02)
- `seed:v1-3.7.1` Develop materials-management strategies that keep products and materials in use (P02, M01)
- `seed:v1-3.7.2` Plan and run waste reduction programmes for facilities and communities (P02)
- `seed:v1-3.7.5` Conduct material flow analysis for facilities, supply chains and regions (P02)

**Competencies enacted here:**

- `seed:v1-6.7.1` Assess human health risks from environmental exposures [core] — enactment `seed:ena-6.7.1-waste`
- `seed:DB-C03` Supervise automated and AI-assisted process control in environmental operations [core] — enactment `seed:ena-db-c03-waste`
- `seed:DB-C06` Protect operational technology at environmental utilities and facilities [core] — enactment `seed:ena-db-c06-waste`
- `seed:DB-C21` Investigate and manage emerging contaminants across media [core] — enactment `seed:ena-db-c21-waste`
- `seed:DB-C25` Target inspections and verify compliance using monitoring data and analytics [core] — enactment `seed:ena-db-c25-waste`
- `seed:DB-C26` Manage a regulated facility's environmental compliance system and obligations calendar [core] — enactment `seed:ena-db-c26-waste`
- `seed:DB-C29` Communicate environmental and health risks under uncertainty [core] — enactment `seed:ena-db-c29-waste`
- `seed:DB-C52` Analyze cumulative burdens and distributional effects of environmental decisions [core] — enactment `seed:ena-db-c52-waste`
- `seed:FC-C14` Operate and supervise uncrewed and automated field systems [core] — enactment `seed:ena-fc-c14-waste`
- `seed:FC-C16` Collect trace-level and genetic environmental samples without contamination [core] — enactment `seed:ena-fc-c16-waste`
- `seed:FC-C24` Manage field sample custody and field quality control [core] — enactment `seed:ena-fc-c24-waste`
- `seed:PS-C09` Build organizational and jurisdictional greenhouse gas inventories for disclosure and reporting [core] — enactment `seed:ena-ps-c09-waste`
- `seed:SC-C12` Track regulatory change and translate it into operating guidance [core] — enactment `seed:ena-sc-c12-waste`
- `seed:SC-C14` Operate within, or oversee, delegated and assumed regulatory programs [core] — enactment `seed:ena-sc-c14-waste`
- `seed:SL-C02` Issue environmental permits and resource-use authorizations as the deciding authority [core] — enactment `seed:ena-sl-c02-waste`
- `seed:SL-C03` Conduct regulatory compliance inspections [core] — enactment `seed:ena-sl-c03-waste`
- `seed:SL-C04` Develop and resolve environmental enforcement cases [core] — enactment `seed:ena-sl-c04-waste`
- `seed:SL-C10` Provide compliance and technical assistance to regulated entities and local governments [core] — enactment `seed:ena-sl-c10-waste`
- `seed:SL-C12` Administer environmental financial assistance to local governments [core] — enactment `seed:ena-sl-c12-waste`

**Roles served (`docs/decisions/mvp_role_set.csv`):** R27 Remediation project manager; R29 Solid waste and materials management specialist; R37 Facility environmental compliance specialist; R11 Environmental permit writer; R12 Environmental compliance inspector; R23 Enforcement case manager.

## Licensure and credential gates

Gates are Credential records on tasks and role variants, never proficiency levels (ADR-0003 T-8). Register records are WP-07's (`data/v2/registers/credentials/`).

| Gate | Issuer | Verification |
|---|---|---|
| Certified Hazardous Materials Manager | IHMM | verified [E: V3-08] |
| Hazardous waste operations and emergency response training (entry gate) | Employer-provided under the federal worker-protection standard; register record `seed:crd-hazwoper` (WP-07) | [J: DB-CR-024] |
| Licensed site professional opinions (state privatized cleanup programmes) | State licensing boards | unverified [J: DB-CR-031] |
| Environmental professional for all appropriate inquiries (regulatory definition, not issued) | Federal definition | [J: DB-CR-032] |
| Landfill and solid waste facility operator certification; association certifications | State programmes; SWANA | unverified [J: DB-CR-027, DB-CR-028] |

## Candidate advisory partners (*candidate*, not committed)

Partners below are **candidates** from DB and AS research (`vocab/modules.yaml`; `docs/research/domain-bench/module_steward_candidates.csv`). None is committed; the commitment register (`data/v2/registers/commitments.csv`) is the only source of committed status. Readiness is DB's [J] rating.

*Candidate:* SWANA; ASTSWMO (state waste and cleanup officials); ITRC (under ECOS); IHMM; state LSP/LSRP boards; EPA OLEM, DoD and DOE cleanup programmes (federal partners). Readiness: Strong [J].

## Demand corpus to build (ADR-0018 §8; P-DB-17)

State cleanup and solid waste programme postings; consulting job architectures; producer responsibility programme plans; remedy decision documents; facility permits.

## Open issues

- v1 3.7.1 and 3.7.5 were rewritten from corporate business-model and tool framing; technology names moved to L4.
- Producer responsibility (DB-C17) is lifecycle `emerging`: state programmes are in first implementation cycles.

*Generated by `docs/build/WP-06/build_briefs.py` from the records; record lists are computed, not typed. Licence: CC BY 4.0 (narrative, ADR-0013).*
