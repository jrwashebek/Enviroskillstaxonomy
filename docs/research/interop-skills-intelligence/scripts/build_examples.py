#!/usr/bin/env python3
"""Build worked examples of the draft EMST v2 model for v1 competencies 2.1.1 and 6.1.2, in every export profile.

Inputs: data/v1_baseline (DE), crosswalks/*.reviewed.sssom.tsv (IA), prototype/outputs/era_shift_by_competency.csv (IA).
Outputs: examples/ (native JSON-LD bundle, SKOS Turtle, CASE 1.1 package, CTDL-ASN JSON-LD, RSD JSON, OB3 alignment,
CSV bundle with Frictionless datapackage.json). Deterministic.  Usage: python scripts/build_examples.py
"""
import csv
import hashlib
import json
import uuid
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]          # .../interop-skills-intelligence
EMST = ROOT.parents[2]
V1 = EMST / "data" / "v1_baseline"
EX = ROOT / "examples"
EX.mkdir(exist_ok=True)
CODES = ["2.1.1", "6.1.2"]
RELEASE = "2.0.0-draft.1"
NOW = "2026-10-23T00:00:00Z"
CONTEXT_URL = "https://w3id.org/emst/context/v2/emst.context.jsonld"
CROCK = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def luhn32(body):
    """Luhn mod-32 check character over the Crockford alphabet (catches all single-symbol errors and most transpositions)."""
    factor, total = 2, 0
    for ch in reversed(body):
        addend = factor * CROCK.index(ch)
        factor = 1 if factor == 2 else 2
        total += addend // 32 + addend % 32
    return CROCK[(32 - total % 32) % 32]
UUID_NS = uuid.uuid5(uuid.NAMESPACE_URL, "https://w3id.org/emst/")


def mint(namespace, typ, seed):
    """Deterministic migration ID: 30 bits of SHA-256(seed) -> 6 Crockford base32 symbols + Luhn mod-32 check symbol.
    Used ONCE at migration; the result is frozen in the ID registry and never recomputed (new concepts get random IDs)."""
    n = int.from_bytes(hashlib.sha256(seed.encode()).digest()[:4], "big") >> 2
    body = "".join(CROCK[(n >> (5 * i)) & 31] for i in reversed(range(6)))
    return f"emst:{namespace}/{typ}-{body}{luhn32(body)}"


def iri(cid):
    return "https://w3id.org/emst/" + cid.split(":", 1)[1]


def uid(cid):
    return str(uuid.uuid5(UUID_NS, iri(cid)))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


comp = pd.read_csv(V1 / "competencies.csv", dtype=str, keep_default_na=False).set_index("code")
tasks = pd.read_csv(V1 / "tasks.csv", dtype=str, keep_default_na=False)
prof = pd.read_csv(V1 / "proficiency.csv", dtype=str, keep_default_na=False)
ind = pd.read_csv(V1 / "indicators.csv", dtype=str, keep_default_na=False)
csr = pd.read_csv(V1 / "craft_stage_reform.csv", dtype=str, keep_default_na=False).set_index("code")
fam = pd.read_csv(V1 / "family_assignments.csv", dtype=str, keep_default_na=False)
sec = pd.read_csv(V1 / "sector_applications.csv", dtype=str, keep_default_na=False)
build = json.loads((V1 / "BUILD_INFO.json").read_text())
WB_SHA = next(i["sha256"] for i in build["inputs"] if i["role"] == "baseline")
rev = pd.read_csv(ROOT / "crosswalks" / "emst_v1_to_esco_skill.reviewed.sssom.tsv", sep="\t", comment="#", dtype=str, keep_default_na=False)
era_path = ROOT / "prototype" / "outputs" / "era_shift_by_competency.csv"
era = pd.read_csv(era_path, dtype=str).set_index("code") if era_path.exists() else None
evalrep = json.loads((ROOT / "prototype" / "outputs" / "eval_report.json").read_text())
p1 = evalrep["evaluation"]["dev"]["acceptable"]["full:fused"]["p1"]


