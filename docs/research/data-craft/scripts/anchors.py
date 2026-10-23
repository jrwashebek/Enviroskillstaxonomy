import csv, sys
OUT=sys.argv[1]
H=["anchor_id","competency_ref","level","observable_behavior","evidence_of_performance","assessment_method","notes"]
L={1:"1-Foundational",2:"2-Intermediate",3:"3-Advanced",4:"4-Expert"}
R=[]
def add(ref,lvl,beh,ev,meth,note=""):
    R.append([None,ref,L[lvl],beh,ev,meth,note])

# DC-CAND-01 Interpret and question environmental data products
c="DC-CAND-01"
add(c,1,"Given a map, chart or monitoring summary, states correctly what was measured, the unit, the spatial and temporal extent and resolution, and the data source; names at least two things the product cannot show.","Short written interpretation of 2-3 unfamiliar data products scored against a key","Work-sample test (30 min, scored rubric)","Universal (Tier DC-1). Target level for all staff, including field and administrative roles.")
add(c,2,"Detects planted problems in a data product (mismatched baselines, truncated axis, unrepresentative sample, scale mismatch between data and decision, missing-data handling) and explains how each would change the conclusion.","Annotated critique of a flawed briefing product","Work-sample test with seeded errors; inter-rater scoring","")
add(c,3,"Reviews colleagues' data products before release and returns specific, actionable corrections; writes the 'limitations' section of products used for decisions.","Review comments and limitations sections in released products","Portfolio review by two assessors","")
add(c,4,"Sets organizational standards for how data products state sources, resolution and limits, and audits compliance across a program.","Published product standard; audit results","Document review plus structured interview","")

# DC-CAND-02 Use AI tools responsibly
c="DC-CAND-02"
add(c,1,"Before using an AI tool for a task, checks whether the tool is approved for that data class; withholds sensitive or controlled information from unapproved tools; checks every factual claim or citation in an AI output against a source before using it; labels AI-assisted content where required.","Task log from a scenario exercise showing data-handling decisions, checks performed and disclosure","Scenario simulation (e.g., draft a site summary with an assistant; scenario contains a sensitive location and a fabricated citation)","Universal (Tier DC-1). Maps to DOL TEN 07-25 content areas 'evaluating AI outputs' and 'managing AI responsibly' (DC-016). Must be tool-agnostic: the exercise can run on whatever assistant the organization uses.")
add(c,2,"Chooses when not to use AI (e.g., where errors are costly and checking costs more than doing); gives the tool sufficient context; detects omissions as well as errors; records the prompt/version/output when the result enters a work product.","Work product with an AI-use note (tool, version, purpose, checks, changes made)","Portfolio review of 3 work products; spot audit","")
add(c,3,"Coaches a team on safe use; writes task-specific guidance (what AI may and may not be used for in a given workflow, with examples of failures seen locally).","Team guidance document with local failure examples","Document review; observation of coaching","")
add(c,4,"Sets organizational AI-use policy and literacy requirements by role, and measures whether staff meet them (not only whether training was completed).","Role-based AI-use policy; literacy assessment results","Document review plus interview with policy owner","EU Art. 4 now requires 'measures' rather than a guaranteed level (DC-017); this anchor asks for measurement anyway.")

# DC-CAND-05 Provenance and lineage
c="DC-CAND-05"
add(c,1,"Records, for own data and outputs, source, date, version, method and any AI tool used, using the organization's template, so that a colleague can find the inputs.","Completed provenance record for a field dataset or analysis","Work-product audit (can a second person locate every input from the record?)","")
add(c,2,"Builds a lineage record for a derived product (inputs -> transformations -> model/AI steps with versions -> human review -> output) and can reproduce or explain any figure in it on request.","Lineage diagram/record attached to a report or dataset","Trace test: assessor picks three numbers in a product; candidate traces each to source within a set time","CEQ data standard v1.2 'data_record_version' and record-origin fields are a concrete model (DC-034).")
add(c,3,"Designs provenance capture into a pipeline or program (automatic logging of versions, prompts and reviewers) and corrects a downstream product when an upstream error is found.","Pipeline design with provenance fields; documented correction notice","Design review by peer; review of an incident/correction file","")
add(c,4,"Sets provenance requirements across an organization or partnership, including for vendor and AI-generated content entering administrative records, and audits them.","Provenance policy; audit findings; contract clauses","Document review; structured interview","In 2024 only 37% of USDA AI use cases reported complete or widely available training-data documentation (DC-002).")

