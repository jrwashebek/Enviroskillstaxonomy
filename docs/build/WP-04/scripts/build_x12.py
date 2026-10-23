"""X12: EMST TX-A floor and DC responsible-AI practice -> DOL AI Literacy Framework (ETA TEN 07-25, Attachment I, 2026-02-13).

Official names verified against the primary attachment (WebFetch of the DOL PDF, 2026-10-23); see the .sssom.yml.
Object IDs are EMST-coined slugs of the official names (DOL publishes no identifiers); upstream text is not stored
in the TSV (no object_label; ADR-0013 §5). Grain: competency x level (ADR-0022 X12); the level is in `other`.
"""
import sys
from pathlib import Path

sys.path.insert(0, "/home/claude/emst/scripts")
import emstlib as L  # noqa: E402

REPO = Path("/home/claude/emst")
OUT = REPO / "data/v2/crosswalks/dol-ai-literacy"
VERSION_TAG = "ten-07-25"
TOOL = "docs/build/WP-04/scripts/build_x12.py@0.1.0"
AUTHOR = "emstagent:A4-DC@wp-04"
OBJ_SRC = "emstsrc:dol-ai-literacy-framework"
OBJ_VER = "ETA TEN 07-25 Attachment I (2026-02-13); names verified 2026-10-23"

# Official names (Attachment I), slug -> official name. Kept in the metadata description, not as object labels.
AREAS = {
    "understand-ai-principles": "Understand AI Principles",
    "explore-ai-uses": "Explore AI Uses",
    "direct-ai-effectively": "Direct AI Effectively",
    "evaluate-ai-outputs": "Evaluate AI Outputs",
    "use-ai-responsibly": "Use AI Responsibly",
}
SUBS = {
    "understand-ai-principles": ["Pattern recognition and probabilistic outputs", "Capabilities and modalities", "Training and inference",
                                 "Hallucinations and accuracy limits", "Human design and oversight"],
    "explore-ai-uses": ["Productivity tools", "Information support", "Creative assistance", "Task-specific applications", "Decision-support systems"],
    "direct-ai-effectively": ["Contextual framing", "Prompting techniques", "Supplying relevant input data", "Iterating on outputs",
                              "Avoiding vague or misleading prompts"],
    "evaluate-ai-outputs": ["Verifying factual accuracy", "Assessing completeness and clarity", "Spotting gaps or logical errors",
                            "Aligning with strategic intent", "Applying human judgment"],
    "use-ai-responsibly": ["Protecting sensitive information", "Following workplace policies and rules", "Avoiding misuse or harm",
                           "Managing context-specific risks", "Maintaining accountability"],
}
PRINCIPLES = ["Enable Experiential Learning", "Embed Learning in Context", "Build Complementary Human Skills", "Address Prerequisites to AI Literacy",
              "Create Pathways for Continued Learning", "Prepare Enabling Roles", "Design for Agility"]


def slug(s):
    return s.lower().replace(" ", "-").replace(",", "")


VALID = set()
for a in AREAS:
    VALID.add(f"DOLAIL:content-area/{a}")
    for s in SUBS[a]:
        VALID.add(f"DOLAIL:content-area/{a}/{slug(s)}")
for p in PRINCIPLES:
    VALID.add(f"DOLAIL:delivery-principle/{slug(p)}")


def obj(path):
    o = f"DOLAIL:{path}"
    assert o in VALID, o
    return o


LABELS = {}
for p in (REPO / "data/v2/core/competencies").glob("*.yaml"):
    d = L.load_yaml(p)
    LABELS[d["id"]] = d["prefLabel"]["en"]
for p in (REPO / "data/v2/core/enactments").glob("*.yaml"):
    d = L.load_yaml(p)
    LABELS[d["id"]] = d["prefLabel"]["en"]

ROWS = []
NTF = "sssom:NoTermFound"