def prov(method="v1-migration", ev="J", conf=None, derived=None, review="unreviewed", agent=None, notes=None, sources=None):
    p = {"method": method, "generatedAt": NOW, "agent": agent or ["emstagent:ia-example-builder-0.1.0"], "evidenceLabel": ev, "reviewStatus": review}
    if conf is not None:
        p["confidence"] = conf
    if derived:
        p["derivedFrom"] = derived
    if notes:
        p["notes"] = notes
    if sources:
        p["sources"] = sources
    return p


CRAFT_VOC = {c: mint("core", "VOC", f"craft:{c}") for c in ["FC", "DC", "SC"]}
graph, mappings, flat = [], [], {"competencies": [], "tasks": [], "proficiency": [], "indicators": []}
for c, lbl in [("FC", "Field craft"), ("DC", "Data craft"), ("SC", "Statecraft")]:
    graph.append({"id": CRAFT_VOC[c], "type": "VocabularyTerm", "vocabulary": "craft", "layer": "L0", "status": "proposed", "version": "0.1.0",
                  "prefLabel": {"en": lbl}, "notation": [{"scheme": "EMSTv1-craft", "value": c}],
                  "provenance": prov(notes="Charter craft; v1 code kept as notation")})

for code in CODES:
    r = comp.loc[code]
    cid = mint("core", "CMP", f"emst-v1-migration:v1:{code}")
    title = r.suggested_title or r.title
    desc = r.description or (r.title[len(r.suggested_title):].strip() if r.suggested_title else "")
    k = csr.loc[code]
    anchors = []
    for lv in ["foundational", "intermediate", "advanced", "expert"]:
        pr = prof[(prof.code == code) & (prof.level == lv)]
        ii = ind[(ind.code == code) & (ind.level == lv)].sort_values("indicator_n")
        a = {"level": f"EMSTv1level:{lv}", "practicedAtLevel": True,
             "indicators": [{"id": mint("core", "IND", f"emst-v1-migration:{x.key}"), "statement": {"en": x.text},
                             "provenance": prov(derived=[{"v1Key": x.key, "sheet": "Proficiency Indicators", "row": int(x.source_row), "workbookSha256": WB_SHA}])}
                            for x in ii.itertuples()]}
        if len(pr):
            a["knowledge"] = {"en": pr.iloc[0].knowledge}
            a["application"] = {"en": pr.iloc[0].application}
            flat["proficiency"].append({"competency_id": cid, "level": lv, "knowledge_en": pr.iloc[0].knowledge, "application_en": pr.iloc[0].application})
        for x in ii.itertuples():
            flat["indicators"].append({"indicator_id": mint("core", "IND", f"emst-v1-migration:{x.key}"), "competency_id": cid, "level": lv, "statement_en": x.text, "v1_key": x.key})
        anchors.append(a)
    fams = [{"family": f"EMSTv1fam:{x.family_code}", "relevance": x.assignment.lower()} for x in fam[fam.code == code].itertuples()]
    enact = [{"sectorActor": f"EMSTv1:sector/{x.sector}", "note": {"en": x.text},
              "provenance": prov(notes="v1 sector application note; v1 sectors do not match the seven v2 sector actors and must be re-derived")}
             for x in sec[sec.code == code].itertuples()]
    c_rec = {
        "id": cid, "type": "Competency", "layer": "L1", "module": "core", "competencyType": "core",
        "prefLabel": {"en": title}, "statement": {"en": desc}, "definition": {"en": desc},
        "notation": [{"scheme": "EMSTv1", "value": code}],
        "inScheme": ["emst:core/MST-0000000"] if False else [],
        "status": "proposed", "version": "0.1.0", "firstRelease": RELEASE, "lastChangedRelease": RELEASE,
        "craft": {"v1Primary": k.craft_primary, **({"v1Secondary": k.craft_secondary} if k.craft_secondary else {}),
                  "ordinal": {c: ("defining" if c == k.craft_primary else "supporting" if c == k.craft_secondary else "none") for c in ["FC", "DC", "SC"]},
                  "computed": False, "provenance": prov(ev="J", notes="v1 single-analyst irreducibility tag mapped to ordinal fallback; to be re-elicited at task level (CA DP-5)")},
        "proficiency": anchors, "families": fams, "enactments": enact,
        "changeNote": [{"release": RELEASE, "change": "retained", "note": "Migrated from v1 with lineage; content not yet revalidated"}],
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "provenance": prov(derived=[{"v1Key": r.key, "v1Code": code, "sheet": r.source_sheet, "row": int(r.source_row), "workbookSha256": WB_SHA}],
                           notes=("v1 qa_flags: " + r.qa_flags) if r.qa_flags else None),
    }
    c_rec.pop("inScheme")
    graph.append(c_rec)
    flat["competencies"].append({"competency_id": cid, "uri": iri(cid), "v1_code": code, "pref_label_en": title, "statement_en": desc,
                                 "layer": "L1", "module": "core", "status": "proposed", "version": "0.1.0",
                                 "craft_v1_primary": k.craft_primary, "craft_v1_secondary": k.craft_secondary,
                                 "case_uuid": uid(cid), "ctid": "ce-" + uid(cid), "prov_method": "v1-migration", "prov_v1_key": r.key,
                                 "prov_workbook_sha256": WB_SHA})
    for t in tasks[tasks.code == code].sort_values("task_n").itertuples():
        tid = mint("core", "TSK", f"emst-v1-migration:{t.key}")
        graph.append({"id": tid, "type": "Task", "layer": "L2", "module": "core", "prefLabel": {"en": t.text}, "statement": {"en": t.text},
                      "notation": [{"scheme": "EMSTv1-task", "value": t.key.replace("v1:", "")}], "v1Tier": f"T{t.task_n}",
                      "supports": [{"competency": cid, "strength": "defining"}], "status": "proposed", "version": "0.1.0",
                      "provenance": prov(derived=[{"v1Key": t.key, "sheet": "Competencies", "row": int(t.source_row_text), "workbookSha256": WB_SHA}])})
        aid = mint("core", "ASM", f"emst-v1-migration:{t.key}:task13")
        graph.append({"id": aid, "type": "ExposureAssessment", "layer": "L5", "task": tid, "instrument": "emst-v1-task13",
                      "values": {"autoType": t.auto_type, "tacitDensity": t.tacit_density, "careerLadder": t.career_ladder, "vector": t.vector, "horizon": t.horizon},
                      "assessedAt": "2026-02-23", "prefLabel": {"en": f"v1 Task 13 exposure for {t.key}"}, "status": "active", "version": "1.0.0",
                      "provenance": prov(ev="J", derived=[{"v1Key": t.key, "sheet": "Dimension Tags", "row": int(t.source_row_exposure), "workbookSha256": WB_SHA, "v1ProvenanceCode": t.exposure_provenance}],
                                         notes="Single analyst with LLM; no inter-rater reliability (CA audit)")})
        flat["tasks"].append({"task_id": tid, "competency_id": cid, "v1_key": t.key, "tier": f"T{t.task_n}", "statement_en": t.text,
                              "v1_auto_type": t.auto_type, "v1_horizon": t.horizon})
    for m in rev[(rev.subject_id == f"EMSTv1:{code}")].itertuples():
        rec = {"type": "Mapping", "record_id": m.record_id, "subject_id": cid, "subject_label": title, "predicate_id": m.predicate_id,
               "object_id": m.object_id, "object_label": m.object_label, "object_source": "http://data.europa.eu/esco",
               "object_source_version": "v1.2.0 (inferred)", "mapping_justification": m.mapping_justification,
               "confidence": float(m.confidence), "author_id": [m.author_id], "reviewer_id": [m.reviewer_id] if m.reviewer_id else [],
               "mapping_date": m.mapping_date, "review_date": m.review_date, "review_status": m.review_status, "comment": m.comment}
        if m.predicate_modifier:
            rec["predicate_modifier"] = m.predicate_modifier
        if m.similarity_score:
            rec["similarity_score"] = float(m.similarity_score)
            rec["similarity_measure"] = m.similarity_measure
        mappings.append(rec)
    if era is not None and code in era.index:
        e = era.loc[code]
        graph.append({"id": mint("core", "SIG", f"lmps-era:{code}"), "type": "ChangeSignal", "layer": "L5", "signalType": "plan-requirement",
                      "prefLabel": {"en": f"Share of USFS binding plan direction linked to {code}: 2012-rule vs 1982-rule plans"},
                      "about": [cid], "sectorActor": ["EMSTv1:sector/public_agencies"], "jurisdiction": ["https://w3id.org/emst/ext/jurisdiction/US-federal"],
                      "observedPeriod": {"start": "2012", "end": "2026"}, "comparisonPeriod": {"start": "1982", "end": "2011"},
                      "measure": {"name": "delta share of linked binding components (top-1)", "value": float(e.delta), "unit": "proportion",
                                  "ci95": [float(e.ci95_lo), float(e.ci95_hi)], "denominator": "linked standards/guidelines in USFS plans by planning rule"},
                      "direction": "unclear" if not (float(e.ci95_lo) > 0 or float(e.ci95_hi) < 0) else ("increase" if float(e.delta) > 0 else "decrease"),
                      "linkerQuality": {"goldSet": "IA dev gold v0.1 (single AI annotator)", "precisionAt1": p1["mean"], "ci95": p1["ci95"]},
                      "corpus": {"name": "OpenLMP plan components", "version": "0.1.0", "license": "see /home/claude/lmps/LICENSE-DATA"},
                      "caveats": ["Planning-rule era confounds plan format and extraction method with real change", "Linker top-1 precision about 0.5; small shifts are noise"],
                      "status": "proposed", "version": "0.1.0",
                      "provenance": prov(method="lexical-linker", ev="S", agent=["emstagent:ia-prototype-0.1.0"], notes="Demonstration of the L5 record shape, not a finding")})
    if code == "2.1.1":
        mappings.append({"type": "Mapping", "record_id": "emst-v2-onetsoc:15-1299.02:2.1.1", "subject_id": "ONETSOC:15-1299.02",
                         "subject_label": "Geographic Information Systems Technologists and Technicians", "predicate_id": "emst:requiresCompetency",
                         "object_id": cid, "object_label": title, "object_source": "https://www.onetcenter.org/taxonomy.html", "object_source_version": "O*NET-SOC 2019 (O*NET 31.0)",
                         "mapping_justification": "semapv:LLMBasedMatching", "confidence": 0.6, "author_id": ["emstagent:claude-in-session-IA"],
                         "mapping_date": "2026-10-23", "review_status": "candidate",
                         "comment": "Illustrative role-to-competency link; O*NET code verified in ESCO-O*NET crosswalk file; requires FH/LM review"})

