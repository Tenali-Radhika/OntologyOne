# OntologyOne — Architectural Blueprint
**Snowflake CoCo CLI Hackathon (GCC Edition) — Track 5**

---

## 1. Executive Summary & Thesis
**OntologyOne** implements an enterprise supply chain semantic layer and conversational analytics agent powered by Snowflake Cortex, governed metric contracts, and an unbreakable two-tier truth architecture.

### The Thesis
> *"Same question → same governed metric → same calculation → same answer → different authorized context."*

In modern enterprise data platforms, Row Access Policies (RAP) create a fundamental dilemma: when analytical queries sum or average rows under varying role-level entitlements, company-wide executive KPIs diverge across business units (e.g., Procurement sees 94.2% OTD, Logistics sees 89.7%, Planning sees 92.1%). 

**The RAP Paradox Fix ("Unified Aggregate Truth, Entitled Granular Lineage"):**
1. **Tier 1 (Aggregate Truth):** `MART_OTD_AGGREGATE` — Pre-aggregated, RAP-unrestricted certified mart. Any persona querying the company metric receives the exact same certified answer (`91.4%`).
2. **Tier 2 (Entitled Granular Lineage):** Base tables (`CORE_SHIPMENT`, `CORE_ORDER_LINE`) — Strictly governed by Snowflake Row Access Policies and Dynamic Masking. Granular drill-down investigations reveal only the data records each persona is authorized to inspect.

---

## 2. Five-Layer Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────────┐
│               STREAMLIT IN SNOWFLAKE (SiS) / LOCAL UI                  │
│   [1. Command Center]  [2. Ask OntologyOne]  [3. Ontology Explorer]    │
│                       [4. Trust & Lineage DAG]                         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Natural Language & Prompts
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        SNOWFLAKE CORTEX AGENT                          │
│   • Semantic Analyst Tool (Cortex Analyst text-to-SQL)                 │
│   • Unstructured Evidence (Cortex Search Service)                      │
│   • CoCo Custom Skills: metric_explainer, anomaly_narrator, lineage    │
└───────────────────┬────────────────────────────────┬───────────────────┘
                    │                                │
                    ▼ Structured Data                ▼ Unstructured Evidence
┌───────────────────────────────────────┐  ┌─────────────────────────────┐
│  SEMANTIC VIEW (SUPPLY_SEMANTIC)      │  │ CORTEX SEARCH SERVICE       │
│  • 6 Entities, 5 Relationships        │  │ (DOCS_SEARCH_SERVICE)       │
│  • Metric Contracts: OTD_V1, FR_V1    │  │ • SLA_S017.pdf (§4.2)       │
│  • Verified Queries Fixture Suite     │  │ • freight_agreement (§2.1)  │
│  • Deprecated TRAP column defense     │  │ • legacy_metric_memo        │
└───────────────────┬───────────────────┘  └─────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        SNOWFLAKE DATA ENGINE                           │
│   • MART: MART_OTD_AGGREGATE (RAP-Unrestricted Certified Mart)         │
│   • CORE: Dynamic Tables (CORE_SHIPMENT, CORE_ORDER_LINE, ...)         │
│   • RAW: Ingestion Staging Tables (EDI-214 feeds)                      │
│   • GOV: Roles (PLANNER, PROCUREMENT, LOGISTICS, JUDGE), RAP, Masking  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Truth Compiler Concept
OntologyOne establishes a deterministic compile pipeline for every user request:
1. **NL Question**: User expresses an operational question in plain English.
2. **Business Intent**: Intent classifier identifies the domain entity, metric, or anomaly.
3. **Ontology Resolution**: Binds terms to canonical entities (`SUPPLIER`, `PART`, `PLANT`, `ORDER_LINE`, `SHIPMENT`, `CUSTOMER`).
4. **Metric Contract Binding**: Enforces certified contracts (e.g. `OTD_V1`). Rejects uncertified legacy columns (`raw_orders.is_delayed`).
5. **Governed Semantic View**: Routes query to `SUPPLY_SEMANTIC` or fast-path `MART_OTD_AGGREGATE`.
6. **Authorized Execution**: Applies user's active RBAC role, Row Access Policies, and Dynamic Masking.
7. **Lineage & Audit Generation**: Logs SQL, parameters, and contract version to `GOV.AUDIT_LOG`.
8. **Synthesized Finding**: Combines Data Evidence (rows, dates) + Business Evidence (contract clauses) + Labeled AI Recommendations.

---

## 4. Governance & RBAC Model

| Role | Business Scope | Cost Visibility | Row Access Policy Scope |
| :--- | :--- | :--- | :--- |
| **ONTO_PLANNER** | Demand & Inventory Planning | Masked (`NULL`) | All 12 Plants, Global Orders |
| **ONTO_PROCUREMENT** | Supplier Contracts & Sourcing | **Unmasked** (`FLOAT`) | Global Suppliers & Shipments |
| **ONTO_LOGISTICS** | Outbound Freight & Carrier Execution | Masked (`NULL`) | Assigned logistics nodes |
| **ONTO_JUDGE** | Hackathon Evaluation Auditor | **Unmasked** (`FLOAT`) | Unrestricted Global Access |

---

## 5. Deployment with CoCo CLI & Makefile
All lifecycle actions are automated via `Makefile` calling the Snowflake CLI (`snow`):
- `make generate-data`: Seeds deterministic synthetic data matching S1–S5.
- `make test-coco`: Executes the 12/12 Governance & Metric verification suite.
- `make run`: Starts the Streamlit Command Center.
- `make deploy`: Deploys database objects, semantic views, search services, and Streamlit app to Snowflake.
