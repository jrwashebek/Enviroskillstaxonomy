#!/usr/bin/env python3
"""Validate EMST v2 source data: JSON Schema plus every cross-record rule (WP-01; SPEC §17.1, §18).

Checks (issue codes are stable; tests and authoring agents rely on them):
  per record   E-PARSE E-SCHEMA E-LOCATION E-ID-CHECK E-ID-PREFIX E-ID-NAMESPACE E-MODULE-REDEFINES-CORE
               E-COMPUTED-FIELD E-PERSONAL-DATA E-CONFIDENTIAL E-COORDS-CULTURAL E-TRIBAL-HOLD E/W-TRIBAL-LEAK
               E-TEXT-HASH E/W-LINT-TYPING E/W-LINT-INDICATOR E/W-LINT-LENGTH E-LLM-DRAFT E-SOURCE-UNRESOLVED
               E-V1KEY-UNRESOLVED E-V1-WORKBOOK-HASH E-LICENSE-V1 W-LICENSE-V1-REWRITE E-PATHWAY-RECOMMENDED
               E-MODULE-SUBSECTOR E-SEED-CANDIDATE E/W-NOTATION-INTERIM E/W-INDEPENDENCE-KEY-UNLISTED
               E-ORG-TARGET-TRIBAL W-ORG-SMALL-N W-MVP-ROLE-TARGET I-SP12-QUARANTINE E-REVIEW-EVENT-STATUS
               E-LEVEL-DISTRIBUTION W-ROLE-KEY W-COMPUTED-FIELD-DEPRECATED
               (ADR-0030) E/W-MODULE-SUBSECTOR (enactments) E/W-INSTRUMENT-ROLE-MISSING E-INSTRUMENT-LINK-DUPLICATE
               E-ACTING-SELF E-EDGE-REVIEWBY W-EDGE-REVIEW-OVERDUE E-PROVISION-TASK
  cross-record E-ID-DUPLICATE E-REF-DANGLING W-REF-PENDING E-REF-TYPE E-DEPENDENCY-DIRECTION E-TRIBAL-INHERIT
               I-STALE-ASSESSMENT W-COMPETENCY-NO-TASK W-SUPERSEDED-TARGET E-PR2-ATTRIBUTE
               (ADR-0030) I-SUPERSEDED-TARGET-HELD W-EDGE-REDUNDANT E-MIRROR-TWICE E-MIRROR-SELF E-CLO-ENACTMENT-INDICATOR
               E/W-THREE-MODULE I-THREE-MODULE-RECURRENCE E-THREE-MODULE-EXCEPTION-FORMAT W-THREE-MODULE-EXCEPTION-EXPIRED
  waivers      E-WAIVER-FORMAT E-WAIVER-SIGNER I-WAIVER-VOID   (data/v2/governance/lint_waivers.csv; ADR-0029 §5)
  registry     E-REGISTRY-FORMAT E-REGISTRY-APPEND-ONLY E-REGISTRY-TRANSITION E-REGISTRY-MISSING E-REGISTRY-ORPHAN
  crosswalks   E-SSSOM-FORMAT E-SSSOM-VALUE E-SSSOM-THIRD-PARTY-TEXT E-X1-INCOMPLETE E-X1-DECISION E-X1-DUPLICATE
               E-X1-STALE W-X1-PENDING I-SSSOM-1_1-EXTENSION W-SSSOM-REVIEW-PROVENANCE E-SSSOM-SELECTION-1_1
  files        E-PERSONAL-DATA / E-CONFIDENTIAL also run over every other file under data/v2 (CSV, TSV, MD...)

Usage:
  python scripts/validate_v2.py                     # validate data/v2 (exit 1 on any error)
  python scripts/validate_v2.py --strict            # release mode: pending references and draft leaks are errors
  python scripts/validate_v2.py --data-root DIR     # validate another tree (fixtures)
  python scripts/validate_v2.py --registry-base F   # compare the registry with a base copy (CI passes the merge base)
  python scripts/validate_v2.py --json out.json     # machine-readable report
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emstlib as L  # noqa: E402

from jsonschema import Draft202012Validator  # noqa: E402

REGISTRY_COLUMNS = ["id", "type", "namespace", "minted_on", "minted_by", "status", "superseded_by", "first_release"]
REGISTRY_STATUSES = ["candidate", "published", "deprecated", "superseded", "withdrawn"]
REGISTRY_TRANSITIONS = {
    "candidate": {"candidate", "published", "withdrawn"},
    "published": {"published", "deprecated", "superseded", "withdrawn"},
    "deprecated": {"deprecated", "superseded", "withdrawn"},
    "superseded": {"superseded"},
    "withdrawn": {"withdrawn"},
}
SSSOM_REQUIRED = ["subject_id", "predicate_id", "object_id", "mapping_justification"]
SSSOM_COLUMNS = {"record_id", "subject_id", "subject_label", "subject_source", "subject_source_version", "subject_type",
                 "predicate_id", "predicate_modifier", "predicate_label", "object_id", "object_label", "object_source",
                 "object_source_version", "object_type", "mapping_justification", "confidence", "similarity_score",
                 "similarity_measure", "author_id", "author_label", "reviewer_id", "reviewer_label", "reviewer_agreement",
                 "creator_id", "mapping_date", "review_date", "mapping_cardinality", "mapping_provider", "mapping_tool",
                 "mapping_tool_version", "issue_tracker_item", "see_also", "other", "comment", "match_string",
                 "subject_category", "object_category", "curation_rule", "license"}
SSSOM_META_REQUIRED = ["mapping_set_id", "mapping_set_version", "license", "curie_map"]
# fields whose referent being held makes the referring record Tribal-related too (hold inheritance)
DEPENDENT_LINKS = {
    "Task": ["supports.competency"],
    "Indicator": ["competency"],
    "Enactment": ["competency"],
    "KnowledgeStatement": ["supports"],
    "RoleVariant": ["variantOf"],
    "ExposureAssessment": ["task"],
    "CraftRating": ["task", "competency"],
    "FunctionRating": ["task", "competency"],
    "RelevanceRating": ["subject"],
}
# expected referent types for typed links
TYPED_LINKS = {
    ("Task", "supports.competency"): {"Competency"},
    ("Indicator", "competency"): {"Competency"},
    ("Enactment", "competency"): {"Competency"},
    ("Competency", "levels.indicators"): {"Indicator"},
    ("Competency", "knowledge"): {"KnowledgeStatement"},
    ("Competency", "awarenessBundle"): {"KnowledgeStatement"},
    ("Competency", "enactments"): {"Enactment"},
    ("RoleVariant", "variantOf"): {"RoleProfile"},
    ("RoleProfile", "taskBundle.task"): {"Task"},
    ("RoleProfile", "competencyTargets.competency"): {"Competency"},
    ("ExposureAssessment", "task"): {"Task"},
    ("CraftRating", "task"): {"Task"},
    ("CraftRating", "competency"): {"Competency"},
    ("FunctionRating", "task"): {"Task"},
    ("FunctionRating", "competency"): {"Competency"},
    ("DriverEvent", "instrument"): {"Instrument"},
    ("Pathway", "fromVariant"): {"RoleVariant", "RoleProfile"},
    ("Pathway", "toVariant"): {"RoleVariant", "RoleProfile"},
    ("Tool", "servesTasks"): {"Task"},
    ("Tool", "servesCompetencies"): {"Competency"},
    # ADR-0030 (RULINGS_FOR_DE §16-§17)
    ("Enactment", "characteristicInstruments.instrument"): {"Instrument"},
    ("RoleVariant", "instruments.instrument"): {"Instrument"},
    ("DriverEvent", "actingInstrument"): {"Instrument"},
    ("Competency", "mirrors.target"): {"Competency", "Enactment"},
    ("Pathway", "cloOutcomes.competency"): {"Competency"},
    ("Pathway", "sequence.cloOutcomes.competency"): {"Competency"},
    ("Pathway", "sequence.formationProvisions.task"): {"Task"},
}
LINEAGE_KEYS = {"replaces", "replacedBy"}
RELEASABLE_STATUSES = {"candidate", "published", "deprecated", "superseded", "withdrawn"}
LIVE_EXCLUDED_STATUSES = {"superseded", "withdrawn"}
V1_LICENSE = "LicenseRef-EMSTv1-PendingDedication"
AT_OR_AFTER_CANDIDATE = {"candidate", "published", "deprecated"}
SEED_V1_FORBIDDEN = {"candidate", "published", "deprecated", "superseded", "withdrawn"}
IN_FORCE_STATUSES = {"interim-in-force", "in-force", "in-force-litigated", "issued"}
WAIVER_COLUMNS = ["record_id", "rule_id", "text_sha256", "waiver_class", "reviewer", "second_reviewer", "decided_on", "rationale"]
WAIVERS_REL = Path("governance") / "lint_waivers.csv"
THREE_MODULE_REL = Path("governance") / "three_module_exceptions.yaml"
ROLE_REF_RE = re.compile(r"^seed:(R\d{2}-[a-z0-9-]+)(/([a-z-]+)(/[a-z0-9-]+)?)?$")
SELECTION_FLAGS = {("use", "selection"), ("use_class", "selection"), ("useClass", "selection"), ("selection_use", "true")}


class Issue:
    __slots__ = ("code", "severity", "where", "message", "rid")

    def __init__(self, code, where, message, rid=None):
        self.code, self.where, self.message, self.rid = code, str(where), message, rid
        self.severity = {"E": "error", "W": "warning", "I": "info"}[code[0]]

    def as_dict(self):
        return {"code": self.code, "severity": self.severity, "where": self.where, "id": self.rid, "message": self.message}


class Report:
    def __init__(self):
        self.issues: list[Issue] = []
        self.stats: dict = {}

    def add(self, code, where, message, rid=None):
        self.issues.append(Issue(code, where, message, rid))

    def codes(self, severity=None):
        return Counter(i.code for i in self.issues if severity is None or i.severity == severity)

    @property
    def errors(self):
        return [i for i in self.issues if i.severity == "error"]

    def has(self, code):
        return any(i.code == code for i in self.issues)


def _compile(entry):
    if isinstance(entry, dict):
        return re.compile(entry["pattern"], 0 if entry.get("cs") else re.I)
    return re.compile(entry, re.I)


def _get_path(rec, dotted):
    """Values at a dotted path, flattening lists (supports.competency -> every supports[i].competency)."""
    cur = [rec]
    for part in dotted.split("."):
        nxt = []
        for c in cur:
            if isinstance(c, dict) and part in c:
                v = c[part]
                nxt.extend(v if isinstance(v, list) else [v])
            elif isinstance(c, list):
                for x in c:
                    if isinstance(x, dict) and part in x:
                        v = x[part]
                        nxt.extend(v if isinstance(v, list) else [v])
        cur = nxt
    return [c for c in cur if isinstance(c, str)]


def _parse_other(s: str) -> dict:
    out = {}
    for part in (s or "").split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def _lang_values(v):
    if isinstance(v, str):
        return [v]
    if isinstance(v, dict):
        out = []
        for x in v.values():
            out.extend(x if isinstance(x, list) else [x])
        return [x for x in out if isinstance(x, str)]
    return []


def validation_date() -> str:
    """The date edges and register rows are checked against: SOURCE_DATE_EPOCH when set, else today (UTC)."""
    import datetime as _dt
    import os as _os
    sde = _os.environ.get("SOURCE_DATE_EPOCH")
    if sde:
        return _dt.datetime.fromtimestamp(int(sde), _dt.timezone.utc).date().isoformat()
    return _dt.datetime.now(_dt.timezone.utc).date().isoformat()


class Validator:
    def __init__(self, data_root: Path = L.DATA_V2, strict: bool = False, registry_base: Path | None = None,
                 repo_root: Path = L.ROOT, use_git_base: bool = True, check_x1: bool | None = None):
        self.data = Path(data_root)
        self.strict = strict
        self.repo = repo_root
        self.registry_base = registry_base
        self.use_git_base = use_git_base
        self.check_x1 = check_x1
        self.r = Report()
        self.three_module_recurrence: dict[str, list] = {}
        self.today = validation_date()
        self.schema = json.loads(L.SCHEMA_OUT.read_text(encoding="utf-8"))
        self.validator = Draft202012Validator(self.schema)
        lint = L.SCHEMA_DIR / "lint"
        self.computed = L.load_yaml(lint / "computed_fields.yaml")
        self.ilint = L.load_yaml(lint / "indicator_lint.yaml")
        self.tlex = L.load_yaml(lint / "typing_lexicon.yaml")
        self.gov = L.load_yaml(lint / "governed_content.yaml")
        self._prep_patterns()
        self.records: dict[str, tuple] = {}  # id -> (loc, rec)
        self._pending_index: list = []
        self.by_type = defaultdict(list)
        self.hold = self._load_hold()
        self.licensing = self._load_licensing()
        self.planned = self._load_planned_targets()
        self.source_ids = self._load_source_ids()
        self.v1keys, self.v1_competencies = self._load_v1_keys()
        self.copyb_sha = self._copyb_sha()
        self.waivers = self._load_waivers()
        self.valid_waivers = self._valid_waivers()
        self._load_change_vocab()
        self.io_lint = self._load_io_linter()

    # ------------------------------------------------------------------ configuration
    def _prep_patterns(self):
        cf = set(self.computed["fields"])
        snake = {re.sub(r"(?<!^)(?=[A-Z])", "_", f).lower() for f in cf}
        self.computed_names = cf | snake
        self.inverse = {t: set(v) for t, v in (self.computed.get("inverse_fields_by_type") or {}).items()}
        self.transitional = {t: set(v) for t, v in (self.computed.get("transitional_on_drafts") or {}).items()}
        self.computed_paths = {t: list(v) for t, v in (self.computed.get("computed_paths_by_type") or {}).items()}
        th = self.gov["tribal_hold"]
        self.tribal_triggers = [_compile(p) for p in th["triggers"]]
        self.tribal_skip = set(th.get("skip_keys", []))
        self.confidential = [_compile(p) for p in self.gov["confidential_markers"]]
        self.cultural = [_compile(p) for p in self.gov["cultural_site_terms"]]
        self.coord_pats = [_compile(p) for p in self.gov["coordinates"]["patterns"]]
        self.coord_keys = set(self.gov["coordinates"]["keys"])
        pd = self.gov["personal_data"]
        self.pd_pats = {k: re.compile(v) for k, v in pd["patterns"].items()}
        self.pd_allow = set(pd.get("allow_emails") or [])
        self.pd_keys = set(pd["forbidden_keys"])
        self.ilint_rules = []
        for rule in self.ilint["rules"]:
            pat = rule.get("pattern")
            rx = None
            if pat:
                rx = re.compile(("^\\s*(?:" + pat + ")") if rule.get("scope") == "start" else pat, re.I)
            self.ilint_rules.append((rule, rx))
        self.products = [(t["term"], self._term_rx(t)) for t in self.tlex["products"]]
        self.instruments = [(t["term"], self._term_rx(t)) for t in self.tlex["instruments"]]
        tools = self.data / "tools" / "tools.jsonl"
        if tools.exists():
            for line in tools.read_text(encoding="utf-8").splitlines():
                try:
                    for ex in (json.loads(line).get("productExamples") or []):
                        if len(ex) >= 3:            # product names are proper nouns: match case-sensitively (CR-DC-001)
                            self.products.append((ex, self._term_rx({"term": ex, "cs": True})))
                except Exception:  # noqa: BLE001 - parse errors are reported by the record pass
                    pass

    @staticmethod
    def _term_rx(t):
        esc = re.escape(t["term"])
        return re.compile(r"(?<![A-Za-z0-9])" + esc + r"(?![A-Za-z0-9])", 0 if t.get("cs") else re.I)

    def _load_io_linter(self):
        """IO's WP-11 indicator linter (validation/lint_indicators.py) is authoritative for B01-B12 and the publication
        rules when present; schema/lint/indicator_lint.yaml is the fallback."""
        p = self.repo / "validation" / "lint_indicators.py"
        if not p.exists():
            return None
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("emst_io_lint", p)
            mod = importlib.util.module_from_spec(spec)
            sys.modules["emst_io_lint"] = mod          # dataclasses resolve their module through sys.modules
            spec.loader.exec_module(mod)
            tools = self.data / "tools" / "tools.jsonl"
            names = mod.load_jsonl_names(tools if tools.exists() else None, ["prefLabel", "productExamples"],
                                         {"software-product", "platform", "model", "dataset-product", "instrument-model"})
            linter = mod.Linter(mod.load_rules(), "release" if self.strict else "ci", self.valid_waivers, names, [])
            return mod, linter
        except Exception as e:  # noqa: BLE001
            self._io_lint_error = f"{type(e).__name__}: {e}"
            return None

    def check_io_lint(self):
        if getattr(self, "_io_lint_error", None):
            self.r.add("W-LINT-ENGINE", "validation/lint_indicators.py", f"IO linter unavailable, fallback rules used: {self._io_lint_error}")
        if not self.io_lint:
            return
        mod, linter = self.io_lint
        recs, locs = [], {}
        for rid, (loc, rec) in self.records.items():
            if rec.get("type") in ("Indicator", "Competency", "Task", "KnowledgeStatement"):
                recs.append(mod.Record(rec, str(loc)))
                locs[rid] = (loc, rec)
        try:
            hits = linter.lint_set(recs)
        except Exception as e:  # noqa: BLE001
            self.r.add("W-LINT-ENGINE", "validation/lint_indicators.py", f"IO linter failed ({type(e).__name__}: {e}); fallback rules used")
            self.io_lint = None
            for rid, (loc, rec) in locs.items():
                self._fallback_indicator_lint(loc, rec)
            return
        for h in hits:
            if h.severity == "info" or h.status == "waived":
                continue
            loc, rec = locs.get(h.record_id, (h.source, {}))
            if rec.get("type") != "Indicator" and h.rule_id.split("-")[0] in ("B09", "B10"):
                continue        # products/instruments in competency/task text: reported once, by E/W-LINT-TYPING
            seed = rec.get("validationStatus") == "seed-v1"
            code = "E-LINT-INDICATOR" if (h.fails and not seed) else "W-LINT-INDICATOR"
            m = f" [{h.match}]" if h.match else ""
            self.r.add(code, loc, f"{h.rule_id}{m}: {h.message}", h.record_id)

    def _load_waivers(self):
        """data/v2/governance/lint_waivers.csv (ADR-0029 §5.5); IO's validation/waivers/ file is the fallback."""
        p = self.data / WAIVERS_REL
        if not p.exists():
            p = self.repo / "validation" / "waivers" / "indicator_lint_waivers.csv"
        self.waivers_path = p
        if not p.exists():
            return []
        rows = list(csv.reader(p.read_text(encoding="utf-8").splitlines()))
        if not rows:
            return []
        if rows[0] != WAIVER_COLUMNS:
            self.r.add("E-WAIVER-FORMAT", p, f"header must be {','.join(WAIVER_COLUMNS)}")
            return []
        out = []
        for i, row in enumerate(rows[1:], 2):
            if not any(row):
                continue
            if len(row) != len(WAIVER_COLUMNS):
                self.r.add("E-WAIVER-FORMAT", f"{p}:{i}", f"{len(row)} columns, expected {len(WAIVER_COLUMNS)}")
                continue
            w = dict(zip(WAIVER_COLUMNS, row))
            w["_where"] = f"{p}:{i}"
            out.append(w)
        return out

    def _valid_waivers(self):
        """Waivers signed only by pseudonymous humans (pid:); others are reported and never applied (ADR-0012; IO rules)."""
        ok = []
        for w in self.waivers:
            bad = False
            if w["waiver_class"] not in ("accepted-warning", "false-positive"):
                self.r.add("E-WAIVER-FORMAT", w["_where"], f"waiver_class {w['waiver_class']!r} must be accepted-warning or false-positive")
                bad = True
            if not re.fullmatch(r"[0-9a-f]{64}", w["text_sha256"] or ""):
                self.r.add("E-WAIVER-FORMAT", w["_where"], "text_sha256 must be the 64-hex SHA-256 of the normalized statement")
                bad = True
            signers = [("reviewer", w["reviewer"]), ("second_reviewer", w["second_reviewer"])]
            for col, who in signers:
                if (col == "reviewer" or who) and not re.match(r"^pid:", who or ""):
                    self.r.add("E-WAIVER-SIGNER", w["_where"], f"{col} {who!r} is not a pseudonymous human ID (pid:...); agents never sign waivers")
                    bad = True
            if w["waiver_class"] == "false-positive" and not w["second_reviewer"]:
                self.r.add("E-WAIVER-FORMAT", w["_where"], "false-positive waivers need two human reviewers")
                bad = True
            if w["reviewer"] and w["reviewer"] == w["second_reviewer"]:
                self.r.add("E-WAIVER-FORMAT", w["_where"], "reviewer and second_reviewer must differ")
                bad = True
            if not bad:
                ok.append({k: v for k, v in w.items() if not k.startswith("_")})
        return ok

    def _load_change_vocab(self):
        ct = L.load_yaml(self.repo / "vocab" / "change_types.yaml")
        self.independence_keys = {k["key"] for k in (ct.get("independence_keys") or {}).get("keys", [])}
        self.tribal_actors = set(self.schema["$defs"]["v_tribalActor"]["enum"])
        self.sector_actor_terms = set(self.schema["$defs"]["v_sectorActor"]["enum"]) | set(self.schema["$defs"]["v_sectorActorSubtype"]["enum"])
        roles = self.repo / "docs" / "decisions" / "mvp_role_set.csv"
        self.role_keys = {r["role_key"] for r in L.read_csv(roles)} if roles.exists() else set()

    def _load_hold(self):
        p = self.data / "governance" / "tribal_hold.yaml"
        d = L.load_yaml(p) if p.exists() else {}
        held_keys = set(d.get("heldSeedKeys") or [])
        held_v1 = set(d.get("heldV1Codes") or [])
        held_lens = set(d.get("heldV1EthicalLenses") or [])
        return {"keys": held_keys, "v1": held_v1, "lens": held_lens, "tac": bool(d.get("tacConstituted", False))}

    def _load_licensing(self):
        p = self.data / "governance" / "licensing.yaml"
        d = L.load_yaml(p) if p.exists() else {}
        return {"v1Dedication": d.get("v1Dedication", "pending")}

    def _load_planned_targets(self):
        """Planned references (W-REF-PENDING; CR-LC-001 #1): v1 disposition targets, candidates decided for v2.0, and
        MVP role and variant keys (is_planned covers the role pattern)."""
        out = set()
        p = self.data / "migration" / "v1_targets.csv"
        if p.exists():
            out |= {r["target_key"] for r in L.read_csv(p) if r.get("target_key")}
        c = self.repo / "docs" / "decisions" / "candidate_disposition.csv"
        if c.exists():
            out |= {f"seed:{r['cand_id']}" for r in L.read_csv(c) if r.get("decision") in ("core-v2.0", "module-v2.0")}
        return out

    def is_planned(self, ref: str) -> bool:
        if ref in self.planned:
            return True
        m = ROLE_REF_RE.match(ref)
        if not m or m.group(1) not in self.role_keys:
            return False
        return m.group(3) is None or m.group(3) in self.sector_actor_terms

    def planned_is_held(self, ref: str) -> bool:
        if ref in self.hold["keys"]:
            return True
        m = ROLE_REF_RE.match(ref)
        return bool(m and m.group(3) and m.group(3) in self.tribal_actors)

    def _load_source_ids(self):
        ids = set()
        for p in sorted((self.repo / "docs").rglob("sources.csv")):      # research lanes + docs/methods (CR-LM-001 #9)
            try:
                for row in L.read_csv(p):
                    if row.get("source_id"):
                        ids.add(row["source_id"].strip())
            except Exception:  # noqa: BLE001
                continue
        for p in sorted((self.repo / "docs" / "research" / "_verification").glob("*_key_facts.csv")):
            for row in L.read_csv(p):
                if row.get("fact_id"):
                    ids.add(row["fact_id"].strip())
        return ids

    def _load_v1_keys(self):
        keys, comps = set(), set()
        base = self.repo / "data" / "v1_baseline"
        if not base.exists():
            return keys, comps
        for name in ("competencies", "tasks", "proficiency", "indicators", "family_assignments", "ethical_lenses",
                     "sector_applications", "structure", "exposure_sources", "exposure_summary", "craft_stage_reform"):
            p = base / f"{name}.csv"
            if p.exists():
                for row in L.read_csv(p):
                    keys.add(row["key"])
                    if name == "competencies":
                        comps.add(row["key"])
        p = base / "source_text" / "indicators.csv"
        if p.exists():
            keys.update(r["key"] for r in L.read_csv(p))
        return keys, comps

    def _copyb_sha(self):
        p = self.repo / "data" / "v1_baseline" / "BUILD_INFO.json"
        if not p.exists():
            return None
        info = json.loads(p.read_text(encoding="utf-8"))
        return next((i["sha256"] for i in info.get("inputs", []) if i.get("role") == "baseline"), None)

    def v1key_ok(self, key: str) -> bool:
        if key in self.v1keys:
            return True
        m = re.match(r"^(v1:[1-7]\.\d{1,2}\.\d{1,2})(?::(.+))?$", key)
        if not m or m.group(1) not in self.v1_competencies:
            return False
        rest = m.group(2)
        if rest is None:
            return True
        return bool(re.fullmatch(r"(T[1-3](:[a-z0-9_]+)?|L[1-5]|F\d{1,2}|stage|craft|reform|cld|"
                                 r"(foundational|intermediate|advanced|expert)(:I\d{1,2})?|sector:[a-z_]+)", rest))

    # ------------------------------------------------------------------ helpers
    def is_held(self, rid, rec=None):
        if rid in self.hold["keys"]:
            return True
        rec = rec if rec is not None else (self.records.get(rid, (None, None))[1])
        if not isinstance(rec, dict):
            return False
        return rec.get("indigenousDataFlag") is True and rec.get("approvalStatus") != "approved"

    def held_by_lineage(self, rec) -> bool:
        """Does this record descend from held v1 content (ADR-0007 §D; v1 dispositions hold-for-tribal-review)?"""
        for d in (rec.get("provenance") or {}).get("derivedFrom") or []:
            key = d.get("v1Key", "")
            m = re.match(r"^v1:([1-7]\.\d{1,2}\.\d{1,2})(?::(.*))?$", key)
            if not m:
                continue
            if m.group(1) in self.hold["v1"] and d.get("relation") != "reference-only":
                return True
            if m.group(2) and m.group(2) in self.hold["lens"]:
                return True
        if rec.get("type") == "RelevanceRating" and rec.get("objectScheme") == "v1-ethical-lens":
            obj = str(rec.get("object", ""))
            if any(obj.endswith(":" + lens) or obj.endswith("/" + lens) for lens in self.hold["lens"]):
                return True
        return False

    # ------------------------------------------------------------------ pass 1: per-record
    def run(self) -> Report:
        for loc, rec in L.iter_records(self.data):
            self.check_record(loc, rec)
        self.check_duplicates_and_index()
        self.check_io_lint()
        self.check_cross_record()
        self.check_registry()
        self.check_crosswalks()
        self.check_all_files()
        self.stats()
        return self.r

    def check_record(self, loc, rec):
        if isinstance(rec, Exception):
            self.r.add("E-PARSE", loc, f"cannot parse: {rec}")
            return
        if not isinstance(rec, dict):
            self.r.add("E-PARSE", loc, "record is not a mapping")
            return
        rid, typ = rec.get("id"), rec.get("type")
        self._pending_index.append((rid, loc, rec))
        # schema
        errs = sorted(self.validator.iter_errors(rec), key=lambda e: (list(e.absolute_path), e.message))
        for e in errs[:8]:
            path = "/".join(str(p) for p in e.absolute_path) or "(root)"
            self.r.add("E-SCHEMA", loc, f"{path}: {e.message[:300]}", rid)
        if len(errs) > 8:
            self.r.add("E-SCHEMA", loc, f"... {len(errs) - 8} more schema errors", rid)
        if typ not in L.ENTITY:
            return
        self.check_location(loc, rec)
        self.check_id(loc, rec)
        self.check_computed(loc, rec)
        self.check_computed_paths(loc, rec)
        self.check_personal(loc, rec)
        self.check_governed(loc, rec)
        self.check_hash(loc, rec)
        self.check_lint(loc, rec)
        self.check_provenance(loc, rec)
        self.check_semantics(loc, rec)
        if typ == "Pathway" and rec.get("recommended") is True:
            self.r.add("E-PATHWAY-RECOMMENDED", loc, "no pathway may be labelled recommended before the M-03 gate (ADR-0023, ADR-0027)", rid)
        if loc.area not in ("core", "register", "other") and typ in ("Competency", "Task") \
                and rec.get("validationStatus") != "seed-v1" and not rec.get("subsectors"):
            self.r.add("E-MODULE-SUBSECTOR", loc, "module records must cite at least one subsector code (WP-06; ADR-0018)", rid)
        if typ == "Enactment" and rec.get("enactmentKind") == "module" and not rec.get("subsectors") \
                and rec.get("status") not in LIVE_EXCLUDED_STATUSES:
            code = "E-MODULE-SUBSECTOR" if rec.get("status") in AT_OR_AFTER_CANDIDATE else "W-MODULE-SUBSECTOR"
            self.r.add(code, loc, "module enactments cite at least one subsector code in `subsectors` (CR-DB-001 #2; ADR-0030)", rid)

    def check_semantics(self, loc, rec):
        """Record-level rules from the ADR-0029 rulings that JSON Schema cannot express cleanly."""
        rid, typ, status = rec.get("id"), rec.get("type"), rec.get("status")
        # §1.3 no seed-v1 at candidate. Seed-keyed superseded/withdrawn v1 stubs (never minted) are exempt (CR-DE-004, kept by ADR-0030 §1.1).
        if rec.get("validationStatus") == "seed-v1" and status in SEED_V1_FORBIDDEN \
                and (status in AT_OR_AFTER_CANDIDATE or (isinstance(rid, str) and rid.startswith("emst:"))):
            self.r.add("E-SEED-CANDIDATE", loc, f"seed-v1 content cannot be {status}: rewrite it as a draft and review it first (ADR-0029 §1.3; ADR-0030 §1.1)", rid)
        # §8.2 interim EMST-* notation schemes (pre-ADR-0029 encoding of typed fields)
        interim = sorted({n.get("scheme") for n in rec.get("notation") or []
                          if isinstance(n, dict) and str(n.get("scheme", "")).startswith("EMST-")})
        if interim:
            code = "E-NOTATION-INTERIM" if status in AT_OR_AFTER_CANDIDATE else "W-NOTATION-INTERIM"
            self.r.add(code, loc, f"interim notation scheme(s) {', '.join(interim)}: move each value to its typed field (ADR-0029 §8; AUTHORING_GUIDE §12)", rid)
        if typ == "ChangeSignal":
            self._check_signal(loc, rec)
        elif typ == "ExposureAssessment":
            for i, te in enumerate(rec.get("technicalExposure") or []):
                dist = te.get("levelDistribution") if isinstance(te, dict) else None
                if isinstance(dist, dict) and dist:
                    tot = sum(v for v in dist.values() if isinstance(v, (int, float)))
                    if abs(tot - 1.0) > 0.01:
                        self.r.add("E-LEVEL-DISTRIBUTION", loc, f"technicalExposure[{i}].levelDistribution sums to {tot:.3f}, not 1 ± 0.01 (ADR-0029 §9.2)", rid)
            if str(rec.get("targetId", "")).startswith("mvp-role:"):
                self.r.add("W-MVP-ROLE-TARGET", loc, "targetId mvp-role:… is a placeholder; re-key to the RoleProfile/RoleVariant seed key (excluded from releases)", rid)
        elif typ == "DriverEvent":
            if rec.get("eventType") == "submitted-for-review" and rec.get("statusAfter") in IN_FORCE_STATUSES:
                self.r.add("E-REVIEW-EVENT-STATUS", loc, f"a submitted-for-review event cannot put an instrument {rec.get('statusAfter')} (use under-review; ADR-0029 §8.2)", rid)
        elif typ in ("RoleProfile", "RoleVariant") and isinstance(rid, str) and rid.startswith("seed:"):
            self._check_role_key(loc, rid, typ)
        if typ == "DriverEvent" and rec.get("actingInstrument") and rec.get("actingInstrument") == rec.get("instrument"):
            self.r.add("E-ACTING-SELF", loc, "actingInstrument names the event's own instrument (ADR-0030)", rid)
        if typ in ("Enactment", "RoleVariant"):
            self._check_instrument_links(loc, rec)
        if typ in ("Task", "Competency"):
            for i, e in enumerate(rec.get("instrumentSensitivity") or []):
                if not isinstance(e, dict):
                    continue
                if e.get("evidenceLabel") in ("J", "S") and not e.get("reviewBy") and status in AT_OR_AFTER_CANDIDATE:
                    self.r.add("E-EDGE-REVIEWBY", loc, f"instrumentSensitivity[{i}] ({e.get('mechanism')}) is labelled {e.get('evidenceLabel')} and needs reviewBy (ADR-0030)", rid)
                if e.get("reviewBy") and str(e["reviewBy"]) < self.today:
                    self.r.add("W-EDGE-REVIEW-OVERDUE", loc, f"instrumentSensitivity[{i}] ({e.get('mechanism')}) review was due {e['reviewBy']}", rid)
        if typ == "Pathway":
            for j, stp in enumerate(rec.get("sequence") or []):
                tasks = set(stp.get("tasks") or []) if isinstance(stp, dict) else set()
                for prov in (stp.get("formationProvisions") or []) if isinstance(stp, dict) else []:
                    if isinstance(prov, dict) and prov.get("task") not in tasks:
                        self.r.add("E-PROVISION-TASK", loc, f"sequence[{j}] formation provision for {prov.get('task')} is not one of that step's tasks", rid)

    def _check_instrument_links(self, loc, rec):
        rid, status = rec.get("id"), rec.get("status")
        field = "characteristicInstruments" if rec.get("type") == "Enactment" else "instruments"
        seen = Counter()
        missing = []
        for item in rec.get(field) or []:
            if not isinstance(item, dict):
                continue                                  # schema reports the shape (run scripts/convert_instrument_links.py)
            seen[item.get("instrument")] += 1
            if not item.get("role"):
                missing.append(item.get("instrument"))
        for ins, n in sorted(seen.items(), key=lambda kv: str(kv[0])):
            if n > 1:
                self.r.add("E-INSTRUMENT-LINK-DUPLICATE", loc, f"{field} lists {ins} {n} times; one link per instrument", rid)
        if missing and status not in LIVE_EXCLUDED_STATUSES:
            code = "E-INSTRUMENT-ROLE-MISSING" if status in AT_OR_AFTER_CANDIDATE else "W-INSTRUMENT-ROLE-MISSING"
            self.r.add(code, loc, f"{len(missing)} {field} link(s) without a role (requires | enables | constrains | removed-requirement); untyped links decide nothing (ADR-0030)", rid)

    def _check_signal(self, loc, rec):
        rid = rec.get("id")
        st = rec.get("signalStatus")
        key = rec.get("independenceKey")
        if key is None:
            key = next((n.get("value") for n in rec.get("notation") or [] if isinstance(n, dict) and n.get("scheme") == "EMST-independenceKey"), None)
        if st in ("active", "watch") and key and key not in self.independence_keys:
            code = "E-INDEPENDENCE-KEY-UNLISTED" if st == "active" else "W-INDEPENDENCE-KEY-UNLISTED"
            self.r.add(code, loc, f"independenceKey {key!r} is not listed in vocab/change_types.yaml#independence_keys (file a CR to LM/CA)", rid)
        if rec.get("targetType") == "organization":
            actor = rec.get("sectorActor")
            tid = str(rec.get("targetId", ""))
            if rec.get("tribalPrograms") is True or actor in self.tribal_actors or rec.get("indigenousDataFlag") is True \
                    or re.search(r"tribal|tribe|nation\b|pueblo|rancheria|band of", tid, re.I):
                self.r.add("E-ORG-TARGET-TRIBAL", loc, "organization targets are never Tribal governments, organizations or enterprises (ADR-0007 V3; CR-LM-001)", rid)
            n = (rec.get("measure") or {}).get("n")
            if isinstance(n, int) and n < 5:
                self.r.add("W-ORG-SMALL-N", loc, f"organization measure with n = {n} < 5 is suppressed in releases (ADR-0012)", rid)
        if str(rec.get("targetId", "")).startswith("mvp-role:"):
            self.r.add("W-MVP-ROLE-TARGET", loc, "targetId mvp-role:… is a placeholder; re-key to the RoleProfile/RoleVariant seed key (excluded from releases)", rid)
        sps = set(rec.get("scenarioSignposts") or []) | {n.get("value") for n in rec.get("notation") or []
                                                         if isinstance(n, dict) and n.get("scheme") == "EMST-signpost"}
        if sps & {"vocab:scenarios#SP-12", "SP-12"}:
            self.r.add("I-SP12-QUARANTINE", loc, "reads signpost SP-12 (Tribal Council only): quarantined like careFlag, excluded from releases and never counted (ER-0)", rid)

    def _check_role_key(self, loc, rid, typ):
        body = rid[len("seed:"):]
        parts = body.split("/")
        ok = (typ == "RoleProfile" and len(parts) == 1) or \
             (typ == "RoleVariant" and len(parts) in (2, 3) and parts[1] in self.sector_actor_terms)
        if not ok:
            want = "seed:<role_key>" if typ == "RoleProfile" else "seed:<role_key>/<sector_actor>[/<slice>]"
            self.r.add("W-ROLE-KEY", loc, f"{typ} seed key should be {want} (CR-IA-001; AUTHORING_GUIDE §3)", rid)
        elif self.role_keys and parts[0] not in self.role_keys:
            self.r.add("W-ROLE-KEY", loc, f"role_key {parts[0]!r} is not in docs/decisions/mvp_role_set.csv", rid)

    def check_location(self, loc, rec):
        rid, typ = rec.get("id"), rec.get("type")
        kind, where = L.ENTITY[typ]["store"]
        p = loc.path
        if kind in ("yaml", "yaml-register"):
            if p.suffix != ".yaml" and not (kind == "yaml-register" and p.suffix == ".jsonl"):
                self.r.add("E-LOCATION", loc, f"{typ} records are stored one per YAML file", rid)
                return
            if p.suffix == ".yaml":
                if loc.dir_type != typ:
                    self.r.add("E-LOCATION", loc, f"{typ} record in a directory for {loc.dir_type or 'unknown type'}; expected .../{where}/", rid)
                if isinstance(rid, str) and L.is_record_ref(rid) and p.stem != L.id_to_stem(rid):
                    self.r.add("E-LOCATION", loc, f"file name must be {L.id_to_stem(rid)}.yaml", rid)
            if kind == "yaml" and loc.area == "register":
                self.r.add("E-LOCATION", loc, f"{typ} records live under core/ or modules/<ns>/", rid)
            if kind == "yaml-register" and loc.area != "register":
                self.r.add("E-LOCATION", loc, f"{typ} records live under registers/{where}/", rid)
        elif kind == "jsonl":
            rel = p.relative_to(self.data).parts
            if p.suffix != ".jsonl" or rel[0] != where:
                self.r.add("E-LOCATION", loc, f"{typ} records live in data/v2/{where}/…/*.jsonl", rid)
        mod = rec.get("module")
        if loc.area == "core" and kind == "yaml" and mod != "core":
            self.r.add("E-LOCATION", loc, f"record under core/ must have module: core (has {mod!r})", rid)
        if loc.area not in ("core", "register", "other") and mod != loc.area:
            self.r.add("E-LOCATION", loc, f"record under modules/{loc.area}/ must have module: {loc.area} (has {mod!r})", rid)
        if loc.area not in ("core", "register", "other") and not L.namespace_ok(loc.area):
            self.r.add("E-ID-NAMESPACE", loc, f"modules/{loc.area}/ is not a registered namespace (vocab/identifiers.yaml)", rid)

    def check_id(self, loc, rec):
        rid, typ = rec.get("id"), rec.get("type")
        if not isinstance(rid, str):
            return
        if rid.startswith("emst:"):
            if not L.id_regex().match(rid):
                return  # schema reports the pattern
            ns, prefix, code = L.id_parts(rid)
            if not L.luhn32_valid(code):
                self.r.add("E-ID-CHECK", loc, f"check symbol of {rid} is invalid (Luhn mod-32)", rid)
            want = L.ENTITY[typ]["prefix"]
            if prefix != want:
                self.r.add("E-ID-PREFIX", loc, f"{typ} IDs use TYPE {want}, not {prefix}", rid)
            if not L.namespace_ok(ns):
                self.r.add("E-ID-NAMESPACE", loc, f"namespace {ns!r} is not registered", rid)
            if loc.area not in ("core", "register", "other") and ns != loc.area:
                code_ = "E-MODULE-REDEFINES-CORE" if ns == "core" else "E-ID-NAMESPACE"
                self.r.add(code_, loc, f"module {loc.area} may only define IDs minted in its own namespace (found {ns})", rid)

    def check_computed(self, loc, rec):
        rid, typ = rec.get("id"), rec.get("type")
        for path, k, _v in L.walk(rec):
            if k in self.computed_names:
                self.r.add("E-COMPUTED-FIELD", loc, f"computed field {'/'.join(map(str, path + (k,)))} is not allowed in source records (SPEC §14.2; ADR-0021)", rid)
            if not path and k in self.inverse.get(typ, set()):
                if k in self.transitional.get(typ, set()) and rec.get("status") == "draft":
                    self.r.add("W-COMPUTED-FIELD-DEPRECATED", loc, f"{k} on {typ} is now a computed inverse (ADR-0029 §1.2): remove it before candidate; the build ignores it", rid)
                else:
                    self.r.add("E-COMPUTED-FIELD", loc, f"{k} on {typ} is an inverse link computed in bundles; store the link on the other side", rid)

    def check_computed_paths(self, loc, rec):
        for dotted in self.computed_paths.get(rec.get("type"), []):
            head, _, leaf = dotted.rpartition(".")
            node = rec.get(head) if head else rec
            for item in (node if isinstance(node, list) else [node]):
                if isinstance(item, dict) and leaf in item:
                    self.r.add("E-COMPUTED-FIELD", loc, f"{dotted} is computed (State Class View) and never stored (ADR-0030; RULINGS_FOR_DE §19.4)", rec.get("id"))

    def check_personal(self, loc, rec):
        rid = rec.get("id")
        for path, k, _v in L.walk(rec):
            if k in self.pd_keys and not (path and path[-1] in ("measure", "hypothesizedEntity")):
                self.r.add("E-PERSONAL-DATA", loc, f"person-level field {'/'.join(map(str, path + (k,)))} (ADR-0012 I-1)", rid)
        for path, s in L.iter_strings(rec):
            self._personal_text(loc, s, rid, "/".join(map(str, path)))

    def _personal_text(self, loc, s, rid=None, where=""):
        for name, rx in self.pd_pats.items():
            for m in rx.finditer(s):
                if name == "email" and m.group(0) in self.pd_allow:
                    continue
                self.r.add("E-PERSONAL-DATA", loc, f"{name} pattern at {where or 'text'}: {m.group(0)[:40]!r} (ADR-0012 I-1)", rid)

    def check_governed(self, loc, rec):
        rid = rec.get("id")
        strings = list(L.iter_strings(rec))
        text = "\n".join(s for _, s in strings)
        for rx in self.confidential:
            if rx.search(text):
                self.r.add("E-CONFIDENTIAL", loc, f"confidential-information marker {rx.pattern!r}: EMST must not hold confidential Tribal information (ADR-0007 V2)", rid)
        has_coords = any(rx.search(text) for rx in self.coord_pats) or any(k in self.coord_keys for _, k, _ in L.walk(rec))
        if has_coords and any(rx.search(text) for rx in self.cultural):
            self.r.add("E-COORDS-CULTURAL", loc, "coordinates co-occur with cultural-site vocabulary (ADR-0007 V2; P-TN-02)", rid)
        flagged = rec.get("indigenousDataFlag") is True and rec.get("approvalStatus") in ("pending-tribal-review", "withdrawn") \
            and rec.get("sensitivity") == "restricted-governed"
        must_hold = (rid in self.hold["keys"]) or self.held_by_lineage(rec)
        if must_hold and not flagged:
            self.r.add("E-TRIBAL-HOLD", loc, "held under ADR-0007 §D: set indigenousDataFlag: true, approvalStatus: pending-tribal-review, sensitivity: restricted-governed", rid)
        if not rec.get("indigenousDataFlag"):
            hits = set()
            for path, s in strings:
                if any(p in self.tribal_skip for p in path if isinstance(p, str)):
                    continue
                if path and path[0] in ("id", "type", "license", "status", "module", "layer"):
                    continue
                for rx in self.tribal_triggers:
                    m = rx.search(s)
                    if m:
                        hits.add(m.group(0).lower())
            if hits:
                releasable = rec.get("status") in RELEASABLE_STATUSES
                code = "E-TRIBAL-LEAK" if (releasable or self.strict) else "W-TRIBAL-LEAK"
                self.r.add(code, loc, f"Tribal-related text ({', '.join(sorted(hits))}) in an unflagged record: route to TN (gate G-TN) and flag or rewrite (ADR-0007 §D)", rid)

    def check_hash(self, loc, rec):
        if rec.get("type") != "Task":
            return
        st = (rec.get("statement") or {}).get("en")
        if isinstance(st, str) and rec.get("textSha256") and rec["textSha256"] != L.text_sha256(st):
            self.r.add("E-TEXT-HASH", loc, f"textSha256 does not match the normalized statement (expected {L.text_sha256(st)})", rec.get("id"))

    def check_lint(self, loc, rec):
        rid, typ = rec.get("id"), rec.get("type")
        seed = rec.get("validationStatus") == "seed-v1"
        sev = "W" if seed else "E"
        fields = self.tlex["applies_to"].get(typ, [])
        for f in fields:
            for s in _lang_values(rec.get(f)):
                for term, rx in self.products:
                    if rx.search(s):
                        self.r.add(f"{sev}-LINT-TYPING", loc, f"{f} names an L4 product {term!r} (ADR-0003 T-1/T-4): name the function, move the product to L4", rid)
                if typ != "Enactment":
                    for term, rx in self.instruments:
                        if rx.search(s):
                            self.r.add(f"{sev}-LINT-TYPING", loc, f"{f} names an L5 instrument {term!r} (ADR-0003 T-4/T-7): write regulation-neutral text; link the instrument in L5", rid)
        if typ == "Indicator" and self.io_lint is None:
            self._fallback_indicator_lint(loc, rec)
        if typ == "Competency":
            s = (rec.get("statement") or {}).get("en", "")
            if L.word_count(s) > 60:
                self.r.add(f"{sev}-LINT-LENGTH", loc, f"statement has {L.word_count(s)} words (max 60, ADR-0003 G-1)", rid)
        if typ == "Task":
            s = (rec.get("statement") or {}).get("en", "")
            n = L.word_count(s)
            if n and not 8 <= n <= 30:
                self.r.add(f"{sev}-LINT-LENGTH", loc, f"task statement has {n} words (8–30, ADR-0003 G-2)", rid)
            if re.match(r"^\s*\w+\s+(and|or)\s+\w+\b", s):
                self.r.add(f"{sev}-LINT-LENGTH", loc, "compound verb at start of task statement (G-2: one verb per task)", rid)

    def _fallback_indicator_lint(self, loc, rec):
        """B1-B12 from schema/lint/indicator_lint.yaml; used only when IO's linter is unavailable."""
        if rec.get("type") != "Indicator":
            return
        rid = rec.get("id")
        seed = rec.get("validationStatus") == "seed-v1"
        sev = "W" if seed else "E"
        for s in _lang_values(rec.get("statement")):
            for rule, rx in self.ilint_rules:
                rsev = "W" if (seed or rule.get("severity") == "warning") else "E"
                if rx is not None and rx.search(s):
                    self.r.add(f"{rsev}-LINT-INDICATOR", loc, f"{rule['id']} {rule['name']}: {rule['fix']}", rid)
                if rule.get("lexicon") == "products":
                    for term, trx in self.products:
                        if trx.search(s):
                            self.r.add(f"{rsev}-LINT-INDICATOR", loc, f"{rule['id']} names product {term!r}: {rule['fix']}", rid)
                if rule.get("lexicon") == "instruments":
                    for term, trx in self.instruments:
                        if trx.search(s):
                            self.r.add(f"{rsev}-LINT-INDICATOR", loc, f"{rule['id']} names instrument {term!r}: {rule['fix']}", rid)
            if L.word_count(s) > 30:
                self.r.add(f"{sev}-LINT-LENGTH", loc, f"indicator has {L.word_count(s)} words (max 30)", rid)

    def check_provenance(self, loc, rec):
        rid, typ = rec.get("id"), rec.get("type")
        prov = rec.get("provenance") or {}
        if not isinstance(prov, dict):
            return
        # agent output is draft evidence (PHASE4_BUILD_PLAN §1.2; ADR-0024 §5)
        if prov.get("method") == "llm-assisted" and prov.get("reviewStatus") in ("unreviewed", "spot-checked"):
            if typ in L.RATING_TYPES and prov.get("evidenceLabel") != "S":
                self.r.add("E-LLM-DRAFT", loc, "LLM-assisted, unreviewed ratings must carry evidenceLabel S until a human reviews them", rid)
            if rec.get("validationStatus") not in (None, "draft", "seed-v1"):
                self.r.add("E-LLM-DRAFT", loc, f"LLM-assisted, unreviewed content cannot claim validationStatus {rec.get('validationStatus')!r}", rid)
        if rec.get("raterType") == "llm" and rec.get("evidenceLabel") != "S" and prov.get("reviewStatus") in ("unreviewed", "spot-checked", None):
            self.r.add("E-LLM-DRAFT", loc, "raterType llm values carry evidence label S until reviewed", rid)
        for sid in sorted(set(prov.get("sources") or []) | set(rec.get("sources") or [])):
            if isinstance(sid, str) and not L.is_record_ref(sid) and sid not in self.source_ids:
                self.r.add("E-SOURCE-UNRESOLVED", loc, f"source {sid!r} does not resolve to any docs/**/sources.csv or key-facts row", rid)
        v1_text = False
        for d in prov.get("derivedFrom") or []:
            key = d.get("v1Key")
            if key and self.v1keys and not self.v1key_ok(key):
                self.r.add("E-V1KEY-UNRESOLVED", loc, f"derivedFrom v1Key {key!r} does not resolve to data/v1_baseline/", rid)
            if d.get("workbookSha256") and self.copyb_sha and d["workbookSha256"] != self.copyb_sha:
                self.r.add("E-V1-WORKBOOK-HASH", loc, "derivedFrom.workbookSha256 is not the copyB baseline hash (BUILD_INFO.json)", rid)
            if d.get("relation") in ("carried", "recovered"):
                v1_text = True
            elif d.get("relation") in ("rewritten", "split-from", "merged-from") and rec.get("license") == "CC0-1.0" \
                    and self.licensing["v1Dedication"] != "granted" and typ in ("Competency", "Task", "Indicator", "KnowledgeStatement", "Enactment"):
                self.r.add("W-LICENSE-V1-REWRITE", loc, "CC0-1.0 on text derived from v1: confirm no v1 wording survives (ADR-0013; lead's Q2 pending)", rid)
        if v1_text and self.licensing["v1Dedication"] != "granted" and rec.get("license") == "CC0-1.0" \
                and typ not in L.RATING_TYPES:
            self.r.add("E-LICENSE-V1", loc, f"v1-derived text must carry {V1_LICENSE} until the lead's CC0 dedication (ADR-0013; Q2)", rid)

    # ------------------------------------------------------------------ pass 2: cross-record
    def check_duplicates_and_index(self):
        for rid, loc, rec in self._pending_index:
            if not isinstance(rid, str):
                continue
            if rid in self.records:
                prev_loc, prev = self.records[rid]
                code = "E-ID-DUPLICATE"
                if prev_loc.area == "core" and loc.area not in ("core", "register", "other"):
                    code = "E-MODULE-REDEFINES-CORE"
                elif loc.area == "core" and prev_loc.area not in ("core", "register", "other"):
                    code = "E-MODULE-REDEFINES-CORE"
                self.r.add(code, loc, f"id {rid} is already defined in {prev_loc}", rid)
                continue
            self.records[rid] = (loc, rec)
            self.by_type[rec.get("type")].append(rid)

    def _refs(self, rec):
        own = rec.get("id")
        for path, s in L.iter_strings(rec):
            if not path or path[0] in ("id", "provenance"):
                continue
            if any(p in ("v1Seed", "v1Values") for p in path if isinstance(p, str)):
                continue
            if s == own:
                continue
            if path[0] == "outcome" and s.startswith("promoted-to:"):
                s = s[len("promoted-to:"):]
            if L.is_record_ref(s):
                yield tuple(p for p in path if isinstance(p, str)), s

    def check_cross_record(self):
        task_supported = set()
        for rid, (loc, rec) in self.records.items():
            typ = rec.get("type")
            if typ == "Task" and rec.get("status") not in LIVE_EXCLUDED_STATUSES:
                for c in _get_path(rec, "supports.competency"):
                    task_supported.add(c)
            for path, ref in self._refs(rec):
                dotted = ".".join(path)
                target = self.records.get(ref)
                if target is None:
                    planned = self.is_planned(ref)
                    if planned and not self.strict:
                        self.r.add("W-REF-PENDING", loc, f"{dotted} -> {ref} is a planned target (v1 disposition, v2.0 candidate or MVP role) not yet authored", rid)
                    else:
                        self.r.add("E-REF-DANGLING", loc, f"{dotted} -> {ref} does not resolve to any record", rid)
                    if (planned or ref in self.hold["keys"]) and path[0] not in LINEAGE_KEYS and self.planned_is_held(ref) \
                            and not self.is_held(rid, rec):
                        self.r.add("E-TRIBAL-INHERIT", loc, f"{dotted} -> {ref} is a held planned reference; this record must be flagged held too (ADR-0007 §D; CR-LC-001)", rid)
                    continue
                tloc, trec = target
                want = TYPED_LINKS.get((typ, dotted))
                if want and trec.get("type") not in want:
                    self.r.add("E-REF-TYPE", loc, f"{dotted} must reference {'/'.join(sorted(want))}, not {trec.get('type')} ({ref})", rid)
                # dependency direction: core content must not depend on module content (SPEC §3.2)
                if loc.area == "core" and loc.path.suffix == ".yaml" and path[0] not in LINEAGE_KEYS \
                        and tloc.area not in ("core", "register", "other"):
                    self.r.add("E-DEPENDENCY-DIRECTION", loc, f"core record depends on module record {ref} via {dotted}", rid)
                if typ == "Task" and dotted == "supports.competency" and trec.get("status") in LIVE_EXCLUDED_STATUSES \
                        and rec.get("status") not in LIVE_EXCLUDED_STATUSES:
                    succ = [x for x in trec.get("replacedBy") or []]
                    if self.is_held(rid, rec) and succ and all(self.is_held(x) or self.planned_is_held(x) for x in succ):
                        self.r.add("I-SUPERSEDED-TARGET-HELD", loc, f"held task supports {ref}, whose successors are all held: re-pointed after a Tribal Advisory Council exists (ADR-0030 §3.2)", rid)
                    else:
                        self.r.add("W-SUPERSEDED-TARGET", loc, f"task supports {ref}, which is {trec.get('status')}: reassign to its successor(s) {trec.get('replacedBy', [])}", rid)
            # hold inheritance
            if not self.is_held(rid, rec):
                for dotted in DEPENDENT_LINKS.get(typ, []):
                    for ref in _get_path(rec, dotted):
                        if self.is_held(ref):
                            self.r.add("E-TRIBAL-INHERIT", loc, f"{dotted} -> {ref} is held content; this record must be flagged held too (ADR-0007 §D)", rid)
            # staleness of ratings
            if typ in L.RATING_TYPES:
                self._stale(loc, rec)
        for rid in self.by_type.get("Competency", []):
            loc, rec = self.records[rid]
            if rec.get("status") in LIVE_EXCLUDED_STATUSES or rid in task_supported:
                continue
            code = "E-COMPETENCY-NO-TASK" if (rec.get("status") in RELEASABLE_STATUSES or self.strict) else "W-COMPETENCY-NO-TASK"
            self.r.add(code, loc, "competency is not supported by any task (SPEC §5.2; ADR-0003 G-1)", rid)
        self.check_pr2()
        self.check_waivers_current()
        self.check_edges_redundant()
        self.check_mirrors()
        self.check_clo_variants()
        self.check_three_module()

    def check_edges_redundant(self):
        """W-EDGE-REDUNDANT (CR-SC-001 #1): a Task edge already carried by a competency the task supports as primary,
        with no sources beyond that competency's edge."""
        for rid in self.by_type.get("Task", []):
            loc, rec = self.records[rid]
            edges = [e for e in rec.get("instrumentSensitivity") or [] if isinstance(e, dict)]
            if not edges:
                continue
            prim = {}
            for sup in rec.get("supports") or []:
                if isinstance(sup, dict) and sup.get("strength") == "primary" and sup.get("competency") in self.records:
                    for e in self.records[sup["competency"]][1].get("instrumentSensitivity") or []:
                        if isinstance(e, dict):
                            prim.setdefault(e.get("mechanism"), set()).update(e.get("sources") or [])
            for e in edges:
                m = e.get("mechanism")
                if m in prim and set(e.get("sources") or []) <= prim[m]:
                    self.r.add("W-EDGE-REDUNDANT", loc, f"edge {m} is inherited from a primary competency; keep task edges task-specific (ADR-0030)", rid)

    def check_mirrors(self):
        """Mirrors live on the authority side only (CR-SC-001 #3): never both directions, never self."""
        listed = {}
        own_enactments = defaultdict(set)
        for eid in self.by_type.get("Enactment", []):
            c = self.records[eid][1].get("competency")
            if c:
                own_enactments[c].add(eid)
        for rid in self.by_type.get("Competency", []):
            listed[rid] = {m.get("target") for m in self.records[rid][1].get("mirrors") or [] if isinstance(m, dict)}
        for rid, targets in listed.items():
            loc, _ = self.records[rid]
            for t in sorted(x for x in targets if x):
                if t == rid or t in own_enactments[rid]:
                    self.r.add("E-MIRROR-SELF", loc, f"mirrors -> {t} is the record itself or one of its own enactments", rid)
                    continue
                back = listed.get(t, set())
                if t in self.records and self.records[t][1].get("type") == "Enactment":
                    back = listed.get(self.records[t][1].get("competency"), set())
                    if rid in back or (back & own_enactments[rid]):
                        self.r.add("E-MIRROR-TWICE", loc, f"mirror {rid} <-> {t} is stored on both sides; keep it on the authority side only", rid)
                elif rid in back or (back & own_enactments[rid]):
                    if rid < t:                       # report each pair once
                        self.r.add("E-MIRROR-TWICE", loc, f"mirror {rid} <-> {t} is stored on both sides; keep it on the authority side only", rid)

    def check_clo_variants(self):
        """E-CLO-ENACTMENT-INDICATOR (CR-LC-001 #4): enactment indicator variants never appear in the competency's levels[]."""
        for eid in self.by_type.get("Enactment", []):
            loc, e = self.records[eid]
            comp = self.records.get(e.get("competency"), (None, {}))[1]
            generic = {i for lv in comp.get("levels") or [] if isinstance(lv, dict) for i in lv.get("indicators") or []}
            for i in sorted(set(e.get("indicatorVariants") or []) & generic):
                self.r.add("E-CLO-ENACTMENT-INDICATOR", loc, f"indicator variant {i} is also listed in {e.get('competency')} levels[]; variants belong to the enactment only", eid)
        for pid in self.by_type.get("Pathway", []):
            loc, rec = self.records[pid]
            outs = list(rec.get("cloOutcomes") or []) + [o for st in rec.get("sequence") or [] if isinstance(st, dict) for o in st.get("cloOutcomes") or []]
            for o in outs:
                if not isinstance(o, dict) or o.get("competency") not in self.records:
                    continue
                c = self.records[o["competency"]][1]
                if c.get("type") == "Competency" and o.get("level") not in {lv.get("level") for lv in c.get("levels") or [] if isinstance(lv, dict)}:
                    self.r.add("E-REF-TYPE", loc, f"cloOutcomes {o['competency']} has no level {o.get('level')} in its levels[] (CR-LC-001 #2)", pid)

    def check_three_module(self):
        """Three-module rule (ADR-0003 G-4; CR-DB-001 #1; ADR-0030 §1.3) and its exception register."""
        p = self.data / THREE_MODULE_REL
        reg = L.load_yaml(p) if p.exists() else {}
        exceptions = {}
        for i, row in enumerate((reg or {}).get("exceptions") or []):
            where = f"{p}:exceptions[{i}]"
            need = ("competency", "modules", "rationale", "decidedBy", "decidedOn", "reviewBy", "decidedIn")
            if not isinstance(row, dict) or any(not row.get(k) for k in need) or not isinstance(row.get("modules"), list) \
                    or not re.match(r"^(pid:|CA$)", str(row.get("decidedBy", ""))):
                self.r.add("E-THREE-MODULE-EXCEPTION-FORMAT", where, f"rows need {', '.join(need)}; decidedBy is pid:… or CA")
                continue
            if str(row["reviewBy"]) < self.today:
                self.r.add("W-THREE-MODULE-EXCEPTION-EXPIRED", where, f"exception for {row['competency']} was due for review {row['reviewBy']}")
            if row["competency"] not in self.records:
                self.r.add("E-REF-DANGLING", where, f"exception names {row['competency']}, which does not resolve")
            exceptions[row["competency"]] = row
        mods = defaultdict(set)
        for eid in self.by_type.get("Enactment", []):
            e = self.records[eid][1]
            if e.get("enactmentKind") == "module" and e.get("status") not in LIVE_EXCLUDED_STATUSES and e.get("enactedInModule"):
                mods[e.get("competency")].add(e["enactedInModule"])
        task_home = defaultdict(set)
        for tid in self.by_type.get("Task", []):
            t = self.records[tid][1]
            if t.get("status") in LIVE_EXCLUDED_STATUSES:
                continue
            for sup in t.get("supports") or []:
                if isinstance(sup, dict):
                    task_home[sup.get("competency")].add(t.get("homeModule") or t.get("module"))
        role_home = defaultdict(set)
        for pid in self.by_type.get("RoleProfile", []):
            r = self.records[pid][1]
            for ct in r.get("competencyTargets") or []:
                if isinstance(ct, dict):
                    role_home[ct.get("competency")].add(r.get("homeModule") or r.get("module"))
        for cid in self.by_type.get("Competency", []):
            loc, c = self.records[cid]
            if c.get("module") != "core" or c.get("competencyType") != "practice" or c.get("status") in LIVE_EXCLUDED_STATUSES:
                continue
            m = mods.get(cid, set())
            if len(m) in (1, 2) and cid not in exceptions:
                code = "E-THREE-MODULE" if c.get("status") in AT_OR_AFTER_CANDIDATE else "W-THREE-MODULE"
                self.r.add(code, loc, f"core practice competency enacted in only {len(m)} module(s) ({', '.join(sorted(m))}): add a third module enactment, move it to its home module, or ask the CA for an exception (ADR-0003 G-4)", cid)
            recurrence = sorted(x for x in (m | task_home.get(cid, set()) | role_home.get(cid, set())) if x and x != "core")
            self.three_module_recurrence[cid] = recurrence
            self.r.add("I-THREE-MODULE-RECURRENCE", loc, f"modules where this competency recurs: {', '.join(recurrence) or '(none)'} ({len(recurrence)})", cid)

    def check_pr2(self):
        """E-PR2-ATTRIBUTE (ADR-0029 §5.4): above the competency's lowest level that has indicators (from levels[]),
        an Indicator at candidate or later states its distinguishingAttribute. PUB-11 (IO) checks the value."""
        order = {lv: i for i, lv in enumerate(self.schema["$defs"]["v_level"]["enum"])}
        lowest = {}
        for cid in self.by_type.get("Competency", []):
            levels = [lv.get("level") for lv in self.records[cid][1].get("levels") or [] if isinstance(lv, dict) and lv.get("indicators")]
            levels = [x for x in levels if x in order]
            if levels:
                lowest[cid] = min(levels, key=order.get)
        for rid in self.by_type.get("Indicator", []):
            loc, rec = self.records[rid]
            if rec.get("status") not in AT_OR_AFTER_CANDIDATE:
                continue
            low = lowest.get(rec.get("competency"))
            lv = rec.get("level")
            if low and lv in order and order[lv] > order[low] and not rec.get("distinguishingAttribute"):
                self.r.add("E-PR2-ATTRIBUTE", loc, f"indicator at {lv} (above {low}, the lowest level of {rec.get('competency')} with indicators) needs distinguishingAttribute (SPEC §8.2 PR-2)", rid)

    def check_waivers_current(self):
        """A waiver applies only while record id, rule id and normalized-text hash all match (IO rules); report voids."""
        if not self.valid_waivers:
            return
        norm = None
        if self.io_lint:
            mod, linter = self.io_lint
            norm = lambda rec: (lambda f: mod.text_sha256(f[0], linter.rules) if f else None)(linter.statement_fields(mod.Record(rec, "")))  # noqa: E731
        for w in self.valid_waivers:
            target = self.records.get(w["record_id"])
            if target is None:
                self.r.add("I-WAIVER-VOID", self.waivers_path, f"waiver {w['record_id']} {w['rule_id']}: record not found")
                continue
            rec = target[1]
            cur = norm(rec) if norm else L.text_sha256(((rec.get("statement") or {}).get("en")) or "")
            if cur and cur != w["text_sha256"]:
                self.r.add("I-WAIVER-VOID", self.waivers_path, f"waiver {w['record_id']} {w['rule_id']}: text changed since the waiver; it no longer applies", w["record_id"])

    def _stale(self, loc, rec):
        pairs = (("task", "taskTextSha256", "task"), ("competency", "competencyTextSha256", "competency"),
                 ("subject", "subjectTextSha256", "subject"))
        for field, hfield, _ in pairs:
            ref, h = rec.get(field), rec.get(hfield)
            if not (ref and h) or ref not in self.records:
                continue
            _, trec = self.records[ref]
            if trec.get("type") == "Task":
                current = trec.get("textSha256")
            elif trec.get("type") == "Competency":
                current = L.competency_text_sha256((trec.get("prefLabel") or {}).get("en", ""), (trec.get("statement") or {}).get("en", ""))
            else:
                continue
            if current and h != current:
                self.r.add("I-STALE-ASSESSMENT", loc, f"rated text hash differs from current {field} text: excluded from computed views until re-rated or re-attested", rec.get("id"))

    # ------------------------------------------------------------------ registry
    def _read_registry(self, path: Path):
        text = path.read_text(encoding="utf-8")
        rows = list(csv.reader(text.splitlines()))
        return rows

    def check_registry(self):
        reg = self.data / "ids" / "registry.csv"
        minted_records = {rid: v for rid, v in self.records.items() if L.is_emst_id(rid) or str(rid).startswith("emst:")}
        if not reg.exists():
            for rid, (loc, _) in minted_records.items():
                self.r.add("E-REGISTRY-MISSING", loc, f"{rid} is not in data/v2/ids/registry.csv (IDs are minted only by scripts/mint_id.py)", rid)
            return
        rows = self._read_registry(reg)
        if not rows or rows[0] != REGISTRY_COLUMNS:
            self.r.add("E-REGISTRY-FORMAT", reg, f"header must be {','.join(REGISTRY_COLUMNS)}")
            return
        body = rows[1:]
        seen = {}
        for i, row in enumerate(body, 2):
            if len(row) != len(REGISTRY_COLUMNS):
                self.r.add("E-REGISTRY-FORMAT", f"{reg}:{i}", "wrong number of columns")
                continue
            d = dict(zip(REGISTRY_COLUMNS, row))
            if not L.is_emst_id(d["id"]):
                self.r.add("E-REGISTRY-FORMAT", f"{reg}:{i}", f"invalid id {d['id']!r} (pattern or check symbol)")
                continue
            ns, prefix, _ = L.id_parts(d["id"])
            if d["namespace"] != ns:
                self.r.add("E-REGISTRY-FORMAT", f"{reg}:{i}", "namespace column does not match the id")
            if d["type"] not in L.ENTITY or L.ENTITY[d["type"]]["prefix"] != prefix:
                self.r.add("E-REGISTRY-FORMAT", f"{reg}:{i}", f"type {d['type']!r} does not match TYPE prefix {prefix}")
            if d["status"] not in REGISTRY_STATUSES:
                self.r.add("E-REGISTRY-FORMAT", f"{reg}:{i}", f"status {d['status']!r} not in {REGISTRY_STATUSES}")
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", d["minted_on"]):
                self.r.add("E-REGISTRY-FORMAT", f"{reg}:{i}", "minted_on must be YYYY-MM-DD")
            if d["id"] in seen:
                self.r.add("E-REGISTRY-FORMAT", f"{reg}:{i}", f"duplicate id {d['id']} (collision or reuse)")
            seen[d["id"]] = d
        for rid, (loc, rec) in minted_records.items():
            d = seen.get(rid)
            if d is None:
                self.r.add("E-REGISTRY-MISSING", loc, f"{rid} is not in the registry (mint with scripts/mint_id.py)", rid)
            elif d["type"] != rec.get("type") and not (d["type"] in L.RATING_TYPES and rec.get("type") in L.RATING_TYPES):
                self.r.add("E-REGISTRY-FORMAT", loc, f"registry type {d['type']} differs from record type {rec.get('type')}", rid)
        for rid, d in seen.items():
            if rid not in self.records and d["status"] != "withdrawn":
                self.r.add("E-REGISTRY-ORPHAN", reg, f"registry id {rid} ({d['status']}) has no record; records are never deleted (SPEC §12.4)")
        base_rows = self._registry_base_rows()
        if base_rows is not None:
            self._append_only(reg, base_rows, body)

    def _registry_base_rows(self):
        if self.registry_base is not None:
            p = Path(self.registry_base)
            if not p.exists():
                return []
            rows = self._read_registry(p)
            return rows[1:] if rows else []
        if not self.use_git_base:
            return None
        rel = (self.data / "ids" / "registry.csv").resolve()
        try:
            relpath = rel.relative_to(self.repo.resolve())
        except ValueError:
            return None
        try:
            out = subprocess.run(["git", "-C", str(self.repo), "show", f"HEAD:{relpath.as_posix()}"],
                                 capture_output=True, text=True, timeout=20)
        except Exception:  # noqa: BLE001
            return None
        if out.returncode != 0:
            return None
        rows = list(csv.reader(out.stdout.splitlines()))
        return rows[1:] if rows else []

    def _append_only(self, reg, base, body):
        immutable = ["id", "type", "namespace", "minted_on", "minted_by"]
        if len(body) < len(base):
            self.r.add("E-REGISTRY-APPEND-ONLY", reg, f"{len(base) - len(body)} registry row(s) deleted; the registry is append-only (SPEC §12.2)")
        for i, (old, new) in enumerate(zip(base, body), 2):
            o, n = dict(zip(REGISTRY_COLUMNS, old)), dict(zip(REGISTRY_COLUMNS, new))
            for c in immutable:
                if o.get(c) != n.get(c):
                    self.r.add("E-REGISTRY-APPEND-ONLY", f"{reg}:{i}", f"column {c} changed ({o.get(c)!r} -> {n.get(c)!r}); only status transitions are allowed")
            if o.get("status") in REGISTRY_TRANSITIONS and n.get("status") not in REGISTRY_TRANSITIONS[o["status"]]:
                self.r.add("E-REGISTRY-TRANSITION", f"{reg}:{i}", f"status {o['status']} -> {n.get('status')} is not an allowed transition")
            if o.get("first_release") and o["first_release"] != n.get("first_release"):
                self.r.add("E-REGISTRY-APPEND-ONLY", f"{reg}:{i}", "first_release is immutable once set")
            if o.get("superseded_by") and o["superseded_by"] != n.get("superseded_by"):
                self.r.add("E-REGISTRY-APPEND-ONLY", f"{reg}:{i}", "superseded_by is immutable once set (IDs are never re-pointed)")

    # ------------------------------------------------------------------ crosswalks
    def check_crosswalks(self):
        cw = self.data / "crosswalks"
        mp = L.load_yaml(self.repo / "vocab" / "mapping_predicates.yaml")
        self.sssom_ext_only = list(mp.get("justifications_sssom_1_1_only") or [])
        self.sssom_ext_counts = {}
        vocab_pred = set(self.schema["$defs"]["v_mappingPredicate"]["enum"])
        vocab_just = set(self.schema["$defs"]["v_mappingJustification"]["enum"])
        tsvs = sorted(cw.rglob("*.sssom.tsv")) if cw.exists() else []
        for tsv in tsvs:
            self._sssom(tsv, vocab_pred, vocab_just)
        x1 = cw / "emst-v1" / "emst-v1_to_v2.sssom.tsv"
        want_x1 = self.check_x1 if self.check_x1 is not None else (self.data.resolve() == L.DATA_V2.resolve() or x1.exists())
        if want_x1:
            self._x1(x1)

    def _sssom_rows(self, tsv: Path):
        lines = [ln for ln in tsv.read_text(encoding="utf-8").splitlines() if ln and not ln.startswith("#")]
        if not lines:
            return [], []
        header = lines[0].split("\t")
        rows = [dict(zip(header, ln.split("\t"))) for ln in lines[1:]]
        return header, rows

    def _sssom(self, tsv, preds, justs):
        header, rows = self._sssom_rows(tsv)
        meta_p = tsv.with_name(tsv.name[: -len(".sssom.tsv")] + ".sssom.yml")
        if not meta_p.exists():
            self.r.add("E-SSSOM-FORMAT", tsv, f"missing metadata file {meta_p.name}")
            meta = {}
        else:
            meta = L.load_yaml(meta_p) or {}
            for k in SSSOM_META_REQUIRED:
                if k not in meta:
                    self.r.add("E-SSSOM-FORMAT", meta_p, f"metadata lacks {k}")
        for c in SSSOM_REQUIRED:
            if c not in header:
                self.r.add("E-SSSOM-FORMAT", tsv, f"missing required column {c}")
        for c in header:
            if c not in SSSOM_COLUMNS:
                self.r.add("E-SSSOM-FORMAT", tsv, f"unknown column {c} (declare SSSOM 1.1 slots as extensions)")
        third_party = not tsv.parent.name.startswith("emst")
        ext_only = set(self.sssom_ext_only)
        agent_set = any(str(x).startswith("emstagent:") for x in (meta.get("creator_id") or []) + (meta.get("author_id") or [])) \
            or "agent-drafted" in str(meta.get("mapping_set_description", "")).lower()
        n_ext = 0
        for i, row in enumerate(rows, 2):
            where = f"{tsv}:{i}"
            just = row.get("mapping_justification")
            other = _parse_other(row.get("other", ""))
            if just in ext_only:
                n_ext += 1
            selection = any(other.get(k) == v for k, v in SELECTION_FLAGS)
            if selection and just == "semapv:LLMBasedMatching":
                self.r.add("E-SSSOM-SELECTION-1_1", where, "row flagged for selection use still carries semapv:LLMBasedMatching: selection needs two human reviewers (ADR-0022; CR-IA-002)")
            if just == "semapv:MappingReview" and row.get("reviewer_id") and "original_justification" not in other \
                    and (agent_set or str(row.get("author_id", "")).startswith("emstagent:")):
                self.r.add("W-SSSOM-REVIEW-PROVENANCE", where, "reviewed agent-drafted row: keep original_justification=semapv:LLMBasedMatching in `other` (CR-IA-002 #3; ADR-0019 §4)")
            if row.get("predicate_id") not in preds:
                self.r.add("E-SSSOM-VALUE", where, f"predicate {row.get('predicate_id')!r} not in vocab/mapping_predicates.yaml")
            if row.get("mapping_justification") not in justs:
                self.r.add("E-SSSOM-VALUE", where, f"justification {row.get('mapping_justification')!r} not in vocab")
            if row.get("predicate_modifier") not in (None, "", "Not"):
                self.r.add("E-SSSOM-VALUE", where, "predicate_modifier must be Not or empty")
            for c in ("confidence", "similarity_score"):
                v = row.get(c)
                if v not in (None, ""):
                    try:
                        if not 0 <= float(v) <= 1:
                            raise ValueError
                    except ValueError:
                        self.r.add("E-SSSOM-VALUE", where, f"{c} must be a number in [0,1]")
            if row.get("object_id") == "sssom:NoTermFound" and row.get("predicate_id") not in ("emst:retiredWithoutReplacement", "emst:replacedBy", "skos:exactMatch", "skos:closeMatch", "skos:broadMatch", "skos:narrowMatch", "skos:relatedMatch"):
                self.r.add("E-SSSOM-VALUE", where, "sssom:NoTermFound used with an unsupported predicate")
            if third_party and meta.get("license", "").startswith("CC0") and row.get("object_label"):
                self.r.add("E-SSSOM-THIRD-PARTY-TEXT", where, "CC0 mapping sets store external IDs only; move upstream labels to external/ (ADR-0013 §5)")
        if n_ext:
            self.sssom_ext_counts[str(tsv.relative_to(self.data)) if tsv.is_relative_to(self.data) else str(tsv)] = n_ext
            self.r.add("I-SSSOM-1_1-EXTENSION", tsv, f"{n_ext} of {len(rows)} rows use SSSOM 1.1-only justification(s) {', '.join(sorted(ext_only))}: valid as 1.0 plus the declared extension; re-validate when 1.1 is final (CR-IA-002)")

    def _x1(self, x1: Path):
        if not x1.exists():
            self.r.add("E-X1-INCOMPLETE", x1, "X1 v1→v2 crosswalk missing (run scripts/migrate_v1.py)")
            return
        _, rows = self._sssom_rows(x1)
        disp = {r["v1_code"]: r["decision"] for r in L.read_csv(L.DISPOSITION)} if L.DISPOSITION.exists() else {}
        comps = sorted(self.v1_competencies)
        tasks = sorted(k for k in self.v1keys if re.fullmatch(r"v1:[1-7]\.\d{1,2}\.\d{1,2}:T[1-3]", k))
        by_subj = defaultdict(list)
        pairs = Counter()
        for i, row in enumerate(rows, 2):
            subj = row.get("subject_id", "")
            key = "v1:" + subj.split(":", 1)[1] if subj.startswith("EMSTv1:") else subj
            by_subj[key].append((i, row))
            pairs[(key, row.get("predicate_id"), row.get("object_id"))] += 1
        for (key, pred, obj), n in pairs.items():
            if n > 1:
                self.r.add("E-X1-DUPLICATE", x1, f"{key} {pred} {obj} appears {n} times")
        for key in comps + tasks:
            if key not in by_subj:
                self.r.add("E-X1-INCOMPLETE", x1, f"v1 key {key} is not accounted for in X1 (P-DE-08)")
        for key, items in by_subj.items():
            decisions = {re.search(r"decision=([a-z-]+)", r.get("comment", "") or "").group(1) if re.search(r"decision=([a-z-]+)", r.get("comment", "") or "") else None for _, r in items}
            if len(decisions) != 1 or None in decisions:
                self.r.add("E-X1-DECISION", x1, f"{key}: rows must carry exactly one decision (found {sorted(map(str, decisions))})")
                continue
            dec = decisions.pop()
            code = key[3:]
            if code in disp and dec != disp[code]:
                self.r.add("E-X1-DECISION", x1, f"{key}: X1 decision {dec} differs from v1_disposition.csv ({disp[code]})")
            for i, row in items:
                obj = row.get("object_id", "")
                if obj == "sssom:NoTermFound" or not L.is_record_ref(obj):
                    continue
                if obj not in self.records:
                    if self.strict:
                        self.r.add("E-REF-DANGLING", f"{x1}:{i}", f"X1 object {obj} for {key} does not resolve")
                    else:
                        self.r.add("W-X1-PENDING", f"{x1}:{i}", f"X1 object {obj} for {key} is not yet authored")
        # every live record that claims v1 lineage must be an X1 object of that key (X1 regenerated after authoring)
        objects = defaultdict(set)
        for key, items in by_subj.items():
            for _, row in items:
                objects[key].add(row.get("object_id"))
        for rid, (loc, rec) in self.records.items():
            if rec.get("status") in LIVE_EXCLUDED_STATUSES or rec.get("type") in L.RATING_TYPES:
                continue
            for d in (rec.get("provenance") or {}).get("derivedFrom") or []:
                key = d.get("v1Key", "")
                if d.get("relation") in ("carried", "rewritten", "split-from", "merged-from") and \
                        re.fullmatch(r"v1:[1-7]\.\d{1,2}\.\d{1,2}(:T[1-3])?", key) and key in by_subj and rid not in objects[key]:
                    self.r.add("E-X1-STALE", loc, f"record derives from {key} but X1 does not map {key} to it: run python scripts/migrate_v1.py --x1-only", rid)

    # ------------------------------------------------------------------ every file under data/v2
    def check_all_files(self):
        record_files = set(L.iter_record_files(self.data))
        for p in sorted(self.data.rglob("*")):
            if not p.is_file() or p in record_files or p.suffix not in (".csv", ".tsv", ".yml", ".yaml", ".md", ".txt", ".json", ".jsonl"):
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            self._personal_text(p, text, None, p.name)
            for rx in self.confidential:
                if rx.search(text):
                    self.r.add("E-CONFIDENTIAL", p, f"confidential-information marker {rx.pattern!r} (ADR-0007 V2)")

    def stats(self):
        live_core = [rid for rid in self.by_type.get("Competency", [])
                     if self.records[rid][1].get("module") == "core"
                     and self.records[rid][1].get("status") not in LIVE_EXCLUDED_STATUSES]
        held = [rid for rid, (_, rec) in self.records.items() if self.is_held(rid, rec)]
        self.r.stats = {
            "records": len(self.records),
            "byType": dict(sorted(Counter(rec.get("type") for _, rec in self.records.values()).items())),
            "liveCoreCompetencies": len(live_core),
            "liveCoreCompetenciesNotHeld": len([r for r in live_core if r not in set(held)]),
            "heldRecords": len(held),
            "sssom11ExtensionRows": dict(sorted(getattr(self, "sssom_ext_counts", {}).items())),
            "lintWaivers": dict(sorted(Counter(w["rule_id"] for w in self.valid_waivers).items())),
            "issues": dict(sorted(self.r.codes().items())),
        }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data-root", type=Path, default=L.DATA_V2)
    ap.add_argument("--strict", action="store_true", help="release mode")
    ap.add_argument("--registry-base", type=Path, help="base copy of registry.csv for the append-only check")
    ap.add_argument("--no-git-base", action="store_true", help="skip the git HEAD registry comparison")
    ap.add_argument("--json", type=Path, help="write the full report as JSON")
    ap.add_argument("--max-print", type=int, default=60, help="issues printed per severity")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)
    v = Validator(args.data_root, strict=args.strict, registry_base=args.registry_base, use_git_base=not args.no_git_base)
    rep = v.run()
    if args.json:
        args.json.write_text(L.dump_json({"stats": rep.stats, "issues": [i.as_dict() for i in rep.issues]}), encoding="utf-8")
    if not args.quiet:
        for sev in ("error", "warning"):
            items = [i for i in rep.issues if i.severity == sev]
            for i in items[: args.max_print]:
                print(f"{i.code:28} {i.where}  {i.message}")
            if len(items) > args.max_print:
                print(f"... {len(items) - args.max_print} more {sev}s (use --json)")
    print(json.dumps(rep.stats, indent=1))
    n_err = len(rep.errors)
    print(f"{'FAIL' if n_err else 'OK'}: {n_err} errors, {len([i for i in rep.issues if i.severity == 'warning'])} warnings")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
