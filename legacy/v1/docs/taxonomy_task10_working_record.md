# Task 10 Working Record: Workflow Stage Tagging — All Competencies

## Stage Key
- **S1** = Planning & Strategy
- **S2** = Environmental Review & Compliance
- **S3** = Permitting & Authorization
- **S4** = Implementation & Field Operations
- **S5** = Monitoring & Assessment
- **S6** = Adaptive Management & Learning

## Reform Sensitivity Codes
- `NEPA-timeline` — Affected by NEPA review timeline changes
- `CatEx-scope` — Affected by categorical exclusion list expansion
- `S2-S3-boundary` — Affected by changes to the review-permitting boundary
- `digital-permitting` — Affected by digital permitting portal requirements
- `consultation-reform` — Affected by Section 7/Section 106 process changes
- `one-federal-decision` — Affected by concurrent review requirements

## Tagging Rules
- Maximum 2 Primary + 2 Secondary per competency
- Dual-Primary exceptions flagged with ⚠️
- Blank Reform Sensitivity = no reform sensitivity flag (not a zero finding)

---

## Domain 1: Ecological & Scientific Knowledge

### 1.1 Ecosystem Science

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 1.1.1 | Ecosystem dynamics and processes | S1 | S6 | — |
| 1.1.2 | Biodiversity assessment and monitoring | S5 | S1 | NEPA-timeline |
| 1.1.3 | Ecological succession principles | S1 | S6 | — |
| 1.1.4 | Disturbance ecology | S1 | S6 | — |
| 1.1.5 | Habitat requirements analysis | S1 | S2 | NEPA-timeline |

### 1.2 Soil & Water Science

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 1.2.1 | Soil classification and mapping | S1 | S2 | NEPA-timeline |
| 1.2.2 | Soil chemistry and biology | S1 | S5 | — |
| 1.2.3 | Watershed hydrology | S1 | S2 | NEPA-timeline |
| 1.2.4 | Water quality assessment | S5 | S2 | NEPA-timeline, consultation-reform |
| 1.2.5 | Erosion processes and control | S1 | S4 | — |

### 1.3 Forestry Science

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 1.3.1 | Silviculture principles and practices | S1 | S4 | — |
| 1.3.2 | Forest mensuration and inventory | S1 | S5 | NEPA-timeline, CatEx-scope |
| 1.3.3 | Stand dynamics and growth modeling | S1 | S6 | — |
| 1.3.4 | Forest health assessment | S5 | S1 | NEPA-timeline |
| 1.3.5 | Timber management planning | S1 | S3 | NEPA-timeline, CatEx-scope |

### 1.4 Wildlife & Fisheries Biology

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 1.4.1 | Population dynamics and modeling | S1 | S6 | — |
| 1.4.2 | Wildlife survey techniques | S5 | S2 | NEPA-timeline, consultation-reform |
| 1.4.3 | Species identification and classification | S5 | S2 | NEPA-timeline, consultation-reform |
| 1.4.4 | Animal behavior and habitat relationships | S1 | S6 | — |
| 1.4.5 | Fisheries management principles | S1 | S2 | NEPA-timeline, consultation-reform |

### 1.5 Climate Science

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 1.5.1 | Climate data analysis and interpretation | S1 | S6 | — |
| 1.5.2 | Climate vulnerability assessment | S1 | S2 | NEPA-timeline |
| 1.5.3 | Climate adaptation planning | S1 | S6 | — |
| 1.5.4 | Carbon cycle science | S1 | S5 | digital-permitting |
| 1.5.5 | Phenology and climate-biosphere interactions | ⚠️ S1, S5 | — | — |

### 1.6 Biotechnology & Genetics

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 1.6.1 | Conservation genetics principles | S1 | S6 | — |
| 1.6.2 | Environmental DNA (eDNA) methods | S5 | S2 | NEPA-timeline, digital-permitting |
| 1.6.3 | Population genomics and genetic diversity | ⚠️ S1, S5 | — | — |
| 1.6.4 | Molecular ecology applications | S5 | S1 | — |
| 1.6.5 | Genetic tools for species management | S1 | S4 | consultation-reform |

