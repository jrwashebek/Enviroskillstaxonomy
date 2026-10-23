"""mirror-links@0.1.0 (vocab/rules/mirror-links@0.1.0.yaml; RULINGS_FOR_DE §19.1).

Port of pipelines/views/mirror_links.py (WP-08). Variant-level pairs come only from the released X11 emst:mirrorRole
rows; competency-level pairs from Competency.mirrors[] (stored on the authority side; the inverse is not listed twice).
Rows or records involving held variants or Tribal actors are never read.
"""
from __future__ import annotations

from rules import hr_common as H

X11_PREFIX = "emst-public-private/"


def compute(released, mappings, stamp):
    pairs = []
    for name, rows in sorted(mappings.items()):
        if not name.startswith(X11_PREFIX):
            continue
        for r in rows:
            if r.get("predicate_id") != "emst:mirrorRole":
                continue
            a, b = released.get(r.get("subject_id")), released.get(r.get("object_id"))
            if a is None or H.held(a) or (b is not None and H.held(b)):
                continue
            other = H.parse_other(r.get("other"))
            pairs.append({"level": "variant", "subject": r["subject_id"], "object": r.get("object_id"),
                          "relation": "mirrorRole", "subjectPosition": a.get("authorityPosition"),
                          "objectPosition": (b or {}).get("authorityPosition") if b else "external",
                          "positionsInverted": bool(b and a.get("authorityPosition") != b.get("authorityPosition")),
                          "confidence": r.get("confidence"), "reviewStatus": other.get("review_status", "candidate")})
    for cid, c in sorted(released.items()):
        if c.get("type") != "Competency" or H.held(c):
            continue
        for m in c.get("mirrors") or []:
            t = released.get(m.get("target")) if isinstance(m, dict) else None
            if t is None or H.held(t):
                continue
            pairs.append({"level": "competency", "subject": cid, "object": m["target"], "relation": m.get("relation"),
                          "subjectPosition": None, "objectPosition": None, "positionsInverted": True,
                          "confidence": None, "reviewStatus": c.get("validationStatus")})
    pairs.sort(key=lambda p: (p["level"], p["subject"], str(p["object"])))
    return {"pairs": pairs, **stamp}
