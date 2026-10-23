#!/usr/bin/env python3
"""X8 seed (private role variants -> PS reference job architecture) and X11 seed (public <-> private translation,
TR-01...TR-38, with friction fields) — ADR-0022; PS Phase 2 inputs.

Inputs: docs/research/private-sector/private_job_frameworks.csv (PJ rows; EMST-authored reference architecture),
public_private_translation.csv (TR rows), curation/x8_private_ja.csv, curation/x11_public_private.csv (IA judgments
on PS's rows), docs/decisions/mvp_role_set.csv.
Outputs: data/v2/crosswalks/emst-private-ja/0.1.0.sssom.tsv (X8) and emst-public-private/0.1.0.sssom.tsv (X11).
Both object vocabularies are EMST-internal (PS research), so the sets live in `emst-*` folders. Employer names in
the PJ examples are never copied. Licence: Apache-2.0.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sssomlib as S  # noqa: E402

TOOL = "pipelines/crosswalks/x8_x11_private.py@0.1.0"
PS = S.ROOT / "docs" / "research" / "private-sector"
CURIES = {"EMSTpja": "https://w3id.org/emst/research/private-sector/job-architecture/",
          "EMSTtr": "https://w3id.org/emst/research/private-sector/translation/",
          "emstsrc": "https://w3id.org/emst/sources/"}


def roles():
    return {r["role_key"]: r for r in csv.DictReader(open(S.ROOT / "docs/decisions/mvp_role_set.csv", encoding="utf-8"))}


def check_variant(rs, key):
    rk, actor = key.split("/", 1)
    if rk not in rs:
        raise SystemExit(f"unknown role {rk}")
    if actor.split("/")[0] not in rs[rk]["sector_actor_variants"]:
        raise SystemExit(f"{rk} has no {actor} variant in mvp_role_set")
    return rk, actor


def main():
    rs = roles()
    pj = {r["row_id"]: r for r in csv.DictReader(open(PS / "private_job_frameworks.csv", encoding="utf-8"))}
    tr = {r["translation_id"]: r for r in csv.DictReader(open(PS / "public_private_translation.csv", encoding="utf-8"))}
    x8 = []
    for d in csv.DictReader(open(HERE / "curation" / "x8_private_ja.csv", encoding="utf-8")):
        if None in d or len(d) != 7:
            raise SystemExit(f"malformed {d}")
        rk, actor = check_variant(rs, d["variant"])
        if d["pj"] == "NoTermFound":
            obj, wk, extra = S.NO_TERM, S.NO_TERM, {}
        else:
            if d["pj"] not in pj:
                raise SystemExit(f"unknown {d['pj']}")
            obj, wk = f"EMSTpja:{d['pj']}", d["predicate"]
            extra = {"industry": pj[d["pj"]]["employer_type"], "pj_level": pj[d["pj"]]["level"]}
        x8.append(dict(
            record_id=f"emst-x8:{d['variant']}:{obj.split(':', 1)[1]}", subject_id=f"seed:{d['variant']}",
            subject_label=f"{rs[rk]['title']} ({actor} variant)", subject_source="emstsrc:emst-v2-role-variants",
            predicate_id=d["predicate"], predicate_modifier=d["modifier"], object_id=obj,
            object_source="emstsrc:emst-ps-reference-job-architecture",
            object_source_version="PS Phase 2 private_job_frameworks.csv (88 rows, 2026-10-23)",
            mapping_justification="semapv:LLMBasedMatching", confidence=d["confidence"], author_id=S.AUTHOR,
            mapping_date=S.TODAY, mapping_tool=TOOL,
            other=S.other_field(weakest_match_type=wk, role_level=d["role_level"], review_status="candidate",
                                evidence="S", rater_type="llm", model=S.MODEL, prompt=S.PROMPT, **extra),
            comment=d["rationale"] + " Requires PS confirmation."))
    x11 = []
    for d in csv.DictReader(open(HERE / "curation" / "x11_public_private.csv", encoding="utf-8")):
        if None in d or len(d) != 10:
            raise SystemExit(f"malformed {d}")
        if d["tr"] not in tr:
            raise SystemExit(f"unknown {d['tr']}")
        rk, actor = check_variant(rs, d["subject"])
        if d["object"].startswith("PJ-"):
            obj, osrc = f"EMSTpja:{d['object']}", "emstsrc:emst-ps-reference-job-architecture"
        else:
            check_variant(rs, d["object"])
            obj, osrc = f"seed:{d['object']}", "emstsrc:emst-v2-role-variants"
        t = tr[d["tr"]]
        x11.append(dict(
            record_id=f"emst-x11:{d['tr']}:{d['subject']}:{obj.split(':', 1)[1]}", subject_id=f"seed:{d['subject']}",
            subject_label=f"{rs[rk]['title']} ({actor} variant)", subject_source="emstsrc:emst-v2-role-variants",
            predicate_id=d["predicate"], object_id=obj, object_source=osrc,
            object_source_version="2.0.0-draft; PS translation rows 2026-10-23",
            mapping_justification="semapv:LLMBasedMatching", confidence=d["confidence"], author_id=S.AUTHOR,
            mapping_date=S.TODAY, mapping_tool=TOOL, see_also=f"EMSTtr:{d['tr']}",
            other=S.other_field(weakest_match_type=d["predicate"] if d["predicate"].startswith("skos:") else "skos:relatedMatch",
                                translation_id=d["tr"], friction_posture_change=d["posture_change"],
                                friction_licensure_gap=d["licensure_gap"], friction_pay_direction=d["pay_direction"],
                                private_ja=d["private_ja"].replace("|", " "), shared_v1_codes=t["shared_emst_v1_codes"].replace("|", " "),
                                ps_evidence=t["evidence_label"], review_status="candidate", evidence="S", rater_type="llm",
                                model=S.MODEL, prompt=S.PROMPT),
            comment=d["rationale"] + " Seeded from PS translation row; requires PS and CM confirmation."))
    S.write_set("emst-private-ja", "0.1.0", {
        "mapping_set_version": "0.1.0-draft",
        "mapping_set_title": "X8 seed: EMST private role variants to the PS reference job architecture",
        "mapping_set_description": (
            "Agent-drafted candidate mappings from MVP private role variants to PS's Phase 2 reference job architecture "
            "(industry x job family x career stream x level; 88 rows). Objects are EMST research rows (EMSTpja). "
            "industry and pj_level in `other`; role_level names the EMST level. GSA labor-category data is a candidate "
            "public seed still to investigate (P-PS-08). Not a compensation or classification benchmark."),
        "subject_source": "emstsrc:emst-v2-role-variants", "subject_source_version": "2.0.0-draft (MVP role set 2026-10-23)",
        "object_source": "emstsrc:emst-ps-reference-job-architecture", "object_source_version": "0.1.0 (PS Phase 2)",
        "mapping_tool": TOOL,
    }, x8, CURIES)
    S.write_set("emst-public-private", "0.1.0", {
        "mapping_set_version": "0.1.0-draft",
        "mapping_set_title": "X11 seed: public <-> private role translations with friction fields (TR-01...TR-38)",
        "mapping_set_description": (
            "Seed of the public-private translation set from PS's Phase 2 translation rows, keyed to MVP role variants. "
            "emst:mirrorRole marks pairs with inverted authority position (regulator <-> regulated party or consultant "
            "preparer). Friction fields in `other`: friction_posture_change, friction_licensure_gap, "
            "friction_pay_direction ('not assessed' where PS gave no pay evidence). TR rows outside the MVP role set "
            "(e.g. TR-13 safety, TR-14 cultural resources, TR-15 realty) are not seeded; TR-14 touches "
            "government-to-government consultation and is left for TN review. see_also names the TR row."),
        "subject_source": "emstsrc:emst-v2-role-variants", "subject_source_version": "2.0.0-draft",
        "object_source": "emstsrc:emst-v2-role-variants", "object_source_version": "2.0.0-draft; PS translation 2026-10-23",
        "mapping_tool": TOOL,
    }, x11, CURIES)
    print(json.dumps({"x8": S.summarize(x8), "x11": S.summarize(x11),
                      "x11_translation_rows_seeded": len({S.parse_other(r["other"])["translation_id"] for r in x11}),
                      "x11_translation_rows_available": len(tr)}, indent=1))


if __name__ == "__main__":
    main()