### 1.7 Novel Ecosystems & Adaptation

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 1.7.1 | Novel ecosystem recognition and assessment | S1 | S6 | — |
| 1.7.2 | Assisted migration and managed relocation | S1 | S3 | consultation-reform |
| 1.7.3 | Climate refugia identification | S1 | S5 | — |
| 1.7.4 | Ecological transformation management | S1 | S6 | — |
| 1.7.5 | Non-analog futures planning | S1 | S6 | — |

### 1.8 Sustainable Agriculture Science

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 1.8.1 | Agroecology principles | S1 | S6 | — |
| 1.8.2 | Soil carbon dynamics | S1 | S5 | digital-permitting |
| 1.8.3 | Regenerative agriculture systems | S1 | S4 | — |
| 1.8.4 | Agricultural-ecological integration | S1 | S6 | — |
| 1.8.5 | Food systems ecology | S1 | S6 | — |

### Domain 1 Summary
- S1 Primary: 35 | S5 Primary: 7 | Dual Primary (S1+S5): 2
- S2 Secondary: 9 | S6 Secondary: 15 | S4 Secondary: 4 | S3 Secondary: 2 | S5 Secondary: 3 | S1 Secondary: 3
- Reform flags: 12 competencies flagged. NEPA-timeline: 8; consultation-reform: 5; digital-permitting: 2; CatEx-scope: 2

---

## Domain 2: Technical & Technological Skills

### 2.1 Geospatial Technologies

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 2.1.1 | GIS operation | ⚠️ S1, S5 | — | digital-permitting |
| 2.1.2 | Remote sensing data analysis | S5 | S1 | digital-permitting, NEPA-timeline |
| 2.1.3 | GPS data collection and management | S4 | S5 | — |
| 2.1.4 | Spatial analysis and modeling | S1 | S2 | NEPA-timeline, S2-S3-boundary |
| 2.1.5 | Cartography and visualization | S1 | S2 | NEPA-timeline |

### 2.2 Data Management & Analysis

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 2.2.1 | Database design and management | S5 | S1 | digital-permitting |
| 2.2.2 | Statistical analysis and interpretation | S5 | S6 | — |
| 2.2.3 | Data quality control and validation | S5 | S2 | NEPA-timeline, digital-permitting |
| 2.2.4 | Programming and scripting | S5 | S6 | digital-permitting |
| 2.2.5 | Metadata standards and management | S5 | S1 | digital-permitting |

### 2.3 Field Technology

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 2.3.1 | Environmental sensor deployment and maintenance | S5 | S4 | digital-permitting |
| 2.3.2 | Drone/UAS operation and data collection | S5 | S4 | digital-permitting, NEPA-timeline |
| 2.3.3 | Field data recording systems | S4 | S5 | — |
| 2.3.4 | Mobile applications for field science | S4 | S5 | digital-permitting |
| 2.3.5 | Remote communication systems | S4 | — | — |

### 2.4 Advanced Analytics

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 2.4.1 | Machine learning for environmental applications | S5 | S6 | digital-permitting |
| 2.4.2 | Predictive modeling and simulation | S1 | S6 | NEPA-timeline |
| 2.4.3 | Decision support systems | S1 | S6 | digital-permitting, one-federal-decision |
| 2.4.4 | Network analysis | S1 | S5 | — |
| 2.4.5 | Time series analysis | S5 | S6 | — |

### 2.5 Digital Collaboration Tools

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 2.5.1 | Virtual meeting facilitation | S1 | S2 | digital-permitting |
| 2.5.2 | Collaborative document management | S1 | S2 | digital-permitting, NEPA-timeline |
| 2.5.3 | Project management software | S1 | S4 | — |
| 2.5.4 | Knowledge management systems | S6 | S1 | — |
| 2.5.5 | Digital workflow design | S1 | S3 | digital-permitting, one-federal-decision |

