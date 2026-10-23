"""venue-applicability@1.0.0 (RULINGS_FOR_DE §16.4; ADR-0030). Moved from docs/build/WP-05/ci/ and extended with the
typed-role cases named in the rule file's `tests`. Fixtures: tests/fixtures/venue/ (synthetic; validate clean)."""
from __future__ import annotations

import copy
import shutil

import pytest

from conftest import FIXTURES, L

from rules import venue_applicability as V

FX = FIXTURES / "venue"
BURDEN, LITIGATED = "seed:fx-wp05-burden", "seed:fx-wp05-litigated"


def records(root=FX):
    out = {}
    for _loc, rec in L.iter_records(root):
        if isinstance(rec, dict):
            out[rec["id"]] = rec
    return out


def table(as_of, recs=None):
    doc = V.compute(recs if recs is not None else records(), as_of)
    return {(r["competency"], r["sectorActor"]): r for r in doc["rows"]}, doc


def with_links(recs, ena_id, links):
    recs = copy.deepcopy(recs)
    recs[ena_id]["characteristicInstruments"] = links
    return recs


def add_instrument(recs, iid, events):
    recs = copy.deepcopy(recs)
    base_ins = next(r for r in recs.values() if r["type"] == "Instrument")
    recs[iid] = dict(copy.deepcopy(base_ins), id=iid)
    base_ev = next(r for r in recs.values() if r["type"] == "DriverEvent")
    for n, (date, etype, status) in enumerate(events):
        eid = f"{iid}/evt-{n}"
        recs[eid] = dict(copy.deepcopy(base_ev), id=eid, instrument=iid, eventDate=date, eventType=etype, statusAfter=status)
    return recs


def test_fixtures_validate_clean():
    import validate_v2
    rep = validate_v2.Validator(FX, use_git_base=False, check_x1=False).run()
    assert [(i.code, i.where) for i in rep.errors] == []


# ---- the WP-05 prototype cases, now with typed requires links
def test_rescinded_requires_gives_no_current_basis_state_keeps_required():
    t, _ = table("2026-10-23")
    assert t[(BURDEN, "federal")]["venueApplicability"] == "no-current-basis"
    assert t[(BURDEN, "state")]["venueApplicability"] == "required-basis"


def test_actor_without_linked_instrument_is_permitted_and_flagged():
    r = table("2026-10-23")[0][(BURDEN, "ngo")]
    assert r["venueApplicability"] == "permitted" and r["basisLinked"] is False


def test_as_of_before_a_rescission_gives_required_basis():
    assert table("2024-12-31")[0][(BURDEN, "federal")]["venueApplicability"] == "required-basis"


def test_litigated_in_force_counts_and_proposed_does_not():
    t, _ = table("2026-10-23")
    assert t[(LITIGATED, "federal")]["venueApplicability"] == "required-basis"
    assert t[(LITIGATED, "local")]["venueApplicability"] == "permitted"


def test_federal_view_carries_as_of_and_note_and_never_excludes():
    _, doc = table("2026-10-23")
    v = doc["federal"][BURDEN]
    assert v["federalApplicability"] == "no-current-basis" and v["asOf"] == "2026-10-23" and "no exclusion" in v["note"]


# ---- typed-role cases (rule file `tests`)
def test_active_removed_requirement_alone_is_permitted():
    recs = add_instrument(records(), "seed:fx-ins/revoking-order", [("2025-01-20", "issued", "issued")])
    recs = with_links(recs, "seed:fx-ena-burden-ngo", [{"instrument": "seed:fx-ins/revoking-order", "role": "removed-requirement"}])
    r = table("2026-10-23", recs)[0][(BURDEN, "ngo")]
    assert r["venueApplicability"] == "permitted" and r["basisLinked"] is False
    assert r["context"] == [{"instrument": "seed:fx-ins/revoking-order", "role": "removed-requirement", "status": "issued"}]


