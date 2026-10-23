"""Every tunable of the EMST linker in one place (ADR-0019). Nothing here is fitted to held-out gold data."""
import os
from pathlib import Path

PKG = Path(__file__).resolve().parent
LINKER_ROOT = PKG.parent
EMST_ROOT = Path(os.environ.get("EMST_ROOT", LINKER_ROOT.parents[1]))
DATA_V2 = EMST_ROOT / "data" / "v2"
SEED = 20261023

# Retrieval
TOP_K = 10
# Field weights for the competency document (repetition keeps the weighting transparent; Phase 2 values)
FIELD_REPEAT = {"prefLabel": 3, "altLabel": 1, "statement": 2, "definition": 1, "tasks": 2, "indicators": 1,
                "v1Seed": 1}
FUSION = {"tfidf": 0.35, "bm25": 0.35, "semantic": 0.30}
SEMANTIC_BACKEND = os.environ.get("EMST_SEMANTIC", "wordllama")   # "wordllama" | "none"

# Confidence: ranker agreement with the fused top-1 (monotonic on both Phase 2 splits, ADR-0019 Context)
AGREEMENT_BANDS = {3: "high", 2: "medium"}   # number of base rankers whose top-1 equals the fused top-1
ABSTAIN_RAW_COS = 0.08                      # below this raw TF-IDF cosine the item is flagged as a coverage gap

# DP-18a: families or modules switched to task-level linking (empty until the criterion fires and a change record
# cites the evaluation). Never edit without that change record.
TASK_TARGET_FAMILIES: tuple = ()

# Statuses excluded from the index
EXCLUDED_STATUSES = {"superseded", "withdrawn", "deprecated"}

# Domain stop-lists (from the Phase 2 prototype)
PLAN_STOP = set("""
shall should will must may would could can might also within where when which that this these those such other
plan plans planning area areas management managed manage managing project projects activity activities action actions
maintain maintained maintaining provide provided providing ensure ensured ensuring consistent consistency
desired condition conditions guideline guidelines standard standards objective objectives goal goals
component components direction including include includes included applicable appropriate appropriately
e.g i.e etc per use used using year years annual annually percent
""".split())
COMP_STOP = set("""
understands understand understanding applies apply applying develops develop developing leads lead leading
expert advanced intermediate foundational basic knowledge principles concepts practice practices professional
designs design designing implements implement implementing recognizes recognize explains
programs program approaches approach methods method techniques technique tools tool systems system
""".split())
