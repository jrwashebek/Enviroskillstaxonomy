#!/usr/bin/env python3
"""Hand WP-08's P1 task bundles to the X2 provisional frame (WP-09 open item 3).

Writes pipelines/x2/p1_frame.yaml in the format build_candidates.py reads (competencyToP1Roles), recomputed from the
P1 RoleProfiles' bundles, plus taskToP1Roles: the exact bundled tasks (the frame 'becomes exactly the bundled tasks of
the P1 roles', per the file's own header). A copy goes to docs/build/WP-08/generated/x2_p1_frame.yaml.
Licence: Apache-2.0."""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import viewlib as V  # noqa: E402

TARGET = V.ROOT / "pipelines" / "x2" / "p1_frame.yaml"
HEADER = """# P1-corridor task frame for X2 (WP-09), regenerated from WP-08's P1 task bundles by
# pipelines/views/x2_frame_from_bundles.py (do not hand-edit). Licence: CC0-1.0.
# taskToP1Roles is the exact frame: every task bundled in a P1 RoleProfile (seed:<role_key>), keyed by task, with the
# short role codes that bundle it. competencyToP1Roles is kept for build_candidates.py@current, which selects every
# live task supporting a listed competency: it is a superset of the exact frame until IA switches the builder to
# taskToP1Roles (WP-08 handoff). Role->O*NET-SOC pools still come from X3. Judgment basis: [S] WP-08 agent drafts.
"""


def main():
    d = V.Data()
    t2r, c2r = defaultdict(set), defaultdict(set)
    for r in d.roles():
        if d.tier(r) != "P1":
            continue
        code = d.role_key(r)[:3]
        for i in r["taskBundle"]:
            t2r[i["task"]].add(code)
            for s in (d.get(i["task"]) or {}).get("supports") or []:
                if s.get("strength") == "primary":
                    c2r[d.seed_of(s["competency"]).split(":", 1)[1]].add(code)     # keyed by the competency's seed key
    body = {"frameVersion": "0.2.0-wp08-bundles", "source": "data/v2/**/roles/ (P1 RoleProfiles, WP-08, 2026-10-23)",
            "competencyToP1Roles": {k: sorted(v) for k, v in sorted(c2r.items())},
            "taskToP1Roles": {k: sorted(v) for k, v in sorted(t2r.items())}}
    text = HEADER + V.L.dump_yaml(body)
    TARGET.write_text(text, encoding="utf-8")
    V.write_text(V.OUT / "x2_p1_frame.yaml", text)
    print(f"X2 frame: {len(t2r)} bundled P1 tasks; {len(c2r)} competencies")


if __name__ == "__main__":
    main()
