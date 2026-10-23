#!/usr/bin/env python3
"""Generate schema/emst.schema.json and schema/emst.context.jsonld (WP-01).

The structural schema is hand-maintained in schema/src/emst.schema.src.yaml. Every enumeration that names an L0
term is GENERATED here from vocab/*.yaml (all 19 schemes), together with the EmstId pattern
(vocab/identifiers.yaml), the entity-type list and per-type dispatcher (vocab/competency_types.yaml#entity_kinds)
and the StateClassRecord field set (vocab/state_class_fields.yaml). A vocabulary change therefore reaches the
schema only through a reviewed vocab PR plus a rebuild, and CI's `--check` fails if the committed schema is stale.

Usage:
  python scripts/build_schema.py            # write schema/emst.schema.json and schema/emst.context.jsonld
  python scripts/build_schema.py --check    # exit 1 if either file differs from what would be generated
  python scripts/build_schema.py --list     # print each generated enum and its source
"""
from __future__ import annotations

import argparse
import copy
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emstlib as L  # noqa: E402

VOCAB_FILES = sorted(p.name for p in L.VOCAB.glob("*.yaml"))


def _notations(items):
    out = []
    for it in items or []:
        if isinstance(it, dict):
            v = it.get("notation", it.get("value"))
        else:
            v = it
        if v is not None:
            out.append(v if not isinstance(v, bool) else str(v).lower())
    return out


def _uniq(seq):
    seen, out = set(), []
    for s in seq:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


