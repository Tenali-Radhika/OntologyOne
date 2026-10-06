"""
OntologyOne - Deterministic Synthetic Supply Chain Data Generator
Calibrated for Snowflake CoCo Hackathon Track 5
Thesis: Same question -> same governed metric -> same calculation -> same answer -> different authorized context.
"""

import os
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
os.makedirs(FIXTURES_DIR, exist_ok=True)

def generate_suppliers():
    suppliers = []
    # 50 suppliers
    for i in range(1, 51):
        s_id = f"S-{i:03d}"
        if s_id == "S-017":
            name = "MicroCore Silicon Dynamics"
            tier = "Tier 1"
            country = "Germany"
            risk = "Critical"
        else:
            name = f"Global Vendor {i} Corp"
            tier = random.choice(["Tier 1", "Tier 2", "Tier 3"])
            country = random.choice(["USA", "Germany", "Japan", "Mexico", "Taiwan", "South Korea"])
            risk = random.choice(["Low", "Medium", "High"])
        suppliers.append({
            "supplier_id": s_id,
            "supplier_name": name,
            "tier": tier,
            "country": country,
            "risk_level": risk
        })
    return pd.DataFrame(suppliers)

def generate_plants():
    # 12 plants across regions
    plants = [
        {"plant_id": "P01", "plant_name": "Midwest Auto Stamping", "region": "North America", "country": "USA"},
        {"plant_id": "P02", "plant_name": "Great Lakes Powertrain", "region": "North America", "country": "USA"},
        {"plant_id": "P03", "plant_name": "Midwest Advanced Assembly", "region": "North America", "country": "USA"},
        {"plant_id": "P04", "plant_name": "Texas Heavy Assembly", "region": "North America", "country": "USA"},
        {"plant_id": "P05", "plant_name": "Ontario Precision Modules", "region": "North America", "country": "Canada"},
        {"plant_id": "P06", "plant_name": "Bavaria Mechatronics", "region": "EMEA", "country": "Germany"},
        {"plant_id": "P07", "plant_name": "Southeast Integration Campus", "region": "North America", "country": "USA"},
        {"plant_id": "P08", "plant_name": "Lyon Propulsion Systems", "region": "EMEA", "country": "France"},
        {"plant_id": "P09", "plant_name": "Pacific Precision Works", "region": "North America", "country": "USA"},
        {"plant_id": "P10", "plant_name": "Tokyo Robotics Fabrication", "region": "APAC", "country": "Japan"},
        {"plant_id": "P11", "plant_name": "Singapore Micro-Assembly", "region": "APAC", "country": "Singapore"},
        {"plant_id": "P12", "plant_name": "Nuevo Leon Sub-Assembly", "region": "North America", "country": "Mexico"},
    ]
    return pd.DataFrame(plants)

def generate_parts(suppliers_df):
    parts = []
    # 200 parts total
    # Exactly 17 parts supplied by S-017
    s17_parts = [f"PART-MCU-{100+i}" for i in range(1, 18)]
    for p_id in s17_parts:
        parts.append({
            "part_id": p_id,
            "part_name": f"Microcontroller Unit {p_id[-3:]}",
            "category": "Electronics",
            "unit_cost": round(random.uniform(45.0, 120.0), 2),
            "supplier_id": "S-017"
        })

    # Remaining 183 parts
    other_suppliers = [s for s in suppliers_df["supplier_id"] if s != "S-017"]
    categories = ["Electronics", "Mechanical", "Fasteners", "Structural", "Fluidics"]
    for i in range(len(s17_parts) + 1, 201):
        p_id = f"PART-{i:04d}"
        parts.append({
            "part_id": p_id,
            "part_name": f"Industrial Sub-Assembly {i}",
            "category": random.choice(categories),
            "unit_cost": round(random.uniform(15.0, 350.0), 2),
            "supplier_id": random.choice(other_suppliers)
        })
    return pd.DataFrame(parts)

def generate_customers():
    customers = []
    # 500 customers
    segments = ["Enterprise", "Strategic", "Commercial"]
    regions = ["North America", "EMEA", "APAC"]
    for i in range(1, 501):
        customers.append({
            "customer_id": f"CUST-{1000+i}",
            "customer_name": f"Client Enterprise {i:03d} LLC",
            "segment": random.choice(segments),
            "region": random.choice(regions)
        })
    return pd.DataFrame(customers)

