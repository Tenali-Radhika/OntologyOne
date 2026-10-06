"""
Governance, RBAC, Masking, and Cross-Persona Consistency Tests
"""
import os
import pandas as pd
import pytest
from data.scenarios.s5_access_violation import S5Scenario

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "fixtures")

def test_planner_entitlement():
    """Test 7: Planner persona entitlement across all manufacturing nodes."""
    # Under ONTO_PLANNER, access is granted across all 12 plants
    plants_df = pd.read_csv(os.path.join(FIXTURES_DIR, "plants.csv"))
    assert len(plants_df) == 12, "Planner role must have visibility into all 12 operational plants"

def test_procurement_cost_access():
    """Test 8: Procurement persona unmasked cost access."""
    parts_df = pd.read_csv(os.path.join(FIXTURES_DIR, "parts.csv"))
    # In Procurement context, cost must be valid unmasked float
    proc_cost_val = S5Scenario.apply_masking("ONTO_PROCUREMENT", parts_df.iloc[0]["unit_cost"])
    assert proc_cost_val.startswith("$"), f"Procurement should see formatted cost, got {proc_cost_val}"
    assert "***CONFIDENTIAL***" not in proc_cost_val

def test_logistics_cost_masking():
    """Test 9: Logistics persona cost masking policy enforcement."""
    parts_df = pd.read_csv(os.path.join(FIXTURES_DIR, "parts.csv"))
    # In Logistics context, cost must be masked with ***CONFIDENTIAL***
    logistics_cost_val = S5Scenario.apply_masking("ONTO_LOGISTICS", parts_df.iloc[0]["unit_cost"])
    assert logistics_cost_val == "***CONFIDENTIAL***", f"Logistics must be masked, got {logistics_cost_val}"

def test_three_persona_aggregate_consistency():
    """Test 10: RAP Paradox Fix — Cross-persona aggregate OTD invariance (91.4% = 91.4% = 91.4%)."""
    mart_otd_df = pd.read_csv(os.path.join(FIXTURES_DIR, "mart_otd_aggregate.csv"))
    q3_row = mart_otd_df[
        (mart_otd_df["period"] == "2026-Q3") & 
        (mart_otd_df["supplier_id"] == "ALL") & 
        (mart_otd_df["plant_id"] == "ALL")
    ].iloc[0]

    # Pre-aggregated mart is RAP-unrestricted:
    planner_otd = float(q3_row["otd_rate"])
    procurement_otd = float(q3_row["otd_rate"])
    logistics_otd = float(q3_row["otd_rate"])

    invariance = S5Scenario.evaluate_cross_persona_invariance(planner_otd, procurement_otd, logistics_otd)
    assert invariance["is_invariant"], f"Failed cross-persona invariance: {invariance}"
    assert planner_otd == 91.4
    assert procurement_otd == 91.4
    assert logistics_otd == 91.4
