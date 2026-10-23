#!/usr/bin/env python3
"""Fetch O*NET reference data for X2 (EMST task -> O*NET task/DWA) into a local cache OUTSIDE the CC0 data tree.

O*NET content is CC BY 4.0 (U.S. DOL/ETA). EMST CC0 files store O*NET IDs only (ADR-0013 §5); task text is kept
in the cache (default: $EMST_ONET_CACHE or ~/.cache/emst/onet) with attribution and is never committed.

Sources
  31.0  https://www.onetcenter.org/dl_files/database/db_31_0_text.zip  (target release, Aug 2026; V3-01/V4-08)
        Files used: Task Statements.txt, Tasks to DWAs.txt, DWA Reference.txt, Occupation Data.txt.
        STATUS 2026-10-23: onetcenter.org is refused by this session's egress proxy (403); run where it is reachable.
  27.2  O*NET 27.2 task statements as redistributed with the Eloundou et al. labels (openai/GPTs-are-GPTs @
        0471612f, data/full_onet_data.tsv, sha256 f169a958...). ADR-0022 requires an explicit mapping to the 27.x
        tasks on which Eloundou labels sit; this pool also serves until 31.0 is reachable.
Usage: python pipelines/onet/fetch_onet.py [--release 31.0|27.2] [--cache DIR]
Writes <cache>/<release>/MANIFEST.json with URL, sha256, retrieval time and licence. Licence: Apache-2.0.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import os
import sys
import urllib.request
import zipfile
from pathlib import Path

SOURCES = {
    "31.0": {"url": "https://www.onetcenter.org/dl_files/database/db_31_0_text.zip", "sha256": None,
             "members": ["Task Statements.txt", "Tasks to DWAs.txt", "DWA Reference.txt", "Occupation Data.txt"]},
    "27.2": {"url": "https://raw.githubusercontent.com/openai/GPTs-are-GPTs/0471612fef3cc22b74fb884d27bff9dbd3770582/data/full_onet_data.tsv",
             "sha256": "f169a9581462188ae4be77361c3355c443a16d6901df7964a317f3ad060d9f43", "members": None},
}
ATTRIBUTION = ("This product includes information from the O*NET Database by the U.S. Department of Labor, Employment "
               "and Training Administration (USDOL/ETA), used under the CC BY 4.0 license. O*NET is a trademark of "
               "USDOL/ETA. EMST has modified some or all of the information; USDOL/ETA has not approved, endorsed or "
               "tested these modifications.")


def default_cache():
    return Path(os.environ.get("EMST_ONET_CACHE", Path.home() / ".cache" / "emst" / "onet"))


def fetch(release: str, cache: Path) -> Path:
    src = SOURCES[release]
    out = cache / release
    out.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(src["url"], timeout=120) as r:
        data = r.read()
    sha = hashlib.sha256(data).hexdigest()
    if src["sha256"] and sha != src["sha256"]:
        raise SystemExit(f"hash mismatch for {release}: {sha}")
    files = {}
    if src["members"]:
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            names = {Path(n).name: n for n in z.namelist()}
            for m in src["members"]:
                b = z.read(names[m])
                (out / m).write_bytes(b)
                files[m] = hashlib.sha256(b).hexdigest()
    else:
        (out / "full_onet_data.tsv").write_bytes(data)
        files["full_onet_data.tsv"] = sha
    man = {"release": release, "url": src["url"], "sha256": sha, "files": files,
           "retrieved": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "license": "CC-BY-4.0",
           "attribution": ATTRIBUTION}
    (out / "MANIFEST.json").write_text(json.dumps(man, indent=1))
    return out


def load_tasks(release: str, cache: Path | None = None):
    """Return list of {onetsoc, task_id, task, task_type} for a cached release."""
    import csv
    base = (cache or default_cache()) / release
    if release == "27.2":
        rows = csv.DictReader(open(base / "full_onet_data.tsv", encoding="utf-8"), delimiter="\t")
        return [{"onetsoc": r["O*NET-SOC Code"], "task_id": str(int(float(r["Task ID"]))), "task": r["Task"],
                 "task_type": r.get("Task Type", "")} for r in rows]
    rows = csv.DictReader(open(base / "Task Statements.txt", encoding="utf-8"), delimiter="\t")
    return [{"onetsoc": r["O*NET-SOC Code"], "task_id": r["Task ID"], "task": r["Task"],
             "task_type": r.get("Task Type", "")} for r in rows]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--release", default="31.0", choices=sorted(SOURCES))
    ap.add_argument("--cache", type=Path, default=default_cache())
    a = ap.parse_args()
    try:
        out = fetch(a.release, a.cache)
    except Exception as e:  # noqa: BLE001
        print(f"fetch failed for O*NET {a.release}: {e}", file=sys.stderr)
        sys.exit(2)
    print(f"O*NET {a.release} cached in {out}")


if __name__ == "__main__":
    main()
