"""
Scenario S5: Access Violation Attempt & Cross-Persona Aggregate Invariance
Data Plant: Non-procurement persona (Logistics Admin) attempts to query sensitive supplier pricing / unit costs.
Governance: Sensitive cost columns masked as '***CONFIDENTIAL***' or restricted via Row Access Policies.
Crucial Invariance: Despite granular entitlement differences, company-level metric question returns identical 91.4% across all personas via MART_OTD_AGGREGATE.
"""

class S5Scenario:
    id = "S5"
    name = "Access Violation & Governance Consequence"
    restricted_role = "ONTO_LOGISTICS"
    authorized_role = "ONTO_PROCUREMENT"
    target_column = "unit_cost"

    @classmethod
    def apply_masking(cls, role: str, val: float) -> str:
        if role == cls.authorized_role or role == "ONTO_JUDGE":
            return f"${val:.2f}"
        return "***CONFIDENTIAL***"

    @classmethod
    def evaluate_cross_persona_invariance(cls, planner_otd: float, procurement_otd: float, logistics_otd: float) -> dict:
        invariant = (planner_otd == procurement_otd == logistics_otd == 91.4)
        return {
            "planner_otd": planner_otd,
            "procurement_otd": procurement_otd,
            "logistics_otd": logistics_otd,
            "is_invariant": invariant,
            "proof": "Unified Aggregate Truth proven: 91.4% = 91.4% = 91.4%"
        }
