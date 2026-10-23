"""Configuration for the EMST linking prototype (IA role, EMST v2 Phase 2).

Every tunable is here so a reviewer can see, in one place, what the baseline assumes.
Paths can be overridden with environment variables so the prototype runs outside this machine.
"""
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROTO = HERE.parent
EMST_ROOT = Path(os.environ.get("EMST_ROOT", PROTO.parents[3]))  # .../emst
LMPS_ROOT = Path(os.environ.get("LMPS_ROOT", "/home/claude/lmps"))

V1_BASELINE = EMST_ROOT / "data" / "v1_baseline"
DATA = PROTO / "data"
GOLD = PROTO / "gold"
OUT = PROTO / "outputs"

SEED = 20261023

# ---- Sampling of plan components (LMPs demand signal) ----
SAMPLE_TYPES = ["monitoring", "standard", "guideline"]
SAMPLE_STATES = ["MT", "ID", "CA", "WA", "OR", "CO", "UT", "WY"]
SAMPLE_N = 300
SAMPLE_STATE_AGENCY_MIN = 30          # guarantee some non-USFS (state) plan components
TEXT_MIN_CHARS, TEXT_MAX_CHARS = 80, 1500
TEXT_MIN_WORDS = 12
GOLD_N = 60

# ---- Retrieval ----
TOP_K = 10
# Field weights used when building the competency "document" (repetition-based weighting keeps it transparent)
FIELD_REPEAT = {"title": 3, "description": 2, "tasks": 2, "proficiency": 1, "indicators": 1, "sector": 0}
# Score fusion weights (applied to per-query min-max-normalised scores)
FUSION = {"tfidf": 0.35, "bm25": 0.35, "semantic": 0.30}
SEMANTIC_BACKEND = os.environ.get("EMST_SEMANTIC", "wordllama")  # "wordllama" | "none"

# ---- Confidence bands (set a priori from the score distribution of the 300-component sample, NOT from gold) ----
# fused top-1 score is in [0,1] after normalisation; margin = top1 - top2 of the *raw* tfidf cosine.
BAND_RULES = {
    "high":   {"min_raw_cos": 0.20, "min_margin": 0.03},
    "medium": {"min_raw_cos": 0.12, "min_margin": 0.0},
}
# below "medium" -> "low" (route to review queue / candidate gap)
ABSTAIN_RAW_COS = 0.08   # below this the item is flagged "no adequate competency" candidate

# ---- Domain stop-lists ----
# Plan boilerplate: deontic verbs, plan-structure words and codes that carry no skill content.
PLAN_STOP = set("""
shall should will must may would could can might also within where when which that this these those such other
forest forests forestwide forest-wide plan plans planning national grassland grasslands unit units
area areas management managed manage managing project projects activity activities action actions
maintain maintained maintaining provide provided providing ensure ensured ensuring consistent consistency
desired condition conditions guideline guidelines standard standards objective objectives goal goals
component components direction including include includes included applicable appropriate appropriately
fw ma ga mon gdl std dc obj suit gl st mg mgmt rmz rma e.g i.e etc per use used using
year years annual annually percent acres acre within mile miles site sites level levels
""".split())
# Competency boilerplate: proficiency-scale verbs that appear in every competency.
COMP_STOP = set("""
understands understand understanding applies apply applying develops develop developing leads lead leading
expert advanced intermediate foundational basic knowledge principles concepts practice practices professional
shapes advances designs design designing implements implement implementing recognizes recognize explains
programs program approaches approach methods method techniques technique tools tool systems system
environmental natural resource resources
""".split())
