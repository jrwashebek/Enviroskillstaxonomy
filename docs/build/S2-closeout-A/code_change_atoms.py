#!/usr/bin/env python3
"""S2 close-out A: coding pass over the WP-08 change-view atoms (CR-FH-001 #2 ruling; work order "coding-pass",
A7 FH raters, A9 LM writes the WP-10-lane files; done here in full).

Every atom in docs/build/WP-08/change_view_inputs.yaml goes to exactly one or more destinations:
  1. Technology task atoms (drivers AI, sensing-tech or automation-robotics, or 'stable' claims that current tools do
     not compress the task) -> three llm passes under emst-exposure@2.0: construct (a) technical exposure per vector,
     coded blind from the task text (XR-01; pass-specific random order, rating/xpass{n}.txt), plus contentChangeType
     coded with the atom's claim visible (rating/xchange.txt). Written to
     data/v2/assessments/emst-exposure@2.0/s2a-wp08-atoms-pass{n}.jsonl. One assessment per task and pass (a task in two
     roles' atoms is rated once). Deployment mode (construct b) is not coded: it needs a deployment evidence packet.
  2. Policy-reform atoms -> SC task-edge review (moves_task_edges.py rule: store only task-specific edges). The
     review finds every policy mechanism already inherited on SC-authored tasks; two proposals go to other lanes.
  3. Fiscal, demographic, workforce-capacity, climate and market atoms -> watch ChangeSignals. Where a sourced
     sector-level signal backs a role-level claim and no role-targeted signal exists, the published measure is attached
     to the role as a new watch signal (LM's convention for BLS projections: one signal per role, same independence key).
     Claims with no sourced measure are not turned into signals (nothing is invented); they are listed for LM/FS.
Output table: generated/change_atom_conversion.csv. Every value: raterType llm, evidence S, gate G0, unreviewed.
Usage: python3 docs/build/S2-closeout-A/code_change_atoms.py
Licence: Apache-2.0 (code); records CC0-1.0.
"""
from __future__ import annotations

import copy
import glob
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import emstlib as L  # noqa: E402

GEN = "2026-10-23T18:30:00Z"
TECH = {"AI", "sensing-tech", "automation-robotics"}
OTHER = {"fiscal", "demographic", "workforce-capacity", "climate", "market"}
ATOMS = ROOT / "docs/build/WP-08/change_view_inputs.yaml"
XOUT = L.DATA_V2 / "assessments" / "emst-exposure@2.0"
SIGOUT = L.DATA_V2 / "signals" / "2026" / "s2a-change-view-atoms.jsonl"
AGENT_X = "emstagent:fh-xrater-{n}@s2-closeout-a"
AGENT_W = "emstagent:fh-agent@s2-closeout-a"

# role-level non-technology claims backed by a sourced sector-level signal: (atom index, parent signal, role)
ATTACH = [
    (29, "seed:sig/foresight/ws-10-obbba-ira-rescissions", "seed:R09-restoration-project-lead"),
    (51, "seed:sig/headcount/epa-12849-jan-2026", "seed:R12-environmental-compliance-inspector"),
    (52, "seed:sig/headcount/federal-civilian-minus-12pct", "seed:R13-resource-program-manager"),
    (52, "seed:sig/headcount/epa-12849-jan-2026", "seed:R13-resource-program-manager"),
    (69, "seed:sig/foresight/ws-36-fire-season-2026", "seed:R07-fuels-prescribed-fire-specialist"),
]
# SC review of policy atoms (see moves_task_edges.py): proposals for tasks outside the SC lane
POLICY_PROPOSALS = {
    55: "Proposal to DC (author of DC-CAND-21): add a DM-14 digital-process edge on DC-CAND-21 (AI governance in review); "
        "no task-specific edge needed.",
    66: "Proposal to DB (author of seed:db-4.3.2-t4): task-specific DM-17 operator-certification edge with the FAA Part 108 "
        "proposal as context (beyond-visual-line-of-sight rules pending); the parent competency carries no edge.",
}


def load_recs():
    recs = {}
    for f in glob.glob(str(L.DATA_V2 / "core" / "*" / "*.yaml")) + glob.glob(str(L.DATA_V2 / "modules" / "*" / "*" / "*.yaml")):
        r = L.load_yaml(Path(f))
        if isinstance(r, dict) and r.get("id"):
            recs[r["id"]] = r
    return recs


def load_signals():
    sig = {}
    for f in glob.glob(str(L.DATA_V2 / "signals" / "*" / "*.jsonl")):
        if f.endswith("s2a-change-view-atoms.jsonl"):
            continue
        for line in Path(f).read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                sig[r["id"]] = r
    return sig


