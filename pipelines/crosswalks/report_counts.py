#!/usr/bin/env python3
"""Generate WP-09 counts (never typed): per mapping set and per register, written to
docs/build/WP-09/crosswalk_counts.json and printed. Licence: Apache-2.0."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sssomlib as S  # noqa: E402

OUT = S.ROOT / "docs" / "build" / "WP-09" / "crosswalk_counts.json"


def main():
    sets = {}
    for tsv in sorted(S.XW.rglob("*.sssom.tsv")):
        yml = tsv.with_name(tsv.name[: -len(".sssom.tsv")] + ".sssom.yml")
        md = S.L.load_yaml(yml) if yml.exists() else {}
        if S.AUTHOR not in (md or {}).get("creator_id", []):
            continue
        rows = S.read_set(tsv)
        st = S.summarize(rows)
        st["review_status"] = dict(Counter(S.parse_other(r.get("other", "")).get("review_status", "?") for r in rows))
        st["llm_justification_rows"] = sum(1 for r in rows if r["mapping_justification"] == "semapv:LLMBasedMatching")
        sets[str(tsv.relative_to(S.ROOT))] = st
    reg = {}
    for d, typ in (("opm_series", "SeriesRecord"), ("state_classes", "StateClassRecord")):
        files = sorted((S.L.DATA_V2 / "registers" / d).glob("*.yaml"))
        recs = [S.L.load_yaml(f) for f in files]
        reg[d] = {"records": len(recs)}
        if typ == "SeriesRecord":
            reg[d]["by_status"] = dict(Counter(r["seriesStatus"] for r in recs))
        else:
            reg[d]["by_jurisdiction"] = dict(Counter(r["id"].split("/")[1] for r in recs))
    out = {"generated_by": "pipelines/crosswalks/report_counts.py", "sets": sets, "registers": reg,
           "totals": {"sets": len(sets), "rows": sum(v["rows"] for v in sets.values())}}
    OUT.write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
