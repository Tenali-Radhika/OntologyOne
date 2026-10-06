"""
Scenario S3: Freight Surcharge Anomaly
Data Plant: Coastal Lane LANE-NW-04 freight cost spiked +30% due to peak maritime congestion.
Document: freight_agreement.pdf §2.1 (Peak Maritime Congestion Surcharge Clause).
Expected: LANE-NW-04 identified, cost surge decomposed into freight rate increase while piece price remained constant.
Action: AI-generated recommendation: Renegotiate surcharge or reroute intermodal traffic.
"""

class S3Scenario:
    id = "S3"
    name = "Freight Surcharge Anomaly"
    flagged_lane = "LANE-NW-04"
    doc_citation = "freight_agreement.pdf §2.1 (Peak Maritime Congestion Surcharge)"
    
    recommendations = [
        "AI-generated recommendation: Audit monthly bills of lading for LANE-NW-04 under FA-2025-CARRIER-08 §3 audit provisions.",
        "AI-generated recommendation: Evaluate rerouting container flows via alternative inland rail corridors to bypass coastal congestion."
    ]

    @classmethod
    def evaluate(cls, shipments_df):
        lane_nw = shipments_df[shipments_df["lane_id"] == "LANE-NW-04"]["freight_cost"].mean()
        other_lanes = shipments_df[shipments_df["lane_id"] != "LANE-NW-04"]["freight_cost"].mean()
        cost_ratio = lane_nw / other_lanes

        return {
            "lane_nw_avg_freight": round(lane_nw, 2),
            "other_lanes_avg_freight": round(other_lanes, 2),
            "cost_premium_percent": round((cost_ratio - 1.0) * 100, 1),
            "has_30_pct_surge": cost_ratio >= 1.25
        }
