"""LC (A8) content for S2 close-out builder B: v1 5.1.3, 5.4.1 and 5.6.4 rewritten in place (work-order rows 20-22;
ADR-0030 §3.1 M1 for 5.6.4). Content evidence label J; basis in editorialNote.
"""
import s2b_lib as S

LC = ["LC"]
T, WS, RA, SEW, SIM, PR, KT = ("task-book-observation", "work-sample", "record-audit", "seeded-error-work-sample",
                               "simulation-role-play", "portfolio-review", "knowledge-test")


def d(key, rel="rewritten"):
    return {"v1Key": key, "relation": rel}


def rg(m="M", c="none", p="general", g="none", u="M"):
    return {"mentorshipDependence": m, "cycleDependence": c, "placeBoundness": p, "credentialGate": g, "currencyDecay": u}


INTERP = {
    "id": "seed:v1-5.1.3", "roles": LC, "row": "20",
    "label": "Interpret natural and cultural resources for visitors and community audiences",
    "alt": ["Environmental interpretation", "Interpretive materials development", "Heritage interpretation", "Interpretive planning"],
    "definition": (
        "Helping visitors and community audiences find meaning in natural and cultural features through theme-based "
        "programmes, guided walks, talks, signs, exhibits and digital media: researching accurate content, designing for "
        "the audience and the site, delivering or producing the interpretation, testing it with users and evaluating "
        "whether it worked, including interpretive planning for a site. Cultural content is interpreted only from sources "
        "cleared for public use with the communities whose heritage it is. Excludes visitor orientation and safety "
        "messaging (v1 5.5.1, parks), environmental education programmes (v1 5.4.1) and communicating technical findings "
        "(v1 5.1.1)."),
    "statement": (
        "Researches accurate natural and cultural content, builds programmes, walks, signs, exhibits and digital media "
        "around a clear theme for the intended audience and site, delivers or produces them, tests materials with users, "
        "and evaluates whether audiences made the intended connections, revising the interpretation from that evidence."),
    "reusability": "cross-subsector",
    "learningDesign": {"assessmentContext": {"en": "Assess through observed programmes against an interpretive performance standard, interpretive media portfolios and evaluation records; on site."},
                       "recommendedModes": ["WBL", "MEN", "CAP"]},
    "derived": [d("v1:5.4.5", "merged-from")],
    "adr": ["ADR-0030", "ADR-0004", "ADR-0003", "ADR-0011"],
    "note": (
        "S2 close-out B (A8 LC; ADR-0030 §4 core residue). Carried as core practice in cluster X04 and rewritten in place "
        "to v2 rules; absorbs v1 5.4.5 (interpretive materials), whose three task seeds are rewritten so they no longer "
        "duplicate 5.1.3-T2. Module enactments in parks, forest and wildlife were written in WP-06. v1 Expert indicators "
        "naming awards, publication or recognition are retired (B03, B04). Interpretive guide certification is a "
        "Credential, not a level. Needed by R21 (P2). Basis [J]."),
    "levels": {
        "L1": [
            {"id": "seed:lc-interp-l1-a", "mode": "unaided", "methods": [T, SIM],
             "text": "Delivers a scripted interpretive programme or walk to the site's interpretive plan, answering visitor questions accurately and referring those it cannot answer.",
             "served": ["seed:v1-5.1.3-T1"], "derived": [d("v1:5.1.3:foundational:I1"), d("v1:5.1.3:foundational:I2"), d("v1:5.1.3:foundational:I4")]},
            {"id": "seed:lc-interp-l1-b", "mode": "unaided", "methods": [WS, RA],
             "text": "Drafts interpretive text for a sign or brochure to the programme's style guide and word limit, citing the source for each fact.",
             "served": ["seed:v1-5.4.5-T1"], "derived": [d("v1:5.4.5:foundational:I1")]},
        ],
        "L2": [
            {"id": "seed:lc-interp-l2-a", "mode": "unaided", "methods": [WS, T], "att": "ATT-AUT",
             "text": "Designs an original interpretive programme around one theme for a stated audience, adapting activities for age and ability and recording the theme and objectives.",
             "served": ["seed:v1-5.1.3-T3", "seed:v1-5.4.5-T2"], "derived": [d("v1:5.1.3:intermediate:I1"), d("v1:5.1.3:intermediate:I2")]},
            {"id": "seed:lc-interp-l2-b", "mode": "unaided", "methods": [WS, RA], "att": "ATT-CPX",
             "text": "Tests a draft sign, panel or digital piece with members of the target audience, revising the text or design where most testers missed the theme.",
             "served": ["seed:v1-5.4.5-T3"], "derived": [d("v1:5.4.5:intermediate:I5")]},
        ],
        "L3": [
            {"id": "seed:lc-interp-l3-a", "mode": "unaided", "methods": [WS, PR], "att": "ATT-SCO",
             "text": "Prepares an interpretive plan for a site that sets themes, audiences, media and locations within resource protection and accessibility limits.",
             "served": ["seed:lc-interp-plan"], "derived": [d("v1:5.1.3:advanced:I1"), d("v1:5.4.5:advanced:I1")]},
            {"id": "seed:lc-interp-l3-b", "mode": "unaided", "methods": [RA, WS], "att": "ATT-SCO",
             "text": "Evaluates an interpretive programme or exhibit against its objectives from visitor observation or feedback, recording the changes made from the results.",
             "served": ["seed:lc-interp-evaluate"], "derived": [d("v1:5.1.3:advanced:I4"), d("v1:5.4.5:advanced:I4")]},
            {"id": "seed:lc-interp-l3-c", "mode": "unaided", "methods": [T, RA], "att": "ATT-FOR",
             "text": "Coaches interpreters and volunteers against an interpretive performance standard, giving each written feedback from an observed programme.",
             "served": ["seed:lc-interp-coach"], "derived": [d("v1:5.1.3:advanced:I3")]},
            {"id": "seed:lc-interp-l3-d", "mode": "assisted", "methods": [SEW, WS], "att": "ATT-AUG",
             "text": "Checks AI-generated or translated interpretive text against verified sources and the theme, correcting each factual or cultural error before it is published.",
             "served": ["seed:lc-interp-verify-generated"]},
        ],
        "L4": [
            {"id": "seed:lc-interp-l4-a", "mode": "unaided", "methods": [PR, WS], "att": "ATT-SCO",
             "text": "Sets interpretive standards and review steps for a park system or programme, covering accuracy checks, accessibility and review of cultural content with source communities.",
             "served": ["seed:lc-interp-standards"]},
            {"id": "seed:lc-interp-l4-b", "mode": "unaided", "methods": [PR, RA], "att": "ATT-SCO",
             "text": "Directs interpretive media development across sites, ranking projects by visitor need and resource sensitivity and approving each final design.",
             "served": ["seed:v1-5.1.3-T2"], "derived": [d("v1:5.4.5:expert:I1")]},
        ],
    },
    "tasks": [
        {"id": "seed:v1-5.1.3-T1", "wf": "WF-OPERATE", "field": "on-site-required", "formation": "partial", "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Lead a guided walk or programme that connects visitors with the site's ecological or cultural features through one interpretive theme",
         "regime": rg("M", "seasonal", "site-specific", u="M")},
        {"id": "seed:v1-5.1.3-T2", "wf": "WF-BUILD", "field": "on-site-preferred", "formation": "partial",
         "text": "Develop interpretive signs or exhibits for a visitor centre or trail from verified content, following the site's interpretive plan",
         "regime": rg("M", "none", "site-specific", u="L")},
        {"id": "seed:v1-5.1.3-T3", "wf": "WF-OPERATE", "field": "on-site-preferred", "formation": "partial", "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Structure an interpretive talk around a theme, tangible features and an invitation to act, rehearsing it before delivery",
         "regime": rg("M", "none", "site-specific", u="M")},
        {"id": "seed:v1-5.4.5-T1", "wf": "WF-BUILD", "field": "remote", "formation": "partial",
         "text": "Write interpretive text for brochures and trail signs within word limits, citing a verified source for every fact",
         "regime": rg("M", "none", "site-specific", u="L"),
         "note": "v1 5.4.5-T1 duplicated 5.1.3-T2 (signs and exhibits); rewritten as the writing task."},
        {"id": "seed:v1-5.4.5-T2", "wf": "WF-OPERATE", "field": "on-site-preferred", "formation": "partial", "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Adapt an interpretive piece for visitors with different languages, ages and abilities, including tactile, audio and plain-language versions",
         "regime": rg("M", "none", "general", u="L")},
        {"id": "seed:v1-5.4.5-T3", "wf": "WF-LEARN", "field": "on-site-preferred", "formation": "partial", "rel": ["public"],
         "text": "Test draft interpretive materials with target visitors before production, revising text or design where testers missed the theme",
         "regime": rg("M", "none", "site-specific", u="L")},
        {"id": "seed:lc-interp-plan", "wf": "WF-PLAN", "field": "on-site-preferred", "formation": "partial",
         "text": "Prepare an interpretive plan for a site that sets themes, audiences, media and locations within resource protection limits",
         "regime": rg("M", "multi-year-or-rare-event", "site-specific", u="L"), "contrib": ["seed:IA-CC-02"] if False else None},
        {"id": "seed:lc-interp-evaluate", "wf": "WF-LEARN", "field": "on-site-preferred", "formation": "partial",
         "text": "Evaluate an interpretive programme or exhibit against its objectives using visitor observation or feedback, recording the revisions made",
         "regime": rg("M", "seasonal", "site-specific", u="L")},
        {"id": "seed:lc-interp-verify-generated", "wf": "WF-BUILD", "field": "remote", "formation": "yes",
         "text": "Verify AI-generated or machine-translated interpretive text against verified sources and the theme, correcting factual or cultural errors before publication",
         "regime": rg("M", "none", "site-specific", u="M"), "contrib": ["seed:DC-CAND-13"],
         "note": "G-2 split: verifying generated text alongside the writing task seed:v1-5.4.5-T1."},
        {"id": "seed:lc-interp-coach", "wf": "WF-LEARN", "field": "on-site-required", "formation": "partial",
         "text": "Coach interpreters and volunteers from observed programmes, giving written feedback against the programme's interpretive standard",
         "regime": rg("M", "seasonal", "general", u="L"), "contrib": ["seed:IO-C01"]},
        {"id": "seed:lc-interp-standards", "wf": "WF-MANAGE", "field": "remote", "formation": "no",
         "text": "Set interpretive standards and review steps for a park system, including accuracy checks, accessibility and review of cultural content",
         "regime": rg("L", "none", "general", u="L")},
    ],
}

