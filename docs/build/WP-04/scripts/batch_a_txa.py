"""Batch A: TX-A transversal floor (DC-CAND-01, -02, -13 + craft enactments, v1 7.2.3, DC-CAND-05)."""
from lib import (Bundle, competency, craft_enactment, df, indicator, rewrite_seed_competency, rewrite_seed_task, task,
                 write)

CAND = lambda c: [{"scheme": "EMST-candidate", "value": c}]  # noqa: E731
OUT_T = []

# =============================================================================== DC-CAND-01
C = "seed:DC-CAND-01"
T = {k: f"seed:dc-01-{k}" for k in ("interpret-product", "flag-limits", "review-release", "set-product-standard")}
OUT_T += [
    task(T["interpret-product"], "Interpret an environmental map, chart or monitoring summary before using it in a decision, stating what was measured, where, when and at what resolution.",
         [C], "WF-ASSESS", "remote-capable", "partial", regime={"mentorshipDependence": "L", "placeBoundness": "general", "currencyDecay": "L"},
         sources=["DC-044", "DC-035"]),
    task(T["flag-limits"], "Flag the limits of a data product received from others, such as scale mismatch, unrepresentative samples, shifted baselines or missing data, before relying on it.",
         [C], "WF-MONITOR", "remote-capable", "partial", regime={"mentorshipDependence": "M", "placeBoundness": "general", "currencyDecay": "M"},
         sources=["DC-044"]),
    task(T["review-release"], "Review a colleague's environmental data product before release, returning specific corrections to its stated sources, resolution and limitations.",
         [C], "WF-MONITOR", "remote", "partial", sources=["DC-044"]),
    task(T["set-product-standard"], "Set the organizational standard for how environmental data products state their sources, resolution and limitations, auditing compliance across a programme.",
         [C], "WF-MANAGE", "remote", "partial"),
]
b = Bundle(C, "dc-cand-01")
b.ind("L1", "States what an unfamiliar map, chart or monitoring summary measured, with its unit, extent, resolution and source, matching the answer key.", "u", ["ws"], [T["interpret-product"]])
b.ind("L1", "Names at least two things a given data product cannot show before using it, citing the product's scale, sample or period.", "u", ["ws"], [T["interpret-product"], T["flag-limits"]])
b.ind("L2", "Detects planted problems in a briefing product, such as a mismatched baseline or truncated axis, explaining how each would change the conclusion.", "u", ["sews"], [T["flag-limits"]], attr="cpx")
b.ind("L2", "Identifies a scale mismatch between a data product and the decision it is used for, recommending a product at the decision's scale.", "u", ["ws"], [T["flag-limits"]], attr="cpx")
b.ind("L3", "Reviews colleagues' data products before release, returning corrections that the authors can act on without further clarification.", "u", ["pr"], [T["review-release"]], attr="sco")
b.ind("L3", "Writes the limitations section of a decision product, stating what the data cannot support and which result would change the recommendation.", "u", ["pr"], [T["review-release"]], attr="kno")
b.ind("L4", "Sets an organizational standard for how data products state sources, resolution and limits, documenting the basis for each requirement.", "u", ["pr", "bars"], [T["set-product-standard"]], attr="gui")
b.ind("L4", "Audits compliance with the data-product standard across a programme, reporting deviations by product type to programme leadership.", "u", ["ra"], [T["set-product-standard"]], attr="sco")
b.write_indicators()
write(competency(
    C, "Interpret and question environmental data products in everyday work",
    "The capability to read maps, charts, dashboards, model outputs and monitoring summaries correctly and to recognize their limits before relying on them. It covers what was measured, where, when, how and at what resolution. It excludes producing the analysis, which belongs to data-craft practice competencies.",
    "Reads environmental data products such as maps, charts, dashboards, model outputs and monitoring summaries correctly; identifies what was measured, where, when, by whom and at what resolution; recognizes the limits of a product before relying on it; and asks the questions that expose misuse, such as scale, sample, baseline and missing data.",
    "transversal", ("L1", "L4"), b.levels(), cluster="TX-A", lifecycle="established", evidence="J",
    sources=["DC-044", "DC-035", "DC-030"], alt=["Environmental data literacy"], notation=CAND("DC-CAND-01"),
    reusability="transversal",
    note="TX-A universal floor: every role profile carries L1 (ADR-0025 §1; P-DC-05). Candidate row DC-CAND-01 (core-v2.0). Basis [J]: DC report §3 tier DC-1; anchors DC-ANC-001…004. Crosswalked to the DOL AI Literacy Framework only where data literacy meets AI use (X12)."))

