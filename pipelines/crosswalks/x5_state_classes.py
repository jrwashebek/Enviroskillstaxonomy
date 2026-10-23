#!/usr/bin/env python3
"""X5 — EMST role variants -> state and local class records (ADR-0022; SPEC §5.21; vocab/state_class_fields.yaml).

Inputs: curation/x5_classes.yaml (class facts; paraphrase and numbers only), curation/x5_variant_class.csv (IA
judgments), docs/decisions/mvp_role_set.csv. Pilot jurisdictions: TX, WA, PA (state); Lewis County WA (county
environmental health); Philadelphia Water Department (municipal utility).
Outputs:
  data/v2/registers/state_classes/seed-class--<jur>--<code>.yaml   StateClassRecord per class with facts
  data/v2/crosswalks/<set>/2026-10-23.sssom.tsv                     one mapping set per jurisdiction
Verbatim spec text is not stored (hash-and-URL rule): workDescriptionText and mqText hold the URL, retrieval date
and a null sha256 until the text is fetched into a restricted store. Licence: Apache-2.0.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sssomlib as S  # noqa: E402

L = S.L
TOOL = "pipelines/crosswalks/x5_state_classes.py@0.1.0"
SNAP = "2026-10-23"
REG = L.DATA_V2 / "registers" / "state_classes"
SETS = {  # jurisdiction key -> (target dir, CURIE prefix, IRI base, set title, object source version)
    "TX": ("state-class-tx", "TXclass", "https://w3id.org/emst/ext/state-class/TX/",
           "X5 EMST role variants to Texas State Classification Plan classes",
           "Texas State Classification Plan job descriptions as published on 2026-10-23 (revisions 2019-09-01 to 2026-07-01)"),
    "WA": ("state-class-wa", "WAclass", "https://w3id.org/emst/ext/state-class/WA/",
           "X5 EMST role variants to Washington classified-service classes",
           "Washington OFM class specifications as published on 2026-10-23 (effective 2025-07-01 revisions)"),
    "PA": ("state-class-pa", "PApos", "https://w3id.org/emst/ext/state-class/PA/",
           "X5 EMST role variants to Pennsylvania DEP classes and position overrides (pilot state)",
           "Commonwealth of Pennsylvania position extracts and postings as retrieved by SL (2025-2026); class codes not exposed"),
    "WA-LEWIS": ("local-class-wa-lewis-county", "LewisCoWA", "https://w3id.org/emst/ext/local-class/WA-lewis-county/",
                 "X5 EMST role variants to Lewis County (WA) classes: county environmental health",
                 "Lewis County class specification SN313 (2007) and 2026 master salary schedule"),
    "PA-PHL": ("local-class-pa-philadelphia-water", "PHLclass", "https://w3id.org/emst/ext/local-class/PA-philadelphia/",
               "X5 EMST role variants to City of Philadelphia classes: Philadelphia Water Department (municipal utility)",
               "City of Philadelphia civil-service class specifications 7E45 (rev. 2010) and 7E49 (rev. 2023)"),
}


def variant_exists(vid: str) -> bool:
    stem = L.id_to_stem(vid) + ".yaml"
    return any(p.name == stem for p in L.DATA_V2.glob("**/variants/*.yaml"))


def record(c, jur, maps):
    j = jur[c["jur"]]
    rid = f"seed:class/{c['jur']}/{c['code']}"
    text_ref = {"storage": "hash-and-url", "url": c["url"], "retrieved": SNAP, "sha256": None,
                "note": "Verbatim text not stored in CC0 files (reuse terms unverified); fetch and hash into a restricted store."}
    mq = dict(text_ref)
    mq["paraphrase"] = c["mq"] if not c["mq"].startswith("as ") else f"Same as {c['mq'][3:]}."
    pay = ({"min": c["pay"][0], "max": c["pay"][1], "currency": "USD", "basis": j["payBasis"]} if c.get("pay")
           else {"min": None, "max": None, "currency": "USD", "rangeLabel": c["grade"], "note": "amounts not retrieved"})
    rec = {
        "id": rid, "type": "StateClassRecord", "prefLabel": {"en": c["title"]},
        "notation": [{"scheme": f"class-{c['jur']}", "value": c["code"]}],
        "jurisdictionId": j["id"], "employerType": j["employerType"], "agency": j["agency"],
        "classCode": c["code"], "classTitle": c["title"], "seriesId": c["series"],
        "levelIndex": {"ordinal": c["level"][0], "label": str(c["level"][1])},
        "supervisoryStatus": c["sup"], "specEffectiveDate": c["spec"],
        "workDescriptionText": text_ref, "mqText": mq, "mqLocation": j["mqLocation"], "degreeRule": c["degree"],
        "licensesRequired": c.get("lic", []), "payBasis": j["payBasis"] if c.get("pay") else j["payBasis"],
        "payMinMax": pay, "payGradeLabel": c["grade"], "payEffectiveDate": c["payDate"],
    }
    if c.get("bu"):
        rec["bargainingUnit"] = c["bu"]
    if c.get("mil"):
        rec["militaryEquivalent"] = [{"source": "SL-052", "note": "class listed in the Texas SAO military crosswalk (native crosswalk; candidate gold set for X5); codes not extracted"}]
    rec["emstMapping"] = maps or [{"roleVariantKey": None, "note": "no current mapping" + (" (class abolished)" if c.get("abolished") else "")}]
    notes = [f"Dated record as of {SNAP}; re-run each 1 July or on plan revision (ADR-0022 X5)."]
    if c.get("note"):
        notes.append(c["note"])
    if c.get("flsa"):
        notes.append(f"FLSA: {c['flsa']}.")
    rec.update({"editorialNote": {"en": " ".join(notes)}, "layer": "L6", "module": "core", "status": "draft",
                "validationStatus": "draft", "license": "CC0-1.0", "sensitivity": "public", "reviewBy": "2027-07-01",
                "provenance": {"method": "llm-assisted", "agent": [S.AUTHOR], "generatedAt": f"{SNAP}T19:00:00Z",
                               "toolVersion": S.MODEL, "promptVersion": S.PROMPT, "evidenceLabel": "E",
                               "sources": sorted(set(c["src"])), "reviewStatus": "unreviewed",
                               "adr": ["ADR-0022", "ADR-0006"]}})
    return rid, rec


def main():
    cur = L.load_yaml(HERE / "curation" / "x5_classes.yaml")
    jur = cur["jurisdictions"]
    classes = {(c["jur"], c["code"]): c for c in cur["classes"]}
    roles = {r["role_key"]: r for r in csv.DictReader(open(S.ROOT / "docs/decisions/mvp_role_set.csv", encoding="utf-8"))}
    rows_by_set = {k: [] for k in SETS}
    maps_by_class = {}
    for m in csv.DictReader(open(HERE / "curation" / "x5_variant_class.csv", encoding="utf-8")):
        if None in m or len(m) != 9:
            raise SystemExit(f"malformed row {m}")
        rk, actor = m["variant"].split("/", 1)
        if rk not in roles:
            raise SystemExit(f"unknown role {rk}")
        if actor.split("/")[0] not in roles[rk]["sector_actor_variants"]:
            raise SystemExit(f"{rk} has no {actor} variant in mvp_role_set")
        j = m["jur"]
        dirname, pfx, _, _, osv = SETS[j]
        has_rec = (j, m["code"]) in classes
        rid = f"emst-x5-{j.lower()}:{rk}/{actor}:{m['code']}"
        rows_by_set[j].append(dict(
            record_id=rid, subject_id=f"seed:{rk}/{actor}", subject_label=f"{roles[rk]['title']} ({actor} variant)",
            subject_source="emstsrc:emst-v2-role-variants", predicate_id=m["predicate"], predicate_modifier=m["modifier"],
            object_id=f"{pfx}:{m['code']}", object_source=f"emstsrc:{dirname}", object_source_version=osv,
            mapping_justification="semapv:LLMBasedMatching", confidence=m["confidence"], author_id=S.AUTHOR,
            mapping_date=S.TODAY, mapping_tool=TOOL,
            other=S.other_field(weakest_match_type=m["predicate"], role_level=m["role_level"], review_status="candidate",
                                evidence=m["evidence"], rater_type="llm", model=S.MODEL, prompt=S.PROMPT,
                                register_record=(f"seed:class/{j}/{m['code']}" if has_rec else "pending"),
                                grain="position-override" if m["code"].startswith("pos-") else "class"),
            comment=m["rationale"] + " Requires human SME confirmation; not a classification or qualification decision."))
        if has_rec:
            vid = f"seed:{rk}/{actor}"
            link = {"roleVariant": vid} if variant_exists(vid) else {
                "roleVariantKey": f"{rk}/{actor}",
                "pending": "role variant not yet authored by WP-08; re-run this script to link it (CR-IA-001 key)"}
            maps_by_class.setdefault((j, m["code"]), []).append({
                **link, "roleLevel": m["role_level"], "matchType": m["predicate"],
                "confidence": float(m["confidence"]), "reviewer": None, "reviewDate": None, "competencyTargets": [],
                "crosswalkRecord": rid,
                "note": "competency targets with level are added when WP-08 authors the role profile"})
    REG.mkdir(parents=True, exist_ok=True)
    nrec = 0
    for key, c in classes.items():
        rid, rec = record(c, jur, maps_by_class.get(key))
        L.write_yaml(REG / f"{L.id_to_stem(rid)}.yaml", rec)
        nrec += 1
    stats = {"class_records": nrec}
    for j, rows in rows_by_set.items():
        dirname, pfx, base, title, osv = SETS[j]
        S.write_set(dirname, SNAP, {
            "mapping_set_version": "0.1.0-draft", "mapping_set_title": title,
            "mapping_set_description": (
                "Agent-drafted candidate mappings from MVP role variants (seed:<role_key>/<sector_actor>, CR-IA-001) to "
                "native class codes; class grain, with position overrides only for the PA pilot (ADR-0022 X5; SL "
                "disagreement 6). role_level in `other` names the EMST role level the class corresponds to; "
                "register_record names the dated StateClassRecord (data/v2/registers/state_classes/) or 'pending'. "
                "Native state crosswalks (TX military crosswalk, PA federal-title equivalencies) are candidate gold sets. "
                "Not a classification, qualification or selection decision."),
            "subject_source": "emstsrc:emst-v2-role-variants", "subject_source_version": "2.0.0-draft (MVP role set 2026-10-23)",
            "object_source": f"emstsrc:{dirname}", "object_source_version": osv, "mapping_tool": TOOL,
            "comment": f"Snapshot {SNAP}; re-run each 1 July or when the plan revises.",
        }, rows, {pfx: base, "emstsrc": "https://w3id.org/emst/sources/"})
        stats[dirname] = S.summarize(rows)
    print(json.dumps(stats, indent=1))


if __name__ == "__main__":
    main()
