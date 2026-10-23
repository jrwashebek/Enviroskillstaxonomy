#!/usr/bin/env python3
"""Write the one-page module briefs in docs/modules/ (WP-06). Prose per module is below; every list of records
(competencies, enactments, roles) is generated from data/v2 and docs/decisions/mvp_role_set.csv, never typed."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import emstlib as L  # noqa: E402

DATA = REPO / "data" / "v2"
OUTDIR = REPO / "docs" / "modules"

SUBS = {t["notation"]: t["prefLabel"] for t in L.load_yaml(REPO / "vocab" / "subsectors.yaml")["terms"]}
MODS = {t["namespace"]: t for t in L.load_yaml(REPO / "vocab" / "modules.yaml")["terms"]}
ROLES = {r["role_key"].split("-")[0]: r for r in csv.DictReader(open(REPO / "docs" / "decisions" / "mvp_role_set.csv", encoding="utf-8"))}

COMMON_STATUS = (
    "**Status:** editorial section authored centrally for wave 1 (ADR-0018; ADR-0009). It is not a stewarded module: "
    "no Module Stewardship Agreement exists and no partner is committed. Every record here is an agent draft "
    "(`validationStatus: draft`, `reviewStatus: unreviewed`; content evidence label J, ratings S). Nothing here is SME "
    "agreement, Delphi retention or job-analysis confirmation.")

PARTNER_NOTE = ("Partners below are **candidates** from DB and AS research (`vocab/modules.yaml`; "
                "`docs/research/domain-bench/module_steward_candidates.csv`). None is committed; the commitment register "
                "(`data/v2/registers/commitments.csv`) is the only source of committed status. Readiness is DB's [J] rating.")

BRIEF = {
    "water": dict(
        scope_in="Drinking water treatment and distribution, wastewater collection, treatment and resource recovery, and municipal stormwater programmes and green infrastructure; the operator side of utilities and the regulator side of public water system compliance.",
        scope_out="Water-quality standards, discharge permit writing, watersheds and groundwater (MOD-02 `waterq`); laboratory accreditation (MOD-18, wave 2); engineering design sealed by a licensed engineer.",
        roles=["R24", "R25", "R22", "R37", "R03"],
        gates=[
            ("Drinking water treatment and distribution operator certification, graded by system classification", "State certification programmes; standardized exams and need-to-know criteria from Water Professionals International (formerly ABC) in many states", "verified [E: V3-08; SL-E29]"),
            ("Wastewater treatment and collection operator certification", "State certification boards; WPI exams in many states", "verified [E: V3-08]"),
            ("Operator in responsible charge (sign-off authority)", "State law; recorded as `signOffAuthority: licensure` on tasks", "[J]"),
            ("Professional Engineer for design", "State engineering boards", "unverified [J: DB-CR-007]"),
            ("Erosion and stormwater credentials (CPESC; CPSWQ, CESSWI)", "EnviroCert International", "CPESC verified [E: V3-08]; others unverified [J]"),
        ],
        partners="AWWA; WEF; Water Professionals International (formerly ABC; exam criteria); state operator certification boards; NRWA/RCAP (small systems); ASDWA (review); EPA Office of Water (federal partner). Readiness: Strong [J].",
        demand="Utility and state job postings; operator need-to-know criteria and exam blueprints (may be proprietary: AS/IA to negotiate use); state class specifications; consumer confidence reports; sanitary survey forms.",
        issues=["Licensure may stretch time-to-certify if automation removes hands-on tasks [S; confirm with certification-board data].",
                "Core DB-C05 (asset management) and PS-C09 (greenhouse gas inventories) are planned but not yet authored: the enactments here point at their seed keys (`W-REF-PENDING`). DB-C06 (operational-technology security) is not yet authored; its enactment is listed in the WP-06 worklog for wiring."],
    ),
    "waterq": dict(
        scope_in="Water resources, hydrology and supply planning, groundwater and source-water protection, surface water-quality regulation (load allocations, discharge permits, certifications), wetlands and compensatory mitigation, and stream assessment.",
        scope_out="Utility operations (MOD-01 `water`); marine and coastal management (MOD-13, wave 3); laboratory analysis (MOD-18).",
        roles=["R17", "R11", "R12", "R09", "R23"],
        gates=[
            ("Professional Wetland Scientist / Wetland Professional in Training", "Society of Wetland Scientists Professional Certification Program", "verified [E: V3-08]"),
            ("Professional Geologist licence", "State geology boards (ASBOG exams)", "unverified [J: DB-CR-015]"),
            ("Professional Hydrologist", "American Institute of Hydrology", "unverified [J: DB-CR-014]"),
            ("Certified Ground Water Professional; water well contractor licence", "NGWA; state agencies", "unverified [J]"),
            ("Professional Engineer", "State engineering boards", "unverified [J]"),
        ],
        partners="ACWA (state clean water administrators); the state wetland managers' association (current name to verify); SWS Professional Certification Program; AIH; NGWA; EPA Office of Water, USGS and USACE Regulatory (federal partners). Readiness: Moderate [J].",
        demand="State permit-writer and water-quality class specifications; discharge permit fact sheets and conditions; load-allocation reports; mitigation bank instruments; state water-rights decisions.",
        issues=["The regulated-waters definition is still proposed (L5 `seed:ins/wotus-definition`); delineation and dredge-and-fill content is written jurisdiction-neutral [E: V2].",
                "Discharge permit writing is the SL-C02 `waterq` enactment (absorbs DB-C07), not a module competency (ADR-0018)."],
    ),
    "air": dict(
        scope_in="Ambient monitoring and data quality, emissions inventories and modelling for attainment planning, stationary-source permitting and inspection (as enactments of core competencies), and smoke management for prescribed and managed fire.",
        scope_out="Mobile-source engineering; greenhouse gas markets (MOD-10, wave 3); climate mitigation planning (MOD-08, wave 2).",
        roles=["R28", "R03", "R07", "R11", "R12", "R37"],
        gates=[
            ("Visible-emissions observer certification (reference opacity method), renewed every six months", "Accredited smoke schools", "unverified [J: DB-CR-019]"),
            ("Qualified source testing individual / observer", "Stack testing accreditation body (to verify)", "unverified [J: DB-CR-020]"),
            ("Accredited greenhouse gas verifier (state programme)", "State air agency (e.g. California)", "unverified [J: DB-CR-021]"),
            ("Professional Engineer for some permits", "State engineering boards", "unverified [J]"),
        ],
        partners="NACAA; AAPCA; A&WMA; EPA Air Pollution Training Institute curricula as a federal partner, whose 2025-26 operating status could not be confirmed [E: DB-ECO-012, not-found]. Readiness: Moderate [J].",
        demand="State and local air agency postings and class specifications; operating and construction permit conditions; state implementation plan submittals; monitoring network plans.",
        issues=["v1 6.7.5 was split here; its three task seeds were moved from `core/` to `modules/air/` with their successors (DB-C13, DB-C14).",
                "The federal greenhouse gas reporting programme is under reconsideration (L5 `seed:ins/ghgrp-reconsideration`); facility-reporting content is regime-neutral."],
    ),
    "waste": dict(
        scope_in="Solid waste collection, processing and disposal; producer responsibility and materials management; hazardous waste determination and generator compliance; contaminated-site assessment, remedy selection and long-term stewardship; transaction due diligence; regulation of solid waste facilities.",
        scope_out="Chemicals and pesticide regulation and facility-wide EHS management (MOD-05, wave 2); emergency hazardous-materials response beyond the core field-safety practice.",
        roles=["R27", "R29", "R37", "R11", "R12", "R23"],
        gates=[
            ("Certified Hazardous Materials Manager", "IHMM", "verified [E: V3-08]"),
            ("Hazardous waste operations and emergency response training (entry gate)", "Employer-provided under the federal worker-protection standard; register record `seed:crd-hazwoper` (WP-07)", "[J: DB-CR-024]"),
            ("Licensed site professional opinions (state privatized cleanup programmes)", "State licensing boards", "unverified [J: DB-CR-031]"),
            ("Environmental professional for all appropriate inquiries (regulatory definition, not issued)", "Federal definition", "[J: DB-CR-032]"),
            ("Landfill and solid waste facility operator certification; association certifications", "State programmes; SWANA", "unverified [J: DB-CR-027, DB-CR-028]"),
        ],
        partners="SWANA; ASTSWMO (state waste and cleanup officials); ITRC (under ECOS); IHMM; state LSP/LSRP boards; EPA OLEM, DoD and DOE cleanup programmes (federal partners). Readiness: Strong [J].",
        demand="State cleanup and solid waste programme postings; consulting job architectures; producer responsibility programme plans; remedy decision documents; facility permits.",
        issues=["v1 3.7.1 and 3.7.5 were rewritten from corporate business-model and tool framing; technology names moved to L4.",
                "Producer responsibility (DB-C17) is lifecycle `emerging`: state programmes are in first implementation cycles."],
    ),
    "envhealth": dict(
        scope_in="Local and state environmental public health services: inspections and plan review (food, onsite wastewater, pools, housing), outbreak and complaint investigation, vector control and extreme heat preparedness.",
        scope_out="Laboratory analysis (MOD-18); occupational health; population-level risk assessment as such (core v1 6.7.1, enacted here).",
        roles=["R26", "R12"],
        gates=[
            ("Registered Environmental Health Specialist / Registered Sanitarian", "NEHA", "verified [E: V3-08]"),
            ("State sanitarian or environmental health specialist registration", "State boards (subset of states)", "unverified [J: DB-CR-044]"),
            ("Certified Professional - Food Safety", "NEHA", "unverified [J: DB-CR-045]"),
            ("Onsite wastewater installer, inspector and designer licences; public-health pesticide applicator licence", "State and local programmes", "unverified [J: DB-CR-047, DB-CR-036]"),
        ],
        partners="NEHA (verified active [E: V3-07]); NACCHO; APHL; EHAC (degree accreditation); CDC and FDA environmental health programmes (federal partners). Readiness: Strong [J].",
        demand="County and city health department postings and class specifications; state food and onsite codes; inspection standardization procedures.",
        issues=["Extreme heat (DB-C39) is lifecycle `emerging`; its home here follows the home-module rule and may need MOD-08 and MOD-09 enactments in wave 2."],
    ),
    "hazards": dict(
        scope_in="Hazard mitigation planning and fundable projects, environmental and historic preservation review of disaster-funded projects, local floodplain administration, and rapid post-disaster field assessment.",
        scope_out="Response operations under incident command as such (core DB-C42, not yet authored); climate adaptation planning (MOD-08, wave 2).",
        roles=["R30", "R10", "R06"],
        gates=[
            ("Certified Floodplain Manager", "ASFPM", "verified [E: V3-08]"),
            ("Certified Emergency Manager / Associate Emergency Manager", "IAEM", "unverified [J: DB-CR-066]"),
            ("Incident command training and national qualification system positions", "FEMA Emergency Management Institute; authorities having jurisdiction", "unverified [J: DB-CR-068]"),
        ],
        partners="IAEM; NEMA (state emergency management directors); ASFPM (verified active [E: V3-07]); FEMA Emergency Management Institute (federal partner). Readiness: Strong [J].",
        demand="County and city floodplain administrator and emergency management postings; adopted hazard mitigation plans; floodplain ordinances; disaster-programme environmental review records.",
        issues=["Federal mitigation funding programmes changed in 2025-26; programme status must be verified by WP-15 before any external statement [J: DB-030].",
                "Historic preservation consultation content covered by the ADR-0007 hold is not authored in any enactment here."],
    ),
    "forest": dict(
        scope_in="Silviculture, inventory, stand projection, forest health, management and harvest planning, timber sale and stewardship agreements, certification conformance, wildland fire suppression, prescribed fire, fuels, fire behaviour and intelligence, post-fire stabilization, rangeland monitoring and grazing, resource roads, and the public-lands minerals enactment.",
        scope_out="Restoration practice and invasive species control as such (core); working lands and private-landowner programmes (MOD-14, wave 2, except the early draft FH-C03); smoke-management decisions by air regulators (home MOD-03 `air`).",
        roles=["R14", "R06", "R07", "R08", "R18", "R34", "R02"],
        gates=[
            ("Wildland fire position qualifications (crew to burn boss and analyst positions)", "USWFS-USFS aligned federal qualification standards effective January 2027; NWCG standards updated January 2026", "verified [E: V3-13]"),
            ("SAF Certified Forester", "Society of American Foresters", "verified [E: V3-08]"),
            ("State registered or licensed forester; state certified prescribed burn manager", "State boards and forestry agencies (minority of states)", "unverified [J: DB-CR-072, DB-CR-082]"),
            ("Certified Professional in Rangeland Management", "SRM", "unverified [J: DB-CR-075]"),
            ("ISA Certified Arborist (tree risk)", "International Society of Arboriculture", "verified [E: V3-08]"),
            ("Remote pilot certificate for uncrewed aircraft", "Federal aviation authority", "unverified [J: DB-CR-091]"),
        ],
        partners="SAF and SRM (verified active [E: V3-07]); NASF (state foresters); USWFS/USFS training organizations with NWCG as reviewer. Readiness: Strong [J].",
        demand="OpenLMP plan components (strong for this module: range, roads, minerals, smoke [E: IA §5.7; DB-011]); federal and state forester and fire position descriptions; certification audit reports.",
        issues=["TN-C06 is held under ADR-0007 §D and is not authored or described here; TN drafts only.",
                "IA-CC-05 is an early draft homed in `extract` (wave 2); its public-lands enactment and tasks live here (ADR-0018 s.4).",
                "Protect suggestions (v1 1.3.2, 4.3.2) are listed for the Editorial Board, not set (ADR-0015).",
                "Lands and realty is core PS-C15 with a public-lands enactment planned here; PS-C15 is not yet authored."],
    ),
    "wildlife": dict(
        scope_in="Inland fisheries management, fisheries stock assessment, hatchery and aquatic propagation, humane capture and handling, and international wildlife and fisheries agreements.",
        scope_out="Wildlife survey, habitat assessment and population dynamics as such (core v1 4.1.2, 1.1.5, 1.4.1); marine and coastal management (MOD-13, wave 3); listed-species consultation as such (core FH-C01, enacted here).",
        roles=["R15", "R16", "R02"],
        gates=[
            ("Certified / Associate Wildlife Biologist", "The Wildlife Society", "verified [E: V3-08]"),
            ("Certified / Associate Fisheries Professional", "American Fisheries Society", "unverified [J: DB-CR-074]"),
            ("Scientific collection permits, animal-care protocol approval, controlled-drug authorization for immobilization", "Agencies and institutions", "[J]"),
        ],
        partners="TWS and AFS (verified active [E: V3-07]); AFWA (state fish and wildlife agencies); USFWS and NOAA Fisheries (federal partners). Readiness: Strong [J].",
        demand="State fish and wildlife agency class specifications; stock assessment reports and review panel records; hatchery management plans.",
        issues=["No module competency covers wildlife population and harvest management; role R15 relies on core competencies. Flagged for the CA: stay with core or add a candidate (scope expansion; not authored).",
                "Actor enactment notes requested by TN for fisheries content are held (ADR-0007)."],
    ),
    "parks": dict(
        scope_in="Visitor information and safety, recreation opportunity and visitor-use management, scenic resources and wilderness character, on parks and protected areas at all levels of government.",
        scope_out="Interpretation and trail construction as such (core v1 5.1.3 and 4.2.5); law enforcement (credential-gated role variant); urban planning (MOD-17, wave 2).",
        roles=["R21"],
        gates=[
            ("Certified Park and Recreation Professional", "NRPA", "unverified [J: DB-CR-083]"),
            ("Certified Interpretive Guide / Planner / Host", "National Association for Interpretation", "unverified [J: DB-CR-084]"),
            ("Law enforcement commission for protection rangers (variant gate, not a level)", "Agency", "[J]"),
            ("Wilderness first aid / first responder", "Various providers", "unverified [J: DB-CR-092]"),
        ],
        partners="NRPA; NAI; the national association of state park directors; NPS and state park systems (agency partners). Readiness: Moderate [J]. Pulled forward from DB's wave 3 by the CA for 0025 and NPS coverage (ADR-0018).",
        demand="Federal 0025 and state park ranger position descriptions; visitor use management plans; OpenLMP recreation, scenery and wilderness components (motorized recreation/ROS and scenic clusters [E: IA §5.7]).",
        issues=["v1 4.2.5 (trails) is enacted in two wave-1 modules only; not enacted here to avoid a thin record (see the three-module coverage table)."],
    ),
}


def recs(ns, kind):
    out = []
    for p in sorted((DATA / "modules" / ns / kind).glob("*.yaml")):
        r = L.load_yaml(p)
        if r.get("status") in ("superseded", "withdrawn"):
            continue
        out.append(r)
    return out


def comp_line(r):
    life = "" if r.get("lifecycleState") == "established" else f" — lifecycle {r.get('lifecycleState')}"
    subs = ", ".join(r.get("subsectors") or [])
    return f"- `{r['id']}` {r['prefLabel']['en']} ({subs}){life}"


def brief(ns):
    b = BRIEF[ns]
    m = MODS[ns]
    comps = recs(ns, "competencies")
    enas = recs(ns, "enactments")
    core_index = {}
    for p in (DATA / "core" / "competencies").glob("*.yaml"):
        r = L.load_yaml(p)
        core_index[r["id"]] = r["prefLabel"]["en"]
    mod_index = {}
    for p in (DATA / "modules").glob("*/competencies/*.yaml"):
        r = L.load_yaml(p)
        mod_index[r["id"]] = (r["prefLabel"]["en"], r["module"])
    lines = [f"# {m['notation']} {m['prefLabel']} — module brief (`{ns}`)", "",
             COMMON_STATUS, "",
             "## Scope", "",
             "**Subsectors:** " + "; ".join(f"{s} {SUBS[s]}" for s in m["subsectors"]) + ".", "",
             f"**In scope:** {b['scope_in']}", "",
             f"**Out of scope:** {b['scope_out']}", "",
             "**Module competencies (home here):**", ""]
    lines += [comp_line(r) for r in comps] or ["- none"]
    lines += ["", "**Competencies enacted here:**", ""]
    seen = []
    for e in enas:
        c = e["competency"]
        if c in core_index:
            label, where = core_index[c], "core"
        elif c in mod_index:
            label, where = mod_index[c][0], mod_index[c][1]
        else:
            label, where = "(planned; not yet authored)", "core"
        seen.append(f"- `{c}` {label} [{where}] — enactment `{e['id']}`")
    lines += seen or ["- none"]
    lines += ["", "**Roles served (`docs/decisions/mvp_role_set.csv`):** " +
              "; ".join(f"{k} {ROLES[k]['title']}" for k in b["roles"] if k in ROLES) + ".", "",
              "## Licensure and credential gates", "",
              "Gates are Credential records on tasks and role variants, never proficiency levels (ADR-0003 T-8). Register records are WP-07's (`data/v2/registers/credentials/`).", "",
              "| Gate | Issuer | Verification |", "|---|---|---|"]
    lines += [f"| {g} | {i} | {v} |" for g, i, v in b["gates"]]
    lines += ["", "## Candidate advisory partners (*candidate*, not committed)", "", PARTNER_NOTE, "", f"*Candidate:* {b['partners']}", "",
              "## Demand corpus to build (ADR-0018 §8; P-DB-17)", "", b["demand"], "",
              "## Open issues", ""]
    lines += [f"- {x}" for x in b["issues"]]
    lines += ["", "*Generated by `docs/build/WP-06/build_briefs.py` from the records; record lists are computed, not typed. Licence: CC BY 4.0 (narrative, ADR-0013).*", ""]
    return "\n".join(lines)


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    for ns in BRIEF:
        (OUTDIR / f"{MODS[ns]['notation']}_{ns}.md").write_text(brief(ns), encoding="utf-8")
        print("wrote", OUTDIR / f"{MODS[ns]['notation']}_{ns}.md")


if __name__ == "__main__":
    main()