# =============================================================================== DC-CAND-02
C = "seed:DC-CAND-02"
T = {k: f"seed:dc-02-{k}" for k in ("decide-use", "direct-tool", "check-output", "protect-inputs", "disclose-use", "team-guidance", "role-requirements")}
OUT_T += [
    task(T["decide-use"], "Decide whether an approved AI tool may be used for a work task, given the data class involved and the cost of an undetected error.",
         [C], "WF-MANAGE", "remote", "partial", lifecycle="emerging", sources=["DC-016", "DC-013"]),
    task(T["direct-tool"], "Direct an AI tool with the task context, source documents and constraints it needs, iterating on its output until the draft meets the work standard.",
         [C], "WF-ASSESS", "remote", "partial", lifecycle="emerging", sources=["DC-016"]),
    task(T["check-output"], "Check every factual claim and citation in an AI-assisted draft against its source before the draft enters a work product.",
         [C, ("seed:DC-CAND-13", "contributing")], "WF-MONITOR", "remote", "partial", lifecycle="emerging", sources=["DC-016", "DC-001"]),
    task(T["protect-inputs"], "Withhold sensitive, controlled or confidential-business information from AI tools not approved for that data class, following the employer's data-handling rules.",
         [C, ("seed:DC-CAND-07", "contributing")], "WF-MANAGE", "remote", "no", lifecycle="emerging", sources=["DC-016"]),
    task(T["disclose-use"], "Disclose AI involvement in a work product by recording the tool, version, purpose, checks performed and changes made.",
         [C, ("seed:DC-CAND-05", "contributing")], "WF-MONITOR", "remote", "no", lifecycle="emerging", sources=["DC-008"]),
    task(T["team-guidance"], "Write task-specific guidance for a team on where AI may and may not be used in a workflow, illustrated with local failure examples.",
         [C], "WF-LEARN", "remote", "partial", lifecycle="emerging"),
    task(T["role-requirements"], "Set role-based AI-use and literacy requirements for an organization, measuring through scored work samples whether staff meet them.",
         [C], "WF-MANAGE", "remote", "partial", lifecycle="emerging", sources=["DC-017"]),
]
b = Bundle(C, "dc-cand-02")
b.ind("L1", "Checks that an AI tool is approved for the data class before entering task information, withholding sensitive items such as rare-species locations.", "a", ["sews", "sjt"], [T["protect-inputs"], T["decide-use"]], lifecycle="emerging")
b.ind("L1", "Verifies each factual claim and citation in an AI-assisted draft against a source, correcting or removing any claim that cannot be traced.", "a", ["sews"], [T["check-output"]], lifecycle="emerging", safety=True)
b.ind("L1", "Labels AI-assisted content in a work product where the employer's rules require disclosure, recording the tool used and the checks performed.", "a", ["ra"], [T["disclose-use"]], lifecycle="emerging")
b.ind("L2", "Declines AI use for a task where checking the output would cost more than doing the work by hand, and documents the basis.", "a", ["sjt", "pr"], [T["decide-use"]], attr="aug", lifecycle="emerging")
b.ind("L2", "Directs an AI tool with the context and source documents a task needs, checking each iteration against the work standard before accepting the draft.", "a", ["ws"], [T["direct-tool"]], attr="aug", lifecycle="emerging")
b.ind("L2", "Records the prompt, tool version and output whenever an AI-assisted result enters a work product, so that a reviewer can check it.", "a", ["ra"], [T["disclose-use"]], attr="aug", lifecycle="emerging")
b.ind("L3", "Coaches team members on AI use in a workflow, reviewing their AI-assisted products and returning documented corrections.", "a", ["tbo", "pr"], [T["team-guidance"]], attr="for", lifecycle="emerging")
b.ind("L3", "Writes task-specific guidance stating where AI may and may not be used in a workflow, illustrated with failures observed locally.", "u", ["pr"], [T["team-guidance"]], attr="gui", lifecycle="emerging")
b.ind("L4", "Sets role-based AI-use rules and literacy requirements for an organization, specifying the work products each role must be able to show.", "u", ["pr", "bars"], [T["role-requirements"]], attr="sco", lifecycle="emerging")
b.ind("L4", "Measures whether staff meet the organization's AI literacy requirements through scored work samples, reporting gaps by role.", "u", ["pr"], [T["role-requirements"]], attr="sco", lifecycle="emerging")
b.write_indicators()
write(competency(
    C, "Use AI tools responsibly in everyday environmental work",
    "The capability to decide whether and how to use a general-purpose or embedded AI tool for a work task, direct it with adequate context, check its output before acting, protect sensitive information and disclose AI involvement, within the employer's rules. It excludes designing review systems and governing AI portfolios, which are data-craft specialist competencies.",
    "Decides whether and how to use a general-purpose or embedded AI tool for an environmental work task; gives it adequate context; checks outputs for accuracy, completeness and fitness before acting; keeps sensitive and controlled information out of unapproved tools; discloses AI involvement in work products; and follows the employer's AI rules.",
    "transversal", ("L1", "L4"), b.levels(), cluster="TX-A", lifecycle="emerging", evidence="E",
    sources=["DC-015", "DC-016", "DC-013", "DC-001", "DC-017"], alt=["Everyday AI literacy"], notation=CAND("DC-CAND-02"),
    reusability="transversal",
    note="TX-A universal floor: every role profile carries L1 (ADR-0025 §1; P-DC-05). Candidate row DC-CAND-02 (core-v2.0). Lifecycle emerging: enterprise AI assistants are deployed agency-wide with training (DC-013, DC-001); DOL frames AI literacy for the whole public workforce (DC-015). Crosswalked to the DOL AI Literacy Framework (X12, data/v2/crosswalks/dol-ai-literacy/). Tool and policy names live in L4/L5, never in this text."))

