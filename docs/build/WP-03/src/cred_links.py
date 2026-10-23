"""Credential gates (ADR-0003 T-8) linked to WP-03 tasks, using records in data/v2/registers/credentials/ (WP-07).
Kinds: required | preferred | entry. Gates the register does not yet hold are listed in the WP-03 worklog handoff."""
RPC = "seed:crd-remote-pilot-certificate"
FIRE = "seed:crd-wildland-fire-position-qualification"
PEST = "seed:crd-pesticide-applicator"
WFA = "seed:crd-wilderness-first-aid"
ISA = "seed:crd-isa-certified-arborist-utility-specialist-munici"
DWO = "seed:crd-drinking-water-treatment-operator"
WWO = "seed:crd-wastewater-treatment-operator"
ICS = "seed:crd-nims-ics-training"
ESC = "seed:crd-certified-erosion-sediment-and-storm-water-inspe"

LINKS = {
    "seed:v1-4.5.4-T1": [(RPC, "required")],
    "seed:v1-2.3.2-T1": [(RPC, "required")],
    "seed:v1-2.3.2-T2": [(RPC, "required")],
    "seed:v1-4.5.4-T2": [(RPC, "required")],
    "seed:fc-uas-bvlos-supervise": [(RPC, "required")],
    "seed:fc-uas-ignition": [(FIRE, "required")],
    "seed:v1-4.2.2-T1": [(PEST, "required")],
    "seed:fc-edrr-contain": [(PEST, "preferred")],
    "seed:v1-4.4.2-T1": [(WFA, "required")],
    "seed:fc-fa-monitor": [(WFA, "required")],
    "seed:fc-fa-evac-decision": [(WFA, "required")],
    "seed:fc-tree-visual": [(ISA, "preferred")],
    "seed:fc-tree-advanced": [(ISA, "preferred")],
    "seed:fc-tree-mitigate": [(ISA, "preferred")],
    "seed:db-c03-monitor-loops": [(DWO, "required"), (WWO, "required")],
    "seed:db-c03-validate-recs": [(DWO, "required"), (WWO, "required")],
    "seed:db-c03-override": [(DWO, "required"), (WWO, "required")],
    "seed:db-c03-manual": [(DWO, "required"), (WWO, "required")],
    "seed:db-c03-override-criteria": [(DWO, "required"), (WWO, "required")],
    "seed:v1-4.4.3-T1": [(ICS, "preferred")],
    "seed:v1-4.4.5-T3": [(ICS, "preferred")],
    "seed:v1-4.2.4-T3": [(ESC, "preferred")],
}
NOTES = {
    "seed:v1-4.2.2-T1": "The applicator licence applies when the prescription uses chemical methods.",
    "seed:fc-tree-visual": "The usual required gate (a tree risk assessment qualification) is not yet in the register; arborist certification linked as preferred.",
    "seed:db-c03-monitor-loops": "Operator licence for the facility type (drinking water or wastewater) in responsible charge; one of the two applies.",
    "seed:v1-4.5.4-T1": "Public-aircraft operations under agency authority use an agency pilot qualification (not yet in the register).",
}