def is_tech(a):
    return a["target"] != "role" and (bool(set(a["drivers"]) & TECH) or
                                      (a["kind"] == "stable" and re.search(r"compress|tool", a["note"], re.I)))


def main():
    atoms = L.load_yaml(ATOMS)["atoms"]
    recs = load_recs()
    sigs = load_signals()
    frame = {}
    for i, a in enumerate(atoms):
        if is_tech(a):
            frame.setdefault(a["target"], []).append(i)
    tasks = sorted(frame)
    texts = {t: recs[t]["statement"]["en"] for t in tasks}
    for t in tasks:
        if recs[t].get("indigenousDataFlag"):
            raise SystemExit(f"{t} is held; never in a rating frame")
    change = {}
    for line in (HERE / "rating" / "xchange.txt").read_text().splitlines():
        if line.strip() and not line.startswith("#"):
            pos, *vals = line.split()
            change[tasks[int(pos) - 1]] = vals
    XOUT.mkdir(parents=True, exist_ok=True)
    for n in (1, 2, 3):
        order = sorted(texts.items())
        random.seed(10 + n)
        random.shuffle(order)
        lines = [l.split() for l in (HERE / "rating" / f"xpass{n}.txt").read_text().splitlines() if l.strip()]
        if len(lines) != len(order):
            raise SystemExit(f"xpass{n}: {len(lines)} ratings for {len(order)} tasks")
        out = []
        for pos, llm, rob, sen, conf in lines:
            tid, text = order[int(pos) - 1]
            stem = L.id_to_stem(tid)
            roles = sorted({atoms[i]["role"] for i in frame[tid]})
            out.append({
                "id": f"seed:asm/s2a-x-pass{n}/{stem}", "type": "ExposureAssessment",
                "prefLabel": {"en": f"S2 close-out A exposure pass {n} of {tid} (WP-08 change-view atom)"},
                "layer": "L5", "module": "core", "status": "draft", "license": "CC0-1.0", "sensitivity": "public",
                "task": tid, "taskTextSha256": L.text_sha256(text),
                "technicalExposure": [{"vector": "llm-cognitive", "level": llm}, {"vector": "robotics", "level": rob},
                                      {"vector": "sensing", "level": sen}],
                "contentChangeType": change[tid][n - 1],
                "raterType": "llm", "raterId": AGENT_X.format(n=n), "assessedAt": "2026-10-23",
                "method": (f"blind: true (construct a coded from the task text only, pass-specific random order seed "
                           f"{10 + n}; XR-01@2.0); contentChangeType coded separately with the WP-08 atom claim visible "
                           f"(atoms {', '.join(str(i) for i in frame[tid])}; roles {', '.join(roles)}); construct b not "
                           "coded (no deployment evidence packet). Same model and session as the author of the atoms' "
                           "role bundles: run-to-run consistency only, LLM-coder gate G0."),
                "confidence": conf, "instrument": "emst-exposure@2.0",
                "codebookVersion": "emst-exposure-codebook@2.0.0-draft (vocab/exposure_instrument_v2.yaml 2.0.0-draft)",
                "evidenceLabel": "S", "sources": [],
                "provenance": {"method": "llm-assisted", "agent": [AGENT_X.format(n=n)], "generatedAt": GEN,
                               "toolVersion": "claude-opus-5-5",
                               "promptVersion": f"docs/build/S2-closeout-A/rating/xpass{n}.txt + xchange.txt@s2a-exposure@1",
                               "evidenceLabel": "S", "reviewStatus": "unreviewed",
                               "adr": ["ADR-0008", "ADR-0028", "ADR-0030"]}})
        out.sort(key=lambda r: r["id"])
        L.write_jsonl(XOUT / f"s2a-wp08-atoms-pass{n}.jsonl", out)
    # ---------------------------------------------------------------- role-attached watch signals
    new_sigs = []
    for i, parent_id, role in ATTACH:
        p = sigs[parent_id]
        s = copy.deepcopy(p)
        slug = parent_id.split("seed:sig/", 1)[1]
        s["id"] = f"seed:sig/{slug}/{role.split(':', 1)[1]}"
        s["targetType"] = "RoleProfile"
        s["targetId"] = role
        s["prefLabel"] = {"en": p["prefLabel"]["en"] + f", attached to {role.split(':', 1)[1]}"}
        s["crosswalkPath"] = [f"attached from {parent_id} (sector-actor level) to {role} by WP-08 change-view atom {i}"]
        s["crosswalkMinMatchType"] = "skos:relatedMatch"
        s["signalStatus"] = "watch"
        s["reviewStatus"] = "unreviewed"
        s["evidenceLabel"] = "S"
        s["drivers"] = sorted(set(atoms[i]["drivers"]) & OTHER) or s.get("drivers")
        s["corroboration"] = p.get("corroboration", 1)
        s["editorialNote"] = {"en": (f"Role attachment of {parent_id} for the WP-08 role-level claim (atom {i}): "
                                     f"\"{atoms[i]['note']}\" Same published measure and independence key as the parent, "
                                     "so it is never counted twice (ADR-0028). Attachment is an agent judgment (S); "
                                     "LM to confirm (CR-FH-001 #2).")}
        s["provenance"] = {"method": "llm-assisted", "agent": [AGENT_W], "generatedAt": GEN,
                           "toolVersion": "docs/build/S2-closeout-A/code_change_atoms.py",
                           "promptVersion": "s2-closeout-a@1", "evidenceLabel": "S", "reviewStatus": "unreviewed",
                           "adr": "ADR-0028", "sources": sorted(set((p.get("provenance") or {}).get("sources") or []))}
        if not s["provenance"]["sources"]:
            s["provenance"].pop("sources")
        s["promptVersion"] = "s2-closeout-a@1"
        s["toolVersion"] = "docs/build/S2-closeout-A/code_change_atoms.py"
        new_sigs.append(s)
    new_sigs.sort(key=lambda r: r["id"])
    L.write_jsonl(SIGOUT, new_sigs)
    attached = {}
    for i, parent_id, role in ATTACH:
        attached.setdefault(i, []).append(f"seed:sig/{parent_id.split('seed:sig/', 1)[1]}/{role.split(':', 1)[1]}")
    # ---------------------------------------------------------------- conversion table
    rows = []
    for i, a in enumerate(atoms):
        dests = []
        dr = set(a["drivers"])
        if is_tech(a):
            dests.append("exposure: 3 llm passes (emst-exposure@2.0; s2a-wp08-atoms-pass1..3)")
        elif a["target"] != "role" and dr & TECH:
            dests.append("technology claim at role level: not a task assessment")
        if a["target"] == "role" and dr & TECH:
            dests.append("role-level technology claim: covered by role-targeted signals " +
                         (", ".join(s for s in a["signals"] if sigs.get(s, {}).get("targetId", "").startswith(a["role"]))
                          or "(none)"))
        if "policy-reform" in dr:
            if a["target"] == "role":
                dests.append("policy (role): computed from linked instruments and their events " +
                             (", ".join(a["instruments"]) or "(no instrument linked)"))
            elif i in POLICY_PROPOSALS:
                dests.append("policy (task): " + POLICY_PROPOSALS[i])
            else:
                dests.append("policy (task): SC review - mechanism inherited from the primary competency; no "
                             "task-specific edge")
        if dr & OTHER:
            role_sigs = [s for s in a["signals"] if sigs.get(s, {}).get("targetId", "").startswith(a["role"])]
            ctx = [s for s in a["signals"] if s not in role_sigs]
            parts = []
            if role_sigs:
                parts.append("existing role-targeted watch signals " + ", ".join(role_sigs))
            if i in attached:
                parts.append("new role-attached watch signals " + ", ".join(attached[i]))
            if ctx and i not in attached:
                parts.append("sector-level context signals " + ", ".join(ctx))
            if not parts:
                parts.append("no sourced measure: not turned into a signal (listed for LM/FS)")
            dests.append(f"{'/'.join(sorted(dr & OTHER))}: " + "; ".join(parts))
        if not dests:
            dests.append("no driver and not a technology claim")
        rows.append({"atom": i, "role": a["role"], "target": a["target"], "kind": a["kind"],
                     "drivers": "|".join(a["drivers"]), "destination": " || ".join(dests)})
    (HERE / "generated").mkdir(exist_ok=True)
    (HERE / "generated" / "change_atom_conversion.csv").write_text(
        L.csv_text(["atom", "role", "target", "kind", "drivers", "destination"], rows), encoding="utf-8")
    # consistency (not reliability)
    per = {}
    for n in (1, 2, 3):
        for line in (XOUT / f"s2a-wp08-atoms-pass{n}.jsonl").read_text().splitlines():
            r = json.loads(line)
            per.setdefault(r["task"], []).append((tuple(x["level"] for x in r["technicalExposure"]), r["contentChangeType"]))
    same_x = sum(1 for v in per.values() if len({x for x, _ in v}) == 1)
    same_c = sum(1 for v in per.values() if len({c for _, c in v}) == 1)
    summary = {"atoms": len(atoms), "technologyTasksCoded": len(tasks), "exposureRecords": 3 * len(tasks),
               "roleAttachedSignals": len(new_sigs), "policyProposals": len(POLICY_PROPOSALS),
               "allPassesEqual": {"technicalExposure": same_x, "contentChangeType": same_c},
               "note": "run-to-run consistency of one model, not inter-rater reliability; values stay assessment pending"}
    (HERE / "generated" / "change_atom_coding_summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