# =============================================================================== DC-CAND-13 (+ enactments)
C = "seed:DC-CAND-13"
SC_ENA, FC_ENA, DC_ENA = "seed:v1-7.1.4-A", "seed:ena-dc-cand-13-fc", "seed:ena-dc-cand-13-dc"
T = {"v1t1": "seed:v1-7.2.1-T1", "v1t2": "seed:v1-7.2.1-T2", "v1t3": "seed:v1-7.2.1-T3",
     "sample": "seed:dc-13-sample-validate", "draft": "seed:dc-13-verify-ai-draft", "lead": "seed:dc-13-lead-high-stakes",
     "standard": "seed:dc-13-set-validation-standard", "batch-accept": "seed:dc-13-accept-batch",
     "comments": "seed:dc-13-check-comment-grouping", "record": "seed:dc-13-record-ai-in-record"}
OUT_T += [
    rewrite_seed_task(T["v1t1"], "Evaluate AI-generated species identifications, habitat assessments or ecological predictions against field observations, accepting, correcting or rejecting each before use.",
                      [C], "WF-MONITOR", "remote-capable", "yes", lifecycle="emerging",
                      regime={"mentorshipDependence": "H", "placeBoundness": "ecosystem-type", "currencyDecay": "M"}),
    rewrite_seed_task(T["v1t2"], "Check an AI-assisted regulatory analysis or compliance summary against the applicable legal text and source records before it enters a decision document.",
                      [C], "WF-REVIEW", "remote", "partial", lifecycle="emerging"),
    rewrite_seed_task(T["v1t3"], "Record the validation findings for an AI-generated product, stating what was checked, what was changed and the confidence the check supports.",
                      [C, ("seed:DC-CAND-05", "contributing")], "WF-MONITOR", "remote", "partial", lifecycle="emerging"),
    task(T["sample"], "Validate a large batch of AI detections or comment codes by drawing a defined sample, reviewing it and estimating the batch error rate.",
         [C], "WF-MONITOR", "remote", "partial", lifecycle="emerging", sources=["DC-001"], evidence="E"),
    task(T["draft"], "Verify an AI-drafted section of an environmental document against the cited source records, correcting unsupported statements before the section goes forward.",
         [C], "WF-REVIEW", "remote", "partial", lifecycle="emerging", sources=["DC-001", "DC-032"], evidence="E",
         note="Absorbs FH-C15 (AI drafting with documented human review; candidate_disposition merge-into DC-CAND-13)."),
    task(T["lead"], "Lead validation of an AI output for a novel or high-stakes use, explaining to the decision-maker the confidence the validation supports.",
         [C], "WF-MONITOR", "remote-capable", "yes", lifecycle="emerging"),
    task(T["standard"], "Set an organizational validation standard for AI-assisted environmental analysis, revising it against the failures logged in operational use.",
         [C], "WF-MONITOR", "remote", "partial", lifecycle="emerging"),
    task(T["batch-accept"], "Set acceptance rules for batches of AI outputs from estimated error rates and their intervals, stating when a batch must be re-checked.",
         [C], "WF-MONITOR", "remote", "no", lifecycle="emerging", note="DC enactment task (validation at volume)."),
    task(T["comments"], "Sample machine-grouped public comments to confirm that substantive and unique comments were not merged away before responses are drafted.",
         [C, ("seed:DC-CAND-16", "contributing")], "WF-REVIEW", "remote", "partial", lifecycle="emerging", modes=["MODE-ENGAGE"], rel=["public"],
         sources=["DC-001"], evidence="E", note="SC enactment task; legal-adequacy anchor carried from SC-C05 (ADR-0025 ownership ruling)."),
    task(T["record"], "Record in the administrative record which analyses and drafts were AI-assisted and what human review each received before the decision is signed.",
         [C, ("seed:DC-CAND-05", "contributing")], "WF-REVIEW", "remote", "partial", lifecycle="emerging", modes=["MODE-RESOLVE"],
         note="SC enactment task; AI provenance in the administrative record (FS-C03 content stays with SC-C02; this task is the validation-floor side)."),
]
b = Bundle(C, "dc-cand-13")
b.ind("L1", "Checks an AI output against its source or field evidence using the workflow checklist, correcting or rejecting errors before the output is used.", "a", ["sews"], [T["v1t1"], T["v1t2"]], lifecycle="emerging", safety=True)
b.ind("L1", "Rejects a planted fabricated citation and an implausible identification in a seeded work sample, recording why each was rejected.", "a", ["sews"], [T["v1t1"], T["v1t2"]], lifecycle="emerging")
b.ind("L1", "Records which items of an AI-generated product were checked and which were changed, using the workflow's validation record.", "a", ["ra"], [T["v1t3"]], lifecycle="emerging")
b.ind("L2", "Validates a batch of AI outputs by drawing a defined sample and estimating the batch error rate within a stated tolerance.", "a", ["ws", "sews"], [T["sample"]], attr="cpx", lifecycle="emerging")
b.ind("L2", "Flags omissions and out-of-scope answers in AI outputs, as well as errors, across the document and data types met in own work.", "a", ["sews"], [T["draft"], T["v1t2"]], attr="cpx", lifecycle="emerging")
b.ind("L3", "Validates AI outputs for a novel or high-stakes use, explaining to the decision-maker the confidence the result supports.", "a", ["bars", "pr"], [T["lead"]], attr="cpx", lifecycle="emerging")
b.ind("L3", "Reviews colleagues' AI-assisted products before release, returning documented corrections where their checks were incomplete.", "a", ["pr"], [T["lead"]], attr="sco", lifecycle="emerging")
b.ind("L4", "Sets an organizational standard for checking AI-assisted analyses, specifying evidence types and sample sizes by consequence of error.", "a", ["pr", "bars"], [T["standard"]], attr="gui", lifecycle="emerging")
b.ind("L4", "Revises the validation standard against failures logged in operational use, documenting each change and its basis.", "a", ["pr"], [T["standard"]], attr="sco", lifecycle="emerging")
b.write_indicators()

