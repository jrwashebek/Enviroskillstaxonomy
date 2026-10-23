# MOD-11 Forests, rangelands, fire and public-lands multiple use — module brief (`forest`)

**Status:** editorial section authored centrally for wave 1 (ADR-0018; ADR-0009). It is not a stewarded module: no Module Stewardship Agreement exists and no partner is committed. Every record here is an agent draft (`validationStatus: draft`, `reviewStatus: unreviewed`; content evidence label J, ratings S). Nothing here is SME agreement, Delphi retention or job-analysis confirmation.

## Scope

**Subsectors:** L01 Forestry; L05 Rangeland management; L07 Wildland fire.

**In scope:** Silviculture, inventory, stand projection, forest health, management and harvest planning, timber sale and stewardship agreements, certification conformance, wildland fire suppression, prescribed fire, fuels, fire behaviour and intelligence, post-fire stabilization, rangeland monitoring and grazing, resource roads, and the public-lands minerals enactment.

**Out of scope:** Restoration practice and invasive species control as such (core); working lands and private-landowner programmes (MOD-14, wave 2, except the early draft FH-C03); smoke-management decisions by air regulators (home MOD-03 `air`).

**Module competencies (home here):**

- `seed:FC-C08` Monitor rangeland condition with calibrated field indicators (L05)
- `seed:FH-C02` Prepare and administer timber sale, stewardship and partner implementation agreements (L01, L08)
- `seed:FS-C05` Fuse multi-source fire intelligence into operational decision support (L07) — lifecycle emerging
- `seed:IA-CC-01` Plan, authorize and monitor livestock grazing on shared rangelands (L05)
- `seed:IA-CC-04` Plan, maintain and decommission resource road and trail transportation systems (L01, U02)
- `seed:PS-C23` Manage forests to certification-scheme standards (L01)
- `seed:v1-1.3.1` Prescribe and implement silvicultural treatments for stand objectives (L01)
- `seed:v1-1.3.2` Inventory forest resources to stated precision with field plots and remote sensing (L01)
- `seed:v1-1.3.3` Project stand development under alternative treatments with calibrated growth models (L01)
- `seed:v1-1.3.4` Assess forest health and diagnose biotic and abiotic stressors (L01)
- `seed:v1-1.3.5` Plan forest management and timber harvests to meet ecological and economic objectives (L01)
- `seed:v1-4.3.1` Suppress wildland fire safely with ground tactics and resources (L07)
- `seed:v1-4.3.2` Conduct prescribed fire from burn planning through ignition, holding and evaluation (L07, L01, L05)
- `seed:v1-4.3.3` Design fuels treatments that reduce wildfire hazard and verify their effects in the field (L07, L01)
- `seed:v1-4.3.4` Predict fire behaviour from fuels, weather and topography for operations and planning (L07)
- `seed:v1-4.3.5` Stabilize burned areas after wildfire from field assessment of burn severity and values at risk (L07, L01)

**Competencies enacted here:**

