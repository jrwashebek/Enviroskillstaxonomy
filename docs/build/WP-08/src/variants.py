"""RoleVariant specs: one per sector actor listed in mvp_role_set.csv (+ named slices). Tribal variants are held stubs.

Authority position, sector actor and subtype are editorial (SPEC section 10 rule 6). Credential gates and sign-off are
verified facts only with E-labelled sources (rule 8); they are recorded here as FH drafts. taskAdds `w` is a time share.
"""
from wp08lib import T, V

PROF = {"entry": "GS-5 to GS-7", "journey": "GS-9 to GS-11", "senior": "GS-12 to GS-13", "lead": "GS-13 to GS-14",
        "strategic": "GS-14 to GS-15"}
TECH = {"entry": "GS-3 to GS-5", "journey": "GS-6 to GS-7", "senior": "GS-8 to GS-9", "lead": "GS-9 to GS-11"}


def band(levels, table):
    return "; ".join(f"{table[k]} [{k}]" for k in levels if k in table)


FED = dict(industry="public-administration", ownership="public", delivery="in-house")
NGO = dict(industry="nonprofit-services", ownership="nonprofit")
ACAD = dict(subtype="university", industry="education-research", ownership="public", delivery="in-house")


def fed(pos, subtype, levels, table=PROF, **kw):
    return V("federal", pos, subtype=subtype, band=band(levels, table), **FED, **kw)


def st(pos, subtype="state-agency", **kw):
    return V("state", pos, subtype=subtype, industry="public-administration", ownership="public", delivery="in-house", **kw)


def lo(pos, subtype="county", **kw):
    return V("local", pos, subtype=subtype, industry=kw.pop("industry", "public-administration"), ownership="public",
             delivery=kw.pop("delivery", "in-house"), **kw)


def ngo(pos, subtype, delivery="in-house", **kw):
    return V("ngo", pos, subtype=subtype, delivery=delivery, **NGO, **kw)


def pr(pos, industry="consulting-engineering", ownership="private-closely-held", delivery="contracted", **kw):
    return V("private", pos, subtype="firm", industry=industry, ownership=ownership, delivery=delivery, **kw)


def ac(**kw):
    return V("academic", "advisor-researcher", **ACAD, **kw)


TRIBAL = V("tribal", "resource-manager", subtype="federally-recognized-tribe")
FIRE_Q = ("wildland-fire-position-qualification", "required")
WFA = ("wilderness-first-aid", "preferred")


