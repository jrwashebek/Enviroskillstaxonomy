## Data Craft (DC): Phase 2 summary

All eight CSVs passed validation, but `report.md` is not on disk: the harness blocks subagents from writing report files. Its full text is in the section below. Please save it verbatim to `/home/claude/emst/docs/research/data-craft/report.md`.

**Definition.** Data craft is the disciplined capacity to turn observations of environmental systems into *warranted* evidence, models and decision support: designing what gets measured, stewarding data so it stays fit for use and properly governed, analysing and modelling with honest uncertainty, and putting results in front of decision-makers in a form they can act on. Because more and more of that computation is now done by machines, data craft also includes specifying, validating, supervising and answering for AI-generated analysis.

**Top findings**
- **Most environmental AI is classical ML.** I computed this from OMB's 2025 inventory, cloned from GitHub. USDA, DOI and EPA report 438 use cases; 86 are deployed, and 59 of those are classical ML. Only 8 deployed cases are generative AI, and the 2 deployed agentic cases are administrative. [E]
- **Generative AI is deployed for text work.** The uses are Forest Service plan review, FWS comment analysis (analyst-verified) and NEPA drafting pilots. The tools churn: DOI's PCAT was retired between inventories. [E]
- **High-impact designations hinge on human review.** The high-impact environmental cases are ML that drives payments or enforcement. Three other cases escaped the designation because a human is claimed as the "principal basis" of the decision. Whether review is substantive is a data-craft skill. [E]
- **Plans demand durable analysis, not AI.** None of the 58,544 OpenLMP plan components mentions AI; 3,843 require monitoring. Models, platforms and policy memos turn over in one to three years. [E]
- **Domain 2 is mostly tool-framed.** Of its 35 competencies I rate 9 as durable, 16 as mixed and 10 as tool fluency. Verdicts: carry 3, change 25, retire 7. [J]

**Top proposals**
- **P-DC-01:** warrant-based craft definition with five durable functions.
- **P-DC-02:** rules DC-R1–R5 separating durable competencies (L1) from the tools layer (L4). This answers your DP-3 question.
- **P-DC-03 / P-DC-04:** restructure Domain 2 and stand up a 53-entry tools layer with a deprecation policy.
- **P-DC-05:** universal data and AI literacy (DC-CAND-01, DC-CAND-02).
- **P-DC-06 / P-DC-07:** assurance and stewardship clusters.
- **P-DC-10:** four scope-of-accountability levels assessed with seeded-error work samples.
- **P-DC-13:** a v1 data-integrity fix. The SA 2.6 exposure codes in the database contradict the working record.

**Biggest expected disagreement: SC.** v1 7.1.4 makes AI governance SC-only. I argue risk tiering and review design need data craft. LM is second: I argue v1's substitution (S) codes on comment and policy analysis are not supported by deployment evidence.

**Evidence gaps.** The team's web-search budget ran out early. FAIR, CARE, EPA model guidance, the Evidence Act, ISO/IEC 42001, ESDT, Destination Earth, Digital Promise, ESIP and DataONE are marked `unverified`. Claims that rest on them are labelled [J].

**Files** (all in `/home/claude/emst/docs/research/data-craft/`):
- `sources.csv` (60)
- `candidate_competencies.csv` (22)
- `role_signals.csv` (16)
- `v1_assessment.csv` (57)
- `durable_vs_tool_classification.csv` (38; an extra structured file)
- `tools_layer_proposal.csv` (53)
- `datacraft_proficiency_anchors.csv` (48)
- `ecosystem.csv` (32)

The build scripts are in `/tmp/claude-0/-home-claude/fbbe9940-26ca-5e5a-9a05-1e06b16da4ee/scratchpad/build/`.

---
