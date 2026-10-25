"""Release gate (build plan §5): publication status for items 6 and 7, and the Q13 sign-off path (project lead decision
Q13, 2026-10-24; DATA_FIX_BRIEF §10-11)."""
from __future__ import annotations

from conftest import L

import release_gate as G

REVIEWED = {"reviewer_id": "pid:fx-h1"}


def _sets(reviewed=True):
    rows = {"emst-v1/x": [{"subject_id": f"EMSTv1:{i}"} for i in range(3)]}
    for code in G.REVIEWED_SUBSET:
        d = G.CROSSWALKS[code][0].rstrip("-") + ("-tx" if code == "X5" else "")
        rows[f"{d}/1"] = [dict({"subject_id": "s"}, **(REVIEWED if reviewed else {}))]
    return rows


def _signoff(reviewer_date="2026-11-01", sign_date="2026-11-02", reviewer="pid:fx-sme1"):
    return {"humanReviewers": [{"reviewer": reviewer, "role": "subject-matter reviewer", "date": reviewer_date}],
            "projectLeadSignature": {"date": sign_date, "scope": "external publication"}}


def test_status_line_until_items_6_and_7_pass():
    st = G.publication_status(_sets(reviewed=False), {}, 3)
    assert st["line"] == "not cleared for external publication; items 6 and 7 fail" and not st["cleared"]
    assert st["item6"]["withoutHumanReviewedSubset"] == list(G.REVIEWED_SUBSET)
    st = G.publication_status(_sets(), {}, 3)
    assert st["line"] == "not cleared for external publication; item 7 fails"
    st = G.publication_status(_sets(), _signoff(), 3)
    assert st["cleared"] and st["line"].startswith("items 6 and 7 pass")
    assert not G.publication_status(_sets(), _signoff(), 4)["item6"]["pass"]       # X1 incomplete


def test_q13_needs_a_named_human_reviewer_before_the_lead_signs():
    assert not G.signoff_state({})["valid"]
    assert not G.signoff_state({"projectLeadSignature": {"date": "2026-11-02"}})["valid"]          # no reviewer
    assert not G.signoff_state(_signoff(reviewer_date="2026-11-03"))["valid"]                      # review after signing
    assert not G.signoff_state(_signoff(reviewer="emstagent:as-agent@1"))["valid"]                 # an AI agent is advisory
    assert not G.signoff_state(_signoff(sign_date=""))["valid"]                                    # reviewed, not signed
    assert G.signoff_state(_signoff())["valid"]


def test_crosswalk_codes_follow_adr_0022():
    assert G.crosswalk_of("opm-series/2026-10-23") == "X4"
    assert G.crosswalk_of("opm-series-competency/2026-10-23") is None              # competency -> series is not X4
    assert G.crosswalk_of("local-class-wa-lewis-county/2026-10-23") == "X5"
    assert G.crosswalk_of("soc/2018") == "X3" and G.crosswalk_of("emst-v1/emst-v1_to_v2") == "X1"


def test_rc1_signoff_record_is_well_formed():
    s = G.load_signoff("2.0.0-rc.1")
    assert s.get("release") == "2.0.0-rc.1" and "Q13" in s.get("rule", "")
    for r in s.get("humanReviewers") or []:                                        # pseudonymous people only
        assert str(r["reviewer"]).startswith("pid:") and r.get("date")
    sig = s.get("projectLeadSignature")
    assert sig is None or (isinstance(sig, dict) and sig.get("date"))
    for c in s.get("advisoryAgentChecks") or []:
        assert c.get("effect") == "advisory"


def test_gate_item_7_text_records_the_q13_path():
    plan = (L.ROOT / "docs" / "decisions" / "PHASE4_BUILD_PLAN.md").read_text(encoding="utf-8")
    gate = plan.split("## 5. Release gate", 1)[1].split("\n## ", 1)[0]
    item7 = next(ln for ln in gate.splitlines() if ln.startswith("7. "))
    assert "project lead" in item7 and "named human subject-matter reviewer" in item7 and "advisory" in item7
    signoff = (L.ROOT / "docs" / "methods" / "WP15_SIGNOFF.md").read_text(encoding="utf-8")
    assert "Q13" in signoff and "AS co-signs" not in signoff