### 2.6 AI-Enhanced Environmental Monitoring

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 2.6.1 | Computer vision for environmental applications | S5 | S6 | digital-permitting |
| 2.6.2 | Acoustic monitoring and analysis with AI | S5 | S6 | digital-permitting, NEPA-timeline |
| 2.6.3 | Predictive analytics for resource management | S6 | S1 | — |
| 2.6.4 | Automated data processing and QC with AI | S5 | — | digital-permitting |
| 2.6.5 | AI model interpretation and explainability | S5 | S2 | digital-permitting |

### 2.7 Immersive Technologies

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 2.7.1 | Augmented reality field applications | S4 | S5 | — |
| 2.7.2 | Virtual reality environmental education | S1 | — | digital-permitting |
| 2.7.3 | Digital twin development and management | ⚠️ S1, S5 | — | digital-permitting, one-federal-decision |
| 2.7.4 | Immersive visualization design | S1 | S2 | digital-permitting, NEPA-timeline |
| 2.7.5 | 3D landscape modeling | S1 | S5 | NEPA-timeline |

### Domain 2 Summary
- S1 Primary: 10 | S5 Primary: 13 | S4 Primary: 5 | S6 Primary: 2 | Dual Primary (S1+S5): 2
- Reform flags: 20 competencies flagged. digital-permitting: 15; NEPA-timeline: 7; one-federal-decision: 2; S2-S3-boundary: 1

---

## Domain 3: Management & Administrative Skills

### 3.1 Project Management (Zero-Core in Task 9)

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 3.1.1 | Project planning and scheduling | S1 | S4 | — |
| 3.1.2 | Budget development and management | S1 | S4 | digital-permitting |
| 3.1.3 | Risk assessment and mitigation | S1 | S4 | — |
| 3.1.4 | Contract and agreement administration | S3 | S4 | digital-permitting |
| 3.1.5 | Performance monitoring and evaluation | S5 | S6 | — |

### 3.2 Strategic Planning (Zero-Core in Task 9)

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 3.2.1 | Organizational assessment | S1 | S6 | — |
| 3.2.2 | Vision and mission development | S1 | — | — |
| 3.2.3 | Goal setting and objective definition | S1 | S6 | — |
| 3.2.4 | Implementation strategy design | S1 | S4 | — |
| 3.2.5 | Adaptive management planning | S1 | S6 | — |

### 3.3 Resource Administration (Zero-Core in Task 9)

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 3.3.1 | Personnel management and supervision | S4 | S1 | — |
| 3.3.2 | Equipment and asset management | S4 | S1 | — |
| 3.3.3 | Facilities operations and maintenance | S4 | — | — |
| 3.3.4 | Procurement and purchasing | S1 | S4 | digital-permitting |
| 3.3.5 | Records management and documentation | S5 | S3 | digital-permitting |

### 3.4 Financial Management

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 3.4.1 | Digital financial systems and data-driven budgeting | S1 | S5 | digital-permitting |
| 3.4.2 | Emerging conservation finance mechanisms | S1 | S3 | digital-permitting, S2-S3-boundary |
| 3.4.3 | Cryptocurrency, digital payments, and decentralized finance | S1 | — | digital-permitting |
| 3.4.4 | Automated financial operations and AI-enhanced compliance | S5 | S1 | digital-permitting |
| 3.4.5 | Real-time impact measurement and financial transparency | S5 | S6 | digital-permitting |

### 3.5 Leadership (Zero-Core in Task 9)

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 3.5.1 | Leading through digital transformation | S1 | S6 | digital-permitting |
| 3.5.2 | Remote and hybrid team leadership | S4 | S1 | — |
| 3.5.3 | Building organizational resilience and managing change fatigue | S1 | S6 | — |
| 3.5.4 | Cross-generational leadership and bridging technological divides | S1 | S4 | — |
| 3.5.5 | Ethical leadership in AI and algorithmic decision-making | S1 | S6 | digital-permitting |

