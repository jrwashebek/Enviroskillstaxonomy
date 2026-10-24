#!/usr/bin/env python3
"""Mirror-role links (ADR-0017 section 4): pairs of role variants that share tasks with inverted authority position,
read from X11 (emst:mirrorRole rows) and checked against the variants' editorial authority positions. Also asserts
the WP-08 acceptance pairs: R11 <-> R37, R12 <-> R37 and R11 <-> the applicant-side preparer variant.
Output: docs/build/WP-08/generated/mirror_links.json. Licence: Apache-2.0."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import viewlib as V  # noqa: E402

GEN = "pipelines/views/mirror_links.py@0.1.0"
X11 = V.L.DATA_V2 / "crosswalks" / "emst-public-private" / "0.1.0.sssom.tsv"
REQUIRED = [("R11-environmental-permit-writer", "R37-facility-environmental-compliance-specialist"),
            ("R12-environmental-compliance-inspector", "R37-facility-environmental-compliance-specialist"),
            ("R11-environmental-permit-writer", "R37-facility-environmental-compliance-specialist/private/applicant-preparer")]


def main():
    d = V.Data()
    pairs = []
    for r in V.read_set(X11):
        if r["predicate_id"] != "emst:mirrorRole":
            continue
        a, b = d.get(r["subject_id"]), d.get(r["object_id"])
        pairs.append({"subject": r["subject_id"], "object": r["object_id"], "record": r["record_id"],
                      "subjectPosition": (a or {}).get("authorityPosition"),
                      "objectPosition": (b or {}).get("authorityPosition") if b else "external (PS reference job architecture)",
                      "confidence": float(r["confidence"] or 0), "friction": V.parse_other(r["other"]).get("friction_posture_change"),
                      "positionsInverted": bool(a and b and a.get("authorityPosition") != b.get("authorityPosition"))})
    checks = []
    for x, y in REQUIRED:
        sk = lambda rid: d.seed_of(rid).split(":", 1)[1] if d.seed_of(rid).startswith("seed:") else rid  # noqa: E731
        ok = any(sk(p["subject"]).startswith(x + "/") and
                 (sk(p["object"]) == y if "/" in y else sk(p["object"]).startswith(y + "/"))
                 for p in pairs)
        checks.append({"from": x, "to": y, "linked": ok})
    out = {"stamp": V.stamp("mirror-links", "0.1.0", GEN), "pairs": pairs, "acceptanceChecks": checks,
           "note": "Mirror pairs are agent-drafted X11 rows (review_status candidate); mobility friction fields are in X11 `other`."}
    V.write_json(V.OUT / "mirror_links.json", out)
    print(checks)
    if not all(c["linked"] for c in checks):
        raise SystemExit("required mirror link missing")


if __name__ == "__main__":
    main()
