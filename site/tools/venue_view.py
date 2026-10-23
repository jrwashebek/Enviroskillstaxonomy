#!/usr/bin/env python3
"""Compute the venue-applicability view over a release bundle with the registered rule implementation.

The explorer reads federal applicability only from a computed view (ADR-0016 §4). Until build_release.py emits
views/venue_applicability.json (CR-CP-001 A1, CR-SC-001 #4), this adapter applies DE's registered rule
venue-applicability@1.0.0 (scripts/rules/venue_applicability.py#compute) to the records of the release bundle, so held
and excluded records are never read. It writes only to the output path given. Licence: Apache-2.0.

Usage: python3 site/tools/venue_view.py <release_dir> <out.json> [--as-of YYYY-MM-DD]
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from rules import venue_applicability as VA  # noqa: E402


def main(argv):
    release, out = Path(argv[0]), Path(argv[1])
    as_of = argv[argv.index("--as-of") + 1] if "--as-of" in argv else None
    graph = json.loads((release / "emst.bundle.jsonld").read_text(encoding="utf-8"))["@graph"]
    manifest = next((r for r in graph if r.get("type") == "Release"), {})
    as_of = as_of or manifest.get("released") or "9999-12-31"
    released = {r["id"]: r for r in graph if isinstance(r, dict) and r.get("id") and r.get("type") not in ("Release", "Mapping")}
    view = VA.compute(released, as_of, {"ruleId": VA.RULE_ID, "ruleVersion": VA.RULE_VERSION,
                                        "computedBy": "site/tools/venue_view.py over the release bundle"})
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(view, indent=1, sort_keys=True), encoding="utf-8")
    print(f"[venue] {len(view['rows'])} competency-actor rows (venue-applicability@{VA.RULE_VERSION}, as of {as_of}) -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