### 3.6 Corporate Sustainability & ESG Management

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 3.6.1 | ESG strategy development and implementation | S1 | S2 | digital-permitting |
| 3.6.2 | Sustainability reporting and disclosure | S2 | S5 | digital-permitting, S2-S3-boundary |
| 3.6.3 | Stakeholder engagement for sustainability | S1 | S2 | — |
| 3.6.4 | Materiality assessment and prioritization | S1 | S2 | — |
| 3.6.5 | Sustainability performance metrics and KPIs | S5 | S1 | digital-permitting |

### 3.7 Circular Economy & Waste Systems

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 3.7.1 | Circular economy strategy and business model design | S1 | S4 | — |
| 3.7.2 | Waste reduction and zero waste programs | S4 | S5 | — |
| 3.7.3 | Product lifecycle assessment and design | S2 | S1 | digital-permitting |
| 3.7.4 | Reverse logistics and closed-loop systems | S4 | S1 | — |
| 3.7.5 | Material flow analysis and optimization | S1 | S5 | digital-permitting |

### Domain 3 Summary
- S1 Primary: 19 | S2 Primary: 2 | S3 Primary: 1 | S4 Primary: 5 | S5 Primary: 5 | S6 Primary: 0
- Reform flags: 9 competencies flagged (but some carry multiple codes). digital-permitting: 7 (dominant); S2-S3-boundary: 2

---

## Domain 4: Field Operations & Implementation

### 4.1 Field Assessment & Monitoring

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 4.1.1 | Vegetation sampling and assessment | S5 | S1 | NEPA-timeline |
| 4.1.2 | Wildlife observation and sign interpretation | S5 | S2 | NEPA-timeline, consultation-reform |
| 4.1.3 | Water quality testing and aquatic surveys | S5 | S3 | NEPA-timeline, consultation-reform |
| 4.1.4 | Soil characterization and sampling | S5 | S1 | — |
| 4.1.5 | Digital data collection and management | S4 | S5 | digital-permitting |

### 4.2 Land Management Implementation

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 4.2.1 | Restoration techniques and implementation | S4 | S5 | — |
| 4.2.2 | Invasive species control | S4 | S5 | CatEx-scope |
| 4.2.3 | Prescribed burning and fire management | S4 | S3 | CatEx-scope, NEPA-timeline, consultation-reform |
| 4.2.4 | Erosion control and watershed treatment | S4 | S5 | — |
| 4.2.5 | Trail construction and maintenance | S4 | — | CatEx-scope |

### 4.3 Fire Management

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 4.3.1 | Wildland firefighting | S4 | — | — |
| 4.3.2 | Prescribed fire planning and execution | ⚠️ S4, S1 | — | CatEx-scope, NEPA-timeline |
| 4.3.3 | Fuels management | S4 | S1 | CatEx-scope, NEPA-timeline |
| 4.3.4 | Fire weather and behavior analysis | S4 | S1 | — |
| 4.3.5 | Post-fire rehabilitation | S4 | S5 | NEPA-timeline |

### 4.4 Safety & Emergency Response (Zero-Core in Task 9)

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 4.4.1 | Occupational safety and risk management | S4 | — | — |
| 4.4.2 | First aid and emergency medical response | S4 | — | — |
| 4.4.3 | Search and rescue operations | S4 | — | — |
| 4.4.4 | Hazardous materials awareness and response | S4 | S3 | — |
| 4.4.5 | Emergency communication and incident reporting | S4 | S3 | — |

### 4.5 Equipment Operation

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 4.5.1 | Hand tool proficiency | S4 | — | — |
| 4.5.2 | Power equipment operation | S4 | S3 | CatEx-scope |
| 4.5.3 | Heavy equipment and vehicle operation | S4 | S3 | — |
| 4.5.4 | Drone/UAS operation for field applications | S4 | S3 | digital-permitting |
| 4.5.5 | Equipment maintenance and repair | S4 | S1 | — |

### 4.6 Sustainable Agriculture Implementation

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 4.6.1 | Regenerative practice implementation | S4 | S5 | — |
| 4.6.2 | Precision agriculture technology use | S4 | S5 | digital-permitting |
| 4.6.3 | Integrated pest management application | S4 | S3 | — |
| 4.6.4 | Irrigation management and water conservation | S4 | S3 | — |
| 4.6.5 | Soil health assessment and management | S5 | S1 | — |