graph.extend(mappings)
bundle = {"@context": CONTEXT_URL, "emst_version": RELEASE, "schema_version": "0.1.0", "released": "2026-10-23",
          "layer_versions": {"L0": "0.1.0", "L1": "0.1.0", "L2": "0.1.0", "L5": "0.1.0", "L6": "0.1.0"},
          "modules": [{"namespace": "core", "steward": "EMST core editorial board (proposed)", "version": "0.1.0"}],
          "license": "https://creativecommons.org/licenses/by/4.0/", "@graph": graph}
(EX / "emst-v2.bundle.example.jsonld").write_text(json.dumps(bundle, indent=1, ensure_ascii=False))

# ---------------- CSV bundle (Frictionless Data Package) ----------------
cb = EX / "csv_bundle"
cb.mkdir(exist_ok=True)
resources = []
for name, rows in flat.items():
    df = pd.DataFrame(rows)
    df.to_csv(cb / f"{name}.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    resources.append({"name": name, "path": f"{name}.csv", "format": "csv", "schema": {"fields": [{"name": c, "type": "string"} for c in df.columns],
                      "primaryKey": [df.columns[0]] if name in ("competencies", "tasks", "indicators") else ["competency_id", "level"]}})
mdf = pd.DataFrame([{k: (";".join(v) if isinstance(v, list) else v) for k, v in m.items() if k != "type"} for m in mappings])
with open(cb / "mappings.sssom.tsv", "w") as f:
    f.write("# curie_map:\n#   emst: https://w3id.org/emst/\n#   ESCO: http://data.europa.eu/esco/skill/\n#   ONETSOC: https://w3id.org/emst/ext/onet-soc/\n#   skos: http://www.w3.org/2004/02/skos/core#\n#   semapv: https://w3id.org/semapv/vocab/\n#   emstagent: https://w3id.org/emst/agent/\n")
    f.write("# mapping_set_id: https://w3id.org/emst/mappings/example/0.1.0\n# license: https://creativecommons.org/licenses/by/4.0/\n")
    mdf.to_csv(f, sep="\t", index=False)
