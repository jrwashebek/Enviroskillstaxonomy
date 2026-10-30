// EMST public interface: cross-cutting copy. Owner: content designer (an AI agent on the HCD team).
// Rules and patterns: docs/CONTENT_GUIDE.md. Comprehension test stimuli: docs/COMPREHENSION_TESTS.md.
// Licence: Apache-2.0.
//
// How to use this file
//  - Plain US English, sentence case, grade 8 or lower. Do not edit strings without re-running the checks in
//    CONTENT_GUIDE.md (reading level and claims hygiene).
//  - Templates use {name} tokens. Call fill(template, vars). A token with no value is left as it is, so a missing
//    value shows up in QA instead of disappearing.
//  - About pages are arrays of blocks. Their text may hold tokens (fill them with aboutVars(core), or use
//    fillBlocks(blocks, aboutVars(core))) and inline links written as [link text](href). The about view must
//    render those links as <a>. Every href is either a "#/" route or an https URL with no query string.
//  - Numbers never appear as typed text. Every count comes from app/data through a token.
//  - Lines marked "rc.1 fact" are true of release 2.0.0-rc.1. Re-check them for every release.
//  - The held-records policy (HELD_POLICY) is core.status.held.policy, quoted verbatim. Never paraphrase it.

const ISSUES = "https://github.com/jrwashebek/Enviroskillstaxonomy/issues";
const REPO = "https://github.com/jrwashebek/Enviroskillstaxonomy";
const GOVERNANCE = "https://github.com/jrwashebek/Enviroskillstaxonomy/tree/main/docs/governance";

// Verbatim copy of core.status.held.policy (checked against the data by the CONTENT_GUIDE script).
const HELD_POLICY = "Content under the project's Tribal content hold is excluded from every build until a Tribal Advisory Council approves it. These pages neither show nor describe it; the release notes give only a count of held records.";

/** Replace {name} tokens with values from vars. Unknown tokens stay as they are. */
export function fill(template, vars = {}) {
  return String(template ?? "").replace(/\{(\w+)\}/g, (m, k) =>
    Object.prototype.hasOwnProperty.call(vars, k) && vars[k] !== undefined && vars[k] !== null ? String(vars[k]) : m);
}

/** Fill every string in an array of about-page blocks. Returns new blocks; the originals are not changed. */
export function fillBlocks(blocks, vars = {}) {
  const f = (x) => (typeof x === "string" ? fill(x, vars) : Array.isArray(x) ? x.map(f) : x);
  return (blocks || []).map((b) => Object.fromEntries(Object.entries(b).map(([k, v]) => [k, f(v)])));
}

const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const longDate = (iso) => {
  const [y, m, d] = String(iso || "").split("-").map(Number);
  return y && m && d ? `${d} ${MONTHS[m - 1]} ${y}` : String(iso || "");
};
const num = (n) => (typeof n === "number" ? n.toLocaleString("en-US") : String(n ?? ""));
const GATE_RESULT = { pass: "passed", conditional: "passed with conditions", fail: "not passed" };

/** Token values for the about pages and exports, all taken from core data. */
export function aboutVars(core) {
  const r = core?.release || {};
  const gate = core?.status?.gate || {};
  const vars = {
    release: r.id,
    releaseDate: longDate(r.date),
    year: String(r.date || "").slice(0, 4),
    heldN: num(core?.status?.held?.n),
    gateAsOf: longDate(gate.asOf),
  };
  const failed = [];
  for (const it of gate.items || []) {
    vars[`gate${it.n}`] = GATE_RESULT[it.result] || it.result;
    if (it.result === "fail") failed.push(String(it.n));
  }
  vars.gateFailed = failed.length ? failed.join(" and ") : "none";
  return vars;
}

// ---------------------------------------------------------------- use tiers

const NOT_FOR_PEOPLE = [
  "Screen, score or rank people who apply for a job.",
  "Set a job's series, grade or pay (classification).",
  "Rate how well an employee does their job.",
  "Choose which jobs or people to cut in a reduction in force.",
];

const use = {
  describe: {
    label: "Describe and plan",
    short: "Use for describing work and planning. Not for decisions about people.",
    youCan: [
      "Describe the work of a role in a workforce plan or grant report.",
      "Map a course or training program to the tasks a role does.",
      "Find task wording to start a job or position description. Your HR office must then review and change it.",
    ],
    youCant: NOT_FOR_PEOPLE,
    why: "AI agents drafted these records, and no practitioner has checked them yet. That is enough to describe work in broad terms. It is not enough for decisions about people.",
  },
  exploratory: {
    label: "Explore only",
    short: "Use for exploring ideas only. Not for plans or decisions.",
    youCan: [
      "Explore what a new course might cover, such as a class on prescribed fire.",
      "Talk about how a kind of work may change in the next few years.",
      "Spot new skills to keep an eye on.",
    ],
    youCant: [
      "State it as fact in a workforce plan or report.",
      "Build a training plan or task book from it.",
      "Use it in hiring, or to set a job's grade or pay.",
      "Use it to rate staff or to decide who to lay off.",
    ],
    why: "The evidence behind these records is thin. Some describe work that may only be starting. Others have skill levels that no expert panel has placed yet.",
  },
  develop: {
    label: "Train and develop",
    short: "For training and development plans. No record reaches this use yet.",
    youCan: [
      "Build a training plan or a task book.",
      "Write an individual development plan with a staff member.",
      "Let people check their own skills against the levels.",
    ],
    youCant: NOT_FOR_PEOPLE,
    why: "Training shapes people's careers. It needs content that practitioners have checked, with skill levels that experts agree on.",
    notReached: "No record reaches this use yet. First, practitioners from at least three kinds of employer must review the content. Then an expert panel must agree on the level of each skill statement.",
  },
  select: {
    label: "Job analysis input",
    short: "Only as one input to an employer's own job analysis. No record reaches this use yet.",
    youCan: [
      "Give your experts a first list of tasks to rate in your own job analysis.",
      "Check your experts' task list against EMST's to find gaps.",
      "Reuse task wording in a job posting once your own job analysis confirms it.",
    ],
    youCant: [
      "Screen, score or rank applicants straight from EMST.",
      "Set a job's series, grade or pay (classification).",
      "Rate how well an employee does their job.",
      "Choose which jobs or people to cut in a reduction in force.",
    ],
    why: "Hiring changes people's lives. It needs evidence about the specific job. OPM's memo of 27 August 2026 on AI in hiring says subject-matter experts must check AI-drafted job analysis against the job's real duties.",
    notReached: "No record reaches this use yet. A record would need everything the training use needs. It would also need a job analysis that confirms it for that kind of job, a plan to check for unfair effects on groups of applicants, and full records of how it was tested. Even then, it is only one input to an employer's own job analysis.",
  },
};