def generate_enums(vocab_dir: Path = L.VOCAB) -> dict[str, dict]:
    """Return {def_name: {"enum": [...], "source": "file#path"}} for every generated enumeration."""
    V = {name[:-5]: L.load_yaml(vocab_dir / name) for name in sorted(p.name for p in vocab_dir.glob("*.yaml"))}
    E: dict[str, dict] = {}

    def put(name, values, src):
        values = _uniq([str(v) if not isinstance(v, (int, float)) or isinstance(v, bool) else v for v in values])
        if not values:
            raise ValueError(f"empty enumeration {name} from {src}")
        E[name] = {"enum": values, "source": src}

    a = V["authority_positions"]
    put("v_authorityPosition", _notations(a["terms"]), "authority_positions.yaml#terms")
    put("v_signOffAuthority", _notations(a["sign_off_authority"]["values"]), "authority_positions.yaml#sign_off_authority")

    c = V["change_types"]
    put("v_contentChangeType", _notations(c["content_change_types"]["values"]), "change_types.yaml#content_change_types")
    put("v_roleSignalType", _notations(c["role_signal_types"]["values"]), "change_types.yaml#role_signal_types")
    put("v_signalDirection", c["signal_directions"]["values"], "change_types.yaml#signal_directions")
    put("v_directionConfidence", c["signal_directions"]["direction_confidence"], "change_types.yaml#signal_directions.direction_confidence")
    put("v_driverTag", _notations(c["driver_tags"]["values"]), "change_types.yaml#driver_tags")
    put("v_horizon", c["horizons"]["values"], "change_types.yaml#horizons")
    put("v_steepCategory", c["steep_v_categories"], "change_types.yaml#steep_v_categories")
    put("v_signalReliability", _notations(c["signal_reliability"]["values"]), "change_types.yaml#signal_reliability")

    ct = V["competency_types"]
    put("v_competencyType", _notations(ct["terms"]), "competency_types.yaml#terms")
    clusters = [cl["notation"] for t in ct["terms"] for cl in t.get("clusters", [])]
    put("v_transversalCluster", clusters, "competency_types.yaml#terms.transversal.clusters")
    put("v_reusability", _notations(ct["reusability"]["values"]), "competency_types.yaml#reusability")
    kinds = [k["kind"] for k in ct["entity_kinds"]]
    put("v_entityType", ["VocabularyTerm"] + kinds, "competency_types.yaml#entity_kinds (+ VocabularyTerm, SPEC §5.1)")
    ena = [x for k in ct["entity_kinds"] for x in k.get("enactment_kinds", [])]
    put("v_enactmentKind", ena, "competency_types.yaml#entity_kinds.Enactment.enactment_kinds")

    cr = V["crafts"]
    put("v_craft", _notations(cr["terms"]), "crafts.yaml#terms")
    put("v_craftComponent", [x["notation"] for t in cr["terms"] for x in t.get("components", [])], "crafts.yaml#terms.components")
    E["v_craftRatingValue"] = {"enum": [x["value"] for x in cr["rating_scale"]["values"]], "source": "crafts.yaml#rating_scale.values"}
    put("v_craftScale", [cr["rating_scale"]["scale_id"]] + list(cr["rating_scale"]["alternative_scales"]), "crafts.yaml#rating_scale")
    put("v_fieldDependency", cr["task_attributes"]["field_dependency"]["values"], "crafts.yaml#task_attributes.field_dependency")
    put("v_formationDependency", [str(v).lower() if isinstance(v, bool) else v for v in cr["task_attributes"]["formation_dependency"]["values"]],
        "crafts.yaml#task_attributes.formation_dependency")
    rr = cr["reproduction_regime_attributes"]
    put("v_mentorshipDependence", rr["mentorship_dependence"]["values"], "crafts.yaml#reproduction_regime_attributes.mentorship_dependence")
    put("v_cycleDependence", rr["cycle_dependence"]["values"], "crafts.yaml#reproduction_regime_attributes.cycle_dependence")
    put("v_placeBoundness", [x["value"] for x in rr["place_boundness"]["values"]], "crafts.yaml#reproduction_regime_attributes.place_boundness")
    put("v_credentialGateLevel", rr["credential_gate"]["values"], "crafts.yaml#reproduction_regime_attributes.credential_gate")
    put("v_currencyDecay", rr["currency_decay"]["values"], "crafts.yaml#reproduction_regime_attributes.currency_decay")

    put("v_driverMechanism", _notations(V["driver_mechanisms"]["terms"]), "driver_mechanisms.yaml#terms (retired excluded)")

    ev = V["evidence_labels"]
    put("v_evidenceLabel", _notations(ev["evidence_labels"]), "evidence_labels.yaml#evidence_labels")
    put("v_provenanceMethod", ev["provenance_methods"], "evidence_labels.yaml#provenance_methods")
    put("v_derivedFromRelation", ev["derived_from_relations"], "evidence_labels.yaml#derived_from_relations")
    put("v_reviewStatus", _notations(ev["review_statuses"]), "evidence_labels.yaml#review_statuses")
    put("v_raterType", _notations(ev["rater_types"]), "evidence_labels.yaml#rater_types")
    put("v_changeRecordType", _notations(ev["change_types"]), "evidence_labels.yaml#change_types")
    put("v_semverImpact", ev["semver_impacts"], "evidence_labels.yaml#semver_impacts")
    put("v_commentDisposition", ev["comment_dispositions"], "evidence_labels.yaml#comment_dispositions")

    ex = V["exposure_instrument_v2"]
    k = ex["constructs"]
    put("v_exposureVector", _notations(k["technical_exposure"]["vectors"]), "exposure_instrument_v2.yaml#constructs.technical_exposure.vectors")
    put("v_exposureLevel", _notations(k["technical_exposure"]["levels"]), "exposure_instrument_v2.yaml#constructs.technical_exposure.levels")
    put("v_deploymentMode", _notations(k["deployment_mode"]["modes"]), "exposure_instrument_v2.yaml#constructs.deployment_mode.modes")
    put("v_deploymentStage", k["deployment_mode"]["deployment_stages"], "exposure_instrument_v2.yaml#constructs.deployment_mode.deployment_stages")
    put("v_adoptionStrategy", _notations(k["deployment_mode"]["strategy_tags"]), "exposure_instrument_v2.yaml#constructs.deployment_mode.strategy_tags")
    put("v_staffingOutcome", k["outcome"]["staffing_outcome_values"], "exposure_instrument_v2.yaml#constructs.outcome.staffing_outcome_values")
    put("v_demandDirection", k["outcome"]["scenario_rows"]["demand_direction"], "exposure_instrument_v2.yaml#constructs.outcome.scenario_rows.demand_direction")
    put("v_reproductionRisk", k["outcome"]["scenario_rows"]["reproduction_risk"], "exposure_instrument_v2.yaml#constructs.outcome.scenario_rows.reproduction_risk")
    sta = {x["field"]: x for x in ex["supporting_task_attributes"]}
    put("v_tacitExperienceRequirement", sta["tacitExperienceRequirement"]["values"], "exposure_instrument_v2.yaml#supporting_task_attributes.tacitExperienceRequirement")
    put("v_governedData", sta["governedData"]["values"], "exposure_instrument_v2.yaml#supporting_task_attributes.governedData")
    put("v_v1ExposureFlag", ex["v1_migration_mapping"]["flags"], "exposure_instrument_v2.yaml#v1_migration_mapping.flags")
    put("v_exposureRule", [r["id"] for r in ex["rules"]], "exposure_instrument_v2.yaml#rules")

    ft = V["friction_types"]
    put("v_frictionType", _notations(ft["friction_types"]["values"]), "friction_types.yaml#friction_types")
    put("v_jurisdictionalContext", _notations(ft["jurisdictional_context"]["values"]), "friction_types.yaml#jurisdictional_context")
    put("v_assessmentMethod", _notations(ft["assessment_methods"]["values"]), "friction_types.yaml#assessment_methods")

    idf = V["identifiers"]
    put("v_idTypePrefix", [t["prefix"] for t in idf["types"]], "identifiers.yaml#types")
    put("v_namespace", [n["namespace"] for n in idf["namespaces"]["registered"]], "identifiers.yaml#namespaces.registered")

    lc = V["lifecycle_states"]
    put("v_lifecycleState", _notations(lc["lifecycle_states"]), "lifecycle_states.yaml#lifecycle_states")
    put("v_editorialStatus", _notations(lc["editorial_statuses"]), "lifecycle_states.yaml#editorial_statuses")
    put("v_useTier", _notations(lc["use_tiers"]["values"]), "lifecycle_states.yaml#use_tiers")
    put("v_validationStatus", _notations(lc["validation_statuses"]), "lifecycle_states.yaml#validation_statuses")
    l4 = lc["l4_state_mapping"]
    put("v_toolLifecycleState", [v for kk, v in l4.items() if kk != "description"], "lifecycle_states.yaml#l4_state_mapping")
    put("v_protectCriterion", [f"PC-{i}" for i, _ in enumerate(lc["protect_overlay"]["criteria_two_of"], 1)],
        "lifecycle_states.yaml#protect_overlay.criteria_two_of (PC-n = n-th criterion)")

    mp = V["mapping_predicates"]
    put("v_mappingPredicate", _notations(mp["skos_predicates"]) + _notations(mp["emst_relations"]), "mapping_predicates.yaml#skos_predicates+emst_relations")
    put("v_mappingJustification", mp["justifications"], "mapping_predicates.yaml#justifications")
    put("v_mappingSetId", [s["id"] for s in mp["mapping_sets"]], "mapping_predicates.yaml#mapping_sets")

    mo = V["modules"]
    put("v_moduleId", _notations(mo["terms"]), "modules.yaml#terms")
    put("v_moduleNamespace", [mo["core"]["namespace"]] + [t["namespace"] for t in mo["terms"]], "modules.yaml#core+terms.namespace")

    pl = V["proficiency_levels"]
    put("v_proficiencyLevel", _notations(pl["terms"]), "proficiency_levels.yaml#terms")
    put("v_level", [t["notation"] for t in pl["terms"] if t.get("isLevel", True) is not False], "proficiency_levels.yaml#terms (isLevel)")
    put("v_proficiencyAttribute", _notations(pl["attributes"]), "proficiency_levels.yaml#attributes")
    put("v_augmentationMode", _notations(pl["augmentation_modes"]), "proficiency_levels.yaml#augmentation_modes")
    put("v_roleLevelKey", [b["key"] for b in pl["role_level_bands"]], "proficiency_levels.yaml#role_level_bands")
    put("v_publicationRule", [r["id"] for r in pl["publication_rules"]], "proficiency_levels.yaml#publication_rules")

    sc = V["scenarios"]
    put("v_scenario", _notations(sc["terms"]), "scenarios.yaml#terms")
    put("v_scenarioAxis", _notations(sc["axes"]), "scenarios.yaml#axes")

    sa = V["sector_actors"]
    put("v_sectorActor", _notations(sa["terms"]), "sector_actors.yaml#terms")
    put("v_sectorActorSubtype", [s["notation"] for t in sa["terms"] for s in t.get("subtypes", [])], "sector_actors.yaml#terms.subtypes")
    tribal = [t for t in sa["terms"] if t["notation"] == "tribal"]
    put("v_tribalActor", ["tribal"] + [x["notation"] for t in tribal for x in t.get("subtypes", [])], "sector_actors.yaml#terms.tribal (+subtypes)")
    put("v_industry", sa["industry"]["values"], "sector_actors.yaml#industry")
    put("v_ownership", sa["ownership"]["values"], "sector_actors.yaml#ownership")
    put("v_deliveryModel", _notations(sa["delivery_model"]["values"]), "sector_actors.yaml#delivery_model")

    ss = V["subsectors"]
    put("v_subsector", _notations(ss["terms"]), "subsectors.yaml#terms")
    put("v_subsectorCluster", _notations(ss["clusters"]), "subsectors.yaml#clusters")

    wf = V["work_functions"]
    put("v_workFunction", [t["notation"] for t in wf["terms"]] + [s["notation"] for t in wf["terms"] for s in t.get("subfunctions", [])],
        "work_functions.yaml#terms+subfunctions")
    put("v_workMode", _notations(wf["modes"]["terms"]), "work_functions.yaml#modes")
    put("v_relationshipType", [r["value"] for t in wf["modes"]["terms"] for r in t.get("relationship_types", [])], "work_functions.yaml#modes.relationship_types")

    put("v_workflowProfile", _notations(V["workflow_profiles"]["terms"]), "workflow_profiles.yaml#terms")

    put("v_stateClassField", [_camel(f["field"]) for f in V["state_class_fields"]["fields"]], "state_class_fields.yaml#fields")

    # formerly schema-local code lists, moved into vocab/ by the CA (CR-DE-001 #4; ADR-0029 §1)
    put("v_toolType", _notations(ct["tool_types"]["values"]), "competency_types.yaml#tool_types")
    dm = V["driver_mechanisms"]
    put("v_instrumentType", _notations(dm["instrument_types"]["values"]), "driver_mechanisms.yaml#instrument_types")
    put("v_eventType", _notations(dm["event_types"]["values"]), "driver_mechanisms.yaml#event_types")
    put("v_eventDirection", _notations(dm["event_directions"]["values"]), "driver_mechanisms.yaml#event_directions")
    put("v_instrumentStatus", _notations(dm["instrument_statuses"]["values"]), "driver_mechanisms.yaml#instrument_statuses")
    put("v_credentialType", _notations(a["credential_types"]["values"]), "authority_positions.yaml#credential_types")
    put("v_closureType", _notations(a["closure_types"]["values"]), "authority_positions.yaml#closure_types")
    put("v_pathwayType", _notations(ft["pathway_types"]["values"]), "friction_types.yaml#pathway_types")
    put("v_learningResourceType", _notations(ft["learning_resource_types"]["values"]), "friction_types.yaml#learning_resource_types")
    put("v_frictionDirection", _notations(ft["friction_directions"]["values"]), "friction_types.yaml#friction_directions")
    put("v_frictionSeverity", _notations(ft["friction_severities"]["values"]), "friction_types.yaml#friction_severities")
    put("v_frictionBasis", _notations(ft["friction_bases"]["values"]), "friction_types.yaml#friction_bases")
    put("v_signalStatus", _notations(c["signal_statuses"]["values"]), "change_types.yaml#signal_statuses")
    put("v_signalFamily", _notations(c["signal_families"]["values"]), "change_types.yaml#signal_families")
    put("v_changeIndicatorKind", _notations(c["change_indicator_kinds"]["values"]), "change_types.yaml#change_indicator_kinds")
    put("v_indicatorUseClass", lc["use_tiers"]["indicator_use_classes"], "lifecycle_states.yaml#use_tiers.indicator_use_classes")
    ros = ev["rating_object_schemes"]["values"]
    put("v_ratingObjectScheme", _notations(ros), "evidence_labels.yaml#rating_object_schemes")
    put("v_ratingObjectSchemeV2", [x["notation"] for x in ros if not x.get("v1_only")],
        "evidence_labels.yaml#rating_object_schemes (items without v1_only)")
    put("v_signpost", [x["notation"] for x in sc["signposts"]], "scenarios.yaml#signposts")
    put("v_scenarioPole", [f"{ax['notation']}:{p['notation']}" for ax in sc["axes"] for p in ax["poles"]], "scenarios.yaml#axes.poles")

    used = {s.split("#")[0].split(" ")[0] for s in (e["source"] for e in E.values())}
    missing = sorted(set(VOCAB_FILES) - used)
    if missing:
        raise ValueError(f"vocab files that generate no enumeration: {missing}")
    return E