resources.append({"name": "mappings", "path": "mappings.sssom.tsv", "format": "tsv", "description": "SSSOM/TSV with YAML header"})
(cb / "datapackage.json").write_text(json.dumps({"name": "emst-v2-example", "version": RELEASE, "licenses": [{"name": "CC-BY-4.0"}],
                                                  "profile": "data-package", "resources": resources}, indent=1))

# ---------------- CASE 1.1 package ----------------
doc_uuid = str(uuid.uuid5(UUID_NS, "https://w3id.org/emst/framework/core"))
case = {"CFDocument": {"identifier": doc_uuid, "uri": "https://w3id.org/emst/case/v1p1/CFDocuments/" + doc_uuid, "creator": "EMST (proposed steward)",
                       "title": "Environmental Management Skills Taxonomy — core (example)", "lastChangeDateTime": NOW, "version": RELEASE,
                       "adoptionStatus": "Draft", "language": "en", "licenseURI": {"title": "CC BY 4.0", "identifier": str(uuid.uuid5(UUID_NS, "lic:cc-by-4.0")), "uri": "https://creativecommons.org/licenses/by/4.0/"},
                       "frameworkType": "Competencies", "caseVersion": "1.1",
                       "notes": "Generated from the EMST v2 native bundle. CASE identifiers are UUIDv5 of the EMST IRI, so they are stable and reproducible."},
        "CFItems": [], "CFAssociations": [], "CFDefinitions": {"CFItemTypes": [
            {"identifier": str(uuid.uuid5(UUID_NS, "itemtype:Competency")), "uri": "https://w3id.org/emst/case/itemtype/Competency", "title": "Competency", "typeCode": "Competency", "hierarchyCode": "1", "lastChangeDateTime": NOW},
            {"identifier": str(uuid.uuid5(UUID_NS, "itemtype:Task")), "uri": "https://w3id.org/emst/case/itemtype/Task", "title": "Task", "typeCode": "Task", "hierarchyCode": "2", "lastChangeDateTime": NOW}]}}
