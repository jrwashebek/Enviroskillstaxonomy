# R1 Benchmark: how public skills, occupation and competency taxonomies present themselves

**Author role:** benchmark researcher, EMST HCD team · **Date:** 30 October 2026 · **Status:** desk research. No users were contacted.

**Evidence labels:** [E] means I read the source, and the URL is in that section's source list; every web source was accessed on 30 Oct 2026 unless another date is given. [J] means my professional judgment, with its basis. [S] means speculation, with what would settle it.

---

## 1. Executive summary

1. **Published evidence on how people use taxonomy interfaces is scarce.** [E] The usable pieces I found:
   - England's National Careers Service survey: 54% website satisfaction against 86% for phone and face-to-face (2023–24).
   - Two GOV.UK careers-service assessments (2017, 2019).
   - Australia's 2024 National Skills Taxonomy (NST) consultation: taxonomies are "hard to understand and navigate".
   - NICE's 2021 workshop: employers called the framework "too complex".
   - ESCO's 2019 study visits: labels too long, duplicates, provenance unclear.
   - CareerOneStop's 2024 report: 82% trust, but its usability findings are unpublished.

   Most patterns below are "observed, not tested". EMST should test them, not copy them. [J]

2. **Best provenance pattern: O\*NET's per-occupation "Data sources" page.** [E] It labels each content block with a year and rater type, for example "2025 (ai/sme) task statements". O\*NET already labels AI-assisted content, but by category and one click away. EMST should go to per-record review status.

3. **A status label on every record works and is rare.** [E]
   - Skills England shows a five-state icon-plus-label key: Potential, In development, Approved, Without apprenticeship, Custom.
   - The DoD 8140 matrices say "TBD" for content still being validated.
   - The GOV.UK Design System found users understood a "trial" tag.

   These are the closest precedents for "AI draft, not reviewed" and "Assessment pending".

4. **No benchmark says what a record may or may not be used for.** [E] EMST's per-record use tiers are genuine white space.

5. **Crosswalks are weak everywhere.** [E]
   - ESCO's crosswalks are AI-assisted file downloads with no match type in the interface.
   - O\*NET's expert-reviewed, tiered related occupations show neither basis nor tier.
   - My Next Move for Veterans matches Forest and Conservation Technicians to Cavalry Scout and Wheeled Vehicle Mechanic, with no caveat.

   EMST's role pages print "confidence 0.5" on unreviewed AI matches, which is the same false precision. [E repo, J]

6. **Version skew and decay damage trust.** [E]
   - NICE is 2.2.0 at NIST but 2.0.0 in CISA's search.
   - Australia's Skills Classification is frozen and gated.
   - openskillsnetwork.org/about redirects to an unrelated site.
   - NWCG leaves "Last Modified / Reviewed" blank.

7. **Correction loops are closed or opaque.** [E]
   - SFIA's change-request register shows statuses, but commenting needs an account.
   - JSA collected comments by emailed spreadsheet.
   - ESCO's feedback fora are invitation-only.

   None shows per-record outcomes. [J]

8. **External change EMST must reflect.** [E]
   - OPM's April 2026 consolidation proposal (0455 into 0404, 0029 into 0303).
   - O\*NET's move from five Job Zones to four (from release 30.2), and the 31.0 database (August 2026).
   - NWCG's annual PMS 310-1 revision.

   EMST's OPM and O\*NET records need "as of" dates.

---

## 2. Method and limits

- **How I gathered material.** Live pages were fetched with WebFetch, which returns text, not screenshots. Leads came from WebSearch. Every fetch was made on 30 Oct 2026.
- **Accessibility and mobile notes are inferred from page text and structure only.** No automated or manual accessibility testing was done. [J]
- **Blocked or not retrieved** [E]:
  - O\*NET's home page (permission timeout; record and help pages were retrieved).
  - skillsfuture.gov.sg pages and PDF (metadata only); the IMDA PDF (404).
  - An ESCO occupation record page.
  - SFIA's change-request list (needs an account).
  - The DCWF Tool; an OaSIS profile; a CareerOneStop occupation profile; the Credential Finder application.
  - The ASC explorer (gated, failed to load).
  - openskillsnetwork.org/about (redirects to an unrelated domain; not followed).
- **My web-search budget ran out** before I could look up mySkills myFuture's match display or Singapore's dashboards directly. Those findings rest on documents only, and I say so where it matters.

---

## 3. Site-by-site findings

### 3.1 O\*NET OnLine (US DOL / National Center for O\*NET Development)

**Bottom line:** this is the reference design for record density and progressive disclosure, with a strong provenance trail and weak explanation of computed relationships.

- **Audience and entry points.** The site is search-first: a header box with "Type a title or code". Menus offer Find Occupations, Advanced Searches and Crosswalks. Sister sites (Easy Read, Veterans, Español) are offered from a "More" tab, with a "leaving O\*NET" prompt. [E]
- **Information architecture.** O\*NET-SOC has about 1,016 titles, and the job-coding help says SOC 2018 and CIP 2020 crosswalks are used. Record pages group content under seven headings, from Occupation-Specific Information to Workforce Characteristics. [E]
- **Record page** (Park Naturalists 19-1031.03):
  - Title, code, "Bright Outlook" tag and an "Updated 2026" link.
  - Ten sample reported job titles.
  - Sections showing the top 5 items with "N of M" counts: Tasks 5 of 20, Work Activities 5 of 25, Abilities 5 of 16.
  - Summary, Details and Custom report tabs. The Custom report lets users choose a scale and set a cutoff. [E]
- **How values are shown.**
  - The Summary report shows no numeric scores for skills, knowledge or abilities.
  - Work Context is shown as a respondent distribution in words, for example "82% responded 'Extremely important'". [E]
  - The wage block is explicitly labelled as data for a different occupation (Conservation Scientists), so borrowed data is declared, not hidden. [E]
- **Search.**
  - Keyword search covers alternate titles, descriptions, tasks and work activities. Results are ranked with no visible score.
  - "How do they match?" opens counts of matching titles, tasks and activities, with the query words highlighted. [E]
  - The help pages do not say how misspellings are handled. [E]
- **Comparison and crosswalks.**
  - Related Occupations combine three similarity measures (tasks, titles, knowledge), then expert review, which replaced 280 relations.
  - Results are tiered (top 5, 6–10, 11–20), but the page shows "5 of 10" with no basis or strength. [E] This is hidden basis. [J]
- **Provenance and versioning.**
  - The record page shows "Updated 2026" and the footer "Site updated October 6, 2026".
  - No database version appears on the record page. The version (31.0) appears only on My Next Move's data-sources page (§3.2). [E]
  - O\*NET 31.0 shipped in August 2026, and Job Zones moved from five levels to four starting with 30.2. [E]
- **Data access.**
  - Licence is CC BY 4.0, and every page has "Cite this Page".
  - Downloads in Excel and SQL were joined by CSV, JSON and RDF in July 2026.
  - API v2 exists, with a sign-up.
  - O\*NET content-model frameworks are also published as CTDL-ASN JSON-LD. [E]
