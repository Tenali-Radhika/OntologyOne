"""
Screen 1: Command Center
Persona switcher, KPI cards (certified metrics), alert feed from planted scenarios.
"""
import streamlit as st
import pandas as pd
import os

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "fixtures")

def render_command_center(persona: str):
    st.markdown("## 🧭 Supply Chain Executive Command Center")
    st.markdown(
        f"<div class='persona-badge'>Active Role: <b>{persona}</b> | Environment: <b>ONTO_HACKATHON (Production Governed)</b></div>",
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # Certified KPI Cards (Two-Tier Truth Architecture)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div class='metric-card'>
                <div class='metric-badge certified'>CERTIFIED: OTD_V1</div>
                <div class='metric-title'>On-Time Delivery Rate</div>
                <div class='metric-value'>91.4%</div>
                <div class='metric-delta negative'>▼ -3.4% vs Q2 (94.8%)</div>
                <div class='metric-subtext'>Certified RAP-Unrestricted Mart</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class='metric-card'>
                <div class='metric-badge certified'>CERTIFIED: FR_V1</div>
                <div class='metric-title'>Order Fill Rate</div>
                <div class='metric-value'>88.9%</div>
                <div class='metric-delta positive'>▲ +0.5% vs SLA Target</div>
                <div class='metric-subtext'>Granular Lineage via Order Lines</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class='metric-card'>
                <div class='metric-badge certified'>CERTIFIED: DOI_V1</div>
                <div class='metric-title'>Days of Inventory</div>
                <div class='metric-value'>29.2 Days</div>
                <div class='metric-delta neutral'>● Optimal Buffer Range</div>
                <div class='metric-subtext'>Rolling 30-Day Usage Model</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        # Cost visibility depends on persona
        is_procurement = "Procurement" in persona or "Judge" in persona
        cost_val = "$184.20" if is_procurement else "***CONFIDENTIAL***"
        cost_sub = "Unmasked (Authorized Role)" if is_procurement else "Masked by GOV.MASK_COST_DATA"
        st.markdown(
            f"""
            <div class='metric-card'>
                <div class='metric-badge {"certified" if is_procurement else "restricted"}'>
                    {"CERTIFIED: LC_V1" if is_procurement else "RESTRICTED: LC_V1"}
                </div>
                <div class='metric-title'>Avg Landed Cost / SKU</div>
                <div class='metric-value'>{cost_val}</div>
                <div class='metric-delta {"neutral" if is_procurement else "negative"}'>
                    {"Baseline Tracked" if is_procurement else "Access Prohibited"}
                </div>
                <div class='metric-subtext'>{cost_sub}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Operational Alert Feed from Planted Scenarios
    st.markdown("### 🚨 Live Operational Alert Feed (Governed Anomaly Triggers)")

    alerts = [
        {
            "id": "ALERT-S1",
            "level": "CRITICAL",
            "scenario": "Scenario S1",
            "title": "Severe Supplier Delivery Deterioration: MicroCore Silicon Dynamics (S-017)",
            "description": "Supplier S-017 OTD crashed from 96.2% to 81.7% in Q3 over 8 weeks. Impacting 3 plants (P03, P07, P09), 17 parts, and 428 late shipments. Drives global OTD down to 91.4%.",
            "action": "Trigger vendor review under SLA §2.2 default provisions; expedite 84 shipments.",
            "doc": "SLA_S017.pdf §4.2"
        },
        {
            "id": "ALERT-S2",
            "level": "WARNING",
            "scenario": "Scenario S2",
            "title": "Manufacturing Facility Fill Rate Deficit: Plant P03 (Midwest)",
            "description": "Plant P03 fill rate dropped to 74.2% (below 88.0% minimum operational SLA) due to component starvation. Plant P07 maintains 24% unutilized staging capacity.",
            "action": "Initiate cross-facility order reallocation from P03 to P07 per SOP-OPS-REG-04.",
            "doc": "regional_policy.txt §3"
        },
        {
            "id": "ALERT-S3",
            "level": "NOTICE",
            "scenario": "Scenario S3",
            "title": "Intermodal Freight Surcharge Spike: Corridor LANE-NW-04",
            "description": "Transit corridor LANE-NW-04 landed freight expenses surged +30% following maritime port congestion trigger.",
            "action": "Audit carrier invoices under §3 provisions or reroute container traffic to rail spur.",
            "doc": "freight_agreement.pdf §2.1"
        }
    ]

    for alert in alerts:
        level_class = "alert-crit" if alert["level"] == "CRITICAL" else ("alert-warn" if alert["level"] == "WARNING" else "alert-notice")
        st.markdown(
            f"""
            <div class='alert-box {level_class}'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <span class='badge-{level_class}'>{alert["level"]}</span>
                    <span style='color:#94a3b8; font-size:12px;'>{alert["scenario"]} | Citation: <code>{alert["doc"]}</code></span>
                </div>
                <div style='font-size:16px; font-weight:700; margin:8px 0; color:#f8fafc;'>{alert["title"]}</div>
                <div style='color:#cbd5e1; font-size:13px; line-height:1.5;'>{alert["description"]}</div>
                <div style='margin-top:10px; padding-top:8px; border-top:1px solid rgba(255,255,255,0.08); font-size:12px; color:#38bdf8;'>
                    <b>Prescribed Action:</b> {alert["action"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Quarterly Performance Decomposition Chart
    st.markdown("<br>### 📊 Certified OTD Trend Decomposition (2026-Q2 vs 2026-Q3)")
    trend_data = pd.DataFrame({
        "Period": ["2026-Q2 Baseline", "2026-Q3 Overall", "2026-Q3 S-017 (Deteriorated)", "2026-Q3 Non-S017 Suppliers"],
        "OTD Rate (%)": [94.8, 91.4, 81.7, 94.4],
        "Category": ["Certified Target", "Current Reality", "Root Cause Causal Node", "Healthy Base"]
    })
    st.bar_chart(trend_data.set_index("Period")["OTD Rate (%)"])