# --- DC craft enactment indicators (validation at volume)
dc_inds = [
    indicator("seed:dc-cand-13-dc-l2-a", C, "L2", "Designs a stratified check of AI outputs by confidence band or condition, so that the batch error rate carries a stated interval.", "a", ["ws"], [T["sample"]], attr="cpx", lifecycle="emerging"),
    indicator("seed:dc-cand-13-dc-l3-a", C, "L3", "Sets acceptance rules for a batch of AI outputs from the estimated error rate, rejecting batches whose interval exceeds the tolerance.", "a", ["ws", "pr"], [T["batch-accept"]], attr="gui", lifecycle="emerging"),
    indicator("seed:dc-cand-13-dc-l3-b", C, "L3", "Compares error rates across conditions such as habitat type or document class, flagging conditions where the tool should not be used.", "a", ["ws"], [T["batch-accept"], T["sample"]], attr="cpx", lifecycle="emerging"),
]
# --- SC craft enactment indicators (legal-adequacy anchors carried from SC-C05; authorization from v1 7.1.4)
sc_inds = [
    indicator("seed:dc-cand-13-sc-l2-a", C, "L2", "Samples machine-grouped public comments, confirming that substantive and unique comments were not merged away before responses are drafted.", "a", ["sews"], [T["comments"]], attr="cpx", lifecycle="emerging", safety=True),
    indicator("seed:dc-cand-13-sc-l2-b", C, "L2", "Checks each AI-drafted response to a substantive comment against the comment and the record, so that every response states its reasoned basis.", "a", ["sews", "ra"], [T["comments"]], attr="kno", lifecycle="emerging"),
    indicator("seed:dc-cand-13-sc-l3-a", C, "L3", "Tests an AI-assisted analysis against the applicable legal requirements for the decision, documenting the basis for accepting or revising it.", "a", ["md", "ra"], [T["v1t2"]], attr="kno", jv=True, lifecycle="emerging", safety=True),
    indicator("seed:dc-cand-13-sc-l3-b", C, "L3", "Records which analyses and drafts were AI-assisted, with the human review each received, in the administrative record before the decision is signed.", "a", ["ra"], [T["record"]], attr="sco", lifecycle="emerging"),
    indicator("seed:dc-cand-13-sc-l4-a", C, "L4", "Authorizes the oversight design for an AI-assisted decision workflow, stating the accountable official, the review points and the conditions for suspension.", "a", ["pr", "md"], ["seed:v1-7.1.4-T1"], attr="sco", lifecycle="emerging"),
]
for r in dc_inds + sc_inds:
    write(r, "indicators")

