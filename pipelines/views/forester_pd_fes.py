#!/usr/bin/env python3
"""Regenerate the v1 Forester PD prototype (legacy/v1/docs/forester_pd_transformation.html) from v2 data in FES format.

Source records: seed:R14-forester and its federal variant (bundle + adds - drops, journey level, the GS-9 to GS-11
band that the v1 prototype's GS-0460-09/11 position sits in), competency targets and knowledge statements, the 0460
SeriesRecord, the L1-L5 attribute definitions (vocab/proficiency_levels.yaml, which name their FES parallels) and the
role's journey level band (RoleProfile.roleLevels). Factor levels, points and grade are deliberately left to the
classifier: this is a draft "subject to classification review", not a classification. v1 duty percentages and exposure
calls are not reused (Q7; ADR-0027).

Display gate 1.1.0 (validation/display_gates.yaml; CR-CP-001 B4; ADR-0030 §1.8). The PD shows no time share,
importance, critical, needed-at-entry or distinguishing value and no LLM craft rating (fieldDependency and the other
CraftRating dimensions). Those values are not used to select, order or merge content either (gate `rollups` rule):
duties are grouped by the competency each task primarily supports (Task.supports, an editorial link), major duties are
the competencies whose home module is the role's own module (an editorial field), tasks keep the role record's order,
and each duty carries a blank percentage for the supervisor (gate label fsp_time_share_notice). Formation flags are
editorial design values and are shown inline. The four major-duty groups below are an editorial PD design choice made
by an AI agent (package review issue 18); any home-module competency not named in a group becomes its own duty.

Factors 2-5 are written at the full-performance end of the journey band (the upper level in the role's journey
levelBand) and a separate developmental statement uses the lower level (package review issue 18(b)).

Output: docs/package/forester_pd_fes_draft.md (sector-facing package). Licence of the output: CC0 1.0 as a generated
view; code Apache-2.0.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import viewlib as V  # noqa: E402

GEN = "pipelines/views/forester_pd_fes.py@0.2.0"
OUT = V.ROOT / "docs" / "package" / "forester_pd_fes_draft.md"
LEVEL = "journey"
PCT = "(___%)"
TIME_NOTICE = "% time: set by the supervisor; EMST supplies none before job analysis."  # display-gate role label
CTA = ("To comment, correct an error or ask about the pilot, open an issue at "
       "[github.com/jrwashebek/Enviroskillstaxonomy/issues](https://github.com/jrwashebek/Enviroskillstaxonomy/issues).")

# Editorial grouping of the role's home-module competencies into major duties, in rough work order (agent draft).
DUTY_GROUPS = [
    ("Inventory forest resources and assess forest conditions",
     ["seed:v1-1.3.2", "seed:v1-1.3.4", "seed:v1-1.3.3"]),
    ("Prescribe and implement silvicultural and fuels treatments",
     ["seed:v1-1.3.1", "seed:v1-4.3.3"]),
    ("Plan forest management and timber harvests to meet ecological and economic objectives",
     ["seed:v1-1.3.5"]),
    ("Prepare and administer timber sale, stewardship and partner implementation agreements",
     ["seed:FH-C02"]),
]


def attr(levels_vocab, level, key):
    for t in levels_vocab["terms"]:
        if t.get("notation") == level:
            return (t.get("descriptors") or {}).get(key, "")
    return ""


def lower_first(s):
    return s[:1].lower() + s[1:] if s else s


def sentence(stmt, formation):
    s = stmt.rstrip(".")
    return s + (" *(formation task)*." if formation else ".")


def plain_instrument(label):
    """Instrument labels without qualifiers that lack a checked citation (e.g. 'incl. EXPLORE Act amendments')."""
    return label.split(" incl. ")[0].strip()


def main():
    d = V.Data()
    role = d.get("seed:R14-forester")
    var = d.get("seed:R14-forester/federal")
    ser = d.series["0460"]
    pv = V.L.load_yaml(V.ROOT / "vocab" / "proficiency_levels.yaml")
    band = dict((x, b) for b, lv in V.band_pairs(var["indicativeGradeOrBand"]) for x in lv).get(LEVEL)
    low_grade, _, full_grade = (band or "").partition(" to ")
    level_band = next(r["levelBand"] for r in role["roleLevels"] if r["key"] == LEVEL)
    dev, full = level_band[0], level_band[-1]
    home = role.get("homeModule")

    items = V.at_levels(V.effective_bundle(role, var), [LEVEL])  # role-record order; time shares are not used
    targets = {t["competency"]: t for t in role.get("competencyTargets") or []}
    by_comp = defaultdict(list)
    for i in items:
        by_comp[V.primary_target(d, i["task"], targets)].append(i)
    comp_order = [c for c in targets if c in by_comp] + [c for c in by_comp if c not in targets]

    def home_module(cid):
        return (d.get(cid) or {}).get("homeModule")

    grouped = {c for _, cs in DUTY_GROUPS for c in cs}
    major = [(title, [c for c in cs if c in by_comp]) for title, cs in DUTY_GROUPS]
    major = [(t, cs) for t, cs in major if cs]
    major += [(d.label(c), [c]) for c in comp_order if home_module(c) == home and c not in grouped]
    major_comps = {c for _, cs in major for c in cs}
    related = [c for c in comp_order if c not in major_comps]

    duty_of_task = {}
    for n, (_, cs) in enumerate(major, 1):
        for c in cs:
            for i in by_comp[c]:
                duty_of_task[i["task"]] = f"duty {n}"
    for c in related:
        for i in by_comp[c]:
            duty_of_task[i["task"]] = "the related duties"

    contacts = [i for i in items if any(w in d.statement(i["task"]).lower() for w in
                                        ("landowner", "permittee", "contract", "purchaser", "consulting", "cooperating",
                                         "public", "partner"))]
    contact_duties = sorted({duty_of_task[i["task"]] for i in contacts}, key=lambda s: (not s.startswith("duty"), s))
    nums = [c.split()[1] for c in contact_duties if c.startswith("duty")]
    where = []
    if nums:
        where.append(("duty " if len(nums) == 1 else "duties ") + ", ".join(nums[:-1]) + (" and " if len(nums) > 1 else "")
                     + nums[-1])
    if "the related duties" in contact_duties:
        where.append("the related duties")
    gates = V.gate_text(V.gate_view(d, var.get("credentialGates")))
    instruments = ", ".join(plain_instrument(d.label(i)) for i in V.link_ids(var.get("instruments")))
    pos_ed = ("EMST's series record marks series 0460 as having a positive education requirement. This has not yet been "
              "checked against the current OPM qualification standard, which the servicing HR office should confirm."
              if ser.get("positiveEducationRequirement") else
              "EMST's series record shows no positive education requirement for series 0460; the servicing HR office "
              "should confirm this against the current OPM qualification standard.")

    lines = [
        "# Forester, GS-0460 — position description (FES format), regenerated from EMST v2 data",
        "",
        "> **DRAFT — SUBJECT TO CLASSIFICATION REVIEW.** Not a classification basis / not a job analysis / not for RIF or "
        "rating decisions. Generated from EMST v2 records that AI agents drafted and no human has reviewed. "
        + TIME_NOTICE + " No criticality or needed-at-entry flags are shown. Factor levels, points and grade are left to "
        "the servicing classifier, and the grade band is indicative only.",
        ">",
        "> **Status: draft for NGO-pilot preview (2026-10-23).** Drafted by a team of AI agents (Anthropic's Claude) "
        "working to a charter set by the EMST project lead; not yet reviewed by independent human experts.",
        "",
        "## Position information",
        "",
        f"- **Title, series and grade:** Forester, GS-0460-[grade set by the classifier]. Series 0460 "
        f"{ser['prefLabel']['en']} is {('active' if ser.get('seriesStatus') == 'active' else ser.get('seriesStatus'))} "
        f"in EMST's OPM series register as of {V.AS_OF} (re-check by {ser.get('reviewBy')}).",
        f"- **Indicative band:** {band} (EMST journey level). This draft is written at the full-performance end of the "
        f"band ({full_grade} indicative), with a developmental statement for the lower end ({low_grade} indicative). "
        "Not a classification criterion.",
        "- **Organization:** [to be completed by the servicing HR office: agency, unit, duty station].",
        "- **Supervisory status:** [to be completed by the servicing HR office].",
        "- **FLSA status:** [to be completed by the servicing HR office].",
        "- **Position sensitivity:** [to be completed by the servicing HR office].",
        "- **Bargaining unit status:** [to be completed by the servicing HR office; check with the labor-relations "
        "office before changing a PD on the basis of this draft].",
        "- **Competitive level:** [set by the servicing HR office; EMST content must not be used to define competitive "
        "levels or make retention decisions].",
        "- **Conditions of employment:** [to be determined by the agency, for example a driver's license, fire or incident "
        "duty, arduous duty, or a remote duty station].",
        f"- **Positive education requirement:** {pos_ed}",
        "",
        "## Introduction",
        "",
        f"{role['functionStatement']['en']} {role['definition']['en']}",
        "",
        "The Forester is not one of EMST's 13 corridor roles. It is shown because EMST v1 included a Forester position "
        "description prototype, which this regenerated version replaces.",
        "",
        "## Major duties",
        "",
        f"Each duty carries a blank percentage {PCT} for the supervisor to fill in. {TIME_NOTICE} The supervisor and the "
        "classifier identify the grade-controlling duty. An AI agent grouped the draft tasks into these duties, in "
        "rough work order; tasks marked *(formation task)* are those through which entry foresters build field "
        "judgment (agent-drafted flags).",
        "",
    ]
    for n, (title, cs) in enumerate(major, 1):
        lines += [f"### {n}. {title} {PCT}", ""]
        lines.append(" ".join(sentence(d.statement(i["task"]), i.get("formationTask")) for c in cs for i in by_comp[c]))
        lines.append("")
    if related:
        lines += [f"### {len(major) + 1}. Related duties {PCT}", "",
                  "Performs related work drawn from neighboring occupational areas:", ""]
        for c in related:
            lines.append(f"- **{d.label(c)}.** " + " ".join(sentence(d.statement(i["task"]), i.get("formationTask"))
                                                          for i in by_comp[c]))
        lines += ["",
                  "*Note for the classifier:* several related duties (for example species identification, environmental "
                  "impact review and protected-species consultation) are typical of other series. Confirm that each "
                  "belongs in a 0460 position before keeping it.", ""]

    tg = V.targets_at(d, role, [LEVEL])
    order = {c: k for k, c in enumerate(targets)}
    tg.sort(key=lambda t: order.get(t["competency"], 999))  # role-record order; importance is not used
    practice = [t for t in tg if t["competencyType"] != "transversal"]
    transversal = [t for t in tg if t["competencyType"] == "transversal"]
    lines += ["## Factor 1 — Knowledge required by the position", "",
              "*Draft knowledge statements from the role's competencies at the journey level (agent draft). "
              "Level: [classifier].*", ""]
    for t in practice:
        lines.append(f"- Knowledge of and skill to {lower_first(t['label'])}.")
        for ks in [k["statement"]["en"] for k in d.ks_by_comp.get(t["competency"], [])][:2]:
            lines.append(f"  - {ks}")
    if transversal:
        lines.append("- Basic data and AI skills that every EMST role includes: "
                     + "; ".join(lower_first(t["label"]) for t in transversal) + ".")
    lines += ["- Knowledge of the agency's environmental review procedures and of the partner-agreement authorities "
              f"that apply to forest management projects ({instruments}).", "",
              "## Factor 2 — Supervisory controls", "", "*Level: [classifier].*", "",
              f"{attr(pv, full, 'ATT-AUT')} The supervisor sets objectives, priorities and deadlines; completed "
              "prescriptions, cruises and sale packages are reviewed for conformance with plans and policy.", "",
              "## Factor 3 — Guidelines", "", "*Level: [classifier].*", "",
              f"{attr(pv, full, 'ATT-GUI')} Guidelines include the land management plan, agency silvicultural and "
              "timber-sale manuals and handbooks, inventory protocols, contract specifications and the agency's "
              "environmental review procedures. For AI-assisted and remotely sensed products, the incumbent "
              f"{lower_first(attr(pv, full, 'ATT-AUG'))}", "",
              "## Factor 4 — Complexity", "", "*Level: [classifier].*", "",
              f"{attr(pv, full, 'ATT-CPX')} Prescriptions must balance timber, habitat, fire risk, water and carbon "
              "objectives on stands whose structure, history and health vary; inventory designs must reconcile plot "
              "data with lidar and imagery products.", "",
              "## Factor 5 — Scope and effect", "", "*Level: [classifier].*", "",
              f"{attr(pv, full, 'ATT-SCO')} The work determines how stands are treated and how sales are laid out and "
              "administered, which affects resource conditions for decades and the agency's contract and environmental "
              "compliance record.", "",
              "## Factor 6 — Personal contacts", "", "*Level: [classifier].*", "",
              "Contacts are with other resource specialists, contract purchasers and operators, partner organizations, "
              "landowners and the public in the field and in meetings. They arise mainly in "
              + " and in ".join(where) + ".", "",
              "## Factor 7 — Purpose of contacts", "", "*Level: [classifier].*", "",
              "To plan and coordinate work, explain prescriptions and contract requirements, resolve operational "
              "problems with purchasers and partners, and secure compliance with contract specifications and best "
              "management practices.", "",
              "## Factor 8 — Physical demands", "", "*Level: [classifier].*", "",
              "Field work involves walking long distances over steep, rough and brushy terrain in all seasons, carrying "
              "equipment, and climbing over down timber. The supervisor confirms the physical demands for the duty "
              "station.", "",
              "## Factor 9 — Work environment", "", "*Level: [classifier].*", "",
              "Field work exposes the incumbent to weather extremes, hazard trees, active logging and equipment operations, "
              "insects, wildlife and remote locations with limited communication; protective equipment and the agency's "
              "field safety procedures apply. Office work is in an adequately lighted and ventilated setting.", "",
              f"## Developmental statement (lower end of the band, {low_grade} indicative)", "",
              "At the developmental level the incumbent performs the same duties with closer supervision and narrower "
              f"scope. Supervisory controls: {lower_first(attr(pv, dev, 'ATT-AUT'))} Guidelines: "
              f"{lower_first(attr(pv, dev, 'ATT-GUI'))} Complexity: {lower_first(attr(pv, dev, 'ATT-CPX'))} Scope: "
              f"{lower_first(attr(pv, dev, 'ATT-SCO'))} AI-assisted and remotely sensed products: the incumbent "
              f"{lower_first(attr(pv, dev, 'ATT-AUG'))}", "",
              "## Other information (EMST)", "",
              "- **Credential requirements:** " + (gates or "none recorded with a verified issuer for the federal "
                                                    "variant") + ".",
              "- **Selective placement or quality-ranking factors:** none. EMST v2.0 content is never used for selection; "
              "it is for describing and developing work only.",
              "- **How the work is changing:** no assessment by several independent human raters exists yet for these "
              "tasks (\"assessment pending\"). The v1 prototype's time-reallocation figures were single-analyst estimates "
              "and are methodology history only.",
              "- **Formation tasks:** keep unaided repetitions of the tasks marked *(formation task)* in development "
              "plans, so that entry foresters build field judgment.",
              f"- **Comment or correct:** {CTA}",
              "",
              "---",
              "",
              f"*Provenance (technical note).* Generated by `{GEN}` on {V.AS_OF} from EMST v2 records `{role['id']}` and "
              f"`{var['id']}` (agent drafts: raterType llm, validationStatus draft, evidence label S) and the OPM series "
              f"record `{ser['id']}`. Duty grouping is an editorial choice by an AI agent. Display rule: "
              "`validation/display_gates.yaml` 1.1.0 (no time share, importance, critical, needed-at-entry or "
              "distinguishing value and no craft rating is shown or used). Supersedes the v1 prototype "
              "`legacy/v1/docs/forester_pd_transformation.html` as the package version; v1 duty percentages and exposure "
              "calls are not reused (methodology history only).",
              "",
              "DRAFT — SUBJECT TO CLASSIFICATION REVIEW. Not a classification basis / not a job analysis / not for RIF or "
              "rating decisions.", ""]
    V.write_text(OUT, "\n".join(lines))
    print(f"wrote {OUT.relative_to(V.ROOT)}: {len(major)} major duties + related duties; journey band {band}")


if __name__ == "__main__":
    main()