# DC-CAND-07 Sensitive information protection
c="DC-CAND-07"
add(c,1,"Recognizes sensitive content in own data (rare-species locations, archaeological/cultural sites, Tribal information, personal data) and applies the organization's withholding or generalization rule before sharing.","Shared dataset or map with correct withholding","Scenario test with a mixed dataset containing sensitive items","Cultural-resource and Tribal information rules are owned by SC/TN; this anchors the technical act.")
add(c,2,"Makes and documents a sensitivity determination (reason, category, generalization level, review date), generalizes only the distributed copy, replaces withheld fields with explanatory wording, and checks derived products (summaries, model outputs, figures) for leakage.","Sensitivity determination record; released copy vs stored record","Work-sample test scored against GBIF practices (DC-029)","GBIF: document reason and review date; restrict distributed copy only; never alter stored record (DC-029).")
add(c,3,"Assesses leakage risk in AI and analytics workflows (training sets, embeddings, retrieval corpora, high-resolution model outputs), designs access controls, and negotiates data-sharing terms with data holders.","Risk assessment for an AI/analytics workflow; data-sharing agreement","Design review; structured interview with a data-holder partner (where the partner agrees)","Co-design with TN for Indigenous data; CARE (DC-050).")
add(c,4,"Sets organizational sensitive-data policy, including review cycles and hold-back registers, and accounts to data holders for compliance.","Policy; hold-back register; review-cycle records","Document review; partner feedback","OpenLMP hold-back register is a working pattern (DC-036).")

# DC-CAND-09 Model fitness-for-purpose and validation
c="DC-CAND-09"
add(c,1,"Before using a model output, states the model's intended purpose, input data period and area, and whether the current use falls inside them; flags uses outside that envelope.","Completed fitness-for-use checklist for a model output","Scenario test with in- and out-of-envelope uses","")
add(c,2,"Designs and runs an independent validation (spatially or temporally blocked hold-out or field reference data), reports error by condition (e.g., ecosystem type, season, disturbance class) and identifies where the model should not be used.","Validation report with stratified error and stated domain of applicability","Work-sample: validate a provided model on a provided dataset; scored rubric","Durable practice in EPA 2009 model guidance (DC-051; not re-read).")
add(c,3,"Conducts sensitivity and uncertainty analysis, tests performance under novel (non-analog) conditions, and provides effective challenge to another team's model.","Model evaluation memo including challenge findings","Peer review of an evaluation memo; panel interview","NOAA inventory shows predictability deteriorates under novel conditions (DC-001).")
add(c,4,"Sets validation standards proportional to decision consequence for an organization's model portfolio and decides when models are retired.","Validation standard; retirement decisions with rationale","Document review; structured interview","Links to DC-CAND-19.")

# DC-CAND-11 Uncertainty
c="DC-CAND-11"
add(c,1,"Reports results with the uncertainty provided by the method or tool (interval, confidence class, detection probability) and does not drop it when summarizing.","Summary or briefing slide that retains uncertainty","Work-product review","")
add(c,2,"Identifies the main sources of uncertainty in an analysis (measurement, sampling, model, scenario, AI error), quantifies at least the dominant ones, and states what result would change the recommendation.","Analysis with an uncertainty section and a 'what would change this' statement","Work-sample test; rubric","FBAN/LTAN standards require communicating uncertainty and confidence (DC-047).")
add(c,3,"Translates uncertainty for an authorizing official in decision terms (risk of a wrong call, value of more information), tests the communication with the audience, and holds the caveat under pressure to simplify.","Decision brief; record of audience test; documented disagreement where caveats were contested","Observed briefing (live or recorded) scored by two assessors","SC secondary.")
add(c,4,"Sets organizational conventions for uncertainty language and visuals and evaluates whether decision-makers interpret them correctly.","Conventions guide; comprehension test results","Document review plus evaluation data","")

# DC-CAND-13 Validate AI-generated analyses
c="DC-CAND-13"
add(c,1,"Checks an AI output (species ID, classification, summary, draft) against the source or field evidence using a checklist, corrects or rejects errors, and records what was checked.","Validation checklist with corrections","Work-sample test with seeded errors (incl. a hallucinated citation and an ecologically implausible ID)","Derived from v1 7.2.1 Foundational (DC-045), made observable.")
add(c,2,"Validates outputs across the types met in own work, including omissions and out-of-scope answers; for high-volume outputs, draws and reviews a defined sample and estimates the error rate.","Validation record with sample design and estimated error rate","Work-sample: validate a batch of 200 AI detections or comment codes; score accuracy of the error estimate","FWS DocketScope: 'Results are verified by analysts during comment review' (DC-001).")
add(c,3,"Designs validation protocols for a workflow (what to check, how much, by whom), leads validation of novel or high-stakes uses, and explains to decision-makers the confidence the validation supports.","Validation protocol; validation summary for a decision-maker","Design review plus structured interview","FC secondary for ecological outputs.")
add(c,4,"Sets organizational or sector validation standards for AI-assisted environmental analysis and reviews them against observed failures.","Standard; failure log analysis","Document review","")

# DC-CAND-14 Human-in-the-loop design
c="DC-CAND-14"
add(c,1,"Follows the review steps defined for an AI-assisted workflow and escalates outputs that meet escalation criteria; does not approve outputs not actually reviewed.","Review log showing reviewed items and escalations","Observation or audit of review logs (sampled)","")
add(c,2,"For a workflow, specifies review rates by risk, confidence thresholds, escalation triggers and reviewer qualifications, and shows the reviewer can change the outcome.","Workflow review specification","Design work-sample scored against a rubric","")
add(c,3,"Measures whether review is substantive (override rates, time-on-item, seeded-error catch rate) and redesigns when review degrades into rubber-stamping; keeps reviewers independent of the tool's producer.","Review-quality metrics; redesign record","Audit with seeded errors; panel review of metrics","'Presumed high-impact but not high-impact' designations rest on human review being the principal basis (DC-001).")
add(c,4,"Sets organizational requirements for human oversight by risk tier and reports oversight performance to governance bodies.","Oversight requirements; governance reports","Document review; interview","Authorization of the design is SC (v1 7.1.4).")