write(craft_enactment(
    DC_ENA, C, "DC", "Data craft enactment of AI-output validation: sampling design and error estimation at volume",
    "The data-craft enactment carries the statistical side of validation: designing which AI outputs to check, estimating error rates and their uncertainty by condition, setting batch acceptance rules, and identifying conditions where a tool should not be used. It applies wherever outputs are too many to check one by one, such as comment sets, detections and classifications.",
    indicator_variants=[r["id"] for r in dc_inds], additional_tasks=[T["sample"], T["batch-accept"]], sources=["DC-001", "DC-037"], evidence="E",
    editorial="ADR-0025 §2 layer 3 (DC enactment = sampling design and error estimation for validation at volume). DC is steward of record for the technical content of responsible-AI anchors."))
def _fc_owner_is_dc():
    import os
    import yaml
    p = "/home/claude/emst/data/v2/core/enactments/seed-ena-dc-cand-13-fc.yaml"
    if not os.path.exists(p):
        return True
    return "emstagent:A4-DC@wp-04" in yaml.safe_load(open(p))["provenance"]["agent"]


import glob as _g, os as _os  # noqa: E401
_fc_inds = sorted("seed:" + _os.path.basename(p)[5:-5] for p in _g.glob("/home/claude/emst/data/v2/core/indicators/seed-ind-fcena-dc-cand-13-*.yaml"))
_fc_tasks = sorted("seed:" + _os.path.basename(p)[5:-5] for p in _g.glob("/home/claude/emst/data/v2/core/tasks/seed-fc-txa-*.yaml"))
# The FC enactment record is owned by WP-03 (FC) since its 2026-10-23 commit; do not overwrite it.
if _fc_owner_is_dc():
  write(craft_enactment(
    FC_ENA, C, "FC", "Field craft enactment of AI-output validation: ecological plausibility and field ground truth",
    "The field-craft enactment carries the field side of validation: judging whether an AI identification, map or classification is ecologically plausible for the place, season and condition, and producing or commissioning field reference observations when plausibility is in doubt. It links to the core field-craft practice of ground-truthing remote, modelled and AI-generated outputs.",
    additional_tasks=[T["v1t1"]] + _fc_tasks, indicator_variants=_fc_inds or None, sources=["DC-001"], evidence="J",
    editorial="ADR-0025 §2 layer 3 (FC enactment = ecological plausibility and field ground truth). FC-enactment indicators and tasks are WP-03 (FC) outputs, linked here as indicatorVariants and additionalTasks; FC owns their content. Related FC practice: seed:FC-C02 (FC enactment of TX-A per candidate_disposition)."))
