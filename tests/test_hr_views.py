"""HR and mobility views ported into the release (RULINGS_FOR_DE §19; ADR-0030; CR-FH-001, CR-CP-001).

Moved from pipelines/views/tests/test_views.py: the WP-08 record checks and acceptance pairs are now tests of the
ported views, which read released records only (after the release gate) from a snapshot of data/v2.
"""
from __future__ import annotations

import json
import re
import shutil

import pytest

from conftest import L

import build_release
from rules import (federal_series_profile, hr_common as H, job_family_membership, mirror_links, pathway_edges,
                   role_change, state_class_view)

REALIGNED = re.compile(r"\b(has been realigned|was realigned|consolidated into|is now \d{4})\b", re.I)
PII = re.compile(r"[\w.+-]+@[A-Za-z][\w-]*\.[A-Za-z]{2,}\b|\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b")
STAMP = {"ruleId": "x", "ruleVersion": "0.1.0", "buildCommit": "test"}


@pytest.fixture(scope="module")
def released(tmp_path_factory):
    snap = tmp_path_factory.mktemp("snap") / "v2"
    shutil.copytree(L.DATA_V2, snap)                # content builders write data/v2 concurrently
    b = build_release.Builder(snap, profile="preview", version="2.0.0-dev", build_commit="test")
    rel = {rid: b.clean(r) for rid, r in sorted(b.records.items()) if b.include(rid, r)}
    b.records_snapshot = b.records
    return b, rel, b._mapping_rows(rel)


def _roles(rel):
    return H.roles(rel)


def test_role_records_and_tiers(released):
    _, rel, _ = released
    roles = _roles(rel)
    if not roles:
        pytest.skip("no role records yet")
    assert {H.tier(r) for r in roles} <= {"P1", "P2", "P3", "P4"}
    for r in roles:                                   # agent drafts, never selection
        assert r["validationStatus"] in ("draft", "seed-v1") and all(c.get("criticalForSelection") is not True for c in r.get("competencyTargets") or [])


def test_held_and_tribal_variants_never_released(released):
    b, rel, _ = released
    for rid, r in b.records.items():
        if r.get("type") == "RoleVariant" and r.get("sectorActor") == "tribal":
            assert rid not in rel


def _views(released):
    b, rel, maps = released
    out = {}
    out.update(federal_series_profile.compute(rel, maps, STAMP, "2026-10-23"))
    out.update(state_class_view.compute(rel, STAMP))
    out["views/job_families.json"] = job_family_membership.compute(rel, b.rules["job-family-membership"], STAMP)
    out.update(role_change.compute(rel, {"rows": []}, "2026-10-23", STAMP))
    out["views/mirror_links.json"] = mirror_links.compute(rel, maps, STAMP)
    out["views/pathway_edges.json"] = pathway_edges.compute(rel, STAMP)
    return out


@pytest.fixture(scope="module")
def views(released):
    return _views(released)


def test_fsp_and_scv_carry_the_disclaimer_and_no_realigned_claims(views, released):
    _, rel, _ = released
    series = {r["seriesCode"]: r for r in rel.values() if r.get("type") == "SeriesRecord"}
    for name, doc in views.items():
        if name.startswith(("views/federal_series_profiles/", "views/state_class_views/")):
            assert H.DISCLAIMER in doc["disclaimers"], name
        if name.startswith("views/federal_series_profiles/") and not name.endswith("index.json"):
            rec = series.get(doc["seriesCode"]) or {}
            if not str(rec.get("seriesStatus", "")).startswith("realigned-to:"):
                assert not REALIGNED.search(json.dumps(doc)), name


def test_display_constraints_before_job_analysis(views, released):
    _, rel, _ = released
    for name, doc in views.items():
        if not name.startswith(("views/federal_series_profiles/", "views/state_class_views/")) or name.endswith("index.json"):
            continue
        blocks = doc.get("roles") or [doc]
        for blk in blocks:
            role = rel.get(blk.get("role")) or {}
            for t in (blk.get("duties") or []) + (blk.get("tasks") or []):
                if not H.ja_confirmed(role):
                    assert t["timeShare"] is None and t["importance"] is None and t["pctTimeNote"] == H.PCT_PENDING, name
                if not H.human_reviewed(role):
                    assert t["critical"] == H.PENDING and t["neededAtEntry"] == H.PENDING, name


