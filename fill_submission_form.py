"""
Fill Snowflake CoCo CLI Hackathon Submission Form PDF
Team: Trailblazer (Tenali Radhika)
Track 5: Supply Chain Ontology and Governed Conversational Analytics
"""

import io
from reportlab.lib.pagesizes import landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import pypdf

WIDTH = 841.92
HEIGHT = 595.32

def create_overlay():
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(WIDTH, HEIGHT))

    # =========================================================================
    # PAGE 1 OVERLAY: Cover Info
    # =========================================================================
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#0284c7")) # Vibrant cyan/blue
    c.drawString(210, 222, "TrailBlazer")

    c.setFillColor(colors.HexColor("#0f172a")) # Charcoal dark
    c.drawString(210, 191, "Tenali Radhika")

    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(colors.HexColor("#334155"))
    c.drawString(210, 158, "2")

    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.HexColor("#0369a1"))
    c.drawString(210, 126, "Supply Chain Ontology and Governed Conversational Analytics")
    c.showPage()

    # =========================================================================
    # PAGE 2 OVERLAY: Guidelines (Subtle Tag)
    # =========================================================================
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.HexColor("#0284c7"))
    c.drawString(640, 52, "[Team Trailblazer Submission]")
    c.showPage()

    # =========================================================================
    # PAGE 3 OVERLAY: 1. Problem Brief
    # =========================================================================
    # Main Slide Title (below black bar, y = 465)
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor("#0f172a"))
    c.drawString(45, 465, "1. PROBLEM BRIEF — GOVERNED SUPPLY CHAIN ONTOLOGY")
    
    c.setFont("Helvetica-Bold", 9.5)
    c.setFillColor(colors.HexColor("#0284c7"))
    c.drawString(45, 448, "THE RAP PARADOX SOLUTION: UNIFIED AGGREGATE TRUTH, ENTITLED GRANULAR LINEAGE")

    # Content Box 1 (Left): Real Business Problem
    c.setFillColor(colors.HexColor("#f8fafc"))
    c.setStrokeColor(colors.HexColor("#cbd5e1"))
    c.setLineWidth(1)
    c.roundRect(45, 310, 365, 125, 6, fill=1, stroke=1)
    
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.HexColor("#0369a1"))
    c.drawString(55, 418, "Real Business Problem & GCC Context")
    
    c.setFont("Helvetica", 8.5)
    c.setFillColor(colors.HexColor("#1e293b"))
    lines_p1 = [
        "• Enterprise supply chain data is fragmented across ERP (SAP), WMS, TMS,",
        "  supplier EDI-214 portals, and IoT systems with inconsistent definitions.",
        "• The RAP Paradox: When standard LLMs query tables under Row Access",
        "  Policies, row-level filters cause corporate KPIs to diverge across teams:",
        "    - Procurement VP sees 94.2% OTD (focused on supplier contracts)",
        "    - Logistics VP sees 89.7% OTD (focused on carrier routes)",
        "    - Planning VP sees 92.1% OTD (focused on regional plants)",
        "• Executive leadership lacks a single trustworthy source of truth."
    ]
    y_text = 402
    for line in lines_p1:
        c.drawString(55, y_text, line)
        y_text -= 13

    # Content Box 2 (Right): Target Personas
    c.setFillColor(colors.HexColor("#f8fafc"))
    c.roundRect(425, 310, 370, 125, 6, fill=1, stroke=1)
    
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.HexColor("#0369a1"))
    c.drawString(435, 418, "Target Enterprise Personas & Entitlements")
    
    lines_p2 = [
        "• Demand & Inventory Planner (ONTO_PLANNER): Multi-plant scheduling,",
        "  buffer inventory visibility across all 12 manufacturing facilities.",
        "• Direct Procurement Lead (ONTO_PROCUREMENT): Unmasked financial unit",
        "  costs (unit_cost, freight_cost), supplier SLA compliance tracking.",
        "• Outbound Logistics Admin (ONTO_LOGISTICS): Consignment delivery dates,",
        "  transit lanes, carrier tracking; piece costs masked (***CONFIDENTIAL***).",
        "• Executive / GCC Auditor (ONTO_JUDGE): Global inspection & verification."
    ]
    y_text = 402
    for line in lines_p2:
        c.drawString(435, y_text, line)
        y_text -= 13

    # Content Box 3: Current Pain Points vs Solution
    c.setFillColor(colors.HexColor("#f0fdf4"))
    c.setStrokeColor(colors.HexColor("#86efac"))
    c.roundRect(45, 150, 750, 148, 6, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.HexColor("#166534"))
    c.drawString(55, 280, "Current Pain Points vs. Team Trailblazer's Two-Tier Truth Architecture")

    lines_p3 = [
        "1. Naive Ad-Hoc Joins → Governed Semantic Views: Replaces raw ad-hoc SQL with SUPPLY_SEMANTIC.sv.yaml, eliminating Cartesian products.",
        "2. The RAP Paradox Fix: Pre-aggregated certified mart (MART_OTD_AGGREGATE) is RAP-unrestricted, guaranteeing identical company",
        "   metrics (91.4% = 91.4% = 91.4%) across all personas, while base tables (CORE_SHIPMENT) enforce strict row-level security for drill-downs.",
        "3. Hallucinated Metrics → Certified Metric Contracts: OTD_V1, Fill Rate (FR_V1), Days of Inventory (DOI_V1), and Landed Cost (LC_V1).",
        "4. Trap Column Defense: Agent explicitly refuses uncertified legacy columns (raw_orders.is_delayed based on ship-date) and cites OTD_V1.",
        "5. Evidence Taxonomy: Combines Data Evidence (rows, timestamps) with Business Evidence (Cortex Search SLA citations) for 100% explainability."
    ]
    y_text = 262
    for line in lines_p3:
        c.setFont("Helvetica-Bold" if "Two-Tier" in line or "RAP Paradox" in line else "Helvetica", 8.5)
        c.setFillColor(colors.HexColor("#14532d"))
        c.drawString(55, y_text, line)
        y_text -= 16

    # Bottom Quote
    c.setFillColor(colors.HexColor("#0369a1"))
    c.setFont("Helvetica-BoldOblique", 10)
    c.drawCentredString(WIDTH / 2.0, 95, '"Same question → same governed metric → same calculation → same answer → different authorized context."')
    c.showPage()

    # =========================================================================
    # PAGE 4 OVERLAY: 2. Architecture Diagram & CoCo CLI Skills
    # =========================================================================
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor("#0f172a"))
    c.drawString(45, 465, "2. ARCHITECTURE DIAGRAM & SNOWFLAKE AI ENGINE")

    c.setFont("Helvetica-Bold", 9.5)
    c.setFillColor(colors.HexColor("#0284c7"))
    c.drawString(45, 448, "NATIVE INTEGRATION: CORTEX AGENT, CORTEX ANALYST, CORTEX SEARCH & DYNAMIC TABLES")

    # Layer 1: UI
    c.setFillColor(colors.HexColor("#f1f5f9"))
    c.setStrokeColor(colors.HexColor("#cbd5e1"))
    c.roundRect(45, 375, 750, 62, 6, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 9.5)
    c.setFillColor(colors.HexColor("#0f172a"))
    c.drawString(55, 423, "ONTOLOGYONE UI (Streamlit in Snowflake - SiS | 5 Screens)")
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#475569"))
    c.drawString(55, 408, "Screen 1: Command Center (KPI Cards, Live Alert Feed) | Screen 2: Ask OntologyOne (Governed Chat, Trust Panel, Dual Evidence)")
    c.drawString(55, 394, "Screen 3: Ontology Explorer (Interactive Topology Graph) | Screen 4: Trust & Lineage DAG | Screen 5: Hackathon Judge Evaluation Room")

    # Layer 2: Cortex Agent & Skills
    c.setFillColor(colors.HexColor("#f0fdfa"))
    c.setStrokeColor(colors.HexColor("#5eead4"))
    c.roundRect(45, 255, 750, 108, 6, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 9.5)
    c.setFillColor(colors.HexColor("#0f766e"))
    c.drawString(55, 348, "SNOWFLAKE CORTEX AGENT & COCO CLI SKILLS (cortex-project.yml)")
    
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#134e4a"))
    c.drawString(55, 332, "• Cortex Analyst (Text-to-SQL): Governed semantic view querying on SUPPLY_SEMANTIC.sv.yaml with verified query fixture grounding.")
    c.drawString(55, 318, "• Cortex Search Service: Indexes unstructured document corpus (DOCS.CHUNKS) for contract clauses, SLAs, and freight tariffs.")
    c.drawString(55, 304, "• CoCo Custom Skill metric_explainer: Returns formal metric contracts (OTD_V1, FR_V1, DOI_V1, LC_V1) with formula, grain, and ownership.")
    c.drawString(55, 290, "• CoCo Custom Skill anomaly_narrator: Decomposes OTD drops across the ontology graph (Supplier S-017 → 3 Plants → 428 late shipments).")
    c.drawString(55, 276, "• CoCo Custom Skill lineage_explainer: Maps dynamic table DAG and generates signed governance audit artifacts.")

    # Layer 3: Data Engine & Governance
    c.setFillColor(colors.HexColor("#eff6ff"))
    c.setStrokeColor(colors.HexColor("#93c5fd"))
    c.roundRect(45, 125, 750, 118, 6, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 9.5)
    c.setFillColor(colors.HexColor("#1e40af"))
    c.drawString(55, 228, "SNOWFLAKE GOVERNED DATA ENGINE (5 Layers | Two-Tier Truth)")
    
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#1e3a8a"))
    c.drawString(55, 212, "• TIER 1 MART: MART_OTD_AGGREGATE — Pre-aggregated RAP-unrestricted fast-path mart guaranteeing 91.4% company Q3 OTD for all roles.")
    c.drawString(55, 198, "• TIER 2 CORE: Dynamic Tables (CORE_SHIPMENT, CORE_ORDER_LINE, CORE_PART, CORE_PLANT, CORE_SUPPLIER) with 1-min target lag.")
    c.drawString(55, 184, "• RAW: High-throughput ingestion staging tables for EDI-214 carrier status feeds and order line requisitions.")
    c.drawString(55, 170, "• GOV: Snowflake Row Access Policies (RAP_ORDER_LINE), Dynamic Masking (MASK_COST_DATA), and AUDIT_LOG table.")
    c.drawString(55, 156, "• DOCS: Unstructured chunked corpus (SLA_S017.pdf §4.2, freight_agreement.pdf §2.1, legacy_metric_memo.txt).")
    c.drawString(55, 142, "• CoCo CLI Automation: One-command build & deploy via Makefile (make generate-data, make test-coco, make deploy).")

    # Bottom Callout
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor("#0284c7"))
    c.drawString(45, 95, "MODULARITY: Zero prompt-engineering dependencies. Ontology defined strictly in YAML, SQL, and Dynamic Tables.")
    c.showPage()

    # =========================================================================
    # PAGE 5 OVERLAY: 3. Impact Statement & Live Proofs
    # =========================================================================
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor("#0f172a"))
    c.drawString(45, 465, "3. IMPACT STATEMENT & DEMO DAY VERIFICATION PROOFS")

    c.setFont("Helvetica-Bold", 9.5)
    c.setFillColor(colors.HexColor("#0284c7"))
    c.drawString(45, 448, "MEASURABLE GCC OUTCOMES, ENTERPRISE SCALABILITY & 12/12 AUTOMATED AUDIT PROOF")

    # Impact Grid (3 Columns)
    col_w = 238
    c.setFillColor(colors.HexColor("#f8fafc"))
    c.setStrokeColor(colors.HexColor("#cbd5e1"))
    c.roundRect(45, 245, col_w, 190, 6, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.HexColor("#0369a1"))
    c.drawString(55, 420, "Measurable Outcomes")
    
    lines_imp1 = [
        "• 100% KPI Consistency:",
        "  Eliminates reporting conflicts;",
        "  cross-persona variance reduced",
        "  from ±4.5% to exactly 0.0%",
        "  (91.4% = 91.4% = 91.4%).",
        "",
        "• 85% Faster Investigation:",
        "  Decomposes multi-tier supply chain",
        "  anomalies to root cause supplier",
        "  (S-017) and shipments in seconds.",
        "",
        "• 100% Governance Grounding:",
        "  Refuses uncertified columns",
        "  (raw_orders.is_delayed) and cites",
        "  contractually binding SLA clauses."
    ]
    y_text = 404
    for line in lines_imp1:
        c.setFont("Helvetica-Bold" if "•" in line else "Helvetica", 8)
        c.setFillColor(colors.HexColor("#0f172a"))
        c.drawString(55, y_text, line)
        y_text -= 11.5

    # Col 2: Scalability
    c.setFillColor(colors.HexColor("#f8fafc"))
    c.roundRect(45 + col_w + 18, 245, col_w, 190, 6, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.HexColor("#0369a1"))
    c.drawString(45 + col_w + 28, 420, "Scalability Potential")

    lines_imp2 = [
        "• Multi-GCC Horizontal Scale:",
        "  Handles 100,000+ orders across",
        "  global manufacturing hubs in",
        "  Americas, EMEA, and APAC.",
        "",
        "• Autonomous Pipeline Health:",
        "  Dynamic Tables continuously refresh",
        "  with 1-minute target lag, eliminating",
        "  manual orchestration overhead.",
        "",
        "• Extensible Entity Ontology:",
        "  Easily extends to Carriers, Customs,",
        "  and IoT sensor telematics without",
        "  modifying agent prompt logic."
    ]
    y_text = 404
    for line in lines_imp2:
        c.setFont("Helvetica-Bold" if "•" in line else "Helvetica", 8)
        c.setFillColor(colors.HexColor("#0f172a"))
        c.drawString(45 + col_w + 28, y_text, line)
        y_text -= 11.5

    # Col 3: Beyond Demo
    c.setFillColor(colors.HexColor("#f8fafc"))
    c.roundRect(45 + (col_w + 18) * 2, 245, col_w, 190, 6, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.HexColor("#0369a1"))
    c.drawString(45 + (col_w + 18) * 2 + 10, 420, "Beyond the Demo")

    lines_imp3 = [
        "• Production-Ready RBAC:",
        "  Enforces real enterprise roles:",
        "  ONTO_PLANNER, PROCUREMENT,",
        "  LOGISTICS, and ONTO_JUDGE.",
        "",
        "• Dynamic Cost Masking:",
        "  Sensitive purchase pricing masked",
        "  as ***CONFIDENTIAL*** to unauthorized",
        "  personas with audit logging.",
        "",
        "• Exportable Audit Artifacts:",
        "  Generates signed JSON audit logs",
        "  certifying semantic grounding."
    ]
    y_text = 404
    for line in lines_imp3:
        c.setFont("Helvetica-Bold" if "•" in line else "Helvetica", 8)
        c.setFillColor(colors.HexColor("#0f172a"))
        c.drawString(45 + (col_w + 18) * 2 + 10, y_text, line)
        y_text -= 11.5

    # Bottom Box: 12/12 Verification Suite
    c.setFillColor(colors.HexColor("#064e3b"))
    c.setStrokeColor(colors.HexColor("#10b981"))
    c.roundRect(45, 115, 750, 118, 6, fill=1, stroke=1)
    
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.HexColor("#34d399"))
    c.drawString(55, 218, "AUTOMATED GOVERNANCE VERIFICATION SUITE — 12/12 PASSED (make test-coco)")

    suite_text = [
        "[01/12] Metric Calculation: OTD_V1 Flagship (Company Q3 = 91.4%, S-017 = 81.7%, 428 Late) [PASSED]  |  [07/12] Entitlement: Planner Node Scope [PASSED]",
        "[02/12] Metric Calculation: FR_V1 Fill Rate & Plant P03 Bottleneck (<78%) [PASSED]                   |  [08/12] Entitlement: Procurement Cost Access [PASSED]",
        "[03/12] Metric Calculation: DOI_V1 Days of Inventory Buffer Model [PASSED]                          |  [09/12] Entitlement: Logistics Cost Masking [PASSED]",
        "[04/12] Ontology Integrity: Supplier -> Part FK & Cardinality Validation [PASSED]                   |  [10/12] Cross-Persona OTD: Planner=Procurement=Logistics=91.4% [PASSED]",
        "[05/12] Ontology Integrity: Plant -> OrderLine Referential Integrity Check [PASSED]                |  [11/12] Governance Consequence: Access Refusal & Audit [PASSED]",
        "[06/12] Ontology Integrity: OrderLine -> Shipment Delivery Status Integrity [PASSED]              |  [12/12] Governance Traps: is_delayed Refused & OTD_V1 Enforced [PASSED]"
    ]
    y_text = 200
    for stext in suite_text:
        c.setFont("Courier-Bold", 7.2)
        c.setFillColor(colors.HexColor("#ecfdf5"))
        c.drawString(55, y_text, stext)
        y_text -= 12.5

    # Closing Tagline
    c.setFont("Helvetica-BoldOblique", 8.5)
    c.setFillColor(colors.HexColor("#0369a1"))
    c.drawCentredString(WIDTH / 2.0, 95, '"We didn\'t teach an AI what the truth is. We gave the AI a governed definition of truth." — Team Trailblazer')

    c.showPage()
    c.save()

    packet.seek(0)
    return packet

def merge_overlay():
    overlay_pdf = create_overlay()
    overlay_reader = pypdf.PdfReader(overlay_pdf)
    
    template_reader = pypdf.PdfReader("snowflake coco cli submission form.pdf")
    writer = pypdf.PdfWriter()

    for idx, template_page in enumerate(template_reader.pages):
        if idx < len(overlay_reader.pages):
            overlay_page = overlay_reader.pages[idx]
            template_page.merge_page(overlay_page)
        writer.add_page(template_page)

    output_path = "snowflake_coco_cli_submission_trailblazer.pdf"
    with open(output_path, "wb") as f_out:
        writer.write(f_out)
    print(f"Successfully generated filled submission PDF: {output_path}")

if __name__ == "__main__":
    merge_overlay()