def table(spec):
    lv = spec.levels
    k = spec.key[:3]
    T_ = {
        "R01": [
            V("federal", "service-provider", subtype="federal-land-manager", industry="public-administration",
              ownership="public", delivery="contracted", gates=[WFA],
              note="Crews work on federal lands under cooperative agreements; members are not federal employees."),
            st("service-provider", gates=[WFA], note="State-sponsored or state-run corps crews."),
            lo("service-provider", gates=[WFA], note="Local and youth corps crews working for municipalities and counties."),
            ngo("service-provider", "conservation-corps", delivery="contracted", gates=[WFA],
                instruments=["americorps-grant-terminations"], note="Nonprofit corps crews funded by grants and fees."),
            TRIBAL],
        "R02": [
            fed("resource-manager", "federal-land-manager", lv, TECH, gates=[WFA, ("remote-pilot-certificate", "preferred")],
                note="Biological science, forestry, range and soil conservation technician work on federal lands."),
            st("resource-manager", gates=[WFA], note="State fish, wildlife and natural resource technician ladders."),
            lo("resource-manager", subtype="special-district", gates=[WFA]),
            ngo("resource-manager", "land-trust", gates=[WFA]),
            pr("service-provider", gates=[WFA, ("hazwoper", "preferred")],
               adds=[T("fc-haz-hasp", 4, 0.03, "CE"), T("lc-txf-invoice-against-agreement", 2, 0.01, "", "j")],
               note="Consulting field technicians; site safety plans and billing to agreements are added."),
            TRIBAL],
        "R03": [
            fed("advisor-researcher", "federal-science-agency", lv, TECH, gates=[("remote-pilot-certificate", "preferred")],
                note="Hydrologic and physical science technicians in federal science centres."),
            st("regulator", note="Ambient monitoring units that produce data for regulatory programmes."),
            lo("regulated-party", subtype="municipality", industry="utility-water",
               note="Utility and stormwater monitoring for permit compliance."),
            pr("service-provider", gates=[("hazwoper", "preferred")],
               adds=[T("fc-haz-decon-exit", 4, 0.02, "CE")], note="Consulting and laboratory field services."),
            TRIBAL],
        "R04": [
            fed("resource-manager", "federal-land-manager", lv, gates=[("gisp", "preferred")]),
            st("resource-manager", gates=[("gisp", "preferred")]),
            lo("resource-manager", gates=[("gisp", "preferred")], note="County and municipal planning GIS units."),
            ngo("advisor-researcher", "science-ngo"),
            pr("service-provider", gates=[("gisp", "preferred")],
               adds=[T("lc-txf-draft-scope", 3, 0.02, "", "sl"), T("lc-txf-run-quality-review", 4, 0.02, "", "sl")]),
            ac(adds=[T("dc-06-release-package", 3, 0.02)])],
        "R05": [
            fed("advisor-researcher", "federal-science-agency", lv),
            st("resource-manager"),
            ngo("advisor-researcher", "science-ngo"),
            pr("service-provider", industry="env-tech", adds=[T("lc-txf-run-quality-review", 4, 0.02, "", "s")],
               note="Earth-observation and monitoring-technology firms and carbon measurement services."),
            ac(adds=[T("dc-06-release-package", 3, 0.02)])],
        "R06": [
            fed("resource-manager", "federal-land-manager", lv, TECH, gates=[FIRE_Q], signoff=("position-qualification", ["wildland-fire-position-qualification"]),
                instruments=["uswfs-so-3448", "wildland-fire-quals-alignment"]),
            st("resource-manager", gates=[FIRE_Q], signoff=("position-qualification", ["wildland-fire-position-qualification"])),
            lo("resource-manager", subtype="special-district", gates=[FIRE_Q],
               signoff=("position-qualification", ["wildland-fire-position-qualification"])),
            pr("service-provider", gates=[FIRE_Q], signoff=("position-qualification", ["wildland-fire-position-qualification"]),
               note="Contract crews and engines dispatched under agreements."),
            TRIBAL],
        "R07": [
            fed("resource-manager", "federal-land-manager", lv, gates=[FIRE_Q],
                signoff=("position-qualification", ["wildland-fire-position-qualification"]),
                instruments=["wildland-fire-quals-alignment", "fix-our-forests-act"]),
            st("resource-manager", gates=[FIRE_Q, ("state-prescribed-burn-manager", "preferred")],
               signoff=("position-qualification", ["wildland-fire-position-qualification"])),
            lo("resource-manager", gates=[("state-prescribed-burn-manager", "preferred")],
               signoff=("licensure", ["state-prescribed-burn-manager"]), note="County wildfire planning and fuels programmes."),
            ngo("resource-manager", "land-trust", gates=[("state-prescribed-burn-manager", "preferred")],
                signoff=("licensure", ["state-prescribed-burn-manager"])),
            pr("service-provider", gates=[("state-prescribed-burn-manager", "preferred")],
               signoff=("licensure", ["state-prescribed-burn-manager"]),
               note="Contract burn services and utility wildfire-mitigation programmes."),
            TRIBAL],
        "R08": [
            fed("resource-manager", "federal-land-manager", lv, gates=[("wildland-fire-position-qualification", "preferred")],
                instruments=["uswfs-so-3448"]),
            st("resource-manager", gates=[("wildland-fire-position-qualification", "preferred")])],
        "R09": [
            fed("resource-manager", "federal-land-manager", lv, gates=[("contracting-officers-representative", "preferred")],
                instruments=["stewardship-contracting", "good-neighbor-authority"],
                adds=[T("v1-3.1.4-T3", 4, 0.02, "", "sl"), T("sc-select-agreement-instrument", 3, 0.02, "", "sl")]),
            st("resource-manager", instruments=["good-neighbor-authority"]),
            lo("resource-manager", subtype="conservation-district"),
            ngo("resource-manager", "watershed-group", gates=[("cerp", "preferred")],
                adds=[T("lc-txf-prepare-proposal-budget", 3, 0.02, "", "sl")]),
            pr("service-provider", gates=[("cerp", "preferred")],
               adds=[T("lc-txf-negotiate-scope-change", 3, 0.02, "", "sl"), T("lc-txf-invoice-against-agreement", 3, 0.02),
                     T("lc-txf-check-compliance", 3, 0.01, "", "sl")],
               note="Design-build restoration contractors working for public and private owners."),
            TRIBAL],
        "R10": [
            fed("resource-manager", "federal-land-manager", lv,
                instruments=["nepa-fra-2023", "ceq-nepa-regs-removal", "seven-county", "doi-nepa-procedures",
                             "usda-nepa-procedures", "epa-nepa-procedures", "dot-nepa-procedures", "fast-41"],
                note="Reviews land-agency and federally permitted actions under the agency's own procedures."),
            st("regulator", instruments=["state-sepa-ca", "state-sepa-mn", "state-sepa-ny", "state-sepa-wa", "ceqa-2025-reforms",
                                         "nepa-assignment-23usc327"],
               note="State lead-agency review under little-NEPA statutes and assigned transportation review."),
            lo("regulator", instruments=["state-sepa-ca", "state-sepa-wa"], note="Local lead-agency review under state statutes."),
            pr("service-provider", gates=[("aicp-and-aicp-advanced-specialty-certifications", "preferred")],
               drops=["sc-write-review-decision", "sc-evaluate-sponsor-document", "sc-document-independent-evaluation",
                      "sc-issue-preparer-standards", "sc-screen-preparer-conflicts"],
               adds=[T("lc-txf-draft-scope", 3, 0.02, "", "sl"), T("lc-txf-write-approach", 3, 0.02, "", "sl"),
                     T("sc-disclose-assignment-interests", 4, 0.01, "CE"), T("lc-txf-manage-subcontractor", 3, 0.02, "", "sl")],
               note="Consultant preparer working under agency direction; the agency keeps the decision and independent evaluation."),
            TRIBAL],
        "R11": [
            fed("regulator", "federal-regulator", lv, instruments=["cwa-402-npdes", "cwa-404", "caa-title-v", "caa-nsr-psd",
                                                                    "rcra-permits", "state-program-approval-regs"],
                drops=["sc-prepare-delegated-workplan"],
                adds=[T("sc-assess-rule-stringency", 4, 0.03, "", "sl"), T("sc-audit-local-delivery", 3, 0.02, "", "sl")],
                note="Issues permits where programmes are not delegated and oversees delegated state programmes."),
            st("regulator", gates=[("professional-engineer", "preferred")],
               instruments=["cwa-402-npdes", "caa-title-v", "caa-nsr-psd", "rcra-permits", "cwa-404", "florida-404-assumption"],
               juris=["delegated-program-jurisdiction"], note="State programmes issuing permits under delegated or assumed authority."),
            lo("regulator", subtype="regional-authority", instruments=["caa-title-v", "caa-nsr-psd"],
               juris=["delegated-program-jurisdiction"], note="Local air districts and municipal permit programmes."),
            TRIBAL],
        "R12": [
            fed("regulator", "federal-regulator", lv, instruments=["federal-inspection-authorities", "epa-penalty-policies"]),
            st("regulator", gates=[("state-inspector-credential", "required"), ("epa-method-9-visible-emissions-observer-certific", "preferred")],
               signoff=("position-qualification", ["state-inspector-credential"]), instruments=["epa-penalty-policies"],
               juris=["delegated-program-jurisdiction"]),
            lo("regulator", gates=[("state-inspector-credential", "preferred")],
               signoff=("position-qualification", ["state-inspector-credential"])),
            TRIBAL],
        "R13": [
            fed("resource-manager", "federal-land-manager", lv, gates=[("contracting-officers-representative", "preferred")],
                instruments=["appropriations-law", "fy2026-interior-approps", "obbba-ira-rescissions", "good-neighbor-authority"]),
            st("regulator", instruments=["categorical-program-grants"], note="Division and programme managers in state environmental agencies."),
            lo("regulator", note="County and municipal environmental programme managers."),
            ngo("resource-manager", "land-trust", note="Programme directors of land and water conservation organizations."),
            TRIBAL],
        # ---------------------------------------------------------------- P2
        "R14": [fed("resource-manager", "federal-land-manager", lv, instruments=["stewardship-contracting", "good-neighbor-authority"]),
                st("resource-manager", gates=[("state-registered-or-licensed-forester", "preferred")]),
                lo("resource-manager", gates=[("isa-certified-arborist-utility-specialist-munici", "preferred")]),
                ngo("resource-manager", "land-trust"),
                pr("resource-manager", industry="forest-products", delivery="in-house",
                   gates=[("saf-certified-forester", "preferred"), ("state-registered-or-licensed-forester", "preferred")],
                   adds=[T("PS-C23-T1", 4, 0.04, "", "jsl"), T("PS-C23-T2", 4, 0.03, "", "sl"),
                         T("PS-C23-T3", 3, 0.02, "", "sl"), T("PS-C23-T4", 3, 0.02, "", "jsl")],
                   note="Commercial timberland and certification-scheme forestry."),
                TRIBAL],
        "R15": [fed("resource-manager", "federal-land-manager", lv), st("resource-manager"),
                ngo("advisor-researcher", "science-ngo"),
                pr("service-provider", gates=[("certified-wildlife-biologist", "preferred")]), ac(), TRIBAL],
        "R16": [fed("resource-manager", "federal-land-manager", lv), st("resource-manager"),
                ngo("advisor-researcher", "science-ngo"),
                pr("service-provider", gates=[("certified-fisheries-professional-associate-fishe", "preferred")]), ac(), TRIBAL],
        "R17": [fed("advisor-researcher", "federal-science-agency", lv), st("resource-manager"),
                lo("regulated-party", subtype="special-district", industry="utility-water"),
                pr("service-provider", gates=[("professional-hydrologist-hydrologist-in-training", "preferred"),
                                              ("professional-geologist-license", "preferred")]), ac()],
        "R18": [fed("resource-manager", "federal-land-manager", lv, instruments=["federal-land-use-authorizations"],
                    gates=[("certified-professional-in-rangeland-management", "preferred")]),
                st("resource-manager", juris=["state-lands"]), TRIBAL],
        "R19": [fed("advisor-researcher", "federal-agency", lv), st("advisor-researcher"),
                lo("advisor-researcher", subtype="conservation-district"),
                ngo("advisor-researcher", "community-organization", gates=[("nrcs-technical-service-provider-certification", "preferred")])],
        "R20": [fed("advisor-researcher", "federal-science-agency", lv), st("advisor-researcher"),
                ngo("advisor-researcher", "science-ngo"),
                pr("service-provider", gates=[("certified-ecologist-senior-ecologist", "preferred")]), ac()],
        "R21": [fed("resource-manager", "federal-land-manager", lv, gates=[("wilderness-first-aid", "preferred"),
                                                                        ("certified-interpretive-guide-planner-host", "preferred")]),
                st("resource-manager"), lo("resource-manager", subtype="municipality",
                                           gates=[("certified-park-and-recreation-professional", "preferred")])],
        "R22": [fed("regulator", "federal-regulator", lv, gates=[("professional-engineer", "preferred")],
                    signoff=("licensure", ["professional-engineer"])),
                st("regulator", gates=[("professional-engineer", "preferred")], signoff=("licensure", ["professional-engineer"]),
                   instruments=["state-licensing-acts-wi"]),
                lo("regulated-party", subtype="municipality", industry="utility-water", gates=[("professional-engineer", "preferred")],
                   signoff=("licensure", ["professional-engineer"])),
                pr("service-provider", gates=[("professional-engineer", "required")], signoff=("licensure", ["professional-engineer"]))],
        "R23": [fed("regulator", "federal-regulator", lv, instruments=["epa-penalty-policies"]),
                st("regulator", instruments=["epa-penalty-policies"]), lo("regulator")],
        "R24": [fed("regulator", "federal-regulator", lv, instruments=["state-program-approval-regs"]),
                st("regulator", juris=["delegated-program-jurisdiction"], instruments=["state-program-approval-regs"])],
        "R25": [V("federal", "regulated-party", subtype="federal-agency", scheme="FWS",
                  band="WG grade set by the federal wage system job grading standard [entry|journey|senior|lead]",
                  gates=[("drinking-water-treatment-operator", "required"), ("wastewater-treatment-operator", "required")],
                  signoff=("licensure", ["drinking-water-treatment-operator", "wastewater-treatment-operator"]), **FED),
                st("regulated-party", gates=[("drinking-water-treatment-operator", "required"), ("wastewater-treatment-operator", "required")],
                   signoff=("licensure", ["drinking-water-treatment-operator", "wastewater-treatment-operator"]),
                   note="State-operated facilities and plants."),
                lo("regulated-party", subtype="municipality", industry="utility-water",
                   gates=[("drinking-water-treatment-operator", "required"), ("wastewater-treatment-operator", "required"),
                          ("wastewater-collection-operator", "preferred"), ("water-distribution-operator", "preferred")],
                   signoff=("licensure", ["drinking-water-treatment-operator", "wastewater-treatment-operator"])),
                pr("regulated-party", industry="utility-water", ownership="investor-owned", delivery="in-house",
                   gates=[("drinking-water-treatment-operator", "required"), ("wastewater-treatment-operator", "required")],
                   signoff=("licensure", ["drinking-water-treatment-operator", "wastewater-treatment-operator"])),
                TRIBAL],
        "R26": [st("regulator", gates=[("state-registered-sanitarian-environmental-health", "required"), ("rehs-rs", "preferred")],
                   signoff=("licensure", ["state-registered-sanitarian-environmental-health"])),
                lo("regulator", subtype="local-health-department",
                   gates=[("state-registered-sanitarian-environmental-health", "required"), ("rehs-rs", "preferred"),
                          ("certified-professional-food-safety", "preferred")],
                   signoff=("licensure", ["state-registered-sanitarian-environmental-health"])),
                TRIBAL],
        "R27": [fed("regulator", "federal-regulator", lv, gates=[("hazwoper", "required")]),
                st("regulator", gates=[("hazwoper", "required")]),
                pr("service-provider", gates=[("hazwoper", "required"), ("licensed-site-professional-licensed-site-remedia", "preferred"),
                                              ("professional-engineer", "preferred")],
                   signoff=("licensure", ["licensed-site-professional-licensed-site-remedia"]),
                   note="Consultants for responsible parties; licensed-site-professional opinions where state law provides.")],
        "R28": [fed("regulator", "federal-regulator", lv, instruments=["caa-title-v", "caa-nsr-psd"]),
                st("regulator", instruments=["caa-title-v", "caa-nsr-psd"], gates=[("epa-method-9-visible-emissions-observer-certific", "preferred")]),
                lo("regulator", subtype="regional-authority", instruments=["caa-title-v"]),
                pr("service-provider", gates=[("qualified-environmental-professional", "preferred"), ("professional-engineer", "preferred")])],
        "R29": [st("regulator", instruments=[]), lo("regulated-party", subtype="county", industry="waste-materials",
                                                   gates=[("swana-professional-certifications", "preferred"),
                                                          ("state-landfill-solid-waste-facility-operator-cer", "required")]),
                pr("regulated-party", industry="waste-materials", ownership="investor-owned", delivery="in-house",
                   gates=[("state-landfill-solid-waste-facility-operator-cer", "required")])],
        "R30": [fed("funder", "federal-agency", lv, gates=[("certified-floodplain-manager", "preferred")]),
                st("funder", gates=[("certified-floodplain-manager", "preferred")]),
                lo("regulator", gates=[("certified-floodplain-manager", "preferred")], note="Local floodplain administrators."),
                pr("service-provider", gates=[("certified-floodplain-manager", "preferred")]), TRIBAL],
        # ---------------------------------------------------------------- P3
        "R31": [fed("resource-manager", "federal-land-manager", lv), st("regulator"), pr("service-provider")],
        "R32": [fed("advisor-researcher", "federal-agency", lv,
                    note="Internal second-line assurance; position coding provisional (editorial)."),
                st("advisor-researcher", note="Internal second-line assurance; position coding provisional (editorial)."),
                pr("independent-verifier", industry="assurance-audit", delivery="independent-third-party")],
        "R33": [fed("regulator", "federal-regulator", lv, instruments=["permitting-tech-pm-2025", "ceq-permitting-data-standard",
                                                                        "permitting-tech-action-plan"]),
                st("regulator"), lo("regulator", subtype="municipality")],
        "R34": [fed("resource-manager", "federal-land-manager", lv, instruments=["good-neighbor-authority", "stewardship-contracting"]),
                st("resource-manager", instruments=["good-neighbor-authority", "co-hb26-1205"]),
                ngo("service-provider", "land-trust", delivery="contracted"), TRIBAL],
        "R35": [fed("advisor-researcher", "federal-agency", lv), st("advisor-researcher"), lo("advisor-researcher", subtype="municipality"),
                ngo("advisor-researcher", "professional-society"),
                pr("advisor-researcher", industry="consulting-engineering", delivery="in-house")],
        "R36": [pr("regulated-party", industry="corporate-sustainability", ownership="investor-owned", delivery="in-house",
                   instruments=["ca-sb-253", "ca-sb-261", "eu-omnibus-i", "ghgrp-reconsideration"]),
                ngo("regulated-party", "foundation")],
        # ---------------------------------------------------------------- P4
        "R37": [pr("regulated-party", industry="industrial-ehs", ownership="investor-owned", delivery="in-house",
                   gates=[("hazwoper", "preferred"), ("rcra-hazardous-waste-personnel-training", "required"),
                          ("certified-hazardous-materials-manager", "preferred"), ("iso-14001-ems-lead-auditor", "preferred")],
                   signoff=("legal-signatory", []),
                   instruments=["report-certification-rules", "cwa-402-npdes", "caa-title-v", "rcra-permits", "npdes-ereporting-rule"],
                   note="The facility's responsible official certifies reports; this role prepares and checks them."),
                pr("service-provider", industry="consulting-engineering", delivery="contracted", slice="applicant-preparer",
                   label="Facility environmental compliance specialist (private, applicant-side permit preparer)",
                   gates=[("professional-engineer", "preferred"), ("qualified-environmental-professional", "preferred")],
                   drops=["v1-6.1.2-T3", "sc-apply-post-employment-rules"],
                   adds=[T("v1-6.1.3-T1", 5, 0.05, "C", "jsl"), T("sc-prepare-authority-map", 4, 0.03, "", "sl"),
                         T("sc-prepare-negotiation-brief", 3, 0.02, "", "sl"), T("lc-txf-draft-scope", 3, 0.02, "", "sl"),
                         T("sc-screen-assignment-conflicts", 4, 0.01, "C", "sl")],
                   note=("Applicant-side preparer: consultants who prepare permit applications and compliance submissions "
                         "for facilities; the applicant variant in the permit-writer mirror triad (ADR-0017 section 4).")),
                lo("regulated-party", subtype="municipality", industry="utility-water",
                   instruments=["report-certification-rules", "cwa-402-npdes", "npdes-ereporting-rule"]),
                fed("regulated-party", "federal-agency", lv, instruments=["report-certification-rules", "rcra-permits"],
                    note="Compliance staff at federal installations and facilities.")],
    }
    return T_[k]


def for_role(spec):
    return table(spec)
