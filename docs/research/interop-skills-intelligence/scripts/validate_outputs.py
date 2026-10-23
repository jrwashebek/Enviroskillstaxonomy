#!/usr/bin/env python3
"""Validate IA outputs: JSON Schema (meta + examples), JSON-LD context, Turtle, SSSOM files, CSV headers.
Usage: python scripts/validate_outputs.py   (exit code 1 on any failure)"""
import csv
import json
import sys
from pathlib import Path

import jsonschema
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
ok = True


def check(name, cond, detail=""):
    global ok
    print(("PASS " if cond else "FAIL ") + name + (f" — {detail}" if detail else ""))
    ok = ok and cond


schema = json.loads((ROOT / "emst-v2.schema.json").read_text())
try:
    Draft202012Validator.check_schema(schema)
    check("emst-v2.schema.json is a valid 2020-12 schema", True)
except jsonschema.SchemaError as e:
    check("emst-v2.schema.json is a valid 2020-12 schema", False, str(e)[:300])
v = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
bundle = json.loads((ROOT / "examples" / "emst-v2.bundle.example.jsonld").read_text())
errs = sorted(v.iter_errors(bundle), key=lambda e: list(e.path))
check("example bundle validates", not errs, "; ".join(f"{list(e.path)[:3]}: {e.message[:120]}" for e in errs[:5]))
# negative tests: the schema must reject bad records
bad = json.loads(json.dumps(bundle))
bad["@graph"][3]["id"] = "emst:core/CMP-1.1.1"          # v1 code as id
check("rejects v1 code used as id", any(True for _ in v.iter_errors(bad)))
bad = json.loads(json.dumps(bundle))
bad["@graph"][3]["status"] = "superseded"                # superseded without replacedBy
check("rejects superseded without replacedBy", any(True for _ in v.iter_errors(bad)))
bad = json.loads(json.dumps(bundle))
del bad["@graph"][3]["provenance"]
check("rejects record without provenance", any(True for _ in v.iter_errors(bad)))

# every EMST id carries a valid Luhn mod-32 check symbol, and ids are unique
import re as _re  # noqa: E402
CROCK = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def _luhn_ok(code):
    factor, total = 1, 0
    for ch in reversed(code):
        addend = factor * CROCK.index(ch)
        factor = 2 if factor == 1 else 1
        total += addend // 32 + addend % 32
    return total % 32 == 0


ids = _re.findall(r'"(emst:[a-z0-9-]+/[A-Z]{2,3}-([0-9A-Z]{7}))"', json.dumps(bundle))
bad_ck = sorted({i for i, c in ids if not _luhn_ok(c)})
check("all EMST ids pass the Luhn mod-32 check", not bad_ck and len(ids) > 0, ",".join(bad_ck[:5]))
graph_ids = [e["id"] for e in bundle["@graph"] if "id" in e]
check("entity ids are unique in the bundle", len(graph_ids) == len(set(graph_ids)), f"{len(graph_ids)} ids")

# JSON-LD: expand with the local context, then load into rdflib
from pyld import jsonld  # noqa: E402
ctx = json.loads((ROOT / "emst.context.jsonld").read_text())


def loader(url, options=None):
    if url.endswith("emst.context.jsonld"):
        return {"contentType": "application/ld+json", "contextUrl": None, "documentUrl": url, "document": ctx}
    raise RuntimeError("offline: " + url)


jsonld.set_document_loader(loader)
try:
    exp = jsonld.expand(bundle)
    nq = jsonld.to_rdf(exp, {"format": "application/n-quads"})
    n = len([l for l in nq.splitlines() if l.strip()])
    check("bundle expands with emst.context.jsonld (pyld)", n > 100, f"{n} triples")
    undefined = [l for l in nq.splitlines() if "@" in l.split(" ")[1]]
    from rdflib import Graph  # noqa: E402
    from rdflib import Dataset  # noqa: E402
    ds = Dataset()
    ds.parse(data=nq, format="nquads")
    nds = sum(1 for _ in ds.quads((None, None, None, None)))
    check("expanded bundle parses in rdflib", nds == n, f"{nds} quads")
except Exception as e:  # noqa: BLE001
    check("bundle expands with emst.context.jsonld (pyld)", False, str(e)[:300])
# terms used in the bundle that the context does not define would be dropped silently: detect them
used = set()


def walk(o):
    if isinstance(o, dict):
        for k, val in o.items():
            used.add(k)
            if k not in ("measure", "values", "weights", "ordinal", "observedPeriod", "comparisonPeriod", "linkerQuality", "corpus", "frictions", "exposureSummary"):
                walk(val)
    elif isinstance(o, list):
        for x in o:
            walk(x)


walk(bundle["@graph"])
langmaps = {"en"}
undefined = sorted(k for k in used - set(ctx["@context"]) - langmaps if not k.startswith("@"))
check("every bundle key is defined in the context", not undefined, ", ".join(undefined))

