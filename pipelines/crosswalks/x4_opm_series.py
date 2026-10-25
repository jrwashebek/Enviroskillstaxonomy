#!/usr/bin/env python3
"""X4 — OPM series register (dated SeriesRecords) and EMST role -> OPM series mappings (ADR-0022, SPEC §5.20).

Inputs: FH's Phase 2 register docs/research/federal-human-capital/opm_series_register.csv (73 series), the
verified OPM Phase One proposal (CHCO memo 2026-04-24, Appendix A, re-read 2026-10-23; V1-10, FH-014), six series
added for MVP coverage (FH to review), curation/x4_role_series.csv (IA judgments) and FH's
opm_series_to_emst_crosswalk.csv (series -> v1 competency, chained to v2 through X1).
Outputs:
  data/v2/registers/opm_series/seed-opm-series--<code>.yaml     one SeriesRecord per series (status as of 2026-10-23)
  data/v2/crosswalks/opm-series/2026-10-23.sssom.tsv            role -> series (X4)
  data/v2/crosswalks/opm-series-competency/2026-10-23.sssom.tsv v2 competency -> series (FH relationships, chained)
Series proposed for realignment carry seriesStatus proposed-realignment and are never shown as realigned.
Licence: Apache-2.0.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sssomlib as S  # noqa: E402

L = S.L
TOOL = "pipelines/crosswalks/x4_opm_series.py@0.1.0"
FH = S.ROOT / "docs" / "research" / "federal-human-capital"
REG_DIR = L.DATA_V2 / "registers" / "opm_series"
SNAPSHOT = "2026-10-23"
EVENT = "seed:evt/opm-series-realignment-proposal/proposed/2026-04-24"
REVIEW_BY = "2027-01-23"   # quarterly re-check until OPM finalizes Phase One (P-FH-02)

# OPM CHCO memo 2026-04-24, Appendix A (proposed; agency feedback due 2026-05-11; not finalized as of 2026-10-23)
PROPOSED = {"0021": "0303", "0023": "0186", "0029": "0303", "0090": "1001", "0190": "0101", "0410": "0401",
            "0437": "0401", "0455": "0404", "0459": "4701", "0480": "0401", "0487": "0401", "0688": "0601",
            "0698": "0640", "1372": "1301", "1380": "1301"}
# series not in FH's Phase 2 register, added so every MVP role's series exists (titles: IA judgment, FH to verify)
ADDED = {
    "0201": ("Human Resources Management", "0200 Human Resources Management", "R35 knowledge continuity lead"),
    "0601": ("General Health Science", "0600 Medical, Hospital, Dental and Public Health", "proposed receiving series for 0688; R26"),
    "1712": ("Training Instruction", "1700 Education", "R35 knowledge continuity lead"),
    "1801": ("General Inspection, Investigation, Enforcement, and Compliance", "1800 Inspection, Investigation, Enforcement, and Compliance", "R12 inspector; R23 enforcement case manager"),
    "5408": ("Sewage Disposal Plant Operating", "Federal Wage System 5400 Industrial Equipment Operation", "R25 operator at federal facilities"),
    "5409": ("Water Treatment Plant Operating", "Federal Wage System 5400 Industrial Equipment Operation", "R25 operator at federal facilities"),
}
RECEIVING = {}
for old, new in PROPOSED.items():
    RECEIVING.setdefault(new, []).append(old)


def prov(evidence, sources, note=None):
    p = {"method": "llm-assisted", "agent": [S.AUTHOR], "generatedAt": f"{SNAPSHOT}T18:00:00Z",
         "toolVersion": S.MODEL, "promptVersion": S.PROMPT, "evidenceLabel": evidence, "reviewStatus": "unreviewed",
         "adr": ["ADR-0022", "ADR-0027"]}
    if sources:
        p["sources"] = sources
    return p


def edu_flag(v: str):
    v = (v or "").strip()
    if v.startswith("Y?") or v.lower().startswith("verify") or v == "enrollment" or not v:
        return None
    if v.startswith("Y"):
        return True
    if v.startswith("N"):
        return False
    return None


def series_records():
    rows = list(csv.DictReader(open(FH / "opm_series_register.csv", encoding="utf-8")))
    recs = {}
    for r in rows:
        code = r["series"].strip()
        status = f"proposed-realignment" if code in PROPOSED else "active"
        notes = []
        if code in PROPOSED:
            notes.append(f"Proposed for realignment to {PROPOSED[code]} in OPM's Phase One list (CHCO memo 2026-04-24); "
                         f"not final as of {SNAPSHOT}. Say 'proposed for realignment', never 'realigned' or 'consolidated'.")
        if code in RECEIVING:
            notes.append("Proposed receiving series for " + ", ".join(sorted(RECEIVING[code])) + " (not final).")
        notes.append(f"FH Phase 2 note: {r['notes'].strip()}")
        if r["positive_education_requirement"]:
            notes.append(f"FH education flag '{r['positive_education_requirement'].strip()}': qualification standards were "
                         "not re-read (FH-042 not accessed), so positiveEducationRequirement is FH judgment pending verification.")
        notes.append(f"Status as of {SNAPSHOT}; re-check quarterly until OPM finalizes Phase One (P-FH-02).")
        srcs = sorted({s for s in r["source_ids"].split("|") if s} | ({"FH-014", "V1-10"} if code in PROPOSED or code in RECEIVING else set()))
        rec = {
            "id": f"seed:opm-series/{code}",
            "type": "SeriesRecord",
            "prefLabel": {"en": r["title"].strip()},
            "notation": [{"scheme": "OPMseries", "value": code}],
            "seriesCode": code,
            "seriesStatus": status,
        }
        if code in PROPOSED:
            rec["successorSeries"] = PROPOSED[code]
        qs = r["qualification_standard"].strip()
        if qs:
            rec["qualificationStandardVersion"] = qs
        ef = edu_flag(r["positive_education_requirement"])
        if ef is not None:
            rec["positiveEducationRequirement"] = ef
        if code in PROPOSED:
            rec["events"] = [EVENT]
        rec.update({
            "scopeNote": {"en": f"Occupational group: {r['group'].strip()}."},
            "editorialNote": {"en": " ".join(notes)},
            "layer": "L6", "module": "core", "status": "draft", "validationStatus": "draft",
            "license": "CC0-1.0", "sensitivity": "public", "reviewBy": REVIEW_BY,
            "provenance": prov("E" if code in PROPOSED else "J", srcs if code in PROPOSED else [s for s in srcs if s]),
        })
        if rec["provenance"]["evidenceLabel"] == "J" and not rec["provenance"].get("sources"):
            rec["provenance"].pop("sources", None)
        recs[code] = rec
    for code, (title, group, why) in ADDED.items():
        notes = [f"Added by WP-09 (IA) so that every MVP role's federal series exists in the register ({why}); not in "
                 "FH's Phase 2 register; title from IA knowledge, FH to verify against the OPM Handbook of Occupational "
                 "Groups and Families."]
        if code in RECEIVING:
            notes.append("Proposed receiving series for " + ", ".join(sorted(RECEIVING[code])) + " (not final).")
        notes.append(f"Status as of {SNAPSHOT}; re-check quarterly.")
        recs[code] = {
            "id": f"seed:opm-series/{code}", "type": "SeriesRecord", "prefLabel": {"en": title},
            "notation": [{"scheme": "OPMseries", "value": code}], "seriesCode": code, "seriesStatus": "active",
            "scopeNote": {"en": f"Occupational group: {group}."}, "editorialNote": {"en": " ".join(notes)},
            "layer": "L6", "module": "core", "status": "draft", "validationStatus": "draft", "license": "CC0-1.0",
            "sensitivity": "public", "reviewBy": REVIEW_BY, "provenance": prov("J", None),
        }
        recs[code]["provenance"].pop("sources", None)
    return recs


def write_records(recs):
    REG_DIR.mkdir(parents=True, exist_ok=True)
    for code, rec in sorted(recs.items()):
        L.write_yaml(REG_DIR / f"{L.id_to_stem(rec['id'])}.yaml", rec)


def role_rows(recs):
    roles = {r["role_key"]: r for r in csv.DictReader(open(S.ROOT / "docs/decisions/mvp_role_set.csv", encoding="utf-8"))}
    out = []
    for c in csv.DictReader(open(HERE / "curation" / "x4_role_series.csv", encoding="utf-8")):
        if None in c or len(c) != 8:
            raise SystemExit(f"malformed row {c}")
        rk = c["subject"]
        if rk not in roles:
            raise SystemExit(f"unknown role {rk}")
        if c["series"] == "NoTermFound":
            obj, wk, status = S.NO_TERM, S.NO_TERM, ""
            rid = f"emst-x4:{rk}:NoTermFound"
        else:
            if c["series"] not in recs:
                raise SystemExit(f"series {c['series']} not in register")
            obj = f"OPMseries:{c['series']}"
            wk = c["predicate"]
            status = recs[c["series"]]["seriesStatus"]
            rid = f"emst-x4:{rk}:{'Not-' if c['modifier'] else ''}{c['series']}"
        extra = {}
        if status == "proposed-realignment":
            extra = {"target_series_status": "proposed-realignment",
                     "proposed_successor": recs[c["series"]]["successorSeries"], "status_as_of": SNAPSHOT}
        elif status:
            extra = {"target_series_status": status, "status_as_of": SNAPSHOT}
        out.append(dict(
            record_id=rid, subject_id=f"seed:{rk}", subject_label=roles[rk]["title"],
            subject_source="emstsrc:emst-v2-roles", predicate_id=c["predicate"], predicate_modifier=c["modifier"],
            object_id=obj, object_source="emstsrc:opm-series-register",
            object_source_version=f"EMST OPM series register snapshot {SNAPSHOT}",
            mapping_justification="semapv:LLMBasedMatching", confidence=c["confidence"], author_id=S.AUTHOR,
            mapping_date=S.TODAY, mapping_tool=TOOL,
            other=S.other_field(weakest_match_type=wk, applies_to=c["applies_to"], review_status="candidate",
                                evidence=c["evidence"], rater_type="llm", model=S.MODEL, prompt=S.PROMPT,
                                variant="federal", **extra),          # no held marker (ADR-0032, review m14)
            comment=c["rationale"] + " Requires human SME confirmation; not a classification basis."))
    return out, roles


def x1_map():
    m = {}
    for r in S.read_set(L.X1_TSV):
        s = r["subject_id"]
        if s.count(":") != 1:   # task rows (EMSTv1:1.1.1:T1) are not needed here
            continue
        m.setdefault(s.split(":", 1)[1], []).append((r["predicate_id"], r["object_id"]))
    return m


def held_keys():
    h = L.load_yaml(L.GOVERNANCE / "tribal_hold.yaml")
    return set(h.get("heldSeedKeys", [])), set(h.get("heldV1Codes", []))


def competency_rows(recs):
    xm = x1_map()
    hk, hv = held_keys()
    out, skipped_held, skipped_retired = [], 0, 0
    for r in csv.DictReader(open(FH / "opm_series_to_emst_crosswalk.csv", encoding="utf-8")):
        code, v1 = r["series"].strip(), r["emst_v1_code"].strip()
        if v1 in hv:
            skipped_held += 1
            continue
        targets = xm.get(v1, [])
        live = [(p, o) for p, o in targets if o != S.NO_TERM and o not in hk and not o.startswith("seed:tool-")]
        if not live:
            skipped_retired += 1
            continue
        for p, o in live:
            rel = r["relationship"].strip()
            out.append(dict(
                record_id=f"emst-x4c:{o.split(':', 1)[1]}:{code}:{v1}", subject_id=o,
                subject_source="emstsrc:emst-v2-competencies", predicate_id="skos:relatedMatch", object_id=f"OPMseries:{code}",
                object_source="emstsrc:opm-series-register", object_source_version=f"EMST OPM series register snapshot {SNAPSHOT}",
                mapping_justification="semapv:MappingChaining", confidence="0.5" if rel == "core" else "0.35",
                author_id=S.AUTHOR, mapping_date=S.TODAY, mapping_tool=TOOL,
                other=S.other_field(weakest_match_type="skos:relatedMatch", fh_relationship=rel, fh_basis=r["basis"].strip(),
                                    via=f"EMSTv1:{v1} {p}", review_status="candidate", evidence=r["evidence_label"].strip() or "J",
                                    fh_sources=r["source_ids"].strip().replace("|", " "),
                                    target_series_status=recs.get(code, {}).get("seriesStatus", "unregistered")),
                comment=("FH Phase 2 judgment that this competency is " + ("core to" if rel == "core" else "supporting in")
                         + f" series {code}, re-pointed from v1 {v1} to its v2 successor through X1. Navigation-grade only; "
                         "not a classification or qualification criterion.")))
    return out, skipped_held, skipped_retired


def main():
    recs = series_records()
    write_records(recs)
    rows, roles = role_rows(recs)
    curies = {"OPMseries": "https://w3id.org/emst/ext/opm-series/", "emstsrc": "https://w3id.org/emst/sources/"}
    S.write_set("opm-series", SNAPSHOT, {
        "mapping_set_version": "0.1.0-draft",
        "mapping_set_title": "X4 EMST roles to OPM occupational series (federal variants)",
        "mapping_set_description": (
            "Agent-drafted candidate mappings from MVP role profiles (seed:<role_key>; federal variant implied, re-key to "
            "RoleVariant IDs per CR-IA-001) to the EMST OPM series register (data/v2/registers/opm_series/, status as of "
            f"{SNAPSHOT}). Series proposed for realignment in OPM's Phase One list carry target_series_status="
            "proposed-realignment and proposed_successor in `other`; they are never shown as realigned. Predicates as in "
            "X3 (closeMatch interchangeable; broadMatch role is a specialisation within a broad series; narrowMatch the "
            "series is one slice of the role; relatedMatch partial overlap, feeder or destination; Not for disambiguation). "
            "Not a classification basis, not a job analysis, not for RIF or rating decisions."),
        "subject_source": "emstsrc:emst-v2-roles", "subject_source_version": "2.0.0-draft (MVP role set 2026-10-23)",
        "object_source": "emstsrc:opm-series-register", "object_source_version": f"snapshot {SNAPSHOT} (OPM CHCO memo index re-checked per V1-10)",
        "mapping_tool": TOOL,
        "see_also": ["https://www.opm.gov/chcoc/latest-memos/modernization-and-consolidation-of-occupational-series.pdf",
                     "https://www.opm.gov/policy-data-oversight/classification-qualifications/"],
        "comment": "ADR-0022 X4; OPM series codes carry no official URI, so the OPMseries prefix is an EMST namespace for the code.",
    }, rows, curies)
    crows, sh, sr = competency_rows(recs)
    S.write_set("opm-series-competency", SNAPSHOT, {
        "mapping_set_version": "0.1.0-draft",
        "mapping_set_title": "X4 companion: EMST v2 competencies to OPM series (FH Phase 2 core/supporting judgments, chained through X1)",
        "mapping_set_description": (
            "FH's Phase 2 series-to-v1-competency judgments (docs/research/federal-human-capital/opm_series_to_emst_crosswalk.csv) "
            "re-pointed to v2 records through X1 (semapv:MappingChaining). fh_relationship=core|supporting. Rows whose v1 "
            "competency is held, retired or moved to tools are omitted (counts in the WP-09 worklog). "
            "Navigation-grade input for the Federal Series Profile generator (WP-08), not a classification criterion."),
        "subject_source": "emstsrc:emst-v2-competencies", "subject_source_version": "2.0.0-draft",
        "object_source": "emstsrc:opm-series-register", "object_source_version": f"snapshot {SNAPSHOT}",
        "mapping_tool": TOOL,
    }, crows, curies)
    stats = {"series_records": len(recs),
             "by_status": {s: sum(1 for r in recs.values() if r["seriesStatus"] == s) for s in sorted({r["seriesStatus"] for r in recs.values()})},
             "opm-series": S.summarize(rows), "opm-series-competency": S.summarize(crows),
             "competency_rows_skipped_held": sh, "competency_rows_skipped_retired_or_tool": sr}
    print(json.dumps(stats, indent=1))


if __name__ == "__main__":
    main()