def generate_orders_and_shipments(parts_df, plants_df, customers_df):
    """
    Generates orders and shipments ensuring exact S1-S5 planted values:
    S1: S-017 OTD = 81.7% in Q3; exactly 428 late shipments; affects plants P03, P07, P09; 17 parts.
    Company overall Q3 OTD = 91.4%.
    S2: Plant P03 fill rate < 78% (chronic low fill rate).
    S3: Freight surcharge on LANE-NW-04 (+30%).
    S4: raw_orders.is_delayed reads ~94% (wrong legacy ship-date metric).
    """
    order_lines = []
    shipments = []

    start_date = datetime(2025, 1, 1)
    q3_start = datetime(2026, 7, 1)
    q3_end = datetime(2026, 9, 30)

    # Specific late shipment for demo narrative
    anchor_late_shipment = "SH-93821"

    # Part maps
    s17_part_ids = set(parts_df[parts_df["supplier_id"] == "S-017"]["part_id"])
    other_part_ids = list(parts_df[parts_df["supplier_id"] != "S-017"]["part_id"])
    s17_plants = ["P03", "P07", "P09"]
    all_plants = list(plants_df["plant_id"])
    customer_ids = list(customers_df["customer_id"])

    # For S1 calibration:
    # S-017 total Q3 shipments: 428 late / (1 - 0.817) = 428 / 0.183 = ~2,338.79 -> 2,339 total, 1,911 on time, 428 late -> 1911 / 2339 = 81.7015%
    # Overall company Q3 shipments: let's calibrate so total late shipments gives exactly 91.4% OTD!
    # If Company Q3 Total = 10,000 shipments: 9,140 on time, 860 late -> 91.40%
    # S-017 has 2,339 shipments (1,911 on time, 428 late).
    # Other suppliers have 7,661 shipments (7,229 on time, 432 late -> 94.36% OTD).
    # Total Q3 shipments = 10,000. Total on-time = 1,911 + 7,229 = 9,140. Total late = 428 + 432 = 860.
    # Exactly 9,140 / 10,000 = 91.4% OTD!

    order_id_counter = 1
    shipment_id_counter = 1

    # 1. Generate S-017 Q3 shipments
    s17_total = 2339
    s17_late_target = 428
    # Anchor shipment (idx 0) is guaranteed late, sample remaining 427 from range(1, s17_total)
    s17_late_indices = {0} | set(random.sample(range(1, s17_total), s17_late_target - 1))

    for idx in range(s17_total):
        s_id = f"SH-{shipment_id_counter:05d}"
        if idx == 0:
            s_id = anchor_late_shipment  # Ensure SH-93821 exists and is late!
        shipment_id_counter += 1

        ol_id = f"OL-{order_id_counter:06d}"
        order_id_counter += 1

        # Evenly distribute among the 17 S17 parts and P03, P07, P09
        part_id = random.choice(list(s17_part_ids))
        plant_id = random.choice(s17_plants)
        cust_id = random.choice(customer_ids)

        # Dates within Q3
        days_offset = random.randint(0, 91)
        deliv_date = q3_start + timedelta(days=days_offset)
        order_date = deliv_date - timedelta(days=random.randint(18, 30))
        ship_date = deliv_date - timedelta(days=random.randint(2, 5))

        is_late = (idx in s17_late_indices)
        if is_late:
            # Delivered late: promised_date was earlier than delivery_date
            promised_date = deliv_date - timedelta(days=random.randint(2, 7))
            status = "DELIVERED_LATE"
        else:
            # Delivered on time
            promised_date = deliv_date + timedelta(days=random.randint(0, 4))
            status = "DELIVERED_ON_TIME"

        if s_id == anchor_late_shipment:
            # Specifically matched to brief Scene 3 narrative:
            # actual 2026-08-19 vs planned 2026-08-15, LATE
            deliv_date = datetime(2026, 8, 19)
            promised_date = datetime(2026, 8, 15)
            ship_date = datetime(2026, 8, 14)
            order_date = datetime(2026, 7, 20)
            status = "DELIVERED_LATE"

        # Fill rate for order line
        qty_ordered = random.randint(50, 500)
        # S2: Plant P03 has lower fill rate (<78%)
        if plant_id == "P03":
            qty_fulfilled = int(qty_ordered * random.uniform(0.65, 0.76))
        else:
            qty_fulfilled = int(qty_ordered * random.uniform(0.92, 1.0))

        # S4 legacy trap: computed from ship_date vs promised_ship_date (misleading ~94%)
        # legacy flag says delayed only if ship_date was late, which often wasn't!
        is_delayed_legacy = (ship_date > promised_date - timedelta(days=3)) and (random.random() < 0.058)

        # S3 freight lane: LANE-NW-04 has +30% surcharge
        lane_id = random.choice(["LANE-NW-04", "LANE-MW-01", "LANE-SE-02", "LANE-NE-03"])
        base_freight = random.uniform(1500.0, 2100.0)
        if lane_id == "LANE-NW-04":
            freight_cost = round(base_freight * 1.30, 2)  # +30% surcharge
        else:
            freight_cost = round(base_freight, 2)

        order_lines.append({
            "order_line_id": ol_id,
            "order_id": f"ORD-{order_id_counter // 2:05d}",
            "part_id": part_id,
            "plant_id": plant_id,
            "customer_id": cust_id,
            "quantity_ordered": qty_ordered,
            "quantity_fulfilled": qty_fulfilled,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "promised_date": promised_date.strftime("%Y-%m-%d"),
            "is_delayed_legacy": is_delayed_legacy
        })

        shipments.append({
            "shipment_id": s_id,
            "order_line_id": ol_id,
            "carrier_id": random.choice(["CARR-01", "CARR-02", "CARR-03"]),
            "lane_id": lane_id,
            "ship_date": ship_date.strftime("%Y-%m-%d"),
            "delivery_date": deliv_date.strftime("%Y-%m-%d"),
            "promised_date": promised_date.strftime("%Y-%m-%d"),
            "delivery_status": status,
            "freight_cost": freight_cost
        })

    # 2. Generate Non-S017 Q3 shipments (7,661 shipments: exactly 7,229 on time, 432 late)
    other_total = 7661
    other_late_target = 432
    other_late_indices = set(random.sample(range(other_total), other_late_target))

    for idx in range(other_total):
        s_id = f"SH-{shipment_id_counter:05d}"
        shipment_id_counter += 1
        ol_id = f"OL-{order_id_counter:06d}"
        order_id_counter += 1

        part_id = random.choice(other_part_ids)
        plant_id = random.choice(all_plants)
        cust_id = random.choice(customer_ids)

        days_offset = random.randint(0, 91)
        deliv_date = q3_start + timedelta(days=days_offset)
        order_date = deliv_date - timedelta(days=random.randint(15, 30))
        ship_date = deliv_date - timedelta(days=random.randint(2, 5))

        if idx in other_late_indices:
            promised_date = deliv_date - timedelta(days=random.randint(1, 6))
            status = "DELIVERED_LATE"
        else:
            promised_date = deliv_date + timedelta(days=random.randint(0, 4))
            status = "DELIVERED_ON_TIME"

        qty_ordered = random.randint(50, 500)
        if plant_id == "P03":
            qty_fulfilled = int(qty_ordered * random.uniform(0.65, 0.77))
        else:
            qty_fulfilled = int(qty_ordered * random.uniform(0.92, 1.0))

        is_delayed_legacy = (random.random() < 0.055)

        lane_id = random.choice(["LANE-NW-04", "LANE-MW-01", "LANE-SE-02", "LANE-NE-03"])
        base_freight = random.uniform(1500.0, 2100.0)
        if lane_id == "LANE-NW-04":
            freight_cost = round(base_freight * 1.30, 2)
        else:
            freight_cost = round(base_freight, 2)

        order_lines.append({
            "order_line_id": ol_id,
            "order_id": f"ORD-{order_id_counter // 2:05d}",
            "part_id": part_id,
            "plant_id": plant_id,
            "customer_id": cust_id,
            "quantity_ordered": qty_ordered,
            "quantity_fulfilled": qty_fulfilled,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "promised_date": promised_date.strftime("%Y-%m-%d"),
            "is_delayed_legacy": is_delayed_legacy
        })

        shipments.append({
            "shipment_id": s_id,
            "order_line_id": ol_id,
            "carrier_id": random.choice(["CARR-01", "CARR-02", "CARR-03"]),
            "lane_id": lane_id,
            "ship_date": ship_date.strftime("%Y-%m-%d"),
            "delivery_date": deliv_date.strftime("%Y-%m-%d"),
            "promised_date": promised_date.strftime("%Y-%m-%d"),
            "delivery_status": status,
            "freight_cost": freight_cost
        })

    # 3. Add baseline data for Q1 and Q2 2026 to show historical trajectory (Q2 OTD = 94.8% -> Q3 OTD = 91.4%)
    q2_total = 5000
    q2_late_target = int(q2_total * (1 - 0.948)) # 260 late -> 94.8% OTD
    q2_late_indices = set(random.sample(range(q2_total), q2_late_target))

    for idx in range(q2_total):
        s_id = f"SH-{shipment_id_counter:05d}"
        shipment_id_counter += 1
        ol_id = f"OL-{order_id_counter:06d}"
        order_id_counter += 1

        part_id = random.choice(list(parts_df["part_id"]))
        plant_id = random.choice(all_plants)
        cust_id = random.choice(customer_ids)

        deliv_date = datetime(2026, 4, 1) + timedelta(days=random.randint(0, 90))
        order_date = deliv_date - timedelta(days=random.randint(15, 30))
        ship_date = deliv_date - timedelta(days=random.randint(2, 5))

        if idx in q2_late_indices:
            promised_date = deliv_date - timedelta(days=random.randint(1, 5))
            status = "DELIVERED_LATE"
        else:
            promised_date = deliv_date + timedelta(days=random.randint(0, 4))
            status = "DELIVERED_ON_TIME"

        qty_ordered = random.randint(50, 500)
        qty_fulfilled = int(qty_ordered * random.uniform(0.90, 1.0))
        is_delayed_legacy = (random.random() < 0.05)
        freight_cost = round(random.uniform(1500.0, 2100.0), 2)

        order_lines.append({
            "order_line_id": ol_id,
            "order_id": f"ORD-{order_id_counter // 2:05d}",
            "part_id": part_id,
            "plant_id": plant_id,
            "customer_id": cust_id,
            "quantity_ordered": qty_ordered,
            "quantity_fulfilled": qty_fulfilled,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "promised_date": promised_date.strftime("%Y-%m-%d"),
            "is_delayed_legacy": is_delayed_legacy
        })

        shipments.append({
            "shipment_id": s_id,
            "order_line_id": ol_id,
            "carrier_id": random.choice(["CARR-01", "CARR-02", "CARR-03"]),
            "lane_id": "LANE-MW-01",
            "ship_date": ship_date.strftime("%Y-%m-%d"),
            "delivery_date": deliv_date.strftime("%Y-%m-%d"),
            "promised_date": promised_date.strftime("%Y-%m-%d"),
            "delivery_status": status,
            "freight_cost": freight_cost
        })

    return pd.DataFrame(order_lines), pd.DataFrame(shipments)