- **Accessibility and mobile.** Many sections render "Loading..." in text capture, so the content depends on scripts. [E] Progressive enhancement is uncertain. [J]
- **Published evidence.**
  - The National Research Council's 2010 review found O\*NET lacked ongoing feedback from users and recommended a user advisory board. It also noted that O\*NET serves many users as "building blocks". [E]
  - Pages carry "Was this page helpful?", but no results are published. [E]

Sources:
- https://www.onetonline.org/link/summary/19-1031.03
- https://www.onetonline.org/help/online/summary
- https://www.onetonline.org/help/online/reports
- https://ONetOnline.org/help/online/search
- https://www.onetonline.org/help/job_coding
- https://onetcenter.org/whatsnew.html
- https://www.onetcenter.org/dl_files/Related_2024.pdf (5 Feb 2024)
- https://www.onetcenter.org/reports/Related_2025.html (Nov 2025)
- https://onetcenter.org/competencyFrameworks.html
- https://services.onetcenter.org/reference/online/occupation/summary/skills
- https://www.nationalacademies.org/read/12814/chapter/2 (2010)

### 3.2 My Next Move, My Next Move for Veterans and Mi Próximo Paso

**Bottom line:** this is the best plain-language parallel view of the same data. The veterans translator over-promises.

- **Audience and entry points.** The site is task-first: Search, Industries, and Interests (the Interest Profiler). The Veterans and Spanish versions are separate sites. [E]
- **Record page** (Forest & Conservation Technicians):
  - Keyword tags, then "Also called", "What they do" and "On the job, you would" (3 bullets).
  - Knowledge, Skills and Abilities in plain subgroups with no scores.
  - Technology, with "Hot Technology" tags.
  - Education given as text: "2 of 4", then a sentence.
  - Job Outlook as an icon plus words ("New job opportunities are less likely").
  - Explore More, and a print dialog where a teacher or counsellor can add a name to a printed copy. [E]
  - Two "Also called" lists on the same page disagree: four titles in one, six in the other. [E]
- **Provenance.** This is the stand-out pattern. A per-occupation "Data sources" page lists, by section, the year and rater type:
  - "2025 (ai/sme) task statements";
  - "2018 (analyst) skills ratings";
  - "2026 (machine learning/expert) interests ratings";
  - "O\*NET 31.0 Database". [E]

  It is one click from the profile and written in plain words. [J]
- **Crosswalk (veterans).**
  - "Where in the military?" lists matching titles by branch. For Forest & Conservation Technicians these include Cavalry Scout, Intelligence Analyst, Military Police and Wheeled Vehicle Mechanic. "No similar titles were found" repeats for several branches.
  - There is no caveat about match strength. The crosswalk's source is "Defense Manpower Data Center and other sources", with no date. [E]
- **Published evidence.** A Marine Corps career-services article (first published Feb 2021) recommends My Next Move for Veterans for research rather than job search. It notes that most translators key only on the MOS, so equivalents may be incomplete. [E]

Sources:
- https://MyNextMove.org/profile/summary/19-4071.00
- https://www.mynextmove.org/vets/profile/summary/19-4071.00
- https://www.mynextmove.org/vets/help/data/19-4071.00
- https://29palms.usmc-mccs.org/news/whats-with-all-these-military-experience-translators

### 3.3 CareerOneStop (US DOL)

**Bottom line:** a hub of tools with heavy traffic. It publishes some trust data but not its usability findings.

- **Audience and entry points.** Entry is tool-first and section-first: Explore Careers, Find Training, Job Search, Find Local Help, Toolkit and "Resources For". Tool cards include Skills Matcher and mySkills myFuture. There is a keyword search, a skip link, a "Translate" link, and phone and TTY lines. [E] The occupation profile page itself was not retrieved. [E]
- **Skills Matcher.**
  - Users rate 40 skills over four pages. A formula compares them with O\*NET KSA ratings for more than 900 occupations and returns up to 150 careers, each with wage, education and outlook (Bright, Average or Below average).
  - No match score is explained.
  - There is one honest caveat: rating most skills at the same level "may not get reliable career matches". [E]
- **mySkills myFuture** (brochure, undated). It offers "careers that use similar skills" and a "side-by-side chart of likely skill gaps". The hedged wording ("may be a good match", "likely gaps") is a good tone model. [E]
- **Accounts.** Optional login gives saved pages. [E]
- **Published evidence** (2024 Annual Report) [E]:
  - About 18M visits and 185M page views.
  - 82% of survey respondents said they trusted the site.
  - 87% of API users were satisfied.
  - Two usability studies with 22 users covered Job Finder, accounts, how-to guides, video findability and accordion behaviour. Their findings are not published.
  - An 11-member advisory group supports the work.

Sources:
- https://cloudfront.careeronestop.org/Toolkit/Skills/skills.aspx
- https://cloudfront.careeronestop.org/Toolkit/Skills/skills-matcher-help.aspx
- https://cloudfront.careeronestop.org/TridionMultimedia/tcm24-7103_PDF_MSMFbrochure.pdf
- https://stagechatbotapi.careeronestop.org/TridionMultimedia/tcm24-61393_PDF_AnnualReport2024.pdf

### 3.4 ESCO portal (European Commission)

**Bottom line:** the model for version selection, multilingual data and machine access. It is weak on explaining relations and on crosswalk display.

- **Audience and entry points.** The home page offers Classification (Occupations, Skills & Competences, Qualifications), About, Use ESCO, and a stakeholder dropdown covering career advisers, public employment services, job portals, HR vendors and researchers. [E]
- **Information architecture.**
  - The skills pillar has four branches: Transversal, Skills, Knowledge and Language.
  - Occupations sit beneath ISCO-08 at level 5 and below.
  - v1.2.1 has 3,039 occupations and 13,939 skill concepts. [E]
- **Browser.**
  - A hierarchy or search toggle.
  - Filters hidden behind "Show filters": concept type, reusability level (transversal, cross-sectoral, sector-specific, occupation-specific), status (Released or Obsolete), and labels such as Green, Digital and DigComp.
  - A version dropdown (v1.0.9, v1.1.2, v1.2.1) and 28 interface languages. [E]
  - The skills browser showed a "temporary issue on this page" banner when fetched. [E]
- **Record content.**
  - Preferred, non-preferred and hidden labels; description; scope note; regulatory aspect; ISCO code; and essential and optional skills.
  - "Essential" is defined as "usually required ... independent of the work context or the employer". [E] I could not see how the record page lays these out (see §2).
- **Versioning.**
  - The portal shows the current version (v1.2.1, last updated 10/12/2025) and the portal release.
  - A delta file lists v1.2 against v1.1.2 differences.
  - The API takes a `selectedVersion` parameter.
  - "Obsolete" is a filterable status. [E]
