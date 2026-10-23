"""Shared helpers for the EMST v2 data pipeline (WP-01/WP-02, DE).

Paths, canonical YAML, text normalization and hashing, the ADR-0010 identifier form (Crockford base32 body with a
Luhn mod-32 check symbol), the entity catalogue (type -> ID prefix, layer, storage location) and record iteration.
Every other v2 script imports this module so that there is one definition of each rule.

Licence: Apache-2.0 (code).
"""
from __future__ import annotations

import csv
import functools
import hashlib
import io
import json
import re
import unicodedata
from pathlib import Path
from typing import Iterator

import yaml

ROOT = Path(__file__).resolve().parents[1]
VOCAB = ROOT / "vocab"
SCHEMA_DIR = ROOT / "schema"
SCHEMA_SRC = SCHEMA_DIR / "src" / "emst.schema.src.yaml"
SCHEMA_OUT = SCHEMA_DIR / "emst.schema.json"
CONTEXT_OUT = SCHEMA_DIR / "emst.context.jsonld"
LINT_DIR = SCHEMA_DIR / "lint"
DATA_V2 = ROOT / "data" / "v2"
V1_BASELINE = ROOT / "data" / "v1_baseline"
REGISTRY = DATA_V2 / "ids" / "registry.csv"
SEED_MAP = DATA_V2 / "ids" / "seed_map.csv"
GOVERNANCE = DATA_V2 / "governance"
X1_DIR = DATA_V2 / "crosswalks" / "emst-v1"
X1_TSV = X1_DIR / "emst-v1_to_v2.sssom.tsv"
X1_YML = X1_DIR / "emst-v1_to_v2.sssom.yml"
DISPOSITION = ROOT / "docs" / "decisions" / "v1_disposition.csv"
CANDIDATES = ROOT / "docs" / "decisions" / "candidate_disposition.csv"

SCHEMA_VERSION = "2.0.0-draft.3"
IRI_BASE = "https://w3id.org/emst/"

# ---------------------------------------------------------------------------------------------------------------
# Canonical YAML / JSON
# ---------------------------------------------------------------------------------------------------------------


class _Dumper(getattr(yaml, "CSafeDumper", yaml.SafeDumper)):
    pass


def _str_representer(dumper, data):
    style = "|" if "\n" in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


_Dumper.add_representer(str, _str_representer)


_BaseLoader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)   # libyaml when available (much faster)


class _Loader(_BaseLoader):
    """SafeLoader with YAML 1.2 booleans: only true/false are booleans, so vocabulary codes such as
    `yes`, `no`, `on`, `off`, `y`, `n` (e.g. crafts.yaml formation_dependency [yes, partial, no]) stay strings."""


_Loader.yaml_implicit_resolvers = {
    k: [(tag, rx) for tag, rx in v if tag != "tag:yaml.org,2002:bool"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.copy().items()
}
_Loader.add_implicit_resolver("tag:yaml.org,2002:bool", re.compile(r"^(?:true|True|TRUE|false|False|FALSE)$"),
                              list("tTfF"))


def load_yaml(path: Path):
    with open(path, encoding="utf-8") as fh:
        return yaml.load(fh, Loader=_Loader)  # noqa: S506 - SafeLoader subclass


def load_yaml_text(text: str):
    return yaml.load(text, Loader=_Loader)  # noqa: S506


def dump_yaml(obj) -> str:
    """Canonical YAML: insertion order kept, UTF-8, no line wrapping, block style."""
    return yaml.dump(obj, Dumper=_Dumper, sort_keys=False, allow_unicode=True, width=100000,
                     default_flow_style=False)


def write_yaml(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_yaml(obj), encoding="utf-8")


def dump_json(obj, indent: int | None = 1) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=indent, sort_keys=False) + ("\n" if indent is not None else "")


def jsonl_line(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=False, separators=(",", ":"))


def write_jsonl(path: Path, rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(jsonl_line(r) + "\n" for r in rows), encoding="utf-8")


