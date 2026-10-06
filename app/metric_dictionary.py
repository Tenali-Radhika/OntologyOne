"""
Metric Contracts Dictionary component
"""
import streamlit as st
import yaml
import os

def render_metric_contracts():
    st.markdown("### 📜 Certified Metric Contracts Registry")
    st.markdown(
        "**Core Rule:** *One definition per metric.* Zero recomputations across dashboards or agents."
    )

    contracts_file = os.path.join(os.path.dirname(__file__), "..", "ontology", "metric_contracts.yml")
    if os.path.exists(contracts_file):
        with open(contracts_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            contracts = data.get("contracts", [])
    else:
        contracts = []

    for c in contracts:
        with st.expander(f"⭐ {c['id']}: {c['name']} — [{c['status']}]", expanded=(c['id'] == 'OTD_V1')):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(f"**Business Definition:**\n> {c['business_definition']}")
                st.markdown(f"**Mathematical Formula:**\n```sql\n{c['formula']}\n```")
                st.markdown(f"**Grain:** `{c['grain']}`")
                st.markdown(f"**Default Time Horizon:** `{c.get('default_time_dimension', 'N/A')}`")
            with col2:
                st.markdown(f"**Metric Owner:** `{c['owner']}`")
                st.markdown(f"**Canonical Source Table:** `{c['source_table']}`")
                st.markdown(f"**Security & Entitlement Policy:** `{c['security_policy']}`")
                st.markdown(f"**Exclusions:** *{c.get('exclusions', 'None')}*")
                synonyms = ", ".join([f"`{s}`" for s in c.get('synonyms', [])])
                st.markdown(f"**Approved Synonyms:** {synonyms}")
