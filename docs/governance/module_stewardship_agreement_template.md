# EMST Module Stewardship Agreement — template

- **Work package:** WP-13 · **Author:** A10b (AS) · **Date:** 2026-10-23 · **Template licence:** CC0 1.0 (see `LICENSING.md` §2)
- **Builds:** ADR-0009 §3 (phased federation; MSA terms; orphan clause), ADR-0018 (modules, three-module and home-module rules), ADR-0010 (namespaces, IDs), ADR-0013 (no separate licence), ADR-0007 (Tribal hold), ADR-0012 (no personal data), ADR-0024 (evidence by use); SPEC §3.2, §12, §18.2; governance charter Art. 4.7.
- **Provisional status carried:** ADR-0018 is **provisional-pending-verification** — the module structure is accepted, but module-partner readiness rests on [J] claims of which V3 confirmed only a subset (SAF, TWS, AFS, SRM, SER, NEHA, ASFPM active; ISSP credentials issued by GBCI; IEMA now ISEP). ADR-0009 needs the project lead for constituting bodies with external members.
- **Status:** template. **No agreement has been signed and none can take effect before v2.2 (2029).** Through v2.0–v2.1 (2027–2028) modules are editorial sections authored centrally, with candidate advisory partners (Schedule D is the advisory-partner letter used in that period). <!-- PENDING Q8: default — no module is described as stewarded. -->

> **How to use this template.** Text in `[square brackets]` is completed for each agreement. Do not delete the core terms in Articles 3–8; they are the conditions under which the module may carry the EMST name (charter Art. 11). This is not legal advice; each party's counsel reviews the final text.

---

## Parties

This Module Stewardship Agreement ("Agreement") is made on `[date]` between:

1. **`[Steward institution]`**, acting as EMST Steward and holding the EMST name and marks in trust for the EMST Consortium ("the Steward") <!-- PENDING Q3: until a host exists, the project lead signs for EMST. -->; and
2. **`[Module steward organization]`**, `[legal form, address]` ("the Module Steward"), `[and, for a joint stewardship, [second organization]]`.

## Article 1. Purpose

1.1 The Module Steward will maintain the EMST module **`[MOD-nn name]`** (namespace `emst:[namespace]/`; subsectors `[codes from vocab/subsectors.yaml]`) ("the Module") as part of EMST, so that depth in `[subsector]` is maintained by people who practise it, while the EMST core stays coherent and interoperable.

1.2 Recitals: the Module has been an EMST editorial section since `[release]`; the Module Steward served as its advisory partner under the letter dated `[date]` (commitment register ID `[CR-…]`) and completed review cycles on time in `[year]` and `[year]`, satisfying the two-cycle condition in ADR-0009 §3.

## Article 2. Definitions

"Core", "module", "home module", "enactment", "release", "use tier", "validation status" and "Tribal-related content" have the meanings in `docs/standard/SPEC.md` and the governance charter. "Review cycle" means one full pass of the change-request process over the Module's open requests and its scheduled review items, completed in time for the April MINOR release.

## Article 3. Technical conformance (core terms)

The Module Steward will:

3.1 use the **core schema** at the version pinned by each release, the **core L0 vocabularies**, and the Module's registered **namespace** for any new IDs, minted only through the EMST minting process (SPEC §12.2);

3.2 **never redefine a core ID**, and reference core records only in the permitted direction (module → core; core records never depend on module records) (SPEC §3.2);

3.3 apply the **three-module rule** and the **home-module rule**: a competency enacted in three or more modules is proposed for the core; a module-level competency has exactly one home module (ADR-0018 §6);

3.4 publish crosswalks only as SSSOM mapping sets with external **IDs only** (SPEC §15);

3.5 pass the TSC's **conformance check** at each release (SPEC §18.2); a failed check holds the Module's changes back from that release, not the release itself.

## Article 4. Content and evidence (core terms)

4.1 Content meets the **core evidence standard**: every substantive claim labelled E/J/S with resolvable sources; S and X changes supported by two independent sources including at least one demand signal or SME panel data (charter Art. 6.2).

4.2 Content passes the **typing, naming and indicator lint** (no named products or instruments in L1/L2 text; function-based titles; observable indicators) (SPEC §18.4).

4.3 Use tiers and validation statuses are stated honestly: no record is marked `panel-retained`, `job-analysis-confirmed` or `select` without the evidence ADR-0024 requires; agent-assisted text is labelled and carries evidence label S until a named human reviews it.

4.4 No computed field (counts, modal values, roll-ups) is typed into source records (ADR-0021).

## Article 5. Cadence and service (core terms)

5.1 At least **one review cycle per year on the core cadence**, completed by `[date, e.g. 15 February]` for the April MINOR release.

5.2 Triage of Module change requests within 30 days; comment periods and adjudication per `CONTRIBUTING.md` §4.

5.3 Errata affecting adopters (e.g. a wrong licence gate or a mis-stated credential issuer) are corrected for the next PATCH.

## Article 6. People (core terms)

6.1 The Module Steward names a **module lead** (`[role title]`), a **deputy**, and an **SME pool** of at least `[n]` practitioners spanning at least `[three]` sector actors and the relevant crafts, recorded in Schedule B by role and organization (pseudonymous IDs in the repository).

