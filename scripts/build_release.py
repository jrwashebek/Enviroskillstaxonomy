#!/usr/bin/env python3
"""Build EMST release artifacts deterministically from the source records (WP-01; SPEC §17.2; ADR-0010 §1).

Outputs in --out (default dist/<version>/):
  emst.bundle.jsonld          normative JSON-LD bundle (records sorted by id; context inlined)
  csv/*.csv + datapackage.json  CSV + Frictionless data package: competencies, tasks, indicators, task links,
                              HCM skills-library import file, mappings (flattened), release delta feed
  emst.skos.ttl               SKOS: every vocab/ concept scheme + released competencies/tasks + SKOS mappings
  sssom/<set>.sssom.tsv (+.yml)  mapping sets as released (held rows redacted; unreleased successors -> NoTermFound)
  sssom/strict-1.0/<set>.sssom.tsv  generated SSSOM 1.0-strict rendering (1.1-only justifications -> UnspecifiedMatching)
  views/*.json                computed views, each row stamped ruleId/ruleVersion/buildCommit from the active rule file
                              in vocab/rules/ (ADR-0021; ADR-0029 §4): counts, inverse_links, effective_use_tier,
                              assessment_staleness, change_indicators, display_gate; views/agreement/<study>.json
  RELEASE_NOTES.md            generated counts; held items reported only as a count
  delta.json                  added/changed/superseded/withdrawn IDs vs --previous bundle
  SHA256SUMS                  checksums of every file

Release gate (always on): held Tribal-related records, and records attached to a held target, are excluded
(ADR-0007 §D); records carrying LicenseRef-EMSTv1-PendingDedication are excluded from the CC0 files while the lead's
Q2 dedication is pending (ADR-0013); records licensed LicenseRef-EMST-third-party-index-derived are excluded from every
output and counted (ADR-0029 §9.6); quarantined signals (careFlag, SP-12), placeholder `mvp-role:` targets and
organization measures with n < 5 are excluded (ADR-0029 §8.2); v1Seed, editorialNote and stored inverse links are
stripped (inverses are recomputed by inverse-links@1.1.0); drafts are excluded (profile `release`). The build refuses to
run if scripts/validate_v2.py --strict reports errors (skip only with --no-validate, e.g. in tests), and it
re-checks its own output for leaks before writing SHA256SUMS.

Usage:
  python scripts/build_release.py --version 2.0.0-rc.1 [--date 2027-01-15] [--previous dist/2.0.0-rc.0/emst.bundle.jsonld]
  python scripts/build_release.py --profile preview --version 2.0.0-dev     # internal: includes drafts (never held)
Determinism: no wall-clock time is used; --date defaults to SOURCE_DATE_EPOCH, else the latest generatedAt among
included records. Two consecutive builds from the same inputs are byte-identical (tests/test_build_release.py).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import uuid
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emstlib as L  # noqa: E402
from rules import (agreement, assessment_staleness, change_indicator, effective_use_tier, gated_values,  # noqa: E402
                   inverse_links, io_bridge, registry)

V1_LICENSE = "LicenseRef-EMSTv1-PendingDedication"
CC0_IRI = "https://creativecommons.org/publicdomain/zero/1.0/"
UUID_NS = uuid.uuid5(uuid.NAMESPACE_URL, L.IRI_BASE)
_DROP = object()
STRIP_FIELDS = {"v1Seed", "editorialNote"}
RELEASE_STATUSES = {"candidate", "published", "deprecated", "superseded", "withdrawn"}
NOTICE = ("EMST describes work; it is not a selection instrument, not a classification basis, not a job analysis "
          "and not for RIF, adverse action or performance-rating decisions (ADR-0012 I-2; ADR-0024).")
INDIGENOUS_STATEMENT = ("Indigenous knowledge is a distinct body of environmental expertise held and governed by Indigenous "
                        "nations. It is out of scope of EMST by design (ADR-0007; SPEC §16.1).")
TEXT_FIELDS_TO_LANG = {"rationale", "assessmentContext", "authorityBasis", "principal", "accountabilityVenue", "counterSignal",
                       "evidencePlan", "shouldRemainHumanReason", "mitigation", "scopeOfPractice", "assessmentPlan", "note",
                       "description", "costNote"}
THIRD_PARTY_LICENSE = "LicenseRef-EMST-third-party-index-derived"
EXCLUDE_THIRD_PARTY = "third-party index-derived licence (ADR-0013; ADR-0029 §9.6)"
EXCLUDE_HELD = "held (Tribal content hold, ADR-0007 §D)"
DEPENDENT_FIELDS = ("task", "competency", "subject", "targetId", "variantOf")
WAIVER_COLUMNS = ["record_id", "rule_id", "text_sha256", "waiver_class", "reviewer", "second_reviewer", "decided_on", "rationale"]


def git_commit(root: Path) -> str:
    try:
        out = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=10)
        dirty = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--", "data", "vocab", "schema"],
                               capture_output=True, text=True, timeout=20)
        if out.returncode == 0:
            return out.stdout.strip() + ("+uncommitted" if dirty.stdout.strip() else "")
    except Exception:  # noqa: BLE001
        pass
    return "uncommitted"


def case_uuid(rid: str) -> str:
    return str(uuid.uuid5(UUID_NS, L.iri(rid)))


class Builder:
    def __init__(self, data_root=L.DATA_V2, profile="release", version="2.0.0-dev", date=None, previous=None,
                 include_pending_license=False, build_commit=None):
        self.data = Path(data_root)
        self.profile = profile
        self.version = version
        self.previous = previous
        self.include_pending = include_pending_license and profile == "preview"
        gov = self.data / "governance"
        self.hold = L.load_yaml(gov / "tribal_hold.yaml") if (gov / "tribal_hold.yaml").exists() else {}
        self.licensing = L.load_yaml(gov / "licensing.yaml") if (gov / "licensing.yaml").exists() else {"v1Dedication": "pending"}
        self.held_keys = set(self.hold.get("heldSeedKeys") or [])
        self.held_v1 = set(self.hold.get("heldV1Codes") or [])
        self.tac = bool(self.hold.get("tacConstituted"))
        self.commit = build_commit or git_commit(L.ROOT)
        self.records = {}
        for loc, rec in L.iter_records(self.data):
            if isinstance(rec, dict) and isinstance(rec.get("id"), str):
                self.records.setdefault(rec["id"], rec)
        self.excluded = Counter()
        self.date = date or self._default_date()
        self.rules = registry.active_rules()
        self.stamped: set = set()
        cf = L.load_yaml(L.LINT_DIR / "computed_fields.yaml")
        self.inverse_fields = {t: set(v) for t, v in (cf.get("inverse_fields_by_type") or {}).items()}
        self.waivers = self._load_waivers()
        gc = L.load_yaml(L.LINT_DIR / "governed_content.yaml")
        self.triggers = [re.compile(p["pattern"], 0 if p.get("cs") else re.I) if isinstance(p, dict) else re.compile(p, re.I)
                         for p in gc["tribal_hold"]["triggers"]]

    def _load_waivers(self):
        """data/v2/governance/lint_waivers.csv rows signed by pseudonymous humans only (validate_v2 reports the rest)."""
        p = self.data / "governance" / "lint_waivers.csv"
        if not p.exists():
            return []
        out = []
        for w in L.read_csv(p):
            if list(w) != WAIVER_COLUMNS:
                return []
            signers = [w["reviewer"]] + ([w["second_reviewer"]] if w["second_reviewer"] else [])
            if all(x.startswith("pid:") for x in signers) and w["reviewer"] != w["second_reviewer"]:
                out.append(dict(w))
        return out

    def _default_date(self):
        sde = os.environ.get("SOURCE_DATE_EPOCH")
        if sde:
            return dt.datetime.fromtimestamp(int(sde), dt.timezone.utc).date().isoformat()
        dates = sorted(str((r.get("provenance") or {}).get("generatedAt", ""))[:10] for r in self.records.values())
        return dates[-1] if dates and dates[-1] else "1970-01-01"

    # ---------------------------------------------------------------- gate
    def is_held(self, rid, rec):
        if rid in self.held_keys:
            return True
        if rec.get("indigenousDataFlag") is True and not (self.tac and rec.get("approvalStatus") == "approved"):
            return True
        for d in (rec.get("provenance") or {}).get("derivedFrom") or []:
            m = re.match(r"^v1:([1-7]\.\d{1,2}\.\d{1,2})", d.get("v1Key", ""))
            if m and m.group(1) in self.held_v1 and d.get("relation") != "reference-only":
                return True
        return False

    def depends_on_held(self, rec):
        """Records attached to a held target inherit the hold (ADR-0007 §D; ADR-0029 §9.6)."""
        refs = [rec.get(f) for f in DEPENDENT_FIELDS]
        refs += [s.get("competency") for s in rec.get("supports") or [] if isinstance(s, dict)]
        return any(self._held_ref(x) for x in refs if isinstance(x, str))

    @staticmethod
    def quarantined(rec):
        if rec.get("type") != "ChangeSignal":
            return False
        sps = set(rec.get("scenarioSignposts") or []) | {n.get("value") for n in rec.get("notation") or []
                                                         if isinstance(n, dict) and n.get("scheme") == "EMST-signpost"}
        return bool(rec.get("careFlag")) or bool(sps & {"vocab:scenarios#SP-12", "SP-12"})

    def include(self, rid, rec):
        if rec.get("type") == "VocabularyTerm":
            return False
        if self.is_held(rid, rec) or self.depends_on_held(rec):
            self.excluded[EXCLUDE_HELD] += 1
            return False
        if rec.get("license") == THIRD_PARTY_LICENSE:
            self.excluded[EXCLUDE_THIRD_PARTY] += 1
            return False
        if self.quarantined(rec):
            self.excluded["quarantined signal: careFlag or signpost SP-12 (ADR-0028 ER-0; ADR-0029 §8.2)"] += 1
            return False
        if str(rec.get("targetId", "")).startswith("mvp-role:"):
            self.excluded["placeholder mvp-role: target, not yet re-keyed (ADR-0029 §8.2)"] += 1
            return False
        if rec.get("type") == "ChangeSignal" and rec.get("targetType") == "organization" \
                and isinstance((rec.get("measure") or {}).get("n"), int) and rec["measure"]["n"] < 5:
            self.excluded["organization measure with n < 5, suppressed (ADR-0012)"] += 1
            return False
        if rec.get("license") == V1_LICENSE and self.licensing.get("v1Dedication") != "granted" and not self.include_pending:
            self.excluded["v1-derived text pending CC0 dedication (ADR-0013, Q2)"] += 1
            return False
        if self.profile == "release" and rec.get("status") not in RELEASE_STATUSES:
            self.excluded["draft (not in a release)"] += 1
            return False
        if self.profile == "release" and not L.is_emst_id(rid):
            self.excluded["no minted ID"] += 1
            return False
        if rec.get("type") == "Pathway" and rec.get("recommended") is True:
            raise SystemExit(f"release gate: pathway {rid} is labelled recommended (ADR-0023)")
        return True

    def clean(self, rec):
        out = {}
        inverse = self.inverse_fields.get(rec.get("type"), set())
        for k, v in rec.items():
            if k in STRIP_FIELDS or k in inverse:
                continue
            v = self._redact(v)
            if v is _DROP:
                continue
            out[k] = self._lang(k, v)
        return out

    def _held_ref(self, s):
        if not isinstance(s, str) or not L.is_record_ref(s):
            return False
        if s in self.held_keys:
            return True
        r = self.records.get(s)
        return r is not None and self.is_held(s, r)

    def _redact(self, v):
        """Remove references to held records from released records (ADR-0007 §D: held keys never leave the repo)."""
        if isinstance(v, str):
            return _DROP if self._held_ref(v) else v
        if isinstance(v, list):
            items = [self._redact(x) for x in v]
            return [x for x in items if x is not _DROP]
        if isinstance(v, dict):
            out = {}
            for k, x in v.items():
                y = self._redact(x)
                if y is not _DROP:
                    out[k] = y
            if any(self._held_ref(x) for x in v.values() if isinstance(x, str)):
                return _DROP          # an object that names held content is dropped whole (e.g. a supports link)
            return out
        return v

    def _lang(self, key, v):
        if isinstance(v, dict):
            return {k: self._lang(k, x) for k, x in v.items()}
        if isinstance(v, list):
            return [self._lang(key, x) for x in v]
        if key in TEXT_FIELDS_TO_LANG and isinstance(v, str):
            return {"en": v}
        return v

    # ---------------------------------------------------------------- build
    def build(self, out: Path):
        out = Path(out)
        released = {rid: self.clean(rec) for rid, rec in sorted(self.records.items()) if self.include(rid, rec)}
        self.released = released
        self.inverse = inverse_links.compute(released)
        files: dict[str, bytes] = {}
        files["emst.bundle.jsonld"] = self.bundle(released).encode("utf-8")
        files.update(self.csvs(released))
        files["emst.skos.ttl"] = self.skos(released).encode("utf-8")
        files.update(self.sssom(released))
        files.update(self.views(released))
        delta = self.delta(released)
        files["delta.json"] = L.dump_json(delta).encode("utf-8")
        files["csv/delta.csv"] = L.csv_text(["id", "change"], [{"id": i, "change": c} for c in ("added", "changed", "superseded", "withdrawn") for i in delta[c]]).encode()
        files["csv/datapackage.json"] = self.datapackage(files).encode("utf-8")
        files["RELEASE_NOTES.md"] = self.notes(released, delta).encode("utf-8")
        self.self_check(files)
        sums = "".join(f"{L.sha256_bytes(files[name])}  {name}\n" for name in sorted(files))
        files["SHA256SUMS"] = sums.encode()
        out.mkdir(parents=True, exist_ok=True)
        for name, data in files.items():
            p = out / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        return files

    def bundle(self, released):
        ctx = json.loads(L.CONTEXT_OUT.read_text(encoding="utf-8"))["@context"]
        extra = inverse_links.bundle_fields(self.inverse)            # inverse-links@1.1.0 bundle_fields
        if extra:
            self.stamped.add(("inverse-links", str(self.rules["inverse-links"]["version"])))
        graph = [dict(r, **extra.get(rid, {})) for rid, r in released.items()]
        mappings = self._mapping_rows(released)
        for set_name, rows in sorted(mappings.items()):
            for r in rows:
                m = {"type": "Mapping", **{k: v for k, v in r.items() if v not in ("", None)}}
                m["mapping_set_id"] = m.get("mapping_set_id", set_name)
                if "author_id" in m:
                    m["author_id"] = [m["author_id"]]
                graph.append(m)
        manifest = {"id": f"https://w3id.org/emst/release/{self.version}", "type": "Release",
                    "emstRelease": self.version, "schemaVersion": L.SCHEMA_VERSION, "released": self.date,
                    "license": CC0_IRI, "notice": NOTICE, "indigenousKnowledgeStatement": INDIGENOUS_STATEMENT,
                    "buildCommit": self.commit}
        # everything in the default graph: release manifest first, then records sorted by id, then mappings
        return L.dump_json({"@context": ctx, "@graph": [manifest] + graph})

    # ---------------------------------------------------------------- CSV + datapackage
    TABLES = {
        "competencies": ["id", "uri", "case_uuid", "v1_codes", "pref_label_en", "statement_en", "competency_type", "transversal_cluster",
                         "home_module", "module", "status", "lifecycle_state", "use_tier_ceiling", "validation_status",
                         "level_min", "level_max", "replaced_by", "license"],
        "tasks": ["id", "uri", "pref_label_en", "statement_en", "text_sha256", "work_function", "field_dependency",
                  "formation_dependency", "home_module", "module", "status", "lifecycle_state", "validation_status", "license"],
        "task_competency_links": ["task_id", "competency_id", "strength"],
        "indicators": ["id", "competency_id", "level", "statement_en", "augmentation_mode", "use_class", "obs4",
                       "assessment_methods", "jurisdiction_variable", "validation_status"],
        "hcm_skills_library": ["skill_id", "uri", "case_uuid", "ctid", "skill_name", "skill_statement", "category", "module",
                               "status", "replaced_by", "emst_release", "notice"],
        "mappings": ["mapping_set", "subject_id", "predicate_id", "predicate_modifier", "object_id", "mapping_justification",
                     "confidence", "author_id", "mapping_date", "comment"],
    }

    def csvs(self, released):
        rows = defaultdict(list)
        for rid, r in released.items():
            t = r.get("type")
            en = lambda f: (r.get(f) or {}).get("en", "") if isinstance(r.get(f), dict) else (r.get(f) or "")  # noqa: E731
            if t == "Competency":
                rows["competencies"].append({
                    "id": rid, "uri": L.iri(rid), "case_uuid": case_uuid(rid),
                    "v1_codes": "|".join(n["value"] for n in r.get("notation", []) if n.get("scheme") == "EMSTv1"),
                    "pref_label_en": en("prefLabel"), "statement_en": en("statement"), "competency_type": r.get("competencyType", ""),
                    "transversal_cluster": r.get("transversalCluster", ""), "home_module": r.get("homeModule", ""),
                    "module": r.get("module"), "status": r.get("status"), "lifecycle_state": r.get("lifecycleState", ""),
                    "use_tier_ceiling": r.get("useTier", ""), "validation_status": r.get("validationStatus", ""),
                    "level_min": (r.get("levelSpan") or {}).get("min", ""), "level_max": (r.get("levelSpan") or {}).get("max", ""),
                    "replaced_by": "|".join(r.get("replacedBy", [])), "license": r.get("license")})
                rows["hcm_skills_library"].append({
                    "skill_id": rid, "uri": L.iri(rid), "case_uuid": case_uuid(rid), "ctid": "ce-" + case_uuid(rid),
                    "skill_name": en("prefLabel"), "skill_statement": en("statement"), "category": r.get("competencyType", ""),
                    "module": r.get("module"), "status": r.get("status"), "replaced_by": "|".join(r.get("replacedBy", [])),
                    "emst_release": self.version, "notice": NOTICE})
            elif t == "Task":
                rows["tasks"].append({
                    "id": rid, "uri": L.iri(rid), "pref_label_en": en("prefLabel"), "statement_en": en("statement"),
                    "text_sha256": r.get("textSha256"), "work_function": r.get("workFunction", ""),
                    "field_dependency": r.get("fieldDependency", ""), "formation_dependency": r.get("formationDependency", ""),
                    "home_module": r.get("homeModule", ""), "module": r.get("module"), "status": r.get("status"),
                    "lifecycle_state": r.get("lifecycleState", ""), "validation_status": r.get("validationStatus", ""),
                    "license": r.get("license")})
                for s in r.get("supports", []):
                    if s["competency"] in released:
                        rows["task_competency_links"].append({"task_id": rid, "competency_id": s["competency"], "strength": s["strength"]})
            elif t == "Indicator":
                rows["indicators"].append({
                    "id": rid, "competency_id": r.get("competency"), "level": r.get("level"), "statement_en": en("statement"),
                    "augmentation_mode": r.get("augmentationMode", ""), "use_class": r.get("useClass", ""), "obs4": r.get("obs4", ""),
                    "assessment_methods": "|".join(r.get("assessmentMethods", [])),
                    "jurisdiction_variable": str(r.get("jurisdictionVariable", "")).lower(), "validation_status": r.get("validationStatus", "")})
        for set_name, mrows in sorted(self._mapping_rows(released).items()):
            for m in mrows:
                rows["mappings"].append({"mapping_set": set_name, **{k: m.get(k, "") for k in self.TABLES["mappings"] if k != "mapping_set"}})
        return {f"csv/{name}.csv": L.csv_text(cols, rows[name]).encode("utf-8") for name, cols in self.TABLES.items()}

    def datapackage(self, files):
        resources = []
        keys = {"competencies": ["id"], "tasks": ["id"], "indicators": ["id"], "hcm_skills_library": ["skill_id"]}
        fks = {"task_competency_links": [{"fields": "task_id", "reference": {"resource": "tasks", "fields": "id"}},
                                         {"fields": "competency_id", "reference": {"resource": "competencies", "fields": "id"}}],
               "indicators": [{"fields": "competency_id", "reference": {"resource": "competencies", "fields": "id"}}]}
        cols = dict(self.TABLES)
        cols["delta"] = ["id", "change"]
        for name in sorted(cols):
            path = f"{name}.csv"
            schema = {"fields": [{"name": c, "type": "integer" if c == "obs4" else "string"} for c in cols[name]]}
            if name in keys:
                schema["primaryKey"] = keys[name]
            if name in fks:
                schema["foreignKeys"] = fks[name]
            resources.append({"name": name.replace("_", "-"), "path": path, "profile": "tabular-data-resource",
                              "format": "csv", "mediatype": "text/csv", "encoding": "utf-8",
                              "hash": "sha256:" + L.sha256_bytes(files[f"csv/{name}.csv"]), "schema": schema})
        pkg = {"profile": "tabular-data-package", "name": "emst", "title": "Environmental Management Skills Taxonomy",
               "version": self.version, "created": self.date, "licenses": [{"name": "CC0-1.0", "path": CC0_IRI}],
               "description": NOTICE, "resources": resources}
        return L.dump_json(pkg)

    # ---------------------------------------------------------------- SKOS
    @staticmethod
    def _lit(s, lang=None):
        esc = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
        return f'"{esc}"' + (f"@{lang}" if lang else "")

    def skos(self, released):
        lines = ["@prefix skos: <http://www.w3.org/2004/02/skos/core#> .", "@prefix dct: <http://purl.org/dc/terms/> .",
                 "@prefix owl: <http://www.w3.org/2002/07/owl#> .", ""]
        triples = []
        main = f"{L.IRI_BASE}scheme/emst-v2"
        triples.append((main, "a", "skos:ConceptScheme"))
        triples.append((main, "dct:title", self._lit("Environmental Management Skills Taxonomy", "en")))
        triples.append((main, "owl:versionInfo", self._lit(self.version)))
        triples.append((main, "dct:license", f"<{CC0_IRI}>"))
        for vf in sorted(L.VOCAB.glob("*.yaml")):
            v = L.load_yaml(vf)
            scheme = f"{L.IRI_BASE}vocab/{v.get('scheme', vf.stem)}"
            triples.append((scheme, "a", "skos:ConceptScheme"))
            triples.append((scheme, "dct:title", self._lit(str(v.get("title", vf.stem)), "en")))
            if v.get("schemeVersion"):
                triples.append((scheme, "owl:versionInfo", self._lit(str(v["schemeVersion"]))))
            for term in self._vocab_terms(v):
                iri = f"{scheme}/{term['notation']}"
                triples.append((iri, "a", "skos:Concept"))
                triples.append((iri, "skos:inScheme", f"<{scheme}>"))
                triples.append((iri, "skos:notation", self._lit(str(term["notation"]))))
                if term.get("prefLabel"):
                    triples.append((iri, "skos:prefLabel", self._lit(str(term["prefLabel"]), "en")))
                if term.get("definition"):
                    triples.append((iri, "skos:definition", self._lit(L.normalize_text(str(term["definition"])), "en")))
                if term.get("broader"):
                    triples.append((iri, "skos:broader", f"<{scheme}/{term['broader']}>"))
        for rid, r in released.items():
            if r.get("type") not in ("Competency", "Task", "KnowledgeStatement", "RoleProfile"):
                continue
            iri = L.iri(rid)
            triples.append((iri, "a", "skos:Concept"))
            triples.append((iri, "skos:inScheme", f"<{main}>"))
            for lang, txt in (r.get("prefLabel") or {}).items():
                triples.append((iri, "skos:prefLabel", self._lit(txt, lang)))
            for f in ("definition", "statement"):
                for lang, txt in (r.get(f) or {}).items() if isinstance(r.get(f), dict) else []:
                    triples.append((iri, "skos:definition" if f == "definition" else "skos:scopeNote", self._lit(txt, lang)))
            for n in r.get("notation", []):
                triples.append((iri, "skos:notation", self._lit(f"{n['scheme']}:{n['value']}")))
            for rb in r.get("replacedBy", []):
                if rb in released:
                    triples.append((iri, "dct:isReplacedBy", f"<{L.iri(rb)}>"))
        for set_name, rows in sorted(self._mapping_rows(released).items()):
            for m in rows:
                p = m.get("predicate_id", "")
                if p.startswith("skos:") and not m.get("predicate_modifier") and m.get("object_id") != "sssom:NoTermFound":
                    s, o = m.get("subject_id", ""), m.get("object_id", "")
                    if L.is_record_ref(s) and (L.is_record_ref(o) or o.startswith("http")):
                        triples.append((L.iri(s), p, f"<{L.iri(o) if L.is_record_ref(o) else o}>"))
        body = []
        for s, p, o in sorted(set(triples)):
            obj = o if (o.startswith('"') or o.startswith("<") or o.startswith("skos:")) else o
            body.append(f"<{s}> {p} {obj} .")
        return "\n".join(lines + body) + "\n"

    @staticmethod
    def _vocab_terms(v):
        out = []

        def add(t, broader=None):
            if isinstance(t, dict) and t.get("notation") is not None:
                out.append({"notation": t["notation"], "prefLabel": t.get("prefLabel"), "definition": t.get("definition"), "broader": broader})
                for sub in ("subtypes", "subfunctions", "components", "clusters"):
                    for c in t.get(sub, []) or []:
                        add(c, t["notation"])
        for t in v.get("terms", []) or []:
            add(t)
        return [t for t in out if re.fullmatch(r"[A-Za-z0-9._-]+", str(t["notation"]))]

    # ---------------------------------------------------------------- SSSOM
    def _mapping_rows(self, released):
        if hasattr(self, "_mcache"):
            return self._mcache
        sets = {}
        cw = self.data / "crosswalks"
        for tsv in sorted(cw.rglob("*.sssom.tsv")) if cw.exists() else []:
            lines = [ln for ln in tsv.read_text(encoding="utf-8").splitlines() if ln and not ln.startswith("#")]
            if not lines:
                continue
            header = lines[0].split("\t")
            rows = [dict(zip(header, ln.split("\t"))) for ln in lines[1:]]
            name = str(tsv.relative_to(cw))[: -len(".sssom.tsv")]
            out_rows, by_subject = [], defaultdict(list)
            for r in rows:
                obj = r.get("object_id", "")
                subj = r.get("subject_id", "")
                orec = self.records.get(obj)
                if orec is not None and self.is_held(obj, orec) or obj in self.held_keys:
                    by_subject[subj].append(None)
                    continue
                srec = self.records.get(subj)
                if srec is not None and subj not in released:
                    continue
                r = dict(r)
                if L.is_record_ref(obj) and obj not in released:
                    r["object_id"] = "sssom:NoTermFound"
                    r["comment"] = (r.get("comment", "") + "; successor not in this release").strip("; ")
                by_subject[subj].append(r)
            for subj, items in by_subject.items():
                kept = [x for x in items if x is not None]
                if kept:
                    out_rows.extend(kept)
                else:
                    template = next(r for r in rows if r.get("subject_id") == subj)
                    out_rows.append({**template, "object_id": "sssom:NoTermFound",
                                     "comment": "Successor withheld pending Tribal Advisory Council review (ADR-0007 §D); not retired."})
            dec_rx = re.compile(r"^(decision=[a-z-]+)")
            for r in out_rows:
                m = dec_rx.match(r.get("comment", "") or "")
                if m and "withheld" in r.get("comment", ""):
                    r["comment"] = m.group(1) + "; " + r["comment"].split("; ", 1)[-1]
            sets[name] = out_rows
        self._mcache = sets
        return sets

    def sssom(self, released):
        files = {}
        cw = self.data / "crosswalks"
        for name, rows in sorted(self._mapping_rows(released).items()):
            src = cw / f"{name}.sssom.tsv"
            header = [ln for ln in src.read_text(encoding="utf-8").splitlines() if ln and not ln.startswith("#")][0].split("\t")
            files[f"sssom/{name}.sssom.tsv"] = L.csv_text(header, [{k: r.get(k, "") for k in header} for r in rows], delimiter="\t").encode()
            meta = cw / f"{name}.sssom.yml"
            if meta.exists():
                m = L.load_yaml(meta)
                m["mapping_set_version"] = f"{m.get('mapping_set_version', '0')}+emst.{self.version}"
                files[f"sssom/{name}.sssom.yml"] = L.dump_yaml(m).encode()
            strict = self._strict_rows(rows)
            if strict is not None:                      # CR-IA-002 #4: generated SSSOM 1.0-strict rendering, never a source
                hdr = header + ([] if "other" in header else ["other"])
                files[f"sssom/strict-1.0/{name}.sssom.tsv"] = L.csv_text(hdr, [{k: r.get(k, "") for k in hdr} for r in strict], delimiter="\t").encode()
        return files

    def _strict_rows(self, rows):
        only = set(L.load_yaml(L.VOCAB / "mapping_predicates.yaml").get("justifications_sssom_1_1_only") or [])
        if not any(r.get("mapping_justification") in only for r in rows):
            return None
        out = []
        for r in rows:
            r = dict(r)
            j = r.get("mapping_justification")
            if j in only:
                r["mapping_justification"] = "semapv:UnspecifiedMatching"
                other = r.get("other") or ""
                if "original_justification=" not in other:
                    r["other"] = ";".join(x for x in (other, f"original_justification={j}") if x)
            out.append(r)
        return out

    # ---------------------------------------------------------------- computed views (ADR-0021; ADR-0029 §4)
    def _stamp(self, rule):
        st = registry.stamp(self.rules, rule, self.commit)
        self.stamped.add((rule, st["ruleVersion"]))
        return st

    def _tool_names(self, released):
        names = []
        for r in released.values():
            if r.get("type") == "Tool" and r.get("toolType") in ("software-product", "platform", "model", "dataset-product", "instrument-model"):
                names += [v for v in (r.get("prefLabel") or {}).values() if isinstance(v, str)] + list(r.get("productExamples") or [])
        return names

    def views(self, released):
        st = self._stamp
        files = {}
        counts = {**st("counts"), "release": self.version,
                  "byType": dict(sorted(Counter(r["type"] for r in released.values()).items())),
                  "competenciesByKind": dict(sorted(Counter(r.get("competencyType", "unset") for r in released.values() if r["type"] == "Competency").items())),
                  "competenciesByModule": dict(sorted(Counter(r.get("module") for r in released.values() if r["type"] == "Competency").items())),
                  "byLifecycle": dict(sorted(Counter(r.get("lifecycleState", "unset") for r in released.values() if r["type"] in ("Competency", "Task", "RoleProfile")).items())),
                  "coreCompetencies": sum(1 for r in released.values() if r["type"] == "Competency" and r.get("module") == "core" and r.get("status") not in ("superseded", "withdrawn")),
                  "excluded": dict(sorted(self.excluded.items()))}
        files["views/counts.json"] = counts
        files["views/inverse_links.json"] = inverse_links.view_rows(self.inverse, st("inverse-links"))
        # effective-use-tier@1.0.0: header pins IO's tier requirements; lint caps from IO's linter with our waivers
        req_file = "validation/indicator_lint_rules.yaml"
        req_doc = L.load_yaml(L.ROOT / req_file) if (L.ROOT / req_file).exists() else {}
        tier_req = ((req_doc.get("publication_rules") or {}).get("tier_requirements")) or {}
        lint, self.waived = io_bridge.lint(released, self.waivers, self._tool_names(released))
        eut_stamp = st("effective-use-tier")
        files["views/effective_use_tier.json"] = {
            "header": {**eut_stamp, "tierRequirements": f"{req_file}#publication_rules.tier_requirements",
                       "tierRequirementsSha256": io_bridge.file_sha256(req_file),
                       "lintEngine": "validation/lint_indicators.py" if lint is not None else "unavailable (every Indicator capped at develop)",
                       "waivers": len(self.waivers)},
            "rows": effective_use_tier.compute(released, tier_req, lint, eut_stamp)}
        files["views/assessment_staleness.json"] = assessment_staleness.compute(released, st("assessment-staleness"))
        # change-indicator@1.0.0 over released signals and external-index assessments
        ci_stamp = st("change-indicator")
        inputs = [r for r in released.values() if r["type"] == "ChangeSignal"
                  or (r["type"] == "ExposureAssessment" and r.get("raterType") == "external-index")]
        files["views/change_indicators.json"] = {
            "header": {**ci_stamp, "inputs": len(inputs), "note": "Only signalStatus active counts; watch signals feed the 'what's coming' view (ifWatchCounted)."},
            "rows": change_indicator.view_rows(inputs, stamp=ci_stamp)}
        # display-gate@1.0.0 with agreement results emitted from declared studies (none before the S2 studies)
        dg_stamp = st("display-gate")
        ratings = [r for r in released.values() if r["type"] in L.RATING_TYPES]
        results = agreement.emit(ratings, agreement.load_studies(self.data), dg_stamp)
        for sid, res in results.items():
            files[f"views/agreement/{sid}.json"] = res
        files["views/agreement/index.json"] = {**dg_stamp, "schema": "validation/display_gates.yaml#agreement_result_schema",
                                               "studies": sorted(results)}
        files["views/display_gate.json"] = gated_values.compute(released, self.rules["display-gate"], results, dg_stamp)
        return {k: L.dump_json(v).encode() for k, v in files.items()}

    # ---------------------------------------------------------------- delta, notes, self-check
    def delta(self, released):
        prev = {}
        if self.previous and Path(self.previous).exists():
            doc = json.loads(Path(self.previous).read_text(encoding="utf-8"))
            prev = {r["id"]: r for r in doc.get("@graph", []) if isinstance(r, dict) and r.get("id") and r.get("type") not in ("Mapping", "Release")}
        cur = {rid: r for rid, r in released.items()}
        out = {"from": str(self.previous or ""), "to": self.version, "added": [], "changed": [], "superseded": [], "withdrawn": []}
        for rid, r in cur.items():
            if rid not in prev:
                out["added"].append(rid)
            elif json.dumps(prev[rid], sort_keys=True) != json.dumps(r, sort_keys=True):
                status = r.get("status")
                key = status if status in ("superseded", "withdrawn") and prev[rid].get("status") != status else "changed"
                out[key].append(rid)
        return out

    def notes(self, released, delta):
        c = Counter(r["type"] for r in released.values())
        lines = [f"# EMST {self.version} — release notes (generated)", "",
                 f"- Released: {self.date} · schema {L.SCHEMA_VERSION} · build {self.commit} · profile `{self.profile}`",
                 f"- Licence: CC0-1.0 for data and standard text (ADR-0013). {NOTICE}",
                 f"- {INDIGENOUS_STATEMENT}", "", "## Contents (counted by the build)", "", "| Entity | Records |", "|---|---|"]
        lines += [f"| {t} | {n} |" for t, n in sorted(c.items())] or ["| (none) | 0 |"]
        lines += ["", "## Excluded by the release gate", "", "| Reason | Records |", "|---|---|"]
        lines += [f"| {k} | {v} |" for k, v in sorted(self.excluded.items())] or ["| (none) | 0 |"]
        waived = Counter(h.rule_id for h in getattr(self, "waived", []))
        lines += ["", "## Lint waivers applied (data/v2/governance/lint_waivers.csv)", "", "| Rule | Waived hits |", "|---|---|"]
        lines += [f"| {k} | {v} |" for k, v in sorted(waived.items())] or ["| (none) | 0 |"]
        lines += ["", "## Computed-view rules", "", "| Rule | Version |", "|---|---|"]
        lines += [f"| {r} | {v} |" for r, v in sorted(self.stamped)]
        lines += ["", "Held Tribal-related items are reported only as a count (ADR-0007 §D); nothing Tribal-related is published "
                  "before a Tribal Advisory Council approves.", "", "## Delta", "",
                  f"added {len(delta['added'])} · changed {len(delta['changed'])} · superseded {len(delta['superseded'])} · withdrawn {len(delta['withdrawn'])}", ""]
        return "\n".join(lines)

    def self_check(self, files):
        """Release gate re-applied to the output: no held key, no v1Seed, no pending-licence record, no Tribal text."""
        problems = []
        doc = json.loads(files["emst.bundle.jsonld"].decode("utf-8"))
        graph_text = json.dumps(doc["@graph"], ensure_ascii=False)
        others = "".join(v.decode("utf-8", "replace") for k, v in files.items() if k != "emst.bundle.jsonld")
        held_ids = {rid for rid, r in self.records.items() if self.is_held(rid, r)} | self.held_keys
        for k in sorted(held_ids):
            pat = re.compile(r"(?<![A-Za-z0-9._/:-])" + re.escape(k) + r"(?![A-Za-z0-9._/-])")
            if pat.search(graph_text) or pat.search(others):
                problems.append(f"held key {k} present in release output")
        if any('"v1Seed"' in json.dumps(r) for r in doc["@graph"]):
            problems.append("v1Seed present in bundle")
        if THIRD_PARTY_LICENSE in graph_text or THIRD_PARTY_LICENSE in others:
            problems.append(f"{THIRD_PARTY_LICENSE} record present in release output (ADR-0029 §9.6)")
        for r in doc["@graph"]:
            for f in self.inverse_fields.get(r.get("type"), set()) - {"tools", "enactments", "tasks"}:
                if f in r:
                    problems.append(f"stored inverse {f} on {r.get('id')}")
        if self.licensing.get("v1Dedication") != "granted" and not self.include_pending and V1_LICENSE in graph_text:
            problems.append("v1-derived (pending dedication) record present in CC0 bundle")
        for r in doc["@graph"]:
            if r.get("type") in ("Mapping", "Release"):
                continue
            for path, s in L.iter_strings(r):
                if path and path[0] in ("provenance", "id"):
                    continue
                if any(rx.search(s) for rx in self.triggers):
                    problems.append(f"Tribal-related text in released record {r.get('id')} at {'/'.join(map(str, path))}")
                    break
        if problems:
            raise SystemExit("release gate failed:\n  " + "\n  ".join(problems[:20]))


Release = Builder      # name used by vocab/rules/*.yaml#implementation ("scripts/build_release.py#Release.views")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", default="2.0.0-dev")
    ap.add_argument("--date")
    ap.add_argument("--profile", choices=["release", "preview"], default="release")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--data-root", type=Path, default=L.DATA_V2)
    ap.add_argument("--previous", type=Path)
    ap.add_argument("--include-pending-license", action="store_true", help="preview only; output is NOT for distribution")
    ap.add_argument("--no-validate", action="store_true")
    ap.add_argument("--build-commit")
    args = ap.parse_args(argv)
    if not args.no_validate:
        import validate_v2
        rep = validate_v2.Validator(args.data_root, strict=args.profile == "release", use_git_base=False).run()
        if rep.errors:
            for i in rep.errors[:30]:
                print(f"{i.code} {i.where} {i.message}")
            print(f"refusing to build: {len(rep.errors)} validation errors (run scripts/validate_v2.py{' --strict' if args.profile == 'release' else ''})")
            return 1
    b = Builder(args.data_root, args.profile, args.version, args.date, args.previous, args.include_pending_license, args.build_commit)
    out = args.out or (L.ROOT / "dist" / args.version)
    files = b.build(out)
    print(f"built {len(files)} files in {out} ({len(b.released)} records; excluded {dict(b.excluded)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
