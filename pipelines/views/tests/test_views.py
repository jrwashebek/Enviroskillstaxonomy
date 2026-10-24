"""Checks on WP-08 role records and generated HR views (run: python -m pytest -q pipelines/views/tests)."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import viewlib as V  # noqa: E402

D = V.Data()
OUT = V.OUT
REALIGNED = re.compile(r"\b(has been realigned|was realigned|realigned to|consolidated into|is now \d{4})\b", re.I)
PII = re.compile(r"[\w.+-]+@[A-Za-z][\w-]*\.[A-Za-z]{2,}\b|\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b")


def roles_by_tier(t):
    return [r for r in D.roles() if D.tier(r) == t]


def test_37_roles_and_tiers():
    assert len(D.roles()) == 37
    assert [len(roles_by_tier(t)) for t in ("P1", "P2", "P3", "P4")] == [13, 17, 6, 1]


def test_depth_rules():
    for t, (lo, hi, clo, chi) in {"P1": (15, 40, 6, 12), "P2": (15, 40, 6, 10)}.items():
        for r in roles_by_tier(t):
            assert lo <= len(r["taskBundle"]) <= hi, r["id"]
            ncrit = sum(1 for c in r["competencyTargets"] if (c.get("importance") or 0) >= 4)   # WP-08's own drafts only
            assert clo <= ncrit <= chi, (r["id"], ncrit)
            assert abs(sum(i["timeShare"] for i in r["taskBundle"]) - 1) < 0.002, r["id"]


def test_never_selection_and_drafts():
    for r in D.roles():
        assert r["validationStatus"] == "draft" and r["provenance"]["evidenceLabel"] == "S"
        assert all(c.get("criticalForSelection") is not True for c in r["competencyTargets"])


def test_tx_floor_on_every_role():
    for r in D.roles():
        ids = {c["competency"] for c in r["competencyTargets"]}
        assert {D.canon(k) for k in ("seed:DC-CAND-01", "seed:DC-CAND-02", "seed:DC-CAND-13", "seed:DC-CAND-05")} <= ids, r["id"]


def test_emerging_roles_carry_foresight_fields():
    for r in D.roles():
        if r["lifecycleState"] in ("proposed", "emerging"):
            for k in ("evidenceSignals", "feederRoles", "horizon", "scenarioSensitivity", "reviewBy", "counterSignal"):
                assert r.get(k), (r["id"], k)


def test_variant_disclaimers_and_tribal_hold():
    for vid in D.by_type["RoleVariant"]:
        v = D.get(vid)
        if v["sectorActor"] in ("federal", "state"):
            assert V.DISCLAIMER in v["disclaimers"], vid
        if v["sectorActor"] == "tribal":
            assert v["indigenousDataFlag"] and v["approvalStatus"] == "pending-tribal-review"
            assert v["sensitivity"] == "restricted-governed" and not v.get("taskAdds") and not v.get("instruments")


def _outputs():
    return [p for p in OUT.rglob("*") if p.suffix in (".json", ".md", ".csv")]


def test_fsp_disclaimer_and_no_realigned_claims():
    files = list((OUT / "federal-series").glob("*.md")) + list((OUT / "federal-series").glob("*.json"))
    assert files
    for p in files:
        text = p.read_text(encoding="utf-8")
        assert V.DISCLAIMER in text, p
        code = p.stem
        rec = D.series.get(code)
        if rec and not str(rec.get("seriesStatus", "")).startswith("realigned-to:"):
            assert not REALIGNED.search(text), p


def test_every_p1_p2_federal_and_state_variant_has_a_view():
    fed = json.loads((OUT / "federal-series" / "federal_variant_index.json").read_text())["variants"]
    sc = json.loads((OUT / "state-class" / "variant_index.json").read_text())["variants"]
    for r in roles_by_tier("P1") + roles_by_tier("P2"):
        for actor, idx in (("federal", fed), ("state", sc), ("local", sc)):
            v = D.variant_for(r["id"], actor)
            if v:
                assert v["id"] in idx, v["id"]


def test_no_held_ids_or_personal_data_in_outputs():
    held = {vid for vid in D.by_type["RoleVariant"] if V.held(D.get(vid))}
    for p in _outputs():
        text = p.read_text(encoding="utf-8")
        assert not any(h in text for h in held), p
        assert not PII.search(text), p


def test_mirror_links():
    m = json.loads((OUT / "mirror_links.json").read_text())
    assert all(c["linked"] for c in m["acceptanceChecks"])


def test_forester_pd_is_labelled():
    pd = (V.ROOT / "docs" / "package" / "forester_pd_fes_draft.md").read_text(encoding="utf-8")
    assert "SUBJECT TO CLASSIFICATION REVIEW" in pd and V.DISCLAIMER.split(" / ")[0] in pd
    for k in range(1, 10):
        assert f"## Factor {k} " in pd
    # display-gate@1.1.0 (CR-FIX-B-001; ADR-0031 §4.4): the PD carries no percentage, flag or truncation
    assert "% time: set by the supervisor" in pd
    assert not re.search(r"\(\d+(\.\d+)?%\)", pd)             # no numeric duty percentages
    assert "…" not in pd                                          # no truncated statements
    assert "needed-at-entry tasks" not in pd.lower() and "critical tasks" not in pd.lower()


TIME_VALUE = re.compile(r"\b\d{1,3}(\.\d+)?%")
FLAG = re.compile(r"\((?:critical|needed at entry)[^)]*\)|\bcritical, needed at entry\b", re.I)


def test_generated_hr_views_show_no_job_analysis_values():
    """N1 / CR-FIX-B-001: no generated Federal Series Profile or State Class View shows a % time value or a critical /
    needed-at-entry flag while the role is below job-analysis-confirmed (every role is draft at rc.1)."""
    files = [p for sub in ("federal-series", "state-class") for p in (OUT / sub).rglob("*") if p.suffix in (".md", ".json")]
    assert files
    assert all(r["validationStatus"] == "draft" for r in D.roles())
    for p in files:
        text = p.read_text(encoding="utf-8")
        assert not TIME_VALUE.search(text), (p, TIME_VALUE.search(text).group(0))
        assert not FLAG.search(text), p
        if p.suffix == ".json":
            for key in ("pctTime", "timeShare", "critical", "neededAtEntry", "importance", "distinguishing"):
                for m in re.finditer(rf'"{key}": ([^,\n}}]+)', text):
                    assert m.group(1).strip() in ("null", "[]"), (p, key, m.group(1))
