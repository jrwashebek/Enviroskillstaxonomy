"""Batch G: DC-lane knowledge areas (v1 D1/D6 seeds whose disposition is 'core | knowledge-area').
Knowledge areas carry no craft-primary tag and no proficiency indicators; they are assessed by knowledge tests on
linked KnowledgeStatements (ADR-0003 §1; vocab/competency_types.yaml). Their v1 tasks are rewritten to v2 rules and
keep the knowledge area as primary support (ADR-0003 consequences), with contributing links to practice competencies."""
from lib import lm, prov, rewrite_seed_competency, rewrite_seed_task, write

ST = lambda c, n: f"seed:v1-{c}-T{n}"  # noqa: E731
NOTE = "Rewritten by WP-04 as a knowledge area (no craft-primary tag; ADR-0003 consequences, P-DC-12)."


def ks(kid, comp, text, lowest="L1"):
    return {"id": kid, "type": "KnowledgeStatement", "prefLabel": lm(" ".join(text.split()[:10]) + "…"), "statement": lm(text),
            "lowestLevel": lowest, "supports": [comp], "assessmentMethods": ["knowledge-test"], "layer": "L2", "module": "core",
            "status": "draft", "lifecycleState": "established", "useTier": "describe", "validationStatus": "draft",
            "license": "CC0-1.0", "sensitivity": "public", "provenance": prov("J", adr=["ADR-0003", "ADR-0004"])}


def ka(code, title, definition, statement, statements, tasks, note="", alt=None):
    cid = f"seed:v1-{code}"
    kids = []
    for i, (lv, text) in enumerate(statements, 1):
        kid = f"seed:ks-v1-{code}-{i:02d}"
        write(ks(kid, cid, text, lv), "knowledge")
        kids.append(kid)
    rec = rewrite_seed_competency(cid, title, definition, statement, "knowledge-area", ("A", "L4"), [], note=(NOTE + " " + note).strip(),
                                  reusability="cross-subsector", alt=alt)
    rec.pop("levels", None)
    rec["knowledge"] = kids
    rec["useTier"] = "describe"
    # place 'knowledge' before homeModule for readability
    write(rec)
    for t in tasks:
        tid, text, sup, wf, field, form = t[:6]
        kw = t[6] if len(t) > 6 else {}
        write(rewrite_seed_task(tid, text, sup, wf, field, form, **kw))


C = "seed:v1-1.1.1"
ka("1.1.1", "Ecosystem dynamics and processes",
   "The body of knowledge on how energy, water and nutrients move through ecosystems, how species interact through food webs and other interdependencies, and how communities change through succession after disturbance. It underpins assessment, restoration and monitoring work across crafts.",
   "Knowledge of energy flow and nutrient cycling, species interactions and interdependencies, food-web structure, and ecological succession after disturbance, as used to interpret ecosystem condition and to plan restoration, monitoring and management.",
   [("A", "Energy enters most ecosystems through primary production and is transferred through food webs with large losses at each trophic step."),
    ("L1", "Nutrient cycles such as nitrogen and phosphorus link soils, water, vegetation and consumers, and management can speed, slow or redirect them."),
    ("L1", "Succession after disturbance follows site-dependent pathways that depend on residual organisms, propagule supply and site conditions."),
    ("L2", "Keystone species and ecosystem engineers can change community structure far more than their abundance suggests."),
    ("L2", "Successional pathways can stall or diverge into alternative states when thresholds in soils, hydrology or species pools are crossed.")],
   [(ST("1.1.1", 1), "Observe food-web interactions in field studies, recording the species, interaction types and conditions under which each was seen.", [C, ("seed:v1-4.1.2", "contributing")], "WF-ASSESS", "on-site-required", "yes"),
    (ST("1.1.1", 2), "Model nutrient cycling for contrasting habitat types, documenting the model structure, parameters and their sources.", [C, ("seed:v1-2.4.2", "contributing")], "WF-ASSESS", "remote", "partial"),
    (ST("1.1.1", 3), "Develop a restoration plan that accounts for the species interdependencies the target community needs to persist.", [C, ("seed:v1-4.2.1", "contributing")], "WF-PLAN", "remote-capable", "yes"),
    (ST("1.1.3", 1), "Map stages of ecological succession on post-disturbance sites from field plots and imagery, stating the criteria used for each stage.", [C, ("seed:v1-2.1.2", "contributing")], "WF-ASSESS", "on-site-preferred", "yes"),
    (ST("1.1.3", 2), "Project future vegetation states on unmanaged lands from historical data, stating the assumptions and uncertainty of the projection.", [C, ("seed:v1-2.4.2", "contributing")], "WF-ASSESS", "remote", "partial"),
    (ST("1.1.3", 3), "Recommend restoration techniques that work with the site's likely successional pathway, explaining the expected trajectory.", [C], "WF-PLAN", "remote-capable", "yes")],
   note="Absorbs v1 1.1.3 (succession principles as knowledge statements).")