ASSOC = {"skos:exactMatch": "exactMatchOf", "skos:closeMatch": "isRelatedTo", "skos:broadMatch": "isRelatedTo", "skos:narrowMatch": "isRelatedTo", "skos:relatedMatch": "isRelatedTo"}
docref = {"title": case["CFDocument"]["title"], "identifier": doc_uuid, "uri": case["CFDocument"]["uri"]}
for e in graph:
    if e["type"] not in ("Competency", "Task"):
        continue
    it = {"identifier": uid(e["id"]), "uri": iri(e["id"]), "fullStatement": e["statement"]["en"] if e["type"] == "Task" else e["prefLabel"]["en"] + ". " + e["statement"]["en"],
          "abbreviatedStatement": e["prefLabel"]["en"][:60], "CFItemType": e["type"], "humanCodingScheme": e["notation"][0]["value"],
          "language": "en", "lastChangeDateTime": NOW, "CFDocumentURI": docref,
          "notes": f"EMST id {e['id']}; status {e['status']}; version {e['version']}"}
    case["CFItems"].append(it)
    if e["type"] == "Task":
        par = e["supports"][0]["competency"]
        case["CFAssociations"].append({"identifier": str(uuid.uuid5(UUID_NS, e["id"] + "|isChildOf|" + par)), "uri": "https://w3id.org/emst/case/assoc/" + str(uuid.uuid5(UUID_NS, e["id"] + "|isChildOf|" + par)),
                                       "associationType": "isChildOf", "originNodeURI": {"title": e["prefLabel"]["en"][:60], "identifier": uid(e["id"]), "uri": iri(e["id"])},
                                       "destinationNodeURI": {"title": "competency", "identifier": uid(par), "uri": iri(par)}, "lastChangeDateTime": NOW, "CFDocumentURI": docref})
