# ONTOLOGYONE — MASTER EXECUTION BRIEF FOR ANTIGRAVITY (GEMINI 3.8)

> **How to use this document:** Paste this entire file into Antigravity's Agent Manager as the root planning brief. Gemini 3.8 should first produce an Artifact-level plan (ERD + metric contracts + scenario table) for human approval, then spawn the lanes below. Every lane has a mandatory verification gate — never report a lane "done" without executing it.

---

## 0. MISSION

Build **OntologyOne** for the Snowflake CoCo CLI Hackathon (GCC Edition), Track 5: Supply Chain Ontology & Governed Conversational Analytics.

**Thesis (one claim, proven beyond doubt):**
> Same question → same governed metric → same calculation → same answer → different authorized context.

**Non-goals (do NOT build):** huge datasets, many metrics, flashy UI beyond 4 screens, any feature not in this brief. The ontology + metric contracts + governance proof IS the project.

**Judging rubric to optimize:** Real-World Relevance 30% / Technical Execution 40% / Completeness 30%.

---

## 1. UNBREAKABLE RULES (read before generating any code)

1. **Never invent Snowflake syntax.** Consult the local `snowflake-docs/` folder (semantic view YAML spec, Cortex Agent REST, CoCo CLI reference) before generating any artifact; cite file + section in your plan output.
2. **One definition per metric.** Every metric's SQL exists in exactly one place (semantic view + certified mart). No recomputation anywhere, ever.
3. **Two-tier truth architecture (the RAP paradox fix):**
   - `MART_OTD_AGGREGATE` = pre-aggregated, RAP-unrestricted certified mart → company-level metric questions return **identical values for all personas**.
   - Base tables (`SHIPMENT`, `ORDER_LINE`, ...) = persona-entitled via RAP → drill-downs differ per persona, and the agent must state which entitlement policy applied.
   - Market this as **"Unified Aggregate Truth, Entitled Granular Lineage."**
4. **All deploys go through CoCo CLI**, never Snowsight clicks. Maintain a `Makefile` wrapping every deploy so the whole stack rebuilds with one command.
5. **Determinism:** synthetic data generator is seeded; planted scenarios have fixed expected values; the demo is replayable.
6. **AI recommends, humans decide.** Every recommendation block is labeled "AI-generated recommendation." The agent never claims decision authority.
7. **Test-first on the semantic layer:** every metric gets a verified-query fixture; run the suite before reporting any lane complete.

---

## 2. ARCHITECTURE (5 layers)

```
ONTOLOGYONE UI (Streamlit in Snowflake, 4 screens only)
        │
CORTEX AGENT  ← orchestration, intent, tool routing, citations
   ├── SEMANTIC VIEW (ONTO_HACKATHON.CORE.SUPPLY_SEMANTIC)  ← structured truth
   └── CORTEX SEARCH (contracts/SLAs/freight agreements)     ← document evidence
        │
SNOWFLAKE: RAW → CORE (dynamic tables) → MART
RBAC + RAP + Masking | Lineage | Audit log
        │
CoCo CLI drives ALL build & deploy (cortex.yaml + Makefile)
```

Modern layering (per current Snowflake docs): **one Cortex Agent** that uses the semantic view via the Analyst tool and Cortex Search for unstructured evidence. Do not architect Analyst and Agent as competing layers.

**Truth Compiler concept (name it in-app):**
NL question → business intent → ontology → metric contract → governed semantic view → authorized data → SQL → result → lineage + definition + evidence.

---

## 3. ONTOLOGY SPEC

**MVP entities (6):** SUPPLIER, PART, PLANT, ORDER_LINE, SHIPMENT, CUSTOMER.
**Relationships:** supplier—supplies→part—ordered_in→order_line; plant—fulfills→order_line; customer—placed_by→order_line; order_line—shipped_via→shipment. Explicit one_to_many cardinalities; no Cartesian joins.
**Hierarchies:** Region→Country→Plant; Category→Part; Day→Month→Quarter; Tier1→2→3 supplier risk rollup.
**Defer:** INVENTORY, CARRIER entities (add only if time remains after Day 11 freeze).

