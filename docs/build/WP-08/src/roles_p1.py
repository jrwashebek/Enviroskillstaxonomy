"""P1 corridor roles R01-R13 at full depth (COR-1, COR-2, COR-3). Agent drafts; see prompts/wp08-role-profile.md.

Task tuple: T(task, importance 1-5, relative time weight, flags C=critical E=neededAtEntry F=formationTask, levels).
Target string: one token per role level ('-' = not targeted). Change atoms X feed the role-change view inputs.
"""
from wp08lib import C, T, X, Role

E, J, S, LD, ST = "entry", "journey", "senior", "lead", "strategic"

ROLES = [
    # ------------------------------------------------------------------ COR-1
    Role(
        key="R01-conservation-corps-member", tier="P1", area="core", wf="WF-BUILD", levels=[E], life="established",
        title="Conservation corps member", use_tier="develop",
        alt=["corps crew member", "conservation crew member"],
        definition=("Entry field role that builds and maintains trails, restoration and erosion-control treatments and "
                    "invasive-species control on public and private lands, working in supervised crews under safety "
                    "protocols. It is the first formation step for field craft and feeds agency technician roles."),
        function=("Carry out crew-based land treatment work safely to specification, recording what was done and "
                  "learning field judgment through supervised repetition."),
        comps=[
            C("v1-4.2.1", 5, "L1", dist=True), C("v1-4.2.5", 5, "L1", dist=True), C("v1-4.2.2", 4, "L1"),
            C("v1-4.2.4", 4, "L1"), C("v1-4.5.1", 5, "L1"), C("v1-4.5.2", 5, "L1"), C("v1-4.4.1-A", 5, "L1"),
            C("FC-C18", 4, "L1"), C("v1-4.4.2", 4, "L1"), C("v1-4.4.5", 4, "L1"),
            C("FC-C11", 3, "L1"), C("FC-C23", 3, "L1"), C("v1-4.5.3-A", 3, "L1"), C("v1-4.4.1-B", 3, "L1"),
        ],
        tasks=[
            T("v1-4.2.1-T1", 4, 3, "EF"), T("fc-resto-lowtech", 3, 2, "F"), T("v1-4.2.1-T2", 3, 1),
            T("v1-4.7.4-T2", 3, 1), T("v1-4.2.2-T1", 4, 3, "EF"), T("fc-edrr-survey", 3, 1, "F"),
            T("v1-4.2.4-T1", 4, 2, "EF"), T("v1-4.2.4-T3", 3, 1), T("v1-4.2.5-T1", 4, 3, "EF"),
            T("v1-4.2.5-T2", 4, 3, "E"), T("v1-4.2.5-T3", 3, 1, "F"), T("v1-4.5.1-T1", 5, 3, "CEF"),
            T("v1-4.5.1-T2", 3, 1, "E"), T("fc-crosscut", 4, 1, "CF"), T("v1-4.5.2-T1", 5, 2, "CF"),
            T("fc-saw-preuse", 5, 0.5, "CE"), T("fc-saw-buck-limb", 4, 1.5, "CF"), T("v1-4.4.1-T1", 5, 0.8, "CEF"),
            T("fc-risk-stopwork", 5, 0.3, "CE"), T("fc-risk-heat-recognize", 5, 0.3, "CE"),
            T("v1-4.4.2-T1", 5, 0.4, "CEF"), T("v1-4.4.5-T1", 5, 0.3, "CE"), T("v1-4.5.3-T3", 4, 0.4, "E"),
            T("v1-4.4.3-T2", 4, 0.8, "EF"), T("fc-bio-decon", 4, 0.4, "E"), T("v1-4.1.5-T1", 3, 0.8, "E"),
            T("lc-txc-report-near-miss", 4, 0.2, "CE"), T("dc-01-interpret-product", 2, 0.2),
            T("fc-txa-field-check", 2, 0.2, "F"),
        ],
        change=[
            X("role", "entry-path-at-risk", ["fiscal", "policy-reform"],
              "Corps capacity depends on grant funding: the 2025 terminations were largely reinstated in plaintiff "
              "jurisdictions and the 2026 settlement covers FY2026 only; one job board saw corps postings fall.",
              instruments=["americorps-grant-terminations"],
              signals=["sig/postings/conservation-job-board-americorps-2025", "sig/bls-ep-2025-35/45-4011/R01-conservation-corps-member"]),
            X("fc-edrr-survey", "transforming", ["sensing-tech", "AI"],
              "Imagery and environmental DNA detections increasingly nominate survey locations; field confirmation "
              "and treatment stay with the crew."),
            X("v1-4.4.1-T1", "transforming", ["AI"],
              "Template and AI-drafted hazard analyses are becoming common; the crew task shifts to checking them "
              "against the actual site before work."),
            X("v1-4.1.5-T1", "transforming", ["sensing-tech"],
              "Mobile forms replace paper records; completeness rules move into the form, judgment about what to "
              "record stays with the observer."),
            X("v1-4.2.5-T1", "stable", ["fiscal"], "Hand-built trail work is not compressed by current tools; demand "
              "follows maintenance funding."),
        ],
        progresses_to=["R02-field-resource-technician/federal", "R02-field-resource-technician/state"],
        note="No federal series: corps members are programme participants, not federal employees (X4 NoTermFound).",
    ),
    Role(
        key="R02-field-resource-technician", tier="P1", area="core", wf="WF-ASSESS", levels=[E, J], life="established",
        title="Field resource technician", use_tier="develop",
        alt=["biological science technician", "natural resource technician", "field technician"],
        definition=("Entry and journey field role that collects vegetation, wildlife, water and soil data to protocol, "
                    "identifies organisms, keeps sample custody and records with integrity, and checks remote and "
                    "AI-generated products against the ground. It is the largest field entry role and the main "
                    "formation step for identification and measurement judgment."),
        function=("Collect and record defensible field observations and samples to protocol, and verify automated "
                  "and remote products against what is on the ground."),
        comps=[
            C("v1-4.1.1", 5, "L1 L2"), C("v1-4.1.2", 5, "L1 L2"), C("v1-4.1.3", 5, "L1 L2"),
            C("v1-1.4.3", 5, "L1 L2", dist=True), C("FC-C23", 5, "L1 L2"), C("FC-C24", 4, "L1 L2"),
            C("FC-C18", 4, "L1 L2"), C("v1-4.4.1-A", 5, "L1 L2"), C("FC-C02", 4, "L1 L2", dist=True),
            C("v1-4.1.4", 4, "L1 L2"), C("v1-4.4.2", 4, "L1 L2"),
            C("FC-C16", 3, "L1 L2"), C("FC-C11", 3, "L1 L1"), C("FC-C12", 3, "L1 L1"), C("FC-C14", 2, "- L1"),
            C("FC-C01", 3, "L1 L2"), C("FC-C20", 3, "- L2"), C("FC-C22", 2, "- L2"), C("v1-4.5.3-A", 3, "L1 L2"),
            C("v1-4.4.1-B", 3, "L1 L2"),
        ],
        tx_floor={"DC-CAND-13": "L1 L2"},
        tasks=[
            T("v1-4.1.1-T1", 5, 3, "CEF"), T("v1-4.1.1-T3", 5, 2, "CEF"), T("fc-veg-adapt-protocol", 4, 1, "", "j"),
            T("v1-4.1.2-T1", 5, 3, "CEF"), T("v1-4.1.2-T2", 4, 1, "EF"), T("v1-1.4.2-T1", 4, 2, "E"),
            T("v1-4.1.3-T1", 5, 2, "CEF"), T("v1-1.2.4-T1", 5, 2, "CEF"), T("v1-4.1.3-T2", 4, 1, "EF"),
            T("v1-4.1.4-T1", 4, 1, "EF"), T("v1-4.1.4-T2", 4, 1, "E"), T("v1-1.4.3-T1", 5, 2, "CEF"),
            T("fc-id-adjudicate-ai", 4, 1, "CF"), T("v1-4.1.5-T1", 5, 2, "CEF"), T("v1-4.1.5-T2", 4, 1, "E"),
            T("v1-4.1.5-T3", 3, 1, "E"), T("fc-coc-complete", 5, 1, "CE"), T("fc-qc-collect", 4, 1, "E"),
            T("fc-clean-collect", 4, 1, "", "j"), T("fc-nav-route-plan", 4, 0.5, "E"), T("v1-4.4.3-T2", 5, 1, "CEF"),
            T("fc-bio-decon", 4, 0.5, "E"), T("fc-boat-wading", 4, 0.5, "CEF"), T("v1-2.3.2-T2", 3, 0.8, "", "j"),
            T("fc-sensor-service", 3, 1, "", "j"), T("fc-gt-collect-blind", 4, 1, "F", "j"),
            T("fc-gt-mismatch", 3, 0.5, "", "j"), T("fc-txa-field-check", 4, 0.5, "CEF"),
            T("fc-lead-cue-explain", 3, 0.5, "", "j"), T("fc-lead-field-day", 3, 1, "", "j"),
            T("v1-4.4.1-T1", 5, 0.5, "CE"), T("fc-risk-stopwork", 5, 0.2, "CE"), T("v1-4.4.2-T1", 5, 0.3, "CEF"),
            T("v1-4.5.3-T2", 4, 0.5, "CE"), T("fc-sitehist-read", 3, 0.5, "F", "j"),
        ],
        change=[
            X("role", "entry-path-at-risk", ["fiscal", "workforce-capacity"],
              "Seasonal and internship entry routes contracted in 2025; formation tasks done by seasonal crews are "
              "the ones automation also compresses.",
              signals=["sig/headcount/usfs-seasonal-hiring-2025-2026", "sig/postings/conservation-job-board-internships-2025"]),
            X("v1-1.4.2-T1", "transforming", ["sensing-tech", "AI"],
              "Camera traps and acoustic recorders with automated classifiers shift effort from detection in the "
              "field to deployment, servicing and review of detections.",
              signals=["sig/omb-ai-inventory-2025/species-detection"]),
            X("v1-4.1.2-T1", "transforming", ["sensing-tech", "AI"],
              "Passive acoustic and image surveys augment observer counts; observer surveys remain where detection "
              "depends on trained observers."),
            X("fc-id-adjudicate-ai", "new", ["AI"],
              "Accepting or rejecting AI-suggested identifications is new work that only an observer with formed "
              "identification skill can do."),
            X("fc-txa-field-check", "new", ["AI"], "Field checks of AI-generated condition maps and notes are new."),
            X("v1-1.4.3-T1", "stable", ["AI"],
              "Identification aids grow, but unaided identification is kept as a formation task with a by-hand quota "
              "(WP-07 provisions)."),
            X("fc-gt-collect-blind", "emerging", ["sensing-tech", "AI"],
              "Blind reference collection for remote products is growing with satellite and drone products."),
        ],
        entry_from=["R01-conservation-corps-member"],
        progresses_to=["R03-monitoring-data-technician", "R04-geospatial-remote-sensing-analyst",
                       "R05-ground-truth-validation-steward"],
    ),
    Role(
        key="R03-monitoring-data-technician", tier="P1", area="core", wf="WF-MONITOR", levels=[E, J, S],
        life="established", title="Monitoring and data technician", use_tier="develop",
        alt=["environmental monitoring technician", "field data technician", "hydrologic technician"],
        definition=("Field-to-data role that installs, services and verifies sensor networks, collects samples under "
                    "custody, and quality-assures monitoring data from collection to release. Work is shifting from "
                    "manual collection toward verification of automated streams and adjudication of automated flags."),
        function=("Produce monitoring data that are fit for decisions by keeping instruments, samples and data "
                  "streams under verified quality control."),
        comps=[
            C("FC-C01", 5, "L1 L2 L3", dist=True), C("FC-C24", 5, "L1 L2 L3"), C("v1-4.1.3", 4, "L1 L2 L3"),
            C("v1-2.2.3", 5, "L1 L2 L3", dist=True), C("FC-C23", 4, "L1 L2 L2"), C("DC-CAND-04", 4, "- L2 L3"),
            C("FC-C16", 4, "L1 L2 L3"), C("v1-4.4.1-A", 4, "L1 L2 L3"), C("v1-4.4.4-A", 4, "L1 L2 L2"),
            C("v1-2.2.1", 3, "L1 L2 L2"), C("FC-C31", 3, "- - L3"), C("FC-C02", 3, "L1 L2 L2"),
            C("FS-C04", 3, "- L2 L2"), C("FC-C12", 3, "- L1 L2"), C("v1-4.4.1-B", 3, "L1 L2 L3"),
        ],
        tx_floor={"DC-CAND-05": "L1 L2 L2", "DC-CAND-13": "L1 L2 L2"},
        tasks=[
            T("v1-2.3.1-T1", 4, 2, "EF"), T("fc-sensor-service", 5, 3, "CEF"), T("fc-sensor-sidebyside", 5, 2, "CEF"),
            T("v1-4.1.3-T3", 5, 1, "CEF"), T("v1-2.3.1-T2", 4, 1, "E"), T("fc-sensor-siting-bias", 4, 1, "", "js"),
            T("fc-sensor-manual-visit", 4, 1, "", "js"), T("fc-sensor-network-design", 4, 1, "", "s"),
            T("v1-1.2.4-T1", 5, 2, "CEF"), T("v1-4.1.3-T1", 4, 2, "EF"), T("fc-coc-complete", 5, 1, "CE"),
            T("fc-qc-collect", 5, 1, "CE"), T("fc-qc-invalid", 4, 0.5, "CE"), T("fc-qc-investigate", 4, 0.5, "", "s"),
            T("fc-clean-collect", 4, 1, "", "js"), T("v1-2.3.1-T3", 4, 1, "E"), T("dc-223-apply-checks", 5, 2, "CE"),
            T("dc-223-review-flags", 5, 2, "C", "js"), T("v1-2.6.4-T2", 5, 1, "CF", "js"),
            T("v1-2.2.3-T2", 4, 1, "F", "js"), T("dc-04-stream-qc", 4, 1, "", "s"), T("dc-04-versioning", 4, 0.5, "", "js"),
            T("dc-221-data-entry", 3, 1, "E"), T("v1-2.2.1-T2", 3, 1, "", "js"), T("fc-gt-collect-blind", 3, 0.5, "", "j"),
            T("fs-c04-collect-labels", 3, 0.5, "", "js"), T("fc-qa-hot-check", 3, 0.5, "", "s"),
            T("fc-boat-operate", 3, 0.5, "C", "js"), T("v1-4.4.1-T1", 5, 0.3, "CE"), T("fc-haz-hasp", 4, 0.3, "CE"),
            T("dc-05-provenance-record", 3, 0.5, "E"), T("v1-4.1.5-T2", 4, 0.5, "E"),
        ],
        change=[
            X("fc-sensor-service", "transforming", ["sensing-tech"],
              "Networked sensors multiply; field time moves from manual collection to servicing and verifying "
              "deployed instruments.", signals=["sig/omb-ai-inventory-2025/water-hydrology"]),
            X("dc-223-review-flags", "transforming", ["AI", "automation-robotics"],
              "Automated QC applies first-pass flags; the technician adjudicates them against field and instrument "
              "records."),
            X("v1-2.6.4-T2", "emerging", ["AI"],
              "Measuring false-flag and missed-error rates of automated checks is growing work."),
            X("dc-221-data-entry", "declining", ["sensing-tech", "automation-robotics"],
              "Telemetry and mobile capture reduce manual data entry."),
            X("dc-04-stream-qc", "emerging", ["sensing-tech"], "Streaming QC configuration moves to senior technicians."),
            X("v1-1.2.4-T1", "stable", [], "Grab sampling under custody is not compressed; it is a formation task."),
        ],
        entry_from=["R02-field-resource-technician"],
        progresses_to=["R05-ground-truth-validation-steward", "R12-environmental-compliance-inspector"],
    ),
    Role(
        key="R04-geospatial-remote-sensing-analyst", tier="P1", area="core", wf="WF-ASSESS", levels=[J, S, LD],
        life="established", title="Geospatial and remote sensing analyst", use_tier="develop",
        alt=["GIS analyst", "remote sensing analyst", "geospatial specialist"],
        definition=("Analyst role that maps and monitors environmental conditions from imagery and spatial data, builds "
                    "and validates detection and spatial models, designs maps for decisions, and states accuracy and "
                    "uncertainty. Pretrained Earth-observation models change the method layer; validation, transfer "
                    "testing and fitness-for-purpose judgments grow."),
        function=("Turn spatial and remotely sensed data into validated map and model products whose accuracy and "
                  "limits are stated for the decision they serve."),
        comps=[
            C("v1-2.1.2", 5, "L2 L3 L4", dist=True), C("v1-2.1.4", 5, "L2 L3 L4"), C("v1-2.1.5", 4, "L2 L3 L3"),
            C("v1-2.4.1", 4, "L2 L3 L4"), C("DC-CAND-09", 4, "L2 L3 L4", dist=True), C("DC-CAND-08", 4, "L2 L3 L3"),
            C("DC-CAND-11", 4, "L2 L3 L3"), C("FC-C02", 4, "L1 L2 L3"), C("DC-CAND-07", 4, "L2 L2 L3"),
            C("DC-CAND-13", 4, "L2 L3 L3"),
            C("DC-CAND-06", 3, "L2 L2 L3"), C("FS-C04", 3, "- L2 L3"), C("DC-CAND-22", 3, "- - L3"),
            C("v1-2.2.1", 3, "L2 L2 L3"), C("FC-C14", 2, "L1 L1 L1"),
        ],
        tasks=[
            T("dc-212-preprocess", 4, 2, "E", "js"), T("v1-2.1.2-T1", 5, 3, "CE"), T("v1-2.1.2-T2", 5, 3, "CEF"),
            T("v1-2.1.2-T3", 5, 2, "CE"), T("dc-212-reference-design", 4, 1, "", "sl"),
            T("dc-212-circularity-check", 4, 1, "C", "js"), T("dc-212-transfer-test", 4, 1, "", "sl"),
            T("dc-212-specify-product", 4, 1, "", "sl"), T("v1-2.1.1-T2", 4, 2, "E"), T("v1-2.1.4-T1", 4, 2, "E"),
            T("v1-2.1.4-T2", 4, 2), T("v1-2.1.4-T3", 4, 1, "", "sl"), T("v1-2.1.1-T1", 3, 1, "E"),
            T("v1-2.1.5-T1", 4, 2, "E"), T("dc-215-uncertainty-depiction", 4, 1), T("v1-2.1.1-T3", 3, 1, "E"),
            T("v1-2.4.1-T1", 4, 1, "", "sl"), T("dc-241-diagnose-failure", 4, 1, "", "sl"),
            T("v1-2.6.1-T3", 5, 1, "C"), T("dc-09-independent-validation", 5, 1, "C", "sl"),
            T("dc-09-envelope-check", 4, 0.5, "", "sl"), T("dc-08-record-environment", 4, 0.5, "E"),
            T("v1-2.2.4-T1", 3, 1, "EF", "j"), T("dc-08-review-ai-code", 4, 0.5, "C", "js"),
            T("dc-11-retain-uncertainty", 4, 0.5), T("v1-2.2.5-T1", 3, 0.5, "E"), T("dc-07-generalize-copy", 4, 0.5, "C"),
            T("fc-gt-design-sample", 4, 0.5, "", "sl"), T("v1-2.3.2-T3", 3, 0.5), T("dc-214-spatial-standards", 3, 0.5, "", "l"),
            T("dc-22-decision-map", 3, 0.5, "", "l"), T("dc-13-sample-validate", 4, 0.5, "F", "j"),
        ],
        change=[
            X("v1-2.1.2-T2", "transforming", ["AI"],
              "Pretrained Earth-observation models and embeddings compress classification production; the analyst's "
              "time moves to training data, transfer tests and accuracy assessment.",
              signals=["sig/omb-ai-inventory-2025/remote-sensing"]),
            X("dc-212-transfer-test", "new", ["AI"], "Testing pretrained models on local ecosystems before use is new work."),
            X("dc-212-circularity-check", "new", ["AI"],
              "Checking that a product's training data and its validation reference are independent is new work."),
            X("v1-2.1.2-T3", "transforming", ["AI", "sensing-tech"], "Accuracy assessment grows as products multiply."),
            X("v1-2.1.5-T1", "transforming", ["AI"], "Generative tools draft maps and graphics; design for the decision stays."),
            X("dc-08-review-ai-code", "new", ["AI"], "Line-by-line review of AI-generated analysis code is new."),
        ],
        entry_from=["R02-field-resource-technician"],
        progresses_to=["R05-ground-truth-validation-steward"],
    ),
    Role(
        key="R05-ground-truth-validation-steward", tier="P1", area="core", wf="WF-MONITOR", levels=[J, S],
        life="emerging", title="Ground-truth and validation steward", use_tier="develop",
        alt=["validation lead", "reference data steward", "field validation specialist"],
        definition=("Emerging role that designs and stewards field reference data and validation samples for remote, "
                    "modelled and AI-generated products, codes the field causes of mismatch, calibrates observers and "
                    "states whether a product is fit for a stated use."),
        function=("Establish whether remote, modelled and automated products can be relied on, by collecting and "
                  "stewarding independent field reference evidence."),
        comps=[
            C("FS-C04", 5, "L2 L3", dist=True), C("FC-C02", 5, "L2 L3", dist=True), C("FC-C31", 4, "L2 L3"),
            C("DC-CAND-13", 4, "L2 L3"), C("FC-C03", 4, "L2 L3"), C("DC-CAND-09", 4, "L2 L3"),
            C("DC-CAND-15", 4, "L2 L3"), C("DC-CAND-03", 4, "L2 L3"),
            C("v1-1.4.3", 3, "L2 L3"), C("v1-4.1.1", 3, "L2 L2"), C("FC-C23", 3, "L2 L2"), C("DC-CAND-07", 3, "L2 L2"),
        ],
        tasks=[
            T("fc-gt-design-sample", 5, 2, "CE"), T("fc-gt-collect-blind", 5, 3, "CEF"), T("fc-gt-mismatch", 5, 2, "CE"),
            T("fc-gt-fitness", 5, 1, "C", "s"), T("fc-gt-calibration-plots", 4, 1, "", "s"), T("fc-gt-feedback", 4, 1, "E"),
            T("fs-c04-plan-reference", 5, 2, "C", "s"), T("fs-c04-collect-labels", 5, 2, "CEF"), T("fs-c04-relabel", 4, 1, "E"),
            T("fs-c04-maintain", 4, 1), T("fs-c04-generalize-sensitive", 4, 0.5, "C"),
            T("fs-c04-regional-validation", 4, 1, "", "s"), T("fc-qa-blind-check", 4, 1, "EF"),
            T("fc-qa-calibration-session", 4, 1, "", "s"), T("fc-qa-agreement", 4, 1), T("fc-det-review", 4, 1, "E"),
            T("fc-det-error-rates", 4, 1), T("fc-det-implausible", 4, 0.5), T("dc-13-sample-validate", 4, 1, "F"),
            T("dc-09-independent-validation", 4, 1, "", "s"), T("dc-15-label-reference", 4, 1, "E"),
            T("dc-15-build-set", 4, 0.5, "", "s"), T("dc-03-sample-design", 4, 0.5, "", "s"), T("v1-1.4.3-T2", 3, 0.5),
            T("v1-4.1.1-T1", 3, 1, "E"), T("fc-veg-validate-remote", 4, 1),
        ],
        change=[
            X("role", "new-role", ["AI", "sensing-tech"],
              "Validation of remote and AI products is forming as a distinct responsibility; no dedicated federal "
              "series exists (X4 NoTermFound).",
              signals=["sig/bls-ep-2025-35/19-4042/R05-ground-truth-validation-steward"]),
            X("fc-gt-collect-blind", "emerging", ["AI", "sensing-tech"], "Blind reference collection grows with product use."),
            X("fs-c04-plan-reference", "new", ["AI"], "Regional reference networks for Earth-observation models are new."),
            X("fc-det-review", "transforming", ["AI"], "Review queues for classifier detections replace manual screening."),
            X("dc-15-label-reference", "new", ["AI"], "Labelling reference sets blind to tool outputs is new work."),
        ],
        emerging={
            "signals": ["seed:sig/bls-ep-2025-35/15-1299/R05-ground-truth-validation-steward",
                        "seed:sig/bls-ep-2025-35/19-4042/R05-ground-truth-validation-steward"],
            "feeders": [
                {"role": "seed:R02-field-resource-technician", "competencyDeltas": [
                    {"competency": "seed:FC-C02", "fromLevel": "L2", "toLevel": "L3"},
                    {"competency": "seed:FS-C04", "toLevel": "L2"},
                    {"competency": "seed:DC-CAND-13", "fromLevel": "L2", "toLevel": "L3"}]},
                {"role": "seed:R03-monitoring-data-technician", "competencyDeltas": [
                    {"competency": "seed:FC-C02", "fromLevel": "L2", "toLevel": "L3"},
                    {"competency": "seed:DC-CAND-15", "toLevel": "L2"}]},
                {"role": "seed:R04-geospatial-remote-sensing-analyst", "competencyDeltas": [
                    {"competency": "seed:FC-C31", "toLevel": "L2"},
                    {"competency": "seed:FC-C03", "toLevel": "L2"}]}],
            "horizon": "1-3y",
            "scenarios": {"SC1": "up", "SC2": "up", "SC3": "external", "SC4": "down"},
            "counter": ("Validation is absorbed into vendor services with no agency field calibration, so the role "
                        "does not form inside public employers."),
        },
        entry_from=["R02-field-resource-technician", "R03-monitoring-data-technician",
                    "R04-geospatial-remote-sensing-analyst"],
    ),
    # ------------------------------------------------------------------ COR-3
    Role(
        key="R09-restoration-project-lead", tier="P1", area="core", wf="WF-BUILD", levels=[J, S, LD],
        life="established", title="Restoration and land stewardship project lead", use_tier="develop",
        alt=["restoration ecologist", "restoration project manager", "land stewardship coordinator"],
        definition=("Project role that plans, permits, delivers and monitors ecological restoration and land "
                    "stewardship projects: reading site history and reference conditions, adapting treatments to site "
                    "response, designing monitoring, working with landowners and partners, and managing contracts, "
                    "budgets and authorizations."),
        function=("Deliver restoration projects that meet stated ecological objectives, adapting treatments from "
                  "monitoring evidence within budget, schedule and authorizations."),
        comps=[
            C("v1-4.2.1", 5, "L2 L3 L4", dist=True), C("FC-C22", 4, "L2 L3 L3"), C("v1-1.1.5", 4, "L2 L3 L3"),
            C("DC-CAND-03", 4, "L2 L3 L3"), C("PS-C03", 4, "L2 L3 L3"), C("FC-C21", 4, "L2 L3 L3"),
            C("SC-C01", 4, "L2 L2 L3"), C("v1-3.1.4", 4, "L2 L3 L3"), C("v1-1.7.1", 4, "L2 L3 L3", dist=True),
            C("FC-C20", 3, "L2 L3 L3"), C("FC-C28", 3, "L2 L3 L3"), C("PS-C01", 3, "L2 L2 L2"), C("PS-C02", 3, "L2 L2 L2"),
            C("v1-4.2.2", 3, "L2 L2 L2"), C("v1-4.2.4", 2, "L2 L2 L2"), C("v1-1.8.5-A", 3, "L2 L2 L3"),
            C("v1-5.2.5", 3, "- L2 L3"), C("v1-4.4.1-A", 3, "L2 L3 L3"),
        ],
        tasks=[
            T("v1-4.2.1-T3", 5, 2, "C"), T("fc-resto-read-response", 5, 2, "CE"), T("fc-resto-lowtech", 4, 1, "E", "j"),
            T("v1-1.1.1-T3", 4, 1, "", "sl"), T("v1-1.1.5-T1", 4, 1, "E"), T("v1-1.1.5-T3", 4, 1),
            T("v1-1.7.1-T3", 5, 1, "C", "sl"), T("v1-1.7.1-T1", 4, 0.5, "", "sl"), T("fc-sitehist-read", 4, 1, "E"),
            T("fc-sitehist-reconcile", 4, 1), T("fc-sitehist-predict", 4, 0.5, "", "sl"), T("dc-03-questions", 5, 1, "C"),
            T("dc-03-sample-design", 4, 1, "", "sl"), T("dc-03-review-design", 4, 0.5, "", "sl"),
            T("v1-4.2.2-T2", 4, 0.5), T("v1-4.2.4-T2", 3, 0.5, "", "j"), T("fc-land-joint-visit", 4, 1, "E"),
            T("fc-land-volunteers", 3, 0.5), T("fc-camp-schedule", 4, 0.5), T("fc-camp-access", 4, 0.5, "E"),
            T("fc-lead-field-day", 4, 1, "", "js"), T("sc-prepare-authority-map", 4, 0.5, "", "sl"),
            T("v1-6.1.3-T3", 4, 0.5), T("v1-3.1.4-T1", 4, 1), T("v1-3.1.4-T2", 3, 0.5), T("lc-txf-write-approach", 4, 1, "", "sl"),
            T("lc-txf-draft-scope", 3, 0.5), T("v1-3.1.1-T1", 4, 1), T("v1-3.1.1-T3", 4, 0.5, "E"), T("v1-3.1.3-T1", 4, 0.5),
            T("lc-txe-map-system", 3, 0.5, "", "sl"), T("v1-5.2.5-T1", 3, 0.5, "", "sl"), T("fc-risk-briefing", 4, 0.3, "C"),
        ],
        change=[
            X("role", "transforming-role", ["fiscal", "policy-reform"],
              "Rescission of unobligated conservation funds and federal capacity reductions shift restoration delivery "
              "toward partners and contracts.", instruments=["obbba-ira-rescissions"],
              signals=["sig/foresight/ws-10-obbba-ira-rescissions"]),
            X("fc-resto-read-response", "transforming", ["sensing-tech"],
              "Drone and satellite imagery add response evidence between site visits; reading the site stays human."),
            X("lc-txf-write-approach", "transforming", ["AI"],
              "Proposal sections are increasingly AI-drafted; review against the solicitation and the organization's "
              "real capacity grows."),
            X("v1-1.7.1-T3", "emerging", ["climate"],
              "Deciding whether restoration to historical conditions is feasible becomes routine as sites shift state."),
            X("v1-4.2.1-T3", "stable", [], "Adapting treatments from site response is not compressed by current tools."),
        ],
        entry_from=["R01-conservation-corps-member", "R02-field-resource-technician"],
        progresses_to=["R10-environmental-review-specialist", "R13-resource-program-manager"],
    ),
    Role(
        key="R10-environmental-review-specialist", tier="P1", area="core", wf="WF-REVIEW", levels=[J, S, LD],
        life="established", title="Environmental review specialist", use_tier="develop",
        alt=["NEPA specialist", "environmental planner", "environmental review coordinator"],
        definition=("Role that determines the level of environmental review for proposed actions, prepares or directs "
                    "effects analyses, coordinates cooperating agencies and consultations, builds the administrative "
                    "record and writes decision documents under the governing agency procedures. AI drafting compresses "
                    "production; verification, record integrity and litigation resilience grow."),
        function=("Establish, document and defend what a proposed action's effects are and which review it requires, "
                  "so that the deciding official acts on a defensible record."),
        comps=[
            C("SL-C08", 5, "L2 L3 L4", dist=True), C("SC-C03", 5, "L2 L3 L4"), C("SC-C02", 5, "L2 L3 L4"),
            C("SC-C04", 4, "L2 L3 L4"), C("SC-C09", 4, "L2 L3 L4"), C("FH-C01", 4, "L2 L3 L3"),
            C("DB-C50", 4, "L2 L3 L3"), C("SC-C17", 4, "- L3 L4"), C("DC-CAND-16", 4, "L2 L3 L3"),
            C("DC-CAND-13", 4, "L2 L3 L3"),
            C("DB-C52", 3, "L2 L3 L3"), C("SC-C06", 3, "L2 L2 L3"), C("v1-5.2.1", 3, "L2 L2 L3"),
            C("DC-CAND-11", 3, "L2 L2 L3"), C("DB-C29", 3, "L2 L2 L2"), C("PS-C18", 3, "L2 L2 L3"),
            C("v1-7.1.3", 3, "L2 L3 L3"),
        ],
        tasks=[
            T("v1-6.1.4-T1", 5, 4, "CEF"), T("v1-6.1.4-T2", 5, 2, "CF"), T("v1-6.1.4-T3", 5, 2, "C", "sl"),
            T("sc-review-ai-drafted-sections", 5, 2, "CE"), T("sc-write-review-decision", 5, 1, "C", "sl"),
            T("sc-joint-review-document", 4, 1, "", "sl"), T("sc-determine-review-level", 5, 1, "C"),
            T("sc-screen-categorical-exclusion", 4, 2, "E"), T("sc-review-automated-screening", 4, 1, "C"),
            T("sc-adopt-other-agency-exclusion", 3, 0.5, "", "sl"), T("sc-evaluate-sponsor-document", 5, 1, "C", "sl"),
            T("sc-document-independent-evaluation", 4, 0.5, "", "sl"), T("sc-issue-preparer-standards", 4, 0.5, "", "sl"),
            T("v1-6.5.2-T1", 4, 1), T("sc-update-permitting-dashboard", 3, 0.5), T("sc-index-record-documents", 4, 1, "E"),
            T("sc-write-reasoned-explanation", 5, 1, "C", "sl"), T("sc-confirm-comment-responses", 4, 1),
            T("v1-6.4.4-T2", 4, 1, "F"), T("dc-13-check-comment-grouping", 4, 0.5),
            T("sc-identify-likely-claims", 4, 0.5, "", "sl"), T("sc-pre-issuance-record-review", 4, 0.5, "", "l"),
            T("sc-define-area-potential-effects", 4, 0.5), T("sc-assess-historic-effects", 4, 0.5),
            T("sc-prepare-biological-assessment", 4, 1), T("sc-review-ai-effects-determination", 4, 0.5),
            T("sc-compile-species-occurrence", 3, 0.5, "E"), T("v1-6.7.2-T1", 3, 0.5), T("sc-write-engagement-plan", 3, 0.5),
            T("dc-16-extract-table", 3, 0.5), T("sc-screen-preparer-conflicts", 4, 0.3, "C", "sl"),
        ],
        change=[
            X("role", "transforming-role", ["policy-reform"],
              "Review now runs under each agency's own procedures after CEQ's regulations were removed (effective "
              "Jan 8 2026) and after Seven County; the SPEED Act passed the House and is pending in the Senate.",
              instruments=["ceq-nepa-regs-removal", "seven-county", "speed-act", "nepa-fra-2023"]),
            X("v1-6.1.4-T1", "transforming", ["AI", "policy-reform"],
              "AI drafting compresses production of analysis sections; page and time limits tighten scope.",
              signals=["sig/omb-ai-inventory-2025/nepa-permitting", "sig/capability/draftnepabench-coding-agents",
                       "sig/deployment/permitting-ai-shared-services"]),
            X("sc-review-ai-drafted-sections", "new", ["AI"],
              "Verifying AI-drafted sections against the project record is new and grows with drafting tools."),
            X("v1-6.4.4-T2", "transforming", ["AI"], "Machine-assisted comment coding is deployed; tracing to source stays.",
              signals=["sig/omb-ai-inventory-2025/public-comment"]),
            X("sc-review-automated-screening", "new", ["AI"], "Batch review of automated exclusion screening is new."),
            X("sc-update-permitting-dashboard", "new", ["policy-reform"],
              "Public milestone dashboards and the permitting data standard add reporting work.",
              instruments=["ceq-permitting-data-standard", "fast-41"]),
            X("sc-determine-review-level", "transforming", ["policy-reform"],
              "Agency procedures and exclusion adoption change how review level is set."),
        ],
        entry_from=["R09-restoration-project-lead", "R12-environmental-compliance-inspector"],
        progresses_to=["R13-resource-program-manager", "R31-ai-assisted-review-lead"],
    ),
    Role(
        key="R11-environmental-permit-writer", tier="P1", area="core", wf="WF-AUTHORIZE", levels=[J, S, LD],
        life="established", title="Environmental permit writer", use_tier="develop",
        alt=["permit engineer", "permit specialist", "permit reviewer"],
        definition=("Regulatory role that reviews permit applications for completeness, derives limits and conditions "
                    "from technical standards and the record, drafts enforceable permits and fact sheets, negotiates "
                    "conditions, answers comments and administers issued permits, often within a delegated programme. "
                    "Drafting software compresses production; review of drafted conditions grows."),
        function=("Turn an application and the governing standards into permit conditions that are measurable, "
                  "enforceable and traceable to their legal and technical basis."),
        comps=[
            C("SL-C02", 5, "L2 L3 L4", dist=True), C("SC-C16", 5, "L2 L3 L4"), C("SC-C01", 4, "L2 L3 L3"),
            C("SC-C02", 4, "L2 L3 L3"), C("SC-C07", 4, "L2 L3 L4"), C("v1-5.5.2", 4, "L2 L3 L3"),
            C("SC-C14", 4, "L2 L3 L4"), C("SC-C12", 4, "L2 L3 L3"), C("DC-CAND-13", 4, "L2 L3 L3"),
            C("SL-C10", 3, "L2 L2 L3"), C("PS-C18", 3, "L2 L3 L3"), C("v1-7.1.3", 3, "L2 L3 L3"),
            C("DB-C29", 3, "L2 L2 L2"), C("SC-C17", 2, "- L3 L3"),
        ],
        tasks=[
            T("sc-check-permit-completeness", 5, 2, "CE"), T("sc-derive-permit-limits", 5, 3, "CE"),
            T("sc-draft-permit-fact-sheet", 5, 3, "CEF"), T("sc-review-ai-drafted-permit", 5, 2, "CF"),
            T("sc-respond-permit-comments", 4, 1), T("v1-6.4.2-T1", 4, 1), T("sc-test-terms-scenarios", 4, 1, "C"),
            T("sc-verify-ai-draft-instrument", 4, 0.5), T("v1-6.1.3-T2", 4, 1, "E"),
            T("sc-prepare-authority-map", 3, 0.5, "", "sl"), T("sc-negotiate-permit-conditions", 4, 1, "", "sl"),
            T("sc-prepare-negotiation-brief", 3, 0.5, "", "sl"), T("sc-prepare-delegated-workplan", 3, 0.5, "", "l"),
            T("sc-answer-oversight-objection", 4, 0.5, "", "sl"), T("sc-review-automated-permit-checks", 4, 1, "E"),
            T("v1-5.5.2-T3", 3, 1, "E"), T("v1-5.5.2-T2", 3, 0.5), T("sc-screen-regulatory-alerts", 3, 0.5),
            T("sc-update-procedure-version", 3, 0.5, "", "sl"), T("sc-index-record-documents", 4, 0.5, "E"),
            T("sc-write-reasoned-explanation", 4, 0.5, "", "sl"), T("sc-answer-compliance-questions", 3, 0.5),
            T("sc-recuse-covered-matter", 4, 0.2, "C"), T("v1-7.2.1-T2", 4, 0.5, "F"),
        ],
        change=[
            X("sc-draft-permit-fact-sheet", "transforming", ["AI"],
              "Permit-drafting software and AI first drafts compress production; the writer's time moves to "
              "specifying and checking conditions.", signals=["sig/omb-ai-inventory-2025/genai-drafting",
                                                              "sig/omb-ai-inventory-2025/cots-genai-drafting-scale"]),
            X("sc-review-ai-drafted-permit", "new", ["AI"], "Reviewing AI-drafted permits against the record is new."),
            X("sc-review-automated-permit-checks", "new", ["AI", "policy-reform"],
              "Electronic permitting adds automated completeness checks that writers confirm or override.",
              instruments=["permitting-tech-pm-2025", "epermit-act"]),
            X("sc-check-permit-completeness", "transforming", ["AI", "policy-reform"],
              "Completeness review is partly automated in electronic permitting systems."),
            X("sc-derive-permit-limits", "stable", [], "Deriving limits from standards and the record stays with the writer."),
        ],
        entry_from=["R12-environmental-compliance-inspector/state", "R03-monitoring-data-technician"],
        progresses_to=["R13-resource-program-manager"],
        note=("Mirror links (ADR-0017 section 4): the regulated-party mirror is R37 (facility compliance) and the "
              "applicant-side preparer is the R37 applicant-preparer variant; both pairs are recorded in X11 "
              "(emst:mirrorRole) and in generated/mirror_links.json."),
    ),
    Role(
        key="R12-environmental-compliance-inspector", tier="P1", area="core", wf="WF-ENFORCE", levels=[E, J, S],
        life="established", title="Environmental compliance inspector", use_tier="develop",
        alt=["environmental inspector", "compliance officer", "environmental protection specialist (inspections)"],
        definition=("Regulatory field role that plans and conducts compliance inspections, collects evidence under "
                    "custody, writes findings of fact, selects the response the enforcement policy sets, supports "
                    "cases and gives compliance assistance. Monitoring data and automated flags increasingly target "
                    "inspections; on-site inspection and evidence stay human."),
        function=("Establish, with defensible evidence, whether regulated facilities and sites meet their permits and "
                  "rules, and start the response the enforcement policy requires."),
        comps=[
            C("SL-C03", 5, "L1 L2 L3", dist=True), C("SL-C04", 4, "- L2 L3"), C("DB-C25", 4, "- L2 L3"),
            C("FC-C24", 4, "L1 L2 L3"), C("SC-C02", 4, "L1 L2 L3"), C("v1-4.4.4-A", 5, "L1 L2 L2"),
            C("PS-C18", 4, "L1 L2 L3"), C("v1-4.4.1-B", 4, "L1 L2 L3"), C("DC-CAND-13", 4, "L1 L2 L3"),
            C("SL-C10", 3, "L1 L2 L2"), C("FC-C23", 3, "L1 L2 L2"), C("v1-2.2.3", 3, "L1 L2 L2"),
            C("v1-7.1.3", 3, "L1 L2 L3"), C("DB-C29", 3, "L1 L2 L2"), C("IO-C01", 3, "- - L3"), C("v1-4.1.3", 2, "L1 L1 L1"),
        ],
        tasks=[
            T("sc-plan-inspection", 5, 2, "CE"), T("v1-6.1.2-T1", 5, 4, "CEF"), T("sc-collect-inspection-evidence", 5, 2, "CE"),
            T("sc-write-inspection-report", 5, 3, "CE"), T("sc-select-enforcement-response", 4, 1, "", "js"),
            T("v1-1.2.4-T1", 4, 1, "EF"), T("fc-coc-complete", 5, 1, "CE"), T("fc-qc-collect", 4, 0.5, "E"),
            T("fc-qc-defend", 4, 0.3, "", "s"), T("v1-6.1.5-T1", 4, 1, "", "js"), T("v1-6.1.5-T2", 4, 1, "", "js"),
            T("v1-6.1.5-T3", 4, 0.3, "", "s"), T("sc-calculate-civil-penalty", 3, 0.5, "", "s"),
            T("sc-review-anomaly-flags", 4, 1, "C", "js"), T("sc-verify-reported-values", 4, 1, "C"),
            T("sc-rank-facilities-inspection", 3, 0.5, "", "s"), T("sc-evaluate-targeting-method", 3, 0.3, "", "s"),
            T("v1-2.2.3-T2", 3, 0.5, "EF"), T("v1-7.2.1-T2", 4, 0.5, "F", "js"), T("sc-assistance-site-visit", 3, 0.5, "", "js"),
            T("sc-answer-compliance-questions", 3, 0.5), T("v1-4.4.4-T1", 5, 0.3, "CE"), T("fc-haz-hasp", 5, 0.3, "CE"),
            T("fc-haz-energized", 5, 0.2, "CE"), T("lc-txc-exercise-stop-work", 5, 0.2, "CE"),
            T("sc-recuse-covered-matter", 4, 0.2, "C"), T("sc-disclose-assignment-interests", 4, 0.2, "E"),
            T("lc-txd-rate-performance", 3, 0.3, "", "s"), T("fc-txa-field-check", 4, 0.5, "F"),
            T("sc-index-record-documents", 4, 0.5, "E"),
        ],
        change=[
            X("sc-review-anomaly-flags", "new", ["AI", "sensing-tech"],
              "Automated anomaly flags in facility monitoring reports are reviewed before inspection.",
              signals=["sig/omb-ai-inventory-2025/inspection-compliance"]),
            X("sc-rank-facilities-inspection", "transforming", ["AI"], "Data-driven targeting changes inspection selection."),
            X("sc-write-inspection-report", "transforming", ["AI"],
              "Drafted inspection notes compress report production; findings of fact stay the inspector's."),
            X("sc-verify-reported-values", "transforming", ["sensing-tech", "policy-reform"],
              "Electronic reporting and continuous monitoring make independent checks of reported values routine.",
              instruments=["npdes-ereporting-rule"]),
            X("v1-6.1.2-T1", "stable", [], "On-site inspection is not compressed by current tools."),
            X("role", "transforming-role", ["workforce-capacity", "fiscal"],
              "Federal environmental staffing fell sharply in 2025-26; more inspection work rests on state and local "
              "programmes.", signals=["sig/headcount/epa-12849-jan-2026"]),
        ],
        entry_from=["R03-monitoring-data-technician"],
        progresses_to=["R11-environmental-permit-writer/state", "R23-enforcement-case-manager",
                       "R37-facility-environmental-compliance-specialist/private"],
        note=("Mirror link (ADR-0017 section 4): the regulated-party mirror is R37; recorded in X11 (TR-02, "
              "emst:mirrorRole) and in generated/mirror_links.json."),
    ),
    Role(
        key="R13-resource-program-manager", tier="P1", area="core", wf="WF-MANAGE", levels=[S, LD, ST],
        life="established", title="Natural resource and environmental programme manager", use_tier="develop",
        alt=["programme manager", "division manager", "district ranger"],
        definition=("Management role that plans and justifies programme budgets, briefs decision-makers, manages land "
                    "or regulatory programme plans and agreements, tracks instrument and policy change, and protects "
                    "the programme's capacity to form and keep skilled staff, including how AI tools are governed."),
        function=("Keep an environmental or natural resource programme funded, lawful, staffed and able to deliver "
                  "its decisions over budget and policy cycles."),
        comps=[
            C("SC-C10", 5, "L3 L4 L4", dist=True), C("v1-6.2.3", 4, "L3 L4 L4"), C("SC-C18", 5, "L3 L4 L4"),
            C("v1-7.2.2", 4, "L3 L4 L4"), C("FH-C07", 4, "L3 L3 L4"), C("SC-C08", 4, "L3 L4 L4"),
            C("v1-3.1.4", 4, "L3 L4 L4"), C("SC-C11", 4, "L3 L4 L5"), C("PS-C03", 4, "L3 L3 L4"),
            C("DC-CAND-21", 4, "- L4 L5"),
            C("SC-C12", 3, "L3 L3 L4"), C("v1-6.4.5", 3, "L3 L4 L4"), C("IO-C01", 3, "L3 L4 L4"),
            C("v1-1.8.5-A", 3, "L3 L3 L4"), C("v1-4.4.1-B", 3, "L3 L4 L4"), C("PS-C02", 3, "L3 L3 L3"),
            C("DC-CAND-20", 3, "L3 L3 L3"), C("DC-CAND-14", 3, "- L3 L3"),
        ],
        tx_floor={"DC-CAND-02": "L2 L3 L4", "DC-CAND-01": "L2 L2 L3", "DC-CAND-13": "L2 L3 L3", "DC-CAND-05": "L2 L2 L3"},
        tasks=[
            T("sc-prepare-budget-justification", 5, 3, "CE"), T("sc-reconcile-appropriations", 4, 2, "E"),
            T("sc-plan-funding-lapse", 4, 1, "C"), T("sc-brief-appropriators", 4, 1, "", "lx"),
            T("sc-design-fee-schedule", 3, 0.5, "", "lx"), T("sc-assess-reversal-risk", 4, 1, "", "lx"),
            T("sc-advise-instrument-choice", 4, 0.5, "", "x"), T("sc-classify-program-instruments", 3, 0.5),
            T("sc-write-decision-memo", 5, 2, "CE"), T("sc-brief-decision-maker", 5, 1, "CE"), T("sc-record-frank-advice", 5, 0.5, "C"),
            T("sc-prepare-staff-report", 4, 1), T("v1-6.4.5-T1", 3, 1, "E"), T("v1-6.4.5-T2", 4, 0.5, "", "lx"),
            T("sc-write-change-notice", 4, 1, "E"), T("sc-train-on-regulatory-change", 3, 0.5), T("v1-6.5.3-T1", 4, 1),
            T("v1-6.5.3-T3", 4, 1, "E"), T("v1-6.2.3-T1", 5, 2, "C"), T("sc-write-plan-components", 4, 1),
            T("v1-3.1.4-T3", 4, 1, "E"), T("lc-txd-identify-single-incumbent", 4, 1, "C"), T("lc-txd-prepare-handover", 4, 0.5),
            T("v1-7.2.2-T1", 4, 1, "", "lx"), T("lc-txd-advise-ai-adoption", 4, 0.5, "", "lx"),
            T("lc-txd-plan-field-rotations", 4, 0.5), T("v1-3.1.3-T3", 4, 1, "E"), T("dc-21-measures", 3, 0.5, "", "x"),
            T("v1-3.5.5-T3", 4, 0.5, "", "lx"), T("dc-20-requirements", 3, 0.5, "", "l"),
            T("lc-txc-design-learning-process", 3, 0.5, "", "l"), T("lc-txe-compare-interventions", 3, 0.5, "", "lx"),
            T("lc-txd-certify-qualification", 3, 0.3, "", "l"), T("lc-txf-decide-pursuit", 3, 0.3, "", "lx"),
        ],
        change=[
            X("role", "transforming-role", ["fiscal", "workforce-capacity", "demographic"],
              "The federal civilian workforce fell about 12% (Sep 2024 - Jan 2026); EPA's roughly 2,000 year-end-2025 "
              "departures had a 30.3-year median service, so knowledge continuity becomes programme work.",
              signals=["sig/headcount/federal-civilian-minus-12pct", "sig/headcount/epa-12849-jan-2026"]),
            X("lc-txd-identify-single-incumbent", "new", ["demographic", "workforce-capacity"],
              "Identifying single-incumbent knowledge before departures is new routine work."),
            X("sc-plan-funding-lapse", "transforming", ["fiscal"], "Funding-lapse and rescission planning becomes recurrent."),
            X("v1-3.5.5-T3", "new", ["AI", "policy-reform"],
              "Programme managers set rules that keep consequential AI-assisted decisions with accountable people.",
              instruments=["omb-m-25-21"]),
            X("sc-assess-reversal-risk", "emerging", ["policy-reform"], "Instrument reversal risk is assessed routinely."),
            X("sc-write-decision-memo", "transforming", ["AI"], "Drafting tools compress memo production; accountability stays."),
        ],
        entry_from=["R09-restoration-project-lead", "R10-environmental-review-specialist", "R11-environmental-permit-writer"],
        progresses_to=["R35-knowledge-continuity-lead"],
    ),
]

