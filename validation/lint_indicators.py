#!/usr/bin/env python3
"""EMST v2 indicator lint (WP-11 output 1; reference implementation for DE to wire into CI).

Implements the twelve banned constructions (B01-B12), the publication rules (PUB-01..PUB-14) and the advisories
(A01-A03) defined in validation/indicator_lint_rules.yaml, against record text.

Inputs (any mix; directories are walked):
  *.yaml / *.yml   one record, or a list of records (SPEC §17.1 source layout: data/v2/**/<type>/<ID>.yaml)
  *.json / *.jsonl one record, a list, or one record per line
  *.csv            authoring sheet; one Indicator per row (columns named as the SPEC fields; pipe-separated lists)

Usage:
  python validation/lint_indicators.py data/v2 [--mode ci|release] [--json] [--waivers PATH]
         [--tools-lexicon data/v2/tools/tools.jsonl] [--instrument-lexicon PATH] [--rules PATH]

Exit codes: 0 no failing hits; 1 failing hits; 2 usage or input error.

A lint pass is a screen, not validation: it does not make an indicator observable, assessable or job-related.
Records are never modified. No network access. Standard library + PyYAML only.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

import yaml

HERE = Path(__file__).resolve().parent
DEFAULT_RULES = HERE / "indicator_lint_rules.yaml"
DEFAULT_WAIVERS = HERE / "waivers" / "indicator_lint_waivers.csv"
LEVELS = ["L1", "L2", "L3", "L4", "L5"]
ABBREVIATIONS = ["e.g.", "i.e.", "etc.", "u.s.", "vs.", "approx.", "no.", "fig.", "st.", "dept.", "et al."]


# --------------------------------------------------------------------------------------------------- data classes
@dataclass
class Hit:
    record_id: str
    record_type: str
    rule_id: str
    severity: str  # error | warn | info
    message: str
    match: str = ""
    source: str = ""
    status: str = "open"  # open | waived
    fails: bool = False

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class Record:
    data: dict
    source: str
    rtype: str = field(init=False)
    rid: str = field(init=False)

    def __post_init__(self) -> None:
        self.rtype = str(self.data.get("type") or "Indicator")
        self.rid = str(self.data.get("id") or self.data.get("seed") or self.data.get("indicator_id") or f"{self.source}#?")


# --------------------------------------------------------------------------------------------------- text helpers
def load_rules(path: Path = DEFAULT_RULES) -> dict:
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def normalize(text: str, rules: dict | None = None) -> str:
    text = unicodedata.normalize("NFKC", str(text))
    repl = (rules or {}).get("normalization", {}).get("replace") or {
        "‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-", " ": " "}
    for k, v in repl.items():
        text = text.replace(k, v)
    return re.sub(r"\s+", " ", text).strip()


def text_sha256(text: str, rules: dict | None = None) -> str:
    return hashlib.sha256(normalize(text, rules).encode("utf-8")).hexdigest()


def lang(value: Any, key: str = "en") -> str:
    if value is None:
        return ""
    if isinstance(value, dict):
        v = value.get(key)
        if v is None and value:
            v = next(iter(value.values()))
        return "" if v is None else str(v)
    if isinstance(value, list):
        return " ".join(lang(v, key) for v in value)
    return str(value)


def as_list(value: Any) -> list:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [v.strip() for v in value.split("|") if v.strip()]
    return [value]


def as_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if value is None or value == "":
        return None
    s = str(value).strip().lower()
    if s in {"true", "t", "yes", "y", "1"}:
        return True
    if s in {"false", "f", "no", "n", "0"}:
        return False
    return None


def as_int(value: Any) -> int | None:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def words(text: str) -> list[str]:
    return re.findall(r"[a-z][a-z'\-]*", text.lower())


# --------------------------------------------------------------------------------------------------- linter
class Linter:
    def __init__(self, rules: dict, mode: str = "ci", waivers: list[dict] | None = None,
                 extra_products: Iterable[str] = (), extra_instruments: Iterable[str] = ()):
        if mode not in {"ci", "release"}:
            raise ValueError("mode must be ci or release")
        self.rules = rules
        self.mode = mode
        lex = rules["lexicons"]
        self.verbs = set(lex["verbs"])
        self.decision_alts = set(lex["decision_alternatives"])
        self.doc_verbs = set(lex["documentation_verbs"])
        self.unambiguous = set(lex["unambiguous_verbs"])
        self.grad_remove = sorted(lex["gradation_terms"], key=len, reverse=True)
        self.grad_flag = sorted(lex["gradation_flag_terms"], key=len, reverse=True)
        products = list(lex["vendor_products"]) + [p for p in extra_products if p and len(p) > 2]
        self.product_re = self._alternation(products, case_sensitive=True)
        instruments = [i for i in extra_instruments if i and len(i) > 3]
        self.instrument_re = self._alternation(instruments, case_sensitive=False) if instruments else None
        self.grad_flag_re = self._alternation(self.grad_flag, case_sensitive=False)
        self.compiled: list[tuple[dict, dict, re.Pattern]] = []
        for rule in rules["banned_constructions"]:
            for pat in rule["patterns"]:
                if "regex" not in pat:
                    continue
                flags = 0 if pat.get("case_sensitive") else re.IGNORECASE
                rx = pat["regex"]
                if pat.get("anchor") == "start":
                    rx = r"^(?:" + rx + r")"
                self.compiled.append((rule, pat, re.compile(rx, flags)))
        self.pub = {p["id"]: p for p in rules["publication_rules"]["per_indicator"]}
        self.pub_re = {k: re.compile(v["regex"], re.IGNORECASE) for k, v in self.pub.items() if "regex" in v}
        self.adv = [(a, re.compile(a["regex"], re.IGNORECASE)) for a in rules.get("advisories", [])]
        self.waivers = waivers or []
        self.status_order = rules["publication_rules"]["per_competency_level"][-1]["status_order"]

    @staticmethod
    def _alternation(terms: Iterable[str], case_sensitive: bool) -> re.Pattern:
        terms = sorted({t for t in terms if t}, key=len, reverse=True)
        body = "|".join(re.escape(t) for t in terms) or r"(?!x)x"
        return re.compile(r"(?<![\w-])(?:" + body + r")(?![\w-])", 0 if case_sensitive else re.IGNORECASE)

    # ---------------------------------------------------------------- statement-level rules
    def _applies(self, rule: dict, rtype: str) -> bool:
        return rtype in rule.get("applies_to", ["Indicator"])

    def lint_text(self, text: str, rtype: str = "Indicator", rid: str = "", source: str = "") -> list[Hit]:
        t = normalize(text, self.rules)
        hits: list[Hit] = []
        if not t:
            return hits

        def add(rule_id, sev, msg, m=""):
            hits.append(Hit(rid, rtype, rule_id, sev, msg, m, source))

        for rule, pat, rx in self.compiled:
            if not self._applies(rule, rtype):
                continue
            m = rx.search(t)
            if m:
                add(pat["id"], pat["severity"], f"{rule['id']} {rule['name']}: {rule['fix']}", m.group(0))
        by_id = {r["id"]: r for r in self.rules["banned_constructions"]}
        if self._applies(by_id["B09"], rtype):
            m = self.product_re.search(t)
            if m:
                add("B09a", "error", f"B09 {by_id['B09']['name']}: {by_id['B09']['fix']}", m.group(0))
        if self.instrument_re is not None and self._applies(by_id["B10"], rtype):
            m = self.instrument_re.search(t)
            if m:
                add("B10e", "error", f"B10 {by_id['B10']['name']}: {by_id['B10']['fix']}", m.group(0))
        if rtype == "Indicator":
            hits += self._b07(t, rid, rtype, source, by_id["B07"])
            m = self.grad_flag_re.search(t)
            if m:
                add("B08b", "warn", f"B08 {by_id['B08']['name']}: {by_id['B08']['fix']}", m.group(0))
            for adv, rx in self.adv:
                found = rx.search(t)
                if adv.get("invert"):
                    if not found:
                        add(adv["id"], adv["severity"], f"{adv['id']} {adv['name']}: {adv['rule']}")
                elif found:
                    add(adv["id"], adv["severity"], f"{adv['id']} {adv['name']}: {adv['rule']}", found.group(0))
        return hits

    def _leading_chain(self, toks: list[str]) -> tuple[list[str], str, int] | None:
        if not toks or toks[0] not in self.verbs:
            return None
        chain, i, conj = [toks[0]], 1, None
        while i < len(toks):
            tk = toks[i]
            if tk == ",":
                if i + 1 < len(toks) and toks[i + 1] in ("and", "or"):
                    i += 1
                    continue
                if i + 1 < len(toks) and toks[i + 1] in self.verbs:
                    chain.append(toks[i + 1])
                    i += 2
                    continue
                break
            if tk in ("and", "or"):
                j, c = i + 1, tk
                if tk == "and" and j + 1 < len(toks) and toks[j] == "/" and toks[j + 1] == "or":
                    j, c = j + 2, "and/or"
                if j < len(toks) and toks[j] in self.verbs:
                    chain.append(toks[j])
                    conj = c
                    i = j + 1
                break
            break
        if conj and len(chain) >= 2:
            return chain, conj, i
        return None

    def _b07(self, t: str, rid: str, rtype: str, source: str, rule: dict) -> list[Hit]:
        hits = []
        toks = re.findall(r"[a-z][a-z'\-]*|,|/", t.lower())
        lead = self._leading_chain(toks)
        lead_end_word = None
        msg = f"B07 {rule['name']}: {rule['fix']}"
        if lead:
            chain, conj, _ = lead
            lead_end_word = chain[-1]
            if conj in ("and", "and/or"):
                if not all(v in self.doc_verbs for v in chain[1:]):
                    hits.append(Hit(rid, rtype, "B07a", "error", msg, f" {conj} ".join(chain), source))
            elif not all(v in self.decision_alts for v in chain):
                hits.append(Hit(rid, rtype, "B07b", "warn", msg, " or ".join(chain), source))
        seen_lead = False
        for m in re.finditer(r"\b(?:and then|and)\s+([a-z][a-z\-]*)\b", t.lower()):
            w = m.group(1)
            if lead and not seen_lead and w == lead_end_word:
                seen_lead = True
                continue
            if w in self.unambiguous and w not in self.doc_verbs:
                hits.append(Hit(rid, rtype, "B07c", "warn", msg, m.group(0), source))
                break
        return hits

    def strip_gradation(self, t: str) -> list[str]:
        s = " " + normalize(t, self.rules).lower() + " "
        for term in self.grad_remove:
            s = re.sub(r"(?<![\w-])" + re.escape(term.lower()) + r"(?![\w-])", " ", s)
        return words(s)

    # ---------------------------------------------------------------- record-level rules
    def statement_fields(self, rec: Record) -> list[str]:
        fields = self.rules["record_text_fields"].get(rec.rtype, [])
        return [lang(rec.data.get(f)) for f in fields if rec.data.get(f)]

    def lint_indicator_metadata(self, rec: Record, text: str) -> list[Hit]:
        d, hits = rec.data, []
        voc = self.pub["PUB-03"]["vocab"]

        def add(rule_id, sev, msg, m=""):
            hits.append(Hit(rec.rid, rec.rtype, rule_id, sev, msg, m, rec.source))

        t = normalize(text, self.rules)
        # count sentence ends (terminator followed by a capital) after masking abbreviations
        orig = " " + t + " "
        for ab in ABBREVIATIONS:
            orig = re.sub(re.escape(" " + ab), " abbr", orig, flags=re.IGNORECASE)
        n_sent = len(re.findall(r"[.!?](?=\s+[A-Z(\"'])", orig)) + 1
        if n_sent > 1:
            add("PUB-01", "error", "PUB-01 one sentence: split into separate indicators or move context to metadata.")
        n_words = len(t.split())
        if n_words > 30:
            add("PUB-02", "error", f"PUB-02 length: {n_words} words (max 30).")
        missing = [f for f in ["competency", "level", "augmentationMode", "assessmentMethods", "useClass", "obs4",
                               "jurisdictionVariable", "validationStatus"]
                   if d.get(f) in (None, "", [])]
        if missing:
            add("PUB-03", "error", "PUB-03 required metadata missing: " + ", ".join(missing))
        for f in ["augmentationMode", "useClass", "level", "validationStatus"]:
            v = d.get(f)
            if v not in (None, "") and str(v) not in voc[f]:
                add("PUB-03", "error", f"PUB-03 {f} = {v!r} is not a vocabulary value {voc[f]}")
        obs4 = as_int(d.get("obs4"))
        if d.get("obs4") not in (None, "") and obs4 not in (0, 1, 2, 3):
            add("PUB-03", "error", f"PUB-03 obs4 = {d.get('obs4')!r} is not 0-3")
        use = str(d.get("useClass") or "")
        if obs4 in (0, 1):
            add("PUB-04", "error", "PUB-04 OBS-4 0-1 is never released as an indicator; rewrite as a KnowledgeStatement or delete.")
        if use == "select" and obs4 is not None and obs4 != 3:
            add("PUB-04", "error", "PUB-04 useClass select requires obs4 = 3.")
        if use in ("develop", "describe") and obs4 is not None and obs4 < 2:
            pass  # already reported above
        if use == "develop" and not (as_list(d.get("evidenceTypes")) or as_list(d.get("assessmentMethods"))):
            add("PUB-04", "error", "PUB-04 develop requires an evidence plan (evidenceTypes or assessmentMethods).")
        mode = str(d.get("augmentationMode") or "")
        if mode == "assisted" and not self.pub_re["PUB-05"].search(t):
            add("PUB-05", "warn", "PUB-05 assisted mode: state what the person verifies, against what, and how acceptance or rejection is recorded.")
        if mode == "supervisory" and not self.pub_re["PUB-06"].search(t):
            add("PUB-06", "warn", "PUB-06 supervisory mode: state the monitoring, intervention or override the person performs.")
        if mode == "unaided" and self.pub_re["PUB-08"].search(t):
            add("PUB-08", "warn", "PUB-08 unaided mode but the statement describes AI or automated output; check augmentationMode.",
                self.pub_re["PUB-08"].search(t).group(0))
        jv = as_bool(d.get("jurisdictionVariable"))
        generic = self.pub_re["PUB-07"].search(t)
        if generic and jv is False:
            add("PUB-07", "error", "PUB-07 statement refers to applicable requirements: set jurisdictionVariable = true.", generic.group(0))
        if jv is True and not generic:
            add("PUB-07", "warn", "PUB-07 jurisdictionVariable = true but the statement does not use the generic 'applicable … requirements' phrase.")
        return hits

    def lint_record(self, rec: Record) -> list[Hit]:
        hits: list[Hit] = []
        texts = self.statement_fields(rec)
        for txt in texts:
            hits += self.lint_text(txt, rec.rtype, rec.rid, rec.source)
        if rec.rtype == "Indicator":
            hits += self.lint_indicator_metadata(rec, texts[0] if texts else "")
        return hits

    # ---------------------------------------------------------------- cross-record rules
    def lint_set(self, records: list[Record]) -> list[Hit]:
        hits: list[Hit] = []
        for rec in records:
            hits += self.lint_record(rec)
        inds = [r for r in records if r.rtype == "Indicator"]
        comps = {r.rid: r for r in records if r.rtype == "Competency"}
        by_comp: dict[str, dict[str, list[Record]]] = {}
        for r in inds:
            c, lv = str(r.data.get("competency") or ""), str(r.data.get("level") or "")
            if c and lv:
                by_comp.setdefault(c, {}).setdefault(lv, []).append(r)
        for c, levels in by_comp.items():
            # B08a cross-level adjective-only gradation (needs only indicators)
            for k in range(len(LEVELS) - 1):
                lo, hi = levels.get(LEVELS[k], []), levels.get(LEVELS[k + 1], [])
                for a in lo:
                    sa = self.strip_gradation(lang(a.data.get("statement")))
                    for b in hi:
                        sb = self.strip_gradation(lang(b.data.get("statement")))
                        if sa and sa == sb:
                            hits.append(Hit(b.rid, "Indicator", "B08a", "error",
                                            f"B08 adjective-only gradation: identical to {a.rid} ({LEVELS[k]}) apart from gradation terms; change a named attribute.",
                                            source=b.source))
            for lv, rs in levels.items():
                for r in rs:
                    att = r.data.get("distinguishingAttribute")
                    if att and att not in {"ATT-AUT", "ATT-GUI", "ATT-CPX", "ATT-SCO", "ATT-KNO", "ATT-AUG", "ATT-FOR"}:
                        hits.append(Hit(r.rid, "Indicator", "PUB-11", "error", f"PUB-11 distinguishingAttribute {att!r} is not an L0 attribute.", source=r.source))
            if c not in comps:
                continue
            comp = comps[c].data
            span = comp.get("levelSpan") or {}
            lo_s, hi_s = str(span.get("min") or ""), str(span.get("max") or "")
            declared = {str(l.get("level")): l for l in (comp.get("levels") or []) if isinstance(l, dict)}
            for lv, rs in levels.items():
                if lv not in LEVELS:
                    continue
                if lo_s in LEVELS and hi_s in LEVELS and not (LEVELS.index(lo_s) <= LEVELS.index(lv) <= LEVELS.index(hi_s)):
                    for r in rs:
                        hits.append(Hit(r.rid, "Indicator", "PUB-13", "error", f"PUB-13 level {lv} outside levelSpan {lo_s}-{hi_s} of {c}.", source=r.source))
            for lv in sorted(set(levels) | set(declared)):
                if lv not in LEVELS:
                    continue
                listed = declared.get(lv, {}).get("indicators")
                n = len(listed) if isinstance(listed, list) else len(levels.get(lv, []))
                if not 2 <= n <= 5:
                    hits.append(Hit(c, "Competency", "PUB-10", "error", f"PUB-10 level {lv} has {n} indicators (2-5 required).", source=comps[c].source))
                rs = levels.get(lv, [])
                if any(str(r.data.get("useClass")) in ("develop", "select") for r in rs):
                    n3 = sum(1 for r in rs if as_int(r.data.get("obs4")) == 3)
                    if n3 < 2:
                        published = str(comp.get("status") or "draft") in ("candidate", "published")
                        sev = "error" if (self.mode == "release" and published) else "warn"
                        hits.append(Hit(c, "Competency", "PUB-12", sev, f"PUB-12 assessability (PR-3): level {lv} has {n3} indicators at OBS-4 = 3 (2 required for develop/select).", source=comps[c].source))
                checks = declared.get(lv, {}).get("publicationRuleChecks") or {}
                statuses = [str(r.data.get("validationStatus") or "draft") for r in rs]
                best = max((self.status_order.index(s) for s in statuses if s in self.status_order), default=0)
                for key, need in (("existence", "job-analysis-confirmed"), ("consensus", "panel-retained")):
                    val = checks.get(key)
                    if val is True or str(val).lower() == "pass":
                        if best < self.status_order.index(need):
                            hits.append(Hit(c, "Competency", "PUB-14", "error",
                                            f"PUB-14 publicationRuleChecks.{key} = pass at {lv} without human evidence (needs an indicator at validationStatus >= {need}); agent ratings never satisfy PR-1 or PR-4.",
                                            source=comps[c].source))
        self.apply_waivers(hits, records)
        self.finalize(hits, records)
        return hits

    # ---------------------------------------------------------------- waivers and failure
    def apply_waivers(self, hits: list[Hit], records: list[Record]) -> None:
        texts = {}
        for r in records:
            f = self.statement_fields(r)
            if f:
                texts[r.rid] = text_sha256(f[0], self.rules)
        for h in hits:
            for w in self.waivers:
                if w.get("record_id") != h.record_id:
                    continue
                if w.get("rule_id") not in (h.rule_id, h.rule_id[:3]):
                    continue
                if w.get("text_sha256") != texts.get(h.record_id):
                    continue
                reviewers = [w.get("reviewer") or "", w.get("second_reviewer") or ""]
                if any(x.lower().startswith(("llm", "emstagent:")) for x in reviewers if x):
                    continue
                if h.severity == "error":
                    if w.get("waiver_class") == "false-positive" and all(reviewers):
                        h.status = "waived"
                elif h.severity == "warn" and w.get("waiver_class") in ("accepted-warning", "false-positive") and reviewers[0]:
                    h.status = "waived"

    def finalize(self, hits: list[Hit], records: list[Record]) -> None:
        use = {r.rid: str(r.data.get("useClass") or "") for r in records if r.rtype == "Indicator"}
        flagged_select = set()
        for h in hits:
            if h.status == "waived":
                continue
            if h.severity == "error":
                h.fails = True
            elif h.severity == "warn":
                if use.get(h.record_id) == "select" and not h.rule_id.startswith("PUB-12"):
                    flagged_select.add(h.record_id)
                    h.fails = self.mode == "release"
        for rid in sorted(flagged_select):
            sev = "error" if self.mode == "release" else "warn"
            hits.append(Hit(rid, "Indicator", "PUB-04", sev,
                            "PUB-04 useClass select requires no unwaived lint flags (SPEC §5.3).", fails=self.mode == "release"))


# --------------------------------------------------------------------------------------------------- loading
def _records_from_obj(obj: Any, source: str) -> list[Record]:
    if obj is None:
        return []
    if isinstance(obj, list):
        return [Record(o, source) for o in obj if isinstance(o, dict)]
    if isinstance(obj, dict):
        if "records" in obj and isinstance(obj["records"], list):
            return [Record(o, source) for o in obj["records"] if isinstance(o, dict)]
        return [Record(obj, source)]
    return []


CSV_ALIASES = {"indicator_id": "id", "text": "statement", "v2_indicator": "statement", "competency_ref": "competency",
               "augmentation_mode": "augmentationMode", "use_class": "useClass", "obs4_code": "obs4",
               "jurisdiction_variable": "jurisdictionVariable", "validation_status": "validationStatus",
               "assessment_methods": "assessmentMethods", "evidence_types": "evidenceTypes"}


def load_path(path: Path) -> list[Record]:
    recs: list[Record] = []
    files = [path] if path.is_file() else sorted(p for p in path.rglob("*") if p.is_file())
    for f in files:
        suf = f.suffix.lower()
        try:
            if suf in (".yaml", ".yml"):
                for doc in yaml.safe_load_all(f.read_text(encoding="utf-8")):
                    recs += _records_from_obj(doc, str(f))
            elif suf == ".json":
                recs += _records_from_obj(json.loads(f.read_text(encoding="utf-8")), str(f))
            elif suf == ".jsonl":
                for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                    if line.strip():
                        recs += _records_from_obj(json.loads(line), f"{f}:{i}")
            elif suf == ".csv":
                with open(f, encoding="utf-8", newline="") as fh:
                    for i, row in enumerate(csv.DictReader(fh), 2):
                        row = {CSV_ALIASES.get(k, k): v for k, v in row.items() if k}
                        row.setdefault("type", "Indicator")
                        recs.append(Record(row, f"{f}:{i}"))
        except (yaml.YAMLError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise SystemExit(f"lint_indicators: cannot parse {f}: {exc}")
    return recs


def load_waivers(path: Path | None) -> list[dict]:
    if not path or not path.exists():
        return []
    with open(path, encoding="utf-8", newline="") as fh:
        return [dict(r) for r in csv.DictReader(fh)]


def load_jsonl_names(path: Path | None, fields: list[str], type_filter: set[str] | None = None) -> list[str]:
    if not path or not path.exists():
        return []
    names = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if type_filter and str(obj.get("toolType")) not in type_filter:
            continue
        for fld in fields:
            v = obj.get(fld)
            if isinstance(v, dict):
                names += [str(x) for x in v.values() if isinstance(x, str)]
                names += [str(y) for x in v.values() if isinstance(x, list) for y in x]
            elif isinstance(v, list):
                names += [lang(x) for x in v]
            elif v:
                names.append(str(v))
    return names


# --------------------------------------------------------------------------------------------------- CLI
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--mode", choices=["ci", "release"], default="ci")
    ap.add_argument("--rules", type=Path, default=DEFAULT_RULES)
    ap.add_argument("--waivers", type=Path, default=DEFAULT_WAIVERS)
    ap.add_argument("--tools-lexicon", type=Path, default=None)
    ap.add_argument("--instrument-lexicon", type=Path, default=None)
    ap.add_argument("--json", action="store_true", help="emit a JSON report")
    ap.add_argument("--show-info", action="store_true")
    args = ap.parse_args(argv)
    rules = load_rules(args.rules)
    tools = load_jsonl_names(args.tools_lexicon, ["prefLabel", "productExamples"],
                             {"software-product", "platform", "model", "dataset-product", "instrument-model"})
    instruments = load_jsonl_names(args.instrument_lexicon, ["citation", "prefLabel", "altLabel"])
    linter = Linter(rules, args.mode, load_waivers(args.waivers), tools, instruments)
    records: list[Record] = []
    for p in args.paths:
        if not p.exists():
            print(f"lint_indicators: no such path {p}", file=sys.stderr)
            return 2
        records += load_path(p)
    hits = linter.lint_set(records)
    failing = [h for h in hits if h.fails]
    if args.json:
        summary = {"records": len(records), "hits": len(hits), "failing": len(failing),
                   "by_rule": {}, "mode": args.mode, "ruleset_version": rules.get("version")}
        for h in hits:
            summary["by_rule"][h.rule_id] = summary["by_rule"].get(h.rule_id, 0) + 1
        print(json.dumps({"summary": summary, "hits": [h.as_dict() for h in hits]}, indent=2, ensure_ascii=False))
    else:
        for h in hits:
            if h.severity == "info" and not args.show_info:
                continue
            flag = "FAIL" if h.fails else ("waived" if h.status == "waived" else h.severity)
            m = f" [{h.match}]" if h.match else ""
            print(f"{h.source}: {h.record_id}: {flag} {h.rule_id}{m} {h.message}")
        print(f"lint_indicators: {len(records)} records, {len(hits)} hits, {len(failing)} failing ({args.mode} mode)")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