for m in mappings:
    if m["review_status"] != "accepted" or m.get("predicate_modifier") == "Not" or not m["subject_id"].startswith("emst:") or m["object_id"] == "sssom:NoTermFound":
        continue
    esco_uri = "http://data.europa.eu/esco/skill/" + m["object_id"].split(":", 1)[1]
    aid = str(uuid.uuid5(UUID_NS, m["record_id"]))
    case["CFAssociations"].append({"identifier": aid, "uri": "https://w3id.org/emst/case/assoc/" + aid, "associationType": ASSOC[m["predicate_id"]],
                                   "originNodeURI": {"title": m["subject_label"][:60], "identifier": uid(m["subject_id"]), "uri": iri(m["subject_id"])},
                                   "destinationNodeURI": {"title": m["object_label"], "identifier": m["object_id"].split(":", 1)[1], "uri": esco_uri, "targetType": "ESCO"},
                                   "notes": f"SKOS {m['predicate_id']} (confidence {m['confidence']}); CASE has no close/broad/narrow types, so precision is lost", "lastChangeDateTime": NOW, "CFDocumentURI": docref})
(EX / "emst-v2.case-1.1.example.json").write_text(json.dumps(case, indent=1, ensure_ascii=False))

# ---------------- CTDL-ASN ----------------
ALIGN = {"skos:exactMatch": "ceasn:exactAlignment", "skos:closeMatch": "ceasn:majorAlignment", "skos:broadMatch": "ceasn:broadAlignment",
         "skos:narrowMatch": "ceasn:narrowAlignment", "skos:relatedMatch": "ceasn:minorAlignment"}
fw_id = "https://w3id.org/emst/framework/core"
ctdl = {"@context": "https://credreg.net/ctdlasn/schema/context/json", "@graph": [{
    "@id": fw_id, "@type": "ceasn:CompetencyFramework", "ceterms:ctid": "ce-" + doc_uuid, "ceasn:name": {"en-us": "Environmental Management Skills Taxonomy — core (example)"},
    "ceasn:description": {"en-us": "Example export of the EMST v2 draft model."}, "ceasn:inLanguage": ["en-US"], "ceasn:license": "https://creativecommons.org/licenses/by/4.0/",
    "ceasn:publicationStatusType": "http://purl.org/ASN/scheme/ASNPublicationStatus/Draft", "ceasn:hasTopChild": [], "ceasn:dateModified": NOW[:10]}]}