C = "seed:v1-1.1.4"
ka("1.1.4", "Disturbance ecology",
   "The body of knowledge on how fires, floods, storms, droughts, insects and disease affect ecosystems, on disturbance regimes and their history, and on how systems resist, recover from or reorganize after disturbance.",
   "Knowledge of disturbance agents and regimes (frequency, severity, extent and seasonality), their history at a site, interactions among disturbances, and the resistance, recovery and reorganization of ecosystems after disturbance, as used by fire, restoration, hazards and monitoring work.",
   [("A", "A disturbance regime is described by the frequency, severity, extent and seasonality of disturbance events at a place."),
    ("L1", "Fire history can be reconstructed from fire scars, stand ages, charcoal and records, each with different spatial and temporal resolution."),
    ("L2", "Interacting disturbances, such as drought followed by insects and fire, can produce effects that neither causes alone."),
    ("L2", "Recovery after disturbance depends on legacies such as surviving organisms, seed banks, soils and dead wood.")],
   [(ST("1.1.4", 1), "Analyze fire history records for a landscape to describe the frequency, severity and seasonality of past fires, stating the limits of each source.", [C, ("seed:v1-2.2.2", "contributing")], "WF-ASSESS", "remote", "partial"),
    (ST("1.1.4", 2), "Assess ecosystem resilience after a flood or wildfire from field evidence of legacies, regeneration and soil condition.", [C, ("seed:FC-C02", "contributing")], "WF-ASSESS", "on-site-required", "yes"),
    (ST("1.1.4", 3), "Design a post-disturbance recovery plan that sets treatment priorities from ecological thresholds and observed site conditions.", [C, ("seed:v1-4.2.1", "contributing")], "WF-PLAN", "remote-capable", "yes")])

