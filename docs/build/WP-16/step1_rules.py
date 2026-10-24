#!/usr/bin/env python3
"""WP-16 rule activations in vocab/rules/ (ADR-0031 §1 P-01, §2 P-02). Idempotent text edits that keep comments.

P-01: display-gate@1.1.0 draft -> active; display-gate@1.0.0 active -> superseded (supersededBy 1.1.0).
P-02: the six HR and mobility view rules (0.1.0) interim -> active, implementation pointer names the ported module.
Licence: Apache-2.0.
"""
from __future__ import annotations

from pathlib import Path

RULES = Path(__file__).resolve().parents[3] / "vocab" / "rules"
NOTE_DG11 = ("  - {date: '2026-10-23', note: \"Activated by the CA at WP-16 (ADR-0031 §1; P-01): IO's implementation in "
             "validation/display_gates.yaml 1.1.0 and display_gate.py#decide_role_value accepted with IO's judgment calls (a) "
             "and (c); call (b) narrowed: editorial design values render at describe tier only until panel-retained, as "
             "definition.editorial_rule says, so the gates file's develop branch for pid:-reviewed values is not ratified. "
             "Views emit role-profile rows through decide() (scripts/rules/gated_values.py).\"}\n")
NOTE_DG10 = ("  - {date: '2026-10-23', note: \"Superseded by display-gate@1.1.0 at WP-16 (ADR-0031 §1). Kept so past builds "
             "stay reproducible.\"}\n")
HR = {
    "federal-series-profile@0.1.0.yaml": "scripts/rules/federal_series_profile.py#compute",
    "state-class-view@0.1.0.yaml": "scripts/rules/state_class_view.py#compute",
    "job-family-membership@0.1.0.yaml": "scripts/rules/job_family_membership.py#compute",
    "role-change@0.1.0.yaml": "scripts/rules/role_change.py#compute",
    "mirror-links@0.1.0.yaml": "scripts/rules/mirror_links.py#compute",
    "pathway-edges@0.1.0.yaml": "scripts/rules/pathway_edges.py#compute",
}
NOTE_HR = ("  - {{date: '2026-10-23', note: \"Activated by the CA at WP-16 (ADR-0031 §2; P-02). The release port in "
           "{impl} reads released records only, finds variants by variantOf and sectorActor (never by seed-key suffix), and "
           "applies display-gate@1.1.0; the WP-08 generator stays an authoring preview.\"}}\n")


def edit(name, fn):
    p = RULES / name
    t = p.read_text(encoding="utf-8")
    new = fn(t)
    if new != t:
        p.write_text(new, encoding="utf-8")
        print(f"edited vocab/rules/{name}")


def dg11(t):
    t = t.replace("\nstatus: draft\n", "\nstatus: active\n", 1)
    if "Activated by the CA at WP-16" not in t:
        t = t.rstrip("\n") + "\n" + NOTE_DG11
    return t


def dg10(t):
    t = t.replace("\nstatus: active\n", "\nstatus: superseded\nsupersededBy: display-gate@1.1.0\n", 1)
    if "Superseded by display-gate@1.1.0 at WP-16" not in t:
        t = t.rstrip("\n") + "\n" + NOTE_DG10
    return t


def hr(impl):
    def fn(t):
        t = t.replace("\nstatus: interim\n", "\nstatus: active\n", 1)
        lines = t.split("\n")
        for i, ln in enumerate(lines):
            if ln.startswith("implementation: ") and not ln.startswith(f"implementation: {impl}"):
                lines[i] = f"implementation: {impl} (called from scripts/build_release.py#Builder.views)"
        t = "\n".join(lines)
        if "Activated by the CA at WP-16" not in t:
            lines = t.split("\n")
            idx = max(i for i, ln in enumerate(lines) if ln.startswith("  - {date: '"))     # last changeNote entry
            lines.insert(idx + 1, NOTE_HR.format(impl=impl.split("#")[0]).rstrip("\n"))
            t = "\n".join(lines)
        return t
    return fn


if __name__ == "__main__":
    edit("display-gate@1.1.0.yaml", dg11)
    edit("display-gate@1.0.0.yaml", dg10)
    for name, impl in HR.items():
        edit(name, hr(impl))
