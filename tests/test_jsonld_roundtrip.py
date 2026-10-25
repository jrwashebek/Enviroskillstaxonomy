"""rc.1 fix pass M11 (DATA_FIX_BRIEF §9): the JSON-LD bundle loses no key on expand -> compact with the shipped context,
and SKOS never asserts an agent-drafted mapping as a bare triple."""
from __future__ import annotations

import json
from collections import defaultdict

from pyld import jsonld

from conftest import FIXTURES, L, overlay_tree

import build_release

TASK = "emst:core/TSK-EF34GHP"
CMP = "emst:core/CMP-AB12CDN"


def _no_network(url, options=None):
    raise RuntimeError(f"no network: {url}")


jsonld.set_document_loader(_no_network)


def _paths(o, p=()):
    """Key paths of a node; null values are not data in JSON-LD (they mean 'no value'), and '@none' is the
    compaction of a plain literal under a language-map term, so neither counts."""
    if isinstance(o, dict):
        for k, v in o.items():
            if v is None or k == "@none":
                continue
            yield p + (k,)
            yield from _paths(v, p + (k,))
    elif isinstance(o, list):
        for v in o:
            yield from _paths(v, p)


def roundtrip_losses(doc, per_type=None):
    ctx = doc["@context"]
    by = defaultdict(list)
    for n in doc["@graph"]:
        by[n.get("type")].append(n)
    lost = defaultdict(set)
    for t, nodes in by.items():
        for n in nodes[:per_type] if per_type else nodes:
            c = jsonld.compact(jsonld.expand({"@context": ctx, **n}), ctx)
            c.pop("@context", None)
            lost[t] |= set(_paths(n)) - set(_paths(c))
    return {t: sorted("/".join(p) for p in v) for t, v in lost.items() if v}


def _tree(tmp_path):
    data = overlay_tree(tmp_path / "src")
    role = L.load_yaml(FIXTURES / "records" / "valid" / "RoleProfile.yaml")
    role["taskBundle"][0]["task"] = TASK
    role["competencyTargets"][0]["competency"] = CMP
    (data / "core" / "roles").mkdir(parents=True, exist_ok=True)
    L.write_yaml(data / "core" / "roles" / "seed-fx-rol.yaml", role)
    ena = L.load_yaml(FIXTURES / "records" / "valid" / "Enactment.yaml")
    ena["competency"] = CMP
    (data / "core" / "enactments").mkdir(parents=True, exist_ok=True)
    L.write_yaml(data / "core" / "enactments" / "seed-fx-ena.yaml", ena)
    tool = L.load_yaml(FIXTURES / "records" / "valid" / "Tool.yaml")
    tool["servesTasks"] = [TASK]
    (data / "tools").mkdir(exist_ok=True)
    (data / "tools" / "tools.jsonl").write_text(L.jsonl_line(tool) + "\n")
    d = data / "crosswalks" / "fx"
    d.mkdir(parents=True)
    (d / "1.sssom.tsv").write_text(
        "record_id\tsubject_id\tpredicate_id\tobject_id\tmapping_justification\tconfidence\tauthor_id\tmapping_tool\tother\tcomment\n"
        f"a\t{TASK}\tskos:closeMatch\tX:1\tsemapv:LLMBasedMatching\t0.6\temstagent:fx@1\tfx.py@1\trater_type=llm;review_status=candidate\tagent row\n"
        f"b\t{CMP}\tskos:closeMatch\thttps://example.org/x/2\tsemapv:ManualMappingCuration\t0.9\tpid:fx-h1\tfx.py@1\treviewer=pid:fx-h2;review_status=reviewed\thuman row\n")
    (d / "1.sssom.yml").write_text(L.dump_yaml({"mapping_set_id": "https://w3id.org/emst/crosswalks/fx/1", "mapping_set_version": "0.0.1",
                                                "license": "https://creativecommons.org/publicdomain/zero/1.0/",
                                                "curie_map": {"X": "https://example.org/x/"}}))
    return data


def test_bundle_round_trips_without_losing_a_key(tmp_path):
    data = _tree(tmp_path)
    b = build_release.Builder(data, profile="preview", version="2.0.0-dev", build_commit="test")
    files = b.build(tmp_path / "out")
    doc = json.loads(files["emst.bundle.jsonld"])
    types = {n.get("type") for n in doc["@graph"]}
    assert {"Release", "Mapping", "RoleProfile", "Enactment", "Tool", "Task", "CompetencyLevelOutcome"} <= types
    assert roundtrip_losses(doc) == {}
    m = next(n for n in doc["@graph"] if n.get("type") == "Mapping" and n.get("record_id") == "a")
    assert m["other"] == "rater_type=llm;review_status=candidate" and m["mapping_tool"] == "fx.py@1" and m["confidence"] == 0.6
    assert b.context_check(doc) == []


def test_context_defines_the_keys_the_review_found_dropped():
    ctx = json.loads(L.CONTEXT_OUT.read_text(encoding="utf-8"))["@context"]
    for k in ("other", "mapping_tool", "see_also", "reviewer", "matchType", "reviewDate", "crosswalkRecord", "roleVariantKey",
              "storage", "retrieved", "paraphrase", "sha256", "min", "max", "currency", "rangeLabel", "agentDraft"):
        assert k in ctx, k
    assert ctx["agentDraft"]["@type"] == "@json"
    scr = {"@context": ctx, "id": "emst:core/SCR-XXXXXXX", "type": "StateClassRecord",
           "emstMapping": {"reviewer": "pid:fx", "matchType": "skos:closeMatch", "reviewDate": "2026-10-25",
                           "crosswalkRecord": "r1", "roleVariantKey": "k"},
           "payMinMax": {"min": 1, "max": 2, "currency": "USD", "rangeLabel": "A"},
           "workDescriptionText": {"storage": "url-only", "retrieved": "2026-10-23", "sha256": "ab"},
           "mqText": {"storage": "url-only", "paraphrase": "p"}}
    assert roundtrip_losses({"@context": ctx, "@graph": [{k: v for k, v in scr.items() if k != "@context"}]}) == {}


def test_context_check_reports_an_undefined_key(tmp_path):
    data = overlay_tree(tmp_path / "src")
    b = build_release.Builder(data, profile="preview", version="2.0.0-dev", build_commit="test")
    ctx = json.loads(L.CONTEXT_OUT.read_text(encoding="utf-8"))["@context"]
    doc = {"@context": ctx, "@graph": [{"id": "x", "type": "Task", "zzNotATerm": 1, "agentDraft": {"anyKey": 1}}]}
    assert b.context_check(doc) == ["context: 1 keys at Task/zzNotATerm have no JSON-LD term (dropped on expansion)"]


def test_skos_asserts_only_human_reviewed_mappings(tmp_path):
    import rdflib
    data = _tree(tmp_path)
    b = build_release.Builder(data, profile="preview", version="2.0.0-dev", build_commit="test")
    files = b.build(tmp_path / "out")
    g = rdflib.Graph()
    g.parse(data=files["emst.skos.ttl"].decode(), format="turtle")
    close = set(g.triples((None, rdflib.URIRef("http://www.w3.org/2004/02/skos/core#closeMatch"), None)))
    assert {(str(s), str(o)) for s, _, o in close} == {(L.iri(CMP), "https://example.org/x/2")}
