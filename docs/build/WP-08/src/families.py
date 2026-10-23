"""JobFamily records: v1 F1-F15 successors for navigation only (ADR-0006 section 5). F4 and F13 are split (P-DB-14);
no Tribal profession family (TN veto 5); no F16 (ADR-0020). Membership is computed by
pipelines/views/job_families.py under rule job-family-membership@0.1.0 (parameters:
pipelines/views/rules/job-family-membership@0.1.0.yaml). Definitions are named by the work (ADR-0016)."""
import wp08lib as W

RULE = "job-family-membership@0.1.0"

FAMILIES = [
    ("F01", "forest-management", "Forest management",
     "Managing forested landscapes through inventory, silviculture, forest health and harvest planning on public or private land.",
     "Core when the work needs knowledge of trees and stand dynamics specifically; general ecological, data or project work "
     "that foresters also use is supporting only (carried from v1 Task 5 family F1).", []),
    ("F02", "fish-wildlife-management", "Fish and wildlife management",
     "Assessing and managing fish and wildlife populations and their habitats, including capture, survey, harvest and propagation.",
     "Core when the work targets animal populations or their habitat use; habitat-only vegetation work is supporting (v1 F2).", []),
    ("F03", "ecological-restoration", "Ecological restoration",
     "Planning, implementing and monitoring treatments that restore ecological structure and function, adapting them to site response.",
     "Core when the primary objective is restorative; productive or multi-use objectives belong to forest or rangeland families (v1 F3).", []),
    ("F04a", "watershed-water-resources", "Watershed science and water resources",
     "Measuring, modelling and protecting surface water, groundwater and watersheds for supply, quality and hazard decisions.",
     "Core when water is the managed resource and the work is assessment, planning or protection; plant operation is F04b "
     "(split of v1 F4, P-DB-14).", ["seed:fh-family-f04b-water-utility-operations"]),
    ("F04b", "water-utility-operations", "Water and wastewater utility operations",
     "Operating and overseeing drinking water, wastewater and stormwater systems to quality targets and permit limits.",
     "Core when the work runs or regulates treatment and distribution systems in responsible charge (split of v1 F4, P-DB-14).",
     ["seed:fh-family-f04a-watershed-water-resources"]),
    ("F05", "conservation-science-ecology", "Conservation science and ecology",
     "Studying biodiversity, habitats and ecosystem change and designing monitoring that supports valid inference.",
     "Core when the work produces ecological evidence or inference; implementation of treatments is restoration (v1 F5).", []),
    ("F06", "climate-adaptation", "Climate science and adaptation",
     "Analyzing climate observations and projections and planning adaptation for species, ecosystems, infrastructure and communities.",
     "Core when climate change is the analytic or planning object (v1 F6).", []),
    ("F07", "environmental-data-geospatial", "Environmental data science and geospatial analysis",
     "Building, validating and stewarding environmental data, spatial, remote-sensing and model products and their reference data.",
     "Core when the deliverable is a data, map or model product with stated accuracy (v1 F7).", []),
    ("F08", "regulation-review-authorization", "Environmental review, authorization and compliance",
     "Reviewing effects of proposed actions, authorizing uses, inspecting and enforcing, and administering regulatory programmes.",
     "Core when the work sits on either side of a regulatory relationship; authority position is a variant attribute (v1 F8; ADR-0017).", []),
    ("F09", "land-use-resource-planning", "Land use and resource planning",
     "Preparing land, resource, recreation and hazard mitigation plans and the regulations that implement them.",
     "Core when the deliverable is a plan or plan component (v1 F9).", []),
    ("F10", "working-lands", "Working lands and agricultural conservation",
     "Helping private and public land managers adopt conservation practices on farms, ranches and grazing lands.",
     "Core when the work is conservation planning or practice delivery on working lands (v1 F10).", []),
    ("F11", "interpretation-communication", "Interpretation, engagement and risk communication",
     "Informing, engaging and protecting the public through interpretation, facilitation and communication of environmental risk.",
     "Core when the audience's understanding or participation is the outcome (v1 F11).", []),
    ("F12", "fire-management", "Wildland fire management",
     "Suppressing wildland fire, planning and executing fuels treatments and prescribed fire, and producing fire intelligence.",
     "Core when the work is organized around fire; fire used as a silvicultural tool alone is forest management (v1 F12).", []),
    ("F13a", "environmental-public-health", "Environmental public health services",
     "Inspecting, investigating and preventing illness and injury from environmental hazards in communities and facilities.",
     "Core when the work protects human health from environmental exposures through inspection or investigation (split of "
     "v1 F13, P-DB-14).", ["seed:fh-family-f13b-cumulative-burden-analysis"]),
    ("F13b", "cumulative-burden-analysis", "Cumulative-burden and distributional-effects analysis",
     "Analyzing cumulative environmental burdens and how the effects of decisions are distributed across affected communities.",
     "Core when distributional or cumulative effects are the analytic object (split of v1 F13, P-DB-14; programme labels are "
     "search aliases only, ADR-0016).", ["seed:fh-family-f13a-environmental-public-health"]),
    ("F14", "corporate-compliance-disclosure", "Facility compliance, disclosure and sustainability reporting",
     "Keeping regulated organizations in compliance and preparing environmental disclosures and their evidence for assurance.",
     "Core when the work is done for a regulated or reporting entity (v1 F14).", []),
    ("F15", "environmental-finance-markets", "Environmental finance and markets",
     "Designing and administering environmental financial assistance, credit and market transactions and their verification.",
     "Core when money, credits or financial instruments are the object of the work (v1 F15).", []),
]


def records():
    out = []
    for code, slug, label, definition, boundary, related in FAMILIES:
        rid = f"seed:fh-family-{code.lower()}-{slug}"
        alt = {"F13b": ["environmental justice analysis", "cumulative impacts"], "F14": ["corporate sustainability", "ESG"],
               "F04b": ["water utilities"], "F07": ["GIS", "remote sensing"]}.get(code)
        rec = {"id": rid, "type": "JobFamily", "prefLabel": {"en": label}, "definition": {"en": definition},
               "boundaryCriteria": {"en": boundary}, "memberRule": RULE,
               "notation": [{"scheme": "EMSTv1family", "value": code}],
               "layer": "L3", "module": "core", "status": "draft", "lifecycleState": "established",
               "useTier": "describe", "validationStatus": "draft", "license": "CC0-1.0", "sensitivity": "public",
               "editorialNote": {"en": ("Navigation only; membership is computed (never stored) by "
                                        f"pipelines/views/job_families.py under {RULE}. Boundary criteria condensed from "
                                        "legacy/v1/docs/profession_family_definitions.md (v1 text dedicated CC0).")},
               "provenance": W.prov(adr=["ADR-0006", "ADR-0016", "ADR-0020", "ADR-0021"])}
        if alt:
            rec["altLabel"] = {"en": alt}
        if related:
            rec["scopeNote"] = {"en": "Split sibling: " + ", ".join(related)}
        out.append(rec)
    return out
