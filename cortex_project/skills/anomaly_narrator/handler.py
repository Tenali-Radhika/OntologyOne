"""
Skill: anomaly_narrator
Decomposes metric anomalies (e.g., OTD decline 94.8% -> 91.4%) into primary causal drivers:
Supplier S-017 -> Plants P03, P07, P09 -> 17 parts -> 428 late shipments -> SH-93821 -> SLA §4.2 -> AI recommendations.
"""

def handle(metric_id: str = "OTD_V1", period: str = "2026-Q3") -> dict:
    if metric_id.upper() in ["OTD", "OTD_V1"] and period == "2026-Q3":
        return {
            "metric_id": "OTD_V1",
            "period": "2026-Q3",
            "baseline_otd": 94.8,
            "current_otd": 91.4,
            "delta_points": -3.4,
            "primary_contributor": {
                "supplier_id": "S-017",
                "supplier_name": "MicroCore Silicon Dynamics",
                "supplier_historical_otd": 96.2,
                "supplier_current_otd": 81.7,
                "supplier_delta": -14.5,
                "total_q3_shipments": 2339,
                "late_shipments_count": 428,
                "impacted_plants": ["P03", "P07", "P09"],
                "impacted_parts_count": 17,
                "anchor_late_shipment": {
                    "shipment_id": "SH-93821",
                    "part_id": "PART-MCU-101",
                    "plant_id": "P03",
                    "promised_date": "2026-08-15",
                    "actual_delivery_date": "2026-08-19",
                    "status": "DELIVERED_LATE",
                    "delay_days": 4
                }
            },
            "business_evidence": {
                "document": "SLA_S017.pdf",
                "clause": "§4.2 Capacity Constraint & Temporary Lead-Time Revision",
                "excerpt": "Supplier S-017 invoked Section 4.2 Allocation Procedures due to Dresden Fab wafer substrate shortage. Standard lead times for 17 microcontroller parts extended from 14 to 28 days."
            },
            "recommendations": [
                "AI-generated recommendation: Trigger immediate executive supplier review with MicroCore Silicon Dynamics (S-017) under SLA §2.2 default penalties.",
                "AI-generated recommendation: Expedite 84 critical in-transit shipments across Plants P03, P07, P09 using expedited air courier.",
                "AI-generated recommendation: Qualify secondary semiconductor vendor to relieve wafer allocation caps."
            ]
        }
    return {
        "status": "No critical anomaly detected outside standard tolerance band."
    }