def row(subj, level, pred, target, conf, why, via=(), weakest=None):
    assert subj in LABELS, subj
    oid = NTF if target is None else obj(target)
    rid_tail = "NoTermFound" if target is None else target.split("/")[-1]
    rid = f"emst-x12:{subj.split(':', 1)[1]}:{level}:{rid_tail}"
    other = [f"weakest_match_type={weakest or pred}", f"emst_level={level}"]
    if via:
        other.append("via_indicators=" + "|".join(via))
    other += ["review_status=candidate", "evidence=J", "rater_type=llm", "model=claude-opus-5-5", "prompt=wp04-x12@1",
              "co_owner_review=LC"]
    if target is None:
        other.append("no_term_reason=dol-lacks-environmental-validation-content")
    ROWS.append({"record_id": rid, "subject_id": subj, "subject_label": LABELS[subj], "subject_source": "emstsrc:emst-v2-competencies",
                 "predicate_id": pred, "object_id": oid, "object_source": OBJ_SRC, "object_source_version": OBJ_VER,
                 "mapping_justification": "semapv:LLMBasedMatching", "confidence": f"{conf:.2f}", "author_id": AUTHOR,
                 "mapping_date": "2026-10-23", "mapping_tool": TOOL, "other": ";".join(other), "comment": why})


CA = "content-area"
# ---------------------------------------------------------------- TX-A floor
C = "seed:DC-CAND-02"
row(C, "L1", "skos:closeMatch", f"{CA}/use-ai-responsibly/protecting-sensitive-information", 0.70,
    "L1 checks that a tool is approved for the data class and withholds sensitive items before entering task information; DOL's element covers which data stay out of AI tools.", ["seed:dc-cand-02-l1-a"])
row(C, "L1", "skos:closeMatch", f"{CA}/use-ai-responsibly/following-workplace-policies-and-rules", 0.65,
    "The floor requires following the employer's AI rules; the L1 approved-tool check is the observable act.", ["seed:dc-cand-02-l1-a"])
row(C, "L1", "skos:relatedMatch", f"{CA}/use-ai-responsibly/maintaining-accountability", 0.50,
    "L1 labels AI-assisted content and records checks; DOL's accountability element is broader and does not specify disclosure.", ["seed:dc-cand-02-l1-c"])
row(C, "L1", "skos:closeMatch", f"{CA}/evaluate-ai-outputs/verifying-factual-accuracy", 0.65,
    "L1 verifies each factual claim and citation against a source before use.", ["seed:dc-cand-02-l1-b"])
row(C, "L1", "skos:relatedMatch", f"{CA}/explore-ai-uses", 0.40,
    "Deciding whether and how to use an AI tool for a task draws on knowing the uses DOL lists; EMST assesses the decision, not the survey of uses.", ["seed:dc-cand-02-l1-a"])
row(C, "L1", "skos:relatedMatch", f"{CA}/understand-ai-principles", 0.30,
    "Principles (probabilistic outputs, hallucination, training) are knowledge underpinning the floor; EMST has no knowledge statements for them yet.")
row(C, "L2", "skos:closeMatch", f"{CA}/direct-ai-effectively", 0.60,
    "L2 directs a tool with the task context and source documents and iterates, checking each draft against the work standard.", ["seed:dc-cand-02-l2-b"])
row(C, "L2", "skos:relatedMatch", f"{CA}/use-ai-responsibly/managing-context-specific-risks", 0.50,
    "L2 declines AI use where checking would cost more than doing the work; DOL's element names context-specific risk without a decision rule.", ["seed:dc-cand-02-l2-a"])
row(C, "L3", "skos:relatedMatch", "delivery-principle/prepare-enabling-roles", 0.35,
    "L3 coaches a team and writes task-specific guidance; DOL's principle prepares the people who support AI literacy. A delivery principle, not a content area.", ["seed:dc-cand-02-l3-a", "seed:dc-cand-02-l3-b"])
row(C, "L4", "skos:closeMatch", None, 0.70,
    "no-term reason: the framework sets content areas and delivery principles but no assessable attainment standard by role; L4 measures attainment with scored work samples.", ["seed:dc-cand-02-l4-b"])