# DC-CAND-15 Evaluation sets and benchmarking
c="DC-CAND-15"
add(c,1,"Labels items for a reference set following written guidelines without seeing tool outputs, and flags ambiguous items.","Labeled items with ambiguity flags","Agreement with expert labels on a check subset","OpenLMP gold set: blind annotation (DC-037).")
add(c,2,"Builds a representative reference set for a task (sampling frame, labeling guide, double-labeling of a subset, agreement statistic) and computes precision/recall or equivalent for a tool against it.","Evaluation report with agreement and performance metrics","Work-sample: build and score a small evaluation set","OpenLMP: kappa 0.939 on doubly annotated pages (DC-037).")
add(c,3,"Compares candidate tools and the current human process on the same set, reports error by subgroup or condition, tests LLM-judge scoring against human scoring before relying on it, and recommends adopt/limit/reject.","Comparative evaluation memo with recommendation","Peer review; structured interview","DraftNEPABench uses LLM judges against SME rubrics (DC-032) - judges need human validation.")
add(c,4,"Establishes an organizational evaluation program (shared reference sets, re-testing after model updates, publication of results) and requires local evaluation before adoption or procurement.","Evaluation program charter; re-test records","Document review","")

# DC-CAND-16 LLM-assisted text analysis
c="DC-CAND-16"
add(c,1,"Uses an approved tool to extract or summarize content from a plan, permit or comment set and verifies each extracted statement against the cited passage.","Extraction table with source page/paragraph for each row and verification marks","Work-sample with seeded misattributions","")
add(c,2,"Designs an extraction or coding scheme, runs it over a document set, measures omission and fabrication rates on a sample, and documents limits for the responsible official.","Coded dataset; error-rate memo","Work-sample scored against a gold set","Deployed: USFS plan review, FWS DocketScope; pilots at EPA, BLM, NOAA (DC-001).")
add(c,3,"Builds a reusable pipeline (schema, prompts or models, retrieval, citation tracing, evaluation) whose outputs can enter an administrative record, and maintains it through model changes.","Pipeline documentation; evaluation results across model versions","Design review; re-run test after model swap","SC secondary: legal sufficiency stays with the official.")
add(c,4,"Sets organizational rules for when LLM-derived analyses may enter decision documents and how they are disclosed and audited.","Policy; audit results","Document review; interview","")

# DC-CAND-17 Agentic workflow supervision
c="DC-CAND-17"
add(c,1,"Runs an approved agent on a bounded task, reads its action log, and stops it when it acts outside the task.","Annotated action log","Scenario simulation with an agent that drifts out of scope","Emergent (evidence label S). Re-anchor after the 2026 inventory.")
add(c,2,"Scopes a multi-step task for an agent (inputs, permitted tools, stop conditions, checkpoints), verifies intermediate products and final result, and records responsibility.","Task specification and verification record","Work-sample in sandbox","Coding agents on DraftNEPABench (DC-032).")
add(c,3,"Designs agent workflows for a team with least-privilege permissions, audit logging, and failure-recovery steps; tests for silent failure.","Workflow design; failure tests","Design review; red-team exercise","")
add(c,4,"Sets organizational conditions under which agents may act on systems or records and reviews incidents.","Policy; incident reviews","Document review","")

# DC-CAND-19 Model risk management
c="DC-CAND-19"
add(c,1,"Identifies when a model or AI output they use feeds a consequential decision (payment, permit, enforcement, safety, cultural resources) and checks that it is on the organization's inventory with an assigned owner.","Inventory check record","Scenario test","")
add(c,2,"Completes a model/AI risk assessment for a use (purpose, consequence, failure modes, affected parties, validation status, monitoring plan) and proposes a risk tier.","Risk assessment form","Work-sample scored against a rubric","M-25-21 high-impact definition and minimum practices (DC-007).")
add(c,3,"Provides independent challenge to a model owner, sets monitoring and re-validation triggers (data drift, model update, new use), and recommends pause or retirement when criteria are not met.","Challenge memo; monitoring plan; pause/retire recommendation","Peer review; panel interview","SR 11-7 'effective challenge' as cross-sector precedent (DC-059; not re-read).")
add(c,4,"Runs a model-risk program across a portfolio (inventory, tiering, independent validation, reporting to governance) and is accountable for its results.","Program charter; portfolio report","Document review; interview","USDA FPAC satellite crop-verification models are the environmental high-impact archetype (DC-001).")

for i,r in enumerate(R,1): r[0]=f"DC-ANC-{i:03d}"
with open(OUT,"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(H); w.writerows(R)
print(len(R))
