"""assessment-staleness@1.0.0 (vocab/rules/assessment-staleness@1.0.0.yaml; ADR-0029 §4.4).

  task ratings        stale = task.textSha256 set and ≠ rating.taskTextSha256
  competency ratings  (v1-analyst) stale = competency_text_sha256(prefLabel.en, statement.en) ≠ competencyTextSha256
                      (subjectTextSha256 on RelevanceRating)
  role-target ratings occupation-grain external-index records are never stale by text (they lapse by index release)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import emstlib as L  # noqa: E402


def _competency_hash(c: dict) -> str:
    return L.competency_text_sha256((c.get("prefLabel") or {}).get("en", ""), (c.get("statement") or {}).get("en", ""))


def compute(released: dict, stamp: dict) -> list[dict]:
    rows = []
    for rid, r in sorted(released.items()):
        if r.get("type") not in L.RATING_TYPES:
            continue
        if r.get("task") in released:
            cur = released[r["task"]].get("textSha256")
            rows.append({"assessment": rid, "task": r["task"], "stale": bool(cur and cur != r.get("taskTextSha256")), **stamp})
            continue
        for field, hfield in (("competency", "competencyTextSha256"), ("subject", "subjectTextSha256")):
            target = released.get(r.get(field))
            if target is not None and target.get("type") == "Competency" and r.get(hfield):
                rows.append({"assessment": rid, field: r[field], "stale": _competency_hash(target) != r[hfield], **stamp})
                break
        else:
            if r.get("type") == "ExposureAssessment" and r.get("targetId") and not r.get("task"):
                rows.append({"assessment": rid, "target": r["targetId"], "stale": False, "basis": "index-release", **stamp})
    return rows


def stale_ids(released: dict) -> set[str]:
    """IDs of the released ratings that are stale under this rule (ADR-0032; review M8).

    For the bundle: D-BUILD sets the computed flag `stale: true` on these rating nodes (REQUESTS_FOR_BUILD R-03), so a
    v1 or v2 assessment whose rated text no longer matches its subject is marked where it is read, not only in
    views/assessment_staleness.json. Staleness stays computed: it is never stored in a source record (SPEC §14).
    """
    return {row["assessment"] for row in compute(released, {}) if row.get("stale")}