def read_csv(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def csv_text(header: list[str], rows: list[dict], delimiter: str = ",") -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=header, delimiter=delimiter, lineterminator="\n", extrasaction="raise")
    w.writeheader()
    for r in rows:
        w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in header})
    return buf.getvalue()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


# ---------------------------------------------------------------------------------------------------------------
# Text normalization and hashes (SPEC §5.5 textSha256; §5.12 taskTextSha256)
# ---------------------------------------------------------------------------------------------------------------


def normalize_text(s: str) -> str:
    """NFC, whitespace collapsed to single spaces, trimmed. The rated/hashed form of every statement."""
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s or "")).strip()


def text_sha256(s: str) -> str:
    return sha256_bytes(normalize_text(s).encode("utf-8"))


def competency_text_sha256(label: str, statement: str) -> str:
    """Hash pinned by competency-level ratings: normalized 'label\\nstatement'."""
    return sha256_bytes((normalize_text(label) + "\n" + normalize_text(statement)).encode("utf-8"))


def word_count(s: str) -> int:
    return len(normalize_text(s).split()) if s else 0


# ---------------------------------------------------------------------------------------------------------------
# Identifiers (ADR-0010; vocab/identifiers.yaml)
# ---------------------------------------------------------------------------------------------------------------

CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
SEED_RE = re.compile(r"^seed:[A-Za-z0-9][A-Za-z0-9._/-]{0,119}$")
SEED_PATTERN = SEED_RE.pattern


@functools.lru_cache(maxsize=None)
def _vocab_identifiers() -> dict:
    return load_yaml(VOCAB / "identifiers.yaml")


@functools.lru_cache(maxsize=None)
def id_regex() -> re.Pattern:
    return re.compile(_vocab_identifiers()["form"]["regex"])


def luhn32_check(body: str) -> str:
    """Luhn mod-32 check symbol over the Crockford alphabet (generation: rightmost body symbol doubled)."""
    factor, total = 2, 0
    for ch in reversed(body):
        addend = factor * CROCKFORD.index(ch)
        factor = 1 if factor == 2 else 2
        total += addend // 32 + addend % 32
    return CROCKFORD[(32 - total % 32) % 32]


def luhn32_valid(code: str) -> bool:
    """Validate body+check (7 symbols)."""
    if not code or any(c not in CROCKFORD for c in code):
        return False
    factor, total = 1, 0
    for ch in reversed(code):
        addend = factor * CROCKFORD.index(ch)
        factor = 2 if factor == 1 else 1
        total += addend // 32 + addend % 32
    return total % 32 == 0


def encode_body(n: int, length: int = 6) -> str:
    return "".join(CROCKFORD[(n >> (5 * i)) & 31] for i in reversed(range(length)))


def is_emst_id(s) -> bool:
    if not isinstance(s, str):
        return False
    if not id_regex().match(s):
        return False
    return luhn32_valid(s.rsplit("-", 1)[1])


def is_seed(s) -> bool:
    return isinstance(s, str) and bool(SEED_RE.match(s))


def is_record_ref(s) -> bool:
    return is_emst_id(s) or is_seed(s)


def id_parts(emst_id: str) -> tuple[str, str, str]:
    """emst:<ns>/<TYPE>-<code> -> (ns, TYPE, code)."""
    ns, local = emst_id[len("emst:"):].split("/", 1)
    typ, code = local.rsplit("-", 1)
    return ns, typ, code


def iri(emst_id: str) -> str:
    if is_emst_id(emst_id):
        return IRI_BASE + emst_id[len("emst:"):]
    if is_seed(emst_id):
        return IRI_BASE + "seed/" + emst_id[len("seed:"):]
    return emst_id


def id_to_stem(rid: str) -> str:
    if is_seed(rid):
        return "seed-" + rid[len("seed:"):].replace("/", "--")
    if rid.startswith("emst:"):
        return rid.split("/", 1)[1]
    raise ValueError(f"not a record id: {rid!r}")


