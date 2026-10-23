"""WP-01: cross-record rules fail on seeded violations (tests/fixtures/violations/*) and pass on the base tree."""
from __future__ import annotations

import pytest

from conftest import FIXTURES, L, overlay_tree

import validate_v2

CASES = sorted(p.name for p in (FIXTURES / "violations").iterdir() if p.is_dir())
BASE_REG = FIXTURES / "trees" / "base" / "data" / "v2" / "ids" / "registry.csv"


def run(data, **kw):
    kw.setdefault("use_git_base", False)
    kw.setdefault("check_x1", False)
    return validate_v2.Validator(data, **kw).run()


def test_base_tree_is_clean(tmp_path):
    rep = run(overlay_tree(tmp_path), registry_base=BASE_REG)
    assert [(i.code, i.where, i.message) for i in rep.issues] == []


def test_violation_suite_covers_every_required_check():
    required = {"registry-deleted-row", "registry-edited-row", "module-redefines-core", "module-mints-core-namespace",
                "tribal-held-key-unflagged", "tribal-leak-candidate", "tribal-inherit", "tribal-coords-cultural",
                "confidential-marker", "personal-data-text", "personal-data-field", "typing-lint", "indicator-lint",
                "computed-field", "x1-incomplete"}
    assert required <= set(CASES)


@pytest.mark.parametrize("case", CASES)
def test_seeded_violation_is_caught(tmp_path, case):
    d = FIXTURES / "violations" / case
    exp = L.load_yaml(d / "expect.yaml")
    data = overlay_tree(tmp_path, d)
    rep = run(data, registry_base=BASE_REG if exp["registryBase"] else None, check_x1=exp["checkX1"], strict=exp["strict"])
    codes = set(rep.codes())
    for code in exp["expect"]:
        assert code in codes, f"{case}: expected {code}, got {sorted(codes)}"
    assert rep.errors, f"{case} must fail CI"


def test_registry_status_transition_is_allowed(tmp_path):
    data = overlay_tree(tmp_path)
    reg = data / "ids" / "registry.csv"
    lines = reg.read_text().splitlines()
    parts = lines[1].split(",")
    parts[5], parts[7] = "published", "2.0.0-rc.1"
    lines[1] = ",".join(parts)
    reg.write_text("\n".join(lines) + "\n")
    cmp = next((data / "core" / "competencies").glob("CMP-*.yaml"))
    rec = L.load_yaml(cmp)
    rec.update(status="published", versionIntroduced="2.0.0-rc.1", lastChangedIn="2.0.0-rc.1")
    L.write_yaml(cmp, rec)
    rep = run(data, registry_base=BASE_REG)
    assert [i.code for i in rep.errors] == []


def test_draft_tribal_text_warns_and_strict_mode_errors(tmp_path):
    data = overlay_tree(tmp_path)
    rec = L.load_yaml(FIXTURES / "records" / "valid" / "Competency.yaml")
    rec.update(id="seed:fx-draft-leak", scopeNote={"en": "Includes consultation with Tribal governments."})
    L.write_yaml(data / "core" / "competencies" / "seed-fx-draft-leak.yaml", rec)
    assert "W-TRIBAL-LEAK" in run(data).codes()
    assert "E-TRIBAL-LEAK" in run(data, strict=True).codes()


def test_lint_on_seed_records_is_a_warning(tmp_path):
    data = overlay_tree(tmp_path)
    text = "Use ArcGIS to map plots for the annual field season report"
    rec = L.load_yaml(FIXTURES / "records" / "valid" / "Task.yaml")
    rec.update(id="seed:fx-seed-lint", prefLabel={"en": text}, statement={"en": text}, textSha256=L.text_sha256(text),
               validationStatus="seed-v1")
    L.write_yaml(data / "core" / "tasks" / "seed-fx-seed-lint.yaml", rec)
    codes = run(data).codes()
    assert "W-LINT-TYPING" in codes and "E-LINT-TYPING" not in codes


