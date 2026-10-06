"""
Screen 3: Ontology Explorer
Interactive entity graph (Supplier -> Part -> OrderLine -> {Plant, Customer} -> Shipment)
Click/select entity -> grain, PK, relationships, metrics using it, security policy.
"""
import streamlit as st
import yaml
import os

def render_ontology_explorer():
    st.markdown("## 🕸️ Supply Chain Ontology Explorer")
    st.markdown(
        "Interactive topology graph mapping the 6 enterprise MVP entities, their foreign keys, "
        "and metric contracts binding structured truth to operational execution."
    )

    # Visual Entity Graph Representation using Mermaid and Cards
    st.markdown("### Entity Topology Graph")
    st.markdown(
        """
```mermaid
graph LR
    SUPPLIER[SUPPLIER<br>50 Vendors] -->|supplies| PART[PART<br>200 SKUs]
    PART -->|ordered_in| ORDER_LINE[ORDER_LINE<br>15,000 Lines]
    PLANT[PLANT<br>12 Hubs] -->|fulfills| ORDER_LINE
    CUSTOMER[CUSTOMER<br>500 Accounts] -->|places| ORDER_LINE
    ORDER_LINE -->|shipped_via| SHIPMENT[SHIPMENT<br>15,000 Freight Moves]

    classDef primary fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;
    class SUPPLIER,PART,PLANT,CUSTOMER,ORDER_LINE,SHIPMENT primary;
```
        """
    )

    st.markdown("---")
    st.markdown("### Entity Inspector")

    entities_data = {
        "SUPPLIER": {
            "name": "SUPPLIER",
            "icon": "🏭",
            "grain": "Discrete Commercial Vendor",
            "primary_key": "supplier_id (e.g. S-001, S-017)",
            "record_count": "50 active vendors",
            "attributes": ["supplier_id", "supplier_name", "tier (Tier 1/2/3)", "country", "risk_level (Low/Med/High/Crit)"],
            "relationships": [
                "SUPPLIER supplies PART (1 : N, condition: SUPPLIER.supplier_id = PART.supplier_id)"
            ],
            "metrics": ["OTD_V1 (Supplier aggregation)", "Supplier Risk Index"],
            "security_policy": "Supplier name protected; cost data restricted."
        },
        "PART": {
            "name": "PART",
            "icon": "⚙️",
            "grain": "Discrete Component SKU",
            "primary_key": "part_id (e.g. PART-MCU-101)",
            "record_count": "200 parts (17 supplied by S-017)",
            "attributes": ["part_id", "part_name", "category", "unit_cost (Float)", "supplier_id (FK)"],
            "relationships": [
                "PART supplies ORDER_LINE (1 : N)",
                "SUPPLIER supplies PART (N : 1)"
            ],
            "metrics": ["Landed Cost (LC_V1)", "Days of Inventory (DOI_V1)"],
            "security_policy": "STRICT MASKING: unit_cost is masked as ***CONFIDENTIAL*** to non-Procurement roles."
        },
        "PLANT": {
            "name": "PLANT",
            "icon": "🏢",
            "grain": "Internal Manufacturing Campus",
            "primary_key": "plant_id (e.g. P01, P03, P07, P09)",
            "record_count": "12 facilities across North America, EMEA, APAC",
            "attributes": ["plant_id", "plant_name", "region", "country"],
            "relationships": [
                "PLANT fulfills ORDER_LINE (1 : N)"
            ],
            "metrics": ["Order Fill Rate (FR_V1)", "Plant Utilization", "Staging Line Capacity"],
            "security_policy": "Logistics personas filtered by operating region via RAP_ORDER_LINE."
        },
        "CUSTOMER": {
            "name": "CUSTOMER",
            "icon": "👥",
            "grain": "Purchasing Enterprise Account",
            "primary_key": "customer_id (e.g. CUST-1001)",
            "record_count": "500 enterprise customers",
            "attributes": ["customer_id", "customer_name", "segment (Strategic/Enterprise)", "region"],
            "relationships": [
                "CUSTOMER places ORDER_LINE (1 : N)"
            ],
            "metrics": ["Customer SLA Punctuality (OTD_V1)", "Customer Fill Rate"],
            "security_policy": "Standard enterprise visibility across planning roles."
        },
        "ORDER_LINE": {
            "name": "ORDER_LINE",
            "icon": "📋",
            "grain": "Discrete Purchase Order Requisition Line",
            "primary_key": "order_line_id (e.g. OL-000001)",
            "record_count": "15,000 line items",
            "attributes": ["order_line_id", "order_id", "part_id (FK)", "plant_id (FK)", "customer_id (FK)", "quantity_ordered", "quantity_fulfilled", "order_date", "promised_date", "is_delayed_legacy (TRAP)"],
            "relationships": [
                "ORDER_LINE shipped_via SHIPMENT (1 : N)",
                "PART ordered_in ORDER_LINE (N : 1)",
                "PLANT fulfills ORDER_LINE (N : 1)"
            ],
            "metrics": ["Order Fill Rate (FR_V1)", "Promised Date Compliance"],
            "security_policy": "Governed by RAP_ORDER_LINE based on user role and plant assignment."
        },
        "SHIPMENT": {
            "name": "SHIPMENT",
            "icon": "🚚",
            "grain": "Outbound Freight Consignment / Bill of Lading",
            "primary_key": "shipment_id (e.g. SH-93821)",
            "record_count": "15,000 shipments",
            "attributes": ["shipment_id", "order_line_id (FK)", "carrier_id", "lane_id (e.g. LANE-NW-04)", "ship_date", "delivery_date", "promised_date", "delivery_status", "freight_cost"],
            "relationships": [
                "ORDER_LINE shipped_via SHIPMENT (N : 1)"
            ],
            "metrics": ["Flagship OTD_V1", "Landed Freight Cost (LC_V1)", "Carrier Punctuality"],
            "security_policy": "freight_cost dynamically masked by GOV.MASK_COST_DATA."
        }
    }

    selected_entity = st.selectbox(
        "Select an Entity to inspect metadata, relationships, and governance:",
        options=list(entities_data.keys()),
        index=0
    )

    data = entities_data[selected_entity]

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(
            f"""
            <div class='metric-card' style='text-align:left;'>
                <div style='font-size:20px; font-weight:800; color:#38bdf8;'>{data["icon"]} {data["name"]}</div>
                <div style='color:#94a3b8; font-size:13px; margin-bottom:12px;'>Grain: {data["grain"]}</div>
                <p><b>Primary Key:</b> <code>{data["primary_key"]}</code></p>
                <p><b>Total Catalog Volume:</b> {data["record_count"]}</p>
                <p><b>Security & RAP Policy:</b> <span style='color:#f59e0b;'>{data["security_policy"]}</span></p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown("#### Attributes & Data Dictionary")
        st.write(data["attributes"])

        st.markdown("#### Bound Relationships")
        for rel in data["relationships"]:
            st.markdown(f"- 🔗 `{rel}`")

        st.markdown("#### Certified Metrics Dependent on this Entity")
        for m in data["metrics"]:
            st.markdown(f"- 📈 **{m}**")
