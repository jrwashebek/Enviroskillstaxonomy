#!/usr/bin/env python3
"""Re-cut a release in one command (rc.1 fix pass; DATA_FIX_BRIEF "Sequence" step 3; docs/release/<version>/BUILD.md).

From a clean commit this is the whole re-cut: the build stamp is HEAD, and the build refuses to run if any build
input differs from HEAD. Before the commit exists, pass --pending: the stamp is "<HEAD>+recut-pending-commit", which
claims no clean commit, and the orchestrator re-runs this command from the clean commit before tagging.

Steps (each stops the run on failure):
  1. scripts/build_schema.py --check                       schema and context current with schema/src and vocab/
  2. scripts/build_release.py --profile release            strict validation, then dist/<version>/
  3. the same build again into dist/<version>-twin/ (--no-validate) and a byte-for-byte comparison
  4. pipelines/views/build_views.sh                        WP-08 views the explorer reads (deterministic)
  5. site: EMST_RELEASE_DIR=dist/<version> npm run build   the explorer from this release (runs check-output.mjs)
  6. scripts/release_docs.py --version <version>           RELEASE_NOTES.md, counts.json, delta_v1.json, PATHWAYS.md, BUILD.md
  7. scripts/release_gate.py --run-ci --twin ...           every CI check (pytest, validator, npm test) and the §5 gate:
                                                           GATE_REPORT.md and gate_evidence.json
Usage:
  python scripts/recut_release.py --version 2.0.0-rc.1                 # from the clean commit (the tagging run)
  python scripts/recut_release.py --version 2.0.0-rc.1 --pending       # pre-commit candidate
Options: --as-of YYYY-MM-DD (gate date; default today, UTC), --skip-site, --skip-ci (gate without the CI commands).
Never commits or tags. Licence: Apache-2.0.
"""
from __future__ import annotations

import argparse
import datetime as dt
import filecmp
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
NODE_PATH = "/opt/node22/bin"


def run(cmd, cwd=ROOT, env=None):
    print("$", " ".join(str(c) for c in cmd), flush=True)
    r = subprocess.run([str(c) for c in cmd], cwd=str(cwd), env=env)
    if r.returncode != 0:
        raise SystemExit(f"recut stopped: {' '.join(str(c) for c in cmd)} exited {r.returncode}")


def same_tree(a: Path, b: Path) -> list[str]:
    fa = {p.relative_to(a).as_posix() for p in a.rglob("*") if p.is_file()}
    fb = {p.relative_to(b).as_posix() for p in b.rglob("*") if p.is_file()}
    diff = sorted(fa ^ fb)
    diff += [n for n in sorted(fa & fb) if not filecmp.cmp(a / n, b / n, shallow=False)]
    return diff


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--version", required=True)
    ap.add_argument("--pending", action="store_true", help='stamp "<HEAD>+recut-pending-commit" (pre-commit candidate)')
    ap.add_argument("--as-of", default=dt.datetime.now(dt.timezone.utc).date().isoformat())
    ap.add_argument("--skip-site", action="store_true")
    ap.add_argument("--skip-ci", action="store_true")
    a = ap.parse_args(argv)
    head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    stamp = ["--build-commit", f"{head}+recut-pending-commit"] if a.pending else []
    dist, twin = ROOT / "dist" / a.version, ROOT / "dist" / f"{a.version}-twin"
    env = dict(os.environ)
    env.pop("SOURCE_DATE_EPOCH", None)
    run([PY, "scripts/build_schema.py", "--check"])
    for d in (dist, twin):
        shutil.rmtree(d, ignore_errors=True)
    run([PY, "scripts/build_release.py", "--profile", "release", "--version", a.version, *stamp], env=env)
    run([PY, "scripts/build_release.py", "--profile", "release", "--version", a.version, "--out", twin, "--no-validate", *stamp], env=env)
    diff = same_tree(dist, twin)
    if diff:
        raise SystemExit(f"recut stopped: the two builds differ: {diff[:10]}")
    print(f"determinism: dist/{a.version} and dist/{a.version}-twin are byte-identical")
    run(["bash", "pipelines/views/build_views.sh"])
    if not a.skip_site:
        senv = dict(env, PATH=f"{NODE_PATH}:{env.get('PATH', '')}", EMST_RELEASE_DIR=str(dist), EMST_VERSION=a.version,
                    EMST_PROFILE="release")
        run(["npm", "run", "build"], cwd=ROOT / "site", env=senv)
    run([PY, "scripts/release_docs.py", "--version", a.version])
    run([PY, "scripts/release_gate.py", "--version", a.version, "--as-of", a.as_of, "--twin", twin]
        + ([] if a.skip_ci else ["--run-ci"]))
    print(f"recut done: dist/{a.version} stamped {head + ('+recut-pending-commit' if a.pending else '')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
