"""venue-applicability@1.0.0 (vocab/rules/venue-applicability@1.0.0.yaml; ADR-0016 §3-4, ADR-0030; CR-SC-001 #2, #4).

For each released competency C and each non-Tribal sector-actor family F with at least one released actor Enactment
of C, L = the typed links Enactment.characteristicInstruments[] {instrument, role} of those enactments, and
R = the links with role `requires`:
  required-basis    any r in R is active as of asOf
  no-current-basis  R is non-empty and every r in R is inactive
  permitted         otherwise (no requires link, or requires links whose status is pending or no-event)
Links with role enables, constrains or removed-requirement never decide the value; they are listed in context[].
A link without a role counts as nothing and is reported in untypedLinks. Tribal and held enactments are never read.
An instrument's status as of asOf is DriverEvent.statusAfter of its latest released event with eventDate <= asOf;
a submitted-for-review event never yields an active status.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import emstlib as L  # noqa: E402

RULE_ID = "venue-applicability"
RULE_VERSION = "1.0.0"
NOTE_FEDERAL = "Computed from typed requires links and dated instrument status; shown with no exclusion (Q4 default)."


def _rule(root: Path = L.ROOT) -> dict:
    return L.load_yaml(root / "vocab" / "rules" / f"{RULE_ID}@{RULE_VERSION}.yaml")


def family_map(root: Path = L.ROOT) -> dict[str, str]:
    """Sector-actor notation (family or subtype) -> family (vocab/sector_actors.yaml top-level notation)."""
    d = L.load_yaml(root / "vocab" / "sector_actors.yaml")
    out = {}
    for t in d["terms"]:
        out[t["notation"]] = t["notation"]
        for s in t.get("subtypes", []) or []:
            out[s["notation"]] = t["notation"]
    return out


def instrument_status(events: list[dict], as_of: str, active: set) -> tuple[str, bool]:
    """(status as of asOf, has a dated event on or before asOf)."""
    dated = sorted((e for e in events if str(e.get("eventDate", "")) and str(e["eventDate"]) <= as_of),
                   key=lambda e: (str(e["eventDate"]), str(e.get("id"))))
    if not dated:
        return "no-event", False
    last = dated[-1]
    status = last.get("statusAfter") or "no-event"
    if last.get("eventType") == "submitted-for-review" and status in active:
        status = "under-review"            # a submitted-for-review event never yields an active status
    return status, True


def _links(enactment: dict) -> list[dict]:
    out = []
    for item in enactment.get("characteristicInstruments") or []:
        if isinstance(item, str):
            out.append({"instrument": item})       # pre-ADR-0030 untyped string: counts as nothing
        elif isinstance(item, dict) and item.get("instrument"):
            out.append(item)
    return out


def held(rec: dict) -> bool:
    return rec.get("indigenousDataFlag") is True or rec.get("approvalStatus") == "pending-tribal-review"


def compute(released: dict, as_of: str, stamp: dict | None = None, root: Path = L.ROOT) -> dict:
    """Returns the view document {header, rows, federal}."""
    rule = _rule(root)
    d = rule["definition"]
    active, inactive = set(d["active_statuses"]), set(d["inactive_statuses"])
    fam_of = family_map(root)
    stamp = stamp or {"ruleId": RULE_ID, "ruleVersion": RULE_VERSION}
    events = defaultdict(list)
    for r in released.values():
        if r.get("type") == "DriverEvent" and r.get("instrument"):
            events[r["instrument"]].append(r)
    by_comp: dict = defaultdict(lambda: defaultdict(list))
    for rid, e in released.items():
        if e.get("type") != "Enactment" or e.get("enactmentKind") != "actor" or held(e):
            continue
        fam = fam_of.get(str(e.get("actorType")))
        if fam is None or fam == "tribal":
            continue                                   # Tribal actors are never read (ADR-0007 §D)
        c = e.get("competency")
        if c in released and released[c].get("type") == "Competency":
            by_comp[c][fam].append(rid)
    rows = []
    status_cache: dict = {}

    def st(iid):
        if iid not in status_cache:
            status_cache[iid] = instrument_status(events.get(iid, []), as_of, active)
        return status_cache[iid]

    for cid in sorted(by_comp):
        for fam in sorted(by_comp[cid]):
            enas = sorted(by_comp[cid][fam])
            links = [lk for eid in enas for lk in _links(released[eid])]
            requires = sorted({lk["instrument"] for lk in links if lk.get("role") == "requires"})
            context = sorted({(lk["instrument"], lk["role"]) for lk in links if lk.get("role") and lk.get("role") != "requires"})
            untyped = sum(1 for lk in links if not lk.get("role"))
            deciding = [{"instrument": i, "status": st(i)[0]} for i in requires]
            statuses = [x["status"] for x in deciding]
            if any(s in active for s in statuses):
                value = "required-basis"
            elif statuses and all(s in inactive for s in statuses):
                value = "no-current-basis"
            else:
                value = "permitted"
            rows.append({"competency": cid, "sectorActor": fam, "venueApplicability": value, "asOf": as_of,
                         "basisLinked": bool(requires), "basisVerified": any(st(i)[1] for i in requires),
                         "untypedLinks": untyped, "deciding": deciding,
                         "context": [{"instrument": i, "role": role, "status": st(i)[0]} for i, role in context],
                         "enactments": enas, **stamp})
    federal = {}
    for r in rows:
        if r["sectorActor"] != "federal":
            continue
        note = NOTE_FEDERAL
        if not r["basisLinked"]:
            note += " Basis not yet linked."
        elif not r["basisVerified"]:
            note += " Basis linked, status not yet verified."
        federal[r["competency"]] = {"federalApplicability": r["venueApplicability"], "asOf": as_of,
                                    "basisLinked": r["basisLinked"], "basisVerified": r["basisVerified"], "note": note}
    return {"header": {**stamp, "asOf": as_of}, "rows": rows, "federal": federal}