// ---------------------------------------------------------------- statuses

const review = {
  unreviewed: { label: "Not yet reviewed by people", plain: "No person has reviewed this record yet." },
  "spot-checked": { label: "Spot-checked", plain: "A person reviewed a sample of records like this one." },
  reviewed: { label: "Reviewed by a person", plain: "A named reviewer read and checked this record." },
  validated: { label: "Passed its use test", plain: "It passed the checks set for its use, such as an expert panel and a study of how well raters agree." },
  gold: { label: "Reference set", plain: "It is part of a small set that two people coded on their own. The set is used to test other coding." },
};

const evidence = {
  E: { label: "Sourced", plain: "Based on a source that was read and is cited." },
  J: { label: "Judgment", plain: "A reasoned judgment with its basis stated. In this release, an AI agent made it, not a person." },
  S: { label: "Speculation", plain: "Plausible but not yet supported. It says what would confirm it or rule it out." },
};

const lifecycle = {
  watch: { label: "On watch", plain: "Something may be starting in this work, but it is not yet shown to exist across the sector. It is dropped if no new evidence comes in by its review date." },
  proposed: { label: "Proposed", plain: "A draft definition exists. Early evidence points to it, such as a new rule or several signals." },
  emerging: { label: "Emerging", plain: "Seen in real work, such as job postings at more than one kind of employer, but not yet long-standing." },
  established: { label: "Established", plain: "Long-standing work in the sector. This says the work is real. It does not say that EMST's description of it has been checked." },
  declining: { label: "Declining", plain: "Demand for this work is falling, or other work is taking its place." },
  withdrawn: { label: "Withdrawn", plain: "No longer current. It is kept for the record and is not for any use." },
  lapsed: { label: "Lapsed", plain: "A watch item that ended because no new evidence came in by its review date." },
  merged: { label: "Merged", plain: "Combined into another record. Links lead to that record." },
};

const pending = {
  title: "Assessment pending",
  body: "{assessed} of {total} {unit} assessed so far. Not shown yet:",
  what: {
    importance: "importance",
    timeShare: "share of work time",
    critical: "whether it is critical",
    neededAtEntry: "whether it is needed on day one",
    craft: "mix of field, data and policy skill",
    exposure: "exposure to AI and automation",
    workFunction: "type of work",
  },
  why: "No group of practitioners has rated these yet. We show nothing rather than a guess, so the order of this list says nothing about importance.",
  next: "These values will appear after a study with practitioners checks them. No study has reported yet.",
};

const match = {
  exactMatch: "Exact fit",
  closeMatch: "Close fit, not the same",
  broadMatch: "Broader {noun}",
  narrowMatch: "More specific {noun}",
  relatedMatch: "Related in part",
  mirrorRole: "Mirror role: similar work on the other side of a permit or inspection",
  not: "Not a match (noted by an AI agent)",
  none: "No matching {noun} found",
  unreviewed: "AI-suggested, not reviewed",
  twoCoders: "Two AI coders agreed",
  disagree: "AI coders disagreed; a person needs to decide",
  note: "AI agents suggested these links to help you find related items. No person has checked them. They do not mean EMST matches O*NET, ESCO, OPM or any state system, and EMST makes no such claim until people review them.",
};

const sourceGrade = {
  A: "Strong source: original data or a peer-reviewed study",
  B: "Good source: a trusted secondary source that names its original data",
  C: "Limited source: one secondary source or one practitioner's report",
  D: "Weak source: an unchecked story or a vendor's claim",
};

const formation = {
  tag: "Formation task",
  explain: "Learned through supervised practice on the job, not from a course alone.",
};

const ladder = {
  title: "Review path",
  steps: [
    { key: "draft", label: "Drafted by AI agents", plain: "AI agents wrote the first version from sources." },
    { key: "ai-checked", label: "Checked by AI agents and scripts", plain: "AI agents checked facts against sources, and automated tests checked the data." },
    { key: "practitioner-reviewed", label: "Reviewed by practitioners", plain: "People who do this work read it and correct it." },
    { key: "reliability-tested", label: "Tested for agreement", plain: "Several trained people rate it on their own, to see if they agree." },
    { key: "validated", label: "Cleared for a stated use", plain: "It passed every check needed for one use, such as training." },
  ],
  state: { done: "Done", current: "Current step", todo: "Not yet" },
  next: "Next step for this record: review by practitioners.",
};