### 4.7 Urban Environmental Infrastructure

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 4.7.1 | Green infrastructure installation | S4 | S3 | — |
| 4.7.2 | Urban forestry operations | S4 | S5 | — |
| 4.7.3 | Stormwater system management | S4 | S5 | digital-permitting |
| 4.7.4 | Urban habitat restoration | S4 | S5 | CatEx-scope |
| 4.7.5 | Green building systems maintenance | S4 | S5 | digital-permitting |

### Domain 4 Summary
- S4 Primary: 28 | S5 Primary: 5 | Dual Primary (S4+S1): 1
- S2 Primary: 0 | S2 Secondary: 0 — Complete S2 absence
- S6 Primary: 0 | S6 Secondary: 0 — Complete S6 absence
- Reform flags: 13 competencies flagged. CatEx-scope: 6 (dominant); NEPA-timeline: 4; digital-permitting: 4; consultation-reform: 2

---

## Domain 5: Communication, Engagement & Social Skills

### 5.1 Public Communication

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 5.1.1 | Written communication for diverse audiences | S1 | S6 | — |
| 5.1.2 | Public speaking and presentation | S1 | S2 | — |
| 5.1.3 | Environmental interpretation | S4 | S1 | — |
| 5.1.4 | Social media and digital outreach | S1 | S4 | digital-permitting |
| 5.1.5 | Science communication and storytelling | S6 | S1 | — |

### 5.2 Stakeholder Engagement

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 5.2.1 | Stakeholder identification and analysis | S1 | S2 | NEPA-timeline |
| 5.2.2 | Meeting facilitation and design | S1 | S2 | NEPA-timeline, digital-permitting |
| 5.2.3 | Collaborative decision-making processes | S1 | S3 | consultation-reform |
| 5.2.4 | Conflict resolution and mediation | S1 | S2 | NEPA-timeline |
| 5.2.5 | Partnership development and management | S1 | S3 | consultation-reform, one-federal-decision |

### 5.3 Cultural Competency

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 5.3.1 | Cross-cultural communication | S1 | S4 | — |
| 5.3.2 | Indigenous knowledge integration | S1 | S2 | consultation-reform |
| 5.3.3 | Cultural resource identification | S2 | S3 | consultation-reform, NEPA-timeline |
| 5.3.4 | Diversity, equity, and inclusion practices | S1 | S6 | — |
| 5.3.5 | Environmental justice principles | S2 | S1 | consultation-reform |

### 5.4 Education & Outreach

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 5.4.1 | Educational program development | S1 | S4 | — |
| 5.4.2 | Curriculum design for environmental education | S1 | — | — |
| 5.4.3 | Volunteer program management | S4 | S1 | — |
| 5.4.4 | Citizen science coordination | S5 | S1 | digital-permitting |
| 5.4.5 | Interpretive materials development | S1 | S4 | — |

### 5.5 Customer Service (Zero-Core in Task 9)

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 5.5.1 | Visitor information services | S4 | — | — |
| 5.5.2 | Permit administration | S3 | S4 | digital-permitting |
| 5.5.3 | Complaint resolution | S4 | S2 | — |
| 5.5.4 | Public relations management | S1 | S4 | digital-permitting |
| 5.5.5 | Accessibility accommodations | S1 | S4 | — |

### 5.6 Social Science & Behavioral Change

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 5.6.1 | Environmental psychology and behavior change theory | S1 | S6 | — |
| 5.6.2 | Social science research methods | S5 | S1 | — |
| 5.6.3 | Community organizing and mobilization | S1 | S4 | consultation-reform |
| 5.6.4 | Social marketing for sustainability | S1 | S5 | — |
| 5.6.5 | Participatory methods and community-based research | S1 | S2 | consultation-reform |

