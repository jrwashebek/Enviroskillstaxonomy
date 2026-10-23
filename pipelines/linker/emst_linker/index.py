"""Hybrid retrieval index: TF-IDF cosine + BM25 + optional static semantic embeddings, fused by per-query min-max.

Used both by the competency linker (index = EMST competency documents) and by crosswalk candidate generation
(index = an upstream framework's concepts, e.g. ESCO skills for X7).
"""
from __future__ import annotations

import hashlib
import re

import numpy as np
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer

from . import config as C

TOKEN = re.compile(r"[a-z][a-z0-9\-]+")


def make_stop(extra=()):
    return set(ENGLISH_STOP_WORDS) | set(extra)


DEFAULT_STOP = make_stop(C.PLAN_STOP | C.COMP_STOP)


def _stem(w):
    # deliberately crude, deterministic suffix stripping (no model download)
    for suf in ("ization", "ations", "ation", "ments", "ment", "ings", "ing", "ies", "ed", "es", "s"):
        if len(w) > len(suf) + 3 and w.endswith(suf):
            return w[: -len(suf)] + ("y" if suf == "ies" else "")
    return w


def tokenize(text, stop=DEFAULT_STOP):
    toks = [t.strip("-") for t in TOKEN.findall((text or "").lower())]
    return [_stem(t) for t in toks if t and t not in stop and len(t) > 2]


class HybridIndex:
    def __init__(self, docs, ids, short=None, semantic=None, stop=DEFAULT_STOP):
        if len(docs) != len(ids):
            raise ValueError("docs and ids differ in length")
        self.ids = list(ids)
        self.stop = stop
        tok = lambda t: tokenize(t, self.stop)  # noqa: E731
        self._tok = tok
        self.tfidf = TfidfVectorizer(tokenizer=tok, lowercase=False, ngram_range=(1, 2), min_df=1,
                                     sublinear_tf=True, token_pattern=None)
        self.D = self.tfidf.fit_transform(docs)
        self.bm25 = BM25Okapi([tok(d) or ["_empty_"] for d in docs], k1=1.2, b=0.75)
        self.sem, self.sem_name = None, "none"
        want = C.SEMANTIC_BACKEND if semantic is None else semantic
        if want == "wordllama":
            try:
                self.sem = _WordLlama()
                self.Dsem = self.sem.embed(short if short is not None else docs)
                self.sem_name = self.sem.name
            except Exception as e:  # pragma: no cover - environment dependent
                print(f"[emst_linker] semantic backend unavailable ({e}); lexical only")
                self.sem = None
        h = hashlib.sha256()
        for i, d in zip(self.ids, docs):
            h.update(f"{i}\t{d}\n".encode("utf-8"))
        self.index_sha256 = h.hexdigest()

    def scores(self, texts):
        Q = self.tfidf.transform(texts)
        out = {"tfidf": (Q @ self.D.T).toarray(),
               "bm25": np.vstack([self.bm25.get_scores(self._tok(t) or ["_empty_"]) for t in texts])}
        if self.sem is not None:
            out["semantic"] = self.sem.embed(texts) @ self.Dsem.T
        return out

    @staticmethod
    def fuse(raw, weights=None):
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

    def rank(self, texts, k=None):
        k = k or C.TOP_K
        raw = self.scores(texts)
        S = self.fuse(raw)
        order = np.argsort(-S, axis=1)[:, :k]
        return order, S, raw

    def agreement(self, raw, fused_top):
        """Number of base rankers whose own top-1 equals the fused top-1 (Phase 2 confidence signal)."""
        n = np.zeros(len(fused_top), dtype=int)
        for s in raw.values():
            n += (np.argmax(s, axis=1) == fused_top).astype(int)
        return n


class _WordLlama:
    """WordLlama static token embeddings (weights ship inside the PyPI wheel; no model download)."""

    def __init__(self):
        from pathlib import Path
        import wordllama
        from wordllama import WordLlama
        pkg = Path(wordllama.__file__).parent
        self.m = WordLlama.load(cache_dir=pkg, disable_download=True)
        self.name = f"wordllama-{getattr(wordllama, '__version__', '0.4.0.post1')}-l2_supercat_256"

    def embed(self, texts):
        return np.asarray(self.m.embed(list(texts), norm=True), dtype=np.float32)
