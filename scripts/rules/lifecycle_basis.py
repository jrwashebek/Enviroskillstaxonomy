"""Lifecycle entry tests (vocab/lifecycle_states.yaml#<state>.entry_test; ADR-0032, CR-CA-001; data-method review M7).

Lifecycle describes the WORK in the sector, validationStatus describes the record. A record in L1-L4 may be `proposed`
or `emerging` only when its `lifecycleBasis` meets the state's entry test; otherwise it is `watch`. This module applies
the test to the evidence a record names, so the D-DATA fix script that writes `lifecycleBasis` and
scripts/validate_v2.py (E-LIFECYCLE-BASIS) compute the same counts.

  proposed  >= 3 independent signals of >= 2 signal families from >= 2 sector actors, or a mandate (an Instrument with
            an `effective` DriverEvent on or before the test date). Independence is change-indicator@1.1.0 ER-1
            (disjoint providers, upstreamSource and processingChain; one observationId counts once).
  emerging  >= 10 postings or PDs (postings-pds signals: measure.n over distinct observations) across >= 2 sector
            actors, or a named operating programme with an E source; roles also need >= 1 feeder role.
The 12-month posting window of `emerging` is not applied: no posting-family evidence exists in rc.1 (CHANGE_SIGNALS.md
§11), so the count is 0 either way; the window is checked when the first posting baseline lands.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import emstlib as L  # noqa: E402
from rules import change_indicator as CI  # noqa: E402

TESTED_STATES = ("proposed", "emerging")
L1_L4_TYPES = {"Competency", "Indicator", "Enactment", "Task", "KnowledgeStatement", "RoleProfile", "RoleVariant",
               "JobFamily", "Pathway"}
TEST_REF = "vocab/lifecycle_states.yaml#{state}.entry_test"


def entry_tests(root: Path = L.ROOT) -> dict:
    d = L.load_yaml(root / "vocab" / "lifecycle_states.yaml")
    return {s["notation"]: s.get("entry_test") for s in d["lifecycle_states"] if s.get("entry_test")}


def evidence_ids(rec: dict, records: dict) -> list:
    """The evidence a record names: its own evidenceSignals, else its role's (a variant shares its role's work)."""
    ids = list(rec.get("evidenceSignals") or [])
    if not ids and rec.get("type") == "RoleVariant":
        role = records.get(rec.get("variantOf")) or {}
        ids = list(role.get("evidenceSignals") or [])
    return ids


def counts(evidence: list, records: dict, feeder_roles: int | None = None, cfg=None) -> dict:
    cfg = cfg or CI.default_config()
    sigs = [records[i] for i in evidence if isinstance(records.get(i), dict) and records[i].get("type") == "ChangeSignal"]
    obs = {s.get("observationId") or s.get("id") for s in sigs}
    posts, seen = 0, set()
    actors_posts = set()
    for s in sorted(sigs, key=lambda x: str(x.get("id"))):
        if s.get("signalFamily") != "postings-pds":
            continue
        o = s.get("observationId") or s.get("id")
        n = (s.get("measure") or {}).get("n")
        if o not in seen and isinstance(n, int):
            posts += n
            seen.add(o)
        if s.get("sectorActor"):
            actors_posts.add(s["sectorActor"])
    out = {"signals": len(sigs), "distinctObservations": len(obs),
           "independentSignals": len(CI.max_independent(sigs, cfg)),
           "signalFamilies": len({s.get("signalFamily") for s in sigs if s.get("signalFamily")}),
           "sectorActors": len({s.get("sectorActor") for s in sigs if s.get("sectorActor")}),
           "postingsOrPds": posts, "actorTypes": len(actors_posts)}
    if feeder_roles is not None:
        out["feederRoles"] = feeder_roles
    return out


def mandate_ok(ins_id, records: dict, as_of: str) -> bool:
    if not ins_id or not isinstance(records.get(ins_id), dict) or records[ins_id].get("type") != "Instrument":
        return False
    return any(isinstance(e, dict) and e.get("type") == "DriverEvent" and e.get("instrument") == ins_id
               and e.get("eventType") == "effective" and str(e.get("eventDate")) <= as_of for e in records.values())


def programme_ok(prog, source_ids: set | None) -> bool:
    if not isinstance(prog, dict) or not prog.get("label") or not prog.get("sources"):
        return False
    return source_ids is None or all(s in source_ids for s in prog["sources"])


def meets(state: str, c: dict, tests: dict, *, mandate=False, programme=False, is_role=False) -> bool:
    branches = (tests.get(state) or {}).get("any_of") or []
    ok = False
    for b in branches:
        t = b.get("test")
        if t == "signals":
            ok |= (c["independentSignals"] >= b["min_independent_signals"] and c["signalFamilies"] >= b["min_signal_families"]
                   and c["sectorActors"] >= b["min_sector_actors"])
        elif t == "mandate":
            ok |= bool(mandate)
        elif t == "postings-pds":
            ok |= c["postingsOrPds"] >= b["min_postings_or_pds"] and c["actorTypes"] >= b["min_actor_types"]
        elif t == "operating-programme":
            ok |= bool(programme)
    if ok and state == "emerging" and is_role:
        ok = (c.get("feederRoles") or 0) >= 1
    return ok


def evaluate(rec: dict, records: dict, state: str, as_of: str, tests: dict | None = None, source_ids: set | None = None,
             cfg=None) -> dict:
    """The lifecycleBasis fields (testedFor, test, result, evidence, counts; mandate/programme when stated)."""
    tests = tests or entry_tests()
    basis = rec.get("lifecycleBasis") or {}
    ev = list(basis.get("evidence")) if basis.get("evidence") is not None else evidence_ids(rec, records)
    is_role = rec.get("type") == "RoleProfile"
    c = counts(ev, records, len(rec.get("feederRoles") or []) if is_role else None, cfg)
    mandate = mandate_ok(basis.get("mandate"), records, as_of)
    programme = programme_ok(basis.get("operatingProgramme"), source_ids)
    out = {"testedFor": state, "test": TEST_REF.format(state=state),
           "result": "met" if meets(state, c, tests, mandate=mandate, programme=programme, is_role=is_role) else "not-met",
           "evidence": ev, "counts": c}
    for k in ("mandate", "operatingProgramme"):
        if basis.get(k):
            out[k] = basis[k]
    return out