// ---------------------------------------------------------------- about pages

const p = (text) => ({ t: "p", text });
const h2 = (id, text) => ({ t: "h2", id, text });
const ul = (items) => ({ t: "ul", items });
const youCanBlocks = (u) => [p(u.short), p("You can:"), ul(u.youCan), p("You can't:"), ul(u.youCant), p(u.why)];

const read = [
  p("This page explains every label you will see on EMST. Each label on a record links to its section here."),

  h2("use-tiers", "What you can use EMST for"),
  p("Every record says what it may be used for. There are four uses, from lightest to heaviest: explore only, describe and plan, train and develop, and job analysis input."),
  p("In release {release}, every record is either “explore only” or “describe and plan”. No record reaches the training or job analysis uses yet."), // rc.1 fact
  { t: "notice", kind: "caution", title: "Never for decisions about people", text: "EMST describes work. It is not a job analysis, a basis for classification, a crediting plan or an assessment. Do not use it to hire, to set pay or grade, to rate performance, to discipline staff or to choose who to lay off." },

  h2("use-describe", "Describe and plan"),
  ...youCanBlocks(use.describe),

  h2("use-exploratory", "Explore only"),
  ...youCanBlocks(use.exploratory),

  h2("use-develop", "Train and develop"),
  { t: "notice", kind: "info", title: "Not reached in this release", text: use.develop.notReached },
  p("When a record reaches this use, you could:"),
  ul(use.develop.youCan),
  p("Even then, you can't:"),
  ul(use.develop.youCant),
  p(use.develop.why),

  h2("use-select", "Job analysis input"),
  { t: "notice", kind: "info", title: "Not reached in this release", text: use.select.notReached },
  p("When a record reaches this use, you could:"),
  ul(use.select.youCan),
  p("Even then, you can't:"),
  ul(use.select.youCant),
  p(use.select.why),

  h2("ai-drafted", "Drafted by AI agents"),
  { t: "example", label: "On a record", text: "Drafted by AI agents. Not yet reviewed by people." },
  p("AI agents wrote the record. The EMST project lead set the rules the agents follow. No person has checked this record yet."),
  ul([
    "What AI agents did: found sources, drafted the record and checked facts against the sources.",
    "What people did: the EMST project lead wrote the charter, the rules the agents work to.",
    "Not done yet: review by people who do the work, a study of how well raters agree, and a job analysis.",
  ]),
  p("AI-drafted does not mean wrong. It means not yet checked by people. Use each record only as its use label says, and tell us when you find an error."),
  p("Some text says “Wording carried over from EMST version 1”. One analyst wrote it with an AI assistant, and it has not been rewritten yet."),
  p("Names such as “Chief Taxonomy Architect” are AI agent roles, not people. See [How it was made](#/about/made) for the full review path."),

  h2("review", "Review status"),
  { t: "dl", items: Object.values(review).map((r) => [r.label, r.plain]) },
  p("In release {release}, every record is “Not yet reviewed by people”."), // rc.1 fact

  h2("evidence", "Evidence labels: E, J and S"),
  p("Each record carries one letter that says what it rests on."),
  { t: "dl", items: Object.entries(evidence).map(([k, e]) => [`${k}: ${e.label}`, e.plain]) },

  h2("pending", "Assessment pending"),
  p("Some values need people to rate them before we can show them. Until a study checks them, EMST shows “Assessment pending” instead of a number. Pending never means zero or unimportant."),
  p("These values are pending:"),
  ul(Object.values(pending.what).map((w) => w[0].toUpperCase() + w.slice(1))),
  { t: "example", label: "On a role page", text: "Assessment pending. None of this role's tasks has been assessed yet. The order of the list says nothing about importance." },
  p(pending.next),
  p("Some tasks also have codes from EMST version 1, made by one analyst with an AI assistant. They sit in a closed drawer marked “not for decisions”. They are never counted, averaged or put in charts."),

  h2("lifecycle", "How established the work is"),
  p("This label is about the work in the world, not about EMST's description of it."),
  { t: "dl", items: Object.values(lifecycle).map((l) => [l.label, l.plain]) },

  h2("matches", "Links to other systems"),
  p("Some records link to O*NET, ESCO, OPM job series or state job classes. Each link has a match type."),
  { t: "dl", items: [
    ["Close fit, not the same", "Much of the meaning is shared, but not all of it."],
    ["Broader", "The other item covers more than the EMST item."],
    ["More specific", "The other item covers less than the EMST item."],
    ["Related in part", "The two items overlap only in part."],
    ["Mirror role", "Similar work, seen from the other side of a permit or an inspection. For example, a state inspector and the person at a plant who deals with the inspector."],
    ["Not a match", "An AI agent noted that these items are different, to avoid confusion."],
    ["No match found", "The AI agents looked and found nothing that fits."],
  ] },
  p("Every link is “AI-suggested, not reviewed”. Some links also say whether two AI coders agreed, or disagreed and need a person to decide."),
  { t: "notice", kind: "info", title: "Not a claim that EMST matches these systems", text: match.note },
  p("We show no confidence numbers on screen. The AI agents' own numbers are not calibrated, so they would look more exact than they are. The data files keep them."),

  h2("source-grades", "Source grades (A to D)"),
  p("Signals about change carry a grade for their source. The grade rates the source, not the claim, and it is not a statistic. The AI agent that entered the signal set the grade. No one has graded it again from the original source yet."),
  { t: "dl", items: Object.entries(sourceGrade).map(([k, v]) => [k, v]) },

  h2("formation", "Formation tasks"),
  p("A formation task is learned through supervised practice on the job, not from a course alone. New staff build it by doing it many times with feedback. AI agents drafted this label too."),

  h2("held", "Held records"),
  p(HELD_POLICY),
  p("Held records in release {release}: {heldN}"),

  h2("not-gov", "Not a government website"),
  p("EMST is an independent, open project. It is not a government website. No government agency runs it or has endorsed it."),
  p("Pages about OPM job series and state job classes show how EMST's draft roles might relate to them. Those pages do not come from OPM or any state, and EMST is not affiliated with either."),
];