EE = {
    "id": "seed:v1-5.4.1", "roles": LC, "row": "21",
    "label": "Design and deliver environmental education programmes",
    "alt": ["Educational program development", "Curriculum design for environmental education", "Environmental literacy programmes",
            "Outdoor education"],
    "definition": (
        "Designing, delivering and evaluating structured environmental learning experiences for school, youth and adult "
        "audiences: setting learning objectives, aligning curricula with the education standards that apply, designing "
        "lessons and field experiences, preparing materials, managing programme logistics and safety, assessing learning "
        "and improving the programme from evidence. Absorbs curriculum design (v1 5.4.2) and the instructional-design "
        "remainder of immersive learning (v1 2.7.2). Excludes workforce learning and formation design (v1 7.2.2, TX-D), "
        "interpretation for visitors (v1 5.1.3) and community-science protocols (v1 5.4.4)."),
    "statement": (
        "Sets learning objectives for an audience, designs lessons, curricula and field experiences aligned with the "
        "education standards that apply, prepares materials and manages logistics and safety, delivers or supports "
        "delivery, assesses what participants learned, and revises the programme from that evidence."),
    "reusability": "cross-subsector",
    "learningDesign": {"assessmentContext": {"en": "Assess through lesson and curriculum work samples, observed delivery and evaluation records; field and classroom settings."},
                       "recommendedModes": ["WBL", "MEN", "CAP", "CL"]},
    "derived": [d("v1:5.4.2", "merged-from")],
    "adr": ["ADR-0030", "ADR-0004", "ADR-0003", "ADR-0011", "ADR-0026"],
    "note": (
        "S2 close-out B (A8 LC; ADR-0030 §4 core residue). Rewritten in place as environmental education programmes and "
        "curricula in cluster X04; absorbs v1 5.4.2 (curriculum design) and the instructional-design remainder of v1 "
        "2.7.2 (its three tasks, rewritten by DC in WP-04, already support this competency and are left as they are). "
        "Workforce learning lives in TX-D (LC verdict). Named national or state education standards are L5 instruments "
        "or external references, not text here; 'learning styles' in v1 text is not carried. Needed by R21 (P2). Basis [J]."),
    "levels": {
        "L1": [
            {"id": "seed:lc-ee-l1-a", "mode": "unaided", "methods": [T, RA],
             "text": "Delivers an established education programme to its lesson plan, adapting activities for the group's age with guidance and recording attendance and participant feedback.",
             "served": ["seed:lc-ee-deliver"], "derived": [d("v1:5.4.1:foundational:I1"), d("v1:5.4.1:foundational:I2"), d("v1:5.4.1:foundational:I5")]},
            {"id": "seed:lc-ee-l1-b", "mode": "unaided", "methods": [RA, T],
             "text": "Prepares materials, permissions and safety arrangements for a field programme or youth camp against the programme checklist before participants arrive.",
             "served": ["seed:v1-5.4.1-T2"], "derived": [d("v1:5.4.1:foundational:I3")]},
        ],
        "L2": [
            {"id": "seed:lc-ee-l2-a", "mode": "unaided", "methods": [WS, PR], "att": "ATT-AUT",
             "text": "Designs a programme or lesson sequence with measurable learning objectives, activities matched to each objective and an assessment for each, for a stated audience.",
             "served": ["seed:v1-5.4.1-T1", "seed:v1-5.4.2-T2"], "derived": [d("v1:5.4.1:intermediate:I1"), d("v1:5.4.2:intermediate:I1")]},
            {"id": "seed:lc-ee-l2-b", "mode": "unaided", "methods": [WS, RA], "att": "ATT-KNO", "jv": True,
             "text": "Aligns a curriculum unit with the applicable education standards, mapping each lesson to the standard it addresses.",
             "served": ["seed:v1-5.4.2-T1"], "derived": [d("v1:5.4.2:intermediate:I2")]},
            {"id": "seed:lc-ee-l2-c", "mode": "unaided", "methods": [RA, WS], "att": "ATT-AUT",
             "text": "Revises a programme after a formative evaluation, recording which participant results or feedback prompted each change.",
             "served": ["seed:v1-5.4.1-T3"], "derived": [d("v1:5.4.1:intermediate:I5"), d("v1:5.4.2:intermediate:I6")]},
        ],
        "L3": [
            {"id": "seed:lc-ee-l3-a", "mode": "unaided", "methods": [WS, RA], "att": "ATT-CPX",
             "text": "Evaluates a programme's learning outcomes with a pre-post or comparison design, reporting effects with their limits to funders and partners.",
             "served": ["seed:lc-ee-evaluate-outcomes"], "derived": [d("v1:5.4.1:advanced:I3")]},
            {"id": "seed:lc-ee-l3-b", "mode": "unaided", "methods": [WS, PR], "att": "ATT-SCO",
             "text": "Builds a programme partnership with schools or youth organizations that sets roles, schedules, safety responsibilities and the outcome data each partner shares.",
             "served": ["seed:lc-ee-partnership"], "derived": [d("v1:5.4.1:advanced:I7")]},
            {"id": "seed:lc-ee-l3-c", "mode": "assisted", "methods": [SEW, WS], "att": "ATT-AUG",
             "text": "Checks AI-generated lesson content or simulations against verified science and the learning objectives, correcting each error before use with learners.",
             "served": ["seed:lc-ee-verify-generated"]},
        ],
        "L4": [
            {"id": "seed:lc-ee-l4-a", "mode": "unaided", "methods": [PR, WS], "att": "ATT-SCO",
             "text": "Sets an organization's education strategy, choosing audiences, programme portfolio and evaluation measures, and the evidence used to drop or expand programmes.",
             "served": ["seed:lc-ee-evaluate-outcomes"], "derived": [d("v1:5.4.1:advanced:I1")]},
            {"id": "seed:lc-ee-l4-b", "mode": "unaided", "methods": [T, RA], "att": "ATT-FOR",
             "text": "Trains partner educators to deliver a curriculum to fidelity, observing delivery and recording where adaptations changed the learning objectives.",
             "served": ["seed:lc-ee-train-educators"], "derived": [d("v1:5.4.1:expert:I5")]},
        ],
    },
    "tasks": [
        {"id": "seed:v1-5.4.1-T1", "wf": "WF-PLAN", "field": "remote-capable", "formation": "partial", "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Design an outdoor education programme with learning objectives tied to environmental literacy goals for a stated audience",
         "regime": rg("M", "none", "general", u="L")},
        {"id": "seed:v1-5.4.1-T2", "wf": "WF-MANAGE", "field": "on-site-preferred", "formation": "no",
         "text": "Arrange logistics, materials, permissions and safety coverage for a youth camp or stewardship day before participants arrive",
         "regime": rg("L", "seasonal", "site-specific", u="L"), "contrib": ["seed:v1-4.4.1-A"]},
        {"id": "seed:v1-5.4.1-T3", "wf": "WF-LEARN", "field": "remote", "formation": "partial",
         "text": "Evaluate participant feedback and learning results after a programme, recording the changes planned for the next delivery",
         "regime": rg("M", "seasonal", "general", u="L")},
        {"id": "seed:v1-5.4.2-T1", "wf": "WF-PLAN", "field": "remote", "formation": "partial",
         "text": "Develop lesson plans aligned with the applicable science education standards, mapping each lesson to the standard it addresses",
         "regime": rg("M", "none", "general", u="M")},
        {"id": "seed:v1-5.4.2-T2", "wf": "WF-PLAN", "field": "remote-capable", "formation": "partial",
         "text": "Create a learning module on a local environmental topic such as watersheds or fire ecology, with field activities and assessments",
         "regime": rg("M", "none", "ecosystem-type", u="L")},
        {"id": "seed:v1-5.4.2-T3", "wf": "WF-PLAN", "field": "remote", "formation": "partial",
         "text": "Adapt curriculum materials for different age groups, languages and abilities while keeping the learning objectives intact",
         "regime": rg("M", "none", "general", u="L"), "note": "v1 'learning styles' is not carried (not an evidence-based design basis)."},
        {"id": "seed:lc-ee-deliver", "wf": "WF-OPERATE", "field": "on-site-preferred", "formation": "partial", "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Deliver an environmental education lesson or field programme to its plan, managing group safety at outdoor sites",
         "regime": rg("M", "seasonal", "site-specific", u="M")},
        {"id": "seed:lc-ee-evaluate-outcomes", "wf": "WF-LEARN", "field": "remote", "formation": "partial",
         "text": "Evaluate a programme's learning outcomes with a pre-post or comparison design, reporting effects and their limits",
         "regime": rg("M", "seasonal", "general", u="L")},
        {"id": "seed:lc-ee-verify-generated", "wf": "WF-PLAN", "field": "remote", "formation": "yes",
         "text": "Verify AI-generated lesson content or simulations against verified science and the learning objectives, correcting errors before use with learners",
         "regime": rg("M", "none", "general", u="M"), "contrib": ["seed:DC-CAND-13"],
         "note": "G-2 split: verifying generated content alongside the lesson-design tasks."},
        {"id": "seed:lc-ee-partnership", "wf": "WF-MANAGE", "field": "remote-capable", "formation": "partial", "modes": ["MODE-ENGAGE"], "rel": ["stakeholder"],
         "text": "Negotiate an education partnership with a school or youth organization that sets roles, schedule, safety duties and shared outcome data",
         "regime": rg("M", "none", "site-specific", u="L"), "contrib": ["seed:v1-5.2.5"]},
        {"id": "seed:lc-ee-train-educators", "wf": "WF-LEARN", "field": "on-site-preferred", "formation": "partial",
         "text": "Train partner educators to deliver a curriculum to fidelity, observing their delivery and recording each adaptation",
         "regime": rg("M", "seasonal", "general", u="L")},
    ],
}

