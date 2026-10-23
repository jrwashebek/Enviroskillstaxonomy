#!/usr/bin/env python3
"""The single writer of EMST persistent IDs (ADR-0010 §2; SPEC §12.2).

IDs have the form emst:<namespace>/<TYPE>-<6 Crockford base32><1 Luhn mod-32 check>. Bodies are 30 random bits
from the operating system CSPRNG (`secrets`). Every minted ID is appended to the append-only registry
data/v2/ids/registry.csv (id,type,namespace,minted_on,minted_by,status,superseded_by,first_release); a body that
already exists in the namespace × type is rejected and re-drawn. IDs are minted only when a record reaches
`candidate`; drafts keep `seed:` keys. IDs are never reused and never re-pointed.

Commands
  promote <seed-key | record.yaml> --by AGENT   mint an ID for a draft record, set status candidate, rename the file,
                                                rewrite every reference to the seed key under data/v2, log seed_map.csv
  mint --type Competency --namespace core --by AGENT [--count N]   mint bare IDs (testing, bulk reservation)
  transition <ID> --to published [--release 2.0.0-rc.1] [--superseded-by ID] --by AGENT   registry status change
  verify                                         check every registry row (pattern, check symbol, uniqueness)

Options: --registry PATH and --data-root DIR (tests use temporary copies).
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import os
import re
import secrets
import sys
from contextlib import contextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emstlib as L  # noqa: E402

COLUMNS = ["id", "type", "namespace", "minted_on", "minted_by", "status", "superseded_by", "first_release"]
TRANSITIONS = {"candidate": {"published", "withdrawn"}, "published": {"deprecated", "superseded", "withdrawn"},
               "deprecated": {"superseded", "withdrawn"}, "superseded": set(), "withdrawn": set()}
AGENT_RE = re.compile(r"^(emstagent:[A-Za-z0-9._@/+-]{2,80}|pid:[a-z0-9][a-z0-9-]{3,40})$")


class MintError(Exception):
    pass


@contextmanager
def registry_lock(registry: Path):
    """Exclusive lock (O_EXCL lock file) so there is exactly one writer at a time."""
    lock = registry.with_name(registry.name + ".lock")
    registry.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as e:
        raise MintError(f"registry is locked by another writer ({lock}); remove the lock only if no mint is running") from e
    try:
        os.write(fd, str(os.getpid()).encode())
        yield
    finally:
        os.close(fd)
        lock.unlink(missing_ok=True)


def read_registry(registry: Path) -> list[dict]:
    if not registry.exists():
        return []
    with open(registry, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    return rows


def ensure_registry(registry: Path) -> None:
    if not registry.exists() or registry.stat().st_size == 0:
        registry.parent.mkdir(parents=True, exist_ok=True)
        registry.write_text(",".join(COLUMNS) + "\n", encoding="utf-8")
    else:
        header = registry.read_text(encoding="utf-8").splitlines()[0]
        if header != ",".join(COLUMNS):
            raise MintError(f"unexpected registry header in {registry}: {header}")


def draw(namespace: str, prefix: str, existing: set[str]) -> str:
    """Draw a fresh ID; re-draw on collision with any existing ID in the namespace × type."""
    for _ in range(1000):
        body = L.encode_body(secrets.randbits(30))
        rid = f"emst:{namespace}/{prefix}-{body}{L.luhn32_check(body)}"
        if rid not in existing:
            return rid
    raise MintError("could not draw a unique ID in 1000 attempts (namespace × type nearly full?)")


def _append_rows(registry: Path, rows: list[dict]) -> None:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\n")
    for r in rows:
        w.writerow({k: r.get(k, "") for k in COLUMNS})
    with open(registry, "a", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())


def mint(entity_type: str, namespace: str, by: str, count: int = 1, registry: Path = L.REGISTRY,
         today: str | None = None) -> list[str]:
    if entity_type not in L.ENTITY:
        raise MintError(f"unknown entity type {entity_type!r}")
    prefix = L.ENTITY[entity_type]["prefix"]
    if prefix is None:
        raise MintError(f"{entity_type} has no TYPE prefix in vocab/identifiers.yaml; it keeps a seed: key (CR-DE-002)")
    if not L.namespace_ok(namespace):
        raise MintError(f"namespace {namespace!r} is not registered in vocab/identifiers.yaml")
    if not AGENT_RE.match(by or ""):
        raise MintError("--by must be a pseudonymous ID (pid:...) or software agent (emstagent:...)")
    today = today or dt.date.today().isoformat()
    with registry_lock(registry):
        ensure_registry(registry)
        existing = {r["id"] for r in read_registry(registry)}
        new = []
        for _ in range(count):
            rid = draw(namespace, prefix, existing)
            existing.add(rid)
            new.append(rid)
        _append_rows(registry, [{"id": rid, "type": entity_type, "namespace": namespace, "minted_on": today,
                                 "minted_by": by, "status": "candidate", "superseded_by": "", "first_release": ""}
                                for rid in new])
    return new


def transition(rid: str, to: str, by: str, registry: Path = L.REGISTRY, release: str | None = None,
               superseded_by: str | None = None) -> None:
    if not AGENT_RE.match(by or ""):
        raise MintError("--by must be a pseudonymous ID or software agent")
    with registry_lock(registry):
        rows = read_registry(registry)
        hit = [r for r in rows if r["id"] == rid]
        if not hit:
            raise MintError(f"{rid} is not in the registry")
        r = hit[0]
        if to not in TRANSITIONS.get(r["status"], set()):
            raise MintError(f"{r['status']} -> {to} is not allowed")
        if to == "superseded":
            if not superseded_by or not L.is_emst_id(superseded_by):
                raise MintError("--superseded-by must name the successor's EMST ID")
            r["superseded_by"] = superseded_by
        if to == "published" and release:
            if r["first_release"]:
                raise MintError("first_release is already set")
            r["first_release"] = release
        r["status"] = to
        text = ",".join(COLUMNS) + "\n"
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\n")
        for row in rows:
            w.writerow({k: row.get(k, "") for k in COLUMNS})
        registry.write_text(text + buf.getvalue(), encoding="utf-8")


def verify(registry: Path = L.REGISTRY) -> list[str]:
    problems, seen = [], set()
    rx = L.id_regex()
    for i, r in enumerate(read_registry(registry), 2):
        rid = r.get("id", "")
        if not rx.match(rid):
            problems.append(f"line {i}: {rid!r} does not match the ID pattern")
            continue
        ns, prefix, code = L.id_parts(rid)
        if not L.luhn32_valid(code):
            problems.append(f"line {i}: {rid} has an invalid check symbol")
        if rid in seen:
            problems.append(f"line {i}: duplicate {rid}")
        seen.add(rid)
        if r.get("namespace") != ns:
            problems.append(f"line {i}: namespace column {r.get('namespace')!r} != {ns}")
        if L.ENTITY.get(r.get("type"), {}).get("prefix") != prefix:
            problems.append(f"line {i}: type {r.get('type')!r} does not use prefix {prefix}")
    return problems


# ---------------------------------------------------------------------------------------------------------------
# promote: draft (seed key) -> candidate (minted ID)
# ---------------------------------------------------------------------------------------------------------------

def _find_record(key_or_path: str, data_root: Path):
    p = Path(key_or_path)
    if p.suffix == ".yaml" and p.exists():
        return p, L.load_yaml(p)
    if not L.is_seed(key_or_path):
        raise MintError(f"{key_or_path!r} is neither a seed key nor a record file")
    for loc, rec in L.iter_records(data_root):
        if isinstance(rec, dict) and rec.get("id") == key_or_path:
            if loc.line:
                raise MintError(f"{key_or_path} is a line-oriented record ({loc}); promote JSONL records with their batch")
            return loc.path, rec
    raise MintError(f"no record with id {key_or_path}")


def _ref_regex(seed: str) -> re.Pattern:
    return re.compile(r"(?<![A-Za-z0-9._/:-])" + re.escape(seed) + r"(?![A-Za-z0-9._/-])")


def rewrite_references(seed: str, new_id: str, data_root: Path) -> list[Path]:
    """Replace every whole-token occurrence of a seed key with the minted ID across data/v2 text files."""
    rx = _ref_regex(seed)
    changed = []
    for p in sorted(data_root.rglob("*")):
        if not p.is_file() or p.suffix not in (".yaml", ".jsonl", ".tsv", ".csv", ".yml") or p.parent.name == "ids":
            continue
        text = p.read_text(encoding="utf-8")
        new_text = rx.sub(new_id, text)
        if new_text != text:
            p.write_text(new_text, encoding="utf-8")
            changed.append(p)
    return changed


def promote(key_or_path: str, by: str, data_root: Path = L.DATA_V2, registry: Path | None = None,
            namespace: str | None = None, today: str | None = None) -> tuple[str, Path]:
    registry = registry or (data_root / "ids" / "registry.csv")
    path, rec = _find_record(key_or_path, data_root)
    seed = rec.get("id")
    if not L.is_seed(seed):
        raise MintError(f"{path} already has a persistent ID ({seed})")
    if rec.get("status") != "draft":
        raise MintError(f"only draft records are promoted (status is {rec.get('status')!r})")
    if rec.get("indigenousDataFlag") is True and rec.get("approvalStatus") != "approved":
        raise MintError("held Tribal-related content is never promoted to candidate before Tribal Council approval (ADR-0007 §D)")
    if rec.get("validationStatus") == "seed-v1":
        raise MintError("v1 seed records must be authored (validationStatus draft) before they become candidates")
    ns = namespace or rec.get("module")
    new_id = mint(rec["type"], ns, by, registry=registry, today=today)[0]
    rewrite_references(seed, new_id, data_root)
    rec = L.load_yaml(path)
    rec["id"] = new_id
    rec["status"] = "candidate"
    new_path = path.with_name(L.id_to_stem(new_id) + ".yaml")
    L.write_yaml(new_path, rec)
    if new_path != path:
        path.unlink()
    seed_map = data_root / "ids" / "seed_map.csv"
    if not seed_map.exists():
        seed_map.write_text("seed_key,id,minted_on,minted_by\n", encoding="utf-8")
    with open(seed_map, "a", encoding="utf-8", newline="") as fh:
        csv.writer(fh, lineterminator="\n").writerow([seed, new_id, today or dt.date.today().isoformat(), by])
    return new_id, new_path


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--registry", type=Path)
    ap.add_argument("--data-root", type=Path, default=L.DATA_V2)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("promote")
    p.add_argument("record")
    p.add_argument("--by", required=True)
    p.add_argument("--namespace")
    m = sub.add_parser("mint")
    m.add_argument("--type", required=True)
    m.add_argument("--namespace", required=True)
    m.add_argument("--by", required=True)
    m.add_argument("--count", type=int, default=1)
    t = sub.add_parser("transition")
    t.add_argument("id")
    t.add_argument("--to", required=True)
    t.add_argument("--by", required=True)
    t.add_argument("--release")
    t.add_argument("--superseded-by")
    sub.add_parser("verify")
    args = ap.parse_args(argv)
    registry = args.registry or (args.data_root / "ids" / "registry.csv")
    try:
        if args.cmd == "mint":
            for rid in mint(args.type, args.namespace, args.by, args.count, registry):
                print(rid)
        elif args.cmd == "promote":
            rid, path = promote(args.record, args.by, args.data_root, registry, args.namespace)
            print(f"{rid}  {path}")
        elif args.cmd == "transition":
            transition(args.id, args.to, args.by, registry, args.release, args.superseded_by)
            print(f"{args.id} -> {args.to}")
        elif args.cmd == "verify":
            problems = verify(registry)
            for x in problems:
                print(x)
            print(f"{'FAIL' if problems else 'OK'}: {len(read_registry(registry))} registry rows")
            return 1 if problems else 0
    except MintError as e:
        print(f"mint_id: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