- **Crosswalks.** The ESCO–O\*NET (CSV, 2023) and ESCO–NACE (XLSX, 2026) crosswalks were built with machine learning or AI and documented in technical reports. Relation types are not shown on the page, and crosswalks are downloads, not record features. [E]
- **Data access.** Downloads, a web-service API, and the ESCO Skill–Occupation Matrix tables. [E]
- **Published evidence.** The 2019 Member State Working Group paper "Measuring the success of ESCO" reports study visits [E]:
  - Textkernel found labels too long and near-duplicate skills, and asked for clearer documentation of provenance, such as the criteria for essential versus optional.
  - EURES found duplicates such as "use MS office" and "use office systems".
  - Minor fixes were easy to schedule, while structural ones needed evidence.

Sources:
- https://esco.ec.europa.eu/en
- https://esco.ec.europa.eu/en/classification/skill
- https://esco.ec.europa.eu/en/escopedia/occupations-pillar
- https://esco.ec.europa.eu/es/node/189
- https://esco.ec.europa.eu/system/files/2024-05/V1.2%20Launch%20-%20ESCO%20SEC%20combined%20-%20final%20clean.pdf
- https://esco.ec.europa.eu/hu/use-esco/other-crosswalks
- https://esco.ec.europa.eu/en/about-esco/publications/publication/crosswalk-between-esco-and-onet-technical-report (2022)
- https://esco.ec.europa.eu/system/files/2021-07/5baec5da-824d-446a-8cec-91ae5fa3eebcMSWG_9-3_Measuring_the_success_of_ESCO.pdf (Jan 2019)
- https://esco.ec.europa.eu/system/files/2021-07/2e360c35-21d7-4f80-94f8-7b6c397ebfe97_-_ESCO_feedback_mechanism_MSWG.pdf

### 3.5 NICE Workforce Framework for Cybersecurity (NIST resource center; CISA NICCS tools)

**Bottom line:** a well-versioned data product spread across tools that disagree about the version, with a hover-driven career visual.

- **Information architecture.** Work Role Categories, then Work Roles (with IDs such as OG-WRL-017), then Task, Knowledge and Skill (TKS) statements (T/K/S IDs), plus Competency Areas (NF-COM-xxx). Version 2.2.0 has 962 tasks, 693 knowledge statements and 556 skills. [E]
- **Function over title.** NICCS states that work roles are "not synonymous to job titles or occupations". [E]
- **Versioning.**
  - NIST marks "CURRENT VERSION: 2.2.0" and publishes a change summary for each release.
  - The 2.2.0 summary is dated 28 Apr 2026. The NIST banner reads "April 28, 2025", an inconsistency on the page.
  - The summary lists removed IDs (K0663, S0768, T1648) and replaced IDs (K0828 to K0803, and others). [E]
  - Formats are CPRT browse, XLSX, JSON, a CTDL publication and the SP 800-181r1 PDF. [E]
- **Version skew.**
  - NICCS's Work Role Search says it uses Components v2.0.0.
  - NIST's tools page says the NICCS tools derive from v1.0.0.
  - NIST itself lists 2.2.0 as current. [E]
- **Cyber Career Pathways Tool.** A "work role galaxy" where hovering shows a pop-up and draws lines to related roles. It offers side-by-side comparison of overlapping TKS. Overlap is described only as "most overlapping", with no numbers, and the guide mentions no text alternative. [E]
- **Published evidence.** The NIST workshop report (5 May 2021, 61 registrants) found [E]:
  - employers called the framework "Too complex" and reported a "Lack of comprehension";
  - employers wanted a 5-tier proficiency scale while educators wanted 3;
  - there was a risk of "assessment exhaustion" with fine-grained statements;
  - employers asked for standard job-description templates and self-assessments.

Sources:
- https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center/nice-framework-current-versions
- https://www.nist.gov/document/nice-framework-v220-summary-changes-april-2026pdf
- https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center/resources/nice-framework-tools
- https://niccs.cisa.gov/tools/nice-framework/work-role
- https://niccs.cisa.gov/tools/cyber-career-pathways-tool/user-guide
- https://www.nist.gov/document/nice-framework-competencies-workshop-report

### 3.6 DoD Cyber Workforce Framework (DCWF) and DoD 8140 qualification matrices

**Bottom line:** an explicit "TBD" state and qualification tied to function. The codes confuse people.

- **Framework.** 7 categories, 33 specialty areas and 54 work roles. Each role has a definition, tasks and KSAs, defined by "the work an individual is performing", not by title or series. The interactive DCWF Tool was not retrieved. [E]
- **Matrices.**
  - Each work role has Basic, Intermediate and Advanced options for education, training and certification.
  - A blank cell means no option at that level, though a higher-level option may apply. "TBD" means content "still being validated".
  - Each matrix carries its own update date (CS 2024-10-01, IT 2024-02-20, Cyber Enablers 2024-06-10). [E]
- **Published evidence (secondary).** A practitioner explainer (20 Oct 2026) says readers:
  - start from their own certificates instead of the position's work-role code;
  - miss additional roles;
  - misread the cascade between proficiency levels;
  - treat blank or TBD cells as acceptance.

  It also says a certificate in the workbook does not qualify someone for every role. [E]

Sources:
- https://dodcio.defense.gov/Cyber-Workforce/DCWF
- https://public.cyber.mil/cw/dcwf
- https://public.cyber.mil/wid/dod8140/qualifications-matrices
- https://cybersecjobs.com/how-to-read-the-dod-8140-qualification-matrices/

### 3.7 SFIA (Skills Framework for the Information Age)

**Bottom line:** the best treatment of levels, and the only public change-request register found. Its licence and accounts limit openness.

- **Entry points.**
  - Levels of responsibility: 1 Follow, 2 Assist, 3 Apply, 4 Enable, 5 Ensure/advise, 6 Initiate/influence, 7 Set strategy/inspire/mobilise.
  - An A–Z skills list with search by title, code, keyword and job title.
  - The full framework view (category, then subcategory, then skill and levels).
  - Quick-start "views" for cloud, cyber, AI and similar areas. [E]
- **Record design.**
  - SFIA 9 (October 2024) restructured skill pages, adding a responsibility-level explanation and an "essence" statement per level in collapsible accordions.
  - The rationale was user-driven. The A–Z list was "very popular", but scrolling it was time-consuming without the exact name, so a search was added. [E]
- **Correction loop.**
  - SFIA 10 is in consultation, with release tentatively between Q2 2027 and Q1 2028.
  - Anyone may submit a change request. Requests are listed as pending, accepted, resolved or deferred, can be linked from skill descriptions, and are judged by a global Design Authority.
  - Commenting needs a free account, and the list page itself asked for an account when fetched. [E]
- **Licence.** "All use of SFIA is under licence." It is free for personal and most internal use. Redistribution, copying framework content to other websites, and commercial use need a fee-bearing licence. [E]
- **Downloads.** Excel, PDF and RDF; the summary chart requires registration. [E]

Sources:
- https://www.sfia-online.org/en/framework
- https://sfia-online.org/en/sfia-9/responsibilities
- https://sfia-online.org/en/sfia-9/sfia-9-release-notes/making-sfia-easier-to-consume (modified 28 Oct 2024)
- https://sfia-online.org/en/sfia-10
- https://sfia-online.org/en/sfia-9/change-requests
- https://sfia-online.org/en/licensing-sfia