def _status_pattern(values) -> str:
    """One anchored alternation: literal notations plus each item's own pattern (CR-DE-001 #4)."""
    alts = []
    for v in values:
        if v.get("pattern"):
            alts.append(v["pattern"].lstrip("^").rstrip("$"))
        else:
            alts.append(re.escape(v["notation"]))
    return "^(" + "|".join(alts) + ")$"


def _camel(snake: str) -> str:
    head, *rest = snake.split("_")
    return head + "".join(w[:1].upper() + w[1:] for w in rest)


def state_class_fields(vocab_dir: Path = L.VOCAB) -> dict:
    """StateClassRecord properties and MUST list from SL's minimal common fields (vocab/state_class_fields.yaml)."""
    d = L.load_yaml(vocab_dir / "state_class_fields.yaml")
    props, required = {}, []
    for f in d["fields"]:
        if f["field"] == "provenance":          # the common-base provenance object carries it
            continue
        name = _camel(f["field"])
        fmt = str(f.get("format", "")).strip().lower()
        ex = str(f.get("vocab_or_example", "")).strip()
        if fmt == "enum" and re.fullmatch(r"[a-z0-9-]+(\|[a-z0-9-]+)+", ex):
            schema = {"enum": ex.split("|")}
        elif fmt == "iso date":
            schema = {"$ref": "#/$defs/Date"}
        elif fmt == "number":
            schema = {"type": "number"}
        elif fmt == "enum list" and re.fullmatch(r"[a-z0-9-]+(\|[a-z0-9-]+)+", ex):
            schema = {"type": "array", "uniqueItems": True, "items": {"enum": ex.split("|")}}
        elif fmt.startswith("list") or fmt == "enum list":
            schema = {"type": "array"}
        elif fmt in ("record", "structured (from, to, ratio)"):
            schema = {"type": ["object", "array"]}
        elif fmt == "numbers":
            schema = {"type": ["array", "object"]}
        else:
            schema = {"type": ["string", "number", "boolean", "object", "array"]}
        schema["description"] = f"{f.get('definition', '')} [{f['requirement']}; vocab/state_class_fields.yaml]".strip()
        props[name] = schema
        if f["requirement"] == "MUST":
            required.append(name)
    return {"type": "object", "required": required, "properties": props}