const made = [
  p("This page says who made EMST, how, and what has not happened yet."),

  h2("made-what", "What EMST is"),
  p("EMST stands for Environmental Management Skills Taxonomy. It describes environmental work. It lists the tasks people do and the skills behind them, which EMST calls competencies. It also shows how a role differs from one employer to another, such as a federal agency, a state, a nonprofit or a firm."),

  h2("made-who", "Who made it"),
  p("AI agents (Anthropic's Claude) researched and drafted every record and page. Each agent had a specialist role. They all worked to a charter, a set of rules, written by the EMST project lead."),
  p("Names such as “Chief Taxonomy Architect” or “EMST's federal HR agent” are AI agent roles, not people."),

  h2("made-checks", "Checks that ran"),
  ul([
    "Automated tests check every build. They test the data's structure and the links between records. They also look for personal data, held content and claims we must not make.",
    "AI agents checked facts against their sources in October 2026.",
    "A display rule hides every rating that has not passed a reliability study. You see “Assessment pending” instead.",
    "A claims list stops the site from repeating facts that could not be confirmed.",
  ]),

  h2("made-not-yet", "What has not happened yet"),
  ul([
    "No one who does this work has reviewed any record.",
    "No reliability study has tested any rating.",
    "No job analysis has been done for any role.",
    "No person has reviewed the links to O*NET, ESCO, OPM series or state job classes.",
    "No person has signed off the release.",
  ]), // rc.1 facts

  h2("made-path", "The review path"),
  p("Each record moves up these steps. In release {release}, every record is on the second step."), // rc.1 fact
  ul(ladder.steps.map((s) => `${s.label}: ${s.plain}`)),
  p("Dates will appear here only once they are set."),

  h2("made-help", "How you can help"),
  p("If you do this work, your corrections matter most. See [Corrections and contributing](#/about/corrections)."),
];

const status = [
  p("Before anyone outside the project may rely on a release, it must pass eight checks. This page shows how release {release} did, as of {gateAsOf}. Scripts and AI agents ran the checks. No person has signed them."),
  { t: "notice", kind: "caution", title: "Not cleared for publication", text: "Release {release} is a test version for a pilot preview. It is not cleared for publication outside the project. Checks not passed: {gateFailed}." },

  h2("status-checks", "The eight checks"),
  { t: "dl", items: [
    ["1. Automated tests: {gate1}", "The automated tests ran when the release was built."],
    ["2. Size of the core list: {gate2}", "The core list of competencies stays within its planned size."],
    ["3. Use limits: {gate3}", "Every record states its use. None is cleared for hiring. No rating is shown unless raters were shown to agree."],
    ["4. Scope: {gate4}", "The first group of work areas is in. Later groups are left out, apart from a few named early drafts."],
    ["5. Roles: {gate5}", "All planned roles are drafted. Some federal series and state class views are missing, because no person has checked the links they would be built from."],
    ["6. Links to other systems: {gate6}", "No person has reviewed a sample of the links to O*NET, OPM series, ESCO or state classes. For O*NET tasks, the two AI coders also agreed too little."],
    ["7. Human sign-off: {gate7}", "No named subject-matter expert has reviewed the release, and the EMST project lead has not signed it."],
    ["8. Early decisions: {gate8}", "The project lead's first decisions are on record."],
  ] },
  p("Read the full report: [Release gate report on GitHub](https://github.com/jrwashebek/Enviroskillstaxonomy/blob/main/docs/release/{release}/GATE_REPORT.md)."),
];

const data = [
  p("EMST is open data. You may copy, change and share it for any purpose, without asking."),

  h2("data-get", "Get the data"),
  p(`The release files are built from the project's GitHub repository. They are not yet posted as a download. Until they are, you can build them yourself by following the README in [EMST on GitHub](${REPO}).`),
  p("To take one role's tasks with you, use “Copy tasks as text” or “Download CSV” on the role page."),

  h2("data-files", "What a release contains"),
  { t: "dl", items: [
    ["Spreadsheet files (CSV)", "Tables of roles, tasks, competencies and other records. They open in any spreadsheet program."],
    ["Full data set (JSON-LD)", "Every record and link in one file, for developers."],
    ["Vocabulary file (SKOS)", "The terms and how they relate, for data and library systems."],
    ["Link files", "Every link the AI agents suggested to O*NET, ESCO, OPM series or state classes. Each one comes with the agent's notes and review status."],
    ["Release notes", "What changed, what is held back, and known issues."],
  ] },

  h2("data-cite", "How to cite"),
  { t: "example", label: "Citation", text: `EMST project lead ({year}). Environmental Management Skills Taxonomy, draft release {release}. Drafted by AI agents; not yet reviewed by people. ${REPO}` },
  p("Each record also has “Copy citation”, which adds the record's ID."),

  h2("data-ids", "Record IDs"),
  p("Each record has an ID, such as emst:core/ROL-ZJFCC09. IDs are candidates until version 2.0.0, so they may still change. Always cite the release with the ID."),

  h2("data-caveats", "Keep the caveats with the data"),
  p("If you reuse or share EMST, keep “Drafted by AI agents. Not yet reviewed by people.” with it, and keep each record's use label. Leave “Assessment pending” as it is. Never turn it into a zero or a blank."),

  h2("data-license", "License"),
  ul([
    "Data and standard text: CC0 1.0. This puts them in the public domain.",
    "Code: Apache 2.0.",
    "Reports and other publications: CC BY 4.0.",
  ]),
];