C = "seed:v1-1.2.2"
ka("1.2.2", "Soil science: physics, chemistry, biology and classification",
   "The body of knowledge on soil physical, chemical and biological properties, soil classification and mapping, and soil carbon dynamics, as used to interpret soil condition, plan land use and conservation, and estimate carbon stocks and change.",
   "Knowledge of soil physical, chemical and biological properties, soil formation, classification and mapping, nutrient and carbon dynamics, and contamination, as used to interpret soil condition, guide land use and conservation practice, and estimate soil carbon stocks and their change under management.",
   [("A", "Soil properties such as texture, structure, organic matter and pH control water holding, nutrient supply and biological activity."),
    ("L1", "Soil classification groups soils by diagnostic horizons and properties, and survey maps carry map-unit purity limits that affect site decisions."),
    ("L2", "Soil carbon stocks change slowly relative to measurement error, so detecting change needs repeated, depth-controlled sampling over years."),
    ("L2", "Soil biological activity responds to disturbance, amendments and moisture faster than total organic carbon does.")],
   [(ST("1.2.1", 2), "Create digital soil maps from field observations and environmental covariates, reporting map accuracy against held-out field sites.", [C, ("seed:v1-2.1.4", "contributing")], "WF-ASSESS", "remote", "partial",
     {"note": "Split from v1 1.2.1: digital soil mapping as DC tasks within the soil science knowledge area (v1_disposition 1.2.1)."}),
    (ST("1.2.1", 3), "Interpret soil maps to guide land-use planning and conservation practice, accounting for map-unit inclusions and scale limits.", [C], "WF-PLAN", "remote-capable", "partial"),
    (ST("1.2.2", 1), "Collect soil samples to a stated design and interpret laboratory results for nutrient levels and microbial activity.", [C, ("seed:v1-4.1.4", "contributing")], "WF-ASSESS", "on-site-required", "yes"),
    (ST("1.2.2", 2), "Diagnose soil health problems caused by contamination or nutrient deficiency from field and laboratory evidence.", [C], "WF-ASSESS", "on-site-preferred", "yes"),
    (ST("1.2.2", 3), "Recommend soil amendments that improve fertility and biological function, stating expected effects and how to verify them.", [C], "WF-PLAN", "remote-capable", "partial"),
    (ST("1.8.2", 1), "Estimate soil carbon stocks and their change in agricultural systems from depth-controlled samples or calibrated models, stating the error.", [C, ("seed:DC-CAND-03", "contributing")], "WF-ASSESS", "remote-capable", "partial",
     {"note": "Merged from v1 1.8.2 (soil carbon dynamics). MRV measurement tasks for markets go to PS-C06 (module markets)."}),
    (ST("1.8.2", 2), "Evaluate how management practices affect soil carbon accumulation, separating real change from sampling and measurement error.", [C, ("seed:v1-2.2.2", "contributing")], "WF-ASSESS", "remote", "partial"),
    (ST("1.8.2", 3), "Prepare the soil-carbon evidence that a carbon programme or market requires, documenting methods, uncertainty and verification steps.", [C], "WF-MONITOR", "remote", "partial")],
   note="Broadened per v1_disposition 1.2.2; absorbs v1 1.2.1 (classification; split with v1 4.1.4) and v1 1.8.2 (soil carbon).")

C = "seed:v1-1.2.3"
ka("1.2.3", "Watershed hydrology",
   "The body of knowledge on how water moves through landscapes, from precipitation through infiltration, runoff, streamflow and groundwater, and how land cover, soils, topography and management change those pathways.",
   "Knowledge of the water balance, precipitation, infiltration, runoff generation, streamflow, groundwater and surface-water interaction, and the effects of land cover, soils, topography, climate and management on hydrologic response, as used in water, forest, hazards and restoration work.",
   [("A", "A watershed water balance links precipitation, evapotranspiration, storage change, runoff and groundwater recharge."),
    ("L1", "Streamflow records combine stage measurements with a rating curve that must be checked against direct discharge measurements."),
    ("L2", "Land-cover change, impervious surface and soil compaction alter runoff timing and peak flows more than annual totals."),
    ("L2", "Groundwater and surface water exchange in both directions, so pumping or drainage can change streamflow at a distance.")],
   [(ST("1.2.3", 1), "Measure streamflow, precipitation and groundwater levels to a monitoring protocol so that the records can support a watershed model.", [C, ("seed:v1-4.1.3", "contributing")], "WF-MONITOR", "on-site-required", "yes"),
    (ST("1.2.3", 2), "Analyze hydrologic records to identify flood risk and water-availability trends, stating the record length and its limits.", [C, ("seed:v1-2.2.2", "contributing")], "WF-ASSESS", "remote", "partial"),
    (ST("1.2.3", 3), "Develop a watershed management plan that reduces runoff and improves infiltration, stating the hydrologic effect expected from each measure.", [C], "WF-PLAN", "remote-capable", "partial")])