def build_schema(vocab_dir: Path = L.VOCAB, src: Path = L.SCHEMA_SRC) -> dict:
    s = L.load_yaml(src)
    enums = generate_enums(vocab_dir)
    defs = s["$defs"]
    for name, e in enums.items():
        defs[name] = {"enum": e["enum"], "$comment": f"GENERATED from vocab/{e['source']}"}
    idf = L.load_yaml(vocab_dir / "identifiers.yaml")
    defs["EmstId"] = {
        "type": "string",
        "description": "Persistent EMST ID (ADR-0010): emst:<namespace>/<TYPE>-<6 Crockford base32><Luhn mod-32 check>. "
                       "The check symbol is verified by scripts/validate_v2.py.",
        "pattern": idf["form"]["regex"],
        "$comment": "GENERATED from vocab/identifiers.yaml#form.regex",
    }
    for name, (fname, key) in {"SeriesStatus": ("mapping_predicates.yaml", "series_statuses"),
                               "SourceStatus": ("evidence_labels.yaml", "source_statuses")}.items():
        defs[name] = {"type": "string", "pattern": _status_pattern(L.load_yaml(vocab_dir / fname)[key]["values"]),
                      "$comment": f"GENERATED from vocab/{fname}#{key}"}
    defs["SignpostRef"] = {"enum": ["vocab:scenarios#" + x for x in enums["v_signpost"]["enum"]],
                           "$comment": "GENERATED from vocab/scenarios.yaml#signposts"}
    scf = state_class_fields(vocab_dir)
    scf["$comment"] = "GENERATED from vocab/state_class_fields.yaml#fields"
    defs["StateClassFields"] = scf
    # dispatcher: one if/then per entity type; every entity kind must have a $def
    types = enums["v_entityType"]["enum"]
    missing = [t for t in types if t not in defs]
    if missing:
        raise ValueError(f"entity kinds in vocab without a schema $def: {missing}")
    s["allOf"] = [{"if": {"properties": {"type": {"const": t}}, "required": ["type"]}, "then": {"$ref": f"#/$defs/{t}"}}
                  for t in types]
    # fixed key order: header, then dispatcher, then $defs (structural first, generated after, sorted)
    out = {k: s[k] for k in ("$schema", "$id", "title", "description", "type", "required", "properties")}
    out["$comment"] = ("GENERATED by scripts/build_schema.py from schema/src/emst.schema.src.yaml and vocab/*.yaml. "
                       "Do not edit; run the script. Schema version " + L.SCHEMA_VERSION + ".")
    out["allOf"] = s["allOf"]
    gen_names = ("EmstId", "StateClassFields", "SeriesStatus", "SourceStatus", "SignpostRef")
    structural = {k: v for k, v in defs.items() if not k.startswith("v_") and k not in gen_names}
    generated = {k: defs[k] for k in sorted(k for k in defs if k.startswith("v_") or k in gen_names)}
    out["$defs"] = {**structural, **generated}
    return out