### 3.8 Singapore SkillsFuture Skills Frameworks

**Bottom line:** not directly observable. The pages returned only metadata (see §2). The findings below come from secondary and official documents.

- **Model.**
  - Sector frameworks cover career pathways, job roles and skills, including Technical Skills and Competencies (TSCs) with proficiency levels.
  - An official employer page frames the framework for HR design and skills investment.
  - A commercial explainer (22 Mar 2026) describes TSC levels 1–6, calls the PDFs "detailed but can be dense" and some TSC names "sometimes bureaucratic", and notes that many private employers use their own frameworks. [E, secondary and non-official]
- **Transitions.**
  - SSG's January 2025 Skills and Job Mobility Dashboard weighs five factors together: wage, demand level, demand growth, skills similarity and historical transitions between roles.
  - Its Skills Matrix plots demand against transferability, giving four quadrants. [E] I could not inspect the dashboard UI. [E]
- **Change since my knowledge.** The data.gov.sg course directory lists the publisher as "Skills and Workforce Development Agency (SWDA)". SSG's own news is still branded SSG. [E] This may indicate an agency merger in 2025–26. [S] An official SSG or MOM announcement would settle it.

Sources:
- https://skillsfuture.gov.sg/skills-framework/environmental-services (metadata only)
- https://skillsfuture.gobusiness.gov.sg/support-and-programmes/understand/skills-frameworks
- https://www.ssg.gov.sg/newsroom/ssg-launches-interactive-dashboards/ (22 Jan 2025)
- https://www.skillup.sg/blog/skills-framework-singapore
- https://data.gov.sg/datasets/d_b5802b76f409764c16dde4bf2feb19cd/view

### 3.9 Australia: Jobs and Skills Australia (JSA), the Australian Skills Classification (ASC) and the National Skills Taxonomy (NST)

**Bottom line:** honest about the limits of machine-learning drafts, but the product decayed. The consultation evidence is the most useful user evidence I found.

- **ASC model.**
  - 10 core competencies, each with a 10-point proficiency scale and a description per value.
  - Specialist tasks, grouped into clusters and families, and technology tools.
  - The last update was December 2023. The ASC is being decommissioned in favour of the NST and remains available "for research". [E]
- **Caveats at point of use** [E]:
  - Sharing a task "is not a measure of overall similarity or direct transferability".
  - Clusters ignore licensing.
  - The legacy explorer warns that the data is machine-learning output, "not validated by tripartite stakeholders", and that the transition model may find no strong matches.
  - The explorer requires signing a Data Access Agreement each session. When fetched, it was stuck at 0% loading.
- **Correction loop.** In 2023, JSA released 21 draft occupation profiles as per-occupation Excel files for comment by email. It was the first time drafts were opened before publication. [E]
- **Published evidence.** The NST consultation summary (6 Nov 2024; 68 submissions, 45 interviews, 367 workshop attendees) found [E]:
  - Usability and adoption problems recur. Taxonomies are "hard to understand and navigate", including for careers counsellors.
  - People want simple language and an intuitive interface.
  - Trust in career platforms is low, and there were past concerns about ASC accuracy.
  - Targeted updates should be "clearly labelled as not full updates".
  - Most employers and educators oppose taxonomy-defined proficiency.
  - People ask for drill-down browse, a table builder, separate general and technical access points, APIs and a glossary.
  - AI may confuse new tools with new skills.

Sources:
- https://jobsandskills.gov.au/data/australian-skills-classification
- https://www.jobsandskills.gov.au/legacy/658583848265767365788375737676836776658383737073676584737978
- https://www.jobsandskills.gov.au/consultations/draft-australian-skills-classification-occupation-profiles (2023)
- https://jobsandskills.gov.au/consultations/australian-skills-classification-user-survey
- https://jobsandskills.gov.au/sites/default/files/2024-11/nst_consultation_summary.pdf
- https://www.jobsandskills.gov.au/data/national-skills-taxonomy
- https://www.jobsandskills.gov.au/news/explore-australias-occupations-new-osca-occupation-profiles

### 3.10 Canada: OaSIS and NOC (ESDC)

**Bottom line:** strong version handling. Its scales are borrowed from O\*NET and its rating guide is not public.

- **Entry points.**
  - OaSIS: search by keyword, by code, or by category and descriptor; advanced multi-descriptor search; A–Z browse.
  - "Skills Match" finds occupations similar in skills and abilities.
  - A version selector offers 2025, 2023 and 2022, each "Version 1.0". [E]
  - NOC's Comparative search compares up to three structure items across NOC 2021, 2016, 2011 and 2006, in English or French. [E]
- **Method transparency** [E]:
  - Initial ratings were imported from O\*NET, and its 7-point scale was converted to 5 points case by case.
  - Importance was replaced by a hidden yes/no "applicability".
  - Later revisions use only Canadian sources.
  - The Canadian Rating Guide that explains each level is not published (contact ESDC).
  - Skills Match thresholds are described only as "adequate".
- **Accessibility.** The site is bilingual. No more could be observed. [E]

Sources:
- https://noc.esdc.gc.ca/Oasis/OasisWelcome
- https://noc.esdc.gc.ca/OASIS/OASISMethodology
- https://noc.esdc.gc.ca/Oasis/OasisVersions
- https://noc.esdc.gc.ca/Compare/ComparativeSearch

### 3.11 Lightcast Open Skills

**Bottom line:** fast-moving and data-driven. Record pages are dense with upsell and carry no record-level version or licence.

- **Information architecture.** Category, then subcategory, then skill (about 32–33k skills). Types are Specialized, Common, and Certification/License. Each skill has aliases for extraction. [E]
- **Record page** ("Open Educational Resources") [E]:
  - Tabs: About, Related Titles, Related Occupations, Job Postings, API Access.
  - Related skills are stated to be "based on the last 5 months of job postings data". This is a good provenance note.
  - No version, date or licence appears on the page.
  - Calls to action include "Speak with a Data Pro", a demo, a newsletter, and "summarize in ChatGPT, Claude, Perplexity" buttons. Some content is duplicated.
- **Provenance and versioning.**
  - The developer docs say most definitions are "generated by AI and curated by in-house taxonomists". The public FAQ instead says most definitions link to Wikipedia (CC BY-SA). [E]
  - Release cadence is described as every two weeks on one page and monthly on another. There is a public changelog and a suggestion form. [E]
- **Licence.** Free use with attribution under the terms. Full API access is by contract. [E]

Sources:
- https://lightcast.io/open-skills/skills/ESF1E0AEB19D24A227F7/open-educational-resources
- https://lightcast.io/open-skills/faqs
- https://skills.lightcast.io/faqs
- https://docs.lightcast.io/lightcast-api/docs/general-taxonomies-skills

### 3.12 Open Skills Network (OSN), OSMT and Rich Skill Descriptors (RSDs)

**Bottom line:** a good data model for provenance and alignment. Its public home is decaying.

