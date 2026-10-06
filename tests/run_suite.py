"""
OntologyOne - 12/12 Governance & Metric Verification Test Runner
Snowflake CoCo CLI Hackathon Track 5
"""
import sys
import os
import time

# Ensure root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.metric.test_metrics import (
    test_otd_v1_calculation,
    test_fr_v1_calculation,
    test_doi_v1_calculation
)
from tests.ontology.test_ontology_relationships import (
    test_supplier_part_relationship,
    test_order_plant_relationship,
    test_order_shipment_relationship
)
from tests.governance.test_entitlements_and_cross_persona import (
    test_planner_entitlement,
    test_procurement_cost_access,
    test_logistics_cost_masking,
    test_three_persona_aggregate_consistency
)
from tests.agent.test_scenarios_and_traps import (
    test_unauthorized_query_rejection,
    test_s4_trap_column_refusal
)

TEST_SPECS = [
    ("Metric Definition & Calculation", "OTD_V1 Flagship (Company Q3 = 91.4%, S-017 = 81.7%, 428 Late)", test_otd_v1_calculation),
    ("Metric Definition & Calculation", "FR_V1 Order Fill Rate & Plant P03 Bottleneck (<78%)", test_fr_v1_calculation),
    ("Metric Definition & Calculation", "DOI_V1 Days of Inventory Calculation (Current Stock / Usage)", test_doi_v1_calculation),
    ("Ontology Relationship Integrity", "Supplier -> Part Foreign Key & Cardinality Validation", test_supplier_part_relationship),
    ("Ontology Relationship Integrity", "Plant -> OrderLine Referential Integrity Check", test_order_plant_relationship),
    ("Ontology Relationship Integrity", "OrderLine -> Shipment Foreign Key & Delivery Status", test_order_shipment_relationship),
    ("Entitlement & Access Policy", "Planner Persona Scope & Multi-Plant Node Visibility", test_planner_entitlement),
    ("Entitlement & Access Policy", "Procurement Persona Unmasked Financial & Unit Cost Access", test_procurement_cost_access),
    ("Entitlement & Access Policy", "Logistics Persona Cost Masking (***CONFIDENTIAL*** Enforcement)", test_logistics_cost_masking),
    ("Cross-Persona OTD Consistency", "RAP Paradox Proof: Planner(91.4%) == Procurement(91.4%) == Logistics(91.4%)", test_three_persona_aggregate_consistency),
    ("Governance Consequence (S5)", "Unauthorized Access Attempt Refusal & Audit Logging", test_unauthorized_query_rejection),
    ("Governance Traps & Defense (S4)", "Refusal of Deprecated raw_orders.is_delayed & OTD_V1 Enforcement", test_s4_trap_column_refusal)
]

def run():
    print("=" * 80)
    print(" ONTOLOGYONE -- GOVERNANCE & SEMANTIC VERIFICATION SUITE")
    print(" Snowflake CoCo CLI Hackathon Track 5 -- Automated 12-Gate Audit")
    print("=" * 80)
    print(f" Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    print(" Target Environment: ONTO_HACKATHON (CORE / MART / GOV)")
    print("-" * 80)

    passed_count = 0
    total_count = len(TEST_SPECS)

    for i, (category, name, test_func) in enumerate(TEST_SPECS, 1):
        print(f"[{i:02d}/{total_count:02d}] {category:<30} | {name:<55} ... ", end="")
        try:
            test_func()
            print("[PASSED]")
            passed_count += 1
        except Exception as e:
            print(f"[FAILED] ({e})")

    print("-" * 80)
    if passed_count == total_count:
        print("\n================================================================================")
        print(f"                    *** GOVERNANCE AUDIT: {passed_count}/{total_count} PASSED ***")
        print("        Unified Aggregate Truth Proven: 91.4% = 91.4% = 91.4%")
        print("            Grounding: 100% Certified Semantic Specification")
        print("================================================================================\n")
        return 0
    else:
        print(f"\nAUDIT FAILED: {passed_count}/{total_count} passed.\n")
        return 1

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    sys.exit(run())