def generate_inventory(parts_df, plants_df):
    records = []
    for _, part in parts_df.iterrows():
        for _, plant in plants_df.iterrows():
            usage_30d = random.randint(300, 3000)
            avg_daily_usage = usage_30d / 30.0
            # Target DOI between 18 and 45 days
            doi = random.uniform(18.0, 45.0)
            stock = int(avg_daily_usage * doi)
            records.append({
                "part_id": part["part_id"],
                "plant_id": plant["plant_id"],
                "current_stock_quantity": stock,
                "usage_quantity_30d": usage_30d,
                "days_of_inventory": round(doi, 1),
                "snapshot_date": "2026-09-30"
            })
    return pd.DataFrame(records)

def generate_mart_otd_aggregate():
    """
    Certified pre-aggregated MART_OTD_AGGREGATE.
    Two-tier truth architecture: RAP-unrestricted certified mart!
    """
    rows = [
        # Enterprise-wide Q3 2026
        {
            "period": "2026-Q3",
            "supplier_id": "ALL",
            "plant_id": "ALL",
            "total_shipments": 10000,
            "on_time_shipments": 9140,
            "otd_rate": 91.4,
            "status": "CERTIFIED"
        },
        # Prior quarter Q2 2026 showing slide from 94.8% -> 91.4%
        {
            "period": "2026-Q2",
            "supplier_id": "ALL",
            "plant_id": "ALL",
            "total_shipments": 5000,
            "on_time_shipments": 4740,
            "otd_rate": 94.8,
            "status": "CERTIFIED"
        },
        # Supplier S-017 slide from 96.2% to 81.7%
        {
            "period": "2026-Q2",
            "supplier_id": "S-017",
            "plant_id": "ALL",
            "total_shipments": 1200,
            "on_time_shipments": 1154,
            "otd_rate": 96.2,
            "status": "CERTIFIED"
        },
        {
            "period": "2026-Q3",
            "supplier_id": "S-017",
            "plant_id": "ALL",
            "total_shipments": 2339,
            "on_time_shipments": 1911,
            "otd_rate": 81.7,
            "status": "CERTIFIED"
        },
        # Impacted plants P03, P07, P09 for S-017
        {
            "period": "2026-Q3",
            "supplier_id": "S-017",
            "plant_id": "P03",
            "total_shipments": 812,
            "on_time_shipments": 655,
            "otd_rate": 80.7,
            "status": "CERTIFIED"
        },
        {
            "period": "2026-Q3",
            "supplier_id": "S-017",
            "plant_id": "P07",
            "total_shipments": 774,
            "on_time_shipments": 638,
            "otd_rate": 82.4,
            "status": "CERTIFIED"
        },
        {
            "period": "2026-Q3",
            "supplier_id": "S-017",
            "plant_id": "P09",
            "total_shipments": 753,
            "on_time_shipments": 618,
            "otd_rate": 82.1,
            "status": "CERTIFIED"
        }
    ]
    return pd.DataFrame(rows)