# ---------------------------------------------------------------------- COR-2 (forest module: fire competencies are
# module records, so these profiles live in data/v2/modules/forest/roles/; core roles never link to them)
ROLES += [
    Role(
        key="R06-wildland-fire-operations", tier="P1", area="forest", wf="WF-RESPOND", levels=[E, J, S, LD],
        life="established", title="Wildland fire operations (crew to supervisor)", use_tier="develop",
        alt=["wildland firefighter", "fire crew member", "engine or hand crew supervisor"],
        definition=("Operational fire role from crew member to crew supervisor: constructing and holding fireline, "
                    "firing and mop-up, saw and hand-tool work, fire weather and behaviour observation, crew safety "
                    "and emergency response, and, at senior levels, size-up, tactical direction and crew development. "
                    "Position qualifications are credential gates, not levels."),
        function=("Contain and control wildland fire safely with ground tactics, keeping crews within the safety "
                  "margins of observed fire behaviour."),
        comps=[
            C("v1-4.3.1", 5, "L1 L2 L3 L4", dist=True), C("v1-4.4.1-A", 5, "L1 L2 L3 L4"), C("v1-4.5.2", 5, "L1 L2 L3 L3"),
            C("v1-4.5.1", 4, "L1 L2 L2 L2"), C("FC-C18", 4, "L1 L2 L3 L3"), C("v1-4.3.4", 4, "L1 L2 L3 L3"),
            C("FC-C20", 4, "- L2 L3 L4"), C("v1-4.4.5", 4, "L1 L2 L3 L3"), C("v1-4.4.2", 4, "L1 L2 L2 L3"),
            C("v1-4.4.1-B", 4, "L1 L2 L3 L4"),
            C("v1-4.3.2", 3, "L1 L2 L2 L3"), C("FC-C26", 3, "L1 L1 L2 L2"), C("v1-4.5.3-A", 3, "L1 L2 L2 L2"),
            C("v1-4.5.5", 2, "L1 L1 L1 L1"), C("IO-C01", 3, "- - L3 L3"), C("v1-4.3.5", 2, "- L1 - -"),
            C("DB-C29", 2, "- - L2 L2"),
        ],
        tasks=[
            T("v1-4.3.1-T1", 5, 4, "CEF", "ej"), T("v1-4.3.1-T3", 4, 3, "EF", "ej"), T("v1-4.3.1-T2", 5, 1, "C", "jsl"),
            T("db-4.3.1-t4", 5, 1, "C", "sl"), T("db-4.3.1-t5", 5, 1, "C", "sl"), T("v1-4.3.4-T1", 4, 1, "EF", "ej"),
            T("v1-4.3.4-T3", 4, 0.5, "", "sl"), T("db-4.3.4-t4", 4, 0.5, "", "sl"), T("v1-4.2.3-T1", 4, 1, "F", "ej"),
            T("v1-4.2.3-T3", 4, 0.5, "", "js"), T("v1-4.5.2-T1", 5, 2, "CF", "ejs"), T("fc-saw-preuse", 5, 0.5, "CE"),
            T("fc-saw-decline", 5, 0.3, "C"), T("fc-saw-evaluate", 4, 0.3, "", "sl"), T("v1-4.5.1-T1", 5, 2, "CEF", "ej"),
            T("v1-4.5.1-T2", 3, 0.5, "E", "ej"), T("fc-risk-briefing", 5, 0.5, "C", "sl"), T("fc-risk-stopwork", 5, 0.3, "CE"),
            T("fc-risk-heat-recognize", 5, 0.3, "CE"), T("fc-risk-heat-smoke", 4, 0.3, "", "sl"),
            T("lc-txc-review-generated-briefing", 4, 0.2, "", "sl"), T("v1-4.4.5-T1", 5, 0.3, "CE"),
            T("v1-2.3.5-T1", 4, 0.3, "E"), T("v1-4.4.2-T1", 5, 0.3, "CE"), T("v1-4.4.2-T2", 5, 0.2, "C", "sl"),
            T("fc-nav-device-failure", 4, 0.3, "E"), T("v1-4.5.3-T2", 4, 0.5, "CE"), T("fc-tree-worksite", 5, 0.5, "CE"),
            T("fc-lead-field-day", 4, 1, "", "sl"), T("fc-lead-readiness", 4, 0.5, "", "l"), T("fc-lead-aar", 4, 0.5, "", "sl"),
            T("v1-4.5.5-T1", 3, 0.5, "E"), T("v1-4.3.5-T2", 3, 0.5, "", "j"), T("lc-txd-rate-performance", 4, 0.3, "", "sl"),
            T("lc-txe-answer-public-questions", 3, 0.2, "", "sl"),
        ],
        change=[
            X("role", "transforming-role", ["policy-reform", "workforce-capacity"],
              "Federal wildland fire is being consolidated in the U.S. Wildland Fire Service, and the January 2027 "
              "standards align USWFS and USFS federal qualifications.",
              instruments=["uswfs-so-3448", "wildland-fire-quals-alignment"]),
            X("role", "skill-shift", ["climate"],
              "Workload grows with fire activity: the 2026 season ran well above the ten-year average.",
              signals=["sig/foresight/ws-36-fire-season-2026"]),
            X("db-4.3.1-t4", "transforming", ["sensing-tech", "AI"],
              "Satellite and camera detection reaches the size-up earlier; ground size-up of fuels and values stays.",
              signals=["sig/omb-ai-inventory-2025/fire-smoke"]),
            X("lc-txc-review-generated-briefing", "new", ["AI"],
              "Generated hazard briefings are checked on site before delivery."),
            X("v1-4.3.4-T1", "transforming", ["sensing-tech"],
              "Automated stations supply indices; hand calculation is kept as a formation task (WP-07 by-hand quota)."),
            X("v1-4.3.1-T1", "stable", [], "Fireline construction is not compressed by current tools."),
        ],
        entry_from=["R01-conservation-corps-member", "R02-field-resource-technician"],
        progresses_to=["R07-fuels-prescribed-fire-specialist", "R08-fire-intelligence-analyst"],
    ),
    Role(
        key="R07-fuels-prescribed-fire-specialist", tier="P1", area="forest", wf="WF-BUILD", levels=[J, S, LD],
        life="established", title="Fuels and prescribed fire specialist", use_tier="develop",
        alt=["fuels specialist", "prescribed fire specialist", "burn boss"],
        definition=("Role that assesses fuels, designs and supervises fuels treatments, writes and executes burn plans, "
                    "makes go/no-go decisions, plans smoke management with air regulators, evaluates fire effects and "
                    "treatment effectiveness, and works with landowners and partners across ownerships."),
        function=("Reduce wildfire hazard and restore fire-adapted conditions through fuels treatments and prescribed "
                  "fire executed within prescription and air-quality limits."),
        comps=[
            C("v1-4.3.2", 5, "L2 L3 L4", dist=True), C("v1-4.3.3", 5, "L2 L3 L4", dist=True), C("v1-4.3.4", 4, "L2 L3 L3"),
            C("DB-C15", 4, "L2 L3 L3"), C("v1-4.4.1-A", 5, "L2 L3 L4"), C("FC-C20", 4, "L2 L3 L4"),
            C("DB-C29", 4, "L2 L2 L3"), C("v1-4.4.1-B", 4, "L2 L3 L4"),
            C("FC-C28", 3, "L2 L3 L3"), C("FC-C02", 3, "L2 L2 L3"), C("v1-4.1.1", 3, "L2 L2 L2"), C("FC-C22", 3, "L2 L3 L3"),
            C("FC-C21", 3, "L2 L3 L3"), C("FC-C14", 3, "L1 L2 L2"), C("v1-4.5.2", 3, "L2 L2 L2"), C("PS-C03", 2, "- L2 L3"),
            C("IO-C01", 3, "- L3 L3"),
        ],
        tasks=[
            T("v1-4.3.2-T1", 5, 3, "C"), T("v1-4.3.2-T2", 5, 1, "CF", "sl"), T("v1-4.2.3-T1", 4, 1, "E", "j"),
            T("v1-4.2.3-T2", 5, 2, "CE"), T("v1-4.2.3-T3", 5, 1, "C"), T("db-4.3.2-t4", 4, 0.5, "C", "sl"),
            T("fc-uas-ignition", 4, 0.5, "", "js"), T("v1-4.3.2-T3", 4, 1), T("v1-4.3.3-T1", 5, 2, "CE"),
            T("db-4.3.3-t4", 4, 1, "EF", "j"), T("v1-4.3.3-T2", 4, 2), T("v1-4.3.3-T3", 4, 1), T("v1-4.3.4-T2", 4, 1, "E"),
            T("DB-C15-T2", 5, 1, "C"), T("DB-C15-T5", 3, 0.5), T("v1-4.1.1-T1", 3, 1, "", "j"), T("fc-sitehist-read", 3, 0.5),
            T("fc-camp-schedule", 4, 0.5), T("fc-camp-access", 3, 0.5), T("fc-land-joint-visit", 3, 0.5, "", "sl"),
            T("lc-txe-answer-public-questions", 3, 0.5, "", "sl"), T("lc-txe-draft-advisory", 3, 0.3, "", "sl"),
            T("fc-risk-briefing", 5, 0.5, "C"), T("fc-lead-field-day", 4, 0.5), T("v1-4.5.2-T1", 4, 0.5, "C", "j"),
            T("v1-3.1.1-T3", 3, 0.5, "", "sl"), T("lc-txd-rate-performance", 3, 0.3, "", "l"), T("fc-gt-mismatch", 3, 0.3),
            T("lc-txc-exercise-stop-work", 5, 0.2, "C"),
        ],
        change=[
            X("db-4.3.3-t4", "new", ["sensing-tech", "AI"],
              "Remotely sensed fuel maps replace much plot sampling; field verification of fuel-model assignments is "
              "new routine work.", signals=["sig/openlmp/term-remote-sensing-lidar-drone-2012-vs-1982"]),
            X("v1-4.3.3-T1", "transforming", ["sensing-tech"], "Fuels assessment shifts from plots to verifying mapped fuels."),
            X("db-4.3.2-t4", "emerging", ["automation-robotics", "policy-reform"],
              "Aerial ignition by uncrewed aircraft is spreading; beyond-visual-line-of-sight rules are pending (watch).",
              instruments=["faa-part-108"], signals=["sig/policy/faa-part-108-final-at-oira"]),
            X("v1-4.3.2-T1", "transforming", ["AI"],
              "Burn plan sections are increasingly drafted from templates or AI; prescription judgment stays."),
            X("DB-C15-T2", "transforming", ["sensing-tech", "AI"], "Smoke dispersion forecasts improve; receptor judgment stays."),
            X("role", "skill-shift", ["climate", "workforce-capacity"],
              "Fuels and prescribed fire workload grows with fire activity while federal capacity has fallen.",
              signals=["sig/foresight/ws-36-fire-season-2026", "sig/headcount/usfs-gt25pct-2024-09-to-2026-01"]),
        ],
        entry_from=["R06-wildland-fire-operations", "R09-restoration-project-lead"],
    ),
    Role(
        key="R08-fire-intelligence-analyst", tier="P1", area="forest", wf="WF-ASSESS", levels=[J, S, LD],
        life="emerging", title="Fire intelligence analyst (continuous operations)", use_tier="develop",
        alt=["fire behaviour analyst", "predictive services analyst", "fire intelligence specialist"],
        definition=("Emerging year-round role that fuses satellite, camera, sensor, weather and resource data into "
                    "operational fire intelligence, adjudicates automated detections, predicts spread with stated "
                    "confidence, tracks forecast skill and briefs duty officers and incident leaders."),
        function=("Give fire managers timely, validated intelligence on fire activity and expected behaviour, with "
                  "its confidence stated, so that resources are ordered on evidence."),
        comps=[
            C("FS-C05", 5, "L2 L3 L4", dist=True), C("v1-4.3.4", 5, "L2 L3 L4"), C("DC-CAND-12", 4, "L2 L3 L4"),
            C("DC-CAND-11", 4, "L2 L3 L4"), C("DB-C29", 4, "L2 L3 L3"), C("FC-C02", 4, "L2 L2 L3"),
            C("v1-2.1.2", 4, "L2 L3 L3"), C("DC-CAND-13", 4, "L2 L3 L3"),
            C("DC-CAND-22", 3, "L2 L3 L3"), C("DC-CAND-09", 3, "L2 L3 L3"), C("v1-2.1.4", 3, "L2 L2 L3"),
            C("DB-C15", 2, "- L2 L2"),
        ],
        tasks=[
            T("FS-C05-T1", 5, 4, "CE"), T("FS-C05-T2", 5, 2, "CEF"), T("FS-C05-T3", 5, 2, "C"), T("FS-C05-T4", 4, 1),
            T("v1-4.3.4-T2", 5, 2, "CEF"), T("db-4.3.4-t4", 4, 1), T("v1-4.3.4-T3", 4, 1, "", "sl"),
            T("dc-12-skill-tracking", 4, 1, "", "sl"), T("dc-12-fitness-requirements", 4, 0.5, "", "l"),
            T("dc-12-restrict-retire", 4, 0.5, "", "l"), T("v1-2.7.3-T3", 3, 1), T("dc-11-incident-confidence-briefing", 5, 1, "C"),
            T("dc-11-quantify-sources", 4, 0.5), T("fc-txa-field-check", 4, 0.5, "F", "j"), T("fc-gt-fitness", 3, 0.5, "", "sl"),
            T("v1-2.1.2-T1", 4, 1, "E"), T("v1-2.1.4-T1", 3, 0.5), T("dc-22-decision-map", 3, 0.5, "", "l"),
            T("lc-txe-prepare-message-map", 3, 0.5, "", "sl"), T("DB-C15-T4", 3, 0.5, "", "sl"), T("dc-09-envelope-check", 3, 0.5),
            T("fc-txa-escalate", 4, 0.3, "C"),
        ],
        change=[
            X("role", "new-role", ["sensing-tech", "AI", "policy-reform"],
              "Year-round fire intelligence is forming as satellite constellations and detection networks come "
              "online and federal fire is consolidated.",
              instruments=["uswfs-so-3448"], signals=["sig/foresight/ws-31-firesat-operational"]),
            X("FS-C05-T1", "new", ["AI", "sensing-tech"], "Continuous multi-source fusion is new work."),
            X("FS-C05-T2", "new", ["AI", "sensing-tech"], "Adjudicating automated detections before ordering is new.",
              signals=["sig/omb-ai-inventory-2025/fire-smoke"]),
            X("v1-4.3.4-T2", "transforming", ["AI"],
              "Spread models run continuously; hand-worked predictions are kept as a formation check (WP-07)."),
            X("dc-12-skill-tracking", "new", ["AI"], "Tracking forecast skill against observed outcomes is new."),
        ],
        emerging={
            "signals": ["seed:sig/bls-ep-2025-35/15-1299/R08-fire-intelligence-analyst",
                        "seed:sig/foresight/ws-31-firesat-operational"],
            "feeders": [
                {"role": "seed:R06-wildland-fire-operations", "competencyDeltas": [
                    {"competency": "seed:v1-4.3.4", "fromLevel": "L3", "toLevel": "L3"},
                    {"competency": "seed:FS-C05", "toLevel": "L2"},
                    {"competency": "seed:DC-CAND-11", "fromLevel": "L1", "toLevel": "L2"}]},
                {"role": "seed:R04-geospatial-remote-sensing-analyst", "competencyDeltas": [
                    {"competency": "seed:v1-4.3.4", "toLevel": "L2"},
                    {"competency": "seed:FS-C05", "toLevel": "L2"}]}],
            "horizon": "1-3y",
            "scenarios": {"SC1": "up", "SC2": "up", "SC3": "reshape", "SC4": "flat"},
            "counter": ("The function stays inside incident fire-behaviour and long-term analyst positions with no "
                        "year-round staffing."),
        },
        entry_from=["R06-wildland-fire-operations", "R04-geospatial-remote-sensing-analyst"],
        note="Resolves the WFIC-1 gate (ADR-0020): no separate profession family, no WFIC-2/3.",
    ),
]