- **RSD model** [E]:
  - A canonical URL as identity.
  - A skill statement written as {Subject}{Predicate}{Context}.
  - Fields for category, keywords, occupations, employers and certifications.
  - Alignments typed as exact, major (the default, meaning close but not exact), broad, minor, narrow and prerequisite.
  - Author, creator, derivedFrom, licence, and lastChangeDateTime.

  Status values and verification are not in the description I could read. [E]
- **Stewardship.** In February 2025, WGU announced that OSMT and RSDs are moving to Credential Engine. [E] On 30 Oct 2026, openskillsnetwork.org/about redirected (302) to an unrelated commercial domain. [E] This suggests the domain has lapsed or been repurposed. [S] A WHOIS check or an OSN or Credential Engine statement would settle it.
- **Usability evidence.** One OSMT GitHub issue (Mar 2023) reports that publishing to the Credential Registry is manual: export, reformat as CSV, upload. [E]

Sources:
- https://rsd.openskillsnetwork.org
- https://wgu.edu/blog/strengthening-our-commitment-to-skills-based-future2502.html (4 Feb 2025)
- https://github.com/wgu-opensource/osmt/issues/346
- https://www.openskillsnetwork.org/about (redirect observed, not followed)

### 3.13 Credential Engine (Credential Finder, CTDL)

**Bottom line:** raw data is exposed behind every page, but coverage is uneven and only a subset can be exported.

- Credential Finder searches Registry data. Each detail page has a JSON-LD icon that shows the raw Registry record. Users can build, download and share comparisons, and embeddable widgets are available. [E] I did not retrieve the application itself.
- CSV export "provides only a subset of key information". Full CTDL needs a Registry account. The export guidance names the site inconsistently (credentiafinder.org, credentialfinder.com, credentialfinder.org). [E]
- CTDL-ASN describes competencies. O\*NET now publishes its frameworks in it (§3.1). [E]
- The Counting Credentials 2025 report (December 2025) counts about 1.85M credentials and says many counts are estimates. It does not report Registry coverage. [E]

Sources:
- https://credentialengine.org/develop-solutions/credential-finder/
- https://guidance.credentialengine.org/credential-finder-export-instructions/ (9 Apr 2024)
- https://credentialengine.org/credential-transparency/ctdl/
- https://credentialengine.org/resources/open-skills-and-rich-skill-descriptors-ctdl-enables-connections-and-collaboration/
- https://credentialengine.org/wp-content/uploads/2025/12/Counting-Credentials-2025-Report.pdf

### 3.14 UK National Careers Service (England)

**Bottom line:** GOV.UK patterns used well, plain-language profiles, and the best published satisfaction data. The website lags human channels badly.

- **Information architecture.** Explore careers, then job sector, then a list of profiles ("Showing 21 to 40 of 68"). Each list entry shows title, alternative titles, a one-line description, a salary range and "Found in" sectors. There are no filters. [E]
- **GOV.UK cues** [E]:
  - skip link and cookie banner;
  - a "Beta" phase banner with "How could we improve this service?";
  - breadcrumbs;
  - "Is this page useful?";
  - Open Government Licence.
- **Record page** (Ecologist) [E]:
  - Salary, hours and when you could work.
  - How to become: university, apprenticeship (Level 7), volunteering, professional body.
  - What it takes (skills); What you'll do; Career path and progression.
  - Current opportunities: live courses, and "no apprenticeships found".
  - A "green job" flag.
  - No last-updated date and no per-profile sources, only a site-wide "Information sources".
- **Published evidence** [E]:
  - Year 13 (2023–24): 54% of 501 website users were satisfied (down from 63%), against 86% for phone and face-to-face. Explore Careers was rated useful by 92% of its users.
  - Digital First Careers alpha (Jan 2017):
    - many profiles were outdated, with no strategy to maintain and verify them;
    - search had not been tested;
    - users could not browse between profiles;
    - everyone was pushed into building a skills profile, which could hold sensitive data.
  - Get Help to Retrain beta (Nov 2019):
    - pre-filled skill checkboxes helped users rethink their skills;
    - the panel asked that job matches show market size and growth;
    - "apprenticeships" put users off;
    - keyboard and ARIA issues were found.

Sources:
- https://nationalcareers.service.gov.uk/explore-careers/job-sector/agriculture-environment-and-animal-care/view-all-sector-careers?page=2
- https://nationalcareers.service.gov.uk/job-profiles/ecologist
- https://assets.publishing.service.gov.uk/media/6717b451d94d2c219a54058a/National_Careers_Service_Customer_Sat_and_Prog_Annual_Report_Year_13.pdf
- https://www.gov.uk/service-standard-reports/digital-first-careers-alpha-assessment
- https://www.gov.uk/service-standard-reports/get-help-to-retrain-beta-assessment-report

### 3.15 Skills England occupational maps (formerly IfATE)

**Bottom line:** the clearest status-on-every-record design found.

- **Entry points.**
  - 15 routes.
  - Search by occupation name, standard code, product, job title or keyword.
  - Progression maps.
  - Green theme maps.
  - "My Maps", which needs login. [E]
- **Record page** (Agricultural engineer, OCC1247) [E]:
  - Route, Level 6, print to PDF, share.
  - A status label with an icon and an explanation: "Potential occupational standard" means a route panel has identified a need but no group has formed yet.
  - A contact address for helping develop the standard.
  - The status key covers Potential, In development, Approved, Without apprenticeship, and Custom.
  - No SOC code appears on the page, although the API exposes it.
- **Data access.** Public API (/api/v1/) with a key, under the Open Government Licence. It requires a Skills England logo and attribution. Expansions include knowledge, skills and behaviours (KSBs), duties, and the links between duties and KSBs. [E]
- **Accessibility.** An accessibility statement is linked. No list alternative to the visual maps is described. [E]

Sources:
- https://occupational-maps.skillsengland.education.gov.uk/
- https://occupational-maps.skillsengland.education.gov.uk/maps/occupation/OCC1247
- https://occupational-maps.skillsengland.education.gov.uk/public-api/

### 3.16 OPM classification standards and the Handbook of Occupational Groups and Families

**Bottom line:** authoritative but PDF-bound and slow to change. 2026 consolidation makes "as of" dating essential.

- **Handbook** (December 2018 PDF) [E]:
  - Groups, then four-digit series, each with a narrative definition and exclusion cross-references.
  - Asterisks mark the type of standard: 0401, 0408, 0454 and 0460 have job family standards; 0455 and 0462 are flysheets.
  - It "does not provide grading criteria".
- **0401 qualification standard (HTML).**
  - Basic requirements and pilot duties; skip links.
  - No last-updated date.
  - The text refers to "A above", but no item A appears on the page. [E]
- **GS-0456 Wildland Fire Management** standard: issued June 2022, with DOI interpretive guidance in March 2023 using factor-level descriptions and benchmarks. [E]
- **Change.** OPM memo of 24 Apr 2026 [E]:
  - proposes consolidating 115 series affecting about 4,926 employees;
  - 0455 Range Technician moves to 0404, and 0029 moves to 0303;
  - 0401 receives several series;
  - updated standards follow through September 2027.

  A third-party blog turned it into "RIF risk" labels within two days. [E]