# ---------------------------------------------------------------- ADR-0029 rulings: warnings and transitional rules
def _valid(t, **kw):
    rec = L.load_yaml(FIXTURES / "records" / "valid" / f"{t}.yaml")
    rec.update(kw)
    return rec


def _base_task_id(data):
    return L.load_yaml(next((data / "core" / "tasks").glob("TSK-*.yaml")))["id"]


def test_role_seed_keys_follow_cr_ia_001(tmp_path):
    data = overlay_tree(tmp_path)
    d = data / "core" / "roles"
    L.write_yaml(d / "seed-R02-field-resource-technician.yaml", _valid("RoleProfile", id="seed:R02-field-resource-technician"))
    L.write_yaml(d / "seed-bad-role--x--y--z.yaml", _valid("RoleProfile", id="seed:bad-role/x/y/z"))
    dv = data / "core" / "variants"
    L.write_yaml(dv / "seed-R02-field-resource-technician--state.yaml",
                 _valid("RoleVariant", id="seed:R02-field-resource-technician/state", variantOf="seed:R02-field-resource-technician"))
    L.write_yaml(dv / "seed-R99-unknown--state.yaml", _valid("RoleVariant", id="seed:R99-unknown/state", variantOf="seed:R02-field-resource-technician"))
    L.write_yaml(dv / "seed-R02-field-resource-technician--galaxy.yaml",
                 _valid("RoleVariant", id="seed:R02-field-resource-technician/galaxy", variantOf="seed:R02-field-resource-technician"))
    flagged = {i.rid for i in run(data).issues if i.code == "W-ROLE-KEY"}
    assert flagged == {"seed:bad-role/x/y/z", "seed:R99-unknown/state", "seed:R02-field-resource-technician/galaxy"}


def test_change_signal_warnings(tmp_path):
    data = overlay_tree(tmp_path)
    tid = _base_task_id(data)
    recs = [
        _valid("ChangeSignal", id="seed:fx-w-key", targetId=tid, signalStatus="watch", independenceKey="unlisted-key"),
        _valid("ChangeSignal", id="seed:fx-w-org", targetType="organization", targetId="opm-agency:AG00",
               measure=dict(_valid("ChangeSignal")["measure"], n=3)),
        _valid("ChangeSignal", id="seed:fx-w-mvp", targetType="RoleProfile", targetId="mvp-role:R02-field-resource-technician"),
        _valid("ChangeSignal", id="seed:fx-w-sp12", targetId=tid, scenarioSignposts=["vocab:scenarios#SP-12"]),
        _valid("ChangeSignal", id="seed:fx-w-nota", targetId=tid, notation=[{"scheme": "EMST-impact", "value": "2"}]),
    ]
    p = data / "signals" / "fixture" / "w.jsonl"
    p.parent.mkdir(parents=True)
    p.write_text("".join(L.jsonl_line(r) + "\n" for r in recs))
    by = {}
    for i in run(data).issues:
        by.setdefault(i.rid, set()).add(i.code)
    assert "W-INDEPENDENCE-KEY-UNLISTED" in by["seed:fx-w-key"]
    assert "W-ORG-SMALL-N" in by["seed:fx-w-org"] and "E-ORG-TARGET-TRIBAL" not in by["seed:fx-w-org"]
    assert "W-MVP-ROLE-TARGET" in by["seed:fx-w-mvp"]
    assert "I-SP12-QUARANTINE" in by["seed:fx-w-sp12"]
    assert "W-NOTATION-INTERIM" in by["seed:fx-w-nota"]
    assert not [i for i in run(data).errors if i.rid and i.rid.startswith("seed:fx-w-") and i.code != "E-REF-DANGLING"]


