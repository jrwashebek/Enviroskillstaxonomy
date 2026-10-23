"""WP-10 L5 watch items (ADR-0015 s2; SPEC 5.15): DC-CAND-17, PS-C19, FS-C16 (TN-C13 stays held and is not authored).

A watch item = a signal cluster + a hypothesized entity, review-by +12 months, lapses without new evidence.
Promotion to lifecycle `proposed` needs >= 3 independent signals of >= 2 types from >= 2 sector actors, or one
mandate with an effective date (vocab/lifecycle_states.yaml). Each item carries its counter-signal (FS s7).
"""
from wp10_common import base, provenance, write_yaml_record, WATCH_REVIEW_BY

ITEMS = [
    dict(cand="DC-CAND-17", key="supervise-agentic-ai-workflows",
         etype="Competency", label="Supervise agentic AI workflows in environmental analysis",
         fn=("Scope tasks delegated to AI agents that plan and take multi-step actions; set permissions and stop conditions; "
             "insert checkpoints; review action logs; detect silent failure; and answer for the result."),
         signals=["seed:sig/capability/draftnepabench-coding-agents", "seed:sig/deployment/agentic-use-cases-usda-doi-epa-2025",
                  "seed:sig/foresight/ws-29-mercor-agent-training"],
         sources=["DC-001", "DC-032", "FS-038", "LM-110"],
         counter=("No environmental agentic use case reaches deployed stage in the 2026 federal inventory, and no posting or PD in the "
                  "October 2026 baseline names agent supervision duties; or agent tasks are absorbed by existing AI-output validation (DC-CAND-01/-13)."),
         note=("Signals span three families (capability, deployment, postings) and two sector actors (federal, private), so the ADR-0015 "
               "count for 'proposed' is close; evidence remains S because environmental deployments are not evidenced. Disposition: "
               "candidate_disposition.csv row DC-CAND-17 (watch).")),
    dict(cand="PS-C19", key="price-disclose-ai-augmented-services",
         etype="Competency", label="Price and disclose AI-augmented environmental services",
         fn=("Estimate effort and price work when AI changes labour hours; choose fixed-fee or value pricing; disclose AI use and "
             "validation steps to clients and regulators."),
         signals=["seed:sig/foresight/ws-13-consulting-ai-comment-tools", "seed:sig/policy/omb-m-26-04-llm-contract-terms"],
         sources=["FS-008", "LM-111"],
         counter=("Public procurement and consulting contracts keep hour-based billing with no AI-use disclosure clauses through the "
                  "2027 review; or disclosure is handled by a generic procurement competency rather than an environmental one."),
         note="Two signals of two types (deployment, policy) from two sector actors; S/J evidence. Confirm with firm disclosures, procurement clauses and contract templates (PS)."),
    dict(cand="FS-C16", key="translate-climate-risk-data-for-communities",
         etype="Competency", label="Translate climate-risk data into navigable adaptation options for communities",
         fn=("Turn hazard, exposure and funding information into options small jurisdictions and households can act on; broker "
             "technical assistance as federal support thins."),
         signals=["seed:sig/foresight/ws-08-disaster-database-discontinued", "seed:sig/foresight/ws-10-obbba-ira-rescissions"],
         sources=["FS-037", "FS-036"],
         counter=("No state or local posting in the baseline or the next two quarterly diffs names the function, and rewritten v1 1.5.3 "
                  "(which absorbs DB-C38) covers it without a distinct deliverable."),
         note="Overlaps rewritten v1 1.5.3; watch until distinct demand is documented in state/local postings (SL, IA). Both signals are supply-side (data and funding withdrawal), not demand."),
]

# TN-C13 is NOT authored here: it stays held and quarantined (data/v2/governance/tribal_hold.yaml lists TN-C01..TN-C13).
# No signals are authored or linked for it under the Tribal gate; a Tribal Advisory Council decides whether and how it
# is described (ADR-0007; candidate_disposition.csv row TN-C13).
WATCH_DIR = "data/v2/core/watch-items"


def build():
    recs = []
    for it in ITEMS:
        r = base("seed:watch-" + it["cand"], "WatchItem", it["label"], editorial_note=it["note"],
                 scope_note="Counter-signal (what would show it is not forming): " + it["counter"],
                 notation=[{"scheme": "candidateDisposition", "value": it["cand"]}])
        r.update({
            "lifecycleState": "watch",
            "reviewBy": WATCH_REVIEW_BY,
            "signals": it["signals"],
            "hypothesizedEntity": {"type": it["etype"], "label": {"en": it["label"]}, "functionStatement": {"en": it["fn"]}},
            "outcome": "open",
            "provenance": provenance(it["sources"], "S", adr="ADR-0015"),
        })
        recs.append(r)
    for r in recs:
        write_yaml_record(WATCH_DIR, r)
    return {"WatchItem": len(recs)}
