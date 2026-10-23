"""WP-02 acceptance: v1 seeds, restored text, prior-evidence tags, X1 completeness, no stored summaries, held content."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict


from conftest import L

import migrate_v1

DISP = {r["v1_code"]: r for r in L.read_csv(L.DISPOSITION)}
V1_COMPS = [r["key"] for r in L.read_csv(L.V1_BASELINE / "competencies.csv")]
V1_TASKS = [r["key"] for r in L.read_csv(L.V1_BASELINE / "tasks.csv")]
INFO = json.loads((L.DATA_V2 / "migration" / "MIGRATION_INFO.json").read_text())
DE_PATHS = ("assessments/emst-v1-", "crosswalks/emst-v1", "migration/", "governance/", "ids/")


def _records():
    out = {}
    for loc, rec in L.iter_records(L.DATA_V2):
        if isinstance(rec, dict):
            out.setdefault(rec.get("id"), (loc, rec))
    return out


RECS = _records()


def seeds(typ):
    return {rid: r for rid, (_, r) in RECS.items() if r.get("type") == typ and str(rid).startswith("seed:v1-")
            and (r.get("provenance") or {}).get("method") == "v1-migration"}


def test_222_competency_and_666_task_seeds():
    comp = {rid for rid in seeds("Competency") if re.fullmatch(r"seed:v1-\d\.\d+\.\d+", rid)}
    task = {rid for rid in seeds("Task") if re.fullmatch(r"seed:v1-\d\.\d+\.\d+-T[1-3]", rid)}
    assert len(V1_COMPS) == 222 and len(V1_TASKS) == 666
    assert comp == {f"seed:v1-{k[3:]}" for k in V1_COMPS}
    assert task == {f"seed:v1-{k[3:].replace(':', '-')}" for k in V1_TASKS}


def test_seed_records_validate_without_errors(real_report):
    def mine(where):
        return "/seed-v1-" in where or any(p in where for p in DE_PATHS)
    errs = [(i.code, i.where, i.message) for i in real_report.errors if mine(i.where)]
    assert errs == []


def test_v1_text_is_cc0_under_the_lead_dedication():
    lic = L.load_yaml(L.GOVERNANCE / "licensing.yaml")
    assert lic["v1Dedication"] == "granted" and "PROJECT_LEAD_DECISIONS.md" in lic["v1DedicationRecord"]
    assert migrate_v1.V1_LICENSE == "CC0-1.0"
    assert INFO["licensing"]["license"] == "CC0-1.0"
    for rid, (_, r) in RECS.items():
        if (r.get("provenance") or {}).get("method") == "v1-migration":
            assert r["license"] == "CC0-1.0" and "ADR-0013" in r["provenance"]["adr"], rid


def test_every_seed_has_provenance_and_legacy_facets():
    for typ in ("Competency", "Task"):
        for rid, r in seeds(typ).items():
            d = r["provenance"]["derivedFrom"][0]
            assert d["relation"] == "carried" and d["workbookSha256"] == INFO["copyBWorkbookSha256"], rid
            assert r["validationStatus"] == "seed-v1" and r["license"] == migrate_v1.V1_LICENSE, rid
            assert r["v1Domain"]["code"] and r["v1SkillArea"]["code"], rid
            assert any(n["scheme"] == "EMSTv1" for n in r["notation"]), rid


def test_seed_status_follows_the_disposition():
    want = {"carry": "draft", "rewrite": "draft", "move-to-module": "draft", "merge": "superseded", "split": "superseded",
            "move-to-tools": "superseded", "hold-for-tribal-review": "superseded", "retire": "withdrawn"}
    for code, d in DISP.items():
        r = RECS[f"seed:v1-{code}"][1]
        assert r["status"] == want[d["decision"]], code
        if r["status"] == "superseded":
            assert r["replacedBy"], code
        if d["decision"] == "move-to-module":
            assert r["module"] != "core" and RECS[f"seed:v1-{code}"][0].area == r["module"], code


def test_restored_text_from_source():
    c = INFO["counts (generated)"]
    assert c["restoredIndicators"] == 2104
    assert c["restoredKnowledgeApplicationLevels"] == 120
    assert c["titleDescriptionSplits"] == 19
    d5 = RECS["seed:v1-5.1.1"][1]["v1Seed"]["levels"]
    assert all(lv.get("knowledge") and lv.get("application") and lv.get("indicators") for lv in d5)
    split = RECS["seed:v1-1.2.4"][1]
    assert split["prefLabel"]["en"] == "Water quality assessment" and split["v1Seed"]["titleDescriptionSplit"]


def test_restoration_sample_covers_10_percent_and_passes():
    rows = L.read_csv(L.DATA_V2 / "migration" / "restoration_sample.csv")
    by_kind = Counter(r["kind"] for r in rows)
    pops = {r["kind"]: int(re.search(r"population (\d+)", r["note"]).group(1)) for r in rows}
    for kind, n in by_kind.items():
        assert n >= 0.10 * pops[kind], kind
    assert sum(pops[k] for k in pops if k.startswith("indicator")) == 2104
    assert all(r["result"] == "pass" and r["verbatim_in_source"] == "true" for r in rows)


def test_x1_accounts_for_every_v1_key_once_per_decision():
    text = L.X1_TSV.read_text(encoding="utf-8").splitlines()
    header = text[0].split("\t")
    rows = [dict(zip(header, ln.split("\t"))) for ln in text[1:] if ln]
    by = defaultdict(list)
    for r in rows:
        by["v1:" + r["subject_id"].split(":", 1)[1]].append(r)
    assert set(by) == set(V1_COMPS) | set(V1_TASKS)
    pairs = Counter((r["subject_id"], r["predicate_id"], r["object_id"]) for r in rows)
    assert max(pairs.values()) == 1
    for key, items in by.items():
        decisions = {re.match(r"decision=([a-z-]+)", r["comment"]).group(1) for r in items}
        assert len(decisions) == 1, key
        if key in V1_COMPS:
            assert decisions == {DISP[key[3:]]["decision"]}, key
    retired = [r for r in rows if r["subject_id"] == "EMSTv1:3.4.3"]
    assert retired == [r for r in retired if r["object_id"] == "sssom:NoTermFound" and r["predicate_id"] == "emst:retiredWithoutReplacement"]
    split_rows = [r for r in rows if r["subject_id"] == "EMSTv1:4.4.1"]
    assert {r["predicate_id"] for r in split_rows} == {"emst:splitInto"} and len(split_rows) == 2


def test_counts_by_decision_are_generated_from_the_csv():
    assert INFO["counts (generated)"]["competencySeedsByDecision"] == dict(sorted(Counter(d["decision"] for d in DISP.values()).items()))


def test_no_stored_summary_migrated():
    forbidden = set(L.load_yaml(L.LINT_DIR / "computed_fields.yaml")["fields"])
    snake = {re.sub(r"(?<!^)(?=[A-Z])", "_", f).lower() for f in forbidden}
    for rid, (_, r) in RECS.items():
        if (r.get("provenance") or {}).get("method") != "v1-migration":
            continue
        for _, k, _ in L.walk(r):
            assert k not in forbidden | snake, (rid, k)


def test_v1_tags_are_prior_evidence_only():
    v1 = [r for _, (loc, r) in RECS.items() if r.get("raterType") == "v1-analyst"]
    assert len([r for r in v1 if r["type"] == "ExposureAssessment"]) == 666 + 786
    kinds = Counter((r["type"], r.get("objectScheme")) for r in v1)
    assert kinds[("CraftRating", None)] == 222 and kinds[("FunctionRating", None)] == 222
    assert kinds[("RelevanceRating", "v1-family")] == 1002 and kinds[("RelevanceRating", "v1-ethical-lens")] == 35
    for r in v1:
        assert r["raterId"] == "v1-analyst-01" and r["confidence"] == "low" and r["provenance"]["derivedFrom"][0]["relation"] in ("prior-evidence", "recovered")
        assert r["status"] == "draft" and "technicalExposure" not in r
    flags = Counter(f for r in v1 for f in r.get("v1Flags", []))
    for f in ("text_misaligned", "reconstructed_d2", "d2_divergent", "reconciled_d6_2026_03", "normative_h", "pre15a_hybrid"):
        assert flags[f] > 0, f
    s_calls = [r for r in v1 if r["type"] == "ExposureAssessment" and r["v1Values"].get("auto_type") in ("S", "V")]
    assert s_calls and all(r["deploymentMode"] == "compressive" and r["sWatch"] for r in s_calls)   # XR-04
    dual = RECS["seed:v1stage/4.3.2"][1]["v1Values"]
    assert dual["stage_primary_2"] == "S1" and dual["dual_primary_exception"] is True


def test_held_content_is_flagged():
    flags = {"indigenousDataFlag": True, "approvalStatus": "pending-tribal-review", "sensitivity": "restricted-governed"}
    for code in ("5.3.2", "6.5.1", "7.1.1"):
        for rid in [f"seed:v1-{code}"] + [f"seed:v1-{code}-T{n}" for n in (1, 2, 3)]:
            r = RECS[rid][1]
            assert {k: r.get(k) for k in flags} == flags, rid
    assert RECS["seed:v1-5.3.3-T2"][1]["governedData"] == "tribal"
    for rid, (_, r) in RECS.items():
        if r.get("objectScheme") == "v1-ethical-lens" and r["object"].endswith("/L2"):
            assert r.get("indigenousDataFlag") is True, rid


def test_migration_is_deterministic_and_current():
    assert migrate_v1.main(["--check"]) == 0


# ---------------------------------------------------------------- ADR-0029 §3: stability tier and CLD
def test_no_record_carries_the_v1_stability_tier():
    bad = []
    for loc, rec in L.iter_records(L.DATA_V2):
        if not isinstance(rec, dict):
            continue
        for path, k, _v in L.walk(rec):
            if k in ("stabilityTier", "stability_tier"):
                bad.append((rec.get("id"), "/".join(map(str, path + (k,)))))
        v1v = rec.get("v1Values") or {}
        for k in ("stability_tier", "tier"):
            if k in v1v:
                bad.append((rec.get("id"), f"v1Values/{k}"))
    assert not bad, bad[:10]


def test_cld_prior_evidence_is_v1_analyst_only_and_never_computed_input():
    import rules  # noqa: F401  - the computed-view rule implementations
    from rules import change_indicator, effective_use_tier
    cld = [rec for _loc, rec in L.iter_records(L.DATA_V2 / "assessments" / "emst-v1-cld") if isinstance(rec, dict)]
    assert len(cld) == 222
    for rec in cld:
        assert rec["raterType"] == "v1-analyst" and rec["confidence"] == "low" and rec["objectScheme"] == "v1-cld"
        assert {d["relation"] for d in rec["provenance"]["derivedFrom"]} == {"prior-evidence"}
    # the change-indicator rule drops v1-analyst records before counting (ER-0) ...
    ind = {"targetId": cld[0]["subject"], "direction": "decline", "driver": "AI", "kind": "role-change"}
    assert change_indicator.evaluate(ind, cld)["counted"] == []
    # ... and the effective-use-tier evidence cap reads validationStatus only, never v1 prior evidence
    assert "v1-cld" not in json.dumps(effective_use_tier.INPUT_FIELDS)