- `seed:v1-1.4.3` Identify organisms from field characters, specimens, images and recordings [core] — enactment `seed:ena-1.4.3-forest`
- `seed:v1-1.5.2` Assess climate vulnerability of species, ecosystems, infrastructure and communities [core] — enactment `seed:ena-1.5.2-forest`
- `seed:v1-4.2.2` Detect, treat and monitor invasive species in the field [core] — enactment `seed:ena-4.2.2-forest`
- `seed:v1-5.1.3` Environmental interpretation [core] — enactment `seed:ena-5.1.3-forest`
- `seed:v1-6.2.3` Prepare and revise management plans for publicly held lands [core] — enactment `seed:ena-6.2.3-forest`
- `seed:DB-C05` (planned; not yet authored) [core] — enactment `seed:ena-db-c05-forest`
- `seed:DB-C15` Plan smoke management for prescribed and managed fire within air quality requirements [air] — enactment `seed:ena-db-c15-forest`
- `seed:DB-C50` Review effects of proposed actions on historic properties and resolve them through consultation [core] — enactment `seed:ena-db-c50-forest`
- `seed:DC-CAND-12` Build, run and validate environmental forecast and scenario systems [core] — enactment `seed:ena-dc-cand-12-forest`
- `seed:FC-C02` Ground-truth remote-sensed, modelled and AI-generated outputs in the field [core] — enactment `seed:ena-fc-c02-forest`
- `seed:FC-C03` Adjudicate automated species detections using field-formed identification expertise [core] — enactment `seed:ena-fc-c03-forest`
- `seed:FC-C11` Apply field biosecurity and decontamination protocols [core] — enactment `seed:ena-fc-c11-forest`
- `seed:FC-C14` Operate and supervise uncrewed and automated field systems [core] — enactment `seed:ena-fc-c14-forest`
- `seed:FC-C21` Work alongside landowners, permittees, volunteers and communities on the land [core] — enactment `seed:ena-fc-c21-forest`
- `seed:FC-C26` Assess tree risk and structural condition [core] — enactment `seed:ena-fc-c26-forest`
- `seed:FC-C31` Calibrate field observers and run field measurement quality assurance [core] — enactment `seed:ena-fc-c31-forest`
- `seed:FH-C01` Assess effects on protected species and conduct interagency consultation on proposed actions [core] — enactment `seed:ena-fh-c01-forest`
- `seed:IA-CC-05` Administer mineral and energy authorizations and reclamation [extract] — enactment `seed:ena-ia-cc-05-forest`
- `seed:SC-C08` Design and administer cross-jurisdictional stewardship agreements [core] — enactment `seed:ena-sc-c08-forest`
- `seed:SL-C02` Issue environmental permits and resource-use authorizations as the deciding authority [core] — enactment `seed:ena-sl-c02-forest`
- `seed:SL-C08` Conduct environmental impact review of proposed actions [core] — enactment `seed:ena-sl-c08-forest`

**Roles served (`docs/decisions/mvp_role_set.csv`):** R14 Forester; R06 Wildland fire operations (crew to supervisor); R07 Fuels and prescribed fire specialist; R08 Fire intelligence analyst (continuous operations); R18 Rangeland management specialist; R34 Intergovernmental stewardship agreement manager; R02 Field resource technician.

## Licensure and credential gates

Gates are Credential records on tasks and role variants, never proficiency levels (ADR-0003 T-8). Register records are WP-07's (`data/v2/registers/credentials/`).

| Gate | Issuer | Verification |
|---|---|---|
| Wildland fire position qualifications (crew to burn boss and analyst positions) | USWFS-USFS aligned federal qualification standards effective January 2027; NWCG standards updated January 2026 | verified [E: V3-13] |
| SAF Certified Forester | Society of American Foresters | verified [E: V3-08] |
| State registered or licensed forester; state certified prescribed burn manager | State boards and forestry agencies (minority of states) | unverified [J: DB-CR-072, DB-CR-082] |
| Certified Professional in Rangeland Management | SRM | unverified [J: DB-CR-075] |
| ISA Certified Arborist (tree risk) | International Society of Arboriculture | verified [E: V3-08] |
| Remote pilot certificate for uncrewed aircraft | Federal aviation authority | unverified [J: DB-CR-091] |

## Candidate advisory partners (*candidate*, not committed)

Partners below are **candidates** from DB and AS research (`vocab/modules.yaml`; `docs/research/domain-bench/module_steward_candidates.csv`). None is committed; the commitment register (`data/v2/registers/commitments.csv`) is the only source of committed status. Readiness is DB's [J] rating.

*Candidate:* SAF and SRM (verified active [E: V3-07]); NASF (state foresters); USWFS/USFS training organizations with NWCG as reviewer. Readiness: Strong [J].

## Demand corpus to build (ADR-0018 §8; P-DB-17)

OpenLMP plan components (strong for this module: range, roads, minerals, smoke [E: IA §5.7; DB-011]); federal and state forester and fire position descriptions; certification audit reports.

## Open issues

- TN-C06 is held under ADR-0007 §D and is not authored or described here; TN drafts only.
- IA-CC-05 is an early draft homed in `extract` (wave 2); its public-lands enactment and tasks live here (ADR-0018 s.4).
- Protect suggestions (v1 1.3.2, 4.3.2) are listed for the Editorial Board, not set (ADR-0015).
- Lands and realty is core PS-C15 with a public-lands enactment planned here; PS-C15 is not yet authored.

*Generated by `docs/build/WP-06/build_briefs.py` from the records; record lists are computed, not typed. Licence: CC BY 4.0 (narrative, ADR-0013).*