# ---------------------------------------------------------------------------------------------------------------
# JSON-LD context (SPEC §17.1: field names = context terms)
# ---------------------------------------------------------------------------------------------------------------

PREFIXES = {
    "emst": "https://w3id.org/emst/", "emstv": "https://w3id.org/emst/vocab#", "emstagent": "https://w3id.org/emst/agent/",
    "seed": "https://w3id.org/emst/seed/", "EMSTv1": "https://w3id.org/emst/v1/",
    "skos": "http://www.w3.org/2004/02/skos/core#", "dct": "http://purl.org/dc/terms/", "prov": "http://www.w3.org/ns/prov#",
    "schema": "https://schema.org/", "owl": "http://www.w3.org/2002/07/owl#", "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#", "sssom": "https://w3id.org/sssom/", "semapv": "https://w3id.org/semapv/vocab/",
    "ceasn": "https://purl.org/ctdlasn/terms/", "ceterms": "https://purl.org/ctdl/terms/",
}
# Terms whose IRIs follow IA's draft context (docs/research/interop-skills-intelligence/emst.context.jsonld).
FIXED_IRIS = {
    "prefLabel": "skos:prefLabel", "altLabel": "skos:altLabel", "definition": "skos:definition", "scopeNote": "skos:scopeNote",
    "editorialNote": "skos:editorialNote", "notation": "emstv:notation", "scheme": "emstv:notationScheme", "value": "skos:notation",
    "inScheme": "skos:inScheme", "broader": "skos:broader", "replaces": "dct:replaces", "replacedBy": "dct:isReplacedBy",
    "changeNote": "skos:changeNote", "license": "dct:license", "provenance": "emstv:provenance", "agent": "prov:wasAttributedTo",
    "generatedAt": "prov:generatedAtTime", "derivedFrom": "prov:wasDerivedFrom", "sources": "dct:source", "confidence": "sssom:confidence",
    "publisher": "dct:publisher", "rights": "dct:rights", "url": "schema:url", "note": "skos:note", "jurisdiction": "dct:spatial",
    "observedPeriod": "dct:temporal", "versionIntroduced": "emstv:firstRelease", "lastChangedIn": "emstv:lastChangedRelease",
}
JSON_BLOBS = {"v1Values", "v1Seed", "measure", "corpus", "linkerQuality", "externalSource", "interRaterAgreement", "schemeAttributes",
              "scenarioSensitivity", "targetLevels", "values", "levelSpan", "publicationRuleChecks", "durationAndCost",
              "issuerVerified", "reproductionRegime", "learningDesign", "protect", "observedPeriod", "comparisonPeriod",
              "hypothesizedEntity", "indicativeGradeOrBand", "accountabilityConstraint", "signOffAuthority", "v1Domain", "v1SkillArea"}