const corrections = [
  p("If you do this work, you can make EMST better. Tell us when a task, a level or a link is wrong, or when work is missing."),

  h2("corr-how", "How to report a problem"),
  ul([
    "Copy the record reference. It names the record and the release.",
    "Open GitHub Issues. You need a free GitHub account, and what you post is public.",
    "Start a new issue. Paste the reference, then say what is wrong and what it should say.",
    "Do not include names, email addresses or anything about a staff member.",
    "Watch the issue on GitHub for replies.",
  ]),
  p(`[Open GitHub Issues](${ISSUES})`),
  { t: "notice", kind: "info", title: "Before you post", text: "GitHub needs a free account, and issues are public. If you work for an agency, check its rules on posting in public first." },

  h2("corr-next", "What happens next"),
  p("For now, the EMST project lead decides on changes. The project's draft contributing guide sets time limits for sorting each issue, and asks for reasons when a change is turned down. Accepted changes go into a later release."),

  h2("corr-no-account", "No GitHub account?"),
  p("A way to send corrections without a GitHub account is under consideration. For now, GitHub is the only route."),

  h2("corr-misuse", "Report misuse"),
  p("If you see EMST used to screen, rank, rate or lay off people, please tell us on GitHub Issues. Leave out the names of people."),

  h2("corr-missing", "Suggest a role or task we're missing"),
  p("Open an issue and describe the work in your own words: the job title, the main tasks and the kind of employer. If you came here from a search, your search words are shown on this page so you can copy them."),
  p("Read the full guide: [Contributing to EMST](https://github.com/jrwashebek/Enviroskillstaxonomy/blob/main/docs/governance/CONTRIBUTING.md)."),
];

const held = [
  p(HELD_POLICY),
  p("Held records in release {release}: {heldN}"),
  p(`[Governance documents on GitHub](${GOVERNANCE})`),
];

const accessibility = [
  p("We want everyone to be able to use EMST. That includes people who use a screen reader, a keyboard alone, zoom or high-contrast colors."),

  h2("a11y-target", "Our target"),
  p("The target is WCAG 2.2 at level AA. This prototype has not had a full audit, so we do not claim that it meets the target."),

  h2("a11y-design", "What the prototype is designed to do"),
  ul([
    "Work with a keyboard alone.",
    "Fit small screens, down to 320 pixels wide, without sideways scrolling.",
    "Never rely on color alone. Every status is written in words.",
    "Show nothing only on hover.",
    "Give every chart a table with the same numbers.",
    "Announce each new page and move focus to its main heading.",
    "Spell out abbreviations where they first appear on a page.",
  ]),

  h2("a11y-limits", "Known limits"),
  ul([
    "No one who uses assistive technology has tested this prototype yet.",
    "Automated checks find only some problems.",
    "Much of the record text uses long sentences and technical words. Plainer wording for records has not been written yet.",
  ]),

  h2("a11y-report", "Report a barrier"),
  p(`Tell us on [GitHub Issues](${ISSUES}). You need a free account. A way to report without an account is under consideration.`),
];

const privacy = [
  p("EMST does not collect anything about you."),
  ul([
    "No cookies, no tracking and no analytics.",
    "No accounts and no sign-in.",
    "Nothing is saved in your browser.",
    "What you type in search stays on your device. It is never added to the page address, so search results cannot be shared as a link.",
    "Files you save, such as a CSV file, go only to your device.",
    "The site loads nothing from other websites.",
  ]),
  p("Links to GitHub, O*NET and state job class documents take you to other sites. Those sites have their own privacy rules."),
  p("The company that hosts these pages may keep basic server logs, such as the address a request came from. EMST adds nothing that tracks you."),
];

// ---------------------------------------------------------------- COPY