Sources:
- https://www.opm.gov/fedclass/gshbkocc.pdf
- https://opm.gov/policy-data-oversight/classification-qualifications/general-schedule-qualification-standards/0400/general-natural-resources-management-and-biological-sciences-series-0401
- https://www.doi.gov/sites/doi.gov/files/wildland-fire-management-pcs-interpretive-guidance-final-march-2023-508.pdf
- https://www.opm.gov/chcoc/latest-memos/modernization-and-consolidation-of-occupational-series.pdf
- https://www.fedtools.com/blog/opm-job-series-consolidation-rif-impact-2026

### 3.17 NWCG position catalog, PMS 310-1 and IQCS

**Bottom line:** familiar vocabulary for fire users, with an excellent change log and explicit "None" values. Date fields are left empty.

- **Catalog.** 116 positions. An "IPD Status" column shows which are under review. Asterisks mark positions based on FEMA all-hazard positions. [E]
- **Position page** (FFT2, Operations) [E]:
  - Description and supervisor.
  - Qualification requirements as labelled fields: Required Training (RT-130 after year 1), Required Experience: None, Physical Fitness: Arduous, Other Training: None.
  - Two currency fields, both "None".
  - Dated history: IPD approved May 2019; task book replaced by a job aid May 2008; position created October 1993.
  - "Last Modified / Reviewed" is present but blank.
- **Position history by year.** Each entry has a date, title, code, functional area and change summary (training added or removed, renamed, archived), with a Current or Archived filter, back to at least 2018. [E]
- **PMS 310-1.**
  - Moved from PDF to HTML in October 2020, with a Print PDF option.
  - Revised every year, usually in the third week of January (2026 updates dated 23 Jan 2026).
  - It states "previous versions are obsolete".
  - Agencies may add requirements, but these "may not be imposed upon cooperating agency personnel". [E]
- **IQCS** is an account-based records system and was not examined. [J] It is not a public browsing model.

Sources:
- https://www.nwcg.gov/positions/position-catalog?page=1
- https://www.nwcg.gov/positions/firefighter-type-2-crewmember
- https://www.nwcg.gov/positions/fft2/qualification-requirements
- https://www.nwcg.gov/positions/position-history-by-year
- https://www.nwcg.gov/publications/pms310-1/nwcg-standards-for-wildland-fire-position-qualifications-pms-310-1
- https://www.nwcg.gov/announcement/publications/2026-updates-to-the-nwcg-standards-for-wildland-fire-position-qualifications-pms-310-1

### 3.18 Additional strong examples: Skosmos (AGROVOC) and the GOV.UK and Scottish design systems

- **Skosmos 2.18** (AGROVOC concept page) [E]:
  - Alphabetical, hierarchical and grouped browse.
  - Breadcrumb hierarchy.
  - Content-language search across about 45 languages.
  - The concept URI shown as plain text.
  - Per-concept RDF/XML, Turtle and JSON-LD.
  - Created and modified dates per label. These dates conflicted with the footer date on the page fetched.

  Skosmos 3 (2025) reimplemented the front end "with enhanced responsiveness and accessibility". A community customisation shows a version timeline for each concept. [E]
- **GOV.UK Design System** [E]:
  - The phase banner belongs in the header on every page, paired with the Feedback component (updated July 2026).
  - The "Trial" lifecycle tag: research found users understood it and valued knowing which components were in progress. This is the only direct evidence I found that a status tag is understood.
- **Scottish Government status tag** [E]:
  - short adjective labels in sentence case;
  - the fewest tags possible;
  - colour never the only signal;
  - the same colour for the same status across the service;
  - meets WCAG 2.2 contrast (guidance updated 14 Jan 2025).

Sources:
- https://agrovoc.fao.org/browse/agrovoc/en/page/c_1370613252955
- https://forum.swib.org/t/from-chaos-to-skosmos-publishing-controlled-vocabularies-made-easy/1454
- https://design-system.service.gov.uk/components/phase-banner
- https://design-system.service.gov.uk/community/component-lifecycle-statuses/
- https://designsystem.gov.scot/components/status-tag

### 3.19 Cautionary: third-party re-presentations of open taxonomies

- **WorldOfTaxonomy** re-publishes ESCO records [E]:
  - It shows "equivalent and related codes" with no match type and no licence.
  - An unexplained "Level 11 cross-system mapping" label.
  - A hierarchy breadcrumb that repeats an entry.
- **Nestorbot** builds "AI-powered career" pages from ESCO [E]:
  - an AI replacement-risk score ("17/100") with no stated source;
  - a 3-level self-rating.
- **The fedtools blog** turned OPM's consolidation memo into "consolidation risk" labels for RIF planning within two days. [E]

Implication [J]: once EMST data is downloaded, its caveats travel only if they are in the data itself. EMST's open licence makes such re-presentation likely.

Sources:
- https://worldoftaxonomy.com/codes/esco_occupations/e3cc09ba-7ad5-4411-940c-20613000863a
- https://nestorbot.vercel.app/explore/occupations/forest-ranger
- https://www.fedtools.com/blog/opm-job-series-consolidation-rif-impact-2026

---

## 4. Synthesis 1: pattern table

**Evidence strength:**
- **Strong:** published user research or evaluation.
- **Moderate:** documented design rationale, consultation findings, or long-running practice with stated reasons.
- **Weak:** feature observed only.

**User groups:**
- U1: NGO and conservation-corps programme and training leads
- U2: early-career staff and corps members
- U3: supervisors and crew leads
- U4: state training, curriculum, HR and classification staff
- U5: federal HR, classifiers, training officers, workforce planners
- U6: workforce boards, educators, curriculum designers
- U7: researchers, data users and developers
- U8: career changers and job seekers from outside the sector
- U9: practitioners and subject-matter experts who review and correct