SSSOM_TERMS = ["record_id", "subject_id", "subject_label", "subject_source", "subject_source_version", "predicate_id",
               "predicate_modifier", "object_id", "object_label", "object_source", "object_source_version",
               "mapping_justification", "similarity_score", "similarity_measure", "author_id", "reviewer_id",
               "reviewer_agreement", "mapping_date", "mapping_set_id", "comment"]


def _shape(sch, defs, depth=0):
    """Classify a property schema: lang | ref | refset | date | datetime | bool | num | int | list | obj | str."""
    if depth > 6 or not isinstance(sch, dict):
        return "str"
    if "$ref" in sch:
        name = sch["$ref"].split("/")[-1]
        if name in ("LangMap", "LangMapMulti", "Text"):
            return "lang"
        if name in ("RecordRef", "EmstId", "SeedKey", "AnyRef"):
            return "ref"
        if name == "RefList":
            return "refset"
        if name == "Date":
            return "date"
        if name == "DateTime":
            return "datetime"
        return _shape(defs.get(name, {}), defs, depth + 1)
    if "allOf" in sch:
        return _shape(sch["allOf"][0], defs, depth + 1)
    t = sch.get("type")
    if t == "boolean" or sch.get("const") is False:
        return "bool"
    if t == "integer":
        return "int"
    if t == "number":
        return "num"
    if t == "array":
        inner = _shape(sch.get("items", {}), defs, depth + 1)
        return "refset" if inner == "ref" else "list"
    if t == "object":
        return "obj"
    return "str"


