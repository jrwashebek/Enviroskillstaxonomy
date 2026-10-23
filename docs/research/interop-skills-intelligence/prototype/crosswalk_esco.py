#!/usr/bin/env python3
"""Generate SSSOM candidate mappings EMST v1 competency -> ESCO skill (lexical baseline), then merge reviews.

Inputs (downloaded once into prototype/.cache, verified by SHA-256):
  * ESCO skills (URI + label/alt-label/description text) bundled in the MIT-licensed PyPI wheel
    esco-skill-extractor==0.1.18. Its occupations.csv has 3,658 rows, matching ESCO v1.2.0 exactly (MELO benchmark
    standardised file), so the skills are taken to be ESCO v1.2.0 [inference; verify against the ESCO portal].
  * ESCO preferred labels (v1.1.0) from jensjorisdecorte/Skill-Extraction-benchmark@19305c85, used only to split the
    preferred label off the bundled text (longest-prefix match); unmatched skills get label "(label not derived)".
Outputs (../crosswalks/):
  * emst_v1_to_esco_skill.candidates.sssom.tsv   top-3 lexical candidates per competency (review_status=candidate)
  * emst_v1_to_esco_skill.reviewed.sssom.tsv     candidates merged with crosswalks/review_emst_esco.csv judgments
Usage: python crosswalk_esco.py
"""
import csv
import hashlib
import io
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from emst_link import data  # noqa: E402
from emst_link.index import tokenize  # noqa: E402

CACHE = HERE / ".cache"
XW = HERE.parent / "crosswalks"
WHEEL = "esco_skill_extractor-0.1.18-py3-none-any.whl"
WHEEL_SHA = "ec6e5daa7d3247634a7950faf33ad9d1ca47fa2d7a09b95677f25a6f91f77af0"
LABELS_URL = "https://raw.githubusercontent.com/jensjorisdecorte/Skill-Extraction-benchmark/19305c85e35a74fb2a5128d8ee3798b06470b596/data/skills_en_label.txt"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def fetch():
    CACHE.mkdir(exist_ok=True)
    w = CACHE / WHEEL
    if not w.exists():
        subprocess.run([sys.executable, "-m", "pip", "download", "--no-deps", "-q", "esco-skill-extractor==0.1.18", "-d", str(CACHE)], check=True)
    wb = w.read_bytes()
    assert sha(wb) == WHEEL_SHA, "ESCO bundle wheel hash changed; re-verify before use"
    with zipfile.ZipFile(io.BytesIO(wb)) as z:
        skills = pd.read_csv(z.open("esco_skill_extractor/data/skills.csv"))
    lp = CACHE / "skills_en_label_v1.1.0.txt"
    if not lp.exists():
        lp.write_bytes(urllib.request.urlopen(LABELS_URL, timeout=60).read())
    labels = [l.strip() for l in lp.read_text().splitlines() if l.strip()]
    return skills, labels, {"wheel_sha256": sha(wb), "labels_sha256": sha(lp.read_bytes())}


def pref_labels(skills, labels):
    by_first = {}
    for l in labels:
        by_first.setdefault(l.split()[0], []).append(l)
    out = []
    for t in skills.description.astype(str):
        cands = [l for l in by_first.get(t.split()[0], []) if t.startswith(l + " ") or t == l]
        out.append(max(cands, key=len) if cands else "(label not derived)")
    return out


HEADER = """# curie_map:
#   EMSTv1: https://w3id.org/emst/v1/competency/
#   ESCO: http://data.europa.eu/esco/skill/
#   skos: http://www.w3.org/2004/02/skos/core#
#   semapv: https://w3id.org/semapv/vocab/
#   orcid: https://orcid.org/
#   emstagent: https://w3id.org/emst/agent/
# mapping_set_id: https://w3id.org/emst/mappings/emst-v1-esco-skill/{kind}/0.1.0
# mapping_set_version: 0.1.0-draft
# mapping_set_title: EMST v1 competencies to ESCO skills ({kind})
# mapping_set_description: Lexical TF-IDF candidates (top-3 per competency) for human review. Not an endorsed crosswalk.
# license: https://creativecommons.org/licenses/by/4.0/
# subject_source: https://w3id.org/emst/v1
# subject_source_version: v1 (20260223 reconciled copyB; data/v1_baseline)
# object_source: http://data.europa.eu/esco
# object_source_version: ESCO v1.2.0 (inferred from bundle; see crosswalk_method.md)
# mapping_tool: emst-ia-prototype/crosswalk_esco.py
# mapping_tool_version: 0.1.0
# extension_definitions:
#   - slot_name: review_status
#     property: https://w3id.org/emst/vocab/reviewStatus
#     type_hint: http://www.w3.org/2001/XMLSchema#string
# comment: Inputs {inputs}. URIs for EMST v1 are proposed w3id paths, not yet registered.
"""