def test_state_class_view_files_are_named_by_jurisdiction_and_class(views, released):
    _, rel, _ = released
    names = [n for n in views if n.startswith("views/state_class_views/") and not n.endswith("index.json")]
    assert names and not [n for n in names if n.split("/")[-1].startswith("unknown--")]
    docs = [views[n] for n in names]
    assert len({d["classRecord"] for d in docs}) == len(docs)  # one file per class record: no stem collisions


def test_job_family_weights_are_one_before_job_analysis(released):
    b, rel, _ = released
    roles = [r for r in _roles(rel) if not H.ja_confirmed(r)]
    if not roles:
        pytest.skip("no role records yet")
    rule = b.rules["job-family-membership"]
    doc = job_family_membership.compute(rel, rule, STAMP)
    excl = set(rule["parameters"]["excludeTargets"])
    for fam in doc["families"]:
        anchors = set(rule["parameters"]["families"][fam["family"]]["anchors"])
        for m in fam["members"]:
            role = rel[m["role"]]
            tg = [t for t in role["competencyTargets"] if t["competency"] not in excl]
            assert m["share"] == round(sum(1 for t in tg if t["competency"] in anchors) / len(tg), 3)


def test_role_change_counts_tasks_not_time(views):
    for name, doc in views.items():
        if name.startswith("views/role_change/") and not name.endswith("summary.json"):
            assert "timeShare" not in json.dumps(doc), name
            for v in doc["variants"]:
                for lv in v["roleLevels"]:
                    assert lv["counts"]["assessed"] + lv["counts"]["pending"] == len(lv["tasks"])


@pytest.mark.parametrize("subject,obj", [
    ("R11-environmental-permit-writer", "R37-facility-environmental-compliance-specialist"),
    ("R12-environmental-compliance-inspector", "R37-facility-environmental-compliance-specialist"),
    ("R11-environmental-permit-writer", "R37-facility-environmental-compliance-specialist/private/applicant-preparer"),
])
def test_wp08_acceptance_mirror_pairs(views, released, subject, obj):
    _, rel, _ = released
    seed_of = {v: k for k, v in L.load_seed_map().items()}      # minted IDs back to their seed keys (ADR-0031 §6)
    key = lambda rid: seed_of.get(str(rid), str(rid))            # noqa: E731
    if not any(key(r["id"]).startswith(f"seed:{subject.split('/')[0]}") for r in _roles(rel)):
        pytest.skip("role records not present")
    pairs = views["views/mirror_links.json"]["pairs"]

    def match(p):
        s, o = key(p["subject"]).split(":", 1)[1], key(p["object"]).split(":", 1)[-1]
        return s.startswith(subject + "/") and (o == obj if obj.count("/") > 1 else o.startswith(obj + "/") or o == obj)
    assert any(match(p) for p in pairs if p["level"] == "variant")


def test_pathway_edges_are_never_recommended(views):
    for e in views["views/pathway_edges.json"]["edges"]:
        assert "not a recommendation" in e["label"] and all(p["recommended"] is False for p in e["pathways"] if isinstance(p, dict))
        assert e["shared"]["N"] + len(e["gap"]) == e["shared"]["M"]


def test_no_held_ids_or_personal_data_in_views(views, released):
    b, _, _ = released
    held = {rid for rid, r in b.records.items() if H.held(r) or b.is_held(rid, r)}
    text = json.dumps(views)
    assert not [h for h in held if f'"{h}"' in text]
    assert not PII.search(text)


def test_ported_views_never_read_data_v2_or_authoring_inputs():
    for name in ("federal_series_profile", "state_class_view", "job_family_membership", "role_change", "mirror_links",
                 "pathway_edges", "hr_common"):
        src = (L.ROOT / "scripts" / "rules" / f"{name}.py").read_text(encoding="utf-8")
        assert "iter_records" not in src and "DATA_V2" not in src and "change_view_inputs" not in src.split('"""', 2)[-1], name