C = "seed:v1-1.4.1"
ka("1.4.1", "Population dynamics and modelling",
   "The body of knowledge on how populations grow, decline and respond to environmental change and management, including demographic rates, density dependence, stochasticity and population viability.",
   "Knowledge of population growth, demographic rates, density dependence, age and stage structure, environmental and demographic stochasticity, metapopulations and population viability, as used by wildlife, fisheries, forest health and conservation work to interpret trends and project management effects.",
   [("A", "Population change results from births, deaths, immigration and emigration, which vary with age, stage and conditions."),
    ("L1", "Count data reflect both abundance and detection, so trends in counts can mislead when detection changes."),
    ("L2", "Small populations face extinction risk from demographic and environmental stochasticity even when average growth is positive."),
    ("L2", "Population viability analyses are sensitive to vital-rate estimates and their variance, so sensitivity analysis is part of the result.")],
   [(ST("1.4.1", 1), "Analyze population trends from field data with a statistical model that accounts for detection and sampling effort.", [C, ("seed:v1-2.2.2", "contributing")], "WF-ASSESS", "remote", "partial"),
    (ST("1.4.1", 2), "Simulate population responses to habitat change or management actions, documenting vital-rate sources and their uncertainty.", [C, ("seed:v1-2.4.2", "contributing")], "WF-ASSESS", "remote", "partial"),
    (ST("1.4.1", 3), "Prepare a population viability assessment for an at-risk species, reporting extinction risk with its sensitivity to vital-rate estimates.", [C, ("seed:v1-2.4.2", "contributing")], "WF-ASSESS", "remote", "partial")])

C = "seed:v1-1.5.4"
ka("1.5.4", "Climate system, carbon cycle and climate-biosphere interactions",
   "The body of knowledge on the climate system, the carbon cycle in ecosystems, how land management affects carbon storage and emissions, and climate-biosphere interactions including phenology and phenological mismatch.",
   "Knowledge of the climate system and its drivers, carbon stocks and fluxes in vegetation, soils and waters, management effects on sequestration and emissions, carbon accounting concepts, and climate-biosphere interactions such as shifts in phenology and resulting mismatches between species.",
   [("A", "Ecosystem carbon is stored in live biomass, dead wood, litter and soils, and disturbance moves carbon among these pools and the atmosphere."),
    ("L1", "Carbon accounting distinguishes stocks from fluxes and requires a stated baseline, boundary and treatment of permanence and leakage."),
    ("L2", "Phenological shifts with warming differ among species, which can decouple interacting species such as pollinators and plants."),
    ("L2", "Management that raises short-term carbon storage can raise long-term risk of loss where disturbance regimes are changing.")],
   [(ST("1.5.4", 1), "Estimate carbon stocks and fluxes in forests, soils or other ecosystems from field measurements and models, stating the error of each estimate.", [C, ("seed:v1-2.4.2", "contributing")], "WF-ASSESS", "remote-capable", "partial"),
    (ST("1.5.4", 2), "Evaluate how management alternatives affect carbon sequestration and storage over a stated horizon, including disturbance risk.", [C], "WF-PLAN", "remote", "partial"),
    (ST("1.5.4", 3), "Prepare carbon estimates for organizational reporting or project documentation, stating the baseline, boundary and uncertainty used.", [C], "WF-MONITOR", "remote", "partial"),
    (ST("1.5.5", 1), "Monitor phenological events such as bud break, flowering or migration timing with field observation or imagery, following a standard protocol.", [C, ("seed:v1-4.1.1", "contributing")], "WF-MONITOR", "on-site-preferred", "yes"),
    (ST("1.5.5", 2), "Analyze phenological trends and their relationships to climate variables, accounting for changes in observation effort.", [C, ("seed:v1-2.2.2", "contributing")], "WF-ASSESS", "remote", "partial"),
    (ST("1.5.5", 3), "Assess phenological mismatches between interacting species and their ecological consequences from monitoring evidence.", [C], "WF-ASSESS", "remote", "partial")],
   note="Broadened per v1_disposition 1.5.4; absorbs v1 1.5.5 (phenology).")