| # | Pattern | Best example (URL) | Evidence strength | Most relevant to |
|---|---|---|---|---|
| P1 | Per-record "data sources" page: each block labelled with year and rater type, including AI | My Next Move data page: mynextmove.org/vets/help/data/19-4071.00 | Weak (observed). ESCO users asked for clearer provenance (Moderate) | U5, U4, U7, U9 |
| P2 | Lifecycle status on every record, icon plus words, with a public key | Skills England: occupational-maps.skillsengland.education.gov.uk/maps/occupation/OCC1247 | Moderate. GOV.UK found users understood a "trial" tag | All |
| P3 | Explicit "still being validated" state in place of a value (TBD, None) | DoD 8140 matrices: public.cyber.mil/wid/dod8140/qualifications-matrices; NWCG FFT2 | Weak. The 2026 explainer shows users misread blanks and TBD | U5, U3, U4 |
| P4 | Summary first: top 5 plus "N of M" plus Show all; Details and Custom views | O\*NET Summary: onetonline.org/link/summary/19-1031.03 | Weak to moderate (long practice) | U3, U4, U5, U6 |
| P5 | Plain-language twin view: no scores, ratings in words ("2 of 4"), printable with a name | My Next Move: MyNextMove.org/profile/summary/19-4071.00 | Weak. Supported by NST "simple language" (Moderate) | U2, U8, U1 |
| P6 | "Why did this match?" on search results | O\*NET: ONetOnline.org/help/online/search | Weak | U8, U2, U4 |
| P7 | Ratings as respondent distributions in words ("82% responded...") | O\*NET Work Context | Weak | U5, U7 (later, once gates pass) |
| P8 | Borrowed or chained data openly labelled ("data for Conservation Scientists") | O\*NET wage block | Weak | U5, U7 |
| P9 | Dated per-record change history, filterable by Current or Archived | NWCG: nwcg.gov/positions/position-history-by-year | Moderate (annual cycle) | U3, U5, U7, U9 |
| P10 | Version selector, delta file, API version parameter, "Obsolete" status | ESCO: esco.ec.europa.eu/en/classification/skill | Moderate | U7, U4, U6 |
| P11 | Release change summary listing removed and replaced IDs | NICE 2.2.0 summary (nist.gov) | Moderate | U7, U5 |
| P12 | Public change-request register with statuses, linked from records | SFIA: sfia-online.org/en/sfia-10 | Moderate (stated process) | U9, U1 |
| P13 | Draft records released for comment before publication | JSA draft profiles (2023) | Moderate | U9, U1, U3 |
| P14 | Caveat placed at the point of comparison ("not a measure of ... transferability") | JSA ASC: jobsandskills.gov.au/data/australian-skills-classification | Moderate | U8, U2, U6 |
| P15 | Multi-factor transitions (wage, demand, growth, similarity, historical moves) instead of one score | SSG mobility dashboard (Jan 2025) | Weak (not inspected) | U8, U2, U6 |
| P16 | Job matches show the size and trend of the job market | GOV.UK Get Help to Retrain beta (2019) | Strong (assessment panel) | U8, U6 |
| P17 | Levels as named verbs plus an "essence" statement in accordions | SFIA 9: sfia-online.org/en/sfia-9/responsibilities | Moderate (user-driven redesign) | U3, U4, U6, U2 |
| P18 | Function, not title: "work roles are not job titles" | NICCS work-role page; DCWF | Weak | U5, U4 |
| P19 | Cite this page, CC BY 4.0, RDF/JSON/CSV, CTDL-ASN | O\*NET; onetcenter.org/competencyFrameworks.html | Moderate (6,700+ web-service users) | U7, U6 |
| P20 | Concept URI plus per-concept RDF/Turtle/JSON-LD; multilingual browse | Skosmos/AGROVOC | Moderate (mature open source) | U7 |
| P21 | Phase banner plus feedback on every page | GOV.UK Design System; NCS | Moderate | All, especially U9 |
| P22 | Hedged language for matches ("may be a good match", "likely gaps") | mySkills myFuture brochure | Weak | U8, U2 |
| P23 | Agency-variation rule stated ("may not be imposed upon cooperating agency personnel") | NWCG PMS 310-1 | Weak | U3, U5, U4 |

---

## 5. Synthesis 2: anti-patterns, with evidence

Details and sources are in the site sections cited.

1. **Audience-first or tool-first home pages** (CareerOneStop, ESCO) [E §3.3, 3.4].
   - A GOV.UK alpha found the scope "unclear" and everyone pushed into one flow [E §3.14].
   - [J] U5 and U8 may want the same role page, so a role-first entry is safer. [S] A first-click test would settle it.
2. **Code-first or jargon labels.**
   - DoD 8140 users start from certificates, not codes [E §3.6].
   - ESCO labels are too long [E §3.4].
   - EMST's footer shows "`agentDraft` sub-object", "raterType" and "OBS-4" on every page [E repo: /home/claude/emst/site/_site/index.html].
3. **Unexplained precise scores.**
   - Nestorbot's "17/100" AI risk; ASC's 10-point scale; OaSIS's hidden 7-to-5 point conversion; Skills Matcher's unexplained ranking [E §3.19, 3.9, 3.10, 3.3].
   - EMST prints "confidence 0.5" on unreviewed AI crosswalk rows [E repo: /home/claude/emst/site/_site/roles/rol-0014znd/index.html].
4. **Over-promising military translators.** My Next Move for Veterans matches with no strength, basis, caveat or date [E §3.2]. [J] EMST's seasonal-fire pathways for U8 face the same risk.
5. **Version skew across official surfaces** (NICE 2.2.0 against 2.0.0 against "v1.0.0") [E §3.5].
6. **Hidden basis for computed relationships** (O\*NET related occupations; the NICE galaxy) [E §3.1, 3.5]. Lightcast at least names the basis, "last 5 months of job postings" [E §3.11].
7. **Empty or conflicting dates.** NWCG blank field; AGROVOC conflicting dates; NOC Compare stamped 2019 while offering NOC 2021; undated NCS profiles [E §3.17, 3.18, 3.10, 3.14].
8. **Gated or decaying access.** ASC agreement; SFIA accounts; Credential Finder accounts; OSN domain [E §3.9, 3.7, 3.13, 3.12].
9. **Hover-only or visual-only exploration.** The NICE galaxy; occupational maps with no list view described [E §3.5, 3.15]. [J] This breaks EMST's own "nothing hover-only" release gate.
10. **Upsell-dense record pages** (Lightcast) [E §3.11].
11. **Caveats that do not travel with the data.** WorldOfTaxonomy; Nestorbot; classification data recast as RIF risk [E §3.19].
12. **Contradictory parallel lists on one record.** My Next Move shows two different "Also called" lists [E §3.2].

---

## 6. Synthesis 3: white space that EMST must fill anyway