### Domain 5 Summary
- S1 Primary: 14 | S2 Primary: 3 | S3 Primary: 1 | S4 Primary: 5 | S5 Primary: 3 | S6 Primary: 1
- First S6 Primary in taxonomy: 5.1.5 Science communication (capstone of S5→S6 bottleneck argument)
- Reform flags: 11 competencies flagged. consultation-reform: 5 (dominant); digital-permitting: 4; NEPA-timeline: 2 (note: some competencies counted under multiple codes); one-federal-decision: 1

---

## Domain 6: Policy, Planning, Law & Economics

### 6.1 Environmental Law & Regulation

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 6.1.1 | Environmental policy analysis | S2 | S1 | NEPA-timeline, S2-S3-boundary |
| 6.1.2 | Regulatory compliance assessment | S2 | S3 | S2-S3-boundary, NEPA-timeline |
| 6.1.3 | Permitting procedures | S3 | S2 | NEPA-timeline, S2-S3-boundary, one-federal-decision |
| 6.1.4 | NEPA process implementation | S2 | S3 | NEPA-timeline, CatEx-scope, S2-S3-boundary, one-federal-decision |
| 6.1.5 | Enforcement procedures | S2 | S5 | S2-S3-boundary |

### 6.2 Land Use Planning

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 6.2.1 | Comprehensive land use planning | S1 | S2 | NEPA-timeline |
| 6.2.2 | Zoning and land classification | S1 | S3 | — |
| 6.2.3 | Public land management planning | S1 | S2 | NEPA-timeline, CatEx-scope |
| 6.2.4 | Community planning integration | S1 | S2 | consultation-reform |
| 6.2.5 | Scenario development and analysis | S1 | S6 | — |

### 6.3 Resource Economics

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 6.3.1 | Natural resource valuation | S1 | S2 | NEPA-timeline |
| 6.3.2 | Ecosystem services assessment | S1 | S2 | NEPA-timeline |
| 6.3.3 | Market-based conservation mechanisms | S1 | S3 | digital-permitting |
| 6.3.4 | Economic impact analysis | S2 | S1 | NEPA-timeline, S2-S3-boundary |
| 6.3.5 | Carbon credit and offset programs | S3 | S1 | digital-permitting, S2-S3-boundary |

### 6.4 Policy Development

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 6.4.1 | Policy research and analysis | S1 | S2 | NEPA-timeline |
| 6.4.2 | Policy drafting and review | S1 | S2 | NEPA-timeline, CatEx-scope, S2-S3-boundary |
| 6.4.3 | Regulatory impact assessment | S2 | S1 | NEPA-timeline, one-federal-decision |
| 6.4.4 | Public comment management | S2 | S3 | NEPA-timeline, digital-permitting, consultation-reform |
| 6.4.5 | Legislative process navigation | S1 | S3 | one-federal-decision |

### 6.5 Intergovernmental Relations

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 6.5.1 | Tribal consultation and coordination | S3 | S2 | consultation-reform, one-federal-decision |
| 6.5.2 | Federal-state-local coordination | S3 | S1 | one-federal-decision, consultation-reform |
| 6.5.3 | Interagency agreements development | S3 | S1 | one-federal-decision, S2-S3-boundary |
| 6.5.4 | Cross-jurisdictional planning | S1 | S3 | — |
| 6.5.5 | International conservation agreements | S3 | S1 | consultation-reform |

### 6.6 Environmental Markets

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 6.6.1 | Carbon accounting and quantification | S5 | S3 | digital-permitting, S2-S3-boundary |
| 6.6.2 | Biodiversity credits and habitat banking | S3 | S1 | digital-permitting, S2-S3-boundary |
| 6.6.3 | Environmental market transactions | S3 | S1 | digital-permitting |
| 6.6.4 | Conservation finance mechanisms | S1 | S3 | digital-permitting |
| 6.6.5 | Green bonds and sustainable investment | S1 | S3 | digital-permitting |

