"""Small helpers so WP-05 content files stay readable. Licence: Apache-2.0."""

# instrument registry ids (data/v2/instruments/instruments.jsonl, WP-10) used by WP-05 enactments
INS = {k: f"seed:ins/{k}" for k in [
    "nepa-fra-2023", "ceq-nepa-regs-removal", "ceq-nepa-guidance-2025", "doi-nepa-procedures", "usda-nepa-procedures",
    "dot-nepa-procedures", "epa-nepa-procedures", "nepa-s112-fee", "seven-county", "speed-act", "fast-41",
    "usfs-objection-rule", "ceq-permitting-data-standard", "permitting-tech-action-plan", "permitting-tech-pm-2025",
    "epermit-act", "esa-harm-rescission", "esa-4d-4b2-rules", "esa-s4-s7-regs-2025", "nhpa-s106-regs",
    "wotus-definition", "florida-404-assumption", "ghg-endangerment-rescission", "ghgrp-reconsideration",
    "ceqa-2025-reforms", "co-hb26-1205", "good-neighbor-authority", "long-term-gna-act", "fix-our-forests-act",
    "fy2026-interior-approps", "obbba-ira-rescissions", "ca-sb-253", "ca-sb-261", "sec-climate-disclosure",
    "eu-omnibus-i", "omb-m-25-21", "omb-m-25-22", "co-sb-26-189", "roadless-rule-rescission",
    "opm-merit-hiring-plan", "schedule-policy-career", "opm-series-realignment-proposal"]}


def T(id, text, wf, field="remote-capable", formation="partial", **kw):
    d = {"id": id, "text": text, "wf": wf, "field": field, "formation": formation}
    d.update(kw)
    return d


def I(text, methods, attr=None, obs4=3, mode="unaided", tasks=None, **kw):
    d = {"text": text, "methods": methods, "attr": attr, "obs4": obs4, "mode": mode, "tasks": tasks or []}
    d.update(kw)
    return d


def E(id, label, actor, basis, principal, venue, note, position=None, instruments=None, **kw):
    d = {"id": id, "label": label, "actor": actor, "basis": basis, "principal": principal, "venue": venue,
         "note": note, "position": position, "instruments": [INS[i] for i in (instruments or [])]}
    d.update(kw)
    return d


def ins(*keys):
    return [INS[k] for k in keys]
