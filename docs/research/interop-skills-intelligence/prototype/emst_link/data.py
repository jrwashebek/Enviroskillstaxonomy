"""Data loading: v1 competencies (from DE's normalized baseline) and LMPs plan components."""
import csv
import glob
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from . import config as C

csv.field_size_limit(10**9)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_competencies():
    """Return one row per v1 competency with the text fields used for indexing.

    Uses data/v1_baseline (DE's normalized extract of the copyB reconciled workbook). Where DE flagged
    `title_contains_description`, the cleaned `suggested_title` is used and the overflow text is treated
    as description (it was the description in the source).
    """
    b = C.V1_BASELINE
    comp = pd.read_csv(b / "competencies.csv", dtype=str, keep_default_na=False)
    tasks = pd.read_csv(b / "tasks.csv", dtype=str, keep_default_na=False)
    prof = pd.read_csv(b / "proficiency.csv", dtype=str, keep_default_na=False)
    ind = pd.read_csv(b / "indicators.csv", dtype=str, keep_default_na=False)
    sec = pd.read_csv(b / "sector_applications.csv", dtype=str, keep_default_na=False)

    rows = []
    for _, r in comp.iterrows():
        code = r["code"]
        title = r["suggested_title"] or r["title"]
        desc = r["description"]
        if not desc and r["suggested_title"] and r["title"].startswith(r["suggested_title"]):
            desc = r["title"][len(r["suggested_title"]):].strip()
        t = tasks[tasks.code == code].sort_values("task_n")["text"].tolist()
        p = prof[prof.code == code]
        pr = (p["knowledge"] + " " + p["application"]).tolist()
        ii = ind[ind.code == code]["text"].tolist()
        ss = sec[sec.code == code]["text"].tolist()
        rows.append({
            "code": code, "key": r["key"], "domain": r["domain_num"], "skill_area": r["skill_area_code"],
            "skill_area_name": r["skill_area_name"].title(), "title": title, "description": desc,
            "tasks": " ".join(t), "proficiency": " ".join(pr), "indicators": " ".join(ii), "sector": " ".join(ss),
            "n_tasks": len(t), "n_prof": len(pr), "n_ind": len(ii),
        })
    df = pd.DataFrame(rows)
    manifest = {f: sha256(b / f) for f in ["competencies.csv", "tasks.csv", "proficiency.csv",
                                            "indicators.csv", "sector_applications.csv"]}
    bi = b / "BUILD_INFO.json"
    if bi.exists():
        info = json.loads(bi.read_text())
        manifest["v1_baseline_generated_utc"] = info.get("generated_utc")
        manifest["v1_source_workbook_sha256"] = next((i["sha256"] for i in info.get("inputs", []) if i.get("role") == "baseline"), None)
    return df, manifest


def competency_document(row, repeat=None):
    """Concatenate fields with repetition weights (transparent field weighting)."""
    repeat = repeat or C.FIELD_REPEAT
    parts = []
    for field, n in repeat.items():
        val = row.get(field, "") or ""
        if field == "title":
            val = f"{row['title']} {row['skill_area_name']}"
        parts.extend([val] * n)
    return " ".join(parts)


def load_components(types=None, states=None):
    files = sorted(glob.glob(str(C.LMPS_ROOT / "plans" / "*" / "*" / "*" / "components.csv")))
    frames = []
    for f in files:
        d = pd.read_csv(f, dtype=str, keep_default_na=False)
        d["source_file"] = str(Path(f).relative_to(C.LMPS_ROOT))
        frames.append(d)
    df = pd.concat(frames, ignore_index=True)
    if types:
        df = df[df.component_type.isin(types)]
    if states:
        df = df[df.state.isin(states)]
    df["agency_group"] = np.where(df.agency.str.strip() == "USDA Forest Service", "USFS", "State")
    return df.reset_index(drop=True), files


def usable_text(s):
    s = s.strip()
    if not (C.TEXT_MIN_CHARS <= len(s) <= C.TEXT_MAX_CHARS):
        return False
    if len(s.split()) < C.TEXT_MIN_WORDS:
        return False
    # table-row fragments from the LMPs extractor look like "Header: value | Header: value"
    if s.count(" | ") >= 3:
        return False
    return True


def draw_sample(df):
    """Stratified, deterministic sample: state x component_type, with a floor for state-agency plans."""
    rng = np.random.default_rng(C.SEED)
    df = df[df.text.map(usable_text)].copy()
    df = df.drop_duplicates(subset=["text"])
    picked = []
    # 1) state-agency floor (non-USFS plans are ~5% of the corpus; without a floor they vanish from the sample)
    st = df[df.agency_group == "State"]
    n_state = min(C.SAMPLE_STATE_AGENCY_MIN, len(st))
    picked.append(st.iloc[rng.permutation(len(st))[:n_state]])
    rest = df.drop(picked[0].index)
    # 2) fill remaining quota evenly over state x type cells
    remaining = C.SAMPLE_N - n_state
    cells = [(s, t) for s in C.SAMPLE_STATES for t in C.SAMPLE_TYPES]
    per = remaining // len(cells)
    extra = remaining - per * len(cells)
    shortfall = 0
    for i, (s, t) in enumerate(cells):
        cell = rest[(rest.state == s) & (rest.component_type == t)]
        want = per + (1 if i < extra else 0) + 0
        take = cell.iloc[rng.permutation(len(cell))[:want]]
        shortfall += want - len(take)
        picked.append(take)
        rest = rest.drop(take.index)
    if shortfall > 0:  # top up from any remaining usable component in the target states/types
        pool = rest[rest.state.isin(C.SAMPLE_STATES)]
        picked.append(pool.iloc[rng.permutation(len(pool))[:shortfall]])
    out = pd.concat(picked).reset_index(drop=True)
    out.insert(0, "sample_id", [f"S{i+1:03d}" for i in range(len(out))])
    return out