C = "seed:DC-CAND-13"
row(C, "L1", "skos:broadMatch", f"{CA}/evaluate-ai-outputs", 0.70,
    "EMST validation is the environmental case of evaluating AI outputs: checks against field evidence, source documents and applicable legal text, with a validation record.", ["seed:dc-cand-13-l1-a", "seed:dc-cand-13-l1-c"])
row(C, "L1", "skos:broadMatch", f"{CA}/evaluate-ai-outputs/verifying-factual-accuracy", 0.60,
    "L1 checks outputs against source or field evidence with a checklist; DOL checks against trusted sources or known information.", ["seed:dc-cand-13-l1-a", "seed:dc-cand-13-l1-b"])
row(C, "L1", "skos:relatedMatch", f"{CA}/evaluate-ai-outputs/applying-human-judgment", 0.50,
    "Correcting or rejecting outputs before use applies human judgment; EMST adds the record of what was checked.", ["seed:dc-cand-13-l1-a"])
row(C, "L2", "skos:closeMatch", f"{CA}/evaluate-ai-outputs/assessing-completeness-and-clarity", 0.55,
    "L2 flags omissions and out-of-scope answers as well as errors.", ["seed:dc-cand-13-l2-b"])
row(C, "L2", "skos:relatedMatch", f"{CA}/evaluate-ai-outputs/spotting-gaps-or-logical-errors", 0.45,
    "Omission detection overlaps DOL's gap-spotting element.", ["seed:dc-cand-13-l2-b"])
row(C, "L2", "skos:closeMatch", None, 0.75,
    "no-term reason: validation at volume (drawing a defined sample of AI outputs and estimating the batch error rate) has no counterpart in TEN 07-25.", ["seed:dc-cand-13-l2-a", "seed:dc-cand-13-dc-l2-a"])
row(C, "L4", "skos:closeMatch", None, 0.65,
    "no-term reason: organizational validation standards set by consequence of error are outside a worker literacy framework.", ["seed:dc-cand-13-l4-a"])
row("seed:ena-dc-cand-13-fc", "L1", "skos:closeMatch", None, 0.80,
    "no-term reason: ecological plausibility and field ground truth. DOL's verification checks against trusted sources or known information and sets no domain or field evidence standard.")
row("seed:ena-dc-cand-13-dc", "L3", "skos:closeMatch", None, 0.80,
    "no-term reason: batch acceptance rules from estimated error rates and condition-level error comparison.", ["seed:dc-cand-13-dc-l3-a", "seed:dc-cand-13-dc-l3-b"])
row("seed:v1-7.1.4-A", "L3", "skos:closeMatch", None, 0.80,
    "no-term reason: legal sufficiency of AI-assisted analyses, survival of substantive comments through machine grouping, AI provenance in the administrative record and authorization of oversight. DOL's accountability element is generic.",
    ["seed:dc-cand-13-sc-l2-a", "seed:dc-cand-13-sc-l3-a", "seed:dc-cand-13-sc-l3-b", "seed:dc-cand-13-sc-l4-a"])

C = "seed:v1-7.2.3"
row(C, "L1", "skos:closeMatch", f"{CA}/evaluate-ai-outputs/applying-human-judgment", 0.55,
    "L1 applies an explicit decision checkpoint before accepting an AI output in high-consequence work; DOL asks that outputs not be treated as final without review.", ["seed:ind-v1-7.2.3-l1-a"])
row(C, "L1", "skos:relatedMatch", f"{CA}/understand-ai-principles/hallucinations-and-accuracy-limits", 0.45,
    "Knowing that outputs can be confidently wrong underpins calibrated trust; EMST assesses the calibration behaviour, not the knowledge.", ["seed:ind-v1-7.2.3-l1-b"])
row(C, "L2", "skos:closeMatch", None, 0.75,
    "no-term reason: mapping a specific tool's reliability across operating conditions and keeping calibration records reviewed against outcomes.", ["seed:ind-v1-7.2.3-l2-a", "seed:ind-v1-7.2.3-l2-b"])
