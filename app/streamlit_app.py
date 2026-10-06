"""
OntologyOne - Production Streamlit in Snowflake (SiS) Application
Snowflake CoCo CLI Hackathon (GCC Edition) - Track 5
Thesis: Same question -> same governed metric -> same calculation -> same answer -> different authorized context.
"""

import streamlit as st
import pandas as pd
import json
import time

from app.command_center import render_command_center
from app.ontology_explorer import render_ontology_explorer
from app.lineage import render_trust_and_lineage
from app.judge_room import render_judge_room
from app.evidence import get_evidence_for_query

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="OntologyOne — Governed Supply Chain Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Glassmorphic Dark UI Styling
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
}

code, pre {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Background gradient */
.stApp {
    background: radial-gradient(circle at 10% 20%, rgba(15, 23, 42, 1) 0%, rgba(2, 6, 23, 1) 90%);
    color: #f8fafc;
}

/* Persona badge */
.persona-badge {
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(56, 189, 248, 0.4);
    border-radius: 8px;
    padding: 8px 14px;
    color: #e0f2fe;
    font-size: 13px;
    display: inline-block;
    backdrop-filter: blur(8px);
}

/* KPI Cards */
.metric-card {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 18px;
    text-align: center;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.metric-card:hover {
    border-color: rgba(56, 189, 248, 0.5);
    transform: translateY(-2px);
}

.metric-title {
    color: #94a3b8;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 6px;
}
.metric-value {
    color: #f8fafc;
    font-size: 32px;
    font-weight: 800;
    margin: 8px 0;
}
.metric-delta.negative { color: #f87171; font-size: 13px; font-weight: 600; }
.metric-delta.positive { color: #34d399; font-size: 13px; font-weight: 600; }
.metric-delta.neutral { color: #38bdf8; font-size: 13px; font-weight: 600; }
.metric-subtext { color: #64748b; font-size: 11px; margin-top: 4px; }

.metric-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 10px;
    font-weight: 800;
}
.metric-badge.certified { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; }
.metric-badge.restricted { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #ef4444; }

/* Alert Boxes */
.alert-box {
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 12px;
    backdrop-filter: blur(8px);
}
.alert-crit {
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.35);
}
.alert-warn {
    background: rgba(245, 158, 11, 0.08);
    border: 1px solid rgba(245, 158, 11, 0.35);
}
.alert-notice {
    background: rgba(56, 189, 248, 0.08);
    border: 1px solid rgba(56, 189, 248, 0.35);
}

.badge-alert-crit { background: #ef4444; color: #fff; font-size: 10px; font-weight: 800; padding: 2px 8px; border-radius: 4px; }
.badge-alert-warn { background: #f59e0b; color: #fff; font-size: 10px; font-weight: 800; padding: 2px 8px; border-radius: 4px; }
.badge-alert-notice { background: #0284c7; color: #fff; font-size: 10px; font-weight: 800; padding: 2px 8px; border-radius: 4px; }

/* Evidence chips */
.evidence-chip {
    background: rgba(59, 130, 246, 0.15);
    border: 1px solid rgba(96, 165, 250, 0.4);
    border-radius: 8px;
    padding: 10px 14px;
    margin-top: 8px;
    color: #bfdbfe;
    font-size: 13px;
}

/* Trust Panel */
.trust-panel {
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid rgba(52, 211, 153, 0.4);
    border-radius: 10px;
    padding: 14px;
    margin: 12px 0;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION & PERSONA SWITCHER
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ ONTOLOGYONE")
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, rgba(56, 189, 248, 0.15) 0%, rgba(99, 102, 241, 0.2) 100%); 
                    border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 8px; padding: 10px; margin-bottom: 12px;'>
            <div style='color: #38bdf8; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;'>Snowflake CoCo Hackathon</div>
            <div style='color: #f8fafc; font-size: 14px; font-weight: 800; margin: 2px 0;'>Team Trailblazer 🚀</div>
            <div style='color: #94a3b8; font-size: 11px;'>Lead: <b>Tenali Radhika</b> (GCC Dev)</div>
            <div style='color: #34d399; font-size: 10px; font-weight: 700; margin-top: 4px;'>● Track: Supply Chain Ontology & Conversational Analytics</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    st.markdown("#### 👤 Active Persona Switcher")
    st.markdown(
        "<span style='color:#cbd5e1; font-size:12px;'>Demonstrating the RAP Paradox Fix:</span>",
        unsafe_allow_html=True
    )

    persona_choice = st.radio(
        "Select User Persona:",
        [
            "Demand Planner (ONTO_PLANNER)",
            "Procurement Lead (ONTO_PROCUREMENT)",
            "Logistics Admin (ONTO_LOGISTICS)",
            "Hackathon Judge (ONTO_JUDGE)"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown("#### 📱 Application Screens")
    screen_choice = st.radio(
        "Navigate to:",
        [
            "1. Command Center",
            "2. Ask OntologyOne (Governed Chat)",
            "3. Ontology Explorer",
            "4. Trust & Lineage",
            "5. Hackathon Judge Room ⚖️"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown("#### ⚡ Core Thesis")
    st.markdown(
        "<div style='font-size:11px; color:#94a3b8; line-height:1.4; font-style:italic;'>"
        "\"Same question → same governed metric → same calculation → same answer → different authorized context.\""
        "</div>",
        unsafe_allow_html=True
    )

# -----------------------------------------------------------------------------
# ROUTER: 4 STREAMLIT SCREENS
# -----------------------------------------------------------------------------
if screen_choice == "1. Command Center":
    render_command_center(persona_choice)

elif screen_choice == "2. Ask OntologyOne (Governed Chat)":
    st.markdown("## 💬 Ask OntologyOne — Governed Conversational Intelligence")
    st.markdown(
        f"<div class='persona-badge'>Active Persona: <b>{persona_choice}</b> | Truth Compiler: <b>Active</b></div>",
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # Demo Day Quick Prompts
    st.markdown("##### ⚡ Quick Scenarios (Click to execute deterministic demo query):")
    c1, c2, c3, c4 = st.columns(4)
    quick_prompt = None

    with c1:
        if st.button("🔥 S1: Why did OTD fall?", use_container_width=True):
            quick_prompt = "Why did our company On-Time Delivery rate fall in Q3 2026?"
    with c2:
        if st.button("🏭 S2: Plant P03 Fill Rate", use_container_width=True):
            quick_prompt = "What is the order fill rate for manufacturing plant P03?"
    with c3:
        if st.button("⚠️ S4: Query legacy is_delayed (TRAP)", use_container_width=True):
            quick_prompt = "Can you query raw_orders.is_delayed to see delayed orders?"
    with c4:
        if st.button("🔒 S5: Request Part Costs (SECURITY)", use_container_width=True):
            quick_prompt = "Show me the unit costs and landed spend for all parts supplied by S-017."

    # Chat Input
    user_query = st.text_input(
        "Ask a supply chain operational question:",
        value=quick_prompt if quick_prompt else "Why did our company On-Time Delivery rate fall in Q3 2026?"
    )

    if st.button("🔍 Run Governed Analysis", type="primary") or quick_prompt:
        with st.spinner("Truth Compiler: Compiling business intent to governed metric contract..."):
            time.sleep(0.3)
            evidence = get_evidence_for_query(user_query, persona_choice)

            # Finding Header
            st.markdown(f"### {evidence['title']}")
            st.markdown(evidence["narrative"])

            # Evidence Taxonomy (Two Panels: Data Evidence + Business Evidence)
            st.markdown("<br>#### 🧩 Evidence Taxonomy", unsafe_allow_html=True)
            col_data, col_biz = st.columns([1, 1])

            with col_data:
                st.markdown("##### 📊 Data Evidence (Structured Rows & Dates)")
                if "data_evidence" in evidence:
                    st.json(evidence["data_evidence"])
                else:
                    st.info(f"Verified rows pulled from `{evidence['metric_contract']}` certified mart.")

            with col_biz:
                st.markdown("##### 📑 Business Evidence (Cortex Search Document Citations)")
                for cite in evidence.get("citations", []):
                    st.markdown(
                        f"""
                        <div class='evidence-chip'>
                            <b>Document:</b> <code>{cite['doc']}</code> — <i>{cite['title']}</i><br>
                            <b>Excerpt:</b> "{cite['excerpt']}"
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            # Labeled AI Recommendations
            st.markdown("<br>#### 🤖 Actionable Recommendations", unsafe_allow_html=True)
            for rec in evidence.get("recommendations", []):
                st.markdown(f"- **{rec}**")

            # Trust Panel (Collapsible)
            with st.expander("🛡️ Trust Panel — Governed Metric Lineage & Security", expanded=True):
                st.markdown(
                    f"""
                    <div class='trust-panel'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <span style='background:#059669; color:#fff; font-weight:700; padding:2px 10px; border-radius:4px; font-size:12px;'>
                                [✓ {evidence['grounded_badge']}]
                            </span>
                            <span style='color:#94a3b8; font-size:12px;'>Audit Log ID: <code>LOG-{int(time.time())}</code></span>
                        </div>
                        <div style='margin-top:10px; font-size:13px; color:#e2e8f0;'>
                            <b>Metric Contract:</b> <code>{evidence['metric_contract']}</code> | 
                            <b>Active Persona:</b> <code>{persona_choice.split()[0]}</code> | 
                            <b>Semantic View:</b> <code>CORE.SUPPLY_SEMANTIC</code>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown("**Generated Governed SQL:**")
                st.code(evidence["sql"], language="sql")

            # Export Audit Artifact
            audit_artifact = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC"),
                "persona": persona_choice,
                "user_prompt": user_query,
                "metric_contract": evidence["metric_contract"],
                "generated_sql": evidence["sql"],
                "evidence_citations": [c["doc"] for c in evidence.get("citations", [])],
                "grounding_status": evidence["grounded_badge"]
            }
            st.download_button(
                "📥 Export Signed Governance Audit Artifact (JSON)",
                data=json.dumps(audit_artifact, indent=2),
                file_name=f"audit_artifact_{int(time.time())}.json",
                mime="application/json"
            )

elif screen_choice == "3. Ontology Explorer":
    render_ontology_explorer()

elif screen_choice == "4. Trust & Lineage":
    render_trust_and_lineage()

elif screen_choice == "5. Hackathon Judge Room ⚖️":
    render_judge_room()
