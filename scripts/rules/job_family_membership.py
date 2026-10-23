"""job-family-membership@0.1.0 (vocab/rules/job-family-membership@0.1.0.yaml; RULINGS_FOR_DE §19.1).

Port of pipelines/views/job_families.py (WP-08). Navigation-only membership of released RoleProfiles in released
JobFamilies, never stored. Each competency target weighs 1 unless its importance is job-analysis-confirmed
(display-gate@1.1.0); TX-A floor targets are excluded. Held records are never read.
"""
from __future__ import annotations

from rules import hr_common as H


def compute(released, rule, stamp):
    p = rule.get("parameters") or {}
    excl = set(p.get("excludeTargets") or [])
    fams = {fid: spec for fid, spec in (p.get("families") or {}).items() if fid in released and not H.held(released[fid])}
    members = {fid: [] for fid in fams}
    for role in H.roles(released):
        weight = (lambda t: t.get("importance", 1)) if H.ja_confirmed(role) else (lambda t: 1)
        tg = [t for t in role.get("competencyTargets") or [] if isinstance(t, dict) and t.get("competency") not in excl]
        tot = sum(weight(t) for t in tg) or 1
        for fid, spec in fams.items():
            anchors = set(spec.get("anchors") or [])
            share = sum(weight(t) for t in tg if t.get("competency") in anchors) / tot
            basis = None
            if share >= p.get("minShare", 0.2):
                basis = "anchor share"
            elif role.get("homeModule") in set(spec.get("modules") or []) and share >= p.get("minShareInModule", 0.1):
                basis = "home module and anchor share"
            if basis:
                members[fid].append({"role": role["id"], "basis": basis, "share": round(share, 3),
                                     "whatsComing": role.get("lifecycleState") in ("proposed", "emerging")})
    return {"families": [{"family": fid, "members": sorted(m, key=lambda x: (-x["share"], x["role"])), **stamp}
                         for fid, m in sorted(members.items())],
            "note": "Navigation only; not a classification or a career-ladder claim.", **stamp}