**Flagship metric: OTD_V1 (On-Time Delivery Rate).** Secondary: Fill Rate (FR_V1), Days of Inventory (DOI_V1), Landed Cost (LC_V1). The entire demo must work beautifully on OTD alone; secondary metrics are the "can it handle another?" answer.

**Metric Contract format (render in UI + store in `ontology/metric_contracts.yml`):** Metric, ID, Business Definition, Formula, Grain, Default Time, Exclusions, Owner, Source, Security, Version, Status=CERTIFIED.

The full production semantic view already exists as `ontology/SUPPLY_SEMANTIC.sv.yaml` (entity tables with labels/descriptions, deprecated `IS_DELAYED` trap column, synonyms per metric, `default_aggregation: NONE` on rates, `certified_source` fast-path, 8 verified queries). **Do not redesign it — deploy it, then fix only real schema drift against current docs.**

---

## 4. DATA STRATEGY — story density, not volume

`data/generator.py`: seeded RNG, ~100–200K rows total (50 suppliers, 200 parts, 12 plants, 500 customers, 2 years of orders/shipments).

**5 planted scenarios, each = DATA + DOCUMENT + EXPECTED ANSWER + EXPECTED ACTION + TEST:**

| # | Scenario | Data plant | Document | Expected | Action |
|---|---|---|---|---|---|
| S1 | Supplier deterioration | S-017 OTD slides 96.2%→81.7% over 8 wks; affects plants P03/P07/P09, 17 parts, 428 late shipments; company OTD 94.8%→91.4% in Q3 | SLA_S017.pdf §4.2 (capacity constraint / revised lead-time clause) | S-017 identified as primary contributor | Trigger supplier review; expedite 84 shipments |
| S2 | Plant fill-rate problem | P03 chronic low fill rate | Regional logistics policy | P03 flagged | Inventory reallocation P03→P07 |
| S3 | Freight surcharge | One lane's landed cost +30% | Freight agreement §2.1 (surcharge clause) | Lane identified, cost explained | Renegotiate / reroute |
| S4 | Definition conflict (TRAP) | `raw_orders.is_delayed` computed from SHIP date, not delivery date → legacy "OTD" reads ~94% (wrong) | Legacy metric memo | Agent must explicitly refuse legacy column and cite OTD_V1 | Explain governance |
| S5 | Access violation attempt | Persona asks for data outside entitlement (e.g., Logistics requests supplier costs) | — | Query refused/limited + logged; aggregate OTD still identical | Show governance consequence |

**Two corpora:** structured (SQL tables) + `docs_corpus/` (PDFs/TXT: SLAs, freight agreements, policy memos) → chunked into `DOCS.CHUNKS` → Cortex Search service with citations.

---

## 5. GOVERNANCE SPEC

- **Roles:** `ONTO_PLANNER`, `ONTO_PROCUREMENT`, `ONTO_LOGISTICS`, plus `ONTO_JUDGE` (read-everything evaluator role for hackathon judges).
- **RAP:** persona row filters on base tables (Planner: all plants/suppliers/inventory/orders; Procurement: supplier performance/contracts/costs; Logistics: shipments/carriers/routes). **`MART_OTD_AGGREGATE` deliberately outside all RAPs** — certified aggregate truth.
- **Masking:** costs (freight, unit price, landed cost) masked for non-Procurement; supplier names masked where policy requires.
- **Audit:** every agent answer logs question, persona, generated SQL, metric contract used, rows scanned, entitlement policies applied → `AUDIT_LOG` table (powers the Trust Panel).
- **Demo governance by consequence, not code:** never show policy DDL in the demo; show what each persona can/can't see and that OTD stays 91.4%.

---

## 6. CONVERSATIONAL & INVESTIGATION SPEC

