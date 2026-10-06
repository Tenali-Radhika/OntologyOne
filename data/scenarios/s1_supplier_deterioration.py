"""
Scenario S1: Supplier Deterioration
Data Plant: Supplier S-017 OTD slides from 96.2% to 81.7% over 8 weeks in Q3.
Affects plants P03, P07, P09, 17 parts, 428 late shipments.
Company OTD slides 94.8% -> 91.4%.
Document: SLA_S017.pdf §4.2 (capacity constraint / revised lead-time clause).
Expected: S-017 identified as primary contributor; drill to shipment SH-93821 (actual 2026-08-19 vs planned 2026-08-15, LATE).
Action: Trigger supplier review, expedite 84 shipments, engage second source.
"""

class S1Scenario:
    id = "S1"
    name = "Supplier Deterioration"
    supplier_id = "S-017"
    supplier_name = "MicroCore Silicon Dynamics"
    historical_otd = 96.2
    current_otd = 81.7
    company_baseline_otd = 94.8
    company_current_otd = 91.4
    late_shipments_count = 428
    impacted_parts_count = 17
    impacted_plants = ["P03", "P07", "P09"]
    anchor_shipment = "SH-93821"
    doc_citation = "SLA_S017.pdf §4.2 (Capacity Constraint / Lead-Time Revision)"
    
    recommendations = [
        "AI-generated recommendation: Trigger immediate vendor cure review with MicroCore Silicon Dynamics (S-017) under SLA §2.2 default provisions.",
        "AI-generated recommendation: Expedite 84 critical in-transit microcontroller shipments via dedicated air freight.",
        "AI-generated recommendation: Rebalance safety stock allocations across Plants P03, P07, and P09 to mitigate wafer lead-time extension."
    ]

    @classmethod
    def evaluate(cls, shipments_df, order_lines_df, parts_df):
        # Filter Q3
        q3_shipments = shipments_df[
            (shipments_df["delivery_date"] >= "2026-07-01") & 
            (shipments_df["delivery_date"] <= "2026-09-30")
        ]
        total_q3 = len(q3_shipments)
        on_time_q3 = (q3_shipments["delivery_status"] == "DELIVERED_ON_TIME").sum()
        company_otd = round((on_time_q3 / total_q3) * 100, 1)

        # Merge for S-017
        merged = q3_shipments.merge(order_lines_df, on="order_line_id").merge(parts_df, on="part_id")
        s17 = merged[merged["supplier_id"] == cls.supplier_id]
        s17_on_time = (s17["delivery_status"] == "DELIVERED_ON_TIME").sum()
        s17_total = len(s17)
        s17_late = (s17["delivery_status"] == "DELIVERED_LATE").sum()
        s17_otd = round((s17_on_time / s17_total) * 100, 1)
        plants = sorted(list(s17[s17["delivery_status"] == "DELIVERED_LATE"]["plant_id"].unique()))
        parts = s17["part_id"].nunique()

        return {
            "company_otd": company_otd,
            "supplier_otd": s17_otd,
            "late_shipments": s17_late,
            "impacted_plants": plants,
            "impacted_parts": parts,
            "matches_spec": (
                company_otd == cls.company_current_otd and
                s17_otd == cls.current_otd and
                s17_late == cls.late_shipments_count and
                plants == cls.impacted_plants and
                parts == cls.impacted_parts_count
            )
        }
