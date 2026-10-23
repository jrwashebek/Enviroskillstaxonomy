# MOD-02 Water resources, water-quality regulation and watersheds — module brief (`waterq`)

**Status:** editorial section authored centrally for wave 1 (ADR-0018; ADR-0009). It is not a stewarded module: no Module Stewardship Agreement exists and no partner is committed. Every record here is an agent draft (`validationStatus: draft`, `reviewStatus: unreviewed`; content evidence label J, ratings S). Nothing here is SME agreement, Delphi retention or job-analysis confirmation.

## Scope

**Subsectors:** W04 Water resources, hydrology & water supply planning; W05 Groundwater & hydrogeology; W06 Surface water quality regulation, watershed & wetland programs.

**In scope:** Water resources, hydrology and supply planning, groundwater and source-water protection, surface water-quality regulation (load allocations, discharge permits, certifications), wetlands and compensatory mitigation, and stream assessment.

**Out of scope:** Utility operations (MOD-01 `water`); marine and coastal management (MOD-13, wave 3); laboratory analysis (MOD-18).

**Module competencies (home here):**

- `seed:DB-C08` Develop pollutant load allocations and watershed restoration plans for impaired waters (W06)
- `seed:DB-C10` Plan water supply and allocation under hydrologic uncertainty (W04, W05)
- `seed:DB-C11` Characterize groundwater systems and protect drinking water sources (W05, W01, P04)
- `seed:DB-C47` Administer compensatory mitigation programmes for aquatic resources and habitat (W06, M02, L02)
- `seed:FC-C06` Delineate wetlands and other aquatic resources in the field (W06)
- `seed:FC-C07` Assess stream channel form and function in the field (W06, L08)

**Competencies enacted here:**

- `seed:v1-4.1.3` Measure water quality and survey aquatic communities in the field [core] — enactment `seed:ena-4.1.3-waterq`
- `seed:DB-C25` Target inspections and verify compliance using monitoring data and analytics [core] — enactment `seed:ena-db-c25-waterq`
- `seed:DB-C52` Analyze cumulative burdens and distributional effects of environmental decisions [core] — enactment `seed:ena-db-c52-waterq`
- `seed:DC-CAND-03` Design monitoring and sampling for valid environmental inference [core] — enactment `seed:ena-dc-cand-03-waterq`
- `seed:FC-C01` Deploy, maintain and verify field sensor networks [core] — enactment `seed:ena-fc-c01-waterq`
- `seed:FC-C02` Ground-truth remote-sensed, modelled and AI-generated outputs in the field [core] — enactment `seed:ena-fc-c02-waterq`
- `seed:FC-C11` Apply field biosecurity and decontamination protocols [core] — enactment `seed:ena-fc-c11-waterq`
- `seed:FC-C12` Operate small boats and work safely on water in aquatic, coastal and marine field settings [core] — enactment `seed:ena-fc-c12-waterq`
- `seed:FH-C01` Assess effects on protected species and conduct interagency consultation on proposed actions [core] — enactment `seed:ena-fh-c01-waterq`
- `seed:SC-C14` Operate within, or oversee, delegated and assumed regulatory programs [core] — enactment `seed:ena-sc-c14-waterq`
- `seed:SL-C02` Issue environmental permits and resource-use authorizations as the deciding authority [core] — enactment `seed:ena-sl-c02-waterq`
- `seed:SL-C03` Conduct regulatory compliance inspections [core] — enactment `seed:ena-sl-c03-waterq`
- `seed:SL-C04` Develop and resolve environmental enforcement cases [core] — enactment `seed:ena-sl-c04-waterq`

**Roles served (`docs/decisions/mvp_role_set.csv`):** R17 Hydrologist; R11 Environmental permit writer; R12 Environmental compliance inspector; R09 Restoration and land stewardship project lead; R23 Enforcement case manager.

## Licensure and credential gates

Gates are Credential records on tasks and role variants, never proficiency levels (ADR-0003 T-8). Register records are WP-07's (`data/v2/registers/credentials/`).

| Gate | Issuer | Verification |
|---|---|---|
| Professional Wetland Scientist / Wetland Professional in Training | Society of Wetland Scientists Professional Certification Program | verified [E: V3-08] |
| Professional Geologist licence | State geology boards (ASBOG exams) | unverified [J: DB-CR-015] |
| Professional Hydrologist | American Institute of Hydrology | unverified [J: DB-CR-014] |
| Certified Ground Water Professional; water well contractor licence | NGWA; state agencies | unverified [J] |
| Professional Engineer | State engineering boards | unverified [J] |

## Candidate advisory partners (*candidate*, not committed)

Partners below are **candidates** from DB and AS research (`vocab/modules.yaml`; `docs/research/domain-bench/module_steward_candidates.csv`). None is committed; the commitment register (`data/v2/registers/commitments.csv`) is the only source of committed status. Readiness is DB's [J] rating.

*Candidate:* ACWA (state clean water administrators); the state wetland managers' association (current name to verify); SWS Professional Certification Program; AIH; NGWA; EPA Office of Water, USGS and USACE Regulatory (federal partners). Readiness: Moderate [J].

## Demand corpus to build (ADR-0018 §8; P-DB-17)

State permit-writer and water-quality class specifications; discharge permit fact sheets and conditions; load-allocation reports; mitigation bank instruments; state water-rights decisions.

## Open issues

- The regulated-waters definition is still proposed (L5 `seed:ins/wotus-definition`); delineation and dredge-and-fill content is written jurisdiction-neutral [E: V2].
- Discharge permit writing is the SL-C02 `waterq` enactment (absorbs DB-C07), not a module competency (ADR-0018).

*Generated by `docs/build/WP-06/build_briefs.py` from the records; record lists are computed, not typed. Licence: CC BY 4.0 (narrative, ADR-0013).*
