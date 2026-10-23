#!/usr/bin/env python3
"""
EMST v2 - CM (Career Mobility & Theory of Change) preliminary transferability analysis on v1 tags.

Inputs (read-only):
  legacy/v1/data/20260223_SkillsTaxonomy_Core_V3_reconciled__copyB_aaf34c8c.xlsx, sheet "Dimension Tags"
    - F1..F15 profession-family tags per competency: Core | Supporting | blank
    - Craft Primary (FC|DC|SC), Craft Secondary (FC-sec|DC-sec|SC-sec|blank)
    - T13 CLD flag / severity, Stability Tier

Outputs (written next to this script):
  family_similarity_matrix.csv   15x15 weighted-Jaccard similarity (primary measure; Core=1, Supporting=0.5)
  family_pairs.csv               long form: every ordered pair with all measures, null-model z, directional coverage, gaps
  bridging_competencies.csv      per-competency bridging metrics across family communities
  family_craft_blend.csv         FC/DC/SC blend per family, network position, entry-path (CLD) exposure
  transferability_summary.json   headline numbers quoted in report.md

Method notes (see report.md section 3 for interpretation and limits):
  * Family vectors w(f,c) in {0, 0.5, 1}. Sensitivity runs: Supporting = 0.25, 0.75, and Core-only (0).
  * Weighted Jaccard  J(a,b) = sum_c min(w_a,w_b) / sum_c max(w_a,w_b)         (primary, symmetric)
  * Cosine            cos(a,b)                                                 (symmetric)
  * Specificity-weighted Jaccard: each competency weighted by idf_c = ln(15 / n_c), n_c = families tagging c,
    so competencies every family tags (generic professional skills) do not inflate similarity.
  * Null model: 2,000 permutations shuffling each family's tag vector across competencies (preserves each
    family's Core/Supporting counts); z = (J_obs - mean_null) / sd_null. Controls the "big family" size effect.
  * Directional coverage cov(a->b) = mean over b's Core competencies of w_a(c): how much of the destination's
    core the origin already holds (Core=1, Supporting=0.5, absent=0). Transitions are asymmetric (Dawson et al.).
  * Communities: Louvain on the J-weighted family graph (seeded, resolution 1.0), checked against
    average-linkage hierarchical clustering on 1-J.
  * Bridging: a competency's contribution to between-community similarity = sum over cross-community family
    pairs of min(w_a(c), w_b(c)) divided by the number of cross-community pairs.

Run:  python3 -I docs/research/mobility-workforce-voice/transferability_analysis.py
"""
import json
import math
import os
import sys
from itertools import combinations, permutations

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(REPO, "legacy", "v1", "data",
                   "20260223_SkillsTaxonomy_Core_V3_reconciled__copyB_aaf34c8c.xlsx")
SEED = 20261023
N_PERM = 2000

try:
    import networkx as nx
except ImportError:  # pragma: no cover
    nx = None


def load():
    dt = pd.read_excel(SRC, sheet_name="Dimension Tags", dtype=str)
    fam_cols = [c for c in dt.columns if c.startswith("F") and ":" in c]
    fam_codes = [c.split(":")[0].strip() for c in fam_cols]
    fam_names = {c.split(":")[0].strip(): c.split(":", 1)[1].strip() for c in fam_cols}
    return dt, fam_cols, fam_codes, fam_names


def weight_matrix(dt, fam_cols, sup_w):
    m = np.zeros((len(fam_cols), len(dt)))
    for i, col in enumerate(fam_cols):
        v = dt[col].fillna("").str.strip()
        m[i] = np.where(v == "Core", 1.0, np.where(v == "Supporting", sup_w, 0.0))
    return m


def wjaccard(a, b, cw=None):
    mn, mx = np.minimum(a, b), np.maximum(a, b)
    if cw is not None:
        mn, mx = mn * cw, mx * cw
    return float(mn.sum() / mx.sum()) if mx.sum() > 0 else 0.0


def cosine(a, b):
    d = np.linalg.norm(a) * np.linalg.norm(b)
    return float(a @ b / d) if d > 0 else 0.0


