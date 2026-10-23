"""Step 6: candidate coverage gaps — plan direction the v1 taxonomy does not lexically cover.

Components whose best TF-IDF cosine to any competency is in the bottom tercile are clustered (TF-IDF + NMF)
and each cluster is described by its top terms and example texts. Output is a *review prompt* for DB/CA,
not a list of new competencies.
"""
import numpy as np
import pandas as pd
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

from . import config as C
from .index import tokenize


def run(frame, n_topics=12, max_docs=8000):
    lo = frame[~frame.linked] if "linked" in frame.columns else frame
    lo = lo.sample(n=min(max_docs, len(lo)), random_state=C.SEED) if len(lo) > max_docs else lo
    vec = TfidfVectorizer(tokenizer=tokenize, lowercase=False, min_df=5, max_df=0.3, token_pattern=None)
    X = vec.fit_transform(lo.text)
    nmf = NMF(n_components=n_topics, random_state=C.SEED, init="nndsvda", max_iter=400)
    W = nmf.fit_transform(X)
    terms = np.array(vec.get_feature_names_out())
    rows = []
    for k in range(n_topics):
        top = terms[np.argsort(-nmf.components_[k])[:12]]
        members = np.where(W.argmax(axis=1) == k)[0]
        ex = lo.iloc[members[np.argsort(-W[members, k])[:3]]].text.str.slice(0, 220).tolist() if len(members) else []
        rows.append({"cluster": k, "n_components": int(len(members)), "top_terms": " ".join(top), "examples": " || ".join(ex)})
    out = pd.DataFrame(rows).sort_values("n_components", ascending=False)
    out.to_csv(C.OUT / "coverage_gap_clusters.csv", index=False)
    return {"n_low_similarity_components_clustered": int(len(lo)), "clusters": out[["cluster", "n_components", "top_terms"]].to_dict("records")}
