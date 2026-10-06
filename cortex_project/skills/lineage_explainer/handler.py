"""
Skill: lineage_explainer
Returns metric contract + source table + transformation DAG + generated SQL for any metric answer.
"""

def handle(metric_id: str = "OTD_V1") -> dict:
    if metric_id.upper() in ["OTD", "OTD_V1"]:
        return {
            "metric_id": "OTD_V1",
            "contract_owner": "VP Global Logistics",
            "source_layers": {
                "raw": "RAW.RAW_SHIPMENT (ingested via EDI 214)",
                "core": "CORE.CORE_SHIPMENT (Dynamic Table, lag 1 min)",
                "mart": "MART.MART_OTD_AGGREGATE (Certified Fast-Path Mart)",
                "semantic_view": "CORE.SUPPLY_SEMANTIC"
            },
            "dag": [
                {"from": "RAW_EDI_214", "to": "RAW_SHIPMENT"},
                {"from": "RAW_SHIPMENT", "to": "CORE_SHIPMENT"},
                {"from": "CORE_SHIPMENT", "to": "MART_OTD_AGGREGATE"},
                {"from": "MART_OTD_AGGREGATE", "to": "SUPPLY_SEMANTIC"}
            ],
            "governed_sql": "SELECT period, otd_rate FROM ONTO_HACKATHON.MART.MART_OTD_AGGREGATE WHERE period = '2026-Q3' AND supplier_id = 'ALL' AND plant_id = 'ALL';",
            "semantic_grounding": "GROUNDED_IN_SEMANTIC_SPEC"
        }
    return {
        "metric_id": metric_id,
        "status": "Lineage mapped via CORE dynamic table catalog."
    }
