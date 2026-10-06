"""
Metric Verification Tests: OTD_V1, FR_V1, DOI_V1
"""
import os
import pandas as pd
import pytest

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "fixtures")

def test_otd_v1_calculation():
    """Test 1: Flagship OTD_V1 calculation and S1 planted values."""
    shipments_df = pd.read_csv(os.path.join(FIXTURES_DIR, "shipments.csv"))
    order_lines_df = pd.read_csv(os.path.join(FIXTURES_DIR, "order_lines.csv"))
    parts_df = pd.read_csv(os.path.join(FIXTURES_DIR, "parts.csv"))

    # Q3 company OTD
    q3 = shipments_df[(shipments_df["delivery_date"] >= "2026-07-01") & (shipments_df["delivery_date"] <= "2026-09-30")]
    on_time = (q3["delivery_status"] == "DELIVERED_ON_TIME").sum()
    total = len(q3)
    company_otd = round((on_time / total) * 100, 1)
    assert company_otd == 91.4, f"Expected company Q3 OTD = 91.4%, got {company_otd}%"

    # Supplier S-017 Q3 OTD & late count
    merged = q3.merge(order_lines_df, on="order_line_id").merge(parts_df, on="part_id")
    s17 = merged[merged["supplier_id"] == "S-017"]
    s17_on_time = (s17["delivery_status"] == "DELIVERED_ON_TIME").sum()
    s17_total = len(s17)
    s17_late = (s17["delivery_status"] == "DELIVERED_LATE").sum()
    s17_otd = round((s17_on_time / s17_total) * 100, 1)

    assert s17_otd == 81.7, f"Expected S-017 OTD = 81.7%, got {s17_otd}%"
    assert s17_late == 428, f"Expected S-017 late shipments = 428, got {s17_late}"
    assert s17["part_id"].nunique() == 17, f"Expected 17 parts from S-017, got {s17['part_id'].nunique()}"

def test_fr_v1_calculation():
    """Test 2: Order Fill Rate FR_V1 calculation and S2 plant bottleneck detection."""
    order_lines_df = pd.read_csv(os.path.join(FIXTURES_DIR, "order_lines.csv"))
    p03 = order_lines_df[order_lines_df["plant_id"] == "P03"]
    p03_fr = round((p03["quantity_fulfilled"].sum() / p03["quantity_ordered"].sum()) * 100, 1)
    assert p03_fr < 78.0, f"Expected Plant P03 chronic low fill rate < 78%, got {p03_fr}%"

    p07 = order_lines_df[order_lines_df["plant_id"] == "P07"]
    p07_fr = round((p07["quantity_fulfilled"].sum() / p07["quantity_ordered"].sum()) * 100, 1)
    assert p07_fr >= 90.0, f"Expected Plant P07 high fill rate >= 90%, got {p07_fr}%"

def test_doi_v1_calculation():
    """Test 3: Days of Inventory DOI_V1 calculation."""
    inventory_df = pd.read_csv(os.path.join(FIXTURES_DIR, "inventory.csv"))
    for _, row in inventory_df.head(20).iterrows():
        calc_doi = round(row["current_stock_quantity"] / (row["usage_quantity_30d"] / 30.0), 1)
        assert abs(calc_doi - row["days_of_inventory"]) <= 0.2, "DOI calculation drift detected"