def sim_matrix(W, fn, **kw):
    n = W.shape[0]
    S = np.eye(n)
    for i, j in combinations(range(n), 2):
        S[i, j] = S[j, i] = fn(W[i], W[j], **kw)
    return S


def upper(S):
    iu = np.triu_indices(S.shape[0], 1)
    return S[iu]


def spearman(x, y):
    rx = pd.Series(x).rank().values
    ry = pd.Series(y).rank().values
    return float(np.corrcoef(rx, ry)[0, 1])


def norm_crafts(dt):
    prim = dt["Craft Primary"].fillna("").str.strip().str.upper()
    sec = dt["Craft Secondary"].fillna("").str.strip().str.upper().str.replace("-SEC", "", regex=False)
    return prim, sec


def cld_true(dt):
    v = dt["T13: CLD Flag"].fillna("").str.strip().str.lower()
    return v.isin(["true", "yes"])  # v1 mixes True/False (D1-5,7) with Yes/No (D6)


def _baseline_check(dt, fam_cols):
    """Cross-check family tags against the Phase 1 normalized extract (data/v1_baseline/family_assignments.csv)."""
    p = os.path.join(REPO, "data", "v1_baseline", "family_assignments.csv")
    if not os.path.exists(p):
        return "baseline extract not present"
    fa = pd.read_csv(p, dtype=str)
    long = dt.melt(id_vars=["Competency Code"], value_vars=fam_cols).dropna()
    long["family_code"] = long["variable"].str.split(":").str[0].str.strip()
    m = long.merge(fa, left_on=["Competency Code", "family_code"], right_on=["code", "family_code"],
                   how="outer", indicator=True)
    both = m[m["_merge"] == "both"]
    return {"assignments_xlsx": int(len(long)), "assignments_baseline": int(len(fa)),
            "matched": int(len(both)), "value_mismatches": int((both["value"] != both["assignment"]).sum()),
            "only_in_one_source": int((m["_merge"] != "both").sum())}


