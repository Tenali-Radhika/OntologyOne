# Certified Metric Contracts Registry
**Rule:** One definition per metric. Zero recomputation anywhere in the enterprise.

---

## 1. OTD_V1 — On-Time Delivery Rate (Flagship Metric)

- **ID:** `OTD_V1`
- **Status:** `CERTIFIED` (v1.0.0)
- **Owner:** VP Global Logistics
- **Business Definition:** Percentage of delivered customer orders that arrived at or prior to the contractually promised delivery date.
- **Formula:**
  $$\text{OTD\_V1} = \frac{\sum \text{CASE WHEN } delivery\_date \le promised\_date \text{ THEN 1 END}}{\sum 1}$$
- **Grain:** Shipment / Order Line
- **Default Time Horizon:** `2026-Q3` (July 1, 2026 – September 30, 2026)
- **Target Value:** `91.4%` (overall company Q3 benchmark)
- **Exclusions:** Canceled orders, items in transit without delivery confirmation, RMA returns.
- **Fast-Path Source:** `ONTO_HACKATHON.MART.MART_OTD_AGGREGATE` (RAP-unrestricted)
- **Granular Lineage Source:** `ONTO_HACKATHON.CORE.CORE_SHIPMENT` (subject to persona RAP)
- **Governance Requirement:** Any calculation based on dock dispatch date (`ship_date`) or `raw_orders.is_delayed` is strictly rejected as uncertified.

---

## 2. FR_V1 — Order Fill Rate

- **ID:** `FR_V1`
- **Status:** `CERTIFIED` (v1.0.0)
- **Owner:** Head of Plant Operations
- **Business Definition:** Percentage of customer ordered units successfully completed and dispatched from the manufacturing plant.
- **Formula:**
  $$\text{FR\_V1} = \frac{\sum quantity\_fulfilled}{\sum quantity\_ordered}$$
- **Grain:** Order Line
- **Source:** `ONTO_HACKATHON.CORE.CORE_ORDER_LINE`
- **Benchmark:** $\ge 88.0\%$. Scenario S2 identifies Plant P03 chronic deficit at $74.2\%$.

---

## 3. DOI_V1 — Days of Inventory

- **ID:** `DOI_V1`
- **Status:** `CERTIFIED` (v1.0.0)
- **Owner:** Supply Chain Planning
- **Business Definition:** Estimated operational days current on-hand buffer stock can sustain projected daily customer demand.
- **Formula:**
  $$\text{DOI\_V1} = \frac{\sum current\_stock\_quantity}{\frac{\sum usage\_quantity\_30d}{30}}$$
- **Grain:** Part / Plant
- **Source:** `ONTO_HACKATHON.CORE.CORE_INVENTORY`

---

## 4. LC_V1 — Total Landed Cost

- **ID:** `LC_V1`
- **Status:** `CERTIFIED` (v1.0.0)
- **Owner:** Procurement Director
- **Business Definition:** Delivered cost per purchased part unit, comprising base supplier purchase price plus allocated freight transit surcharge.
- **Formula:**
  $$\text{LC\_V1} = unit\_cost + \frac{freight\_cost}{quantity\_ordered}$$
- **Security:** Visible ONLY to `ONTO_PROCUREMENT` and `ONTO_JUDGE`. Dynamic masking redacts values to `***CONFIDENTIAL***` for other personas.
