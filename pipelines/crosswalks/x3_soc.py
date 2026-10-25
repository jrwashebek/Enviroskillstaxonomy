#!/usr/bin/env python3
"""X3 — EMST role profiles (MVP role keys) and retired v1 families -> O*NET-SOC 2019 and SOC 2018 (ADR-0022).

Input: curation/x3_role_soc.csv (IA judgments; one row per role x target), docs/decisions/mvp_role_set.csv,
reference/*codes.txt (code lists only). Output (two sets, one per upstream version):
  data/v2/crosswalks/onet-soc/2019.sssom.tsv   role -> O*NET-SOC 2019 occupation
  data/v2/crosswalks/soc/2018.sssom.tsv        role -> SOC 2018 detailed occupation (direct rows plus rows chained
                                               from O*NET-SOC detail: role -> O*NET-SOC -> SOC, weakest type kept)
Rows are agent drafts (review_status=candidate); IDs only, no upstream titles (ADR-0013).
Licence: Apache-2.0.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sssomlib as S  # noqa: E402

TOOL = "pipelines/crosswalks/x3_soc.py@0.1.0"
MVP = S.ROOT / "docs" / "decisions" / "mvp_role_set.csv"


def codes(name):
    return {ln.strip() for ln in (HERE / "reference" / name).read_text().splitlines() if ln.strip() and not ln.startswith("#")}


def main():
    soc_codes = codes("soc2018_detailed_codes.txt")
    onet_codes = codes("onetsoc2019_data_codes.txt")
    roles = {r["role_key"]: r for r in csv.DictReader(open(MVP, encoding="utf-8"))}
    cur = list(csv.DictReader(open(HERE / "curation" / "x3_role_soc.csv", encoding="utf-8")))
    warnings = []
    onet_rows, soc_rows = [], []
    n = {"onet": 0, "soc": 0}
    explicit_soc = {(c["subject"], c["code"]) for c in cur if c["scheme"] == "soc"}
    for c in cur:
        if None in c or len(c) != 9:
            raise SystemExit(f"malformed curation row: {c}")
        subj_key = c["subject"]
        if subj_key.startswith("v1fam:"):
            sid = "EMSTv1fam:" + subj_key.split(":", 1)[1]
            ssrc, stype = "emstsrc:emst-v1-families", "owl class"
            label = ""
        else:
            if subj_key not in roles:
                raise SystemExit(f"unknown role key {subj_key}")
            sid = f"seed:{subj_key}"
            ssrc, stype = "emstsrc:emst-v2-roles", "owl class"
            label = roles[subj_key]["title"]
        pred, mod = c["predicate"], c["modifier"]
        # held variants are never marked in `other` (ADR-0032, review m14): held content is counted, never named
        base_other = dict(applies_to=c["applies_to"], review_status="candidate", evidence=c["evidence"],
                          rater_type="llm", model=S.MODEL, prompt=S.PROMPT)
        if c["code"] == "NoTermFound":
            for scheme in ("onet", "soc"):
                n[scheme] += 1
                row = dict(record_id=f"emst-x3-{scheme}:{subj_key}:NoTermFound", subject_id=sid, subject_label=label,
                           subject_source=ssrc, predicate_id=pred, object_id=S.NO_TERM,
                           object_source="emstsrc:onet-soc-2019" if scheme == "onet" else "emstsrc:soc-2018",
                           mapping_justification="semapv:LLMBasedMatching", confidence=c["confidence"],
                           author_id=S.AUTHOR, mapping_date=S.TODAY, mapping_tool=TOOL,
                           other=S.other_field(weakest_match_type=S.NO_TERM, **base_other),
                           comment=c["rationale"] + " Requires human SME confirmation.")
                (onet_rows if scheme == "onet" else soc_rows).append(row)
            continue
        if c["scheme"] == "onetsoc":
            code = c["code"]
            if code not in onet_codes:
                warnings.append(f"{subj_key}: {code} not in O*NET 27.2 data-level code list")
            n["onet"] += 1
            onet_rows.append(dict(
                record_id=f"emst-x3-onet:{subj_key}:{'Not-' if mod else ''}ONETSOC-{code}", subject_id=sid, subject_label=label,
                subject_source=ssrc, predicate_id=pred, predicate_modifier=mod, object_id=f"ONETSOC:{code}",
                object_source="emstsrc:onet-soc-2019", object_source_version="O*NET-SOC 2019 (codes checked against O*NET 27.2 data; O*NET 31.0 uses the same taxonomy)",
                mapping_justification="semapv:LLMBasedMatching", confidence=c["confidence"], author_id=S.AUTHOR,
                mapping_date=S.TODAY, mapping_tool=TOOL,
                other=S.other_field(weakest_match_type=pred, **base_other),
                comment=c["rationale"] + " Requires human SME confirmation."))
            soc = code[:7]
            if (subj_key, soc) in explicit_soc:
                continue
            # chain role -> O*NET-SOC -> SOC: a .00 code is coextensive with its SOC; other suffixes are narrower
            hop = "skos:exactMatch" if code.endswith(".00") else "skos:broadMatch"
            p2 = S.chain(pred, hop)
            if mod == "Not" and hop != "skos:exactMatch":
                continue   # a rejected detailed target says nothing about its broader SOC
            if soc not in soc_codes:
                warnings.append(f"{subj_key}: chained SOC {soc} not in OEWS 2021 detailed list")
            n["soc"] += 1
            soc_rows.append(dict(
                record_id=f"emst-x3-soc:{subj_key}:{'Not-' if mod else ''}SOC2018-{soc}", subject_id=sid, subject_label=label,
                subject_source=ssrc, predicate_id=p2, predicate_modifier=mod, object_id=f"SOC2018:{soc}",
                object_source="emstsrc:soc-2018", object_source_version="SOC 2018",
                mapping_justification="semapv:MappingChaining" if hop != "skos:exactMatch" else "semapv:LLMBasedMatching",
                confidence=c["confidence"], author_id=S.AUTHOR, mapping_date=S.TODAY, mapping_tool=TOOL,
                other=S.other_field(weakest_match_type=S.weakest(pred, hop) if hop != "skos:exactMatch" else pred,
                                    via=f"ONETSOC:{code}", **base_other),
                comment=(f"Chained from ONETSOC:{code} ({pred} then {hop}). " if hop != "skos:exactMatch" else "")
                        + c["rationale"] + " Requires human SME confirmation."))
        elif c["scheme"] == "soc":
            code = c["code"]
            if code not in soc_codes:
                warnings.append(f"{subj_key}: {code} not in OEWS 2021 detailed list")
            n["soc"] += 1
            soc_rows.append(dict(
                record_id=f"emst-x3-soc:{subj_key}:{'Not-' if mod else ''}SOC2018-{code}", subject_id=sid, subject_label=label,
                subject_source=ssrc, predicate_id=pred, predicate_modifier=mod, object_id=f"SOC2018:{code}",
                object_source="emstsrc:soc-2018", object_source_version="SOC 2018",
                mapping_justification="semapv:LLMBasedMatching", confidence=c["confidence"], author_id=S.AUTHOR,
                mapping_date=S.TODAY, mapping_tool=TOOL,
                other=S.other_field(weakest_match_type=pred, **base_other),
                comment=c["rationale"] + " Requires human SME confirmation."))
        else:
            raise SystemExit(f"unknown scheme {c['scheme']}")

    # one row per (subject, SOC, modifier): when several O*NET-SOC rows chain to the same SOC code, keep the
    # strongest predicate (a .00 row is coextensive with its SOC and wins ties) and record the others in `other`
    best = {}
    order = []
    for r in soc_rows:
        k = (r["subject_id"], r["object_id"], r.get("predicate_modifier", ""))
        if k not in best:
            best[k] = r
            order.append(k)
            continue
        cur_r = best[k]
        def rank(x):
            return (S.STRENGTH.get(x["predicate_id"], 0), x["mapping_justification"] != "semapv:MappingChaining")
        keep, drop = (r, cur_r) if rank(r) > rank(cur_r) else (cur_r, r)
        via = S.parse_other(drop["other"]).get("via", drop["object_id"])
        keep["other"] = keep["other"] + f";also_via={via}"
        best[k] = keep
    soc_rows = [best[k] for k in order]

    # every MVP role must appear in both sets (coverage is part of the acceptance)
    for rk in roles:
        for rows, nm in ((onet_rows, "onet-soc"), (soc_rows, "soc")):
            if not any(r["subject_id"] == f"seed:{rk}" for r in rows):
                warnings.append(f"{rk} has no row in {nm}")

    curies = {
        "ONETSOC": "https://www.onetonline.org/link/summary/",
        "SOC2018": "https://www.bls.gov/soc/2018/#",
        "EMSTv1fam": "https://w3id.org/emst/v1/family/",
        "emstsrc": "https://w3id.org/emst/sources/",
    }
    common_desc = (
        "Agent-drafted candidate mappings (review_status=candidate in `other`); no human reviewer yet. Subjects are "
        "MVP role profile keys from docs/decisions/mvp_role_set.csv (seed:<role_key>), to be re-keyed to RoleVariant "
        "IDs when WP-08 authors them (CR-IA-001); `applies_to` in `other` names the variant or level slice. Predicate "
        "rules: closeMatch = core work largely interchangeable for statistics and navigation; broadMatch = the role is "
        "a specialisation of a broader occupation; narrowMatch = the occupation is one slice of the role; relatedMatch = "
        "partial overlap or feeder/destination; skos:closeMatch with predicate_modifier Not and object sssom:NoTermFound = no SOC occupation adequately "
        "covers the role (no NoTermFound row asserts a positive predicate; ADR-0032) (reason in comment). Held variants are not mapped (ADR-0007 §D). v1 family rows "
        "(EMSTv1fam) record the verified v1 errors as predicate_modifier Not and the ADR-0022 §5 additions; the "
        "family sheet is retired as an anchor. Not for classification, selection or RIF decisions."
    )
    t1 = S.write_set("onet-soc", "2019", {
        "mapping_set_version": "0.1.0-draft",
        "mapping_set_title": "X3a EMST roles to O*NET-SOC 2019 occupations",
        "mapping_set_description": common_desc,
        "subject_source": "emstsrc:emst-v2-roles", "subject_source_version": "2.0.0-draft (MVP role set 2026-10-23)",
        "object_source": "emstsrc:onet-soc-2019", "object_source_version": "O*NET-SOC 2019 taxonomy; codes checked against O*NET 27.2 data-level occupations (O*NET 31.0, Aug 2026, keeps O*NET-SOC 2019 per V4-08)",
        "mapping_tool": TOOL,
        "see_also": ["https://www.onetcenter.org/taxonomy.html", "docs/research/_verification/V4_key_facts.csv#V4-08"],
        "comment": "ADR-0022 X3; WP-09. Prepare a SOC 2028 re-map when the final notice is published (planned 2027, V3-02).",
    }, onet_rows, curies)
    t2 = S.write_set("soc", "2018", {
        "mapping_set_version": "0.1.0-draft",
        "mapping_set_title": "X3b EMST roles and retired v1 families to SOC 2018 detailed occupations",
        "mapping_set_description": common_desc + " Rows with mapping_justification semapv:MappingChaining are derived from the O*NET-SOC set; `via` names the intermediate code and weakest_match_type the weaker hop.",
        "subject_source": "emstsrc:emst-v2-roles", "subject_source_version": "2.0.0-draft (MVP role set 2026-10-23); v1 families from data/v1_baseline",
        "object_source": "emstsrc:soc-2018", "object_source_version": "SOC 2018 (codes checked against BLS OEWS May 2021 detailed list)",
        "mapping_tool": TOOL,
        "see_also": ["https://www.bls.gov/soc/2018/", "https://www.bls.gov/soc/2028/2028_soc_revision.htm"],
        "comment": "ADR-0022 X3 and §5 immediate corrections; replaces the v1 family->SOC sheet as anchor.",
    }, soc_rows, curies)
    stats = {"onet-soc/2019": S.summarize(onet_rows), "soc/2018": S.summarize(soc_rows), "warnings": warnings}
    print(json.dumps(stats, indent=1))
    return stats


if __name__ == "__main__":
    main()