def build_context(schema: dict) -> dict:
    defs = schema["$defs"]
    terms: dict[str, dict] = {}

    shapes: dict[str, set] = {}

    def visit(props):
        for name, sch in props.items():
            if name in ("type", "id"):
                continue
            shapes.setdefault(name, set()).add(_shape(sch, defs))

    def collect(sch, depth=0):
        if depth > 8 or not isinstance(sch, dict):
            return
        if "properties" in sch:
            visit(sch["properties"])
            for v in sch["properties"].values():
                collect(v, depth + 1)
        for key in ("items", "additionalProperties"):
            if isinstance(sch.get(key), dict):
                collect(sch[key], depth + 1)
        for key in ("allOf", "anyOf", "oneOf"):
            for sub in sch.get(key, []) or []:
                collect(sub, depth + 1)
        for key in ("then", "else"):
            if isinstance(sch.get(key), dict):
                collect(sch[key], depth + 1)

    for name in sorted(defs):
        if name == "Mapping":
            continue
        collect(defs[name])
    # one mapping per term from all the shapes it takes; conflicting shapes give a plain term
    for name in sorted(shapes):
        sh = {x for x in shapes[name] if x != "obj"} or {"obj"}
        if sh <= {"lang", "str"} and "lang" in sh:
            sh = {"lang"}
        shape = sh.pop() if len(sh) == 1 else "plain"
        t = {"@id": FIXED_IRIS.get(name, f"emstv:{name}")}
        if name in JSON_BLOBS:
            t["@type"] = "@json"
        elif shape == "lang":
            t["@container"] = "@language"
        elif shape == "ref":
            t["@type"] = "@id"
        elif shape == "refset":
            t["@type"] = "@id"
            t["@container"] = "@set"
        elif shape == "date":
            t["@type"] = "xsd:date"
        elif shape == "datetime":
            t["@type"] = "xsd:dateTime"
        elif shape == "bool":
            t["@type"] = "xsd:boolean"
        elif shape == "int":
            t["@type"] = "xsd:integer"
        elif shape == "num":
            t["@type"] = "xsd:double"
        elif shape == "list":
            t["@container"] = "@set"
        terms[name] = t
    ctx = {"@version": 1.1, **PREFIXES, "id": "@id", "type": "@type"}
    for t in schema["$defs"]["v_entityType"]["enum"]:
        ctx[t] = "sssom:Mapping" if t == "Mapping" else f"emstv:{t}"
    for name in sorted(terms):
        ctx[name] = terms[name]
    for name in SSSOM_TERMS:
        iri = {"subject_id": "owl:annotatedSource", "predicate_id": "owl:annotatedProperty",
               "object_id": "owl:annotatedTarget", "comment": "rdfs:comment"}.get(name, f"sssom:{name}")
        term = {"@id": iri}
        if name in ("subject_id", "predicate_id", "object_id", "mapping_justification", "object_source", "subject_source",
                    "mapping_set_id"):
            term["@type"] = "@id"
        if name in ("author_id", "reviewer_id"):
            term["@container"] = "@set"
        if name in ("confidence", "similarity_score", "reviewer_agreement"):
            term["@type"] = "xsd:double"
        ctx[name] = term
    ctx["confidence"] = {"@id": "sssom:confidence"}
    for k in ("emst_version", "schema_version", "released", "graph_license"):
        pass
    ctx["emstRelease"] = {"@id": "owl:versionInfo"}
    ctx["schemaVersion"] = {"@id": "dct:conformsTo"}
    ctx["released"] = {"@id": "dct:issued", "@type": "xsd:date"}
    ctx["Release"] = "emstv:Release"
    ctx["notice"] = {"@id": "emstv:notice"}
    ctx["indigenousKnowledgeStatement"] = {"@id": "emstv:indigenousKnowledgeStatement"}
    ctx["buildCommit"] = {"@id": "emstv:buildCommit"}
    ctx["license"] = {"@id": "dct:license", "@type": "@id"}
    return {"@context": ctx}


