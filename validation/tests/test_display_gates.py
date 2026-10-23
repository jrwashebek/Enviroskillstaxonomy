"""Tests for display_gates.yaml, display_gate.py, reliability.py and lawshe.py (WP-11).

Run: python -m pytest -q validation/tests
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import yaml
import pytest

VAL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(VAL))

import display_gate as G  # noqa: E402
import lawshe  # noqa: E402
import reliability as R  # noqa: E402

GATES = G.load_gates()
HASH = "a" * 64


def result(lb=0.85, n=150, raters=("sme", "analyst"), **kw):
    r = {"dimension": "craft.FC", "codebookVersion": "craft-codebook@1.0.0", "metric": "ordinal", "alpha": lb + 0.05,
         "ciLower": lb, "ciUpper": lb + 0.1, "bootstrapResamples": 10000, "seed": 1, "nUnits": n, "nDistinctRaters": 6,
         "meanRatersPerUnit": 6.0, "raterTypesCounted": list(raters), "preregistrationId": "osf-xxxx", "studyId": "REL-01",
         "studyDate": "2027-03-01", "blindCodingAttested": True, "ruleId": "display-gate", "ruleVersion": "1.0.0-draft",
         "buildCommit": "deadbeef"}
    r.update(kw)
    return r


def value(**kw):
    v = {"dimension": "craft.FC", "codebookVersion": "craft-codebook@1.0.0", "raterTypes": ["sme"], "nHumanRaters": 3,
         "humanConsensus": True, "textSha256": HASH}
    v.update(kw)
    return v


def dec(v=None, r=None, tier="describe", h=HASH):
    return G.decide(v or value(), r, GATES, tier, h)


# ------------------------------------------------------------------------------------------- the seeded CI cases
def test_thresholds_match_adr_0024():
    th = GATES["thresholds"]
    assert th["production_min_lower_bound"] == 0.80 and th["tentative_min_lower_bound"] == 0.667
    assert th["ci"]["bound_used"] == "lower" and GATES["admissibility"]["min_units"] == 120
    assert "llm" in GATES["admissibility"]["rater_types_never_counted"]


@pytest.mark.parametrize("lb,marker,render", [(0.66, "hidden", False), (0.6669, "hidden", False), (0.667, "tentative", True),
                                              (0.70, "tentative", True), (0.80, "production", True), (0.93, "production", True)])
def test_lower_bound_gate(lb, marker, render):
    d = dec(r=result(lb))
    assert d["marker"] == marker and d["render"] is render


def test_no_result_is_assessment_pending():
    d = dec(r=None)
    assert not d["render"] and d["label"] == "assessment_pending"


def test_small_study_is_insufficient():
    assert dec(r=result(0.9, n=100))["label"] == "insufficient_study"


def test_agent_raters_never_count_as_human_agreement():
    assert dec(r=result(0.95, raters=("sme", "llm")))["label"] == "insufficient_study"
    assert dec(r=result(0.95, raters=("llm",)))["label"] == "insufficient_study"
    assert dec(r=result(0.95, raters=("v1-analyst",)))["label"] == "insufficient_study"


def test_unregistered_or_unblinded_study_is_insufficient():
    assert dec(r=result(0.9, preregistrationId=""))["label"] == "insufficient_study"
    assert dec(r=result(0.9, blindCodingAttested=False))["label"] == "insufficient_study"
    assert dec(r=result(0.9, bootstrapResamples=1000))["label"] == "insufficient_study"


def test_codebook_mismatch_and_stale_hash():
    assert not dec(v=value(codebookVersion="craft-codebook@0.9.0"), r=result())["render"]
    assert dec(r=result(), h="b" * 64)["label"] == "stale"
    assert dec(r=result(), h=None)["label"] == "stale"


def test_llm_only_value_and_llm_first_value():
    assert dec(v=value(raterTypes=["llm"]), r=result())["label"] == "assessment_pending"
    assert not dec(v=value(raterTypes=["llm", "sme"], llmGatePassed=False), r=result())["render"]
    assert dec(v=value(raterTypes=["llm", "sme"], llmGatePassed=True), r=result())["render"]


def test_v1_and_external_values_are_not_tags():
    d = dec(v=value(raterTypes=["v1-analyst"]), r=result())
    assert d["marker"] == "drawer-only" and d["label"] == "v1_prior" and not d["render"]
    assert not dec(v=value(raterTypes=["external-index"]), r=result())["render"]


def test_held_content_not_rendered_and_unlabelled():
    d = dec(v=value(held=True), r=result())
    assert d["marker"] == "not-rendered" and d["label"] is None


def test_stratum_gate():
    strata = [{"key": "module", "value": "waste", "nUnits": 40, "alpha": 0.6, "ciLower": 0.55, "ciUpper": 0.7},
              {"key": "module", "value": "forest", "nUnits": 45, "alpha": 0.8, "ciLower": 0.70, "ciUpper": 0.86}]
    r = result(0.82, strata=strata)
    assert dec(v=value(stratum={"module": "waste"}), r=r)["label"] == "below_gate"
    d = dec(v=value(stratum={"module": "forest"}), r=r)
    assert d["render"] and d["marker"] == "tentative"
    d = dec(v=value(stratum={"module": "air"}), r=r)
    assert d["render"] and d["label"] == "stratum_not_estimated"


def test_consensus_requirements():
    assert dec(v=value(humanConsensus=False), r=result())["label"] == "no_consensus"
    assert dec(v=value(nHumanRaters=2), r=result(0.9))["marker"] == "tentative"
    assert dec(v=value(nHumanRaters=1), r=result(0.9))["label"] == "no_consensus"


def test_select_views_admit_production_only():
    assert not dec(r=result(0.70), tier="select")["render"]
    assert dec(r=result(0.85), tier="select")["render"]


def test_rollup_coverage():
    assert G.rollup(["production", "tentative", "hidden"], [0.5, 0.4, 0.1], GATES)["marker"] == "tentative"
    assert not G.rollup(["production", "hidden"], [0.6, 0.4], GATES)["render"]


def test_ci_seeded_cases_listed_in_yaml_cover_the_tests():
    cases = {c["case"] for c in GATES["ci_seeded_cases"]}
    assert len(cases) >= 12


def test_every_dimension_names_metric_and_codebook():
    for d in GATES["dimensions"]:
        assert d["metric"] in R.LEVELS and d["codebook"], d["id"]


# ------------------------------------------------------------------------------------------- reliability.py
NAN = None
KRIPP_2011 = list(zip([1, 2, 3, 3, 2, 1, 4, 1, 2, NAN, NAN, NAN], [1, 2, 3, 3, 2, 2, 4, 1, 2, 5, NAN, 3],
                      [NAN, 3, 3, 3, 2, 3, 4, 2, 2, 5, 1, NAN], [1, 2, 3, 3, 2, 4, 4, 1, 2, 5, 1, NAN]))


@pytest.mark.parametrize("level,expected", [("nominal", 0.743), ("ordinal", 0.815), ("interval", 0.849), ("ratio", 0.797)])
def test_alpha_matches_krippendorff_2011_worked_example(level, expected):
    assert round(R.krippendorff_alpha(KRIPP_2011, level), 3) == expected


def test_alpha_matches_second_published_example():
    w = [[NAN, NAN, NAN, NAN, NAN, 3, 4, 1, 2, 1, 1, 3, 3, NAN, 3], [1, NAN, 2, 1, 3, 3, 4, 3, NAN, NAN, NAN, NAN, NAN, NAN, NAN],
         [NAN, NAN, 2, 1, 3, 4, 4, NAN, 2, 1, 1, 3, 3, NAN, 4]]
    data = list(zip(*w))
    assert round(R.krippendorff_alpha(data, "nominal"), 3) == 0.691
    assert round(R.krippendorff_alpha(data, "interval"), 3) == 0.811


def test_perfect_and_undefined_agreement():
    assert R.krippendorff_alpha([[1, 1], [2, 2], [3, 3]], "nominal") == 1.0
    assert np.isnan(R.krippendorff_alpha([[1, 1], [1, 1]], "nominal"))
    assert R.gate(float("nan")) == "hidden"


def test_bootstrap_is_reproducible_and_brackets_point():
    a = R.bootstrap_alpha(KRIPP_2011, "ordinal", B=2000, seed=7)
    b = R.bootstrap_alpha(KRIPP_2011, "ordinal", B=2000, seed=7)
    assert a == b and a["ciLower"] <= a["alpha"] <= a["ciUpper"] and a["nUnits"] == 11


def test_simulated_study_precision_supports_120_units_x_6_raters():
    """ADR-0024 §4: 120-200 units x 6 raters gives CI half-width ~0.04-0.07. Synthetic latent-trait data."""
    rng = np.random.default_rng(3)
    true = rng.normal(size=150)
    data = np.clip(np.round(true[:, None] + rng.normal(scale=0.5, size=(150, 6)) + 1), 0, 2)
    bs = R.bootstrap_alpha(data, "ordinal", B=2000, seed=1)
    assert (bs["ciUpper"] - bs["ciLower"]) / 2 < 0.08


def test_panel_split_alpha_exceeds_single_rater_alpha():
    rng = np.random.default_rng(5)
    true = rng.normal(size=120)
    data = np.clip(np.round(true[:, None] + rng.normal(scale=0.8, size=(120, 6)) + 1), 0, 2)
    single = R.krippendorff_alpha(data, "ordinal")
    triad = R.panel_split_alpha(data, 3, "ordinal")["alpha"]
    assert triad > single


def test_agreement_result_feeds_the_gate():
    rng = np.random.default_rng(11)
    true = rng.integers(0, 3, size=140)
    data = np.where(rng.random((140, 6)) < 0.92, true[:, None], rng.integers(0, 3, size=(140, 6))).astype(float)
    res = R.agreement_result("craft.FC", "craft-codebook@1.0.0", "ordinal", data, ["sme", "analyst"], "osf-xxxx",
                             "REL-01", "2027-03-01", "deadbeef", True, B=10000, seed=2)
    d = G.decide(value(), res, GATES, "describe", HASH)
    assert res["nUnits"] == 140 and d["render"] and d["marker"] in ("production", "tentative")


# ------------------------------------------------------------------------------------------- lawshe.py
@pytest.mark.parametrize("N,k", [(15, 12), (20, 15), (25, 18), (5, 5), (10, 9)])
def test_lawshe_exact_values_match_adr_0024(N, k):
    assert lawshe.critical_essential(N) == k


def test_lawshe_small_panels_cannot_reach_significance():
    assert lawshe.critical_essential(3) is None and lawshe.critical_essential(4) is None


def test_lawshe_retain_rule():
    assert lawshe.retain(12, 13, 15) and not lawshe.retain(11, 15, 15) and not lawshe.retain(12, 11, 15)


def test_weak_category_caps_marker_at_tentative():
    r = result(0.85, perCategory=[{"category": "2", "nUnits": 14, "alpha": 0.42}, {"category": "0", "nUnits": 60, "alpha": 0.9}])
    assert dec(v=value(category="2"), r=r)["marker"] == "tentative"
    assert dec(v=value(category="0"), r=r)["marker"] == "production"


# ------------------------------------------------------------------------------------------- display-gate@1.1.0 role-profile values
RULE_110 = VAL.parent / "vocab" / "rules" / "display-gate@1.1.0.yaml"
ED = "RoleProfile.competencyTargets.targetLevel"
TS = "RoleProfile.taskBundle.timeShare"


def rv(field, status="draft", reviewers=("emstagent:wp08@1",), **kw):
    v = {"field": field, "validationStatus": status, "reviewers": list(reviewers)}
    v.update(kw)
    return v


def rdec(v, tier="describe", context="role"):
    return G.decide(v, None, GATES, tier, None, context)


@pytest.mark.skipif(not RULE_110.exists(), reason="CA rule file not present")
def test_role_field_lists_match_the_ca_rule_file():
    rule = yaml.safe_load(RULE_110.read_text(encoding="utf-8"))["definition"]
    rp = GATES["role_profile_values"]
    assert set(rp["editorial_design_values"]["fields"]) == set(rule["editorial_design_values"])
    assert set(rp["job_analysis_values"]["fields"]) == set(rule["job_analysis_values"])
    editorial = {e["field"] for e in GATES["not_alpha_gated"]["editorial_definitions"]}
    assert editorial == set(rule["editorial_fields"])
    assert GATES["version"] == "1.1.0" and GATES["agreement_result_schema"]["ruleVersion"] == "1.1.0"


def test_every_role_label_resolves():
    rp = GATES["role_profile_values"]
    used = {rp["editorial_design_values"]["unreviewed"]["label"], rp["editorial_design_values"]["reviewed"]["label"],
            rp["job_analysis_values"]["pending_label"], rp["job_analysis_values"]["hr_classification_min_status"]["pending_label"],
            *rp["job_analysis_values"]["status_labels"].values()}
    assert used <= set(rp["role_labels"])


@pytest.mark.parametrize("field", ["RoleProfile.taskBundle.task", "RoleProfile.roleLevels", "RoleProfile.taskBundle.formationTask",
                                   "RoleProfile.competencyTargets.competency", ED])
def test_agent_drafted_editorial_design_values_render_labelled_at_describe(field):
    d = rdec(rv(field))
    assert d["render"] and d["marker"] == "editorial" and d["label"] == "editorial_draft"


def test_editorial_drafts_not_in_develop_and_never_in_select():
    assert not rdec(rv(ED), tier="develop")["render"]
    assert not rdec(rv(ED), tier="select")["render"]
    assert not rdec(rv(ED, "reviewed", ["pid:p-0007"]), context="select")["render"]
    d = rdec(rv(ED, "reviewed", ["pid:p-0007"]), tier="develop", context="gap-check")
    assert d["render"] and d["label"] == "editorial_reviewed"


@pytest.mark.parametrize("field", ["RoleProfile.taskBundle.importance", TS, "RoleProfile.taskBundle.critical",
                                   "RoleProfile.taskBundle.neededAtEntry", "RoleProfile.competencyTargets.importance",
                                   "RoleProfile.competencyTargets.distinguishing", "RoleProfile.competencyTargets.criticalForSelection"])
def test_agent_drafted_job_analysis_values_are_pending(field):
    d = rdec(rv(field))
    assert not d["render"] and d["marker"] == "pending" and d["label"] == "assessment_pending_job_analysis"


def test_job_analysis_value_needs_a_person_and_reviewed_status():
    assert not rdec(rv(TS, "reviewed", ["emstagent:wp08@1"]))["render"]          # agent review is not review
    assert not rdec(rv(TS, "draft", ["pid:p-0007"]))["render"]                    # a person but status draft
    d = rdec(rv(TS, "reviewed", ["pid:p-0007"]))
    assert d["render"] and d["marker"] == "editorial" and d["label"] == "status_reviewed"
    assert rdec(rv(TS, "reviewed", reviewers=(), reviewedBy="pid:p-0007"))["render"]


@pytest.mark.parametrize("context", ["federal-series-profile", "state-class-view"])
def test_hr_views_need_job_analysis_confirmed_for_time_share_and_importance(context):
    d = rdec(rv(TS, "reviewed", ["pid:p-0007"]), context=context)
    assert not d["render"] and d["label"] == "fsp_time_share_notice"
    assert not rdec(rv("RoleProfile.taskBundle.importance", "panel-retained", ["pid:p-0007"]), context=context)["render"]
    d = rdec(rv("RoleProfile.taskBundle.importance", "job-analysis-confirmed", ["pid:p-0007"]), context=context)
    assert d["render"] and d["label"] == "status_job_analysis_confirmed"
    assert rdec(rv("RoleProfile.taskBundle.critical", "reviewed", ["pid:p-0007"]), context=context)["render"]


def test_select_context_needs_job_analysis_confirmed():
    assert not rdec(rv("RoleProfile.competencyTargets.criticalForSelection", "reviewed", ["pid:p-0007"]), tier="select", context="select")["render"]
    assert rdec(rv("RoleProfile.competencyTargets.criticalForSelection", "job-analysis-confirmed", ["pid:p-0007"]), tier="select", context="select")["render"]


def test_role_values_fail_closed():
    assert not rdec(rv("RoleProfile.taskBundle.colour"))["render"]
    assert not rdec(rv(ED), context="somewhere")["render"]
    assert rdec(rv(ED, held=True))["marker"] == "not-rendered"
    assert not rdec({"field": TS})["render"]


def test_rated_values_unaffected_by_role_routing():
    assert dec(r=result(0.85))["marker"] == "production"
