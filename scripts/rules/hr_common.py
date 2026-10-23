"""Shared helpers for the WP-08/WP-12 HR views (RULINGS_FOR_DE §19; ADR-0030; CR-FH-001, CR-CP-001).

Ported from pipelines/views/viewlib.py. Every function reads RELEASED records only (the dict the release gate
produced); nothing here reads data/v2/ or docs/build/. Display constraints of display-gate@1.1.0 are applied here:
  * timeShare and importance only when the role is job-analysis-confirmed (or criterion-supported);
  * critical and neededAtEntry only when the role is >= reviewed with a pid: reviewer;
  * job-family weights are 1 unless importance is job-analysis-confirmed;
  * role-change summaries count tasks, never time.
"""
from __future__ import annotations

from collections import defaultdict

DISCLAIMER = "Not a classification basis / not a job analysis / not for RIF or rating decisions."
LEVEL_KEYS = ["entry", "journey", "senior", "lead", "strategic"]
VALIDATION_ORDER = ["seed-v1", "draft", "reviewed", "panel-retained", "job-analysis-confirmed", "criterion-supported"]
PCT_PENDING = "% time: set by the supervisor; EMST supplies none before job analysis"
PENDING = "assessment pending"
LIVE_LIFECYCLE = {"established", "declining"}


def held(rec) -> bool:
    return bool(isinstance(rec, dict) and (rec.get("indigenousDataFlag") or rec.get("approvalStatus") == "pending-tribal-review"
                                           or rec.get("tribalPrograms") is True or rec.get("careFlag") is True
                                           or rec.get("sectorActor") == "tribal"))


def at_least(status, floor) -> bool:
    return status in VALIDATION_ORDER and VALIDATION_ORDER.index(status) >= VALIDATION_ORDER.index(floor)


def ja_confirmed(rec) -> bool:
    return at_least((rec or {}).get("validationStatus"), "job-analysis-confirmed")


def human_reviewed(rec) -> bool:
    prov = (rec or {}).get("provenance") or {}
    reviewers = list(prov.get("reviewers") or []) + ([rec.get("reviewer")] if (rec or {}).get("reviewer") else [])
    return at_least((rec or {}).get("validationStatus"), "reviewed") and any(str(r).startswith("pid:") for r in reviewers)


def label(released, rid) -> str:
    r = released.get(rid) or {}
    return (r.get("prefLabel") or {}).get("en", rid)


def statement(released, rid) -> str:
    return ((released.get(rid) or {}).get("statement") or {}).get("en", "")


def tier(role) -> str:
    for n in role.get("notation") or []:
        if isinstance(n, dict) and n.get("scheme") == "MVPtier":
            return str(n.get("value"))
    return "?"


def role_key(role_id: str) -> str:
    return role_id.split(":", 1)[1] if ":" in role_id else role_id


def roles(released):
    return [r for _, r in sorted(released.items()) if r.get("type") == "RoleProfile" and not held(r)]


def variants_of(released):
    out = defaultdict(list)
    for _, v in sorted(released.items()):
        if v.get("type") == "RoleVariant" and not held(v):
            out[v.get("variantOf")].append(v)
    return out


def parse_other(s):
    out = {}
    for part in (s or "").split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def effective_bundle(role, variant):
    drops = set((variant or {}).get("taskDrops") or [])
    items = [dict(i) for i in role.get("taskBundle") or [] if isinstance(i, dict) and i.get("task") not in drops]
    overrides = {o["task"]: o for o in (variant or {}).get("taskOverrides") or [] if isinstance(o, dict) and o.get("task")}
    items = [dict(i, **overrides.get(i["task"], {})) for i in items]
    for a in (variant or {}).get("taskAdds") or []:
        if isinstance(a, dict):
            items.append(dict(a, added=True))
    return items


def at_levels(items, levels):
    return [dict(i) for i in items if set(i.get("roleLevels") or LEVEL_KEYS) & set(levels)]


def gated_task(released, role, item):
    """One bundle task as a view may show it under display-gate@1.1.0."""
    ja, rv = ja_confirmed(role), human_reviewed(role)
    out = {"task": item["task"], "statement": statement(released, item["task"]), "variantAdded": bool(item.get("added"))}
    out["timeShare"] = item.get("timeShare") if ja else None
    out["importance"] = item.get("importance") if ja else None
    out["critical"] = item.get("critical", False) if rv else PENDING
    out["neededAtEntry"] = item.get("neededAtEntry", False) if rv else PENDING
    if not ja:
        out["pctTimeNote"] = PCT_PENDING
    return out


def in_main_section(released, rec_id, home):
    """Module rule (CR-CP-001 B5): home-module (or core) established content renders in the main section."""
    r = released.get(rec_id) or {}
    return (r.get("module") in ("core", home) or r.get("homeModule") in (home,)) and r.get("lifecycleState", "established") in LIVE_LIFECYCLE


def targets_at(released, role, levels):
    ja, rv = ja_confirmed(role), human_reviewed(role)
    out = []
    for t in role.get("competencyTargets") or []:
        if not isinstance(t, dict) or t.get("competency") not in released:
            continue
        tl = {k: v for k, v in (t.get("targetLevels") or {}).items() if k in levels}
        if not tl:
            continue
        c = released[t["competency"]]
        out.append({"competency": t["competency"], "label": label(released, t["competency"]), "targetLevels": tl,
                    "targetLevelLabel": "editorial draft", "importance": t.get("importance") if ja else None,
                    "distinguishing": t.get("distinguishing", False) if rv else PENDING,
                    "competencyType": c.get("competencyType"), "module": c.get("module")})
    return sorted(out, key=lambda x: x["competency"])


def credential_gates(released, variant):
    """Credential gates only where the Credential is issuerVerified with sources (SPEC §10.5 rule 8)."""
    out = []
    for g in (variant or {}).get("credentialGates") or []:
        c = released.get(g.get("credential")) if isinstance(g, dict) else None
        if c and c.get("issuerVerified") and (c.get("sources") or (c.get("provenance") or {}).get("sources")):
            out.append({"credential": g["credential"], "label": label(released, g["credential"]), "kind": g.get("kind")})
    return out


def instrument_status(events_by_instrument, iid, as_of):
    evs = sorted((e for e in events_by_instrument.get(iid, []) if str(e.get("eventDate", "")) <= as_of),
                 key=lambda e: (str(e.get("eventDate")), str(e.get("id"))))
    return evs[-1].get("statusAfter") if evs else "no-event"


def events_by_instrument(released):
    out = defaultdict(list)
    for r in released.values():
        if r.get("type") == "DriverEvent" and r.get("instrument"):
            out[r["instrument"]].append(r)
    return out
