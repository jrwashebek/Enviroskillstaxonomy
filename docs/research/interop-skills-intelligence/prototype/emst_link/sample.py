"""Step 1: draw the 300-component sample and the 60-item gold subset (blind to system output)."""
import json

import numpy as np
import pandas as pd

from . import config as C
from . import data

KEEP = ["sample_id", "plan_id", "state", "unit_id", "unit_name", "agency", "agency_group", "plan_year", "framework",
        "component_id", "native_id", "component_type", "original_type_label", "modality", "themes", "activities",
        "text", "doc_id", "page", "method", "confidence", "enriched_by", "source_file"]


def run():
    df, files = data.load_components(types=C.SAMPLE_TYPES, states=C.SAMPLE_STATES)
    s = data.draw_sample(df)
    s = s[KEEP]
    C.DATA.mkdir(parents=True, exist_ok=True)
    s.to_csv(C.DATA / "sample_components.csv", index=False)
    # gold subset: 2 per state x type cell (48) + 12 more, favouring state-agency plans; chosen without
    # looking at any system ranking so the annotation can be done blind.
    rng = np.random.default_rng(C.SEED + 1)
    picked = []
    for st in C.SAMPLE_STATES:
        for t in C.SAMPLE_TYPES:
            cell = s[(s.state == st) & (s.component_type == t) & (s.agency_group == "USFS")]
            picked += list(cell.sample_id.values[rng.permutation(len(cell))[:2]])
    state_pool = s[(s.agency_group == "State") & (~s.sample_id.isin(picked))]
    picked += list(state_pool.sample_id.values[rng.permutation(len(state_pool))[:8]])
    rest = s[~s.sample_id.isin(picked)]
    picked += list(rest.sample_id.values[rng.permutation(len(rest))[: C.GOLD_N - len(picked)]])
    g = s[s.sample_id.isin(picked)][["sample_id", "state", "agency_group", "component_type", "plan_id", "component_id", "text"]]
    g.to_csv(C.GOLD / "gold_items_blind.csv", index=False)
    # held-out test subset (30), drawn after the dev gold set was annotated and analysed, used only to score
    # changes designed from dev-set failures (acronym expansion, proper-name masking, agreement confidence).
    rng2 = np.random.default_rng(C.SEED + 2)
    pool = s[~s.sample_id.isin(picked)]
    h = []
    for t in C.SAMPLE_TYPES:
        cell = pool[pool.component_type == t]
        h += list(cell.sample_id.values[rng2.permutation(len(cell))[:10]])
    hg = s[s.sample_id.isin(h)][["sample_id", "state", "agency_group", "component_type", "plan_id", "component_id", "text"]]
    hg.to_csv(C.GOLD / "gold_items_heldout_blind.csv", index=False)
    used = sorted(set(s.source_file))
    manifest = {
        "lmps_root": str(C.LMPS_ROOT), "seed": C.SEED, "n_sample": len(s), "n_gold_items": len(g),
        "component_files_used": {f: data.sha256(C.LMPS_ROOT / f) for f in used},
        "filters": {"types": C.SAMPLE_TYPES, "states": C.SAMPLE_STATES, "text_chars": [C.TEXT_MIN_CHARS, C.TEXT_MAX_CHARS],
                    "min_words": C.TEXT_MIN_WORDS, "state_agency_floor": C.SAMPLE_STATE_AGENCY_MIN},
    }
    (C.DATA / "sample_manifest.json").write_text(json.dumps(manifest, indent=1))
    return s, g


if __name__ == "__main__":
    s, g = run()
    print(len(s), len(g))