for e in graph:
    if e["type"] != "Competency":
        continue
    ctdl["@graph"][0]["ceasn:hasTopChild"].append(iri(e["id"]))
    node = {"@id": iri(e["id"]), "@type": "ceasn:Competency", "ceterms:ctid": "ce-" + uid(e["id"]), "ceasn:competencyLabel": {"en-us": e["prefLabel"]["en"]},
            "ceasn:competencyText": {"en-us": e["statement"]["en"]}, "ceasn:codedNotation": e["notation"][0]["value"], "ceasn:isPartOf": fw_id, "ceasn:isTopChildOf": fw_id,
            "ceasn:inLanguage": ["en-US"], "ceasn:dateModified": NOW[:10], "ceasn:comment": {"en-us": [f"EMST id {e['id']} (status {e['status']})"]}}
    for m in mappings:
        if m["subject_id"] == e["id"] and m["review_status"] == "accepted" and m.get("predicate_modifier") != "Not" and m["object_id"].startswith("ESCO:"):
            node.setdefault(ALIGN[m["predicate_id"]], []).append("http://data.europa.eu/esco/skill/" + m["object_id"].split(":", 1)[1])
        if m["object_id"] == e["id"] and m["subject_id"].startswith("ONETSOC:"):
            node.setdefault("ceterms:occupationType", []).append({"@type": "ceterms:CredentialAlignmentObject", "ceterms:frameworkName": {"en-us": "O*NET-SOC 2019"},
                                                                 "ceterms:codedNotation": m["subject_id"].split(":", 1)[1], "ceterms:targetNodeName": {"en-us": m["subject_label"]}})
    ctdl["@graph"].append(node)
(EX / "emst-v2.ctdl-asn.example.jsonld").write_text(json.dumps(ctdl, indent=1, ensure_ascii=False))

# ---------------- RSD (OSMT API v2 shape) ----------------
rsds = []
for e in graph:
    if e["type"] != "Competency":
        continue
    rsds.append({"@context": "https://rsd.openskillsnetwork.org/context-v1.json", "type": "RichSkillDescriptor", "id": iri(e["id"]), "uuid": uid(e["id"]),
                 "status": "draft", "skillName": e["prefLabel"]["en"], "skillStatement": e["statement"]["en"],
                 "category": comp.loc[e["notation"][0]["value"]].skill_area_name.title(), "author": "Environmental Management Skills Taxonomy (EMST)",
                 "keywords": [e["notation"][0]["value"]], "standards": [{"skillName": "EMSTv1 " + e["notation"][0]["value"]}],
                 "alignments": [{"id": "http://data.europa.eu/esco/skill/" + m["object_id"].split(":", 1)[1], "skillName": m["object_label"]}
                                for m in mappings if m["subject_id"] == e["id"] and m["review_status"] == "accepted" and m.get("predicate_modifier") != "Not"
                                and m["predicate_id"] in ("skos:exactMatch", "skos:closeMatch") and m["object_id"].startswith("ESCO:")],
                 "occupations": [{"code": m["subject_id"].split(":", 1)[1], "targetNodeName": m["subject_label"], "frameworkName": "o*net"}
                                 for m in mappings if m["object_id"] == e["id"] and m["subject_id"].startswith("ONETSOC:")],
                 "certifications": [], "employers": [], "collections": [], "publishDate": None, "archiveDate": None,
                 "creationDate": NOW, "updateDate": NOW})
(EX / "emst-v2.rsd.example.json").write_text(json.dumps(rsds, indent=1, ensure_ascii=False))

