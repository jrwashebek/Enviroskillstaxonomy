# MOD-01 Water and wastewater utilities — module brief (`water`)

**Status:** editorial section authored centrally for wave 1 (ADR-0018; ADR-0009). It is not a stewarded module: no Module Stewardship Agreement exists and no partner is committed. Every record here is an agent draft (`validationStatus: draft`, `reviewStatus: unreviewed`; content evidence label J, ratings S). Nothing here is SME agreement, Delphi retention or job-analysis confirmation.

## Scope

**Subsectors:** W01 Drinking water supply & treatment; W02 Wastewater collection, treatment & water reuse; W03 Stormwater & green infrastructure.

**In scope:** Drinking water treatment and distribution, wastewater collection, treatment and resource recovery, and municipal stormwater programmes and green infrastructure; the operator side of utilities and the regulator side of public water system compliance.

**Out of scope:** Water-quality standards, discharge permit writing, watersheds and groundwater (MOD-02 `waterq`); laboratory accreditation (MOD-18, wave 2); engineering design sealed by a licensed engineer.

**Module competencies (home here):**

- `seed:DB-C01` Operate drinking water treatment processes to meet water quality targets (W01)
- `seed:DB-C02` Operate wastewater treatment and resource-recovery processes to permit limits (W02)
- `seed:DB-C09` Inspect stormwater control measures from construction through long-term maintenance (W03, U02)
- `seed:SL-C06` Assure public water system compliance with drinking water requirements (W01)
- `seed:v1-4.7.1` Install green stormwater infrastructure to design specifications (W03, U01)
- `seed:v1-4.7.3` Manage a municipal stormwater programme to meet permit conditions (W03)

**Competencies enacted here:**

- `seed:v1-1.5.2` Assess climate vulnerability of species, ecosystems, infrastructure and communities [core] — enactment `seed:ena-1.5.2-water`
- `seed:v1-4.1.3` Measure water quality and survey aquatic communities in the field [core] — enactment `seed:ena-4.1.3-water`
- `seed:DB-C03` Supervise automated and AI-assisted process control in environmental operations [core] — enactment `seed:ena-db-c03-water`
- `seed:DB-C05` (planned; not yet authored) [core] — enactment `seed:ena-db-c05-water`
- `seed:DB-C06` Protect operational technology at environmental utilities and facilities [core] — enactment `seed:ena-db-c06-water`
- `seed:DB-C21` Investigate and manage emerging contaminants across media [core] — enactment `seed:ena-db-c21-water`
- `seed:DB-C26` Manage a regulated facility's environmental compliance system and obligations calendar [core] — enactment `seed:ena-db-c26-water`
- `seed:DB-C29` Communicate environmental and health risks under uncertainty [core] — enactment `seed:ena-db-c29-water`
- `seed:DC-CAND-04` Engineer environmental sensor-network and streaming data pipelines [core] — enactment `seed:ena-dc-cand-04-water`
- `seed:FC-C16` Collect trace-level and genetic environmental samples without contamination [core] — enactment `seed:ena-fc-c16-water`
- `seed:FC-C24` Manage field sample custody and field quality control [core] — enactment `seed:ena-fc-c24-water`
- `seed:PS-C09` Build organizational and jurisdictional greenhouse gas inventories for disclosure and reporting [core] — enactment `seed:ena-ps-c09-water`
- `seed:SC-C12` Track regulatory change and translate it into operating guidance [core] — enactment `seed:ena-sc-c12-water`
- `seed:SC-C14` Operate within, or oversee, delegated and assumed regulatory programs [core] — enactment `seed:ena-sc-c14-water`
- `seed:SL-C03` Conduct regulatory compliance inspections [core] — enactment `seed:ena-sl-c03-water`
- `seed:SL-C10` Provide compliance and technical assistance to regulated entities and local governments [core] — enactment `seed:ena-sl-c10-water`
- `seed:SL-C12` Administer environmental financial assistance to local governments [core] — enactment `seed:ena-sl-c12-water`

**Roles served (`docs/decisions/mvp_role_set.csv`):** R24 Drinking water programme analyst; R25 Water and wastewater treatment operator; R22 Environmental engineer; R37 Facility environmental compliance specialist; R03 Monitoring and data technician.

## Licensure and credential gates

Gates are Credential records on tasks and role variants, never proficiency levels (ADR-0003 T-8). Register records are WP-07's (`data/v2/registers/credentials/`).

| Gate | Issuer | Verification |
|---|---|---|
| Drinking water treatment and distribution operator certification, graded by system classification | State certification programmes; standardized exams and need-to-know criteria from Water Professionals International (formerly ABC) in many states | verified [E: V3-08; SL-E29] |
| Wastewater treatment and collection operator certification | State certification boards; WPI exams in many states | verified [E: V3-08] |
| Operator in responsible charge (sign-off authority) | State law; recorded as `signOffAuthority: licensure` on tasks | [J] |
| Professional Engineer for design | State engineering boards | unverified [J: DB-CR-007] |
| Erosion and stormwater credentials (CPESC; CPSWQ, CESSWI) | EnviroCert International | CPESC verified [E: V3-08]; others unverified [J] |

## Candidate advisory partners (*candidate*, not committed)

Partners below are **candidates** from DB and AS research (`vocab/modules.yaml`; `docs/research/domain-bench/module_steward_candidates.csv`). None is committed; the commitment register (`data/v2/registers/commitments.csv`) is the only source of committed status. Readiness is DB's [J] rating.

*Candidate:* AWWA; WEF; Water Professionals International (formerly ABC; exam criteria); state operator certification boards; NRWA/RCAP (small systems); ASDWA (review); EPA Office of Water (federal partner). Readiness: Strong [J].

## Demand corpus to build (ADR-0018 §8; P-DB-17)

Utility and state job postings; operator need-to-know criteria and exam blueprints (may be proprietary: AS/IA to negotiate use); state class specifications; consumer confidence reports; sanitary survey forms.

## Open issues

- Licensure may stretch time-to-certify if automation removes hands-on tasks [S; confirm with certification-board data].
- Core DB-C05 (asset management) and PS-C09 (greenhouse gas inventories) are planned but not yet authored: the enactments here point at their seed keys (`W-REF-PENDING`). DB-C06 (operational-technology security) is not yet authored; its enactment is listed in the WP-06 worklog for wiring.

*Generated by `docs/build/WP-06/build_briefs.py` from the records; record lists are computed, not typed. Licence: CC BY 4.0 (narrative, ADR-0013).*