| Need (from EMST constraints) | Closest precedent | What is missing everywhere | Basis |
|---|---|---|---|
| **AI-drafted, unreviewed status per record** | O\*NET labels "(ai/sme)" by category on a sub-page; Lightcast mentions AI definitions in its docs; the ASC banner says "ML output ... not validated" | Record-level review status shown on the record, and saying in plain words who has and has not checked it | [E] §3.1, 3.2, 3.9, 3.11 |
| **Use-tier limits** ("OK for curriculum mapping; not for hiring") | SFIA licences by type of use; DoD 8140 ties roles to qualification; the OPM Handbook "does not provide grading criteria" | No benchmark says per record what it is fit for | [E] §3.6, 3.7, 3.16 |
| **"Assessment pending" in place of values** | DoD "TBD"; NWCG "None"; O\*NET simply omits | A consistent, explained withheld-value state, with a reason and what would change it | [E] §3.6, 3.17 |
| **Crosswalk match strength and review status in the UI** | RSD alignment types in the data model; ESCO crosswalk files; O\*NET military lists | Plain-language match type plus review state on the record, without false precision | [E] §3.4, 3.12, 3.2 |
| **Contested values** | The NICE workshop (5 versus 3 tiers) and NST (proficiency opposed) record disagreement in reports only | Showing on the record that experts disagree, and about what | [E] §3.5, 3.9 |
| **A visible correction loop** | SFIA register (account); JSA spreadsheets by email; ESCO invitation-only fora; Lightcast form; NICE email | Per-record "open corrections" and "what changed because of feedback", public without an account to read | [E] §3.4, 3.7, 3.9, 3.11 |
| **Variation by employer type** | NWCG: agency additions "may not be imposed" on cooperators | Side-by-side variants of the same task by federal, state, NGO or private employer | [E] §3.17; [J] |
| **A held-content (consent) boundary** | None found | A respectful count-only statement pattern | [E] absence. I found no precedent among the sites reviewed |
| **Self-assessment with no account** | Skills Matcher (saving unclear); the NCS alpha warned that skills profiles hold sensitive data | A file-only, local result | [E] §3.3, 3.14 |
| **Foresight with honest uncertainty** | O\*NET "Bright Outlook" (binary); SSG forecasts | Change signals with an evidence grade and a "watch" state | [E] §3.1, 3.8 |
| **"As of" for external reference data** | ESCO version stamp; NWCG annual cycle | Per-record dating of borrowed OPM, O\*NET or state data. This is urgent given the 2026 OPM consolidation and O\*NET Job Zone changes | [E] §3.16, 3.1 |

---

## 7. Ten recommendations for EMST's interface

1. **Add a one-line provenance statement to every record, linked to a "Where this came from" drawer modelled on My Next Move's data page.**
   - Example line: "Drafted by AI agents, Oct 2026 · Not yet reviewed by a practitioner · v1 analyst values: in evidence drawer, not for decisions."
   - The drawer lists each field group with drafter type, date and gate status.
   - Evidence: P1 [E §3.2], ESCO's provenance feedback [E §3.4], NST trust concerns [E §3.9].
2. **Adopt one small set of text-plus-icon status tags, used identically everywhere, with a public key page.**
   - Candidates: "AI draft · not reviewed", "Assessment pending", "Unreviewed match", "Held", "Watch".
   - Follow the Scottish status-tag rules: few tags, adjectives, colour never alone, WCAG 2.2 contrast.
   - Evidence: Skills England's status key [E §3.15], the GOV.UK trial-tag research [E §3.18].
   - [S] Comprehension testing of the five labels with U1 and U5 would settle the wording.
3. **Say what each record can be used for, in "OK for / Not for" form beside the use-tier badge.**
   - Example: "OK for: workforce planning, curriculum mapping. Not for: hiring, classification, RIF or ratings."
   - Replace the long technical footer with a GOV.UK-style phase banner plus a "How to read EMST" link.
   - Evidence: the white space in §6; the phase banner pattern [E §3.18]; NST "simple language" [E §3.9]; the current EMST footer jargon [E repo].
4. **Make search title-first and explain matches.**
   - Search should cover alternative titles, tasks and competencies.
   - Show "Why this matched", with matched alternative titles and tasks highlighted, as O\*NET does.
   - Show codes as secondary metadata.
   - Evidence: P6 [E §3.1]; code-first confusion [E §3.6]; the NCS alpha found search untested [E §3.14].
   - [J] Because EMST search runs locally, this is cheap to compute at build time.
5. **Make record pages summary-first with honest empty states.**
   - Show the top 5 tasks with "Show all 28".
   - Put proficiency levels in accordions with an "essence" line for each L1–L5.
   - Where a value is gated, show "Assessment pending: needs a reliability study" with a link. Never leave a blank cell or field.
   - Evidence: P4 [E §3.1], P17 [E §3.7], P3 [E §3.6, 3.17], and the empty-date anti-pattern [E §3.17].
6. **Redesign crosswalk rows: plain match type plus review state, no decimals.**
   - Replace "broader term, confidence 0.5" with, for example, "Broader category (AI-suggested, not reviewed)".
   - Keep numeric confidences in the downloads, not on the page.
   - Under each crosswalk table, add an ASC-style caveat: "A shared code is not evidence the jobs are equivalent."
   - Evidence: anti-pattern 3 [E repo, §3.19]; P14 [E §3.9]; RSD alignment vocabulary [E §3.12].
7. **Build pathways and "where it can lead" as multi-factor, caveated and text-first.**
   - Show shared competencies, known frictions (licences, fitness, credentials), and labour-market context where it is available.
   - Show no single match percentage.
   - Treat any military or seasonal-fire translator as a starting point, with its minimum basis stated.
   - Give every visual a list or table equivalent, as the release gate already requires.
   - Evidence: anti-patterns 4 and 9 [E §3.2, 3.5]; P15 and P16 [E §3.8, 3.14]; P22 [E §3.3].
8. **Date everything and keep a per-record history.**
   - Each record shows release, first published, last changed, and the "as of" dates of borrowed OPM, O\*NET or state data.
   - A change-log page lists added, retired and replaced IDs, modelled on NWCG and NICE.
   - Flag OPM series records affected by the April 2026 consolidation proposal, for example 0455 to 0404, as "OPM has proposed changes; check current status".
   - Evidence: P9 and P11 [E §3.17, 3.5]; version skew [E §3.5]; the OPM memo [E §3.16].
9. **Make the correction loop visible on the record.**
   - Next to "Report a problem", show a copyable citation block (record ID plus release ID). This is needed because the build forbids query strings on external links, so GitHub issue forms cannot be pre-filled. [E repo README]
   - Publish a static "Corrections register" page, generated at release time from repository issues and grouped by status (open, accepted, declined, deferred), as SFIA does.
   - On each record, show "N open corrections" when there are any.
   - Evidence: P12 and P13 [E §3.7, 3.9]; the closed loops in §6.
   - [S] Whether U9 practitioners will use GitHub at all is untested. A pilot with U1 would settle it.
10. **Make data access and citation carry the caveats.**
    - Every record gets a "Cite this record" line (persistent ID, release, date, licence) and per-record JSON-LD and SKOS links, as Skosmos does.
    - Include use tier, review status and gate status as fields in every CSV and JSON row, so re-publishers inherit them.
    - Give an explicit "do not use for" statement in the licence notes.
    - Evidence: P19 and P20 [E §3.1, 3.18]; anti-pattern 11 (re-presentations that strip caveats) [E §3.19].

---

## 8. Open questions that this desk research cannot settle

- [S] Do U1 and U5 users notice and correctly interpret a status tag such as "AI draft · not reviewed"? A 5-second test and a comprehension test would settle it.
- [S] Does a role-first home page outperform an audience picker for U5 and U8? A first-click test would settle it.
- [S] Would U9 practitioners file corrections on GitHub, or does account friction (SFIA, Credential Engine precedent) suppress them? Pilot metrics from U1 partners would settle it.
- [S] Has Singapore's skills agency been merged or renamed (the SWDA publisher label)? An official source would settle it.
- [S] Has the openskillsnetwork.org domain lapsed? A Credential Engine or OSN statement would settle it.
- [S] What are OPM's final consolidation decisions after May 2026? The OPM final list would settle it.
