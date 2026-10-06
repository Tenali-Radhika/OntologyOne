"""
Skill: metric_explainer
Returns metric contract details, business definitions, and formulas on demand.
"""
import yaml
import os

def load_contracts():
    path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "ontology", "metric_contracts.yml")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return {c["id"]: c for c in data.get("contracts", [])}
    return {}

def handle(metric_id: str = "OTD_V1") -> dict:
    contracts = load_contracts()
    metric_id = metric_id.upper()
    if metric_id in contracts:
        c = contracts[metric_id]
        return {
            "metric_id": c["id"],
            "name": c["name"],
            "status": c["status"],
            "business_definition": c["business_definition"],
            "formula": c["formula"],
            "grain": c["grain"],
            "owner": c["owner"],
            "source_table": c["source_table"],
            "security_policy": c["security_policy"],
            "is_certified": True
        }
    return {
        "error": f"Metric {metric_id} not found in certified contracts registry."
    }
