#!/usr/bin/env python3
"""Write handoff_wp06_field_enactments.csv: proposed module (field) enactments of WP-03 core competencies for WP-06.

Content is FC judgment [J]. `already_enacted` is computed from data/v2/modules/*/enactments/ at run time, so the list
stays honest as WP-06 works. WP-03 does not edit module records (S1 brief; PHASE4_BUILD_PLAN WP-06). Licence: Apache-2.0.
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import emstlib as L  # noqa: E402

P = [  # (competency, module, what changes in the field, suggested additional task or indicator variant)
    ("seed:v1-4.1.1", "forest", "Inventory, fuels and regeneration plots to agency plot protocols; hot/cold/blind checks against measurement-quality objectives.", "Indicator variant: re-measures fuels transects within the programme's tolerance."),
    ("seed:v1-4.1.1", "parks", "Rare-plant and visitor-impact vegetation plots in protected areas; trampling-sensitive access.", "Task: locate and monitor rare-plant populations without creating access trails."),
    ("seed:v1-4.1.1", "wildlife", "Habitat vegetation plots tied to species-use studies.", ""),
    ("seed:v1-4.1.1", "waterq", "Riparian and wetland vegetation sampling, including wetland indicator status for delineation (FC-C06).", ""),
    ("seed:v1-4.1.2", "wildlife", "Home enactment: species-specific survey protocols, permits for listed-species surveys; capture stays in FC-C15.", "Credential gate: survey permit where the protocol requires one."),
    ("seed:v1-4.1.2", "forest", "Pre-project surveys for listed species before timber or fuels work; seasonal survey windows bind schedules.", ""),
    ("seed:v1-4.1.2", "parks", "Visitor-wildlife conflict and habituation monitoring.", ""),
    ("seed:v1-4.1.4", "waterq", "Hydric-soil indicators for wetland delineation (FC-C06).", "Indicator variant: identifies hydric-soil indicators within the regional supplement's criteria."),
    ("seed:v1-4.1.4", "forest", "Soil-disturbance monitoring after harvest and fuels work; erosion-hazard rating.", ""),
    ("seed:v1-4.1.4", "waste", "Contaminated-soil sampling under a site safety plan (with seed:v1-4.4.4-A, FC-C16).", ""),
    ("seed:v1-4.1.4", "hazards", "Post-fire soil burn severity and hydrophobicity tests for emergency stabilization (FC-C25, v1 4.3.5).", ""),
    ("seed:v1-1.1.2", "wildlife", "Multi-taxon inventory and monitoring networks.", ""),
    ("seed:v1-1.1.2", "parks", "Protected-area inventory and monitoring programmes and long-term plots.", ""),
    ("seed:v1-1.1.2", "waterq", "Aquatic biological assessment (macroinvertebrate, fish, algae indices).", ""),
    ("seed:v1-1.1.5", "wildlife", "Home enactment: species habitat models and use studies.", ""),
    ("seed:v1-1.1.5", "forest", "Habitat for listed species built into project design and plan components.", ""),
    ("seed:v1-1.1.5", "waterq", "Aquatic habitat and instream-flow habitat assessment.", ""),
    ("seed:v1-1.7.1", "forest", "Post-fire type conversion and reforestation feasibility.", ""),
    ("seed:v1-1.7.1", "hazards", "State change after floods, landslides or storms; recovery-versus-transformation choices.", ""),
    ("seed:v1-1.7.1", "parks", "Climate-driven change in protected areas and what condition to manage toward.", ""),
    ("seed:FC-C22", "forest", "Stand and fire history from fire scars, stumps and legacy roads.", ""),
    ("seed:FC-C22", "waterq", "Channel history, legacy dams and diversions read from landforms and records.", ""),
    ("seed:FC-C22", "waste", "Former land use read on site during site reconnaissance for environmental site assessment (DB-C19, PS-C13).", "Task: walk a property during site reconnaissance, recording evidence of former land uses that could indicate contamination."),
    ("seed:FC-C23", "waterq", "Monitoring data sheets and electronic forms tied to the quality assurance project plan.", ""),
    ("seed:FC-C23", "envhealth", "Inspection records captured on mobile forms in the field.", ""),
    ("seed:FC-C23", "waste", "Boring logs and field logbooks with evidentiary requirements.", ""),
    ("seed:FC-C28", "wildlife", "Seasonal survey campaigns timed to breeding and migration windows.", ""),
    ("seed:FC-C28", "waterq", "Synoptic and storm-event sampling campaigns timed to flow.", ""),
    ("seed:FC-C28", "hazards", "Post-event field deployments and logistics outside incident command.", ""),
    ("seed:FS-C04", "forest", "Fuels and canopy reference plots for remote-sensed fuels products.", ""),
    ("seed:FS-C04", "hazards", "Damage and burn-severity reference data for remote damage and severity products.", ""),
    ("seed:FS-C04", "wildlife", "Labelled image and audio reference libraries for detection models; sensitive-location handling.", ""),
    ("seed:FC-C18", "forest", "Navigation on fire assignments and remote plots; recovery when positioning fails under canopy.", ""),
    ("seed:FC-C18", "parks", "Backcountry patrol and search operations as specialization.", ""),
    ("seed:FC-C18", "hazards", "Navigation in disaster-altered terrain; search segments.", ""),
    ("seed:FC-C20", "forest", "Fire and timber crews; task-book formation and evaluators.", ""),
    ("seed:FC-C20", "parks", "Trail and corps crews; volunteer crew leaders.", ""),
    ("seed:FC-C20", "wildlife", "Seasonal survey crews; observer training.", ""),
    ("seed:v1-4.2.1", "forest", "Post-fire reforestation and planting-stock handling; drone seeding as a tool (L4).", ""),
    ("seed:v1-4.2.1", "waterq", "Stream and wetland restoration including process-based structures.", ""),
    ("seed:v1-4.2.1", "parks", "Visitor-impact and urban-park restoration with public use.", ""),
    ("seed:v1-4.2.4", "forest", "Road and harvest-unit erosion control.", ""),
    ("seed:v1-4.2.4", "water", "Construction stormwater controls (inspector credential preferred).", ""),
    ("seed:v1-4.2.4", "hazards", "Post-fire emergency stabilization treatments.", ""),
    ("seed:v1-4.2.5", "parks", "Home enactment for trails: visitor-use standards and accessibility.", ""),
    ("seed:v1-4.2.5", "forest", "Recreation and administrative trails; wilderness tool restrictions.", ""),
    ("seed:v1-4.2.5", "wildlife", "Refuge trails and access with seasonal closures for wildlife.", ""),
    ("seed:v1-4.4.1-A", "forest", "Fireline lookouts, communications, escape routes and safety zones; heat and smoke on assignments (links v1 4.3.1, 4.3.2).", ""),
    ("seed:v1-4.4.1-A", "waste", "Field risk alongside the site safety plan at contaminated sites (with seed:v1-4.4.4-A).", ""),
    ("seed:v1-4.4.1-A", "hazards", "Post-disaster sites: unstable structures, debris, floodwater.", ""),
    ("seed:v1-4.4.1-A", "waterq", "Water hazards: wading limits, cold water, boats (FC-C12).", ""),
    ("seed:v1-4.4.2", "forest", "Line medical response on fire assignments.", ""),
    ("seed:v1-4.4.2", "parks", "Visitor medical response by rangers (separate credential-gated variant for EMS).", ""),
    ("seed:v1-4.4.2", "hazards", "Care at disaster field sites.", ""),
    ("seed:v1-4.4.4-A", "waste", "Home enactment: hazardous-waste operations under a site plan; HAZWOPER gate.", ""),
    ("seed:v1-4.4.4-A", "water", "Treatment plants: confined spaces, chlorine and process chemicals.", ""),
    ("seed:v1-4.4.4-A", "hazards", "Debris and disaster sites with unknown materials.", ""),
    ("seed:v1-4.4.4-A", "envhealth", "Inspections at sites with hazardous exposures.", ""),
    ("seed:v1-4.4.5", "forest", "Fire radio protocols and incident communications.", ""),
    ("seed:v1-4.4.5", "hazards", "Communications during response and recovery.", ""),
    ("seed:v1-4.4.5", "parks", "Backcountry patrol check-ins and visitor emergencies.", ""),
    ("seed:v1-4.5.1", "forest", "Fireline hand tools and line construction standards (v1 4.3.1 T1).", ""),
    ("seed:v1-4.5.1", "parks", "Trail tools and wilderness restrictions on mechanized tools.", ""),
    ("seed:v1-4.5.1", "wildlife", "Habitat project hand work.", ""),
    ("seed:v1-4.5.2", "forest", "Felling and bucking on fire and fuels assignments; sawyer qualification as the gate.", "Credential gate: sawyer certification (not yet in the WP-07 register)."),
    ("seed:v1-4.5.2", "parks", "Hazard-tree removal at recreation sites and trail clearing.", ""),
    ("seed:v1-4.5.2", "hazards", "Storm and debris clearing.", ""),
    ("seed:v1-4.5.3-A", "forest", "Fire and forest road driving; engines and crew carriers.", ""),
    ("seed:v1-4.5.3-A", "wildlife", "All-terrain vehicles for survey and refuge work.", ""),
    ("seed:v1-4.5.3-A", "waterq", "Access to remote monitoring stations.", ""),
    ("seed:v1-4.5.5", "forest", "Engines, pumps and saws on fire assignments.", ""),
    ("seed:v1-4.5.5", "waterq", "Sampling gear, sondes and boats.", ""),
    ("seed:v1-4.5.5", "parks", "Trail and maintenance equipment.", ""),
]
FIRE = [  # gaps WP-03 found in WP-06's fire module records (suggestions only)
    ("seed:v1-4.3.2", "forest", "Credential gates: link prescribed-fire tasks to seed:crd-wildland-fire-position-qualification and, for state burns, seed:crd-state-prescribed-burn-manager.", ""),
    ("seed:v1-4.3.2", "forest", "Rare-event adaptation is not yet a task: declaring contingency or wildfire when triggers are met (simulation and after-action review; FCA-RX-3).", "Task: Declare a contingency or wildfire when holding triggers in the burn plan are met, calling contingency resources and recording the trigger."),
    ("seed:v1-4.3.2", "forest", "L1 holding-crew anchor (FCA-RX-1): hold assigned line with lookouts, communications, escape routes and safety zones in place.", "Indicator L1: Holds assigned line with lookouts, communications, escape routes and safety zones in place, reporting spots and slopovers by radio. (Avoid starting with 'Holds': B04a; use 'Keeps assigned line...')"),
    ("seed:v1-4.3.2", "forest", "seed:db-4.3.2-t4 (supervise UAS ignition) can also support the core seed:FC-C14 as contributing (module to core is allowed).", ""),
    ("seed:v1-4.3.1", "forest", "Credential gates: link fireline tasks to seed:crd-wildland-fire-position-qualification.", ""),
]


def main():
    have = defaultdict(set)
    for p in (L.DATA_V2 / "modules").glob("*/enactments/*.yaml"):
        r = L.load_yaml(p)
        have[r.get("competency")].add(r.get("enactedInModule") or p.parts[-3])
    rows = []
    for c, m, note, extra in P + FIRE:
        rows.append({"competency": c, "module": m, "already_enacted": str(m in have.get(c, set())).lower(),
                     "enactments_now": len(have.get(c, set())), "field_enactment_note": note, "suggested_task_or_indicator": extra})
    with open(HERE / "handoff_wp06_field_enactments.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} rows; {sum(1 for r in rows if r['already_enacted'] == 'false')} not yet enacted by WP-06")


if __name__ == "__main__":
    main()