# ---------------------------------------------------------------------------------------------------------------
# Entity catalogue (SPEC §5; vocab/competency_types.yaml#entity_kinds; vocab/identifiers.yaml#types)
# store: ("yaml", <dir>) one record per file under core/ or modules/<ns>/;
#        ("yaml-register", <dir>) one record per file under registers/<dir>/;
#        ("jsonl", <family>) line-oriented files.
# ---------------------------------------------------------------------------------------------------------------

ENTITY = {
    "VocabularyTerm": {"prefix": "VOC", "layers": ["L0"], "store": ("vocab", None)},
    "Competency": {"prefix": "CMP", "layers": ["L1"], "store": ("yaml", "competencies")},
    "Indicator": {"prefix": "IND", "layers": ["L1"], "store": ("yaml", "indicators")},
    "Enactment": {"prefix": "ENA", "layers": ["L1"], "store": ("yaml", "enactments")},
    "Task": {"prefix": "TSK", "layers": ["L2"], "store": ("yaml", "tasks")},
    "KnowledgeStatement": {"prefix": "KNW", "layers": ["L2"], "store": ("yaml", "knowledge")},
    "RoleProfile": {"prefix": "ROL", "layers": ["L3"], "store": ("yaml", "roles")},
    "RoleVariant": {"prefix": "VAR", "layers": ["L3"], "store": ("yaml", "variants")},
    "JobFamily": {"prefix": "FAM", "layers": ["L3"], "store": ("yaml", "families")},
    "Pathway": {"prefix": "PTH", "layers": ["L3", "learning"], "store": ("yaml", "pathways")},
    "Tool": {"prefix": "TL", "layers": ["L4"], "store": ("jsonl", "tools")},
    "ExposureAssessment": {"prefix": "ASM", "layers": ["L5"], "store": ("jsonl", "assessments")},
    "CraftRating": {"prefix": "ASM", "layers": ["L5"], "store": ("jsonl", "assessments")},
    "FunctionRating": {"prefix": "ASM", "layers": ["L5"], "store": ("jsonl", "assessments")},
    "RelevanceRating": {"prefix": "ASM", "layers": ["L5"], "store": ("jsonl", "assessments")},
    "ChangeSignal": {"prefix": "SIG", "layers": ["L5"], "store": ("jsonl", "signals")},
    "WatchItem": {"prefix": "WCH", "layers": ["L5"], "store": ("yaml", "watch-items")},
    "Instrument": {"prefix": "INS", "layers": ["L5"], "store": ("jsonl", "instruments")},
    "DriverEvent": {"prefix": "EVT", "layers": ["L5"], "store": ("jsonl", "events")},
    "FrictionRecord": {"prefix": "FRC", "layers": ["L5"], "store": ("yaml", "frictions")},
    "Credential": {"prefix": "CRD", "layers": ["L6"], "store": ("yaml-register", "credentials")},
    "SeriesRecord": {"prefix": "SER", "layers": ["L6"], "store": ("yaml-register", "opm_series")},
    "StateClassRecord": {"prefix": "SCR", "layers": ["L6"], "store": ("yaml-register", "state_classes")},
    "Mapping": {"prefix": "MAP", "layers": ["L6"], "store": ("sssom", "crosswalks")},
    "LearningResource": {"prefix": "LRN", "layers": ["learning"], "store": ("yaml", "learning-resources")},
    "Bundle": {"prefix": "BND", "layers": ["learning"], "store": ("yaml", "bundles")},
    "Source": {"prefix": "SRC", "layers": ["provenance"], "store": ("yaml", "sources")},
    "ChangeRecord": {"prefix": "CHG", "layers": ["provenance"], "store": ("jsonl", "changes")},
}
YAML_DIR_TO_TYPE = {v["store"][1]: k for k, v in ENTITY.items() if v["store"][0] in ("yaml", "yaml-register")}
JSONL_FAMILIES = {"tools": {"Tool"}, "assessments": {"ExposureAssessment", "CraftRating", "FunctionRating",
                                                     "RelevanceRating"},
                  "signals": {"ChangeSignal"}, "events": {"DriverEvent"}, "changes": {"ChangeRecord"},
                  "instruments": {"Instrument"}}
RATING_TYPES = {"ExposureAssessment", "CraftRating", "FunctionRating", "RelevanceRating"}


