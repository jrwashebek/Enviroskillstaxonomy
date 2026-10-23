"""Transparent retrieval baseline: TF-IDF cosine + BM25 + optional static semantic embeddings, fused.

Nothing here is learned from the gold set. Weights live in config.py.
"""
import re

import numpy as np
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer

from . import config as C

TOKEN = re.compile(r"[a-z][a-z0-9\-]+")
STOP = set(ENGLISH_STOP_WORDS) | C.PLAN_STOP | C.COMP_STOP


def _stem(w):
    # deliberately crude, deterministic suffix stripping (no NLTK download needed)
    for suf in ("ization", "ations", "ation", "ments", "ment", "ings", "ing", "ies", "ed", "es", "s"):
        if len(w) > len(suf) + 3 and w.endswith(suf):
            return w[: -len(suf)] + ("y" if suf == "ies" else "")
    return w


def tokenize(text):
    toks = [t.strip("-") for t in TOKEN.findall(text.lower())]
    return [_stem(t) for t in toks if t and t not in STOP and len(t) > 2]


class Linker:
    def __init__(self, comp_docs, codes, comp_short=None):
        self.codes = list(codes)
        self.tfidf = TfidfVectorizer(tokenizer=tokenize, lowercase=False, ngram_range=(1, 2),
                                     min_df=1, sublinear_tf=True, token_pattern=None)
        self.C = self.tfidf.fit_transform(comp_docs)
        self.bm25 = BM25Okapi([tokenize(d) for d in comp_docs], k1=1.2, b=0.75)
        self.sem = None
        self.sem_backend = "none"
        if C.SEMANTIC_BACKEND == "wordllama":
            try:
                self.sem = _WordLlama()
                # short, clean text embeds better with averaged static vectors than the repeated long doc
                self.Csem = self.sem.embed(comp_short if comp_short is not None else comp_docs)
                self.sem_backend = self.sem.name
            except Exception as e:  # pragma: no cover - environment dependent
                print(f"[linker] semantic backend unavailable ({e}); continuing lexical-only")
                self.sem = None

    def scores(self, texts):
        Q = self.tfidf.transform(texts)
        s_tfidf = (Q @ self.C.T).toarray()
        s_bm25 = np.vstack([self.bm25.get_scores(tokenize(t)) for t in texts])
        out = {"tfidf": s_tfidf, "bm25": s_bm25}
        if self.sem is not None:
            Qs = self.sem.embed(texts)
            out["semantic"] = Qs @ self.Csem.T
        return out

    def fuse(self, raw, weights=None):
        weights = dict(weights or C.FUSION)
        if "semantic" not in raw:
            weights.pop("semantic", None)
        tot = sum(weights.values())
        fused = 0
        for k, w in weights.items():
            s = raw[k]
            lo, hi = s.min(axis=1, keepdims=True), s.max(axis=1, keepdims=True)
            fused = fused + (w / tot) * (s - lo) / np.where(hi - lo == 0, 1, hi - lo)
        return fused

    def rank(self, texts, k=None, variant="fused"):
        k = k or C.TOP_K
        raw = self.scores(texts)
        S = self.fuse(raw) if variant == "fused" else raw[variant]
        order = np.argsort(-S, axis=1)[:, :k]
        return order, S, raw


class _WordLlama:
    """WordLlama static token embeddings (weights ship inside the PyPI wheel; no model download)."""

    def __init__(self):
        from pathlib import Path
        import wordllama
        from wordllama import WordLlama
        pkg = Path(wordllama.__file__).parent
        self.m = WordLlama.load(cache_dir=pkg, disable_download=True)
        self.name = f"wordllama-{getattr(wordllama, '__version__', '?')}-l2_supercat_256"

    def embed(self, texts):
        E = np.asarray(self.m.embed(list(texts), norm=True), dtype=np.float32)
        return E