BEHAV = {
    "id": "seed:v1-5.6.4", "roles": LC, "row": "22",
    "label": "Design and evaluate behaviour-change programmes for environmental outcomes",
    "alt": ["Social marketing for sustainability", "Community-based social marketing", "Environmental behaviour change",
            "Environmental psychology and behaviour-change theory"],
    "definition": (
        "Designing, piloting and evaluating programmes that change specific behaviours with environmental consequences "
        "(water and energy use, waste sorting, wildlife feeding, spread of invasive species, fire-safe practices): "
        "selecting target behaviours, researching barriers and motivators with the audience, choosing behaviour-change "
        "tools grounded in theory, piloting with a comparison, and measuring behaviour rather than awareness. "
        "Behaviour-change theory is held as this competency's knowledge statements (from v1 5.6.1). Excludes general social "
        "science research (v1 5.6.2), public information (v1 5.1.1) and environmental education (v1 5.4.1)."),
    "statement": (
        "Selects target behaviours with environmental consequences, researches the audience's barriers and motivators, "
        "designs interventions with behaviour-change tools grounded in theory, pilots them with a comparison group, and "
        "measures behaviour rather than awareness before scaling, revising or stopping the programme."),
    "reusability": "cross-subsector",
    "learningDesign": {"assessmentContext": {"en": "Assess through audience research, intervention designs, pilot and evaluation records; knowledge statements by knowledge test."},
                       "recommendedModes": ["CL", "WS", "CAP"]},
    "derived": [d("v1:5.6.1", "merged-from")],
    "adr": ["ADR-0030", "ADR-0003", "ADR-0004", "ADR-0011"],
    "note": (
        "S2 close-out B (A8 LC; ADR-0030 §3.1 M1). Rewritten in place as the survivor for designing and evaluating "
        "behaviour-change programmes; absorbs v1 5.6.1 (environmental psychology and behaviour-change theory), which "
        "underpins this one practice and becomes its knowledge statements (ADR-0003 knowledge-area test). v1 5.6.1-T2 "
        "(formative research) duplicated 5.6.4-T1 and is superseded into it; 5.6.1-T1 and T3 are rewritten here. The "
        "'4 Ps' marketing frame is not carried as a task. No P1 role needs it (S3). Basis [J]."),
    "knowledge": [
        {"id": "seed:lc-ks-bc-theories", "lowest": "L1", "derived": [d("v1:5.6.1:intermediate:I1")],
         "text": "Behaviour-change theories, such as planned behaviour, social cognitive and habit or norm-based models, treat intention, ability and context as separate influences on environmental behaviour."},
        {"id": "seed:lc-ks-bc-awareness-gap", "lowest": "L1", "derived": [d("v1:5.6.1:foundational:I3")],
         "text": "Awareness and knowledge gains rarely change behaviour on their own; structural barriers such as cost, convenience and access often dominate."},
        {"id": "seed:lc-ks-bc-tools", "lowest": "L2", "derived": [d("v1:5.6.1:intermediate:I4")],
         "text": "Behaviour-change tools include commitments, prompts, social norms, feedback, incentives and changes to the choice environment, each with known conditions under which it works."},
        {"id": "seed:lc-ks-bc-measurement", "lowest": "L2", "derived": [d("v1:5.6.1:advanced:I3")],
         "text": "Evaluating behaviour change needs direct or validated behaviour measures, a baseline and a comparison, because self-reported intentions overstate change."},
        {"id": "seed:lc-ks-bc-ethics", "lowest": "L2",
         "text": "Social pressure and defaults raise questions of consent and fairness, and the costs of some interventions fall hardest on lower-income households."},
    ],
    "levels": {
        "L1": [
            {"id": "seed:lc-bc-l1-a", "mode": "unaided", "methods": [WS, RA],
             "text": "Conducts audience interviews or surveys on a target behaviour to the research guide, recording each barrier and motivator that respondents name.",
             "served": ["seed:v1-5.6.4-T1"], "derived": [d("v1:5.6.4:foundational:I1"), d("v1:5.6.1:foundational:I1")]},
            {"id": "seed:lc-bc-l1-b", "mode": "unaided", "methods": [RA, T],
             "text": "Implements a programme's intervention activities to the delivery plan, recording delivery counts and any deviation from the plan.",
             "served": ["seed:v1-5.6.4-T2"], "derived": [d("v1:5.6.4:foundational:I3")]},
        ],
        "L2": [
            {"id": "seed:lc-bc-l2-a", "mode": "unaided", "methods": [WS, RA], "att": "ATT-AUT",
             "text": "Selects a target behaviour for a programme by its environmental impact, probability of change and current adoption, documenting the evidence for each.",
             "served": ["seed:lc-bc-select-behaviour"], "derived": [d("v1:5.6.1:foundational:I2")]},
            {"id": "seed:lc-bc-l2-b", "mode": "unaided", "methods": [WS, PR], "att": "ATT-KNO",
             "text": "Designs an intervention that matches a behaviour-change tool to each barrier found in audience research, stating the theory behind each choice.",
             "served": ["seed:v1-5.6.4-T2", "seed:v1-5.6.1-T1"], "derived": [d("v1:5.6.1:intermediate:I3"), d("v1:5.6.4:intermediate:I3")]},
            {"id": "seed:lc-bc-l2-c", "mode": "unaided", "methods": [WS, RA], "att": "ATT-CPX",
             "text": "Pilots an intervention with a comparison group, measuring the target behaviour directly rather than through stated intentions.",
             "served": ["seed:v1-5.6.4-T3"], "derived": [d("v1:5.6.4:intermediate:I6")]},
        ],
        "L3": [
            {"id": "seed:lc-bc-l3-a", "mode": "unaided", "methods": [WS, RA], "att": "ATT-CPX",
             "text": "Evaluates a behaviour-change programme's effect on the target behaviour against a baseline and comparison group, reporting the effect size and its limits.",
             "served": ["seed:lc-bc-evaluate"], "derived": [d("v1:5.6.1:advanced:I3")]},
            {"id": "seed:lc-bc-l3-b", "mode": "unaided", "methods": [WS, PR], "att": "ATT-SCO",
             "text": "Designs a programme that combines communication with changes to infrastructure, incentives or defaults where audience research shows structural barriers dominate.",
             "served": ["seed:v1-5.6.1-T3"], "derived": [d("v1:5.6.1:advanced:I2"), d("v1:5.6.1:advanced:I4")]},
            {"id": "seed:lc-bc-l3-c", "mode": "assisted", "methods": [SEW, RA], "att": "ATT-AUG",
             "text": "Checks AI-generated audience segments or message variants against the audience research data, rejecting each segment or claim the data do not support.",
             "served": ["seed:lc-bc-review-ai-segments"]},
        ],
        "L4": [
            {"id": "seed:lc-bc-l4-a", "mode": "unaided", "methods": [PR, WS], "att": "ATT-SCO",
             "text": "Sets an organization's behaviour-change approach, including target-behaviour selection rules, evaluation standards and ethical limits on persuasive tools.",
             "served": ["seed:lc-bc-decide-scale"]},
            {"id": "seed:lc-bc-l4-b", "mode": "unaided", "methods": [WS, RA], "att": "ATT-CPX",
             "text": "Decides whether to scale, revise or stop a behaviour-change programme from its evaluation evidence, recording the effect, the cost per behaviour changed and the decision.",
             "served": ["seed:lc-bc-decide-scale"]},
        ],
    },
    "tasks": [
        {"id": "seed:v1-5.6.4-T1", "wf": "WF-ASSESS", "field": "remote-capable", "formation": "yes", "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Conduct audience research on a target behaviour, recording barriers, motivators and preferred channels for each audience segment",
         "regime": rg("M", "none", "general", u="M")},
        {"id": "seed:v1-5.6.4-T2", "wf": "WF-PLAN", "field": "remote", "formation": "partial",
         "text": "Design a behaviour-change intervention that matches a tool such as prompts, commitments, norms or incentives to each identified barrier",
         "regime": rg("M", "none", "general", u="L"), "note": "The v1 '4 Ps' marketing frame is not carried; tools are matched to researched barriers."},
        {"id": "seed:v1-5.6.4-T3", "wf": "WF-LEARN", "field": "remote-capable", "formation": "yes",
         "text": "Pilot an intervention with a comparison group, measuring the target behaviour before the programme is scaled or revised",
         "regime": rg("M", "seasonal", "general", u="M")},
        {"id": "seed:v1-5.6.1-T1", "wf": "WF-PLAN", "field": "remote", "formation": "partial",
         "text": "Select a behaviour-change theory that fits a programme's target behaviour, stating which influences the intervention will address",
         "regime": rg("L", "none", "general", u="L")},
        {"id": "seed:v1-5.6.1-T3", "wf": "WF-PLAN", "field": "remote", "formation": "partial",
         "text": "Design changes to infrastructure, incentives or defaults where audience research shows structural barriers outweigh motivation",
         "regime": rg("M", "none", "general", u="L")},
        {"id": "seed:lc-bc-select-behaviour", "wf": "WF-PLAN", "field": "remote", "formation": "partial",
         "text": "Select target behaviours by environmental impact, probability of change and current adoption, documenting the evidence for each",
         "regime": rg("M", "none", "general", u="L")},
        {"id": "seed:lc-bc-evaluate", "wf": "WF-LEARN", "field": "remote", "formation": "partial",
         "text": "Evaluate a behaviour-change programme against a baseline and comparison group, reporting the effect size and cost per behaviour changed",
         "regime": rg("M", "seasonal", "general", u="L"), "contrib": ["seed:v1-2.2.2"]},
        {"id": "seed:lc-bc-review-ai-segments", "wf": "WF-PLAN", "field": "remote", "formation": "yes",
         "text": "Review AI-generated audience segments or message variants against the research data, rejecting unsupported segments and claims",
         "regime": rg("M", "none", "general", u="M"), "contrib": ["seed:DC-CAND-13"],
         "note": "G-2 split: reviewing generated segments alongside the audience-research task seed:v1-5.6.4-T1."},
        {"id": "seed:lc-bc-decide-scale", "wf": "WF-MANAGE", "field": "remote", "formation": "partial",
         "text": "Decide whether to scale, revise or stop a behaviour-change programme from its evaluation evidence, recording the basis",
         "regime": rg("M", "multi-year-or-rare-event", "general", u="L")},
    ],
}

for _t in INTERP["tasks"]:
    if _t.get("contrib") is None:
        _t.pop("contrib", None)


def supersede_5_6_1_t2():
    S.supersede_task("seed:v1-5.6.1-T2", "seed:v1-5.6.4-T1", "22", "LC",
                     "S2 close-out B (ADR-0030 §3.1 M1): duplicates 5.6.4-T1 (audience research on barriers and motivators); superseded into it (merged-from lineage kept in provenance).")


SPECS = [INTERP, EE, BEHAV]
PATCHES = [supersede_5_6_1_t2]