- **Cortex Agent** with tools: (1) semantic view via Analyst tool, (2) Cortex Search on docs corpus, (3) custom Python skill `lineage_explainer` (returns metric contract + source + SQL for any answer).
- **CoCo skills to author:** `metric_explainer` (definition + contract on demand), `anomaly_narrator` (OTD decline → contributor decomposition → supplier → plants → shipments), `recommendation_engine` (labeled AI-generated).
- **Investigation flow that must work end-to-end (S1):**
  "Why did OTD fall?" → 94.8%→91.4% → primary contributor S-017 (96.2%→81.7%) → 3 plants, 17 parts, 428 shipments → drill to shipment SH-93821 (actual 2026-08-19 vs planned 2026-08-15, LATE) → Cortex Search cites SLA_S017 §4.2 → recommendation list.
- **Evidence taxonomy (two panels, always):** Data Evidence (rows, dates, statuses) + Business Evidence (cited document clauses). Finding = Data + Business.
- **Trust Panel (collapsible on every answer):** metric ID, definition, source table, grain, period, record count, numerator/denominator, data role, RAP policy applied, document evidence citation, generated SQL with a **[✓ Grounded in Semantic Spec]** badge.

---

## 7. UI SPEC — exactly 4 Streamlit screens, production polish

1. **Command Center** — persona switcher (● Logistics Admin | ○ Procurement Lead | ○ Demand Planner), KPI cards (certified metrics), alert feed from planted scenarios.
2. **Ask OntologyOne** — chat; every answer shows collapsible generated governed SQL, Cortex Search evidence chips with citations, Trust Panel, export-to-PDF audit artifact.
3. **Ontology Explorer** — interactive entity graph (Supplier→Part→OrderLine→{Plant,Customer}→Shipment); click an entity → grain, PK, relationships, metrics using it, security policy.
4. **Trust & Lineage** — dynamic-table DAG (RAW_EDI → CORE_SHIPMENT → MART_OTD → SEMANTIC_VIEW), metric contract cards, and the **Governance Test Suite panel: "12/12 PASSED"** with the three-persona OTD assertion (91.4% = 91.4% = 91.4%).

---

## 8. EXECUTION SCHEDULE (12 days, extended-window calibrated)

**Day 1–2 — TRUTH (no Streamlit).**
Deliverables: approved ERD Artifact; `ontology/*.yml`; `data/generator.py` + S1–S5 planted; RAW→CORE dynamic tables; `MART_OTD_AGGREGATE`.
**Gate:** SQL worksheet proves correct Q3 OTD = 91.4% and S-017 = 81.7% exactly.

**Day 3–4 — GOVERNANCE.**
Deliverables: deploy `SUPPLY_SEMANTIC.sv.yaml` via CoCo CLI; roles + RAP + masking; verified queries wired.
**Gate:** three personas query "Q3 OTD" → identical value; drill-downs differ; S5 refusal works.

**Day 5–6 — AI.**
Deliverables: Cortex Agent (semantic tool + Search + custom instructions); docs corpus indexed; CoCo skills.
**Gate:** NL question → governed answer with contract + citations; S4 trap answered correctly (agent cites OTD_V1, rejects `is_delayed`).

**Day 7–8 — INVESTIGATION.**
Deliverables: anomaly_narrator skill; S1 full chain (metric→contributor→plants→shipments→SLA evidence→recommendations).
**Gate:** the entire Scene-3/4/5 demo script runs deterministically.

**Day 9–10 — COMMAND CENTER.**
Deliverables: 4 Streamlit screens deployed via CoCo CLI; Trust Panel; audit export.
**Gate:** screenshot review in Antigravity editor; deployed smoke test passes.

**Day 11 — TESTING (feature freeze).**
Deliverables: `make test-coco` suite — 12 tests: metric definition/calculation (OTD, FR, DOI), 3 relationship tests, 3 entitlement tests, cross-persona OTD consistency assertion, unauthorized-query rejection, S4 trap-response test.
**Gate:** 12/12 PASSED output screenshot (this becomes the demo closer).

**Day 12 — JUDGE OPTIMIZATION (no new features).**
Deliverables: README-as-narrative, architecture diagram, 2-min video, 5-min demo script, fallback screenshots, `demo/reset.sql`, `ONTO_JUDGE` role, one-command rebuild proof.

---