def test_linked_revoking_order_never_flips_a_value():
    recs = add_instrument(records(), "seed:fx-ins/revoking-order", [("2025-01-20", "issued", "issued")])
    for ena in ("seed:fx-ena-burden-federal", "seed:fx-ena-burden-state"):
        links = recs[ena]["characteristicInstruments"] + [{"instrument": "seed:fx-ins/revoking-order", "role": "removed-requirement"}]
        recs = with_links(recs, ena, links)
    t, _ = table("2026-10-23", recs)
    assert t[(BURDEN, "federal")]["venueApplicability"] == "no-current-basis"
    assert t[(BURDEN, "state")]["venueApplicability"] == "required-basis"


@pytest.mark.parametrize("role", ["enables", "constrains"])
def test_enables_and_constrains_never_decide(role):
    recs = with_links(records(), "seed:fx-ena-burden-ngo", [{"instrument": "seed:fx-ins/state-statute", "role": role}])
    r = table("2026-10-23", recs)[0][(BURDEN, "ngo")]
    assert r["venueApplicability"] == "permitted" and r["deciding"] == [] and r["context"][0]["role"] == role


def test_requires_with_no_event_is_permitted_linked_not_verified():
    recs = add_instrument(records(), "seed:fx-ins/new-statute", [])
    recs = with_links(recs, "seed:fx-ena-burden-ngo", [{"instrument": "seed:fx-ins/new-statute", "role": "requires"}])
    r = table("2026-10-23", recs)[0][(BURDEN, "ngo")]
    assert (r["venueApplicability"], r["basisLinked"], r["basisVerified"]) == ("permitted", True, False)
    assert r["deciding"] == [{"instrument": "seed:fx-ins/new-statute", "status": "no-event"}]


def test_untyped_link_is_reported_and_counts_as_nothing():
    recs = with_links(records(), "seed:fx-ena-burden-ngo", [{"instrument": "seed:fx-ins/state-statute"}])
    r = table("2026-10-23", recs)[0][(BURDEN, "ngo")]
    assert r["venueApplicability"] == "permitted" and r["untypedLinks"] == 1


def test_tribal_and_held_enactments_are_never_read():
    recs = copy.deepcopy(records())
    recs["seed:fx-ena-burden-ngo"]["actorType"] = "federally-recognized-tribe"
    t, _ = table("2026-10-23", recs)
    assert not [k for k in t if k[1] == "tribal"] and (BURDEN, "ngo") not in t
    recs = copy.deepcopy(records())
    recs["seed:fx-ena-burden-state"]["indigenousDataFlag"] = True
    assert (BURDEN, "state") not in table("2026-10-23", recs)[0]


def test_submitted_for_review_never_yields_an_active_status():
    recs = add_instrument(records(), "seed:fx-ins/pending-rule", [("2026-07-10", "submitted-for-review", "in-force")])
    recs = with_links(recs, "seed:fx-ena-burden-ngo", [{"instrument": "seed:fx-ins/pending-rule", "role": "requires"}])
    r = table("2026-10-23", recs)[0][(BURDEN, "ngo")]
    assert r["venueApplicability"] == "permitted" and r["deciding"][0]["status"] == "under-review"


def test_reinstatement_flips_back_through_events_not_a_stored_flag(tmp_path):
    root = tmp_path / "fx"
    shutil.copytree(FX, root)
    recs = add_instrument(records(root), "seed:fx-ins/unused", [])
    ev = next(r for r in recs.values() if r["type"] == "DriverEvent" and r["instrument"] == "seed:fx-ins/federal-order")
    recs["seed:fx-evt/reinstated"] = dict(copy.deepcopy(ev), id="seed:fx-evt/reinstated", eventDate="2026-09-01",
                                          eventType="enacted", statusAfter="in-force")
    assert table("2026-10-23", recs)[0][(BURDEN, "federal")]["venueApplicability"] == "required-basis"


def test_computed_fields_are_never_stored():
    cf = L.load_yaml(L.LINT_DIR / "computed_fields.yaml")["fields"]
    assert {"venueApplicability", "federalApplicability"} <= set(cf)
