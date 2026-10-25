# EMST v2: what to carry over to the Skills Taxonomy research project

*Written 2026-10-25 by Claude, the orchestrating AI agent, for the EMST project lead. The source of truth is the public repository at https://github.com/jrwashebek/Enviroskillstaxonomy. The full flagship report is at `docs/package/report/flagship_report.md`, currently draft 0.9.1.*

The companion "Skills Taxonomy" project produces the research and literature on the taxonomy. The statements below changed during the v2 build. Writing in that project should match them.

## 1. The taxonomy itself has changed shape

- **v1 structure becomes history.** v1's "7 domains, 45 skill areas, 222 + n competencies" structure is now methodology history. v2 is layered:
  - L0: vocabularies
  - L1: competencies, including six transversal areas
  - L2: tasks
  - L3: role profiles with sector-actor variants
  - L4: tools
  - L5: change signals, instruments and driver events
  - L6: crosswalks

  Wave-1 subsector modules sit on top. v1 domains survive only as a legacy facet.
- **Crafts.** The three crafts (field, data and statecraft) are weighted 0, 1 or 2 on each *task*. The blend for a competency or role is computed, not tagged.
- **Counts.** Current counts come from the release build, `docs/release/2.0.0-rc.1/counts.json`. They are being re-cut after an independent data review. Do not type counts by hand; quote the generated file.
- **v1 statistics.** v1's single-analyst statistics, such as the share of tasks exposed and the FPP findings, may be cited **only as methodology history** (project-lead decision Q7). They are not current findings.

## 2. Corrected facts (use these wordings)

| Topic | Use | Do not say |
|---|---|---|
| AmeriCorps | In April 2025 about $400M in grants were terminated. A court enjoined the terminations in 24 plaintiff states and DC on 5 June 2025. In July 2025 AmeriCorps told terminated grantees, including programs in non-plaintiff states, that they were eligible for reinstatement; uptake is undocumented. An 11 September 2026 settlement with 23 state attorneys general and two governors covers FY2026 in those jurisdictions only. Litigation is stayed to 1 February 2027. | "terminations persisted elsewhere"; "reinstated only in plaintiff states" |
| New Jersey EJ rules | The Appellate Division affirmed them on 5 January 2026. The NJ Supreme Court granted certification in July 2026, and the rules remain in effect pending appeal. | that the rules are settled law |
| Pennsylvania | The Office of Administration has identified federal job titles whose experience *may count as equivalent for certain* Commonwealth titles. It reports 1,350 hires with federal experience since EO 2025-01. | that federal experience is generally equivalent |
| AI exposure | Use percentile bands from the capability index. Analytical, regulatory and planning occupations fall in the top fifth; most field and operations occupations fall in or near the bottom third. | "most/least exposed in the economy"; "exposure splits in two" |
| Federal AI use (OMB 2025 inventory) | 504 use cases in **eleven** environmental units (nine agencies and bureaus and two USDA mission areas). Classical machine learning is 46% of all of them, a majority only of those that report a type. NEPA and permitting accounts for 5 use cases, none deployed. | "nine bureaus"; "most registered AI is classical ML" |
| Forest plan monitoring (OpenLMP) | Components *typed as* monitoring rose under the 2012 rule. 22 of the 36 2012-rule documents are monitoring reports or monitoring plans, so in plan documents alone the shares are about 10% vs 3%, with overlapping intervals. The finding is scoped to western national forests. | "monitoring requirements"; "durable demand for monitoring" |
| Self-assessment questionnaires (Merit Hiring Plan) | Give the rule's exceptions, seasonal work and GS-4 and below, and its FY2028 target. | the rule without its exceptions |
| Scope words | "federal" where the evidence is federal | "public" |
| Budgets | The contraction is a capacity shock. FY2026 Interior–Environment appropriations were only 1.9% below FY2025, enacted in January 2026 after most of the decline. | "budget cuts caused the contraction" |

## 3. Framing that changed

- **Career-ladder ("double squeeze") hypothesis.** It is always presented as a *hypothesis*, with its mechanism and evidence status. It becomes a finding only after named human reviewers, an industrial-organizational psychologist and a labor economist, have validated it, and it is then co-published with a nonpartisan partner. The project lead confirmed this rule on 2026-10-24.
- **Agent drafts are not findings.** Time shares, importance, critical and needed-at-entry flags, AI craft ratings and target levels drafted by AI agents are never shown as results. Every change claim is "assessment pending" until multi-rater human assessment exists.
- **Authorship.** The v2 package was researched and drafted by AI agents to a charter set by the EMST project lead. No independent human expert has reviewed it yet. External publication waits for the project lead's sign-off after at least one named human subject-matter review.
- **Scenarios.** The foresight set is now SC1–SC4, built on two axes: public capacity and AI legitimacy. Older scenario descriptions are superseded.
- **Ecosystem.** The ecosystem atlas (`docs/adoption/ecosystem_atlas.csv`) maps about 450 organizations, indices, programs and funds. The October 2026 scan found **no standing environment-sector coalition on workforce skills and AI**; the closest activity is ad hoc joint statements. That convening role is open.
- **Tribal content.** Indigenous knowledge is out of scope by design. Nothing Tribal-related is published until a Tribal Advisory Council constituted by Tribal governments exists and approves (Q1).

## 4. Project instructions to update

Both projects' instructions still describe v1: "222 + n competencies across 7 domains, 45 skill areas", the Task Sequence v7 and the Excel database as the store. In the v2 repository:
- the source of truth is `data/v2/`, with records in YAML per record;
- the normative release is a JSON-LD bundle, with CSV, SKOS and SSSOM exports;
- decisions are recorded as ADRs (ADR-0001 to ADR-0032) and in `docs/decisions/DECISION_LOG.csv`.

Q10, which asks whether to retire the task sequence and update the project instructions, is still open.
