> **Superseded (2026-10-23).** This is the WP-14 handback for draft 0.9. Draft 0.9.1 applies the evidence review, the package review and the WP-15 corrections: several headline findings below were reworded, the claims list now has 280 rows (none awaiting a register row) and F05/F06 were rebuilt with sensitivity checks. See `docs/review/fixlog_A.md`. Kept for the record only. **Note (2026-10-25, rc.1 package sync):** the current draft is 0.9.2, and its claims list has 283 rows (`docs/review/fixlog_rc1_package_sync.md`). The sign-off path this handback named is replaced by project lead decision Q13 (2026-10-24): external publication is signed by the EMST project lead, after at least one named human subject-matter reviewer has read the report and briefs; AI agent checks, including the adoption-lead role, are advisory. One draft 0.9 headline below used wording the claims register forbids (RPT-01); it is not repeated here.

I wrote `figures/` and `claims_used.csv`. The harness refused the write of `flagship_report.md` ("subagents should return findings as text"), so its full text follows below. LM's WP-15 sign-off clears it for internal drafts and the NGO-pilot preview only; external release needs the project lead's signature under Q13 (see the note above) and the moving-fact re-checks.

The coordinator's updates are in: S. 5653, the Colorado draft rules, the USFS objection rule, NIFC figures, and the `do_not_say` wording.

**Five headline findings, as written:**
1. The biggest force on public environmental jobs right now is a capacity shock, not AI.
2. [Draft 0.9 wording withdrawn: claims register RPT-01 forbids it. Draft 0.9.1 and later read "AI exposure varies widely across environmental work, and the evidence on actual use is still thin."]
3. Roles are being re-bundled, not deleted, and policy is moving faster than technology.
4. The entry path is the risk to watch. It is a hypothesis with a mechanism, not yet a finding.
5. Some moves are right in every plausible future, and they can start now.

**Length:** about 11,000 words, at the top of the target range (11,007 counted, excluding references but including tables and front matter).

**Figures built:** F01–F10 as CSVs, generated and checked by `build_figures.py`. Two are deliberately not built:
- Exposure profiles: Eloundou and Microsoft licence terms are unrecorded, so the report states this finding in words only, with no values.
- Craft blend by role: every craft value is an agent draft.

**Awaiting WP-15:** `claims_used.csv` lists 264 claims; 94 cite register IDs and 135 rest on EMST decision records. 35 are not yet in the register:
- headcount and operations: NRCS −23.8%, the USDA OIG 16% figure, the trail-miles −22% figure, USFS drone hours and pilot share, GAO drone findings;
- labour market and states: Trellis, E2, Census BTOS, Humlum, Yale, GDPval, AEI's first release and labour-market study, CRS's 540 Good Neighbor agreements, Pennsylvania's 1,350 hires, the New York portal, the skills-based-hiring results, pay medians;
- other: the coalition gap, plan content rates, the qualitative exposure profile.

The moving facts also need re-checking: Colorado (26 Oct), OFCCP (26 Oct), Section 106, the USFS objection rule (12 Nov), SPEED Act and S. 5653, and Part 108.

Files are in /home/claude/emst/docs/package/report/:
- claims_used.csv
- figures/build_figures.py
- figures/figures_index.csv
- figures/f01_public_capacity_change.csv … f10_p1_corridors_and_roles.csv

# FULL TEXT OF /home/claude/emst/docs/package/report/flagship_report.md

