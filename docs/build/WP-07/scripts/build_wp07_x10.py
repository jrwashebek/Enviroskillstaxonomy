#!/usr/bin/env python3
"""Build the X10 evidence-equivalence register seed (credential <-> CLO; ADR-0022 X10, ADR-0026 §7; P-LC-07).

Conventions (also written into the set's metadata):
- subject = a Credential in data/v2/registers/credentials/; object = the competency whose CLO (its indicator set at one
  level) the credential may evidence; the CLO level is in `other` as `clo_level=Lx`, because a CLO has no record ID of its
  own (ADR-0026 §1: the CLO is the set of indicators at a level).
- predicate `emst:equivalentEvidence` = the credential is accepted as evidence toward that CLO for recognition of prior
  learning, within the scope stated in `comment`; `predicate_modifier: Not` = it is explicitly NOT accepted as evidence of
  performance at that CLO (typically a training record or knowledge test), which stops credential-as-proficiency drift
  (ADR-0003 T-8).
- Every row is agent-drafted (`semapv:LLMBasedMatching`), unreviewed; `confidence` is LC's judgment, not a similarity
  score. IO validates before any row is used, and no row may be used for selection (training and RPL only).

Usage: python3 docs/build/WP-07/scripts/build_wp07_x10.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "scripts"))
import emstlib as L  # noqa: E402

OUTDIR = REPO / "data" / "v2" / "crosswalks" / "emst-x10-evidence-equivalence"
STEM = "2.0.0-draft"
AUTHOR = "emstagent:lc-agent@wp-07"
DATE = "2026-10-23"
TOOL = "docs/build/WP-07/scripts/build_wp07_x10.py@1"

# (credential, object competency, clo level, negated, confidence, scope comment)
ROWS = [
    ("seed:crd-wildland-fire-position-qualification", "seed:v1-4.4.1-B", "L2", False, 0.6,
     "Partial: task-book evaluation on qualifying assignments evidences briefing and stop-work practice in the incident setting only; field and facility settings need separate evidence. Check currency."),
    ("seed:crd-wildland-fire-position-qualification", "seed:v1-4.3.1", "L1", False, 0.7,
     "Firefighter-type qualifications evidence the entry CLO; higher positions map to higher levels only through MOD-11 anchors (ADR-0004 §8), never by equivalence."),
    ("seed:crd-wildland-fire-position-qualification", "seed:IO-C01", "L3", True, 0.8,
     "Holding a position qualification does not evidence evaluating others; signed evaluator records on completed task books may, through a portfolio review."),
    ("seed:crd-state-prescribed-burn-manager", "seed:v1-4.3.2", "L2", False, 0.5,
     "Partial and state-specific: certification content and practical requirements vary by state; accept with a burn plan and an observed burn record."),
    ("seed:crd-nims-ics-training", "seed:v1-4.4.5", "L1", True, 0.7,
     "Course completion evidences incident-command knowledge statements only, not observed incident communication; use with an exercise or incident observation."),
    ("seed:crd-hazwoper", "seed:v1-4.4.4-A", "L1", True, 0.8,
     "A training record is an entry gate and evidence of instruction, not of observed safe work on a hazardous site; performance needs an observed drill or task-book entry."),
    ("seed:crd-hazwoper", "seed:v1-4.4.1-B", "L1", True, 0.8,
     "Training record only; safety-culture CLOs need observed briefing, stop-work and reporting behaviour."),
    ("seed:crd-remote-pilot-certificate", "seed:FC-C14", "L1", True, 0.6,
     "The certificate rests on a knowledge test, not a practical flight evaluation [J; LC-040 unverified]; accept as evidence for the UAS-rules knowledge statements and as a legal gate, not for flight performance."),
    ("seed:crd-drinking-water-treatment-operator", "seed:DB-C01", "L2", False, 0.6,
     "Grade-dependent: lower grades evidence L1 and higher grades up to L3 through MOD-01 anchors; responsible charge is a sign-off gate, not a level (ADR-0004 §8). State-specific; check currency."),
    ("seed:crd-wastewater-treatment-operator", "seed:DB-C02", "L2", False, 0.6,
     "Grade-dependent as for drinking water; state-specific; check currency."),
    ("seed:crd-certified-wildlife-biologist", "seed:v1-4.1.2", "L2", False, 0.4,
     "Partial: the certification reviews education and experience rather than observing field performance [J]; accept with a survey work sample or blind re-measurement."),
    ("seed:crd-professional-wetland-scientist", "seed:FC-C06", "L2", False, 0.5,
     "Partial: experience-based certification; accept with a delineation work sample checked in the field. Object competency pending authoring (FC, MOD-02)."),
    ("seed:crd-gisp", "seed:v1-2.1.4", "L2", False, 0.5,
     "Partial: portfolio and examination evidence spatial-data practice; tool-specific skills stay in L4 and are not credited here."),
    ("seed:crd-rehs-rs", "seed:LC-C-07", "L2", False, 0.4,
     "Partial: examination-based registration evidences environmental-health knowledge; hazard-investigation performance needs an observed inspection or investigation record."),
    ("seed:crd-saf-certified-forester", "seed:v1-1.3.2", "L2", False, 0.4,
     "Partial: education-and-experience certification; accept with an inventory work sample or cruise-data record."),
    ("seed:crd-cerp", "seed:v1-4.2.1", "L3", False, 0.4,
     "Partial: portfolio-based certification of restoration practice; check that the portfolio includes implementation under non-routine site conditions."),
    ("seed:crd-certified-floodplain-manager", "seed:DB-C43", "L2", False, 0.5,
     "Partial: examination-based; accept with a permit or substantial-damage determination work sample."),
    ("seed:crd-contracting-officers-representative", "seed:PS-C01", "L2", False, 0.4,
     "Partial and public-side only: training-based certification evidences the technical-representative enactment's rules, not scope drafting or negotiation performance."),
    ("seed:crd-state-inspector-credential", "seed:SL-C03", "L2", False, 0.6,
     "Where the programme issues the credential after observed inspections, it evidences independent inspection; check the issuing programme's evaluation record."),
    ("seed:crd-wilderness-first-aid", "seed:v1-4.4.2", "L1", False, 0.7,
     "Courses with a practical skills assessment evidence the entry CLO; check currency (typically two to three years)."),
    ("seed:crd-professional-engineer", "seed:PS-C03", "L3", True, 0.8,
     "Licensure is a legal sign-off gate for engineering work, not evidence of project-delivery performance (ADR-0003 T-8)."),
]


def label(rid):
    for d in ("registers/credentials", "core/competencies"):
        p = REPO / "data" / "v2" / d / f"{L.id_to_stem(rid)}.yaml"
        if p.exists():
            return (L.load_yaml(p).get("prefLabel") or {}).get("en", "")
    for p in (REPO / "data" / "v2" / "modules").glob(f"*/competencies/{L.id_to_stem(rid)}.yaml"):
        return (L.load_yaml(p).get("prefLabel") or {}).get("en", "")
    return ""


def main():
    header = ["subject_id", "subject_label", "predicate_id", "predicate_modifier", "object_id", "object_label",
              "mapping_justification", "confidence", "author_id", "mapping_date", "mapping_tool", "other", "comment"]
    lines = ["\t".join(header)]
    pending = []
    for subj, obj, lvl, neg, conf, comment in ROWS:
        sl, ol = label(subj), label(obj)
        if not sl:
            raise SystemExit(f"credential {subj} not in the register")
        if not ol:
            pending.append(obj)
        row = [subj, sl, "emst:equivalentEvidence", "Not" if neg else "", obj, ol, "semapv:LLMBasedMatching", f"{conf:.2f}",
               AUTHOR, DATE, TOOL, f"clo_level={lvl}; evidence_label=J; review=unreviewed", comment.replace("\t", " ")]
        lines.append("\t".join(row))
    OUTDIR.mkdir(parents=True, exist_ok=True)
    (OUTDIR / f"{STEM}.sssom.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    meta = {
        "mapping_set_id": "https://w3id.org/emst/crosswalks/emst-x10-evidence-equivalence/2.0.0-draft",
        "mapping_set_version": "0.1.0",
        "mapping_set_title": "EMST X10: credential to CLO evidence-equivalence register (seed)",
        "mapping_set_description": ("Seed of the recognition-of-prior-learning register (ADR-0022 X10; ADR-0026 §7). Subjects are EMST "
                                    "credential register records; objects are competencies, with the CLO level in `other` "
                                    "(clo_level=Lx). predicate_modifier Not marks credentials explicitly not accepted as evidence "
                                    "of performance at that CLO. Agent-drafted and unreviewed; IO validates; training and RPL use "
                                    "only, never selection."),
        "license": "https://creativecommons.org/publicdomain/zero/1.0/",
        "subject_source": "https://w3id.org/emst/registers/credentials/",
        "subject_source_version": "2.0.0-draft",
        "object_source": "https://w3id.org/emst/",
        "object_source_version": "2.0.0-draft",
        "mapping_date": DATE,
        "mapping_tool": TOOL,
        "creator_id": [AUTHOR],
        "curie_map": {"emst": "https://w3id.org/emst/", "seed": "https://w3id.org/emst/seed/", "sssom": "https://w3id.org/sssom/",
                      "semapv": "https://w3id.org/semapv/vocab/", "skos": "http://www.w3.org/2004/02/skos/core#",
                      "emstagent": "https://w3id.org/emst/agent/"},
        "extension_definitions": [],
        "comment": "Mapping set X10 (vocab/mapping_predicates.yaml). Owner WP-07 (LC) with IO validation. Objects not yet authored are listed in docs/build/WP-07/WORKLOG.md.",
    }
    (OUTDIR / f"{STEM}.sssom.yml").write_text(L.dump_yaml(meta), encoding="utf-8")
    print(f"wrote {len(ROWS)} X10 rows; objects not yet authored: {sorted(set(pending))}")


if __name__ == "__main__":
    main()
