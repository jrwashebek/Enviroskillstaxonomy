#!/usr/bin/env python3
"""rc.1 fix pass, m7: add the missing review or verification task to the eight competencies the data-method review's
seeded sample found with AI-compressible production and no separate specify, review, verify or defend task
(SPEC §5.5 SHOULD; ADR-0003 G-2; S1 brief). D-DATA; ADR-0032. Idempotent: an existing file is not rewritten.

Each task is a DRAFT with a seed key (status draft; validationStatus draft; evidence label S; LLM-assisted), so it
needs an ID minted by D-BUILD's single writer before any release can carry it (DATA_DONE.md). Only the task and its
`supports` link are written: no role bundle, importance, craft or exposure value is invented. The lint rule
W-LINT-PRODUCTION-REVIEW (scripts/validate_v2.py; validation/production_review_lexicon.yaml) reports every other
competency with the same gap for the content owners.
Run: python3 -I docs/build/rc1-fix/add_review_tasks.py   Licence: Apache-2.0.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rc1lib as R  # noqa: E402

L = R.L
PROMPT = "docs/build/rc1-fix/add_review_tasks.py@rc1-m7"
TASKS = [  # (seed key, competency, module, subsectors, statement)
    ("seed:rc1-m7-adaptation-analysis-review", "emst:core/CMP-94MWBXW", "core", None,
     "Review an adaptation option analysis or climate-adjusted design criteria before adoption, checking each scenario, "
     "return period and assumption against current guidance and recording the corrections made."),
    ("seed:rc1-m7-ecosystem-service-estimate-verify", "emst:core/CMP-G0WT56E", "core", None,
     "Verify an ecosystem service estimate before it is used in a plan, checking the model inputs, beneficiaries and "
     "validation against observations and recording each discrepancy found."),
    ("seed:rc1-m7-legislative-product-verify", "emst:core/CMP-7JXTB4F", "core", None,
     "Verify a bill summary, fiscal note or testimony draft against the bill text and program data before release, "
     "recording each correction and its source."),
    ("seed:rc1-m7-wilderness-analysis-review", "emst:parks/CMP-YS52BS8", "parks", ["L10", "L01"],
     "Review a minimum-requirements analysis or wilderness character trend report before decision, checking indicator "
     "data and baseline methods and recording each correction."),
    ("seed:rc1-m7-biodiversity-analysis-audit", "emst:core/CMP-PYQADZP", "core", None,
     "Audit a biodiversity change analysis before reporting, checking detection assumptions, effort corrections and "
     "taxonomic identifications against the protocol and recording each issue found."),
    ("seed:rc1-m7-compliance-guidance-review", "emst:core/CMP-BR5Q9TJ", "core", None,
     "Review draft compliance guidance or help-line answers against the governing requirements before release, "
     "correcting any misstatement and recording the change for consistency."),
    ("seed:rc1-m7-carbon-estimate-verify", "emst:core/CMP-H55Y4NM", "core", None,
     "Verify a carbon stock or flux estimate before it is reported, checking the baseline, boundary, measurement error "
     "and model choice and recording each correction."),
    ("seed:rc1-m7-agreement-report-verify", "emst:wildlife/CMP-6S8JA64", "wildlife", ["L02", "L03"],
     "Verify a national implementation report under a conservation agreement against monitoring and management records "
     "before submission, recording each figure corrected."),
]


def record(key, comp, module, subsectors, text):
    rec = {"id": key, "type": "Task", "prefLabel": {"en": text}, "layer": "L2", "module": module, "status": "draft",
           "lifecycleState": "established", "useTier": "describe", "validationStatus": "draft", "license": "CC0-1.0",
           "sensitivity": "public", "statement": {"en": text}, "textSha256": L.text_sha256(text),
           "supports": [{"competency": comp, "strength": "primary"}], "workFunction": "WF-MONITOR",
           "fieldDependency": "remote-capable", "formationDependency": "partial", "homeModule": module}
    if subsectors:
        rec["subsectors"] = subsectors
    rec["editorialNote"] = {"en": "Added in the rc.1 fix pass (data-method review m7; ADR-0032): the review or verification "
                                  "step that the competency's production tasks lacked. Agent draft; needs owner review."}
    rec["provenance"] = {"method": "llm-assisted", "agent": [R.AGENT], "generatedAt": f"{R.TODAY}T12:00:00Z",
                         "toolVersion": "claude-opus-5-5", "promptVersion": PROMPT, "evidenceLabel": "S",
                         "reviewStatus": "unreviewed", "adr": ["ADR-0003", "ADR-0032"]}
    return rec


def main():
    n = 0
    for key, comp, module, subs, text in TASKS:
        words = L.word_count(text)
        if not 8 <= words <= 30:
            raise SystemExit(f"{key}: {words} words")
        base = L.DATA_V2 / ("core" if module == "core" else f"modules/{module}") / "tasks"
        path = base / f"{L.id_to_stem(key)}.yaml"
        if path.exists():
            continue
        path.write_text(L.dump_yaml(record(key, comp, module, subs, text)), encoding="utf-8")
        R.LOG.append(str(path.relative_to(L.ROOT)))
        n += 1
    print(f"review tasks written: {n} (of {len(TASKS)})")
    R.summary("add_review_tasks")


if __name__ == "__main__":
    main()