from rdflib import Graph  # noqa: E402,F811
t = Graph().parse(ROOT / "examples" / "emst-v2.skos.example.ttl", format="turtle")
check("SKOS Turtle parses", len(t) > 10, f"{len(t)} triples")
for f in ["emst-v2.case-1.1.example.json", "emst-v2.ctdl-asn.example.jsonld", "emst-v2.rsd.example.json", "ob3-alignment.example.json", "csv_bundle/datapackage.json"]:
    try:
        json.loads((ROOT / "examples" / f).read_text())
        check(f"{f} is valid JSON", True)
    except Exception as e:  # noqa: BLE001
        check(f"{f} is valid JSON", False, str(e))

# SSSOM files: required columns and allowed predicates/justifications
REQ = {"subject_id", "predicate_id", "object_id", "mapping_justification"}
PRED = {"skos:exactMatch", "skos:closeMatch", "skos:broadMatch", "skos:narrowMatch", "skos:relatedMatch", "emst:requiresCompetency"}
for f in sorted((ROOT / "crosswalks").glob("*.sssom.tsv")) + [ROOT / "examples" / "csv_bundle" / "mappings.sssom.tsv"]:
    lines = [l for l in f.read_text().splitlines() if not l.startswith("#")]
    rows = list(csv.DictReader(lines, delimiter="\t"))
    cols = set(rows[0].keys()) if rows else set()
    bad = [r for r in rows if r["predicate_id"] not in PRED or not r["mapping_justification"].startswith("semapv:")]
    check(f"SSSOM {f.name}", REQ <= cols and not bad and len(rows) > 0, f"{len(rows)} rows")

# CSV schemas from TEAM_BRIEF §5 and IA-specific files
HEAD = {
    "sources.csv": "source_id,title,author_or_publisher,date_published,url,source_type,accessed,used_for,quality,status,why_chosen",
    "ecosystem.csv": "entity_id,name,entity_type,owner_or_host,sector_focus,what_it_illuminates,latest_release_or_status,how_emst_connects,integration_detail,url,evidence_label,source_ids,proposed_by",
    "v1_assessment.csv": "element,v1_location,verdict,rationale,evidence_label,source_ids,proposed_by",
    "candidate_competencies.csv": "cand_id,proposed_title,description,craft_primary,craft_secondary,subsector,sector_actors,change_type,driver,evidence_label,source_ids,related_v1_codes,rationale,proposed_by",
    "role_signals.csv": "signal_id,role_title,sector_actor,subsector,signal_type,description,driver,horizon,evidence_label,source_ids,related_v1_codes,proposed_by",
    "standards_appraisal.csv": "standard_id,name,steward,current_version_date,purpose,fit_for_emst,adopt|map|watch,notes,source_ids",
}
ENUMS = {
    "sources.csv": {"source_type": {"peer-reviewed", "government", "standard", "dataset", "index", "industry-report", "job-posting", "grey-literature", "news", "practitioner", "legal"}},
    "v1_assessment.csv": {"verdict": {"carry", "change", "retire", "add", "needs-evidence"}, "evidence_label": {"E", "J", "S"}},
    "ecosystem.csv": {"evidence_label": {"E", "J", "S"}},
    "standards_appraisal.csv": {"adopt|map|watch": {"adopt", "map", "watch", "adopt+map", "avoid"}},
}
src_ids = set()
for f, h in HEAD.items():
    p = ROOT / f
    if not p.exists():
        check(f"{f} present", f in ("candidate_competencies.csv", "role_signals.csv"), "optional" if f in ("candidate_competencies.csv", "role_signals.csv") else "missing")
        continue
    with open(p, newline="") as fh:
        rd = csv.reader(fh)
        header = next(rd)
        rows = list(rd)
    check(f"{f} header", ",".join(header) == h, ",".join(header)[:200])
    widths = {len(r) for r in rows}
    check(f"{f} rows have {len(header)} fields", widths <= {len(header)}, str(widths))
    for col, allowed in ENUMS.get(f, {}).items():
        i = header.index(col)
        badv = sorted({r[i] for r in rows if r[i] not in allowed})
        check(f"{f}.{col} values", not badv, ",".join(badv))
    if f == "sources.csv":
        src_ids = {r[0] for r in rows}
        st = header.index("status")
        badst = [r[st] for r in rows if not (r[st] in {"current", "outdated", "poor-fit", "unverified"} or r[st].startswith("superseded-by:"))]
        check("sources.csv status values", not badst, ",".join(badst[:5]))
# every IA-### cited in CSVs/markdown resolves to sources.csv
import re  # noqa: E402
cited = set()
for p in list(ROOT.glob("*.csv")) + list(ROOT.glob("*.md")):
    if p.name == "sources.csv":
        continue
    cited |= set(re.findall(r"\bIA-\d{3}\b", p.read_text()))
missing = sorted(cited - src_ids)
check("all cited IA-### source IDs resolve", not missing, ",".join(missing))
print("\nALL CHECKS PASSED" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
