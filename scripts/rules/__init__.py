"""Implementations of the computed-view rules defined in vocab/rules/<ruleId>@<version>.yaml (ADR-0021, ADR-0029 §4).

Each module implements one rule; scripts/build_release.py stamps every view row with the ruleId/ruleVersion of the
rule file whose status is active (or interim while no active version exists).
"""
