#!/usr/bin/env python3
"""X7 — EMST v2 competencies -> ESCO skills (ADR-0022): candidate generation, review merge, SSSOM output.

ESCO v1.2.1 (Dec 2025) is the target release (V4-09). The portal and API were unreachable from this session
(proxy 403), so the re-run uses the ESCO skills bundled in esco-skill-extractor 0.1.18 (13,939 skill URIs; 3,658
occupations = ESCO v1.2.0 per MELO; IA-024, WP09-017). v1.2.1 is a minor release that "improved structure without
adding or removing content" (CA-030), so skill URIs are expected to carry over [J]; the set is pinned to v1.2.0 and
must be re-pinned with the CI upstream diff when v1.2.1 files are obtained.

Steps
  1. candidates: hybrid index over ESCO skill texts; query = each live, non-held v2 competency (label, statement,
     supporting tasks); top-K per competency -> pipelines/crosswalks/work/x7_esco-1.2.0_candidates.tsv (IDs and
     scores only; ESCO text never enters the repo).
  2. review sheet (outside the repo, with ESCO labels) -> --sheet PATH, for reviewers.
  3. merge curation/x7_esco_review.csv (reviewed decisions) -> data/v2/crosswalks/esco/1.2.0.sssom.tsv. Only
     reviewed rows are published; unreviewed machine candidates stay in work/.
Usage: python pipelines/crosswalks/x7_esco.py --esco-skills SKILLS.csv --esco-labels LABELS.txt [--sheet OUT.csv]
Licence: Apache-2.0.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "linker"))
import sssomlib as S  # noqa: E402
from emst_linker import corpus  # noqa: E402
from emst_linker.index import HybridIndex, make_stop  # noqa: E402

TOOL = "pipelines/crosswalks/x7_esco.py@0.1.0"
VERSION = "1.2.0"
K = 5
WORK = HERE / "work"
REVIEW = HERE / "curation" / "x7_esco_review.csv"
ESCO_STOP = make_stop("""skill skills knowledge competence ability able using use apply applying work working
relevant related appropriate ensure various different specific""".split())


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load_esco(skills_csv, labels_txt):
    rows = list(csv.DictReader(open(skills_csv, encoding="utf-8")))
    labels = [l.strip() for l in open(labels_txt, encoding="utf-8") if l.strip()] if labels_txt else []
    by_first = {}
    for l in labels:
        by_first.setdefault(l.split()[0], []).append(l)
    out = []
    for r in rows:
        t = r["description"]
        cands = [l for l in by_first.get(t.split()[0] if t else "", []) if t.startswith(l + " ") or t == l]
        out.append({"uri": r["id"], "text": t, "label": max(cands, key=len) if cands else "(label not derived)"})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--esco-skills", required=True)
    ap.add_argument("--esco-labels")
    ap.add_argument("--sheet", help="write a review sheet WITH ESCO labels to this path (outside the repo)")
    ap.add_argument("--k", type=int, default=K)
    ap.add_argument("--bundle-sha", default="ec6e5daa7d3247634a7950faf33ad9d1ca47fa2d7a09b95677f25a6f91f77af0",
                    help="sha256 of the esco-skill-extractor 0.1.18 wheel the skills file came from")
    a = ap.parse_args()
    esco = load_esco(a.esco_skills, a.esco_labels)
    comps, tasks_by, rel_hash = corpus.load()
    idx = HybridIndex([e["text"] for e in esco], [e["uri"] for e in esco], short=[e["label"] + ". " + e["text"][:300] for e in esco],
                      stop=ESCO_STOP)
    queries = []
    for c in comps:
        tasks = " ".join(t for _, t in (tasks_by.get(c["id"]) or [])[:6])
        queries.append(f"{c['label']}. {c['label']}. {c['short']}. {tasks}")
    order, Sc, raw = idx.rank(queries, a.k)
    WORK.mkdir(exist_ok=True)
    cand = []
    for i, c in enumerate(comps):
        for r, j in enumerate(order[i], 1):
            cand.append({"subject_id": c["id"], "rank": r, "object_id": "ESCO:" + esco[j]["uri"].rsplit("/", 1)[1],
                         "fused": round(float(Sc[i, j]), 4), "tfidf": round(float(raw["tfidf"][i, j]), 4)})
    with open(WORK / f"x7_esco-{VERSION}_candidates.tsv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cand[0]), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(cand)
    if a.sheet:
        lab = {"ESCO:" + e["uri"].rsplit("/", 1)[1]: e for e in esco}
        cl = {c["id"]: c for c in comps}
        with open(a.sheet, "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["subject_id", "module", "subject_label", "subject_statement", "rank", "object_id", "esco_label",
                        "esco_text", "fused", "tfidf"])
            for x in cand:
                e = lab[x["object_id"]]
                c = cl[x["subject_id"]]
                w.writerow([x["subject_id"], c["module"], c["label"], c["short"][:300], x["rank"], x["object_id"],
                            e["label"], e["text"][:260], x["fused"], x["tfidf"]])
    # merge reviewed decisions
    rows = []
    score = {(x["subject_id"], x["object_id"]): x for x in cand}
    live = {c["id"]: c for c in comps}
    stale = 0
    if REVIEW.exists():
        for d in csv.DictReader(open(REVIEW, encoding="utf-8")):
            if d["subject_id"] not in live:
                stale += 1          # competency superseded, withdrawn or held since review: not published
                continue
            obj = S.NO_TERM if d["object_id"] == "NoTermFound" else d["object_id"]
            x = score.get((d["subject_id"], obj), {})
            via = d.get("found_by") or ("candidate rank %s" % x["rank"] if x else "targeted search")
            rid = f"emst-x7:{d['subject_id'].split(':', 1)[1]}:{'Not-' if d['modifier'] else ''}{obj.split(':', 1)[1]}"
            rows.append(dict(
                record_id=rid, subject_id=d["subject_id"], subject_label=live[d["subject_id"]]["label"],
                subject_source="emstsrc:emst-v2-competencies", predicate_id=d["predicate"],
                predicate_modifier=d["modifier"], object_id=obj, object_source="emstsrc:esco",
                object_source_version=f"ESCO v{VERSION} (bundled; v1.2.1 not reachable 2026-10-23)",
                mapping_justification="semapv:LLMBasedMatching", confidence=d["confidence"],
                similarity_score=x.get("fused", "") if obj != S.NO_TERM else "",
                similarity_measure="emst_linker fused tfidf+bm25+wordllama (min-max per query)" if x and obj != S.NO_TERM else "",
                author_id=S.AUTHOR, mapping_date=S.TODAY, mapping_tool=TOOL,
                other=S.other_field(weakest_match_type=S.NO_TERM if obj == S.NO_TERM else d["predicate"],
                                    review_status="llm-reviewed-candidate", evidence="S", rater_type="llm",
                                    model=S.MODEL, prompt=S.PROMPT, found_by=via, esco_version_gap="pinned v1.2.0; re-pin to v1.2.1"),
                comment=d["rationale"] + " Requires human SME confirmation."))
    if rows:
        S.write_set("esco", VERSION, {
            "mapping_set_version": "0.1.0-draft",
            "mapping_set_title": "X7 EMST v2 competencies to ESCO skills (reviewed subset; ESCO v1.2.0 pinned, v1.2.1 gap)",
            "mapping_set_description": (
                "Re-run of the Phase 2 EMST v1 -> ESCO v1.2.0 prototype on EMST v2 competency records (live, not "
                "held). Candidates from the emst_linker hybrid index; decisions by an LLM reviewer "
                "(review_status=llm-reviewed-candidate; no human reviewer yet). Rejected candidates are kept with "
                "predicate_modifier Not so they do not resurface; skos:closeMatch sssom:NoTermFound rows record ESCO "
                "gaps (reason in comment). VERSION GAP: ESCO v1.2.1 (Dec 2025) is current; its files were not "
                "reachable, so objects are pinned to the v1.2.0 skill URIs in esco-skill-extractor 0.1.18 "
                f"(wheel sha256 {a.bundle_sha}; skills.csv sha256 {sha(a.esco_skills)}); re-pin via the upstream diff. "
                "Navigation-grade at most until human review (ADR-0022 §4); no claim of ESCO alignment."),
            "subject_source": "emstsrc:emst-v2-competencies", "subject_source_version": f"2.0.0-draft (corpus sha256 {rel_hash[:16]})",
            "object_source": "emstsrc:esco", "object_source_version": f"ESCO v{VERSION} (inferred from bundle; target v1.2.1)",
            "mapping_tool": TOOL,
            "see_also": ["https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/esco-versions",
                         "docs/research/interop-skills-intelligence/crosswalk_method.md"],
        }, rows, {"ESCO": "http://data.europa.eu/esco/skill/", "emstsrc": "https://w3id.org/emst/sources/"})
    print(json.dumps({"esco_skills": len(esco), "competencies_queried": len(comps), "candidate_rows": len(cand),
                      "published_rows": len(rows), "review_rows_stale_subject": stale,
                      "skills_sha256": sha(a.esco_skills), **({"set": S.summarize(rows)} if rows else {})}, indent=1))


if __name__ == "__main__":
    main()
