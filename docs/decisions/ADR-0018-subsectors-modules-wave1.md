# ADR-0018: Subsector vocabulary, module list, core/module boundary and wave 1

- **Decision point:** DP-17 (subsector module list and wave 1; IA's seven public-lands gap functions)
- **Status:** provisional-pending-verification — the structure is accepted; module partner readiness rests on DB/AS [J] claims about credential bodies and associations, of which V3 has confirmed a subset (SAF, TWS, AFS, SRM, SER, NEHA, ASFPM active; ISSP credentials are issued by GBCI; IEMA is now ISEP) [E: V3-07, V3-08]
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** DB, IA, SL, FC, LC, FH, AS, PS, TN, LM
- **Related:** ADR-0002, ADR-0003 (three-module rule), ADR-0009 (phased federation), ADR-0010 (namespaces); `vocab/subsectors.yaml`, `vocab/modules.yaml`

## Context

v1 covers 11 of DB's 44 subsectors fully, 22 partially and 11 not at all; the "None" set includes drinking water, wastewater, groundwater, hazardous waste, environmental public health, emergency management, marine/coastal and transportation environmental — the largest public environmental workforces outside land management [E: DB-003, `subsector_coverage_map.csv`]. Of DB's 18 high-priority subsectors for federal and state strategy, v1 fully covers 2 [J built on E]. IA's linker found seven public-lands functions with no v1 home — range/grazing, recreation and visitor management, scenery, transportation/roads, minerals and energy authorizations, lands and realty, wilderness stewardship — corroborated by blind gold labels and by clustering of 5,994 low-similarity plan components (e.g. range/livestock 641, motorized recreation/ROS 533, scenic 482, roads 419, minerals 391) [E: IA §5.7]. Accreditation coverage fails outside forestry (ABET environmental engineering 1 of 6 criteria; EHAC 2 of 5) [E: LC-001, LC-002, LC-005].

## Decision

1. **Subsector facet (L0):** DB's **44 subsectors in 9 clusters** (Water W01–W06; Pollution control & materials P01–P06; Environmental health H01–H02; Energy & extractives E01–E05; Climate, resilience & hazards C01–C03; Markets, finance & corporate M01–M02; Lands & living resources L01–L11; Built environment U01–U02; Cross-cutting practice X01–X07), polyhierarchical (P-DB-01).
2. **Cluster X is core practice, not a subsector module:** X01 environmental review and impact assessment, X02 compliance inspection and enforcement, X03 environmental justice and community programmes (named by function per ADR-0016), X04 education, interpretation and communication, X05 research and science, X07 environmental data, geospatial and informatics are enacted in every module. **X06 laboratory** becomes module MOD-18 for the analyst job family, while "generate legally defensible analytical data" is a core competency (three-module rule).
3. **Nineteen modules** (DB's 18 plus laboratory), each a namespace and future stewardship unit:

   | Module | Namespace | Subsectors | Wave |
   |---|---|---|---|
   | MOD-01 Water and wastewater utilities | `water` | W01 W02 W03 | **1** |
   | MOD-02 Water resources, water-quality regulation and watersheds | `waterq` | W04 W05 W06 | **1** |
   | MOD-03 Air quality | `air` | P01 | **1** |
   | MOD-04 Waste, materials and remediation | `waste` | P02 P03 P04 | **1** |
   | MOD-05 Chemicals, pesticides and EHS compliance | `ehs` | P05 P06 | 2 |
   | MOD-06 Environmental public health | `envhealth` | H01 H02 | **1** |
   | MOD-07a Extractives: mining, reclamation, oil and gas, orphan wells | `extract` | E03 E04 | 2 (public-lands minerals authorizations drafted in wave 1 as MOD-11 enactments) |
   | MOD-07b Clean energy, grid and energy management | `energy` | E01 E02 E05 | 2 |
   | MOD-08 Climate mitigation and adaptation | `climate` | C01 C02 | 2 |
   | MOD-09 Emergency management, hazard mitigation and floodplain management | `hazards` | C03 | **1** |
   | MOD-10 Corporate sustainability, ESG and environmental markets | `markets` | M01 M02 | 3 (private-led; PS) |
   | MOD-11 Forests, rangelands, fire and public-lands multiple use | `forest` | L01 L05 L07 (+ roads, grazing; lands-and-realty enactment of core PS-C15) | **1** (v1-seeded) |
   | MOD-12 Fish, wildlife and aquatic resources | `wildlife` | L02 L03 | **1** (v1-seeded) |
   | MOD-13 Marine and coastal | `marine` | L04 | 3 |
   | MOD-14 Working lands, restoration and land conservation | `worklands` | L06 L08 L09 | 2 |
   | MOD-15 Parks, recreation, protected areas and visitor use | `parks` | L10 (+ scenery, wilderness, visitor use) | **1** (pulled forward from DB's wave 3) |
   | MOD-16 Cultural resources and historic preservation | `culture` | L11 | 2 (Tribal content under ADR-0007; NATHPO only via the Tribal Council) |
   | MOD-17 Built environment: urban planning and transportation environmental | `built` | U01 U02 | 2 |
   | MOD-18 Environmental laboratory and analytical services | `lab` | X06 | 2 |

4. **IA's seven public-lands gap functions go to modules, not core** (answers IA open Q6): range/grazing (IA-CC-01, merged with FH-C04, DB-C55, C-LM-03 parts), roads and trails transportation systems (IA-CC-04) → MOD-11; lands and realty (IA-CC-06) merges into the cross-sector core competency PS-C15 ("Negotiate and administer land rights, rights-of-way and realty transactions"), because land-rights work recurs in utilities, transportation, land trusts and energy, with a public-lands realty enactment in MOD-11; recreation and visitor use (IA-CC-02 + C-LM-02), scenery (IA-CC-03), wilderness character (IA-CC-07) → MOD-15; mineral and energy authorizations and reclamation (IA-CC-05) → MOD-07a with an MOD-11 enactment drafted in wave 1.
5. **Water/wastewater operations and environmental public health services are modules (MOD-01, MOD-06), commissioned centrally for the federal/state MVP** (answers SL open Q2), because no steward will be ready in time (ADR-0009).
6. **Core/module boundary:** ADR-0003 G-4 three-module rule. **Home-module rule** for contested competencies: a competency has exactly **one home** — the module whose regulatory regime governs the legal sufficiency of its deliverable — with **enactments** elsewhere; if it passes the three-module test it is core. Applied: smoke management → home MOD-03 (CAA smoke programmes) with MOD-11 enactment; EHP review for disaster recovery → home MOD-09 with core review competency; organizational GHG inventories → **core** (enacted in MOD-03 GHGRP, MOD-08, MOD-10); Section 106 effects review → **core** review competency (used in MOD-09, -11, -15, -16, -17) with THPO coordination held under ADR-0007.
7. **Species identification is core** (LC-C-03 with FC's perceptual-expertise component; used in forestry, wildlife, restoration, range, invasives), with regional and module enactments — answering LC open Q4 for tree and plant identification. Treatment operations → MOD-01; EH operations → MOD-06.
8. **Module-specific demand corpora** are part of each wave-1 module build (P-DB-17): utility and state job postings, state class specs, NPDES and Title V permit conditions, disclosure rules; OpenLMP (≈95% USFS western plans) does not stand in for non-land demand.

## Rationale

- Wave 1 = DB's federal/state wave (MOD-01, -02, -03, -04, -06, -09 plus v1-seeded -11, -12), where federal and state need is high and steward readiness is strong in four of the six non-v1 modules (AWWA/WEF/ABC/ASDWA; SWANA/ASTSWMO/ITRC; NEHA/NACCHO/APHL; IAEM/NEMA/ASFPM) [J: DB]. **MOD-15 is pulled forward** because FH's priority series include 0025 Park Ranger, NPS lost more than a quarter of its staff [E: V1-02], and three of IA's gap functions (recreation/visitor use, scenery, wilderness) have strong plan demand.
- Seeding MOD-11 and MOD-12 from v1 *outside* the core keeps v1's public-lands depth from re-skewing the core (DB §8).
- DB's caveat holds: steward *willingness* is AS's question; readiness is weakest where need is growing (climate, extractives, energy), so central commissioning is required there.

## Consequences

- Wave-1 modules roughly double v1's competency count; acceptable only if the core stays within 120–180 and modules stay out of default HR views (DB disagreement on depth vs simplicity).
- DB's [J] credential and framework rows (DB-020…DB-065) are verified before any module content enters a release (P-DB-16).

## Dissent and trade-offs

- **DB** placed parks in wave 3; the CA moved MOD-15 to wave 1 for federal coverage. **PS** may weigh ESG higher than wave 3; federal ESG disclosure work shrank (SEC rule rescission proposed) while California SB 253 first reports are due 10 Nov 2026 [E: V2-15] — PS's private-sector content enters via core disclosure competencies and private variants in wave 1, the full ESG/markets module in wave 3.
- **Trade-off named:** breadth beyond public lands now versus the authoring load of central commissioning (~1 extra editorial FTE through 2028).

## Amendments

- **2026-10-23 — CR-DB-001 / ADR-0030 §1.3 (CA).**
  - **§2, DB-C53:** "Generate legally defensible analytical data" stays in MOD-18 `lab` (wave 2). The laboratory's task core is performed by one job family under one accreditation regime, whatever module the data serve, so it fails the three-module test. The part that recurs across modules is the data user's, and it is core: field custody and field QC in FC-C24, and review of laboratory data for a decision in v1 2.2.3.
  - **§6:** CI checks the three-module rule. A core practice competency with only one or two module enactments needs a third, its home module, or a row in `data/v2/governance/three_module_exceptions.yaml`. Zero module enactments passes, and recurrence is reported.
  - **MOD-12** gains module candidate DB-C56, harvest regulation and game population management.