write(craft_enactment(
    SC_ENA, C, "SC", "Statecraft enactment of AI-output validation: legal sufficiency, record provenance and authorization of oversight",
    "The statecraft enactment carries what makes validated AI output usable in a public decision: legal sufficiency of AI-assisted analyses and drafts; in comment analysis, that substantive and unique comments survive machine grouping and each receives a reasoned response; AI provenance in the administrative record; and authorization of the oversight design by the accountable official.",
    indicator_variants=[r["id"] for r in sc_inds], additional_tasks=[T["comments"], T["record"], "seed:v1-7.1.4-T1"],
    derived=[df("v1:7.1.4", "split-from", "authorization of the oversight design (ADR-0025 §3; v1_disposition 7.1.4 position 1)")],
    sources=["DC-001", "DC-007"], evidence="E",
    editorial="Split target of v1 7.1.4 (authorization part). SC-C05 merges here and into SC-C02; its legal-adequacy anchors survive as the indicator variants (ADR-0025 ownership ruling). SC co-owns authorization; DC is steward of the technical anchors; IO validates. Drafted by DC for SC (A5) review."))

write(competency(
    C, "Validate AI-generated work products before professional use",
    "The capability to check AI-produced identifications, maps, classifications, summaries, regulatory analyses and drafts against independent evidence before they are used in professional work, at the volume the work produces, and to record what was checked and changed. It excludes designing review architectures and setting model risk tiers, which are data-craft specialist competencies.",
    "Checks AI-produced species identifications, maps, classifications, summaries, regulatory analyses and drafts against independent evidence such as field observation, source documents, applicable legal text and expert knowledge; uses structured sampling when volumes are large; and records what was checked, what was changed and the confidence the validation supports.",
    "transversal", ("L1", "L4"), b.levels(), cluster="TX-A", lifecycle="emerging", evidence="E",
    sources=["DC-001", "DC-045", "DC-016", "DC-032"], derived=[df("v1:7.2.1", "merged-from", "v1 7.2.1 is the writing model; rewritten to observable anchors (ADR-0025)")],
    alt=["Validate AI-generated environmental analyses before professional use", "AI-output validation"], notation=CAND("DC-CAND-13"),
    reusability="transversal", enactments=[FC_ENA, DC_ENA, SC_ENA],
    note="TX-A universal floor: every role profile carries L1 on AI-output validation (ADR-0025 §1). Survivor of the validation cluster: absorbs v1 7.2.1, FS-C01 and FH-C15 (candidate_disposition merge-into DC-CAND-13). Craft enactments: FC (ecological plausibility and ground truth), DC (validation at volume), SC (legal sufficiency, record provenance, authorization of oversight; split part of v1 7.1.4)."))

# =============================================================================== v1 7.2.3 (carry, rewritten)
C = "seed:v1-7.2.3"
T = {"t1": "seed:v1-7.2.3-T1", "t2": "seed:v1-7.2.3-T2", "t3": "seed:v1-7.2.3-T3",
     "checkpoint": "seed:dc-723-checkpoint", "programme": "seed:dc-723-calibration-programme"}