def render(vocab_dir: Path = L.VOCAB) -> tuple[str, str]:
    schema = build_schema(vocab_dir)
    return L.dump_json(schema), L.dump_json(build_context(schema))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="fail if committed outputs are stale")
    ap.add_argument("--list", action="store_true", help="list generated enumerations")
    args = ap.parse_args(argv)
    if args.list:
        for name, e in generate_enums().items():
            print(f"{name:32} {len(e['enum']):3}  vocab/{e['source']}")
        return 0
    schema_txt, ctx_txt = render()
    if args.check:
        bad = []
        for path, txt in ((L.SCHEMA_OUT, schema_txt), (L.CONTEXT_OUT, ctx_txt)):
            if not path.exists() or path.read_text(encoding="utf-8") != txt:
                bad.append(str(path.relative_to(L.ROOT)))
        if bad:
            print("STALE (run python scripts/build_schema.py): " + ", ".join(bad))
            return 1
        print("schema and context are current with vocab/")
        return 0
    L.SCHEMA_OUT.write_text(schema_txt, encoding="utf-8")
    L.CONTEXT_OUT.write_text(ctx_txt, encoding="utf-8")
    print(f"wrote {L.SCHEMA_OUT.relative_to(L.ROOT)} and {L.CONTEXT_OUT.relative_to(L.ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