C = "seed:v1-1.6.1"
ka("1.6.1", "Conservation genetics and genomics",
   "The body of knowledge on genetic diversity, gene flow, population structure, inbreeding, adaptive variation and evolutionary potential, and on genetic, genomic, molecular-ecology and environmental-DNA evidence, as used in conservation and management decisions.",
   "Knowledge of genetic diversity, gene flow, population structure, effective population size, inbreeding and genetic load, adaptive variation and evolutionary potential, and of how genetic, genomic, molecular-ecology and environmental-DNA evidence is produced and interpreted for translocation, recovery, captive breeding and management-unit decisions.",
   [("A", "Genetic diversity lets populations adapt; small or isolated populations lose diversity through drift and inbreeding."),
    ("L1", "Environmental DNA detects genetic traces of organisms, so a detection shows recent presence nearby, not necessarily a resident population."),
    ("L2", "Effective population size is usually much smaller than census size and governs the rate at which diversity is lost."),
    ("L2", "Genetic rescue can restore fitness in inbred populations, but mixing distinct lineages carries a risk of outbreeding depression."),
    ("L2", "Genomic data distinguish neutral structure from adaptive variation, which bears on seed-zone and translocation decisions.")],
   [(ST("1.6.1", 1), "Interpret genetic study results to inform translocation, reintroduction or management-unit decisions, stating the limits of the evidence.", [C], "WF-ASSESS", "remote", "partial"),
    (ST("1.6.1", 2), "Assess genetic diversity and structure in populations of conservation concern from genetic data, reporting effective population size estimates.", [C, ("seed:v1-2.2.2", "contributing")], "WF-ASSESS", "remote", "partial"),
    (ST("1.6.1", 3), "Advise managers on genetic considerations in a species recovery plan, stating the risks of each option.", [C], "WF-PLAN", "remote", "partial"),
    (ST("1.6.2", 2), "Interpret environmental DNA results for managers, communicating what a detection or non-detection does and does not show.", [C, ("seed:DC-CAND-11", "contributing")], "WF-ASSESS", "remote", "partial",
     {"note": "Merged from v1 1.6.2 (assay interpretation knowledge; v1_disposition 1.6.2 move-to-tools: method to L4 seed:tool-method, sampling to FC-C16)."}),
    (ST("1.6.2", 3), "Evaluate when environmental DNA is appropriate compared with traditional survey methods for a monitoring question, documenting the trade-offs.", [C, ("seed:DC-CAND-03", "contributing")], "WF-PLAN", "remote", "partial"),
    (ST("1.6.3", 1), "Interpret genomic analyses of population structure, diversity and adaptive variation for a management question, stating the sampling limits.", [C], "WF-ASSESS", "remote", "partial"),
    (ST("1.6.3", 2), "Apply genomic findings to the management of genetic diversity, recommending actions with their expected genetic effects.", [C], "WF-PLAN", "remote", "partial"),
    (ST("1.6.3", 3), "Evaluate inbreeding, genetic load and evolutionary potential in a population of concern from genetic evidence, stating confidence.", [C], "WF-ASSESS", "remote", "partial"),
    (ST("1.6.4", 1), "Apply molecular diet analysis, stable isotopes or microbiome evidence to an ecological question, documenting the method's detection limits.", [C], "WF-ASSESS", "remote", "partial"),
    (ST("1.6.4", 2), "Interpret molecular ecology studies for their management implications, separating firm findings from tentative ones.", [C], "WF-ASSESS", "remote", "partial"),
    (ST("1.6.4", 3), "Identify when molecular approaches can answer a management question that traditional methods cannot, stating the added cost and value.", [C], "WF-PLAN", "remote", "partial"),
    (ST("1.6.5", 1), "Develop genetic management recommendations for a translocation or reintroduction programme, stating source-population choices and risks.", [C], "WF-PLAN", "remote", "partial",
     {"note": "v1 1.6.5 merged into this knowledge area; application tasks are enacted in MOD-12 wildlife (WP-06)."}),
    (ST("1.6.5", 2), "Apply genetic principles to a captive breeding or ex situ conservation programme, setting pairing and retention goals.", [C], "WF-PLAN", "remote", "partial"),
    (ST("1.6.5", 3), "Evaluate a genetic rescue proposal for an inbred population, weighing fitness gains against the risk of outbreeding depression.", [C], "WF-ASSESS", "remote", "partial")],
   note="One knowledge area replaces v1 1.6.1, 1.6.3, 1.6.4 and 1.6.5 and takes the assay-interpretation knowledge of 1.6.2 (v1_disposition).")

