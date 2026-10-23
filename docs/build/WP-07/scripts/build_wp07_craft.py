#!/usr/bin/env python3
"""Write WP-07 craft ratings: three llm-rater passes over the WP-07 task statements (codebook
validation/codebook_craft_ratings.md, emst-craft-codebook@1.0.0-draft, ordinal 0/1/2).

Procedure (honest description, also stored in each record's `method`): for each pass the task statements alone were
listed in a different random order (seeds 1, 22, 333; no competency, v1 code or prior label shown) and rated FC/DC/SC
by the codebook's decision procedure. The same model instance authored the tasks, so the passes are not blind to
authorship; they are run-to-run consistency passes of one rater type, never inter-rater reliability or SME agreement
(protocol_llm_coder_gate.md §1.1). Values are draft evidence (evidence label S).

Usage: python3 docs/build/WP-07/scripts/build_wp07_craft.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(HERE))
import emstlib as L  # noqa: E402
import wp07_content as C  # noqa: E402

OUT = REPO / "data" / "v2" / "assessments" / "emst-craft@0.1"
GEN = "2026-10-23T15:00:00Z"
SEEDS = {1: 1, 2: 22, 3: 333}

# Ratings keyed by the exact task statement prefix (first 60 characters) -> {pass: (FC, DC, SC, confidence)}
R = {}
def r(text, p1, p2, p3):
    R[text] = {1: p1, 2: p2, 3: p3}

h, m, l = "high", "med", "low"
r("Pair departing and early-career staff on live assignments", (1,0,0,m), (1,0,0,m), (1,0,0,m))
r("Review an AI-generated project schedule or cost forecast", (1,1,0,m), (1,1,0,m), (1,1,0,m))
r("Prepare a shared message map with partner agencies", (0,1,2,l), (0,1,2,l), (0,1,2,l))
r("Design a task-book style qualification record", (1,0,1,m), (1,0,1,m), (1,0,1,m))
r("Report near misses and unsafe conditions", (1,0,0,m), (1,0,0,m), (1,0,0,m))
r("Design a unit learning-from-incidents process", (1,0,0,l), (1,0,0,l), (1,0,0,l))
r("Record a field walk-through with a departing colleague", (2,0,0,m), (2,0,0,m), (2,0,0,m))
r("Review an AI-generated system map or causal summary", (1,1,0,m), (1,1,0,m), (1,1,0,m))
r("Run two-way knowledge exchanges", (1,1,0,l), (1,1,0,l), (1,1,0,l))
r("Decide whether to pursue a funding or contract opportunity", (0,0,1,m), (0,0,1,m), (0,0,1,m))
r("Review project progress against the baseline", (0,0,0,h), (0,0,0,h), (0,0,0,h))
r("Review a trainee's AI-assisted work product", (1,1,0,m), (0,1,0,l), (1,1,0,m))
r("Trace a proposed action's second-order effects", (1,2,1,l), (1,2,1,l), (1,2,1,l))
r("Conduct a no-blame review of a near miss or incident", (1,1,0,m), (1,0,0,l), (1,1,0,m))
r("Specify a by-hand quota of unaided work products", (0,1,0,l), (0,1,0,l), (0,1,0,l))
r("Supervise a trainee's repetitions of a formation task", (1,0,0,m), (1,0,0,m), (1,0,0,m))
r("Plan rotations and mentored field assignments", (1,0,0,m), (1,0,0,m), (1,0,0,m))
r("Review an AI-drafted scope of work", (0,0,1,m), (0,0,1,m), (0,0,1,m))
r("Maintain the project schedule baseline", (0,0,0,h), (0,0,0,h), (0,0,0,h))
r("Give corrective feedback after each observed task", (1,0,0,l), (1,0,0,m), (1,0,0,m))
r("Verify an AI-drafted or machine-translated risk notice", (0,1,0,m), (0,1,0,m), (0,1,1,l))
r("Manage a subcontractor's deliverables and invoices", (0,0,1,l), (0,0,0,l), (0,0,1,l))
r("Prepare a contingency plan for each critical project risk", (0,0,0,m), (0,0,0,m), (0,0,0,m))
r("Prepare a budget and justification for a grant application", (0,0,1,l), (0,0,1,l), (0,0,1,l))
r("Prepare a handover record of open commitments", (1,0,1,m), (1,0,1,m), (1,0,1,m))
r("Review an AI-drafted proposal section", (0,0,1,m), (0,0,1,m), (0,0,1,m))
r("Invoice project work against the agreement's billing terms", (0,0,0,h), (0,0,0,h), (0,0,0,h))
r("Conduct a structured critical-decision interview", (1,1,0,l), (1,1,0,l), (1,1,0,l))
r("Advise leadership on the formation consequences", (0,1,1,l), (0,1,1,l), (0,1,1,l))
r("Prepare a change order or agreement modification", (0,0,2,l), (0,0,1,l), (0,0,2,l))
r("Sequence field work within seasonal, weather and regulatory", (1,0,1,m), (1,0,1,m), (1,0,1,m))
r("Negotiate a scope change with a client or partner", (0,0,2,m), (0,0,2,m), (0,0,2,m))
r("Draft a public advisory that states the hazard", (0,1,1,m), (0,1,1,m), (0,1,1,m))
r("Test a draft risk message for comprehension", (0,1,0,l), (0,1,0,l), (0,1,0,l))
r("Write a technical approach that answers each evaluation", (0,1,1,l), (0,1,1,l), (0,1,1,l))
r("Identify knowledge held by one or a few people in a unit", (0,1,0,l), (0,0,0,l), (0,1,0,l))
r("Check a proposal or application against the solicitation", (0,0,1,m), (0,0,0,l), (0,0,1,m))
r("Rate a trainee's observed performance of position tasks", (1,0,1,m), (1,0,1,m), (1,0,1,m))
r("Certify a candidate's qualification for a position", (0,0,2,l), (0,0,1,l), (0,0,2,l))
r("Run quality review of a deliverable before release", (0,1,0,m), (0,1,0,m), (0,1,0,m))
r("Deliver a pre-work safety briefing that covers site hazard", (2,0,0,h), (2,0,0,h), (2,0,0,h))
r("Draft a scope of work with measurable deliverables", (0,0,1,m), (0,0,1,m), (0,0,1,m))
r("Review an AI-generated summary of a departing expert's rec", (1,1,0,l), (1,1,0,l), (1,1,0,l))
r("Calculate estimate at completion from actual costs", (0,1,0,m), (0,1,0,m), (0,1,0,m))
r("Exercise stop-work authority when field, facility or incid", (2,0,0,h), (2,0,0,h), (2,0,0,h))
r("Justify a budget revision to the client or sponsor", (0,0,1,m), (0,0,1,m), (0,0,1,m))
r("Analyze a workflow to identify which entry-level tasks form", (1,1,0,l), (1,1,0,l), (1,1,0,l))
r("Design development pathways that credit prior experience", (0,0,1,l), (0,0,1,l), (0,0,1,l))
r("Verify that a successor can apply transferred knowledge", (1,0,0,m), (1,0,0,m), (1,0,0,m))
r("Monitor contractor or partner deliverables against the agre", (0,0,1,m), (0,0,1,m), (0,0,1,m))
r("Facilitate a participatory system-mapping session", (0,1,1,m), (0,1,1,m), (0,1,1,m))
r("Map a management problem as interacting ecological, institu", (1,2,1,m), (1,2,1,m), (1,2,1,l))
r("Compare alternative interventions on a system map", (0,2,1,m), (0,2,1,m), (0,2,1,m))
r("Design a staged-exposure sequence for an entry role", (1,1,0,l), (1,1,0,l), (1,1,0,l))
r("Document qualification or entrustment decisions", (0,0,1,m), (0,0,1,m), (0,0,1,m))
r("Review a template- or AI-generated hazard briefing", (2,1,0,h), (2,1,0,h), (2,1,0,h))
r("Break a large project into phased work packages", (0,0,0,h), (0,0,0,h), (0,0,0,h))
r("Prepare a project budget that ties labour, subcontract", (0,0,1,m), (0,0,1,m), (0,0,1,m))
r("Identify project risks such as weather delays, access limit", (1,0,1,m), (1,0,1,m), (1,0,1,m))
r("Answer public questions about an uncertain environmental ri", (0,1,1,m), (0,1,1,m), (0,1,1,m))
r("Evaluate whether a redesigned workflow still forms judgment", (1,2,0,l), (1,2,0,l), (1,2,0,l))


def main():
    tasks = [t for c in C.COMPETENCIES for t in c["tasks"]]

    def look(text):
        hits = [k for k in R if text.startswith(k)]
        return hits[0] if len(hits) == 1 else None

    missing = [t["text"] for t in tasks if look(t["text"]) is None]
    unused = set(R) - {look(t["text"]) for t in tasks}
    if missing or unused:
        raise SystemExit(f"rating table mismatch: missing={missing} unused={sorted(unused)}")
    for n in (1, 2, 3):
        rows = []
        rater = f"emstagent:lc-craft-rater-{n}@wp07"
        for t in tasks:
            fc, dc, sc, conf = R[look(t["text"])][n]
            stem = t["key"][len("seed:"):]
            rows.append({
                "id": f"seed:asm/wp07-lc-pass{n}/{stem}", "type": "CraftRating",
                "prefLabel": {"en": f"WP-07 craft pass {n} rating of {t['key']}"},
                "layer": "L5", "module": "core", "status": "draft", "license": "CC0-1.0", "sensitivity": "public",
                "task": t["key"], "taskTextSha256": L.text_sha256(t["text"]), "scale": "ordinal-0-2",
                "values": {"FC": fc, "DC": dc, "SC": sc},
                "raterType": "llm", "raterId": rater, "assessedAt": "2026-10-23",
                "method": (f"emst-craft-codebook@1.0.0-draft decision procedure; statements only, shuffled (seed {SEEDS[n]}); "
                           "same model instance that authored the tasks, so not blind to authorship; run-to-run consistency "
                           "pass, not inter-rater reliability"),
                "confidence": conf, "instrument": "emst-craft@0.1", "codebookVersion": "emst-craft-codebook@1.0.0-draft",
                "evidenceLabel": "S", "sources": [],
                "provenance": {"method": "llm-assisted", "agent": [rater], "generatedAt": GEN, "toolVersion": "claude-opus-5-5",
                               "promptVersion": "wp07-craft-pass@1", "evidenceLabel": "S", "reviewStatus": "unreviewed"}})
        L.write_jsonl(OUT / f"wp07-lc-pass{n}.jsonl", rows)
        print(f"pass {n}: {len(rows)} ratings")


if __name__ == "__main__":
    main()