def test_enactments_are_transitional_on_drafts_only(tmp_path):
    data = overlay_tree(tmp_path)
    d = data / "core" / "competencies"
    L.write_yaml(d / "seed-fx-ena.yaml", _valid("Competency", id="seed:fx-ena", enactments=["emst:core/CMP-AB12CDN"]))
    rep = run(data)
    assert "W-COMPUTED-FIELD-DEPRECATED" in rep.codes() and "E-COMPUTED-FIELD" not in rep.codes()
    assert "E-COMPUTED-FIELD" not in run(data, strict=True).codes()     # drafts never ship; the build ignores the field
    cmp = next(d.glob("CMP-*.yaml"))
    rec = L.load_yaml(cmp)
    rec["enactments"] = ["seed:fx-ena"]
    L.write_yaml(cmp, rec)
    codes = run(data).codes()
    assert "E-COMPUTED-FIELD" in codes and "E-SCHEMA" in codes          # candidate: rejected by schema and validator


def test_task_tools_is_computed(tmp_path):
    data = overlay_tree(tmp_path)
    t = next((data / "core" / "tasks").glob("TSK-*.yaml"))
    rec = L.load_yaml(t)
    rec["tools"] = ["seed:fx-tool"]
    L.write_yaml(t, rec)
    assert "E-COMPUTED-FIELD" in run(data).codes()


def test_waivers_apply_only_while_text_matches(tmp_path):
    import importlib.util
    data = overlay_tree(tmp_path)
    ind = next((data / "core" / "indicators").glob("IND-*.yaml"))
    rec = L.load_yaml(ind)
    rec["statement"] = {"en": "Understands sampling theory and holding times."}       # B01 internal-state verb
    L.write_yaml(ind, rec)
    rep = run(data)
    hits = [i for i in rep.issues if i.rid == rec["id"] and i.code == "E-LINT-INDICATOR"]
    assert hits
    rule = hits[0].message.split()[0].split("[")[0]
    spec = importlib.util.spec_from_file_location("io_lint_t", L.ROOT / "validation" / "lint_indicators.py")
    mod = importlib.util.module_from_spec(spec)
    import sys
    sys.modules["io_lint_t"] = mod
    spec.loader.exec_module(mod)
    sha = mod.text_sha256(rec["statement"]["en"], mod.load_rules())
    w = data / "governance" / "lint_waivers.csv"
    head = "record_id,rule_id,text_sha256,waiver_class,reviewer,second_reviewer,decided_on,rationale\n"
    w.write_text(head + f"{rec['id']},{rule},{sha},false-positive,pid:rev-0001,pid:rev-0002,2026-10-23,synthetic\n")
    rep = run(data)
    assert not [i for i in rep.issues if i.rid == rec["id"] and i.message.startswith(rule)]
    assert rep.stats["lintWaivers"] == {rule: 1}
    rec["statement"] = {"en": "Understands sampling theory and holding times well."}
    L.write_yaml(ind, rec)
    rep = run(data)
    assert "I-WAIVER-VOID" in rep.codes()
    assert [i for i in rep.issues if i.rid == rec["id"] and i.message.startswith(rule)]


def test_sssom_extension_and_review_provenance(tmp_path):
    data = overlay_tree(tmp_path)
    tid = _base_task_id(data)
    d = data / "crosswalks" / "fx-set"
    d.mkdir(parents=True)
    head = "record_id\tsubject_id\tpredicate_id\tobject_id\tmapping_justification\tauthor_id\treviewer_id\tother\n"
    (d / "1.sssom.tsv").write_text(head
                                   + f"a\t{tid}\tskos:closeMatch\tX:1\tsemapv:LLMBasedMatching\temstagent:fx@1\t\treview_status=candidate\n"
                                   + f"b\t{tid}\tskos:closeMatch\tX:2\tsemapv:MappingReview\temstagent:fx@1\tpid:rev-0001\treview_status=reviewed\n"
                                   + f"c\t{tid}\tskos:closeMatch\tX:3\tsemapv:MappingReview\temstagent:fx@1\tpid:rev-0001\toriginal_justification=semapv:LLMBasedMatching\n")
    (d / "1.sssom.yml").write_text(L.dump_yaml({"mapping_set_id": "https://w3id.org/emst/crosswalks/fx-set/1", "mapping_set_version": "0.0.1",
                                                "license": "https://creativecommons.org/publicdomain/zero/1.0/", "curie_map": {"X": "https://example.org/x/"},
                                                "creator_id": ["emstagent:fx@1"]}))
    rep = run(data)
    assert rep.stats["sssom11ExtensionRows"] == {"crosswalks/fx-set/1.sssom.tsv": 1}
    assert "I-SSSOM-1_1-EXTENSION" in rep.codes()
    prov = [i for i in rep.issues if i.code == "W-SSSOM-REVIEW-PROVENANCE"]
    assert len(prov) == 1 and prov[0].where.endswith(":3")
    assert not rep.errors


