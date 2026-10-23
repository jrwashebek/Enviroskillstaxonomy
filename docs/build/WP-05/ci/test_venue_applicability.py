"""Tests for the WP-05 venue-applicability prototype (ADR-0016 section 3-4) on synthetic fixtures.

Run: python3 -m pytest -q docs/build/WP-05/ci/test_venue_applicability.py
The fixtures (docs/build/WP-05/ci/fixtures/) are synthetic and validate with
`python3 scripts/validate_v2.py --data-root docs/build/WP-05/ci/fixtures --no-git-base`.
CR-SC-001 asks DE to move this test into tests/ when the rule is ported to scripts/build_release.py.
"""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import venue_applicability as V  # noqa: E402

FX = HERE / "fixtures"


def table(as_of, root=FX):
    return {(r["competency"], r["sectorActor"]): r for r in V.compute(root, as_of)}


def test_federal_basis_rescinded_gives_no_current_basis_state_keeps_required():
    t = table("2026-10-23")
    assert t[("seed:fx-wp05-burden", "federal")]["venueApplicability"] == "no-current-basis"
    assert t[("seed:fx-wp05-burden", "state")]["venueApplicability"] == "required-basis"


def test_actor_without_linked_instrument_is_permitted_and_flagged():
    r = table("2026-10-23")[("seed:fx-wp05-burden", "ngo")]
    assert r["venueApplicability"] == "permitted"
    assert r["basisLinked"] is False


def test_value_changes_with_as_of_date_not_with_a_stored_flag():
    # before the 2025 rescission the federal order was in effect
    assert table("2024-12-31")[("seed:fx-wp05-burden", "federal")]["venueApplicability"] == "required-basis"


def test_litigated_in_force_counts_as_basis_and_proposed_does_not():
    t = table("2026-10-23")
    assert t[("seed:fx-wp05-litigated", "federal")]["venueApplicability"] == "required-basis"
    assert t[("seed:fx-wp05-litigated", "local")]["venueApplicability"] == "permitted"


def test_reinstatement_flips_back_in_either_direction(tmp_path):
    root = tmp_path / "fx"
    shutil.copytree(FX, root)
    ev = root / "events" / "2026.jsonl"
    src = (FX / "events" / "2025.jsonl").read_text(encoding="utf-8").splitlines()[0]
    line = (src.replace("1994-02-11", "2026-09-01").replace('"decided"', '"enacted"')
            .replace("/decided/", "/enacted/"))
    ev.write_text(line + "\n", encoding="utf-8")
    assert table("2026-10-23", root)[("seed:fx-wp05-burden", "federal")]["venueApplicability"] == "required-basis"


def test_federal_view_carries_as_of_and_note_and_never_excludes():
    view = V.federal_view(V.compute(FX, "2026-10-23"))
    v = view["seed:fx-wp05-burden"]
    assert v["federalApplicability"] == "no-current-basis" and v["asOf"] == "2026-10-23"
    assert "no exclusion" in v["note"]
