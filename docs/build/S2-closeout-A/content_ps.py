"""S2 close-out A content, A7 under the PS code: PS-C15 (land rights, rights-of-way and realty; absorbs IA-CC-06).
Module enactments in forest, water and parks are DB's (work order row PS-C15; ADR-0018 §4); only core actor enactments
are authored here. Reviewer A5 SC: the same agent holds both codes, so the SC review is a self-review and is recorded as
such in the worklog."""
from s2adsl import T, I, E, WS, RA, SIM, PORT, TBO, R

ADR_PS = ["ADR-0003", "ADR-0004", "ADR-0017", "ADR-0018", "ADR-0023", "ADR-0030"]

COMPETENCIES = [
    {
        "id": "seed:PS-C15", "agents": ["PS"], "adr": ADR_PS,
        "label": "Negotiate and administer land rights, rights-of-way and realty actions",
        "alt": ["land agent", "right-of-way agent", "realty specialist", "lands and realty", "easement acquisition",
                "land acquisition", "special-use authorization", "conservation easement stewardship"],
        "definition": "The capability to secure, document and administer rights to use land for environmental, "
                      "infrastructure and conservation purposes: title and encumbrance research, negotiation of easements, "
                      "options, leases, acquisitions and exchanges, right-of-way and special-use authorizations on public "
                      "land, landowner relations and compensation, and monitoring of the terms. Appraisal and land "
                      "surveying as licensed practices are referenced, not covered.",
        "statement": "Researches title and encumbrances; negotiates easements, options, leases, acquisitions and exchanges "
                     "with landowners and agencies; processes right-of-way and special-use applications against plan "
                     "decisions and required review; maintains landowner relations and resolves complaints; and monitors "
                     "and enforces the terms of the rights held.",
        "span": ("L1", "L4"),
        "sources": ["IA-033"],
        "editorial": "S2 close-out A (A7, PS code; reviewer A5 SC, the same agent's other code). Survivor: absorbs IA-CC-06 "
                     "(conduct lands and realty actions; candidate_disposition.csv). Land rights, rights-of-way and realty "
                     "recur in public lands, utilities, transportation, energy and land trusts (G-4); public realty "
                     "specialists and private land agents share the work, which makes it a mobility bridge (PS report "
                     "§3). Lands and realty is one of seven functions found missing in land management plan requirements "
                     "[E: IA-033]. Module enactments for forest, water and parks are DB's (ADR-0018 §4).",
        "sensitivity": [
            ("DM-02", "Permitting timelines and acceleration options change when rights-of-way must be secured for a "
                      "project.", "J", None),
            ("DM-15", "Rental, cost-recovery and compensation rules set the price and terms of the rights.", "J", None),
        ],
        "tasks": [
            T("seed:ps-research-title", "Research the title and recorded encumbrances of a parcel, compiling the chain of "
              "title, easements and reservations that affect a proposed acquisition or crossing", "WF-RESOURCE",
              formation="partial"),
            T("seed:ps-negotiate-easement", "Negotiate an easement, option or lease with a landowner, recording the agreed "
              "terms, the compensation basis and each commitment made", "WF-RESOURCE", field="on-site-preferred",
              formation="yes", modes=["MODE-RESOLVE"], rel=["stakeholder"]),
            T("seed:ps-process-row-application", "Process an application for a right-of-way or special-use authorization "
              "on public land, checking it against the land management plan and the review it requires",
              "WF-AUTHORIZE", formation="partial"),
            T("seed:ps-prepare-land-case-file", "Prepare a land exchange or acquisition case file with the appraisal, title "
              "evidence and public-interest findings the deciding official needs", "WF-RESOURCE", formation="partial"),
            T("seed:ps-resolve-landowner-complaint", "Resolve a landowner's complaint about construction or restoration on a "
              "right-of-way, recording the issue, the remedy agreed and its completion", "WF-RESOURCE",
              field="on-site-preferred", formation="partial", modes=["MODE-RESOLVE"], rel=["stakeholder"]),
            T("seed:ps-monitor-easement-terms", "Monitor a conservation easement or right-of-way on site against its terms, "
              "documenting each violation found and the notice issued", "WF-MONITOR", field="on-site-required",
              formation="yes"),
        ],
        "levels": {
            "L1": [
                I("Compiles the chain of title and recorded encumbrances for a parcel, with no recorded interest missing "
                  "when checked by a title reviewer.", RA + WS, tasks=["seed:ps-research-title"],
                  evidence=["title abstract"]),
                I("Documents an easement monitoring visit with photographs and observations for each term, as observed by "
                  "the supervising agent.", TBO, tasks=["seed:ps-monitor-easement-terms"],
                  evidence=["monitoring report"]),
            ],
            "L2": [
                I("Negotiates a routine easement or lease in a standardized role-play, reaching terms within the authority "
                  "and compensation range given.", SIM, attr="ATT-AUT", tasks=["seed:ps-negotiate-easement"],
                  evidence=["simulation score sheet"]),
                I("Processes a right-of-way application, identifying each plan decision and review requirement it "
                  "triggers, accepted by the authorized officer.", WS, attr="ATT-KNO",
                  tasks=["seed:ps-process-row-application"], evidence=["application review"]),
                I("Resolves a landowner complaint in a seeded case, recording the remedy agreed and its completion date.",
                  SIM + RA, attr="ATT-GUI", tasks=["seed:ps-resolve-landowner-complaint"],
                  evidence=["complaint record"]),
            ],
            "L3": [
                I("Prepares an exchange or acquisition case file that the deciding official accepts without returning it "
                  "for missing title, appraisal or public-interest evidence.", RA, attr="ATT-CPX",
                  tasks=["seed:ps-prepare-land-case-file"], evidence=["case file"]),
                I("Negotiates rights along a multi-parcel route, keeping a commitments register that the project and the "
                  "landowners accept as complete.", PORT, attr="ATT-SCO", obs4=2,
                  tasks=["seed:ps-negotiate-easement"], evidence=["commitments register"]),
                I("Documents an easement violation with evidence of each term breached and issues the notice the easement "
                  "terms require.", WS + RA, attr="ATT-AUT", tasks=["seed:ps-monitor-easement-terms"],
                  evidence=["violation file", "notice"]),
            ],
            "L4": [
                I("Sets a programme's land-rights acquisition and stewardship procedures, with the compensation, "
                  "documentation and monitoring standards agents apply.", PORT, attr="ATT-GUI",
                  tasks=["seed:ps-negotiate-easement", "seed:ps-monitor-easement-terms"], evidence=["procedure"]),
                I("Reviews agents' case files against the procedure, returning each with the defects to correct before "
                  "closing.", RA, attr="ATT-FOR", tasks=["seed:ps-prepare-land-case-file"],
                  evidence=["review comments"]),
            ],
        },
        "enactments": [
            E("seed:ena-ps-c15-federal-land-manager", "Federal realty specialist", "federal-land-manager",
              position="resource-manager",
              basis="Federal land statutes and regulations for special uses, grazing and rights-of-way on public land, "
                    "decided within the governing land management plan; land exchange and acquisition authorities.",
              principal="The authorized officer.", venue="Administrative appeals; federal courts.",
              note="Same realty work as the private land agent, from the authorizing side [J].",
              links=[("federal-land-use-authorizations", R, "Registered without dated events; basis linked, status not "
                                                            "yet verified.")]),
            E("seed:ena-ps-c15-private", "Private land and right-of-way agent", "firm", position="service-provider",
              basis="Contracts with the project sponsor; state real-estate or right-of-way agent licensing where it "
                    "applies; condemnation rules for regulated utilities.",
              principal="The project sponsor.", venue="State utility commissions; state courts in condemnation.",
              note="Utility, transmission and pipeline land agents; transferable from public realty experience [J]."),
            E("seed:ena-ps-c15-land-trust", "Land trust easement holder", "land-trust",
              basis="State conservation easement statutes and the terms of each recorded easement; land trust "
                    "accreditation standards.",
              principal="The land trust's board.", venue="State courts; the state attorney general for charitable assets.",
              note="Holding an easement makes monitoring and enforcement a perpetual duty of the holder [J]."),
        ],
    },
]