row(C, "L3", "skos:relatedMatch", "delivery-principle/build-complementary-human-skills", 0.35,
    "Team calibration programmes protect the human judgment DOL's principle asks programmes to build.", ["seed:ind-v1-7.2.3-l3-a"])

C = "seed:DC-CAND-05"
row(C, "L1", "skos:relatedMatch", f"{CA}/use-ai-responsibly/maintaining-accountability", 0.45,
    "Recording the AI tool used and the source of each input supports accountability; DOL does not mention documenting AI use or provenance.", ["seed:dc-cand-05-l1-a"])
row(C, "L2", "skos:closeMatch", None, 0.75,
    "no-term reason: lineage records tracing inputs, transformations, model and AI steps and human review to an output.", ["seed:dc-cand-05-l2-a"])

C = "seed:DC-CAND-01"
row(C, "L1", "skos:closeMatch", None, 0.70,
    "no-term reason: interpreting environmental data products (what was measured, where, when, at what resolution) is data literacy, outside an AI literacy framework.", ["seed:dc-cand-01-l1-a"])
row(C, "L2", "skos:relatedMatch", f"{CA}/evaluate-ai-outputs/spotting-gaps-or-logical-errors", 0.30,
    "Detecting planted problems in a data product resembles DOL's gap-spotting element applied to non-AI products.", ["seed:dc-cand-01-l2-a"])

# ---------------------------------------------------------------- DC specialist responsible-AI and related DC practice
row("seed:DC-CAND-14", "L2", "skos:relatedMatch", f"{CA}/understand-ai-principles/human-design-and-oversight", 0.45,
    "DOL asks workers to understand that people design and oversee AI; EMST designs the oversight (review rates, thresholds, escalation).", ["seed:dc-cand-14-l2-a"])
row("seed:DC-CAND-14", "L3", "skos:closeMatch", None, 0.80,
    "no-term reason: measuring whether human review is substantive (override rates, time on item, seeded-error catch rates).", ["seed:dc-cand-14-l3-a"])
row("seed:DC-CAND-15", "L2", "skos:closeMatch", None, 0.80,
    "no-term reason: task-specific, independently labelled reference sets and benchmarking AI tools against the current human process.", ["seed:dc-cand-15-l2-a", "seed:dc-cand-15-l3-a"])
row("seed:DC-CAND-16", "L1", "skos:broadMatch", f"{CA}/evaluate-ai-outputs/verifying-factual-accuracy", 0.60,
    "Verifying each machine-extracted statement against the cited passage is a specific case of verifying factual accuracy.", ["seed:dc-cand-16-l1-a", "seed:dc-cand-16-l1-b"])
row("seed:DC-CAND-16", "L1", "skos:relatedMatch", f"{CA}/explore-ai-uses/task-specific-applications", 0.35,
    "Machine-assisted extraction from plans, permits and comments is a task-specific application.", ["seed:dc-cand-16-l1-a"])
row("seed:DC-CAND-16", "L2", "skos:closeMatch", None, 0.75,
    "no-term reason: measuring omission and fabrication rates of an extraction against a gold set and documenting limits for the responsible official.", ["seed:dc-cand-16-l2-b"])
row("seed:DC-CAND-19", "L2", "skos:relatedMatch", f"{CA}/use-ai-responsibly/managing-context-specific-risks", 0.45,
    "A model risk assessment for a use is the organizational form of managing context-specific risk.", ["seed:dc-cand-19-l2-a"])
row("seed:DC-CAND-19", "L3", "skos:closeMatch", None, 0.80,
    "no-term reason: model inventories, consequence tiers, independent challenge and re-validation triggers.", ["seed:dc-cand-19-l3-a", "seed:dc-cand-19-l3-b"])
row("seed:DC-CAND-20", "L2", "skos:closeMatch", None, 0.80,
    "no-term reason: acceptance tests, documentation requirements and data-rights terms for procured AI and analytics services.", ["seed:dc-cand-20-l2-a", "seed:dc-cand-20-l3-b"])