## 9. REPOSITORY LAYOUT (canonical — match exactly)

```
ontologyone/
├── README.md  ├─ Makefile  ├─ cortex-project.yml
├── ontology/ (entities.yml, relationships.yml, metric_contracts.yml, SUPPLY_SEMANTIC.sv.yaml)
├── data/ (generator.py, scenarios/{s1..s5}.py, fixtures/)
├── snowflake/ (01_database.sql … 07_agent.sql: database, raw, core, metrics mart, governance, cortex search, agent)
├── tests/ (metric/, ontology/, governance/, agent/, golden_queries/)
├── app/ (command_center.py, ontology_explorer.py, metric_dictionary.py, lineage.py, evidence.py)
├── cortex_project/ (agents/ontology_agent.yaml, skills/{metric_explainer, anomaly_narrator, lineage_explainer})
├── docs_corpus/ (SLA_S017.pdf, freight_agreement.pdf, legacy_metric_memo.txt, regional_policy.txt)
├── docs/ (architecture.md, ontology.md, metric_contracts.md, demo_script.md)
└── demo/ (scenario.json, reset.sql)
```

---

## 10. ANTAGRAVITY OPERATING MODEL (how Gemini 3.8 should run this)

- **Phase 0 (mandatory):** planning mode → emit ERD, metric contract table, scenario table as Artifacts → **wait for human approval** before any code.
- **Three persistent lanes in Agent Manager:** `data-layer`, `semantic-governance`, `app-demo`. One agent per lane; verification gate per lane per the schedule.
- **Browser-use agents for deployed checks:** log into Snowsight as each persona, run the identical question, screenshot each answer → consistency evidence pack for Demo Day.
- **Editor diffs:** all UI/generated-SQL changes reviewed as diffs in the Antigravity editor; never merge unreviewed.
- **Docs-grounded generation:** cite `snowflake-docs/` file + section for every generated Snowflake artifact in the plan output.

---

## 11. DEMO DAY SCRIPT (5:00 — memorize this as the spec)

- **0:00–0:30 The problem:** three dashboards — Procurement OTD 94.2%, Logistics 89.7%, Planning 92.1%. "Which number is correct?" (pause)
- **0:30–1:30 The proof:** OntologyOne, three personas, same question → 91.4%, 91.4%, 91.4%. Show Metric Contract OTD_V1. *(Optionally open with the anti-pattern: un-governed LLM + raw tables hallucinating SQL, then switch.)*
- **1:30–2:20 Governance:** persona asks for unauthorized data → refused, logged → "yet OTD remains identical."
- **2:20–3:30 Investigation:** "Why did OTD fall?" → 94.8%→91.4% → S-017 (81.7%), 3 plants, 428 shipments → shipment SH-93821 LATE.
- **3:30–4:10 Evidence:** Cortex Search cites SLA_S017 §4.2. Data Evidence + Business Evidence = explainable finding.
- **4:10–4:40 Action:** labeled AI-generated recommendations (expedite, reallocate P03→P07, supplier review, monitor <85%).
- **4:40–5:00 The mic drop:** Governance Test Suite 12/12 PASSED; Planner=Procurement=Logistics=91.4%. Closing line: **"We didn't teach an AI what the truth is. We gave the AI a governed definition of truth."**

---

## 12. PRIORITY HEATMAP (when in doubt, cut bottom-up)

🔥🔥🔥🔥🔥 Ontology · Metric Contracts · Semantic View · Governance proof · Golden queries · Investigation flow
🔥🔥🔥🔥 Cortex Agent · Cortex Search · Deterministic scenarios
🔥🔥🔥 Recommendations · 4-screen UI polish
🔥🔥 Dataset size · Extra metrics · Extra entities

---

## 13. START HERE (first agent actions)

1. Read `snowflake-docs/` fully; list any spec drift vs `SUPPLY_SEMANTIC.sv.yaml`.
2. Emit Phase-0 Artifacts (ERD, metric contracts, scenario table) for approval.
3. On approval, spawn `data-layer` agent on Day 1–2 scope; verify against the Gate before proceeding.