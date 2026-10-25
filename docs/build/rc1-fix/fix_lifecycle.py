#!/usr/bin/env python3
"""rc.1 fix pass, M7 lifecycle (D-DATA; ADR-0032; CR-CA-001; DATA_FIX_BRIEF §4). Idempotent.

Lifecycle describes the WORK in the sector; validationStatus describes the record. Every L1-L4 record that is
`proposed` or `emerging` gets the vocabulary's entry test applied to the evidence it names (scripts/rules/
lifecycle_basis.py, the same code the validator runs) and a stored `lifecycleBasis`:
  * test met            -> state kept;
  * emerging not met but proposed met -> proposed;
  * otherwise           -> watch, reviewBy no later than 12 months from today (vocab watch.review_by_months).
The brief names roles and competencies; the same test is applied to their variants, tasks, indicators, enactments
and pathways, because the entry test belongs to the state, not to the record type, and a watch competency with
"emerging" indicators would repeat the claim the review found unsupported (scope note in ADR-0032).
Writes generated/lifecycle_changes.csv (every record whose state changed). Run: python3 -I docs/build/rc1-fix/fix_lifecycle.py
Licence: Apache-2.0.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rc1lib as R  # noqa: E402

L = R.L
sys.path.insert(0, str(L.ROOT / "scripts"))
from rules import lifecycle_basis as LB  # noqa: E402

REVIEW_BY_WATCH = "2027-10-25"           # today + 12 months (vocab/lifecycle_states.yaml#watch.review_by_months)
RELEASE = "2.0.0-rc.1"


def label(rec):
    return ((rec.get("prefLabel") or {}).get("en") or "")[:90]


def main():
    recs = {r["id"]: r for _, r in R.records() if isinstance(r.get("id"), str)}
    tests = LB.entry_tests()
    changes = []
    for loc, rec in R.records(LB.L1_L4_TYPES):
        if loc.path.suffix != ".yaml":
            continue
        state = rec.get("lifecycleState")
        if state not in LB.TESTED_STATES and not rec.get("lifecycleBasis"):
            continue
        if rec.get("validationStatus") == "seed-v1" or rec.get("status") in ("superseded", "withdrawn"):
            continue
        tested = (rec.get("lifecycleBasis") or {}).get("testedFor") or state
        b = LB.evaluate(rec, recs, tested, R.TODAY, tests)
        new_state, note_extra = state, ""
        if b["result"] == "met":
            new_state = tested
        elif tested == "emerging":
            bp = LB.evaluate(rec, recs, "proposed", R.TODAY, tests)
            if bp["result"] == "met":
                new_state, b = "proposed", bp
            else:
                new_state = "watch"
                c = bp["counts"]
                note_extra = (f"The proposed entry test is not met either ({c['independentSignals']} independent signal(s), "
                              f"{c['signalFamilies']} signal family(ies), {c['sectorActors']} sector actor(s)).")
        else:
            new_state = "watch"
        basis = {**b, "assessedOn": R.TODAY, "assessedBy": R.AGENT}
        c = b["counts"]
        why = (f"Entry test of `{tested}` applied to {c['signals']} evidence signal(s) ({c['distinctObservations']} distinct "
               f"observation(s); {c['independentSignals']} independent; {c['signalFamilies']} family(ies); "
               f"{c['sectorActors']} sector actor(s); {c['postingsOrPds']} postings or PDs): {b['result']}.")
        basis["note"] = {"en": (why + (" " + note_extra if note_extra else "")).strip()}
        old_basis = rec.get("lifecycleBasis")
        if old_basis and {k: v for k, v in old_basis.items() if k not in ("assessedOn", "assessedBy")} == \
                {k: v for k, v in basis.items() if k not in ("assessedOn", "assessedBy")} and new_state == state:
            continue                                    # idempotent: same test, same result, same state

        def fix(r, new_state=new_state, basis=basis, state=state):
            r = R.insert_after(r, "lifecycleState", "lifecycleBasis", basis)
            if new_state != state:
                r["lifecycleState"] = new_state
                if new_state == "watch" and (not r.get("reviewBy") or str(r["reviewBy"]) > REVIEW_BY_WATCH):
                    r["reviewBy"] = REVIEW_BY_WATCH
                notes = list(r.get("changeNote") or [])
                entry = {"release": RELEASE, "note": {"en": f"lifecycleState {state} -> {new_state}: the vocabulary's entry "
                                                            f"test is not met (lifecycleBasis; ADR-0032, CR-CA-001; review M7)."}}
                if entry not in notes:
                    notes.append(entry)
                r["changeNote"] = notes
            return r
        if R.edit_yaml(loc.path, fix) and new_state != state:
            changes.append({"id": rec["id"], "type": rec["type"], "status": rec.get("status"), "label": label(rec),
                            "before": state, "after": new_state, "signals": c["signals"],
                            "independent_signals": c["independentSignals"], "families": c["signalFamilies"],
                            "sector_actors": c["sectorActors"], "postings_or_pds": c["postingsOrPds"]})
    if changes:
        cols = list(changes[0])
        p = Path(__file__).resolve().parent / "generated" / "lifecycle_changes.csv"
        old = L.read_csv(p) if p.exists() else []
        merged = {r["id"]: r for r in old}
        merged.update({r["id"]: {k: str(v) for k, v in r.items()} for r in changes})
        R.write_report("lifecycle_changes.csv", L.csv_text(cols, sorted(merged.values(), key=lambda r: (r["type"], r["id"]))))
    from collections import Counter
    print("lifecycle changes:", dict(Counter((c["type"], c["before"], c["after"]) for c in changes)))
    R.summary("fix_lifecycle")


if __name__ == "__main__":
    main()