row("seed:DC-CAND-21", "L4", "skos:relatedMatch", "delivery-principle/prepare-enabling-roles", 0.30,
    "Enterprise governance includes workforce data and AI capability, which DOL's principle addresses for training systems.", ["seed:dc-cand-21-l4-a"])
row("seed:DC-CAND-21", "L5", "skos:closeMatch", None, 0.75,
    "no-term reason: enterprise data and AI portfolio strategy, catalogue and use-case inventory governance.", ["seed:dc-cand-21-l5-a"])
row("seed:DC-CAND-07", "L1", "skos:relatedMatch", f"{CA}/use-ai-responsibly/protecting-sensitive-information", 0.50,
    "EMST protects sensitive ecological, cultural-resource and personal information in all data products; DOL's element concerns what is entered into AI tools.", ["seed:dc-cand-07-l1-a"])
row("seed:DC-CAND-07", "L3", "skos:closeMatch", None, 0.75,
    "no-term reason: leakage of withheld information through training sets, embeddings, retrieval corpora and high-resolution outputs.", ["seed:dc-cand-07-l3-a"])
row("seed:DC-CAND-09", "L1", "skos:relatedMatch", f"{CA}/understand-ai-principles/hallucinations-and-accuracy-limits", 0.30,
    "Checking a model's intended envelope before use rests on knowing models have accuracy limits.", ["seed:dc-cand-09-l1-a"])
row("seed:DC-CAND-09", "L2", "skos:closeMatch", None, 0.80,
    "no-term reason: independent validation with spatially or temporally blocked hold-outs or field reference data and a stated domain of applicability.", ["seed:dc-cand-09-l2-a"])
row("seed:DC-CAND-18", "L2", "skos:relatedMatch", f"{CA}/direct-ai-effectively/supplying-relevant-input-data", 0.40,
    "Curating the authoritative corpus an assistant retrieves from is the organizational form of supplying relevant input data.", ["seed:dc-cand-18-l2-a"])
row("seed:DC-CAND-18", "L3", "skos:closeMatch", None, 0.70,
    "no-term reason: testing retrieval over a curated corpus for answers drawn from superseded or non-authoritative sources.", ["seed:dc-cand-18-l3-a"])
row("seed:DC-CAND-08", "L2", "skos:relatedMatch", f"{CA}/evaluate-ai-outputs/spotting-gaps-or-logical-errors", 0.40,
    "Testing AI-generated analysis code on cases with known answers is an applied form of spotting errors.", ["seed:dc-cand-08-l2-b"])
# ---------------------------------------------------------------- formation (TX-D, WP-07 record; LC co-owns X12)
row("seed:v1-7.2.2", "L3", "skos:relatedMatch", "delivery-principle/build-complementary-human-skills", 0.50,
    "Designing developmental work that preserves the formation of judgment under AI augmentation corresponds to DOL's complementary-skills principle (LC to review; WP-07 record).")
row("seed:v1-7.2.2", "L3", "skos:relatedMatch", "delivery-principle/enable-experiential-learning", 0.40,
    "Protected, supervised practice is experiential learning (LC to review; WP-07 record).")
row("seed:v1-7.2.2", "L3", "skos:relatedMatch", "delivery-principle/embed-learning-in-context", 0.40,
    "EMST formation design embeds AI practice in real environmental tasks (LC to review; WP-07 record).")

# ---------------------------------------------------------------- write
COLS = ["record_id", "subject_id", "subject_label", "subject_source", "predicate_id", "object_id", "object_source", "object_source_version",
        "mapping_justification", "confidence", "author_id", "mapping_date", "mapping_tool", "other", "comment"]
OUT.mkdir(parents=True, exist_ok=True)
assert len({r["record_id"] for r in ROWS}) == len(ROWS)
for r in ROWS:
    for c in COLS:
        assert "\t" not in r[c] and "\n" not in r[c], (r["record_id"], c)
tsv = "\t".join(COLS) + "\n" + "".join("\t".join(r[c] for c in COLS) + "\n" for r in ROWS)
(OUT / f"{VERSION_TAG}.sssom.tsv").write_text(tsv, encoding="utf-8")

