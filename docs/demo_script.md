# Demo Day Script (5:00 Minute Choreography)
**OntologyOne — Snowflake CoCo Hackathon Track 5**

---

### [0:00–0:30] Scene 1: The Problem — The Three-Dashboard Disconnect
- **Visual:** Open three mock reporting views from different departments:
  - Procurement dashboard displays: **94.2% OTD**
  - Logistics dashboard displays: **89.7% OTD**
  - Planning dashboard displays: **92.1% OTD**
- **Speaker:** 
  > *"Every Monday morning, our executive team asks: 'What is our On-Time Delivery rate?' And every Monday, three different vice presidents give three different numbers. Why? Because each team queries raw tables with ad-hoc joins and differing security filters. Which number is correct? (Pause). The answer is: none of them."*

---

### [0:30–1:30] Scene 2: The Proof — Unified Aggregate Truth
- **Visual:** Switch to **OntologyOne: Command Center**.
- **Action:** Switch persona between:
  - `Logistics Admin` -> Q3 OTD = **91.4%**
  - `Procurement Lead` -> Q3 OTD = **91.4%**
  - `Demand Planner` -> Q3 OTD = **91.4%**
- **Action:** Expand the **Trust Panel** for `OTD_V1`. Point to `[✓ Grounded in Semantic Spec]`.
- **Speaker:**
  > *"With OntologyOne, we solved the Row Access Policy paradox. By separating pre-aggregated certified truth in `MART_OTD_AGGREGATE` from entitled granular base tables, every persona receives the identical governed calculation: 91.4%. Same question, same metric contract, same answer."*

---

### [1:30–2:20] Scene 3: Governance by Consequence
- **Visual:** Switch to **Ask OntologyOne** chat screen as `Logistics Admin`.
- **Prompt:** *"Show me unit costs and total landed spend for all parts supplied by S-017."*
- **Result:** Agent refuses/masks cost data with `***CONFIDENTIAL***` and logs an access violation to `GOV.AUDIT_LOG`.
- **Action:** Re-run the company OTD query: still **91.4%**.
- **Speaker:**
  > *"When an unauthorized persona attempts to access protected pricing, the system refuses and logs the violation. Yet because our architecture is two-tier, company aggregate truth remains rock-solid and invariant."*

---

### [2:20–3:30] Scene 4: The Deep Investigation (Scenario S1)
- **Visual:** Switch to `Demand Planner` persona in chat.
- **Prompt:** *"Why did our company On-Time Delivery rate fall in Q3?"*
- **Action:** Watch the **Truth Compiler** run in real time:
  1. Identifies OTD drop: **94.8% (Q2) -> 91.4% (Q3)** (-3.4 pts).
  2. Identifies primary causal driver: Supplier **S-017 (MicroCore Silicon Dynamics)** sliding from **96.2% -> 81.7%**.
  3. Decomposes impact: Plants **P03, P07, P09**, **17 microcontroller parts**, **428 late shipments**.
  4. Drills into anchor shipment **SH-93821** (promised 2026-08-15, delivered 2026-08-19, LATE).
- **Speaker:**
  > *"OntologyOne doesn't just calculate a metric; it decomposes the entire causal chain across the ontology graph from metric to supplier to plants down to a specific late shipment."*

---

### [3:30–4:10] Scene 5: Unstructured Business Evidence (Cortex Search)
- **Visual:** Agent renders the dual evidence panel:
  - **Left Panel (Data Evidence):** 428 late shipment rows, delivery timestamps, carrier dwell times.
  - **Right Panel (Business Evidence):** Document citation chip citing **SLA_S017.pdf §4.2**.
- **Action:** Click citation chip to view excerpt:
  > *"Due to upstream wafer substrate shortage and clean-room maintenance at Dresden Fab, Supplier S-017 invoked §4.2 allocation restrictions, extending lead times from 14 to 28 days."*
- **Speaker:**
  > *"Data evidence tells you WHAT happened. Business evidence from Cortex Search tells you WHY it happened. Finding = Data Evidence + Contractual Evidence."*

---

### [4:10–4:40] Scene 6: Actionable Recommendations
- **Visual:** Agent presents clearly labeled recommendations:
  - `[AI-generated recommendation]`: Trigger vendor cure meeting under SLA §2.2 default provisions.
  - `[AI-generated recommendation]`: Expedite 84 critical in-transit shipments across P03, P07, P09.
  - `[AI-generated recommendation]`: Reallocate buffer inventory from P07 to P03 per SOP-OPS-REG-04.
- **Speaker:**
  > *"Notice the label: AI-generated recommendation. AI recommends; human leaders decide."*

---

### [4:40–5:00] Scene 7: The Mic Drop — 12/12 Governance Test Suite
- **Visual:** Click over to **Trust & Lineage** tab.
- **Action:** Click **Run Governance Verification Suite**.
- **Display:** Full green audit bar:
  $$\text{GOVERNANCE AUDIT: 12/12 PASSED}$$
  $$\text{Planner (91.4\%) == Procurement (91.4\%) == Logistics (91.4\%) }$$
- **Speaker (Closing Line):**
  > *"We didn't teach an AI what the truth is. We gave the AI a governed definition of truth. Thank you."*
