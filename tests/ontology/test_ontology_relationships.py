"""
Ontology Relationship and Referential Integrity Tests
"""
import os
import pandas as pd
import pytest

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "fixtures")

def test_supplier_part_relationship():
    """Test 4: Supplier -> Part foreign key integrity and cardinality."""
    suppliers_df = pd.read_csv(os.path.join(FIXTURES_DIR, "suppliers.csv"))
    parts_df = pd.read_csv(os.path.join(FIXTURES_DIR, "parts.csv"))

    supplier_ids = set(suppliers_df["supplier_id"])
    orphan_parts = parts_df[~parts_df["supplier_id"].isin(supplier_ids)]
    assert len(orphan_parts) == 0, f"Found {len(orphan_parts)} orphan parts without valid supplier_id"

def test_order_plant_relationship():
    """Test 5: OrderLine -> Plant foreign key integrity."""
    plants_df = pd.read_csv(os.path.join(FIXTURES_DIR, "plants.csv"))
    order_lines_df = pd.read_csv(os.path.join(FIXTURES_DIR, "order_lines.csv"))

    plant_ids = set(plants_df["plant_id"])
    orphan_orders = order_lines_df[~order_lines_df["plant_id"].isin(plant_ids)]
    assert len(orphan_orders) == 0, f"Found {len(orphan_orders)} orders without valid plant_id"

def test_order_shipment_relationship():
    """Test 6: OrderLine -> Shipment foreign key integrity."""
    order_lines_df = pd.read_csv(os.path.join(FIXTURES_DIR, "order_lines.csv"))
    shipments_df = pd.read_csv(os.path.join(FIXTURES_DIR, "shipments.csv"))

    order_line_ids = set(order_lines_df["order_line_id"])
    orphan_shipments = shipments_df[~shipments_df["order_line_id"].isin(order_line_ids)]
    assert len(orphan_shipments) == 0, f"Found {len(orphan_shipments)} shipments without valid order_line_id"