names = "; ".join(f"content-area/{k} = '{v}' (examples: " + ", ".join(f"{slug(s)} = '{s}'" for s in SUBS[k]) + ")" for k, v in AREAS.items())
prin = "; ".join(f"delivery-principle/{slug(p)} = '{p}'" for p in PRINCIPLES)
meta = {
    "mapping_set_id": f"https://w3id.org/emst/crosswalks/dol-ai-literacy/{VERSION_TAG}",
    "mapping_set_version": "0.1.0-draft",
    "mapping_set_title": "X12: EMST TX-A floor and data-craft responsible-AI practice to the DOL Artificial Intelligence Literacy Framework (ETA TEN 07-25)",
    "mapping_set_description": (
        "Agent-drafted candidate mappings (WP-04, DC; LC co-owner reviews), grain competency x level (level in `other`). Subjects are EMST v2 "
        "competencies and craft enactments; objects are the five foundational content areas, their example elements and the seven delivery "
        "principles of 'The Department of Labor's Artificial Intelligence Literacy Framework', Attachment I to Training and Employment Notice "
        "07-25 (February 13, 2026). DOL publishes no identifiers, so object IDs are EMST slugs of the official names, verified against the "
        "primary attachment on 2026-10-23: " + names + "; " + prin + ". sssom:NoTermFound (with skos:closeMatch, the predicate sought) is "
        "recorded where DOL lacks environmental validation content (field ground truth, sampling at volume, legal sufficiency, provenance, "
        "evaluation sets, model risk, procurement). Navigation and analytics grade only (ADR-0022 §4): no public claim of DOL alignment until "
        "a reviewed set exists. Re-run on each DOL revision."),
    "subject_source": "emstsrc:emst-v2-competencies",
    "subject_source_version": "2.0.0-draft",
    "object_source": OBJ_SRC,
    "object_source_version": OBJ_VER,
    "see_also": ["https://www.dol.gov/agencies/eta/advisories/ten-07-25",
                 "https://www.dol.gov/sites/dolgov/files/ETA/advisories/TEN/2025/TEN%2007-25/TEN%2007-25%20%28complete%20document%29.pdf",
                 "https://w3id.org/emst/seed/ins/dol-ai-literacy-framework"],
    "mapping_tool": TOOL,
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "creator_id": [AUTHOR],
    "mapping_date": "2026-10-23",
    "curie_map": {
        "emst": "https://w3id.org/emst/", "seed": "https://w3id.org/emst/seed/", "emstagent": "https://w3id.org/emst/agent/",
        "emstsrc": "https://w3id.org/emst/sources/", "sssom": "https://w3id.org/sssom/", "semapv": "https://w3id.org/semapv/vocab/",
        "skos": "http://www.w3.org/2004/02/skos/core#", "DOLAIL": "https://w3id.org/emst/ext/dol-ai-literacy/ten-07-25/"},
    "extension_definitions": [{"slot_name": "record_id", "property": "https://w3id.org/sssom/record_id", "type_hint": "xsd:string"}],
    "comment": ("EMST crosswalk set X12 (vocab/mapping_predicates.yaml#mapping_sets; ADR-0022, ADR-0025). The framework itself is registered "
                "as the L5 instrument seed:ins/dol-ai-literacy-framework. Object names are a U.S. Government work (17 U.S.C. 105). "
                "Sources: DC-015, DC-016 (corrected in docs/research/_verification/CORRECTIONS_REGISTER.csv, V4)."),
}
(OUT / f"{VERSION_TAG}.sssom.yml").write_text(L.dump_yaml(meta), encoding="utf-8")
from collections import Counter  # noqa: E402
print("X12 rows:", len(ROWS), dict(Counter(r["predicate_id"] + (" NoTermFound" if r["object_id"] == NTF else "") for r in ROWS)))
print("subjects:", len({r["subject_id"] for r in ROWS}), "DOL objects used:", len({r["object_id"] for r in ROWS if r["object_id"] != NTF}))