OUT_T += [
    rewrite_seed_task(T["t1"], "Map the reliability of an AI tool across operating conditions by comparing its outputs with independent evidence, recording where it fails.",
                      [C], "WF-MONITOR", "remote-capable", "partial", lifecycle="emerging"),
    rewrite_seed_task(T["t2"], "Decide whether to accept, qualify or override an AI output in operational work, based on whether the case lies inside the tool's validated reliability envelope.",
                      [C], "WF-MONITOR", "remote-capable", "partial", lifecycle="emerging"),
    rewrite_seed_task(T["t3"], "Review past acceptance and override decisions against observed outcomes, updating the team's calibration record and decision heuristics.",
                      [C], "WF-LEARN", "remote", "partial", lifecycle="emerging"),
    task(T["checkpoint"], "Apply an explicit decision checkpoint before accepting an AI output in high-consequence work, naming the independent evidence relied on.",
         [C], "WF-MONITOR", "remote-capable", "partial", lifecycle="emerging", derived=[df("v1:7.2.3:foundational:I3", "rewritten")]),
    task(T["programme"], "Design a team calibration programme that sets reliability-assessment steps, review schedules and documentation rules for AI tools in operational use.",
         [C], "WF-LEARN", "remote", "partial", lifecycle="emerging", derived=[df("v1:7.2.3:advanced:I1", "rewritten")]),
]
b = Bundle(C, "ind-v1-7.2.3")
X = lambda k: [df(k, "rewritten")]  # noqa: E731
b.ind("L1", "Applies an explicit decision checkpoint before accepting an AI output in high-consequence work, naming the independent evidence relied on.", "a", ["sjt", "sews"], [T["checkpoint"]], lifecycle="emerging", safety=True)
b.ind("L1", "Identifies which outputs in own work carry the highest consequence if taken from an AI tool without independent evidence, listing them for the supervisor.", "u", ["sjt"], [T["checkpoint"]], lifecycle="emerging")
b.ind("L1", "Reports to the supervisor when time pressure or workflow design is pushing acceptance of AI outputs without the required checks.", "a", ["sjt"], [T["t2"]], lifecycle="emerging")
b.ind("L2", "Maps an AI tool's reliability across the operating conditions met in own work by testing its outputs against independent evidence.", "a", ["ws"], [T["t1"]], attr="aug", lifecycle="emerging")
b.ind("L2", "Documents each trust decision and its basis in a calibration record that supports later review against outcomes.", "a", ["ra"], [T["t2"], T["t3"]], attr="aug", lifecycle="emerging")
b.ind("L2", "Explains a specific tool's failure modes to colleagues and supervisors, citing the cases in which its outputs failed checks.", "a", ["bars"], [T["t1"]], attr="aug", lifecycle="emerging")
b.ind("L3", "Designs a team calibration programme that sets reliability-assessment steps, review schedules and documentation rules for AI tools in use.", "a", ["pr"], [T["programme"]], attr="sco", lifecycle="emerging")
b.ind("L3", "Checks whether a team is using an AI tool outside its validated reliability envelope, presenting the evidence and a corrective change.", "a", ["pr", "bars"], [T["programme"]], attr="sco", lifecycle="emerging")
b.ind("L3", "Conducts a retrospective review of past trust decisions against outcome data, revising the team's decision heuristics where bias appears.", "a", ["pr"], [T["t3"]], attr="cpx", lifecycle="emerging")
b.ind("L4", "Sets organizational requirements for calibration records and retrospective reviews of AI-assisted decisions, stating the evidence each review must use.", "a", ["pr", "bars"], [T["programme"]], attr="sco", lifecycle="emerging")
b.ind("L4", "Specifies the workload, time and escalation conditions AI-assisted workflows must meet to protect reviewers' calibration, verifying them in periodic audits.", "a", ["pr", "ra"], [T["programme"]], attr="gui", lifecycle="emerging")
# indicator lineage to v1 indicator keys
_lineage = {"l1-a": "v1:7.2.3:foundational:I3", "l1-b": "v1:7.2.3:foundational:I2", "l1-c": "v1:7.2.3:foundational:I4",
            "l2-a": "v1:7.2.3:intermediate:I1", "l2-b": "v1:7.2.3:intermediate:I4", "l2-c": "v1:7.2.3:intermediate:I2",
            "l3-a": "v1:7.2.3:advanced:I1", "l3-b": "v1:7.2.3:advanced:I2", "l3-c": "v1:7.2.3:advanced:I4",
            "l4-a": "v1:7.2.3:expert:I1", "l4-b": "v1:7.2.3:advanced:I3"}
for r in b.inds:
    k = r["id"].split("ind-v1-7.2.3-")[1]
    r["provenance"]["derivedFrom"] = [df(_lineage[k], "rewritten")]
b.write_indicators()
write(rewrite_seed_competency(
    C, "Calibrate trust in AI and automation",
    "The capability to keep an accurate, evidence-based view of when specific AI and automated tools can be trusted, qualified or overridden in one's own and a team's work, avoiding both automation bias and unwarranted rejection, and to update that view from recorded outcomes. It excludes organizational evaluation programmes (evaluation sets and benchmarking).",
    "Maintains an evidence-based calibration of when to trust, qualify or override the outputs of specific AI and automated tools across operating conditions, avoiding both over-trust and unwarranted rejection; applies explicit decision checkpoints in high-consequence work; and updates that calibration from recorded outcomes of past trust decisions.",
    "transversal", ("L1", "L4"), b.levels(), cluster="TX-A", lifecycle="emerging", evidence="J", sources=["DC-045", "DC-001"],
    alt=["Calibrating professional judgment in human-AI collaboration"], reusability="transversal",
    note="Rewritten by WP-04 (ADR-0025 §1 TX-A: 'Calibrate trust in AI and automation'). Operations enactment is the DB practice competency seed:DB-C03 (supervise automated and AI-assisted process control)."))