# ---------------- Open Badges 3.0 Achievement alignment ----------------
c0 = next(e for e in graph if e["type"] == "Competency")
ob = {"note": "Fragment: the 'achievement' object of an OpenBadgeCredential (OB 3.0) whose alignment points at an EMST competency via its CTDL-ASN and CASE renderings.",
      "achievement": {"id": "https://example.org/achievements/gis-field-mapping-microcredential", "type": ["Achievement"], "name": "GIS for field mapping (example microcredential)",
                      "criteria": {"narrative": "Assessed work sample against EMST indicators at the intermediate level."},
                      "alignment": [{"type": ["Alignment"], "targetName": c0["prefLabel"]["en"], "targetUrl": iri(c0["id"]), "targetCode": c0["notation"][0]["value"],
                                     "targetFramework": "Environmental Management Skills Taxonomy", "targetType": "ceasn:Competency"},
                                    {"type": ["Alignment"], "targetName": c0["prefLabel"]["en"], "targetUrl": iri(c0["id"]), "targetCode": uid(c0["id"]),
                                     "targetFramework": "Environmental Management Skills Taxonomy (CASE)", "targetType": "CFItem"}]}}
(EX / "ob3-alignment.example.json").write_text(json.dumps(ob, indent=1, ensure_ascii=False))

# ---------------- SKOS profile (Turtle) ----------------
from rdflib import Graph, Literal, Namespace, URIRef  # noqa: E402
from rdflib.namespace import DCTERMS, OWL, RDF, SKOS  # noqa: E402

g = Graph()
EM = Namespace("https://w3id.org/emst/")
EV = Namespace("https://w3id.org/emst/vocab#")
g.bind("skos", SKOS); g.bind("dct", DCTERMS); g.bind("emst", EM); g.bind("emstv", EV); g.bind("owl", OWL)
scheme = URIRef("https://w3id.org/emst/core")
g.add((scheme, RDF.type, SKOS.ConceptScheme)); g.add((scheme, SKOS.prefLabel, Literal("EMST core competencies (example)", lang="en")))
g.add((scheme, OWL.versionInfo, Literal(RELEASE)))
tscheme = URIRef("https://w3id.org/emst/core/tasks")
g.add((tscheme, RDF.type, SKOS.ConceptScheme)); g.add((tscheme, SKOS.prefLabel, Literal("EMST core tasks (example)", lang="en")))
for e in graph:
    if e["type"] not in ("Competency", "Task"):
        continue
    s = URIRef(iri(e["id"]))
    g.add((s, RDF.type, SKOS.Concept))
    g.add((s, SKOS.inScheme, scheme if e["type"] == "Competency" else tscheme))
    g.add((s, SKOS.prefLabel, Literal(e["prefLabel"]["en"], lang="en")))
    g.add((s, SKOS.definition, Literal(e["statement"]["en"], lang="en")))
    g.add((s, SKOS.notation, Literal(e["notation"][0]["value"], datatype=EV["v1Code"])))
    g.add((s, EV.status, Literal(e["status"]))); g.add((s, OWL.versionInfo, Literal(e["version"])))
    if e["type"] == "Competency":
        g.add((s, SKOS.topConceptOf, scheme))
    else:
        g.add((s, SKOS.related, URIRef(iri(e["supports"][0]["competency"]))))
for m in mappings:
    if m["review_status"] == "accepted" and m.get("predicate_modifier") != "Not" and m["subject_id"].startswith("emst:") and m["object_id"].startswith("ESCO:"):
        pred = {"skos:exactMatch": SKOS.exactMatch, "skos:closeMatch": SKOS.closeMatch, "skos:broadMatch": SKOS.broadMatch,
                "skos:narrowMatch": SKOS.narrowMatch, "skos:relatedMatch": SKOS.relatedMatch}[m["predicate_id"]]
        g.add((URIRef(iri(m["subject_id"])), pred, URIRef("http://data.europa.eu/esco/skill/" + m["object_id"].split(":", 1)[1])))
(EX / "emst-v2.skos.example.ttl").write_text(g.serialize(format="turtle"))
print("examples written:", sorted(p.name for p in EX.iterdir()))
print({c: mint("core", "CMP", f"emst-v1-migration:v1:{c}") for c in CODES})