export const COPY = {
  site: {
    name: "EMST",
    full: "Environmental Management Skills Taxonomy",
    tagline: "Shared words for environmental work",
    lede: "EMST describes environmental jobs: the tasks people do, the skills behind them, and how the work differs from one employer to another. It is a free, open draft.",
    ribbon: {
      release: "Draft release {id}",
      ai: "Drafted by AI agents, not yet reviewed by people",
      link: "What this means",
    },
    notGov: "An independent open project. Not a government website.",
    footer: {
      authorship: "AI agents researched and drafted these pages and records, working to rules set by the EMST project lead. No person has reviewed them yet.",
      licence: "Data: CC0 1.0, free to reuse. Code: Apache 2.0.",
      issues: "Report a problem on GitHub (free account needed)",
    },
  },

  use,

  ai: {
    line: "Drafted by AI agents. Not yet reviewed by people.",
    lineDated: "Drafted by AI agents on {date}. Not yet reviewed by people.",
    v1: "Wording carried over from EMST version 1, where one analyst wrote it with an AI assistant. Not yet rewritten or reviewed by people.",
    detail: "AI agents drafted this record, following rules set by the EMST project lead, and automated tests checked its format and links. Any sources it cites are listed below; many records cite none. No one who does this work has reviewed it, and no study has tested it. Next on the review path: review by practitioners.",
  },

  review,
  evidence,
  lifecycle,
  pending,
  match,
  sourceGrade,
  formation,
  ladder,

  zero: {
    title: "No results for “{q}”",
    body: "EMST may not cover this work yet, or it may use other words for it. Try a shorter word, a job title, or a series code such as 0460.",
    tryTitle: "Try these instead",
    browseTitle: "Or browse",
    suggest: "Suggest a role or task we're missing",
  },

  empty: {
    filters: { title: "No roles match these filters", body: "Remove a filter, or search for a task instead.", action: "Clear filters" },
  },

  compare: {
    caveat: "Sharing competencies doesn't mean you qualify. Each employer decides what its jobs need.",
    summary: "{a} and {b} share {shared} of the {total} competencies that {b} needs. Tasks in common: {tasks}.",
    onlyA: "Only in {a}",
    onlyB: "Only in {b}",
    shared: "In both roles",
    check: "What to check with the employer",
    noEdge: "EMST has not worked out a path between these two roles. That says nothing about whether the move is possible.",
  },

  actions: {
    cite: "Copy citation",
    citeDone: "Citation copied",
    correct: "Suggest a correction",
    correctSteps: [
      "Copy the record reference. It names the record and the release.",
      "Open GitHub Issues. You need a free GitHub account, and what you post is public.",
      "Start a new issue. Paste the reference, then say what is wrong and what it should say.",
      "Do not include names, email addresses or anything about a staff member.",
      "Watch the issue on GitHub for replies.",
    ],
    noAccount: "No GitHub account? A way to send corrections without one is under consideration. For now, GitHub is the only route.",
    print: "Print",
    copyTasks: "Copy tasks as text",
    csv: "Download CSV",
    exportHeader: "{title}\nFrom EMST, the Environmental Management Skills Taxonomy, draft release {release}.\nTaken from {url} on {date}.\nDrafted by AI agents. Not yet reviewed by people.\nDescribes work only. It is not a job analysis, a basis for classification, a crediting plan or an assessment. Do not use it for hiring, pay, performance ratings or reductions in force.",
    exportFooter: `Data: CC0 1.0, free to reuse. Credit: EMST project lead.\nReport a problem: ${ISSUES} (free GitHub account needed).\nThis copy may be out of date. Check the source page for the latest release.`,
  },

  errors: {
    notFound: { title: "Page not found", body: "This address does not match a page in this release. Record IDs can change until version 2.0.0, so try searching for the record instead." },
    load: { title: "This page did not load", body: "Some of the data did not load. Reload the page. If it still fails, tell us on GitHub Issues." },
    copy: "Copy did not work. Select the text and copy it yourself.",
    noScript: "This site needs JavaScript to show records. You can still read the data in the project's GitHub repository.",
  },

  about: { read, made, status, data, corrections, held, accessibility, privacy },

  held: { heading: "Held records" },
};

// ---------------------------------------------------------------- GLOSSARY
// Terms that appear in app/data, with counts in CONTENT_GUIDE.md. `exp` is empty for terms that are not
// abbreviations: jargon() should then link or show the definition without making an <abbr>.
// Matching: all-capital keys match case-sensitively; other keys match case-insensitively. A plural "s" should
// also match (IDPs, ECQs). Prefer the longest key (O*NET-SOC before O*NET or SOC).