# ---------------------------------------------------------------- ADR-0030 (RULINGS_FOR_DE Batch 2)
@pytest.fixture(scope="module")
def live_validator():
    return validate_v2.Validator(L.DATA_V2, use_git_base=False)


@pytest.mark.parametrize("text,flagged", [
    ("Map plots in InVEST", True), ("invest time in planning", False), ("Record slack water at the gauge", False),
    ("Identify maple seedlings", False), ("Collect points in Field Maps", True), ("Read field maps before survey", False),
])
def test_product_matching_agrees_with_io_linter(live_validator, text, flagged):
    """CR-DC-001: product names are matched case-sensitively, the same way in validate_v2 and IO's linter."""
    de = bool([t for t, rx in live_validator.products if rx.search(text)])
    assert de is flagged
    if live_validator.io_lint:
        _mod, linter = live_validator.io_lint
        assert bool(linter.product_re.search(text)) is flagged


def test_three_module_rule_and_register(tmp_path):
    data = overlay_tree(tmp_path)
    cmp = L.load_yaml(next((data / "core" / "competencies").glob("CMP-*.yaml")))
    d = data / "modules" / "water" / "enactments"
    ena = _valid("Enactment", id="seed:fx-ena-mod", competency=cmp["id"], enactmentKind="module", enactedInModule="water",
                 subsectors=["W01"], module="water")
    for k in ("actorType", "authorityBasis", "principal", "accountabilityVenue", "craft"):
        ena.pop(k, None)
    L.write_yaml(d / "seed-fx-ena-mod.yaml", ena)
    rep = run(data)
    assert "E-THREE-MODULE" in rep.codes()                         # base competency is a candidate
    assert "I-THREE-MODULE-RECURRENCE" in rep.codes()
    reg = data / "governance" / "three_module_exceptions.yaml"
    reg.write_text(L.dump_yaml({"exceptions": [{"competency": cmp["id"], "modules": ["water"], "rationale": "synthetic",
                                                "decidedBy": "CA", "decidedOn": "2026-10-23", "reviewBy": "2020-01-01",
                                                "decidedIn": "ADR-0030"}, {"competency": "seed:nope"}]}))
    codes = run(data).codes()
    assert "E-THREE-MODULE" not in codes and "W-THREE-MODULE-EXCEPTION-EXPIRED" in codes and "E-THREE-MODULE-EXCEPTION-FORMAT" in codes
    ena.pop("subsectors")
    L.write_yaml(d / "seed-fx-ena-mod.yaml", ena)
    assert "W-MODULE-SUBSECTOR" in run(data).codes()