6.2 SME panels used for validation follow the composition rules in charter Art. 4.8 (≤ 30% from any sector actor; ≥ 50% independent where recruited through adopters).

6.3 Members of the Module Steward's staff file conflict-of-interest disclosures and recuse as charter Art. 9 requires.

## Article 7. Licence, marks and data (core terms)

7.1 **No separate licence.** Module content is released under the EMST licensing set (`LICENSING.md`): CC0 1.0 for data and standard text; CC BY 4.0 for narrative publications; Apache-2.0 for code. The Module Steward contributes under the Developer Certificate of Origin; no copyright assignment.

7.2 Third-party material (e.g. the Module Steward's own exam blueprints, accreditation criteria or proprietary standards) is **not** placed in CC0 files; it is cited, paraphrased, or shared under a separate data agreement (Schedule C).

7.3 The Module Steward may describe itself as "EMST module steward for `[module]`" while this Agreement is in force. "EMST-conformant" and "EMST-mapped" claims about its own products require a conformance check (charter Art. 11.3).

7.4 **No personal data.** The Module Steward will not submit person-level data about workers, applicants, members or panelists; panel results enter EMST only as aggregates (ADR-0012).

## Article 8. Tribal-related content (core terms)

8.1 Tribal-related content in the Module is governed by the Tribal Advisory Council, not by this Agreement. Until a TAC exists and approves an item, nothing Tribal-related is published (ADR-0007 §D; `tribal_gate_procedures.md`).

8.2 The Module Steward will not submit Indigenous knowledge content, confidential Tribal information, characterizations of named Tribes, or Tribal employers' documents or postings, and will not represent any Tribe or Tribal organization as participating in the Module.

## Article 9. Decision rights

9.1 Within the Module namespace and the core terms above, the Module Steward **decides** content changes (charter Art. 4.7).

9.2 The **EB** decides release inclusion and any change that affects the core; the **TSC** decides conformance; the **TAC** decides Tribal-related content.

9.3 Disputes between the Module Steward and EMST bodies go first to the EB, then to the AC Executive Group (charter Art. 8.2).

## Article 10. Resources

10.1 `[Choose one and complete.]` (a) The Module Steward contributes staff and SME time in kind, valued at `[$]` a year and reported in EMST's annual report; **or** (b) the Steward pays the Module Steward `[$]` a year for `[FTE / services]` under Schedule E; **or** (c) a combination.

10.2 Funding received for Module work is disclosed in the commitment register. Funders of Module work have no vote on Module content (charter Art. 9.3).

## Article 11. Term, review and the orphan clause

11.1 Term: three years from `[date]`, renewable by written agreement.

11.2 Annual review: the TSC's conformance report and the EB's cycle report are shared with the Module Steward each May.

11.3 **Orphan clause.** If the Module Steward misses **two review cycles**, or withdraws, the Module **returns to the core**: the EB resumes authorship, the Module's IDs and history are kept, and the Module Steward hands over open requests and working files within 60 days. Withdrawal requires `[six]` months' written notice where possible.

11.4 Either party may terminate for material breach of Articles 3–8 after 90 days' notice and an opportunity to cure.

## Article 12. Commitment record and year-five owner

12.1 This Agreement is entered in the commitment register with rung 5 (co-govern), the artifact "Module Stewardship Agreement", the signature date, signatories, review date and the **year-five owner** — the named role at the Module Steward that will be accountable for the Module in year five of the Agreement, and its successor if that role lapses.

12.2 Neither party describes the Module as "stewarded" before both signatures are recorded in the register.

## Signatures

| For the Steward | For the Module Steward |
|---|---|
| Name, title: | Name, title: |
| Date: | Date: |

---

## Schedule A — Module scope

- Module: `[MOD-nn]` · namespace `[namespace]` · subsectors `[codes]` · wave `[1/2/3]`
- Home-module competencies at signature (generated list, not typed): `[link to generated view]`
- Enactments of core competencies maintained by the Module: `[generated view]`
- Credentials and licensure gates relevant to the Module (from the credential register; issuer-verified flag shown): `[generated view]`

## Schedule B — Module lead, deputy and SME pool

| Role | Organization | Sector actor | Craft(s) | Pseudonymous ID in repo |
|---|---|---|---|---|
| `[module lead]` | | | | |

## Schedule C — Data agreements for third-party material (if any)

`[Title, parties, permitted uses, retention, no personal data, no CC0 inclusion.]`

## Schedule D — Advisory-partner letter (for v2.0–v2.1 editorial sections)

> `[Organization]` agrees to serve as **candidate advisory partner** for the EMST editorial section `[module]` for the `[2027/2028]` release cycle. It will `[review drafts of module content / nominate SMEs / host one review session]`, by `[dates]`. This letter creates no stewardship, licence or funding obligation, does not make `[Organization]` the steward of the section, and does not imply endorsement of EMST. EMST will describe `[Organization]` as an advisory partner only after this letter is countersigned and entered in the commitment register (ID `[CR-…]`).
>
> Signed for `[Organization]`: ________ Date: ______ · Signed for EMST: ________ Date: ______

## Schedule E — Payments (if any)

`[Amounts, deliverables, invoicing; firewall: payment does not buy content decisions (charter Art. 9.5).]`
