"""
Scenario S4: Definition Conflict (TRAP)
Data Plant: raw_orders.is_delayed computed from ship date instead of delivery date -> yields deceptive ~94% OTD.
Document: legacy_metric_memo.txt (Deprecation of ship-date metric in favor of OTD_V1).
Expected: Agent explicitly refuses legacy column, cites metric contract OTD_V1, and answers with certified 91.4%.
"""

class S4Scenario:
    id = "S4"
    name = "Definition Conflict (TRAP)"
    trap_column = "is_delayed_legacy"
    certified_metric = "OTD_V1"
    doc_citation = "legacy_metric_memo.txt (Retirement of raw_orders.is_delayed)"

    @classmethod
    def evaluate_trap_refusal(cls, user_prompt: str, agent_response: str) -> dict:
        prompt_mentions_trap = "is_delayed" in user_prompt.lower() or "delayed orders" in user_prompt.lower()
        refused_trap = (
            "refused" in agent_response.lower() or 
            "deprecated" in agent_response.lower() or
            "uncertified" in agent_response.lower() or
            "cannot use" in agent_response.lower() or
            "violates" in agent_response.lower()
        )
        cited_otd_v1 = "otd_v1" in agent_response.lower() or "91.4" in agent_response
        
        return {
            "trap_detected": prompt_mentions_trap,
            "trap_refused": refused_trap,
            "cited_certified_metric": cited_otd_v1,
            "governance_complied": refused_trap and cited_otd_v1
        }
