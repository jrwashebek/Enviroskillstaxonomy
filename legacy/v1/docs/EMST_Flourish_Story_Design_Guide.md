# EMST Flourish Story — Design Guide
**Environmental Management Skills Taxonomy | March 2026**
*Source data: EMST_Flourish_Data_Package.xlsx*

---

## Story Architecture

The story moves from **scope → structure → disruption → risk → reach**. Each slide answers one question a funder or policy audience would naturally ask in sequence. The headline on every slide should carry the argument — not describe what the chart shows, but state what it means.

**Suggested Story title:** *"222 Competencies, Two Disruption Pressures, One Infrastructure"*

---

## Slide 1 — What Was Built
**Sheet:** `S1_Scope` | **Template:** Bar chart (horizontal)
**Headline:** *"222 competencies across 7 domains of environmental management work"*

**Configuration:**
- X-axis: Competencies (numeric)
- Y-axis: Domain (label)
- Sort: by count, descending
- Color: single forest green (#2D6A4F)
- Add a subtitle annotation: "Based on Society of American Foresters–accredited competency standards, validated against OPM and O*NET classification systems"

**Design note:** This slide establishes legitimacy and scope. Keep it clean — no secondary encoding. The point is simply to show the breadth of what was built. Resist adding color coding here; that comes in subsequent slides.

---

## Slide 2 — Three Professional Crafts
**Sheet:** `S2_Craft_by_Domain` | **Template:** Stacked bar (100% normalized)
**Headline:** *"42% of environmental management competencies are Statecraft — the profession is more governance than fieldwork"*

**Configuration:**
- Stack: FC (Fieldcraft), DC (Datacraft), SC (Statecraft) as three segments
- 100% normalized view
- Colors: FC = deep green (#386641), DC = steel blue (#457B9D), SC = amber (#D4A017)
- Label each segment with percentage
- Sort rows: Domain order D1→D7

**Annotation to add:** Flag D1 (Ecological & Scientific Knowledge) as the most Fieldcraft-dominant domain. Flag D6 (Policy & Regulatory) as the most Statecraft-dominant.

**Story rationale:** This is the first structural surprise for most audiences. The assumption is that environmental management is fieldwork; the data shows it is primarily governance and communication. This reframes what "workforce disruption" means — it's not just about field technology but about administrative and regulatory capacity.

---

## Slide 3 — The Jagged Disruption Finding
**Sheet:** `S3_AutoType_by_Domain` | **Template:** Stacked bar (absolute counts)
**Headline:** *"AI disruption is jagged — no domain disrupts uniformly, and 38% of competencies remain Human-Essential"*

**Configuration:**
- Stack order (top to bottom of each bar): H, Ac, V, S, A
- Colors:
  - H (Human-Essential): deep green (#1B4332)
  - Ac (Compressive Augmentation): amber (#D4A017)
  - V (Supervised Automation): steel blue (#457B9D)
  - S (Substitution): red-orange (#E63946)
  - A (Augmentation / lower disruption): light sage (#95D5B2)
- Show absolute counts, not percentages
- Annotate: "D6 is the only domain with both Substitution-level tasks AND high Human-Essential counts"
- Annotate: "D7 (Cross-Cutting Practice): all 7 competencies are Human-Essential — these are the governance mechanisms for AI itself"

**⚠ Data caveat note:** Pre-Task 15A reclassification (12 A→Ac changes in D6) is analytically complete but not yet integrated into V3. Current chart shows D6 Ac=0; correct value is Ac=12. Integrate before using externally.

**Story rationale:** This is the core empirical finding. "Jagged disruption" is more accurate than "AI will replace environmental managers" — and more useful for workforce planning because it localizes risk to specific competencies rather than entire professions.

---

## Slide 4 — Policy Reform Exposure
**Sheet:** `S4_Reform_Flags` (bar) + `S4b_Reform_by_Domain` (stacked, secondary)
**Template:** Horizontal bar chart for S4; stacked bar for S4b
**Headline:** *"58% of competencies carry policy reform sensitivity flags — the regulatory environment is a second disruption layer"*

**S4 configuration:**
- X: Competencies Affected
- Y: Reform Category (sorted by count)
- Color: single coral/orange (#E76F51) to distinguish from the AI/automation palette
- Call out Digital Permitting (66 competencies) as the most pervasive vector

**S4b configuration (use as a follow-on panel or tooltip extension):**
- Stacked by domain, reform codes as stack segments
- Use to show D6 carries the highest reform load (36 flagged competencies)

**Story rationale:** Most workforce disruption analyses focus only on AI/automation. The reform sensitivity layer is distinctive to this taxonomy — it captures the policy environment in which practitioners operate, not just the technology environment. For EPIC's audience, this is the most directly actionable finding.

---

## Slide 5 — Career Ladder Disruption
**Sheet:** `S5_CLD_Severity` | **Template:** Donut chart or horizontal bar
**Headline:** *"AI is hollowing out entry-level pathways, not eliminating senior roles — 22% of competencies show Career Ladder Disruption signals"*

**Configuration:**
- Segments: High (9), Moderate (25), Low (15), No Signal (173)
- Colors: High = red (#E63946), Moderate = amber (#D4A017), Low = light yellow (#FFD60A), No Signal = light gray (#CED4DA)
- If using donut: emphasize the 49 CLD-flagged competencies as a callout number in the center
- Annotation: "All CLD signals are concentrated at entry-level (P-position) rather than senior roles — AI compresses developmental pathways before practitioners build tacit knowledge"

**Story rationale:** This finding reframes the public narrative about AI and jobs. It's not "AI takes senior jobs" — it's "AI removes the rungs that produce senior practitioners." This is the career pipeline argument and is particularly relevant for agency workforce planners.

---

## Slide 6 — Who the Taxonomy Serves
**Sheet:** `S6_Profession_Family` | **Template:** Grouped bar or scatter
**Headline:** *"15 profession families — from Forestry to Conservation Finance — share a common competency infrastructure"*

**Configuration:**
- Option A (grouped bar): X = Profession Family, two bars per family (Core, Supporting)
- Option B (scatter/bubble): X = Core count, Y = Supporting count, size = Total Reach, label = Family name
- Sort by Total Reach (Core + Supporting), descending
- Colors: Core = deep green, Supporting = lighter green
- Annotate: "F5 (Conservation Science) and F8 (Environmental Policy) have the broadest supporting reach"

**Story rationale:** This slide answers "who benefits?" — important for funder audiences who want to see that the investment serves a wide professional ecosystem, not a single specialty.

---

## Slide 7 — Workflow Stage Distribution
**Sheet:** `S7_Workflow_Stage` | **Template:** Bar chart (vertical) or lollipop
**Headline:** *"Half of environmental management competencies live at the Planning & Assessment stage — the profession's upstream work is its most at-risk"*

**Configuration:**
- X: Stage (S1–S6)
- Y: Competency count
- Color gradient: S1 = most saturated, S6 = lightest (emphasizes S1 dominance)
- Annotate S1 (111 competencies) with: "Planning is where digital permitting and NEPA reform hit hardest"
- Annotate S3 (11 competencies) with: "Implementation stage is relatively thin — a curriculum gap"

**Story rationale:** Workflow stage distribution reveals where professional practice concentrates, and therefore where disruption pressure concentrates. S1 dominance + high reform exposure is the double-exposure argument in spatial form.

---

## Slide 8 — Stability of Work
**Sheet:** `S8_Stability_Tier` | **Template:** Donut chart or horizontal stacked bar
**Headline:** *"68% of competencies are in active transition — this is not a stable workforce, and current training systems weren't built for this pace"*

**Configuration:**
- Three segments: Emergent (19), Transition (150), Stable (53)
- Colors: Emergent = bright teal (#00B4D8), Transition = amber (#D4A017), Stable = forest green (#2D6A4F)
- If donut: "150 in Transition" as center callout
- Annotation: "Stable competencies are predominantly Fieldcraft Primary — physical site knowledge persists; procedural and analytical knowledge is in flux"

**Story rationale:** This is the closing argument. After showing scope, structure, disruption, and risk, the stability tier slide lands the "so what" for workforce planning: current training, hiring, and classification systems were designed for a stable-tier world. The taxonomy is infrastructure for a transition-tier reality.

---

## Supplemental — AutoType × Craft Cross-Tab
**Sheet:** `S9_Bubble_Data` | **Template:** Scatter or bubble
**Headline:** *"Craft type predicts disruption exposure — Fieldcraft = Human-Essential; Datacraft = augmentable; Statecraft = split"*

**Use case:** Deep-dive slide for technical or Delphi audiences, not the primary funder narrative. Shows the structural logic underlying the Human-Essential classifications.

---

## Story Flow Summary

| Slide | Question Answered | Key Number |
|-------|-------------------|------------|
| 1: Scope | What was built? | 222 competencies, 7 domains |
| 2: Craft | What kind of work? | 42% Statecraft |
| 3: AI Exposure | What's at risk from automation? | 38% Human-Essential; 17% Compressive |
| 4: Reform | What's at risk from policy? | 58% reform-exposed |
| 5: CLD | Who loses their entry path? | 22% CLD-flagged |
| 6: Profession Families | Who benefits? | 15 families served |
| 7: Workflow Stage | Where in the work cycle? | S1 = 50% of competencies |
| 8: Stability | Is this a stable system? | 68% in transition |

---

## Design Consistency Notes

- **Font:** Use a single sans-serif (Inter or Source Sans) across all slides for body; a serif display font (Playfair Display or similar) for headlines if Flourish permits
- **Color anchor:** Forest green (#2D6A4F) as primary; amber (#D4A017) for transition/risk; red-orange (#E63946) for substitution/high-severity; gray (#CED4DA) for baseline/no-signal
- **Headline discipline:** Every slide headline states the argument, not the chart description. "42% of competencies are Statecraft" is a headline. "Craft distribution by domain" is a label — it belongs in a subtitle, not the H1.
- **Source line:** Include on every slide — "Source: Environmental Management Skills Taxonomy V3, March 2026 | 222 competencies | EPIC / New America Digital Service for the Planet Fellowship"

---

## Pending Data Note

Before finalizing slides 3 and 5 for external distribution:
1. Integrate Pre-Task 15A reclassifications into V3 (12 A→Ac changes in D6; 12 new CLD signals)
2. Populate ethical lens columns (L1–L5) in V3 — currently empty in the database despite Task 15 completion; when integrated, add a Slide 9 on implicit ethical content (88% implicit)