COLS = ["record_id", "subject_id", "subject_label", "predicate_id", "predicate_modifier", "object_id", "object_label",
        "mapping_justification", "confidence", "similarity_score", "similarity_measure", "author_id", "reviewer_id",
        "mapping_date", "review_date", "review_status", "comment"]


def main():
    skills, labels, inputs = fetch()
    skills["label"] = pref_labels(skills, labels)
    comp, _ = data.load_competencies()
    q = [f"{r.title} {r.title} {r.description}" for r in comp.itertuples()]
    vec = TfidfVectorizer(tokenizer=tokenize, lowercase=False, ngram_range=(1, 2), sublinear_tf=True, token_pattern=None, min_df=1)
    vec.fit(list(skills.description.astype(str)) + q)
    E = vec.transform(skills.description.astype(str))
    Q = vec.transform(q)
    S = (Q @ E.T).toarray()
    rows = []
    for i, r in enumerate(comp.itertuples()):
        top = np.argsort(-S[i])[:3]
        for rank, j in enumerate(top, 1):
            uri = skills.id.iloc[j]
            rows.append({
                "record_id": f"emst-v1-esco:{r.code}:{rank}", "subject_id": f"EMSTv1:{r.code}", "subject_label": r.title,
                "predicate_id": "skos:relatedMatch", "predicate_modifier": "", "object_id": "ESCO:" + uri.rsplit("/", 1)[1],
                "object_label": skills.label.iloc[j], "mapping_justification": "semapv:LexicalSimilarityThresholdMatching",
                "confidence": round(float(min(1.0, S[i, j] / 0.5)), 3), "similarity_score": round(float(S[i, j]), 4),
                "similarity_measure": "tfidf-cosine(word 1-2gram, emst stoplists)", "author_id": "emstagent:ia-prototype-0.1.0",
                "reviewer_id": "", "mapping_date": "2026-10-23", "review_date": "", "review_status": "candidate",
                "comment": f"rank {rank} of 3; predicate is a placeholder until reviewed",
            })
    cand = pd.DataFrame(rows, columns=COLS)
    XW.mkdir(exist_ok=True)
    ins = "; ".join(f"{k}={v}" for k, v in inputs.items())
    with open(XW / "emst_v1_to_esco_skill.candidates.sssom.tsv", "w") as f:
        f.write(HEADER.format(kind="candidates", inputs=ins))
        cand.to_csv(f, sep="\t", index=False)
    rev_path = XW / "review_emst_esco.csv"
    if rev_path.exists():
        rev = pd.read_csv(rev_path, dtype=str, keep_default_na=False)
        m = cand.merge(rev, on="record_id", how="inner", suffixes=("", "_rev"))
        m["predicate_id"] = m["predicate_rev"]
        m["predicate_modifier"] = m["modifier_rev"] if "modifier_rev" in m else ""
        m["mapping_justification"] = "semapv:LLMBasedMatching"
        m["reviewer_id"] = "emstagent:claude-in-session-IA"
        m["review_date"] = "2026-10-23"
        m["review_status"] = m["status_rev"]
        m["confidence"] = m["confidence_rev"]
        m["comment"] = m["note_rev"] + " | single-pass LLM review; requires human SME confirmation"
        add_path = XW / "review_emst_esco_additions.csv"
        if add_path.exists():  # mappings found outside the candidate list (recall failures of the lexical matcher)
            m = pd.concat([m[COLS], pd.read_csv(add_path, dtype=str, keep_default_na=False)[COLS]], ignore_index=True)
        with open(XW / "emst_v1_to_esco_skill.reviewed.sssom.tsv", "w") as f:
            f.write(HEADER.format(kind="reviewed", inputs=ins))
            m[COLS].to_csv(f, sep="\t", index=False)
        print("reviewed rows:", len(m), m.review_status.value_counts().to_dict())
    print("candidates:", len(cand), "inputs:", inputs)


if __name__ == "__main__":
    main()
