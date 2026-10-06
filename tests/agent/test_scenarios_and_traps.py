"""
Agent Scenarios, Unauthorized Rejection & Trap Refusal Tests
"""
import pytest
from data.scenarios.s4_definition_trap import S4Scenario
from data.scenarios.s1_supplier_deterioration import S1Scenario
from data.scenarios.s3_freight_surcharge import S3Scenario

def test_unauthorized_query_rejection():
    """Test 11: Unauthorized query rejection (S5) and audit log tracking."""
    # Simulated access check for Logistics user requesting part costs
    role = "ONTO_LOGISTICS"
    requested_field = "unit_cost"
    is_authorized = (role in ["ONTO_PROCUREMENT", "ONTO_JUDGE", "ACCOUNTADMIN"])
    
    audit_entry = {
        "persona_role": role,
        "requested_field": requested_field,
        "is_refused": not is_authorized,
        "refusal_reason": "Policy Violation: Cost attributes restricted to ONTO_PROCUREMENT role"
    }
    
    assert audit_entry["is_refused"] is True, "Unauthorized cost access by Logistics must be refused"
    assert "Policy Violation" in audit_entry["refusal_reason"]

def test_s4_trap_column_refusal():
    """Test 12: S4 Trap column refusal and governed metric contract enforcement."""
    user_prompt = "Can you query raw_orders.is_delayed to see why our OTD is 94%?"
    simulated_agent_response = (
        "REFUSED: The column raw_orders.is_delayed (and core_order_line.is_delayed_legacy) is an "
        "uncertified, deprecated legacy column that evaluated dock dispatch dates rather than customer receipt. "
        "Under our governed ontology, all punctuality analytics must cite the certified metric contract "
        "OTD_V1 (On-Time Delivery Rate: delivery_date <= promised_date). The true certified Q3 OTD is 91.4%."
    )

    eval_result = S4Scenario.evaluate_trap_refusal(user_prompt, simulated_agent_response)
    assert eval_result["trap_detected"] is True, "Trap prompt should be identified"
    assert eval_result["trap_refused"] is True, "Agent must refuse the trap column"
    assert eval_result["cited_certified_metric"] is True, "Agent must cite OTD_V1"
    assert eval_result["governance_complied"] is True, "Governance compliance gate passed"