C = "seed:v1-6.3.1"
ka("6.3.1", "Environmental and natural resource economics",
   "The body of knowledge on market and non-market valuation of natural resources and environmental quality, welfare measures, discounting and the economics of externalities, as used to underpin economic analysis of environmental decisions and ecosystem-service assessment.",
   "Knowledge of market and non-market valuation methods (revealed and stated preference, benefit transfer), welfare measures, discounting, externalities and public goods, and the distributional effects of environmental decisions, as used in economic analysis of decisions, ecosystem-service assessment and budget planning.",
   [("A", "Non-market values such as recreation, scenic quality and clean air can be estimated but are not observed in market prices."),
    ("L1", "Stated-preference estimates depend on survey design, so willingness-to-pay results carry design-related uncertainty."),
    ("L2", "The discount rate chosen can reverse the ranking of alternatives whose costs and benefits fall at different times."),
    ("L2", "Benefit transfer applies values from study sites to policy sites and is valid only where the sites and goods are comparable.")],
   [(ST("6.3.1", 1), "Estimate the economic value of timber, water, recreation or other resources with market and non-market methods, stating the method's limits.", [C], "WF-ASSESS", "remote", "partial"),
    (ST("6.3.1", 2), "Conduct a stated-preference valuation survey with a documented design, sample and treatment of protest responses.", [C, ("seed:v1-5.6.2", "contributing")], "WF-ASSESS", "remote-capable", "partial"),
    (ST("6.3.1", 3), "Present valuation results for budget planning or policy proposals, showing how conclusions change with key assumptions.", [C], "WF-RESOURCE", "remote", "partial")],
   note="Knowledge area underpinning 6.3.2, 6.3.4 and 6.4.3 (v1_disposition 6.3.1).")

C = "seed:v1-6.7.4"
ka("6.7.4", "Toxicology and exposure pathways",
   "The body of knowledge on how toxic substances affect human and ecological health and the routes by which people and organisms are exposed to environmental contaminants in air, water, soil and food.",
   "Knowledge of toxicological principles (dose-response, thresholds, mixtures, bioaccumulation), exposure routes and pathways through air, water, soil and food, susceptible life stages and populations, and the evidence base behind toxicity values, as used by environmental health, remediation and chemicals work.",
   [("A", "Toxicity depends on dose, duration, route of exposure and the susceptibility of the exposed person or organism."),
    ("L1", "A complete exposure pathway needs a source, a release and transport mechanism, a point of exposure and a route of entry."),
    ("L2", "Persistent, bioaccumulative substances can reach higher concentrations in organisms at higher trophic levels than in the environment."),
    ("L2", "Children, pregnant people and some occupational groups can face higher exposure or susceptibility at the same environmental concentration.")],
   [(ST("6.7.4", 1), "Evaluate the toxicity of environmental contaminants at a site from published toxicity values, documenting their sources and uncertainty.", [C, ("seed:v1-6.7.1", "contributing")], "WF-ASSESS", "remote", "partial"),
    (ST("6.7.4", 2), "Assess exposure pathways for chemicals in air, water, soil and food at a site, identifying complete and incomplete pathways.", [C, ("seed:v1-6.7.1", "contributing")], "WF-ASSESS", "remote-capable", "partial"),
    (ST("6.7.4", 3), "Identify vulnerable populations and exposure scenarios for a site, stating the evidence for each scenario.", [C, ("seed:v1-6.7.1", "contributing")], "WF-ASSESS", "remote-capable", "partial")])
print("batch G written")