### 6.7 Environmental Health & Justice

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 6.7.1 | Environmental health risk assessment | S2 | S5 | consultation-reform |
| 6.7.2 | Environmental justice screening and assessment | S2 | S1 | consultation-reform, NEPA-timeline |
| 6.7.3 | Community-based participatory research | S1 | S2 | consultation-reform |
| 6.7.4 | Toxicology and exposure pathways | S2 | S5 | consultation-reform |
| 6.7.5 | Air quality management | S2 | S3 | consultation-reform, NEPA-timeline, S2-S3-boundary |

### 6.8 Climate Finance & Investment

| Code | Title | Primary | Secondary | Reform Sensitivity |
|------|-------|---------|-----------|-------------------|
| 6.8.1 | Climate finance mechanisms | S1 | S3 | digital-permitting, one-federal-decision |
| 6.8.2 | Green bonds and climate bonds | S1 | S3 | digital-permitting |
| 6.8.3 | Carbon markets and trading | S3 | S1 | digital-permitting, S2-S3-boundary |
| 6.8.4 | Adaptation finance | S1 | S3 | consultation-reform, digital-permitting |
| 6.8.5 | Climate investment risk assessment | S1 | S5 | digital-permitting |

### Domain 6 Summary
- S1 Primary: 13 | S2 Primary: 12 | S3 Primary: 10 | S4 Primary: 0 | S5 Primary: 1 | S6 Primary: 0
- S4 completely absent — Domain 6 is governance architecture, not field operations
- Reform flags: 24 competencies flagged (highest density). S2-S3-boundary: 10 (dominant); consultation-reform: 7; digital-permitting: 7; one-federal-decision: 5; NEPA-timeline: 5 (note: Domain 6 NEPA-timeline flags are about governance of review process, not field data collection); CatEx-scope: 2
- Paradigm case: 6.1.4 NEPA process implementation carries 4 simultaneous reform codes

---

## Cross-Domain Reform Sensitivity Totals

| Code | D1 | D2 | D3 | D4 | D5 | D6 | Total |
|------|----|----|----|----|----|----|-------|
| NEPA-timeline | 8 | 7 | 0 | 4 | 2 | 5 | **26** |
| digital-permitting | 2 | 15 | 7 | 4 | 4 | 7 | **39** |
| CatEx-scope | 2 | 0 | 0 | 6 | 0 | 2 | **10** |
| consultation-reform | 5 | 0 | 0 | 2 | 5 | 7 | **19** |
| one-federal-decision | 0 | 2 | 0 | 0 | 1 | 5 | **8** |
| S2-S3-boundary | 0 | 1 | 2 | 0 | 0 | 10 | **13** |
| **Total flags** | **17** | **25** | **9** | **16** | **12** | **36** | **115** |
| **Competencies flagged** | 12 | 20 | 9 | 13 | 11 | 24 | **89** |

---

## Dual-Primary Exception Register

| Code | Title | Stages | Domain | Justification |
|------|-------|--------|--------|---------------|
| 1.5.5 | Phenology and climate-biosphere interactions | S1+S5 | D1 | Same knowledge drives planning timing and monitoring protocol |
| 1.6.3 | Population genomics and genetic diversity | S1+S5 | D1 | Same methods serve management design and long-term status monitoring |
| 2.1.1 | GIS operation | S1+S5 | D2 | Planning map production and monitoring visualization are co-equal professional outputs |
| 2.7.3 | Digital twin development and management | S1+S5 | D2 | Simulation (planning) and calibration (monitoring) are genuinely distinct Primary functions |
| 4.3.2 | Prescribed fire planning and execution | S4+S1 | D4 | Burn plan design and burn execution are both Primary professional outputs for F1/F3/F12 |

---

## Document Status

- **Created**: Task 10 completion, February 2026
- **Purpose**: Operational source of truth for database integration (Task 16), reform sensitivity analysis (Task 13), and Delphi review resolution
- **Companion document**: Task 10 Completion Summary (interpretive findings, structural arguments, causal chain framework)
- **Cross-references**: Task 9 Working Record (profession family tags), Task 6 Workflow Stage Definitions (boundary criteria), Task 8 Craft Assignment Criteria (for Task 11 cross-referencing)