def test_render_is_deterministic_and_states_q13():
    ev = {"version": "9.9.9", "asOf": "2026-10-25", "buildCommit": "c", "released": "2026-10-23", "schemaVersion": "s",
          "sha256SUMS": "x", "files": 1, "bundleSha256": "y", "statusLine": None, "counts": {}, "ci": {},
          "item2": {"coreSizeLine": "Core competencies: 160 released + held core reported as a count (12); range 120-180 (counts@1.1.0)."},
          "item3": {"effectiveUseTierRows": 1, "effectiveUseTier": {"describe": 1}, "elementsWithoutEffectiveTier": [],
                    "selectAnywhere": 0, "displayGateRows": 1, "displayGateDecisions": {"pending": 1}, "displayGateRule": "1.1.0",
                    "agentDraftNodes": 1},
          "item4": {"wave1Present": {"air": 1}, "otherModules": {}},
          "item5": {"roles": 37, "byTier": {"P1": 1}, "depthRange": {"P1": {"tasks": [22, 35], "targets": [16, 31]}},
                    "lifecycleByTier": {"P1": {"established": 1}}, "fspFiles": 1, "p1p2FederalVariants": 1,
                    "p1p2FederalVariantsInAnFsp": 1, "p1p2FederalVariantsWithoutFsp": [], "scvFiles": 1, "p1p2StateVariants": 1,
                    "p1p2StateVariantsIndexed": 1, "p1p2StateVariantsWithAClassView": 1},
          "item6": {c: {"rows": 1, "subjects": 1, "reviewStatus": {}, "raterType": {"llm": 1}, "justification": {}, "humanReviewed": 0}
                    for c in G.CROSSWALKS},
          "x2Detail": {"rows": 316, "withAnOnetObject": 202, "agreed": 153, "agreedIncludingNoTermFound": 198,
                       "agreedAtCloseMatchOrBetter": 16, "noTermFoundWithPositivePredicate": 0,
                       "kappaMatchType": {"value": 0.465, "source": "k.json"}},
          "publication": G.publication_status(_sets(reviewed=False), {}, 3),
          "item7": {"registerRows": 1, "byStatus": {"verified": 1}, "unverifiedOrHeld": [], "recheckOnOrBeforeAsOf": [],
                    "recheckDates": {"2026-11-12": 1}, "recheckOther": {}, "signoffRecord": "docs/release/9.9.9/PUBLICATION_SIGNOFF.yaml",
                    "signoffRecordExists": False, "signoff": G.signoff_state({}), "wp15StatusLine": "- **Owner:** LM", "acr": True,
                    "securityPacket": True},
          "item8": {"Q1": True, "Q2": True, "Q13": True}}
    a, b = G.render(ev), G.render(ev)
    assert a == b
    assert "not cleared for external publication; items 6 and 7 fail" in a
    assert G.Q13 in a and "No human review or signature has been recorded." in a
    assert "agreed at closeMatch or better: 16" in a and "0.465" in a and "< 0.6 → fail" in a
    assert "| 7. " in a and "**fail**" in a


def test_recut_compares_builds_byte_for_byte(tmp_path):
    import recut_release
    a, b = tmp_path / "a", tmp_path / "b"
    for d in (a, b):
        (d / "views").mkdir(parents=True)
        (d / "views" / "x.json").write_text("{}\n")
    assert recut_release.same_tree(a, b) == []
    (b / "views" / "x.json").write_text("{ }\n")
    (b / "extra.txt").write_text("x")
    assert recut_release.same_tree(a, b) == ["extra.txt", "views/x.json"]


def test_build_record_documents_the_one_command_recut(tmp_path):
    import release_docs
    d = tmp_path / "dist"
    d.mkdir()
    (d / "SHA256SUMS").write_bytes(b"0  a\n")
    (d / "emst.bundle.jsonld").write_bytes(b"{}")
    (d / "RELEASE_NOTES.md").write_text("- Released: 2026-10-23 · build abc+recut-pending-commit\n", encoding="utf-8")
    md = release_docs.build_md("9.9.9", d)
    assert "python3 scripts/recut_release.py --version 9.9.9 " in md and "--pending" in md
    assert "+recut-pending-commit" in md and "SOURCE_DATE_EPOCH" in md and "+uncommitted" in md