def main():
    rng = np.random.default_rng(SEED)
    dt, fam_cols, F, names = load()
    n_f, n_c = len(F), len(dt)
    codes = dt["Competency Code"].astype(str).values
    titles = dt["Competency Title"].astype(str).values
    prim, sec = norm_crafts(dt)
    cld = cld_true(dt).values
    sev = dt["T13: CLD Severity"].fillna("").values
    tier = dt["Stability Tier"].fillna("").values

    W = weight_matrix(dt, fam_cols, 0.5)
    tagged = (W > 0)
    n_tag = tagged.sum(axis=0)  # families per competency
    idf = np.where(n_tag > 0, np.log(n_f / np.maximum(n_tag, 1)), 0.0)

    # ---- primary + alternative similarity measures
    J = sim_matrix(W, wjaccard)
    C = sim_matrix(W, cosine)
    Jidf = sim_matrix(W, wjaccard, cw=idf)
    sens = {}
    for label, sw in [("sup0.25", 0.25), ("sup0.75", 0.75), ("core_only", 0.0)]:
        sens[label] = sim_matrix(weight_matrix(dt, fam_cols, sw), wjaccard)

    # ---- null model (column-wise permutation preserves each family's tag counts)
    null = np.zeros((N_PERM, n_f, n_f))
    for k in range(N_PERM):
        Wp = np.array([rng.permutation(row) for row in W])
        null[k] = sim_matrix(Wp, wjaccard)
    mu, sd = null.mean(axis=0), null.std(axis=0, ddof=1)
    Z = np.where(sd > 0, (J - mu) / np.where(sd > 0, sd, 1), 0.0)
    p_hi = (null >= J[None]).mean(axis=0)

    # ---- directional coverage and gaps
    core = (W == 1.0)
    cov = np.zeros((n_f, n_f))
    gaps = {}
    for a, b in permutations(range(n_f), 2):
        cb = np.where(core[b])[0]
        cov[a, b] = W[a, cb].mean() if len(cb) else 0.0
        gaps[(a, b)] = [codes[c] for c in cb if W[a, c] == 0]

    # ---- network: communities + centrality
    comm_of = {i: 0 for i in range(n_f)}
    btw = {i: float("nan") for i in range(n_f)}
    strength = J.sum(axis=1) - 1
    communities = [list(range(n_f))]
    if nx is not None:
        G = nx.Graph()
        for i in range(n_f):
            G.add_node(i)
        for i, j in combinations(range(n_f), 2):
            G.add_edge(i, j, weight=J[i, j], dist=1 - J[i, j])
        communities = [sorted(c) for c in nx.community.louvain_communities(G, weight="weight", resolution=1.0, seed=SEED)]
        communities.sort(key=lambda c: (-len(c), c))
        for k, cset in enumerate(communities):
            for i in cset:
                comm_of[i] = k
        btw = nx.betweenness_centrality(G, weight="dist", normalized=True)
        modularity = nx.community.modularity(G, [set(c) for c in communities], weight="weight")
    else:
        modularity = float("nan")
    # cross-check with hierarchical clustering
    hc_labels = None
    try:
        from scipy.cluster.hierarchy import linkage, fcluster
        from scipy.spatial.distance import squareform
        D = 1 - J
        np.fill_diagonal(D, 0)
        Lk = linkage(squareform(D, checks=False), method="average")
        hc_labels = fcluster(Lk, t=len(communities), criterion="maxclust")
    except Exception:
        pass

    # ---- outputs: similarity matrix
    labels = [f"{f}: {names[f]}" for f in F]
    pd.DataFrame(np.round(J, 3), index=labels, columns=labels).rename_axis("family").to_csv(
        os.path.join(HERE, "family_similarity_matrix.csv"))

    # ---- outputs: pair table (ordered pairs; symmetric measures repeat)
    rows = []
    for a, b in permutations(range(n_f), 2):
        rows.append({
            "origin": F[a], "origin_name": names[F[a]], "destination": F[b], "destination_name": names[F[b]],
            "wjaccard": round(J[a, b], 3), "cosine": round(C[a, b], 3), "wjaccard_specificity": round(Jidf[a, b], 3),
            "wjaccard_sup0.25": round(sens["sup0.25"][a, b], 3), "wjaccard_sup0.75": round(sens["sup0.75"][a, b], 3),
            "wjaccard_core_only": round(sens["core_only"][a, b], 3),
            "null_mean": round(mu[a, b], 3), "null_z": round(Z[a, b], 2), "null_p_ge": round(p_hi[a, b], 4),
            "coverage_origin_to_dest": round(cov[a, b], 3), "coverage_dest_to_origin": round(cov[b, a], 3),
            "asymmetry": round(cov[a, b] - cov[b, a], 3),
            "dest_core_n": int(core[b].sum()), "dest_core_absent_in_origin_n": len(gaps[(a, b)]),
            "dest_core_absent_in_origin": "|".join(gaps[(a, b)]),
            "same_community": comm_of[a] == comm_of[b],
        })
    pairs = pd.DataFrame(rows)
    pairs.to_csv(os.path.join(HERE, "family_pairs.csv"), index=False)

    # ---- outputs: bridging competencies
    cross_pairs = [(a, b) for a, b in combinations(range(n_f), 2) if comm_of[a] != comm_of[b]]
    brows = []
    for c in range(n_c):
        fam_core = [F[i] for i in range(n_f) if W[i, c] == 1.0]
        fam_sup = [F[i] for i in range(n_f) if W[i, c] == 0.5]
        comms_any = sorted({comm_of[i] for i in range(n_f) if W[i, c] > 0})
        comms_core = sorted({comm_of[i] for i in range(n_f) if W[i, c] == 1.0})
        contrib = (sum(min(W[a, c], W[b, c]) for a, b in cross_pairs) / len(cross_pairs)) if cross_pairs else 0.0
        nt = int(n_tag[c])
        if nt == 0:
            btype = "untagged"
        elif len(comms_core) >= 2:
            btype = "cross-community core bridge"
        elif nt >= 10:
            btype = "broad foundation (mostly Supporting)"
        elif len(comms_any) >= 2:
            btype = "cross-community supporting link"
        elif nt == 1:
            btype = "single-family specialist"
        else:
            btype = "within-community"
        brows.append({
            "competency_code": codes[c], "competency_title": titles[c],
            "craft_primary": prim.iloc[c], "craft_secondary": sec.iloc[c],
            "n_core_families": len(fam_core), "n_supporting_families": len(fam_sup), "n_families_tagged": nt,
            "core_families": "|".join(fam_core), "supporting_families": "|".join(fam_sup),
            "communities_reached": len(comms_any), "communities_core": len(comms_core),
            "cross_community_contribution": round(contrib, 4),
            "specificity_idf": round(float(idf[c]), 3),
            "bridge_type": btype,
            "cld_flag": bool(cld[c]), "cld_severity": sev[c], "stability_tier": tier[c],
        })
    bridges = pd.DataFrame(brows).sort_values(
        ["cross_community_contribution", "n_core_families", "competency_code"], ascending=[False, False, True])
    bridges.insert(0, "bridge_rank", range(1, len(bridges) + 1))
    bridges.to_csv(os.path.join(HERE, "bridging_competencies.csv"), index=False)

    # ---- outputs: craft blend per family
    crafts = ["FC", "DC", "SC"]
    base = {k: float((prim == k).mean()) for k in crafts}
    frows = []
    for i, f in enumerate(F):
        idx_core = np.where(W[i] == 1.0)[0]
        idx_all = np.where(W[i] > 0)[0]
        core_mix = {k: float((prim.iloc[idx_core] == k).mean()) if len(idx_core) else 0.0 for k in crafts}
        wmix = {k: 0.0 for k in crafts}
        for c in idx_all:
            if prim.iloc[c] in wmix:
                wmix[prim.iloc[c]] += W[i, c] * 1.0
            if sec.iloc[c] in wmix:
                wmix[sec.iloc[c]] += W[i, c] * 0.5
        tot = sum(wmix.values()) or 1.0
        wmix = {k: v / tot for k, v in wmix.items()}
        ent = -sum(p * math.log(p) for p in wmix.values() if p > 0) / math.log(3)
        dom = max(wmix, key=wmix.get)
        cld_core = cld[idx_core]
        sev_core = sev[idx_core]
        frows.append({
            "family": f, "family_name": names[f], "n_core": len(idx_core), "n_supporting": int((W[i] == 0.5).sum()),
            "core_FC": round(core_mix["FC"], 3), "core_DC": round(core_mix["DC"], 3), "core_SC": round(core_mix["SC"], 3),
            "weighted_FC": round(wmix["FC"], 3), "weighted_DC": round(wmix["DC"], 3), "weighted_SC": round(wmix["SC"], 3),
            "dominant_craft_weighted": dom,
            "blend_evenness_0to1": round(ent, 3),
            "FC_vs_taxonomy_baseline_pp": round(100 * (wmix["FC"] - base["FC"]), 1),
            "DC_vs_taxonomy_baseline_pp": round(100 * (wmix["DC"] - base["DC"]), 1),
            "SC_vs_taxonomy_baseline_pp": round(100 * (wmix["SC"] - base["SC"]), 1),
            "community": comm_of[i], "strength": round(float(strength[i]), 3),
            "betweenness": round(float(btw[i]), 3),
            "core_with_cld_flag_share": round(float(cld_core.mean()) if len(cld_core) else 0.0, 3),
            "core_with_cld_high_or_highest": int(np.isin(sev_core, ["High", "Highest"]).sum()),
        })
    blend = pd.DataFrame(frows)
    blend.to_csv(os.path.join(HERE, "family_craft_blend.csv"), index=False)

    # ---- backbone network (edges only where similarity beats the null model, z > 2) + partition stability
    backbone = {"edges": [], "components": [], "betweenness": {}, "cross_cluster_paths": {}}
    stability = {}
    cluster_cov = {}
    if nx is not None:
        Bk = nx.Graph()
        Bk.add_nodes_from(F)
        for a, b in combinations(range(n_f), 2):
            if Z[a, b] > 2:
                Bk.add_edge(F[a], F[b], weight=J[a, b], dist=1 - J[a, b])
        backbone["edges"] = sorted([(u, v, round(w, 3)) for u, v, w in Bk.edges(data="weight")], key=lambda e: -e[2])
        backbone["components"] = [sorted(c, key=lambda x: int(x[1:])) for c in nx.connected_components(Bk)]
        backbone["betweenness"] = {k: round(v, 3) for k, v in
                                   sorted(nx.betweenness_centrality(Bk, weight="dist").items(), key=lambda x: -x[1])}
        backbone["degree"] = dict(Bk.degree())
        for s_, t_ in [("F12", "F8"), ("F7", "F8"), ("F11", "F1"), ("F15", "F2"), ("F5", "F8")]:
            try:
                backbone["cross_cluster_paths"][f"{s_}->{t_}"] = nx.shortest_path(Bk, s_, t_, weight="dist")
            except nx.NetworkXNoPath:
                backbone["cross_cluster_paths"][f"{s_}->{t_}"] = "no path above chance"
        # co-assignment frequency over 150 Louvain runs (3 resolutions x 50 seeds)
        H = nx.Graph()
        for a, b in combinations(range(n_f), 2):
            H.add_edge(a, b, weight=J[a, b])
        co = np.zeros((n_f, n_f))
        for res in (0.8, 1.0, 1.2):
            for sd in range(50):
                lab = {n: k for k, cs in enumerate(nx.community.louvain_communities(H, weight="weight", resolution=res, seed=sd)) for n in cs}
                co += np.array([[lab[i] == lab[j] for j in range(n_f)] for i in range(n_f)])
        co /= 150
        stability["min_within_community_coassignment"] = round(float(min(co[i, j] for cset in communities for i in cset for j in cset)), 2)
        stability["max_between_community_coassignment"] = round(float(max(
            [co[i, j] for i in range(n_f) for j in range(n_f) if comm_of[i] != comm_of[j]] or [0])), 2)
        stability["finer_partition_res1.3"] = [sorted((F[i] for i in cs), key=lambda x: int(x[1:])) for cs in
                                               nx.community.louvain_communities(H, weight="weight", resolution=1.3, seed=1)]
    # cluster-level directional coverage
    groups = {k: [F[i] for i in cset] for k, cset in enumerate(communities)}
    for ka, ga in groups.items():
        for kb, gb in groups.items():
            sel = pairs[pairs.origin.isin(ga) & pairs.destination.isin(gb)]
            cluster_cov[f"community{ka}->community{kb}"] = round(float(sel.coverage_origin_to_dest.mean()), 3)
    fc_dom = [r["family"] for r in frows if r["core_FC"] >= 0.6]
    cov_into_fc = pairs[pairs.destination.isin(fc_dom) & ~pairs.origin.isin(fc_dom)].coverage_origin_to_dest.mean()
    cov_out_fc = pairs[pairs.origin.isin(fc_dom) & ~pairs.destination.isin(fc_dom)].coverage_origin_to_dest.mean()

    # ---- can a 3-dimensional craft-blend vector discriminate pathways? (CA architecture question 1)
    bv = blend[["weighted_FC", "weighted_DC", "weighted_SC"]].values
    Cb = sim_matrix(bv, cosine)
    ub = upper(Cb)
    craft_blend_check = {
        "pairwise_cosine_min_median_max": [round(float(ub.min()), 3), round(float(np.median(ub)), 3), round(float(ub.max()), 3)],
        "share_of_pairs_cosine_ge_0.95": round(float((ub >= 0.95).mean()), 3),
        "spearman_vs_wjaccard": round(spearman(upper(J), ub), 3),
        "note": "high cosine for most pairs = blends alone cannot separate destinations; use task overlap for similarity",
    }

    # ---- summary
    sym = pairs.loc[[a < b for a, b in zip(pairs.origin.map(F.index), pairs.destination.map(F.index))]].copy()
    top = sym.sort_values("wjaccard", ascending=False).head(8)
    bottom = sym.sort_values("wjaccard").head(8)
    topz = sym.sort_values("null_z", ascending=False).head(8)
    asym = pairs.sort_values("asymmetry", ascending=False).head(8)
    summary = {
        "source": os.path.relpath(SRC, REPO), "n_competencies": int(n_c), "n_families": n_f,
        "competencies_untagged_any_family": int((n_tag == 0).sum()),
        "competencies_single_family": int((n_tag == 1).sum()),
        "median_families_per_competency": float(np.median(n_tag)),
        "mean_pairwise_wjaccard": round(float(upper(J).mean()), 3),
        "range_pairwise_wjaccard": [round(float(upper(J).min()), 3), round(float(upper(J).max()), 3)],
        "pairs_above_null_z2": int((upper(Z) > 2).sum()), "pairs_below_null_zminus2": int((upper(Z) < -2).sum()),
        "spearman_primary_vs": {
            "cosine": round(spearman(upper(J), upper(C)), 3),
            "specificity_weighted": round(spearman(upper(J), upper(Jidf)), 3),
            "sup0.25": round(spearman(upper(J), upper(sens["sup0.25"])), 3),
            "sup0.75": round(spearman(upper(J), upper(sens["sup0.75"])), 3),
            "core_only": round(spearman(upper(J), upper(sens["core_only"])), 3),
        },
        "communities_louvain": [[f"{F[i]} {names[F[i]]}" for i in cset] for cset in communities],
        "modularity": round(float(modularity), 3),
        "hierarchical_labels_same_k": ({F[i]: int(hc_labels[i]) for i in range(n_f)} if hc_labels is not None else None),
        "top_pairs_wjaccard": top[["origin", "destination", "wjaccard", "null_z"]].values.tolist(),
        "bottom_pairs_wjaccard": bottom[["origin", "destination", "wjaccard", "null_z"]].values.tolist(),
        "top_pairs_beyond_chance": topz[["origin", "destination", "wjaccard", "null_z"]].values.tolist(),
        "most_asymmetric_ordered_pairs": asym[["origin", "destination", "coverage_origin_to_dest",
                                               "coverage_dest_to_origin", "asymmetry"]].values.tolist(),
        "bridge_type_counts": bridges["bridge_type"].value_counts().to_dict(),
        "backbone_z_gt_2": backbone,
        "partition_stability": stability,
        "cluster_directional_coverage": cluster_cov,
        "fc_dominant_families_core_FC_ge_0.6": fc_dom,
        "mean_coverage_into_fc_dominant_from_others": round(float(cov_into_fc), 3),
        "mean_coverage_out_of_fc_dominant_to_others": round(float(cov_out_fc), 3),
        "top_bridges": bridges.head(12)[["competency_code", "competency_title", "bridge_type",
                                         "cross_community_contribution"]].values.tolist(),
        "craft_blend_similarity_check": craft_blend_check,
        "cld_share_overall": round(float(cld.mean()), 3),
        "cld_share_top25_bridges": round(float(bridges.head(25).cld_flag.mean()), 3),
        "cld_share_by_bridge_type": {k: round(float(v), 3) for k, v in bridges.groupby("bridge_type").cld_flag.mean().items()},
        "cld_share_by_craft_primary": {k: round(float(v), 3) for k, v in pd.Series(cld).groupby(prim.values).mean().items()},
        "baseline_crosscheck": _baseline_check(dt, fam_cols),
        "domain7_share_of_core_bridges": round(float(
            bridges[bridges.bridge_type == "cross-community core bridge"].competency_code.str.startswith("7.").mean()), 3),
        "taxonomy_craft_baseline": {k: round(v, 3) for k, v in base.items()},
        "cld_flag_value_vocab_seen": sorted(dt["T13: CLD Flag"].fillna("").unique().tolist()),
    }
    with open(os.path.join(HERE, "transferability_summary.json"), "w") as fh:
        json.dump(summary, fh, indent=2, default=str)
    print(json.dumps(summary, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
