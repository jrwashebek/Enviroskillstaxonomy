# EMST v2: status as of 25 October 2026

*Written by Claude, the orchestrating AI agent, for the EMST project lead. Source of truth: https://github.com/jrwashebek/Enviroskillstaxonomy (main at commit 3865ed1). Every count below is copied from `docs/release/2.0.0-rc.1/counts.json`, which the build generates.*

## Where things stand

- **Release candidate.** EMST 2.0.0-rc.1 was built twice from clean commit a0d7281, and the two builds were byte-identical. It is suitable for the NGO-pilot preview and for design partners. It is **not cleared for external publication**:
  - release-gate item 6 fails, because no crosswalk subset has had human review;
  - release-gate item 7 fails, because external publication needs the project lead's sign-off after at least one named human SME has reviewed the release, and the date-sensitive facts still have to be re-checked.
- **Release contents:**

  | Item | Count |
  |---|---|
  | Competencies | 223 (163 of them core) |
  | Tasks | 1,317 |
  | Indicators | 1,699 |
  | Role profiles | 37 (13 P1, 17 P2, 6 P3, 1 P4) |
  | Role variants | 140 |
  | Change-signal records | 107, holding 68 distinct observations |
  | Federal Series Profiles | 13 |
  | State Class Views | 20 |
  | Held records | 163 (count only, under the Tribal hold) |

- **Lifecycle.** 197 competencies are *established*, which means long-standing work, not validated content. 26 are on *watch*. No record met the evidence test for *proposed* or *emerging*.
- **Provenance.** Every rating is an AI-agent draft (`raterType: llm`) or a v1 single-analyst, LLM-assisted prior (labelled S). When one model rated the same thing in several passes, those passes count as one rater.
- **Explorer.** The static explorer has 764 pages. Its output check reported 0 problems, and browser checks on 71 pages found 0 accessibility violations.

## The sector-facing package

| Piece | Where |
|---|---|
| Flagship report, draft 0.9.2 | The repo (`docs/package/report/flagship_report.md`), and a Claude Doc titled "How environmental jobs are changing (EMST v2 flagship report, draft 0.9.2)" |
| Briefing deck, 18 slides | The repo (`docs/package/deck/deck_content.md`), and a Slides artifact titled "How environmental jobs are changing (EMST v2 briefing deck)" |
| 13 role-change briefs and the Forester GS-0460 PD | The repo (`docs/package/briefs/`, `docs/package/forester_pd_fes_draft.md`) |
| Reviews | `docs/review/`: package review, evidence red team, package re-check, data/method review, and the fix logs |

## Project-lead decisions recorded

See `docs/decisions/PROJECT_LEAD_DECISIONS.md`.

- **Q1 (Tribal Advisory Council):** accepted all three provisions.
- **Q2 (v1 text licence):** CC0.
- **Q5 (rollout):** parallel tracks.
- **Q7 (v1 figures):** methodology history only.
- **Q12 (career-ladder hypothesis):** confirmed that it needs named human reviewers before it is published as a finding.
- **Q13 (sign-off):** the project lead signs off after a named human SME review.
- **Q14 (pilot offer):** unchanged.
- **Q15 (repository home):** decide later.
- **Other choices:**
  - the repo history was rewritten to remove private session details;
  - the call to action is GitHub Issues;
  - the package credits "the EMST project lead" only.

## Open items

- **Moving facts to re-check before any external release**, on or after these dates:
  - 26 October 2026: OFCCP effective date; Colorado hearing
  - 10 November 2026: SB 253; Section 106 after the ACHP meeting
  - 12 November 2026: Forest Service objection rule
  - 15 November 2026: S. 5653
  - before every use: Part 108; the OPM series decision; the SOC 2028 schedule
- **Human review needed** for gate items 6 and 7, and in particular a named SME reviewer for the report and the briefs.
- **Open questions with defaults in force:** Q3, Q4, Q6, Q8, Q9, Q10 and Q11.
- **Release tag.** The `v2.0.0-rc.1` tag exists locally. Pushing tags from the working session was refused (HTTP 403), so the tag can be created on GitHub at commit 3865ed1.