export const GLOSSARY = {
  // Agencies and offices
  "BLS": { exp: "Bureau of Labor Statistics", def: "The federal agency that publishes US data on jobs, pay and future job growth." },
  "CEQ": { exp: "Council on Environmental Quality", def: "A White House office that gives the President advice on environmental policy." },
  "DOI": { exp: "US Department of the Interior", def: "The federal department whose agencies manage national parks, wildlife refuges and other public lands." },
  "DOJ": { exp: "US Department of Justice", def: "The federal department that enforces federal law and gives legal advice to agencies." },
  "DOL": { exp: "US Department of Labor", def: "The federal department for workers, job training and job data; it sponsors O*NET." },
  "EPA": { exp: "Environmental Protection Agency", def: "The federal agency that sets and enforces national rules on pollution." },
  "FAA": { exp: "Federal Aviation Administration", def: "The federal agency that oversees flying in the US, including drones." },
  "NIFC": { exp: "National Interagency Fire Center", def: "The center in Boise, Idaho, where US agencies coordinate support for wildland fires." },
  "NRCS": { exp: "Natural Resources Conservation Service", def: "A USDA agency that helps farmers and other private landowners protect soil, water and habitat." },
  "NWCG": { exp: "National Wildfire Coordinating Group", def: "A group of US fire agencies that sets shared standards for wildland fire training and jobs." },
  "OIRA": { exp: "Office of Information and Regulatory Affairs", def: "The part of OMB that reviews major draft federal rules before they are issued." },
  "OMB": { exp: "Office of Management and Budget", def: "The White House office that prepares the federal budget and oversees how agencies work." },
  "OPM": { exp: "Office of Personnel Management", def: "The federal agency that sets HR rules for federal jobs, such as job series and qualification standards." },
  "OSHA": { exp: "Occupational Safety and Health Administration", def: "The federal agency that sets and enforces workplace safety rules." },
  "USDA": { exp: "US Department of Agriculture", def: "The federal department that includes the Forest Service and the Natural Resources Conservation Service." },
  "USFS": { exp: "US Forest Service", def: "The USDA agency that manages national forests and grasslands." },

  // Laws, rules and documents
  "ADA": { exp: "Americans with Disabilities Act", def: "A US civil rights law for people with disabilities; its Title II covers state and local government services, including websites." },
  "CAA": { exp: "Clean Air Act", def: "The main US law for controlling air pollution." },
  "CEQA": { exp: "California Environmental Quality Act", def: "California's law that makes state and local agencies study a project's effects on the environment before they decide on it." },
  "CFR": { exp: "Code of Federal Regulations", def: "The collection of current federal rules, arranged by subject." },
  "CWA": { exp: "Clean Water Act", def: "The main US law for controlling pollution in rivers, lakes, wetlands and coastal waters." },
  "EA": { exp: "environmental assessment", def: "A shorter NEPA document that helps an agency decide whether it needs a full environmental impact statement." },
  "EIS": { exp: "environmental impact statement", def: "The most detailed NEPA document, written when a federal action may have major effects on the environment." },
  "EO": { exp: "executive order", def: "A written order from the President that directs federal agencies." },
  "ESA": { exp: "Endangered Species Act", def: "The US law that protects plants and animals at risk of dying out, and the places they live." },
  "FR": { exp: "Federal Register", def: "The daily federal publication of new rules, proposed rules and notices." },
  "NEPA": { exp: "National Environmental Policy Act", def: "The US law that makes federal agencies look at the effects of a proposed action on the environment before they decide." },
  "NHPA": { exp: "National Historic Preservation Act", def: "The US law that protects historic places; its Section 106 sets out a review for federal projects." },
  "RCRA": { exp: "Resource Conservation and Recovery Act", def: "The US law on handling solid and hazardous waste from the time it is made until it is disposed of." },
  "TEGL": { exp: "Training and Employment Guidance Letter", def: "A guidance letter from the Department of Labor to the states and others who run job training programs." },
  "WIOA": { exp: "Workforce Innovation and Opportunity Act", def: "The federal law that funds job training and local workforce boards." },
  "Title V": { exp: "", def: "The part of the Clean Air Act that requires operating permits for large sources of air pollution." },
  "Section 106": { exp: "", def: "The part of the National Historic Preservation Act that makes federal agencies consider effects on historic places before they act." },
  "Section 7": { exp: "", def: "The part of the Endangered Species Act under which federal agencies consult wildlife agencies so that their actions do not put listed species at risk." },
  "Section 404": { exp: "", def: "The part of the Clean Water Act that requires a permit to put dredged or fill material into waters, including many wetlands." },

  // Permits and programs
  "NPDES": { exp: "National Pollutant Discharge Elimination System", def: "The Clean Water Act permit program for releasing pollutants into US waters." },
  "NSR": { exp: "New Source Review", def: "Clean Air Act permits needed to build or change a large source of air pollution." },
  "PSD": { exp: "Prevention of Significant Deterioration", def: "Clean Air Act permits that keep the air from getting worse in places where it is already clean enough." },
  "MS4": { exp: "municipal separate storm sewer system", def: "A public system of drains and pipes that carries stormwater and needs a Clean Water Act permit." },
  "TMDL": { exp: "total maximum daily load", def: "The most of a pollutant a water body can take and still meet water quality standards, and the plan to get there." },
  "NFIP": { exp: "National Flood Insurance Program", def: "The federal program that offers flood insurance where communities adopt floodplain rules." },

  // HR and workforce
  "SME": { exp: "subject-matter expert", def: "A person with deep, hands-on knowledge of the work being described." },
  "RIF": { exp: "reduction in force", def: "The formal process an employer uses to cut jobs and lay off staff." },
  "GS": { exp: "General Schedule", def: "The main federal pay system for office and professional jobs, with grades from GS-1 to GS-15." },
  "WG": { exp: "Wage Grade", def: "The federal pay system for trades, crafts and labor jobs." },
  "SES": { exp: "Senior Executive Service", def: "The group of top federal career managers just below political appointees." },
  "ECQ": { exp: "Executive Core Qualifications", def: "OPM's list of leadership skills needed to join the Senior Executive Service." },
  "FWCI": { exp: "Federal Workforce Competency Initiative", def: "OPM's project to build competency models for federal jobs." },
  "IDP": { exp: "individual development plan", def: "A written plan that an employee and a supervisor agree on to build skills." },
  "PD": { exp: "position description", def: "The document that lists a job's duties and requirements; in federal jobs it is the basis for setting series and grade." },
  "O*NET": { exp: "Occupational Information Network", def: "The US Department of Labor's free database of the tasks, skills and tools of hundreds of occupations." },
  "O*NET-SOC": { exp: "O*NET Standard Occupational Classification codes", def: "The job codes O*NET uses, based on the federal SOC codes." },
  "SOC": { exp: "Standard Occupational Classification", def: "The federal system that sorts jobs into occupations for statistics, each with a number code." },
  "ESCO": { exp: "European Skills, Competences, Qualifications and Occupations", def: "The European Union's list of skills and occupations, in many languages." },
  "job analysis": { exp: "", def: "A study an employer does, with subject-matter experts, to record a job's tasks and the knowledge and skills it needs." },
  "crediting plan": { exp: "", def: "A guide HR uses to judge whether an applicant's experience meets a job's requirements." },
  "qualification standard": { exp: "", def: "OPM's statement of the least education and experience that federal jobs in a series need." },
  "classification standard": { exp: "", def: "OPM's guide for deciding a federal job's series, title and grade." },
  "class specification": { exp: "", def: "A state or local government's description of a job class, with its duties, minimum qualifications and pay range." },
  "OPM series": { exp: "", def: "A four-digit code OPM uses to group federal jobs by type of work, such as 0460 for forestry." },
  "specialized experience": { exp: "", def: "Experience that gave an applicant the specific skills a federal job needs, as the job announcement describes them." },
  "positive education requirement": { exp: "", def: "A rule that federal jobs in some series need certain degrees or courses, not just experience." },
  "adverse action": { exp: "", def: "A formal action against an employee, such as a suspension, a demotion or a removal." },
  "task book": { exp: "", def: "A record of tasks a trainee must do while an evaluator watches, used to earn a qualification, as in wildland fire." },
  "conservation corps": { exp: "", def: "A program that pays people, often young adults, to do conservation work on crews while they train." },

  // Credentials
  "CFM": { exp: "Certified Floodplain Manager", def: "A credential for people who manage floodplains and flood risk." },
  "CHMM": { exp: "Certified Hazardous Materials Manager", def: "A credential for people who manage hazardous materials." },
  "PE": { exp: "Professional Engineer", def: "A state license that lets an engineer sign and seal engineering work." },
  "REHS": { exp: "Registered Environmental Health Specialist", def: "A credential for environmental health inspectors, also called RS (Registered Sanitarian)." },
  "QEP": { exp: "Qualified Environmental Professional", def: "A credential for people who work in environmental fields." },

  // Field and technical
  "AI": { exp: "artificial intelligence", def: "Computer systems that do tasks such as writing text, sorting data or spotting objects in images." },
  "GIS": { exp: "geographic information system", def: "Software and methods for making maps and studying where things are." },
  "lidar": { exp: "light detection and ranging", def: "A laser method that measures distance, used to map land and forests in three dimensions." },
  "UAS": { exp: "uncrewed aircraft system", def: "A drone, plus its controls and the people who fly it." },
  "QA": { exp: "quality assurance", def: "The planned steps that make sure work and data meet a set standard." },
  "QC": { exp: "quality control", def: "The checks that find and fix errors in work or data." },
  "GHG": { exp: "greenhouse gas", def: "A gas, such as carbon dioxide or methane, that traps heat in the air." },
  "PFAS": { exp: "per- and polyfluoroalkyl substances", def: "A large group of human-made chemicals that last a very long time, often called “forever chemicals”." },
  "HAZWOPER": { exp: "Hazardous Waste Operations and Emergency Response", def: "The OSHA safety standard, and its training, for work at hazardous waste sites and chemical spills." },
  "EHS": { exp: "environment, health and safety", def: "The part of a business that manages pollution, worker safety and the rules for both." },
  "ESG": { exp: "environmental, social and governance", def: "Topics beyond profit that companies report on and investors look at." },
  "ICS": { exp: "Incident Command System", def: "A standard way to organize people and resources for emergencies and wildfires." },
  "IQCS": { exp: "Incident Qualifications and Certification System", def: "A federal database that tracks wildland fire training and qualifications." },
  "IQR": { exp: "interquartile range", def: "The spread of the middle half of a set of ratings; a small IQR means most raters agree." },
  "Delphi panel": { exp: "", def: "A group of experts who rate items on their own over several rounds, seeing a summary each time, until they agree." },
  "prescribed fire": { exp: "", def: "Fire set on purpose, under a written plan and the right weather, to meet land goals; also called a prescribed burn." },
  "burn boss": { exp: "", def: "The person in charge of a prescribed fire on the ground." },
  "ground-truth": { exp: "", def: "To check a map, model or remote sensing product against what is really on the ground." },
  "remote sensing": { exp: "", def: "Gathering facts about land, water or air from a distance, using satellites, aircraft or drones." },
  "silviculture": { exp: "", def: "The practice of growing and tending forests to meet set goals." },
  "riparian": { exp: "", def: "Describes the land along the banks of a river, stream or lake." },
  "remediation": { exp: "", def: "Cleaning up polluted soil, water or sites." },
  "reclamation": { exp: "", def: "Returning land disturbed by mining or drilling to a stable and useful state." },
  "hazard mitigation": { exp: "", def: "Action taken before a disaster to lower long-term risk to people and property." },
  "adaptive management": { exp: "", def: "Managing in cycles: act, watch the results, learn, then adjust." },
  "chain of custody": { exp: "", def: "The signed record of who handled a sample or piece of evidence, and when." },
  "stop-work authority": { exp: "", def: "The right and duty of any worker to stop a job they believe is unsafe." },
  "field craft": { exp: "", def: "Skill in sensing, measuring and acting safely in a real place, learned through supervised time in the field." },
  "data craft": { exp: "", def: "Skill in turning field notes and measurements into evidence people can trust, including checking work done by AI." },
  "statecraft": { exp: "", def: "Skill in turning knowledge into decisions that hold up, by working through laws, agencies, budgets and people." },
};