def main():
    print("Generating synthetic deterministic supply chain ontology data...")
    suppliers_df = generate_suppliers()
    plants_df = generate_plants()
    parts_df = generate_parts(suppliers_df)
    customers_df = generate_customers()
    order_lines_df, shipments_df = generate_orders_and_shipments(parts_df, plants_df, customers_df)
    inventory_df = generate_inventory(parts_df, plants_df)
    mart_otd_df = generate_mart_otd_aggregate()

    # Save to fixtures CSV
    suppliers_df.to_csv(os.path.join(FIXTURES_DIR, "suppliers.csv"), index=False)
    plants_df.to_csv(os.path.join(FIXTURES_DIR, "plants.csv"), index=False)
    parts_df.to_csv(os.path.join(FIXTURES_DIR, "parts.csv"), index=False)
    customers_df.to_csv(os.path.join(FIXTURES_DIR, "customers.csv"), index=False)
    order_lines_df.to_csv(os.path.join(FIXTURES_DIR, "order_lines.csv"), index=False)
    shipments_df.to_csv(os.path.join(FIXTURES_DIR, "shipments.csv"), index=False)
    inventory_df.to_csv(os.path.join(FIXTURES_DIR, "inventory.csv"), index=False)
    mart_otd_df.to_csv(os.path.join(FIXTURES_DIR, "mart_otd_aggregate.csv"), index=False)

    print("Fixtures written successfully to data/fixtures/")
    print(f"Suppliers: {len(suppliers_df)}, Parts: {len(parts_df)}, Plants: {len(plants_df)}, Customers: {len(customers_df)}")
    print(f"Order Lines: {len(order_lines_df)}, Shipments: {len(shipments_df)}")
    
    # Calculate and verify Q3 company OTD
    merged = shipments_df[
        (shipments_df["delivery_date"] >= "2026-07-01") & 
        (shipments_df["delivery_date"] <= "2026-09-30")
    ]
    on_time = (merged["delivery_status"] == "DELIVERED_ON_TIME").sum()
    total = len(merged)
    q3_otd = (on_time / total) * 100
    print(f"VERIFICATION: Q3 Company OTD = {q3_otd:.1f}% ({on_time}/{total}) [Expected 91.4%]")

    # Verify S-017 Q3 OTD
    s17_merged = merged.merge(order_lines_df, on="order_line_id").merge(parts_df, on="part_id")
    s17_q3 = s17_merged[s17_merged["supplier_id"] == "S-017"]
    s17_on_time = (s17_q3["delivery_status"] == "DELIVERED_ON_TIME").sum()
    s17_total = len(s17_q3)
    s17_late = (s17_q3["delivery_status"] == "DELIVERED_LATE").sum()
    s17_otd = (s17_on_time / s17_total) * 100
    print(f"VERIFICATION: S-017 Q3 OTD = {s17_otd:.1f}% ({s17_on_time}/{s17_total}), Late Shipments: {s17_late} [Expected 81.7%, 428 late]")

if __name__ == "__main__":
    main()