def test_instrument_links_edges_mirrors_and_clo_rules(tmp_path):
    data = overlay_tree(tmp_path)
    cmp_p = next((data / "core" / "competencies").glob("CMP-*.yaml"))
    cmp = L.load_yaml(cmp_p)
    ins = _valid("Instrument", id="seed:fx-ins-a")
    (data / "instruments").mkdir()
    (data / "instruments" / "i.jsonl").write_text(L.jsonl_line(ins) + "\n")
    ena = _valid("Enactment", id="seed:fx-ena-links", competency=cmp["id"],
                 characteristicInstruments=[{"instrument": "seed:fx-ins-a"}, {"instrument": "seed:fx-ins-a", "role": "requires"}],
                 indicatorVariants=[cmp["levels"][0]["indicators"][0]])
    L.write_yaml(data / "core" / "enactments" / "seed-fx-ena-links.yaml", ena)
    cmp["mirrors"] = [{"target": "seed:fx-ena-links", "relation": "regulated-party-mirror"}]
    cmp["instrumentSensitivity"] = [{"mechanism": _valid("Competency").get("instrumentSensitivity", [{}])[0].get("mechanism", "DM-01"),
                                     "evidenceLabel": "J"}]
    L.write_yaml(cmp_p, cmp)
    ev = _valid("DriverEvent", id="seed:fx-evt-self", instrument="seed:fx-ins-a", actingInstrument="seed:fx-ins-a")
    (data / "events").mkdir()
    (data / "events" / "e.jsonl").write_text(L.jsonl_line(ev) + "\n")
    codes = run(data).codes()
    for c in ("E-INSTRUMENT-LINK-DUPLICATE", "W-INSTRUMENT-ROLE-MISSING", "E-ACTING-SELF", "E-MIRROR-SELF",
              "E-CLO-ENACTMENT-INDICATOR", "E-EDGE-REVIEWBY"):
        assert c in codes, (c, sorted(codes))


def test_planned_role_references_and_held_planned_refs(tmp_path):
    data = overlay_tree(tmp_path)
    t = _valid("Task", id="seed:fx-planned", supports=[{"competency": "seed:FC-C18", "strength": "primary"}])
    sig = _valid("ChangeSignal", id="seed:fx-sig-role", targetType="RoleVariant", targetId="seed:R02-field-resource-technician/state")
    sig2 = _valid("ChangeSignal", id="seed:fx-sig-tribal", targetType="RoleVariant", targetId="seed:R02-field-resource-technician/tribal")
    L.write_yaml(data / "core" / "tasks" / "seed-fx-planned.yaml", t)
    (data / "signals" / "fx").mkdir(parents=True)
    (data / "signals" / "fx" / "s.jsonl").write_text(L.jsonl_line(sig) + "\n" + L.jsonl_line(sig2) + "\n")
    rep = run(data)
    by = {}
    for i in rep.issues:
        by.setdefault(i.rid, set()).add(i.code)
    assert "W-REF-PENDING" in by["seed:fx-planned"]                 # candidate decided core-v2.0
    assert "W-REF-PENDING" in by["seed:fx-sig-role"] and "E-TRIBAL-INHERIT" not in by["seed:fx-sig-role"]
    assert "E-TRIBAL-INHERIT" in by["seed:fx-sig-tribal"]
    assert "E-REF-DANGLING" in run(data, strict=True).codes()


def test_state_class_competency_targets_are_computed(tmp_path):
    data = overlay_tree(tmp_path)
    rec = _valid("StateClassRecord", id="seed:class--fx--001")
    m = rec.get("emstMapping")
    items = m if isinstance(m, list) else [m] if isinstance(m, dict) else []
    if not items:
        rec["emstMapping"] = [{"roleVariant": "seed:R02-field-resource-technician/state", "competencyTargets": []}]
    else:
        items[0]["competencyTargets"] = []
    d = data / "registers" / "state_classes"
    d.mkdir(parents=True)
    L.write_yaml(d / "seed-class--fx--001.yaml", rec)
    assert "E-COMPUTED-FIELD" in run(data).codes()


def test_live_tree_has_no_untyped_instrument_links():
    import convert_instrument_links
    assert convert_instrument_links.convert(L.DATA_V2, check=True) == (0, 0), "run python scripts/convert_instrument_links.py"