# =============================================================================== DC-CAND-05
C = "seed:DC-CAND-05"
T = {k: f"seed:dc-05-{k}" for k in ("provenance-record", "lineage-record", "trace-figures", "design-capture", "correction-notice", "set-requirements")}
OUT_T += [
    task(T["provenance-record"], "Record the source, date, version, method and any AI tool used for a dataset or analysis, using the organization's provenance template.",
         [C], "WF-MONITOR", "remote-capable", "no", sources=["DC-002", "DC-034"], evidence="E"),
    task(T["lineage-record"], "Build a lineage record for a derived product that traces inputs, transformations, model and AI steps with versions, and human review to the output.",
         [C], "WF-MONITOR", "remote", "no", sources=["DC-034", "DC-037"], evidence="E"),
    task(T["trace-figures"], "Trace any figure in a released environmental product back to its source data and processing steps when a reviewer or challenger requests it.",
         [C], "WF-MONITOR", "remote", "no", modes=["MODE-RESOLVE"], note="Defence task split from production (ADR-0003 G-2)."),
    task(T["design-capture"], "Design automatic provenance capture into a data pipeline so that tool versions, prompts and reviewers are logged without manual entry.",
         [C, ("seed:DC-CAND-04", "contributing")], "WF-PLAN", "remote", "no"),
    task(T["correction-notice"], "Issue a correction notice for every downstream product when an upstream data or model error is found, listing each affected product and fix.",
         [C], "WF-MONITOR", "remote", "partial"),
    task(T["set-requirements"], "Set provenance requirements across an organization or partnership, including for vendor and machine-produced content entering decision records.",
         [C], "WF-MANAGE", "remote", "partial", sources=["DC-008", "DC-002"], evidence="E"),
]
b = Bundle(C, "dc-cand-05")
b.ind("L1", "Records source, date, version, method and any AI tool used for own data and outputs, so that a colleague can locate every input.", "u", ["ra"], [T["provenance-record"]])
b.ind("L1", "Fills every required field of the organization's provenance template for a field dataset, as confirmed by a second person's check.", "u", ["ra"], [T["provenance-record"]])
b.ind("L2", "Builds a lineage record for a derived product from inputs through transformations, model and AI steps and human review to the output.", "u", ["ws", "ra"], [T["lineage-record"]], attr="cpx")
b.ind("L2", "Traces three numbers chosen by an assessor in a product back to source data within the set time, explaining each processing step.", "u", ["ws"], [T["trace-figures"]], attr="cpx")
b.ind("L3", "Designs provenance capture into a pipeline so that tool versions, prompts and reviewers are logged automatically for every run.", "u", ["pr"], [T["design-capture"]], attr="sco")
b.ind("L3", "Issues a correction notice to every downstream product when an upstream error is found, listing the affected products and fixes.", "u", ["ra"], [T["correction-notice"]], attr="sco")
b.ind("L4", "Sets provenance requirements for an organization or partnership, including how vendor and machine-produced content entering decision records is labelled and checked.", "a", ["pr", "bars"], [T["set-requirements"]], attr="sco")
b.ind("L4", "Audits provenance records across a programme against the requirements, reporting gaps by product type and the corrective actions taken.", "u", ["ra"], [T["set-requirements"]], attr="gui")
b.write_indicators()
write(competency(
    C, "Record provenance and AI involvement in work products",
    "The capability to record and preserve where data and derived products came from: sources and versions, methods, transformations, models and AI systems involved, human review steps and responsible parties, so that findings can be traced, reproduced or corrected. Level 1 is part of the universal floor; levels 2 and above are data-craft practice.",
    "Records, for own data and work products, the sources and versions, collection methods, transformations, models and AI systems involved, human review steps and responsible parties; builds lineage records for derived products; and designs provenance capture into workflows, so that any finding can be traced, reproduced or corrected.",
    "transversal", ("L1", "L4"), b.levels(), cluster="TX-A", lifecycle="established", evidence="E",
    sources=["DC-002", "DC-034", "DC-008", "DC-037"], alt=["Document data provenance and lineage for environmental evidence"],
    notation=CAND("DC-CAND-05"), reusability="transversal",
    note="TX-A at L1 (floor), DC practice at L2 and above (candidate_disposition DC-CAND-05; ADR-0025 §1). Precondition for validation and for SC's defensible administrative record (seed:SC-C02 link). Template and data-standard names live in L4/L5."))

for t in OUT_T:
    write(t, "tasks")
print("batch A written:", len(OUT_T), "tasks")
