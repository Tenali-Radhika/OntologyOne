"""
Scenario S2: Plant Fill-Rate Problem
Data Plant: Plant P03 chronic low fill rate (<78%).
Document: regional_policy.txt §3 (Regional balancing & cross-facility allocation protocol).
Expected: Plant P03 flagged as bottleneck.
Action: AI-generated recommendation: Dynamic inventory reallocation and order rerouting P03 -> P07.
"""

class S2Scenario:
    id = "S2"
    name = "Plant Fill-Rate Problem"
    flagged_plant = "P03"
    target_plant = "P07"
    doc_citation = "regional_policy.txt §3 (Cross-Facility Reallocation Protocol)"
    
    recommendations = [
        "AI-generated recommendation: Trigger cross-facility order reallocation from Plant P03 to Plant P07 per SOP-OPS-REG-04.",
        "AI-generated recommendation: Transfer common sub-assembly buffer stock via ground shuttle from Midwest to Southeast campus within 48 hours."
    ]

    @classmethod
    def evaluate(cls, order_lines_df):
        p03_orders = order_lines_df[order_lines_df["plant_id"] == "P03"]
        total_ordered = p03_orders["quantity_ordered"].sum()
        total_fulfilled = p03_orders["quantity_fulfilled"].sum()
        fill_rate = round((total_fulfilled / total_ordered) * 100, 1)

        p07_orders = order_lines_df[order_lines_df["plant_id"] == "P07"]
        p07_fill_rate = round((p07_orders["quantity_fulfilled"].sum() / p07_orders["quantity_ordered"].sum()) * 100, 1)

        return {
            "p03_fill_rate": fill_rate,
            "p07_fill_rate": p07_fill_rate,
            "is_p03_bottleneck": fill_rate < 78.0 and p07_fill_rate > 90.0
        }
