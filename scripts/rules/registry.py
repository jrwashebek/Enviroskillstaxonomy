"""Load the computed-view rule files in vocab/rules/<ruleId>@<version>.yaml (ADR-0021; ADR-0029 §4.1).

The build stamps every view row with the ruleId/ruleVersion of the file whose status is `active`; a rule with no
active version uses its `interim` version. Superseded versions stay in vocab/rules/ for provenance.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import emstlib as L  # noqa: E402

RULES_DIR = L.VOCAB / "rules"
STATUS_PREFERENCE = ("active", "interim")


def rule_files(rules_dir: Path = RULES_DIR) -> dict[str, dict]:
    """{'<ruleId>@<version>': document} for every rule file."""
    out = {}
    for p in sorted(Path(rules_dir).glob("*.yaml")):
        d = L.load_yaml(p) or {}
        out[f"{d.get('ruleId')}@{d.get('version')}"] = dict(d, _path=p)
    return out


def active_rules(rules_dir: Path = RULES_DIR) -> dict[str, dict]:
    """{ruleId: document} choosing status active, else interim (one per ruleId; ties are an error)."""
    by_id: dict[str, list] = {}
    for d in rule_files(rules_dir).values():
        by_id.setdefault(d["ruleId"], []).append(d)
    out = {}
    for rid, docs in sorted(by_id.items()):
        for status in STATUS_PREFERENCE:
            hits = [d for d in docs if d.get("status") == status]
            if len(hits) > 1:
                raise ValueError(f"rule {rid}: {len(hits)} versions are {status}")
            if hits:
                out[rid] = hits[0]
                break
    return out


def stamp(rules: dict, rule_id: str, build_commit: str) -> dict:
    d = rules[rule_id]
    return {"ruleId": rule_id, "ruleVersion": str(d["version"]), "buildCommit": build_commit}
