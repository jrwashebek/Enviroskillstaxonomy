"""Batch E: core Data Craft practice competencies needed by the P1 roles (R03, R04, R05, R08, R10-R13; R31)."""
from lib import df
from spec import T, build

S = []
SEEDT = lambda c, n: f"seed:v1-{c}-T{n}"  # noqa: E731

# ------------------------------------------------------------------ v1 2.1.2 remote sensing (rewrite; absorbs DC-CAND-10)
C = "seed:v1-2.1.2"
S.append(dict(
    id=C, seed=True, prefix="ind-v1-2.1.2", span=("L1", "L4"), evidence="E", sources=["DC-023", "DC-025", "DC-028", "DC-001"],
    title="Analyze remotely sensed data to map and monitor environmental conditions",
    alt=["Remote sensing data analysis", "Earth-observation analysis"],
    definition="The capability to turn satellite, airborne and drone imagery and other remotely sensed data into maps and change estimates of environmental condition with a stated accuracy. It covers preprocessing, classification, change detection, accuracy assessment against independent reference data and, at higher levels, transfer testing of pretrained Earth-observation models and embeddings. Platform operation is L4 fluency.",
    statement="Processes and interprets satellite, airborne and drone imagery and other remotely sensed data to map land cover, vegetation, water, disturbance and change; designs accuracy assessment against independent reference data; reports accuracy by class and condition; and, where pretrained Earth-observation models or embeddings are used, tests their transfer to local ecosystems and guards against circular validation.",
    note="Rewritten by WP-04. Absorbs DC-CAND-10 (EO foundation models and embeddings as L3 indicators; model families in L4) per candidate_disposition merge-into v1:2.1.2. Accuracy assessment with independent reference data is the anchor (DC disposition).",
    tasks=[
        T("t1", SEEDT("2.1.2", 1), "Interpret satellite and aerial imagery to detect changes in vegetation, soil or water condition across a management area between two dates.", "WF-ASSESS", "remote-capable", "partial", rewrite=True),
        T("t2", SEEDT("2.1.2", 2), "Classify preprocessed multispectral imagery into land-cover types using training data whose collection method and date are documented.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("t3", SEEDT("2.1.2", 3), "Assess the accuracy of a remotely sensed map against independent field reference data, reporting error by class and condition.", "WF-MONITOR", "remote-capable", "partial", rewrite=True),
        T("pre", "seed:dc-212-preprocess", "Preprocess imagery for analysis by correcting geometry, radiometry and cloud or shadow contamination, documenting each step and its parameters.", "WF-ASSESS", "remote", "no"),
        T("ref", "seed:dc-212-reference-design", "Design the sample of independent reference sites for a map accuracy assessment so that every class and condition of interest is represented.", "WF-PLAN", "remote-capable", "partial"),
        T("transfer", "seed:dc-212-transfer-test", "Test the transfer of a pretrained Earth-observation model or embedding to a local ecosystem against independent reference data before using its outputs.", "WF-MONITOR", "remote", "partial", lifecycle="emerging", sources=["DC-023", "DC-025", "DC-028"], evidence="E"),
        T("circ", "seed:dc-212-circularity-check", "Check whether a map product shares training data with the reference used to validate it, choosing an independent reference when it does.", "WF-MONITOR", "remote", "partial", sources=["DC-028"], evidence="E"),
        T("spec", "seed:dc-212-specify-product", "Specify a remote-sensing product for a programme decision, stating its classes, minimum mapping unit, accuracy targets and update frequency.", "WF-PLAN", "remote", "partial"),
    ],
    inds=[
        ("L1", "Identifies vegetation, water and disturbance features on supplied imagery, matching a reviewer's interpretation on a check set within the set tolerance.", "u", ["ws", "brm"], ["t1"]),
        ("L1", "Documents the date, sensor class, resolution and processing applied to each image used, so that a reviewer can repeat the analysis.", "u", ["ra"], ["pre"]),
        ("L2", "Classifies imagery into the classes a project needs, reporting an error matrix from independent reference data held out from training.", "u", ["ws"], ["t2", "t3"], {"attr": "gui"}),
        ("L2", "Detects change between image dates with a stated method, separating real change from differences caused by season, sensor or illumination.", "u", ["ws"], ["t1"], {"attr": "cpx"}),
        ("L3", "Designs a reference-site sample for accuracy assessment that represents every class and condition, so that error can be reported by stratum.", "u", ["ws", "pr"], ["ref"], {"attr": "cpx"}),
        ("L3", "Tests a pretrained Earth-observation model or embedding against independent local reference data before use, documenting where accuracy falls below the requirement.", "a", ["ws"], ["transfer"], {"attr": "aug"}),
        ("L3", "Checks that the reference data used for validation were not used to train the product being assessed, replacing them when they were.", "a", ["ws", "pr"], ["circ"], {"attr": "kno"}),
        ("L4", "Specifies remote-sensing products for a programme, stating classes, minimum mapping unit, accuracy targets and update frequency tied to the decisions served.", "u", ["pr"], ["spec"], {"attr": "sco"}),
        ("L4", "Sets accuracy-assessment standards for a programme's remote-sensing products, documenting the reference-data requirements for each product type.", "u", ["pr"], ["spec", "ref"], {"attr": "gui"}),
    ]))

# ------------------------------------------------------------------ v1 2.1.4 spatial analysis (rewrite; absorbs 2.1.1 core, 2.7.5)
C = "seed:v1-2.1.4"
S.append(dict(
    id=C, seed=True, prefix="ind-v1-2.1.4", span=("L1", "L4"),
    title="Conduct spatial analysis and modelling of environmental data", alt=["Spatial analysis and modeling", "GIS analysis"],
    definition="The capability to answer environmental questions with spatial data: choosing data models, coordinate reference systems and topology rules, running overlay, proximity, connectivity, suitability, terrain and surface analyses, and building spatial models whose assumptions and accuracy are stated. Operating a particular GIS product is L4 fluency.",
    statement="Answers environmental questions with spatial data: chooses data models, coordinate reference systems and topology rules; runs overlay, proximity, connectivity, suitability, terrain and surface analyses; builds spatial models whose assumptions and positional and attribute accuracy are stated; and documents workflows so that results can be reproduced and defended.",
    note="Rewritten by WP-04. Absorbs the durable core of v1 2.1.1 (spatial data models, reference systems, topology, query logic; GIS platforms to L4 seed:tool-gis-platforms) and v1 2.7.5 (terrain and surface modelling).",
    tasks=[
        T("t1", SEEDT("2.1.4", 1), "Analyze terrain, habitat connectivity or resource distribution for a planning question, stating the data, projection and accuracy limits that bound the answer.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("t2", SEEDT("2.1.4", 2), "Build a predictive spatial model for a conservation planning question, documenting its inputs, assumptions and validation against independent locations.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("t3", SEEDT("2.1.4", 3), "Evaluate alternative management scenarios with overlay and suitability analysis, documenting weights and criteria so that reviewers can test them.", "WF-PLAN", "remote", "partial", rewrite=True),
        T("z1", SEEDT("2.7.5", 1), "Model terrain, vegetation and infrastructure surfaces in three dimensions, reporting vertical accuracy against surveyed check points.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("z2", SEEDT("2.7.5", 2), "Prepare terrain and surface models for flood, visual-impact or construction analyses, matching resolution and vertical accuracy to each analysis.", "WF-PLAN", "remote", "partial", rewrite=True),
        T("g1", SEEDT("2.1.1", 1), "Maintain spatial layers of land use, vegetation and infrastructure with topology rules, attribute standards and update dates recorded.", "WF-OPERATE", "remote", "no", rewrite=True,
          note="Re-pointed from superseded v1 2.1.1 (move-to-tools) to its durable remainder v1 2.1.4."),
        T("g2", SEEDT("2.1.1", 2), "Run spatial queries and overlays for an environmental assessment, checking that all layers share a coordinate reference system and compatible scales.", "WF-ASSESS", "remote", "no", rewrite=True,
          note="Re-pointed from superseded v1 2.1.1 (move-to-tools) to its durable remainder v1 2.1.4."),
        T("std", "seed:dc-214-spatial-standards", "Set spatial-data standards for a programme covering reference systems, topology rules, accuracy reporting and update cycles.", "WF-MANAGE", "remote", "partial"),
    ],
    inds=[
        ("L1", "Projects and overlays layers for an assigned analysis, checking that all layers share a coordinate reference system before combining them.", "u", ["ws"], ["g2"]),
        ("L1", "Maintains assigned spatial layers to the attribute and topology standards, recording each edit's date and source.", "u", ["ra"], ["g1"]),
        ("L2", "Selects an overlay, proximity or suitability method for a routine planning question, stating the data and accuracy limits that bound the answer.", "u", ["ws"], ["t1", "t3"], {"attr": "gui"}),
        ("L2", "Builds terrain and surface models at a resolution matched to the analysis, reporting vertical accuracy against surveyed check points.", "u", ["ws"], ["z1", "z2"], {"attr": "kno"}),
        ("L3", "Builds a predictive spatial model for a non-routine question, validating it against independent locations and documenting its assumptions.", "u", ["ws", "pr"], ["t2"], {"attr": "cpx"}),
        ("L3", "Documents a spatial workflow so that a reviewer can reproduce each result and test the weights and criteria used.", "u", ["pr"], ["t3"], {"attr": "sco"}),
        ("L4", "Sets spatial-data standards for a programme covering reference systems, topology rules, accuracy reporting and update cycles.", "u", ["pr"], ["std"], {"attr": "gui"}),
        ("L4", "Resolves conflicting spatial analyses in a contested decision, documenting which data and methods the programme accepts and why.", "u", ["pr", "bars"], ["t3"], {"attr": "cpx"}),
    ]))

# ------------------------------------------------------------------ v1 2.1.5 cartography and visualization (rewrite; absorbs 2.7.4)
C = "seed:v1-2.1.5"
S.append(dict(
    id=C, seed=True, prefix="ind-v1-2.1.5", span=("L1", "L4"),
    title="Design maps and visualizations that communicate environmental data and uncertainty", alt=["Cartography and visualization"],
    definition="The capability to design maps, charts and other visual products, including interactive and three-dimensional ones, whose scale, symbology, encoding and depiction of uncertainty fit the audience and the decision. Visualization and immersive platforms are L4.",
    statement="Designs maps, charts and other visual products, including interactive and three-dimensional ones, whose scale, symbology, colour, visual encoding and depiction of uncertainty fit the audience and the decision; tests products with intended users; and avoids encodings that mislead.",
    note="Rewritten by WP-04 around visual encoding and uncertainty depiction for the audience; absorbs the durable part of v1 2.7.4 (immersive platforms to L4 watch seed:tool-immersive-platforms).",
    tasks=[
        T("t1", SEEDT("2.1.5", 1), "Design a map for a stated audience and decision, choosing scale, extent, symbology and colour that the audience reads correctly.", "WF-ASSESS", "remote", "no", rewrite=True, modes=["MODE-ENGAGE"]),
        T("t2", SEEDT("2.1.5", 2), "Apply cartographic conventions for scale, symbology and colour to a map series, so that maps remain comparable across editions.", "WF-ASSESS", "remote", "no", rewrite=True),
        T("t3", SEEDT("2.1.5", 3), "Develop an interactive map product for public or internal users, testing with intended users that they find and interpret key information.", "WF-ASSESS", "remote", "no", rewrite=True, modes=["MODE-ENGAGE"]),
        T("i1", SEEDT("2.7.4", 1), "Create a narrative map product for public engagement that shows environmental change and its uncertainty without overstating precision.", "WF-ASSESS", "remote", "no", rewrite=True, modes=["MODE-ENGAGE"], rel=["public"],
          note="Re-pointed from superseded v1 2.7.4 (move-to-tools) to its durable remainder v1 2.1.5."),
        T("i2", SEEDT("2.7.4", 2), "Build a three-dimensional visual environment from photogrammetry or lidar data, stating its accuracy and the date of the source data.", "WF-ASSESS", "remote", "partial", rewrite=True,
          supports=[C, ("seed:v1-2.1.4", "contributing")], note="Re-pointed from superseded v1 2.7.4 (move-to-tools) to its durable remainder v1 2.1.5."),
        T("i3", SEEDT("2.7.4", 3), "Specify the content, accuracy and accessibility requirements of an immersive visual product for the designers and developers who build it.", "WF-PLAN", "remote", "no", rewrite=True,
          note="Re-pointed from superseded v1 2.7.4 (move-to-tools) to its durable remainder v1 2.1.5."),
        T("g3", SEEDT("2.1.1", 3), "Produce maps for reports, briefings and field crews at the scale, extent and legibility each use requires.", "WF-ASSESS", "remote", "partial", rewrite=True,
          note="Re-pointed from superseded v1 2.1.1 (move-to-tools) to the durable visual-communication remainder v1 2.1.5."),
        T("z3", SEEDT("2.7.5", 3), "Prepare three-dimensional surface data for public visualization, generalizing detail and stating accuracy so that viewers do not over-read the model.", "WF-ASSESS", "remote", "no", rewrite=True, modes=["MODE-ENGAGE"]),
        T("unc", "seed:dc-215-uncertainty-depiction", "Depict the uncertainty of a mapped or charted estimate with an encoding that intended users read correctly in a comprehension check.", "WF-ASSESS", "remote", "no"),
    ],
    inds=[
        ("L1", "Produces a map to an assigned template for a stated audience, with scale, legend, source, date and projection correct on review.", "u", ["ws"], ["g3"]),
        ("L1", "Applies the programme's symbology and colour conventions to a map series, so that maps remain comparable across editions.", "u", ["ws"], ["t2"]),
        ("L2", "Designs a map or chart for a stated audience and decision, choosing an encoding the audience reads correctly in a user test.", "u", ["ws"], ["t1"], {"attr": "gui"}),
        ("L2", "Depicts the uncertainty of a mapped or charted estimate so that users distinguish confident from uncertain areas in a comprehension check.", "u", ["ws"], ["unc"], {"attr": "kno"}),
        ("L3", "Develops an interactive or three-dimensional visual product, testing with intended users that they find and interpret its key information.", "u", ["ws", "pr"], ["t3", "i2"], {"attr": "cpx"}),
        ("L3", "Reviews colleagues' maps and charts for misleading encodings before release, returning specific corrections.", "u", ["pr"], ["i1"], {"attr": "sco"}),
        ("L4", "Sets visual-communication standards for a programme's maps and charts, including uncertainty depiction and accessibility requirements.", "u", ["pr"], ["i3"], {"attr": "gui"}),
        ("L4", "Evaluates whether decision-makers interpret the programme's visual products correctly, revising the standards from the results.", "u", ["pr"], ["unc"], {"attr": "sco"}),
    ]))

# ------------------------------------------------------------------ v1 2.2.1 database design and management (carry, rewritten)
C = "seed:v1-2.2.1"
S.append(dict(
    id=C, seed=True, prefix="ind-v1-2.2.1", span=("L1", "L4"),
    title="Design and manage environmental databases", alt=["Database design and management"],
    definition="The capability to design, populate, query and maintain databases for environmental data so that records stay consistent, secure, recoverable and usable: data models, keys and constraints, query logic, access control, backup and archiving. Database products are L4.",
    statement="Designs, populates, queries and maintains databases for environmental monitoring and management data: builds data models with keys and constraints, writes queries, controls access, and runs backup, archiving and recovery procedures so that records stay consistent, secure and usable over the long term.",
    note="Carried (wording rewritten) by WP-04; database products to L4.",
    tasks=[
        T("t1", SEEDT("2.2.1", 1), "Design a relational data model for environmental monitoring data, with keys, constraints and code lists that prevent inconsistent records.", "WF-PLAN", "remote", "no", rewrite=True),
        T("t2", SEEDT("2.2.1", 2), "Query a monitoring database to answer a programme request, checking the result against known totals before release.", "WF-OPERATE", "remote", "no", rewrite=True),
        T("t3", SEEDT("2.2.1", 3), "Set backup, archiving and recovery procedures for an environmental database, testing recovery on a schedule.", "WF-OPERATE", "remote", "no", rewrite=True),
        T("access", "seed:dc-221-access-control", "Configure role-based access to an environmental database so that sensitive tables are visible only to authorized roles.", "WF-OPERATE", "remote", "no", supports=[C, ("seed:DC-CAND-07", "contributing")]),
        T("entry", "seed:dc-221-data-entry", "Enter field and laboratory records into a monitoring database following the data-entry rules, correcting records the database checks reject.", "WF-OPERATE", "remote-capable", "no"),
        T("migrate", "seed:dc-221-migrate", "Migrate a programme's legacy data to a new data model, reconciling record counts and values and documenting every transformation.", "WF-OPERATE", "remote", "no"),
    ],
    inds=[
        ("L1", "Enters records in a monitoring database following the data-entry rules, correcting any record the database's checks reject.", "u", ["ra"], ["entry"]),
        ("L1", "Runs a standard query against a monitoring database, checking the result against known totals before passing it on.", "u", ["ws"], ["t2"]),
        ("L2", "Writes queries that join and summarize monitoring tables for a programme request, documenting each query so that it can be re-run.", "u", ["ws"], ["t2"], {"attr": "aut"}),
        ("L2", "Tests database backup recovery on schedule, recording the time to restore and any data lost.", "u", ["ra"], ["t3"], {"attr": "kno"}),
        ("L3", "Designs a relational data model for a monitoring programme with keys, constraints and code lists that prevent inconsistent records.", "u", ["ws", "pr"], ["t1"], {"attr": "cpx"}),
        ("L3", "Configures role-based access so that sensitive tables are visible only to authorized roles, verifying access with a test account.", "u", ["ws"], ["access"], {"attr": "sco"}),
        ("L4", "Sets database standards for a programme covering data models, code lists, access control, retention and recovery.", "u", ["pr"], ["t1", "t3"], {"attr": "gui"}),
        ("L4", "Migrates a programme's legacy data to a new data model, reconciling record counts and values and documenting every transformation.", "u", ["pr", "ra"], ["migrate"], {"attr": "cpx"}),
    ]))

# ------------------------------------------------------------------ v1 2.2.2 statistics (carry, rewritten; absorbs 2.4.5)
C = "seed:v1-2.2.2"
S.append(dict(
    id=C, seed=True, prefix="ind-v1-2.2.2", span=("L1", "L4"),
    title="Analyze environmental data statistically and interpret the results", alt=["Statistical analysis and interpretation", "Time series analysis"],
    definition="The capability to choose, apply and interpret statistical methods for environmental data, including designed comparisons, regression, mixed and spatial models, trend and time-series analysis, with honest treatment of assumptions, dependence, detection and uncertainty. Statistical software is L4.",
    statement="Chooses, applies and interprets statistical methods for environmental data, including designed comparisons, regression, mixed and spatial models, trend and time-series analysis; checks assumptions such as independence and detection; states effect sizes with uncertainty; and explains what the results do and do not support.",
    note="Carried (wording rewritten) by WP-04; absorbs v1 2.4.5 time-series analysis as a specialization. Monitoring design moved to DC-CAND-03.",
    tasks=[
        T("t1", SEEDT("2.2.2", 1), "Estimate treatment effects on ecological response variables with a method suited to the design, reporting effect sizes and intervals.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("t2", SEEDT("2.2.2", 2), "Analyze trends in a long-term monitoring dataset, accounting for changes in methods, effort and detection over the record.", "WF-MONITOR", "remote", "partial", rewrite=True),
        T("t3", SEEDT("2.2.2", 3), "Prepare statistical graphics that show the main patterns and their uncertainty for a technical or decision audience.", "WF-ASSESS", "remote", "no", rewrite=True,
          supports=[C, ("seed:v1-2.1.5", "contributing")]),
        T("s1", SEEDT("2.4.5", 1), "Analyze long-term temperature, precipitation or streamflow records for trends and shifts, testing for autocorrelation and changes in measurement.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("s2", SEEDT("2.4.5", 2), "Detect cycles and anomalies in an ecological monitoring time series, separating them from artefacts of sampling or instrument change.", "WF-MONITOR", "remote", "partial", rewrite=True),
        T("s3", SEEDT("2.4.5", 3), "Forecast a resource or stress indicator from its time series, stating the forecast interval and the horizon beyond which it is not useful.", "WF-PLAN", "remote", "partial", rewrite=True),
        T("rev", "seed:dc-222-review-analysis", "Review another analyst's statistical analysis before release, checking design, assumptions and interpretation against the data and the claims made.", "WF-MONITOR", "remote", "partial"),
        T("prep", "seed:dc-222-screen-data", "Screen a dataset for missing values, outliers and unit errors before analysis, recording each correction and its basis.", "WF-MONITOR", "remote", "no"),
    ],
    inds=[
        ("L1", "Runs a specified statistical test on a prepared dataset, reporting the estimate, interval and sample size as the analysis plan requires.", "u", ["ws"], ["t1"]),
        ("L1", "Screens a dataset for missing values, outliers and unit errors before analysis, recording each correction.", "u", ["ra"], ["prep"]),
        ("L2", "Selects a method suited to the design and data for a routine question, checking its assumptions and reporting effect sizes with intervals.", "u", ["ws"], ["t1"], {"attr": "gui"}),
        ("L2", "Analyzes a monitoring time series for trend, accounting for autocorrelation and changes in method or effort across the record.", "u", ["ws"], ["t2", "s1"], {"attr": "cpx"}),
        ("L3", "Analyzes non-routine data with dependence, imperfect detection or unbalanced designs, documenting why the chosen model fits better than alternatives.", "u", ["ws", "pr"], ["s2", "t2"], {"attr": "cpx"}),
        ("L3", "Reviews another analyst's statistical work before release, returning corrections where design, assumptions or interpretation do not support the claims.", "u", ["pr"], ["rev"], {"attr": "sco"}),
        ("L4", "Sets statistical standards for a programme's analyses, covering design review, assumption checks and how uncertainty is reported.", "u", ["pr"], ["rev"], {"attr": "gui"}),
        ("L4", "Resolves disputes over statistical evidence in a contested decision, documenting which analyses the programme relies on and why.", "u", ["pr", "bars"], ["rev"], {"attr": "cpx"}),
    ]))

# ------------------------------------------------------------------ v1 2.2.3 data QC (rewrite; absorbs 2.6.4)
C = "seed:v1-2.2.3"
S.append(dict(
    id=C, seed=True, prefix="ind-v1-2.2.3", span=("L1", "L4"),
    title="Assure the quality of environmental data from collection to release", alt=["Data quality control and validation"],
    definition="The capability to design and run quality assurance and quality control for environmental data from collection to release: protocols, checks, audits, flagging and correction rules, including the design, tuning and audit of automated checks on sensor and batch data. Field calibration and sample handling stay field craft.",
    statement="Designs and runs quality assurance and control for environmental data from collection to release: writes QA protocols; applies range, consistency and completeness checks; audits datasets; designs, tunes and audits automated anomaly flags and corrections on sensor and batch data; records every flag and correction; and trains others on validation rules.",
    note="Rewritten by WP-04 (title/description defect fixed); absorbs v1 2.6.4 (design and audit of automated QC).",
    tasks=[
        T("t1", SEEDT("2.2.3", 1), "Write a quality assurance protocol for a field or laboratory data stream, specifying checks, acceptance criteria and correction rules.", "WF-MONITOR", "remote", "partial", rewrite=True),
        T("t2", SEEDT("2.2.3", 2), "Audit an environmental dataset on a set schedule, identifying errors and anomalies and recording each correction with its basis.", "WF-MONITOR", "remote", "partial", rewrite=True),
        T("t3", SEEDT("2.2.3", 3), "Train staff and partners on the programme's data validation rules, checking their application on a sample of submitted records.", "WF-LEARN", "remote-capable", "partial", rewrite=True),
        T("a1", SEEDT("2.6.4", 1), "Configure automated anomaly detection on a sensor data stream, tuning thresholds against a labelled sample of known errors.", "WF-MONITOR", "remote", "partial", rewrite=True),
        T("a2", SEEDT("2.6.4", 2), "Audit automated flags and corrections on a sensor or batch dataset, measuring false-flag and missed-error rates on a reviewed sample.", "WF-MONITOR", "remote", "partial", rewrite=True),
        T("a3", SEEDT("2.6.4", 3), "Build an automated validation step into a data pipeline from collection to analysis, logging every flag and correction it applies.", "WF-OPERATE", "remote", "no", rewrite=True,
          supports=[C, ("seed:DC-CAND-04", "contributing")]),
        T("apply", "seed:dc-223-apply-checks", "Apply range, consistency and completeness checks to incoming field or laboratory records, flagging failures for correction before entry.", "WF-MONITOR", "remote-capable", "partial"),
        T("review-flags", "seed:dc-223-review-flags", "Review automated flags on a sensor dataset against field and instrument records, accepting, correcting or rejecting each flag.", "WF-MONITOR", "remote-capable", "yes"),
    ],
    inds=[
        ("L1", "Applies the programme's range, consistency and completeness checks to incoming records, flagging each failure for correction before entry.", "u", ["ra"], ["apply"]),
        ("L1", "Records every correction to a data record with its reason, date and the person or rule that made it.", "u", ["ra"], ["apply", "t2"]),
        ("L2", "Audits a dataset on schedule, identifying errors and anomalies and documenting the basis for each correction.", "u", ["ra", "ws"], ["t2"], {"attr": "aut"}),
        ("L2", "Reviews automated flags on a sensor dataset, accepting, correcting or rejecting each flag against field and instrument records.", "a", ["ws"], ["review-flags"], {"attr": "aug"}),
        ("L3", "Writes a quality assurance protocol for a data stream, specifying checks, acceptance criteria and correction rules that others apply consistently.", "u", ["pr"], ["t1"], {"attr": "gui"}),
        ("L3", "Tunes automated anomaly detection against a labelled sample of known errors, reporting false-flag and missed-error rates before deployment.", "s", ["ws"], ["a1", "a2"], {"attr": "aug"}),
        ("L4", "Sets data quality standards for a programme's data streams, including acceptance criteria and the audit cycle for automated checks.", "a", ["pr"], ["t1", "a3"], {"attr": "gui"}),
        ("L4", "Audits automated quality control across a programme for drift and missed errors, ordering corrections where performance falls below the standard.", "s", ["ra"], ["a2"], {"attr": "sco"}),
    ]))

# ------------------------------------------------------------------ v1 2.4.1 learned models (rewrite; absorbs 2.6.1, 2.6.2)
C = "seed:v1-2.4.1"
S.append(dict(
    id=C, seed=True, prefix="ind-v1-2.4.1", span=("L2", "L4"), evidence="E", sources=["DC-001", "DC-038", "DC-039", "DC-040"],
    title="Build and validate automated detection and classification models for environmental observations",
    alt=["Machine learning for environmental applications", "Computer vision and acoustic classification"],
    definition="The capability to train, tune and validate learned models that detect, classify or count species, habitats and features in imagery, sound and sensor data, with validation against ground truth, error reported by condition and outputs fit for human review. Model architectures, libraries and pretrained detectors are L4.",
    statement="Trains, tunes and validates learned models that detect, classify or count species, habitats and features in imagery, acoustic recordings and sensor data; assembles and documents training data; validates against independent ground truth with spatially or temporally blocked hold-outs; reports error by class and condition; and sets thresholds so that outputs can be reviewed.",
    note="Rewritten by WP-04 with a method-neutral title (G-5); absorbs v1 2.6.1 (computer vision) and 2.6.2 (acoustic AI: thresholds and occupancy from detections; acoustic survey design and recorder deployment go to FC-C01/FC-C03).",
    tasks=[
        T("t1", SEEDT("2.4.1", 1), "Train a classification model to detect an invasive species in aerial imagery, documenting training data sources, dates and label quality.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("t2", SEEDT("2.4.1", 2), "Identify patterns in species distribution data with unsupervised clustering, testing whether clusters are stable across samples and settings.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("t3", SEEDT("2.4.1", 3), "Integrate a validated detection model into a monitoring workflow, setting the confidence thresholds at which outputs go to human review.", "WF-MONITOR", "remote", "partial", rewrite=True,
          supports=[C, ("seed:DC-CAND-14", "contributing")]),
        T("v1", SEEDT("2.6.1", 1), "Fine-tune an image classification model to identify species in camera-trap images, holding out whole camera sites for validation.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("v2", SEEDT("2.6.1", 2), "Count wildlife or map vegetation from aerial imagery with an object detection model, reporting count error against manual counts on a sample.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("v3", SEEDT("2.6.1", 3), "Validate a detection model against field ground-truth data, reporting error by habitat, season and image condition.", "WF-MONITOR", "remote-capable", "partial", rewrite=True),
        T("a1", SEEDT("2.6.2", 1), "Deploy acoustic recorders at survey sites following the survey design, recording placement, settings and schedule for later analysis.", "WF-ASSESS", "on-site-required", "yes", rewrite=True,
          supports=["seed:FC-C01", (C, "contributing")], note="Recorder deployment is field craft (v1_disposition 2.6.2: acoustic survey design into FC-C01/FC-C03); re-pointed to FC-C01 for FC review."),
        T("a2", SEEDT("2.6.2", 2), "Set detection thresholds for automated classification of species vocalizations from a verified sample of recordings, stating the expected precision.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("a3", SEEDT("2.6.2", 3), "Estimate occupancy or activity of target species from verified acoustic detections, accounting for imperfect detection.", "WF-ASSESS", "remote", "partial", rewrite=True,
          supports=[C, ("seed:v1-2.2.2", "contributing")]),
        T("diag", "seed:dc-241-diagnose-failure", "Diagnose why a detection model fails at a new site or season, choosing between retraining and a documented restriction on its use.", "WF-MONITOR", "remote", "yes"),
    ],
    inds=[
        ("L2", "Trains a detection or classification model on documented training data, validating it on hold-outs blocked by site or time.", "u", ["ws"], ["t1", "v1"]),
        ("L2", "Reports model error by class, habitat and condition from independent ground truth, not only overall accuracy.", "u", ["ws"], ["v3", "v2"]),
        ("L2", "Sets confidence thresholds for model outputs from a verified sample, stating the expected precision and recall at each threshold.", "u", ["ws"], ["a2", "t3"]),
        ("L3", "Diagnoses why a detection model fails under a new condition, such as a new site or season, documenting a retraining plan or a use restriction.", "u", ["ws", "pr"], ["diag"], {"attr": "cpx"}),
        ("L3", "Designs the human-review step for model outputs, choosing which confidence bands go to reviewers so that the workflow meets its error target.", "s", ["pr"], ["t3"], {"attr": "aug"}),
        ("L4", "Sets development and validation standards for a programme's detection and classification models, including blocked validation and condition-level error reporting.", "u", ["pr"], ["v3"], {"attr": "gui"}),
        ("L4", "Decides when a programme's detection model must be retrained or withdrawn, documenting the performance evidence behind the decision.", "u", ["pr"], ["diag"], {"attr": "aut"}),
    ]))

# ------------------------------------------------------------------ v1 2.4.2 predictive modelling (rewrite; absorbs 2.6.3)
C = "seed:v1-2.4.2"
S.append(dict(
    id=C, seed=True, prefix="ind-v1-2.4.2", span=("L2", "L4"),
    title="Build, calibrate and validate predictive and simulation models of environmental systems", alt=["Predictive modeling and simulation"],
    definition="The capability to build, calibrate, validate and run process, statistical and hybrid models that predict or simulate environmental systems under alternative conditions and scenarios, with sensitivity analysis and honest uncertainty. Named model products are L4; forecast systems run operationally are a separate competency.",
    statement="Builds, calibrates, validates and runs process-based, statistical and hybrid models that predict or simulate environmental systems, such as fire spread, hydrology, populations and vegetation, under alternative conditions and scenarios; conducts sensitivity and uncertainty analysis; tests performance under novel conditions; and presents outputs with their limits to decision-makers.",
    note="Rewritten by WP-04; absorbs v1 2.6.3 (predictive analytics); operational forecasting and early-warning systems are shared with DC-CAND-12.",
    tasks=[
        T("t1", SEEDT("2.4.2", 1), "Run a fire spread model for an incident or plan under alternative weather scenarios, calibrating inputs to observed fire behaviour.", "WF-ASSESS", "remote-capable", "yes", rewrite=True,
          regime={"mentorshipDependence": "H", "cycleDependence": "seasonal", "placeBoundness": "ecosystem-type", "currencyDecay": "M"}),
        T("t2", SEEDT("2.4.2", 2), "Simulate ecosystem response to alternative land-use and climate scenarios, documenting scenario assumptions and the sensitivity of results to each.", "WF-PLAN", "remote", "partial", rewrite=True),
        T("t3", SEEDT("2.4.2", 3), "Present model outputs to stakeholders for an adaptive management decision, stating the conditions under which the projections should not be trusted.", "WF-LEARN", "remote-capable", "partial", rewrite=True,
          supports=[C, ("seed:DC-CAND-11", "contributing")], modes=["MODE-ENGAGE"], rel=["stakeholder"]),
        T("p1", SEEDT("2.6.3", 1), "Build a predictive model of fire risk, pest outbreak or water availability, validating it on years or areas withheld from fitting.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("p2", SEEDT("2.6.3", 2), "Forecast resource management needs from a validated predictive model, stating the horizon and interval for each estimate.", "WF-PLAN", "remote", "partial", rewrite=True),
        T("p3", SEEDT("2.6.3", 3), "Design early-warning thresholds from model predictions that trigger management actions, testing false-alarm and missed-event rates on past records.", "WF-PLAN", "remote", "partial", rewrite=True,
          supports=[C, ("seed:DC-CAND-12", "contributing")]),
        T("sens", "seed:dc-242-sensitivity", "Conduct a sensitivity analysis of a predictive model, ranking the inputs and parameters that most change the result for the decision.", "WF-ASSESS", "remote", "partial"),
        T("doc", "seed:dc-242-run-record", "Record the scenario assumptions, input sources and model version of each model run so that a reviewer can repeat it.", "WF-ASSESS", "remote", "no",
          supports=[C, ("seed:DC-CAND-05", "contributing")]),
    ],
    inds=[
        ("L2", "Calibrates an established model for a routine case, reporting fit for the calibration and validation periods separately.", "u", ["ws"], ["t1", "p1"]),
        ("L2", "Documents the scenario assumptions and input sources of each model run so that a reviewer can repeat it.", "u", ["ra"], ["doc"]),
        ("L3", "Conducts sensitivity and uncertainty analysis for a model, ranking the inputs that most change the result for the decision.", "u", ["ws", "pr"], ["sens"], {"attr": "cpx"}),
        ("L3", "Tests model performance under conditions outside the calibration range, stating where projections should not be used.", "u", ["ws"], ["p1", "p3"], {"attr": "cpx"}),
        ("L3", "Presents model outputs to decision-makers with the conditions under which projections fail, answering challenges with the validation evidence.", "u", ["bars", "sim"], ["t3"], {"attr": "sco"}),
        ("L4", "Develops or extends a model for a novel management problem, documenting the conceptual model, validation design and limits for peer review.", "u", ["pr"], ["t2"], {"attr": "kno"}),
        ("L4", "Sets modelling standards for a programme covering calibration, validation, sensitivity analysis and documentation for each model type.", "u", ["pr"], ["sens"], {"attr": "gui"}),
    ]))

for spec in S:
    build(spec)
print("batch E1 written:", len(S), "competencies")
