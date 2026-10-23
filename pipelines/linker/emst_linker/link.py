"""Link text items to EMST v2 competencies (candidate generation for human review; ADR-0019 §1, §3)."""
from __future__ import annotations

import numpy as np

from . import __version__, config as C, corpus, safety
from .index import HybridIndex


class CompetencyLinker:
    def __init__(self, data_v2=C.DATA_V2, semantic=None):
        self.comps, self.tasks_by, self.release_hash = corpus.load(data_v2)
        if not self.comps:
            raise RuntimeError("no live competency records found")
        self.index = HybridIndex([c["doc"] for c in self.comps], [c["id"] for c in self.comps],
                                 short=[c["short"] for c in self.comps], semantic=semantic)
        self.task_index = {}
        self.version = {"linker": f"emst_linker@{__version__}", "index_sha256": self.index.index_sha256,
                        "corpus_sha256": self.release_hash, "semantic": self.index.sem_name,
                        "target": "competency" if not C.TASK_TARGET_FAMILIES else "competency+task(DP-18a)"}

    def _best_task(self, cid, text):
        tasks = self.tasks_by.get(cid) or []
        if not tasks:
            return None, None
        if cid not in self.task_index:
            self.task_index[cid] = HybridIndex([t for _, t in tasks], [i for i, _ in tasks], semantic="none")
        ti = self.task_index[cid]
        sc = ti.scores([text])["tfidf"][0]
        j = int(np.argmax(sc))
        return tasks[j][0], round(float(sc[j]), 4)

    def link(self, items, k=None):
        """items: iterable of dicts {item_id, text, employer_type?}. Returns (links, quarantined_count, pii_count)."""
        k = k or C.TOP_K
        keep, quarantined, pii = [], 0, 0
        for it in items:
            text, n = safety.strip_pii(it.get("text", ""))
            pii += n
            if safety.quarantine(text, it.get("employer_type")):
                quarantined += 1
                continue
            keep.append((it["item_id"], text))
        out = []
        if not keep:
            return out, quarantined, pii
        texts = [t for _, t in keep]
        order, S, raw = self.index.rank(texts, k)
        agree = self.index.agreement(raw, order[:, 0])
        for i, (iid, text) in enumerate(keep):
            raw_top = float(np.max(raw["tfidf"][i]))
            band = C.AGREEMENT_BANDS.get(int(agree[i]), "low") if "semantic" in raw else \
                ({2: "medium"}.get(int(agree[i]), "low"))
            for r, j in enumerate(order[i], 1):
                cid = self.comps[j]["id"]
                tid, tsc = self._best_task(cid, text) if r <= 3 else (None, None)
                out.append({"item_id": iid, "rank": r, "competency": cid, "fused": round(float(S[i, j]), 4),
                            "tfidf": round(float(raw["tfidf"][i, j]), 4), "evidencesTask": tid,
                            "taskScore": tsc, "confidenceBand": band if r == 1 else None,
                            "abstainCoverageGap": raw_top < C.ABSTAIN_RAW_COS, "reviewStatus": "candidate",
                            **self.version})
        return out, quarantined, pii