@functools.lru_cache(maxsize=None)
def exposure_level_order() -> list[str]:
    """Intensity order of technical-exposure levels (CR-IO-003; ADR-0029 §7). Views and distributions sort E-levels
    by this order, never by code order (E0 < E2 < E1 < E3)."""
    ex = load_yaml(VOCAB / "exposure_instrument_v2.yaml")
    return list(ex["constructs"]["technical_exposure"]["ordinal_order"])


def prefix_entity_map() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for t, e in ENTITY.items():
        if e["prefix"]:
            out.setdefault(e["prefix"], []).append(t)
    return out


@functools.lru_cache(maxsize=None)
def registered_namespaces() -> frozenset[str]:
    return frozenset({n["namespace"] for n in _vocab_identifiers()["namespaces"]["registered"]})


def namespace_ok(ns: str) -> bool:
    return ns in registered_namespaces() or bool(re.match(r"^tribal-[a-z][a-z0-9-]{1,23}$", ns))


# ---------------------------------------------------------------------------------------------------------------
# Record iteration
# ---------------------------------------------------------------------------------------------------------------


class Loc:
    """Where a record came from: file, optional JSONL line, and the namespace/module directory it sits in."""

    def __init__(self, path: Path, line: int | None, area: str, dir_type: str | None):
        self.path, self.line, self.area, self.dir_type = path, line, area, dir_type

    def __str__(self):
        rel = self.path.relative_to(ROOT) if self.path.is_absolute() and ROOT in self.path.parents else self.path
        return f"{rel}:{self.line}" if self.line else str(rel)


def _area_for(path: Path, base: Path) -> tuple[str, str | None]:
    """Return (area, dir_type) for a YAML record path: area 'core' | '<ns>' (module) | 'register'."""
    rel = path.relative_to(base).parts
    if rel[0] == "core" and len(rel) >= 3:
        return "core", YAML_DIR_TO_TYPE.get(rel[1])
    if rel[0] == "modules" and len(rel) >= 4:
        return rel[1], YAML_DIR_TO_TYPE.get(rel[2])
    if rel[0] == "registers" and len(rel) >= 3:
        return "register", YAML_DIR_TO_TYPE.get(rel[1])
    return "other", None


def iter_record_files(base: Path = DATA_V2) -> Iterator[Path]:
    for sub in ("core", "modules", "registers"):
        d = base / sub
        if d.exists():
            yield from sorted(p for p in d.rglob("*.yaml") if p.is_file())
    for fam in JSONL_FAMILIES:
        d = base / fam
        if d.exists():
            yield from sorted(p for p in d.rglob("*.jsonl") if p.is_file())
    d = base / "registers"
    if d.exists():
        yield from sorted(p for p in d.rglob("*.jsonl") if p.is_file())


def iter_records(base: Path = DATA_V2) -> Iterator[tuple[Loc, object]]:
    """Yield (Loc, record) for every source record under base. Parse errors are yielded as (Loc, Exception)."""
    seen = set()
    for p in iter_record_files(base):
        if p in seen:
            continue
        seen.add(p)
        if p.suffix == ".yaml":
            area, dir_type = _area_for(p, base)
            try:
                yield Loc(p, None, area, dir_type), load_yaml(p)
            except Exception as e:  # noqa: BLE001
                yield Loc(p, None, area, dir_type), e
        else:
            rel = p.relative_to(base).parts
            area = "register" if rel[0] == "registers" else "core"
            with open(p, encoding="utf-8") as fh:
                for i, line in enumerate(fh, 1):
                    if not line.strip():
                        continue
                    try:
                        yield Loc(p, i, area, None), json.loads(line)
                    except Exception as e:  # noqa: BLE001
                        yield Loc(p, i, area, None), e


def walk(obj, path=()):
    """Yield (path, key, value) for every dict entry at any depth."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield path, k, v
            yield from walk(v, path + (k,))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, path + (i,))


def iter_strings(obj, path=()):
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from iter_strings(v, path + (k,))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from iter_strings(v, path + (i,))
