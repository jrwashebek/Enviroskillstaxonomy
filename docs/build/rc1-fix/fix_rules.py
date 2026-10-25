#!/usr/bin/env python3
"""rc.1 fix pass, computed-view rule files (D-DATA; ADR-0032). Idempotent: an existing new version is left alone.

Each changed rule gets a new version file in vocab/rules/ (status active) and the old one becomes superseded with
supersededBy; superseded versions stay for reproducibility (SPEC §14.3). change-indicator@1.1.0 and
effective-use-tier@1.1.0 were written by hand with their code; this script writes the others:
  role-change@0.2.0            m9   sourceGrade, not reliability
  federal-series-profile@0.2.0 M10  rows below closeMatch left out; agentConfidence (uncalibrated); unreviewed label
  state-class-view@0.2.0       M10  the same, and one file per class lists every mapped variant
  counts@1.2.0                 m12  ratings by rater type and distinct units; distinct ChangeSignal observations
                                    (D-BUILD REQUESTS_FOR_DATA R4; D-BUILD's build code switches on at 1.2.0)
Run: python3 -I docs/build/rc1-fix/fix_rules.py   Licence: Apache-2.0.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rc1lib as R  # noqa: E402

L = R.L
RULES = L.VOCAB / "rules"
DATE = R.TODAY


def bump(rule, old_v, new_v, subs, note, extra_decided=("ADR-0032",)):
    old_p, new_p = RULES / f"{rule}@{old_v}.yaml", RULES / f"{rule}@{new_v}.yaml"
    t = old_p.read_text(encoding="utf-8")
    if not new_p.exists():
        lines = t.split("\n")
        i = lines.index(f"version: {old_v}")
        assert lines[i + 1] == "status: active", (rule, lines[i + 1])
        lines[i] = f"version: {new_v}"
        if lines[i + 2].startswith("replaces: "):
            lines[i + 2] = f"replaces: {rule}@{old_v}"
        else:
            lines.insert(i + 2, f"replaces: {rule}@{old_v}")
        n = "\n".join(lines)
        for a, b in subs:
            if a not in n:
                raise SystemExit(f"{rule}: text not found: {a[:60]}")
            n = n.replace(a, b, 1)
        head, sep, rest = n.partition("decidedIn: [")
        if sep:
            inner, close, tail = rest.partition("]")
            items = [x.strip() for x in inner.split(",") if x.strip()]
            items += [x for x in extra_decided if x not in items]
            n = head + sep + ", ".join(items) + close + tail
        n = n.rstrip("\n") + f"\n  - {{date: '{DATE}', note: \"{note}\"}}\n"
        new_p.write_text(n, encoding="utf-8")
        R.LOG.append(str(new_p.relative_to(L.ROOT)))
    if f"version: {old_v}\nstatus: active\n" in t:
        t = t.replace(f"version: {old_v}\nstatus: active\n", f"version: {old_v}\nstatus: superseded\nsupersededBy: {rule}@{new_v}\n", 1)
        old_p.write_text(t, encoding="utf-8")
        R.LOG.append(str(old_p.relative_to(L.ROOT)))


def main():
    bump("role-change", "0.1.0", "0.2.0", [
        ("with status (watch/active), family, drivers and reliability. Indicators move only under change-indicator@1.0.0, never here.",
         "with status (watch/active), family, drivers, sourceGrade (the source's Admiralty grade A-D; never called reliability) and observationId. Indicators move only under change-indicator@1.1.0, never here."),
    ], "0.2.0 (rc.1 fix pass, review m9): signals show sourceGrade, not reliability, and their observationId.")
    bump("federal-series-profile", "0.1.0", "0.2.0", [
        ("""  One Federal Series Profile per OPM series that X4 maps, with a positive non-negated predicate, to a released P1, P2 or
  P4 role.""", """  One Federal Series Profile per OPM series that X4 maps, with a positive non-negated predicate at skos:closeMatch or
  stronger, to a released P1, P2 or P4 role."""),
        ("""  held: "Tribal variants and held records are never read.\"""",
         """  held: "Tribal variants and held records are never read."
  match_threshold: "0.2.0 (ADR-0032; review M10; DATA_FIX_BRIEF §5): X4 rows below skos:closeMatch (broadMatch, narrowMatch, relatedMatch) are left out: they are never an alignment. The index counts them (excludedBelowCloseMatch), never lists them."
  agent_confidence: "The X4 row's confidence is the drafting model's own number and cannot be calibrated while no row is reviewed (SPEC §15): shown as `agentConfidence (uncalibrated)`, and the row's reviewStatus reads 'unreviewed agent candidate (not reviewed by a person)' until a pid: reviewer is recorded.\""""),
    ], "0.2.0 (rc.1 fix pass, review M10): rows below closeMatch left out; agentConfidence (uncalibrated); unreviewed agent candidate label.")
    bump("state-class-view", "0.1.0", "0.2.0", [
        ("""  One State Class View per dated StateClassRecord whose emstMapping names a released role variant.""",
         """  One State Class View per dated StateClassRecord whose emstMapping names a released role variant at skos:closeMatch
  or stronger; the file lists every such mapped variant (`variants[]`)."""),
        ("""  held: "Held records, Tribal variants and Tribal-employer class records are never read.\"""",
         """  held: "Held records, Tribal variants and Tribal-employer class records are never read."
  match_threshold: "0.2.0 (ADR-0032; review M10): mappings below skos:closeMatch are left out (never an alignment) and counted in the index (excludedBelowCloseMatch). The mapping's confidence is shown as `agentConfidence (uncalibrated)`; review reads 'unreviewed agent candidate (not reviewed by a person)' until a reviewer is recorded."
  variants: "0.2.0: one file per class; a class mapped to several variants lists each in variants[{variant, role, roleLevels, match, targets, tasks, gates, collapsed}] (0.1.0 kept only the last one written).\""""),
        ('''  fields: "jurisdiction, classCode, classFacts{...}, variant, roleLevels[], targets[], tasks[], gates[], collapsed[], disclaimers[], ruleId, ruleVersion, buildCommit"''',
         '''  fields: "jurisdiction, classCode, classRecord, classFacts{...}, variants[{variant, role, roleLevels[], match{type, agentConfidence (uncalibrated), review}, targets[], tasks[], gates[], collapsed[]}], disclaimers[], ruleId, ruleVersion, buildCommit; index: variants{}, excludedBelowCloseMatch, note"'''),
    ], "0.2.0 (rc.1 fix pass, review M10): mappings below closeMatch left out; agentConfidence (uncalibrated); every mapped variant listed.")
    bump("counts", "1.1.0", "1.2.0", [
        ("""  area (core or module namespace).""",
         """  area (core or module namespace). 1.2.0 (m12; DATA_FIX_BRIEF §10; ADR-0032): ratings (ExposureAssessment,
  CraftRating, FunctionRating, RelevanceRating) by `type` and `raterType` (`ratingsByRaterType`), with distinct rated
  units (task, competency, or subject x object) and distinct `raterId`s per type and rater type
  (`ratingUnitsByRaterType`; repeated passes of one model share one raterId, ADR-0032 M4); ChangeSignal records and
  distinct observations (`changeSignalObservations`: by `observationId`, or the record when none is stored)."""),
        ('''competenciesByLifecycle, byLifecycle, rolesByTier, variantsBySectorActor, coreCompetencies, heldRecords, excluded, redactedReferences, deferredTargets"''',
         '''competenciesByLifecycle, byLifecycle, rolesByTier, variantsBySectorActor, coreCompetencies, heldRecords, excluded, redactedReferences, deferredTargets, ratingsByRaterType, ratingUnitsByRaterType, changeSignalObservations"'''),
    ], "1.2.0 (rc.1 fix pass, m12): ratings by rater type with distinct units and raterIds; distinct ChangeSignal observations.")
    R.summary("fix_rules")


if __name__ == "__main__":
    main()
