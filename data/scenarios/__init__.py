"""
OntologyOne Planted Scenarios (S1 through S5)
"""
from .s1_supplier_deterioration import S1Scenario
from .s2_plant_fill_rate import S2Scenario
from .s3_freight_surcharge import S3Scenario
from .s4_definition_trap import S4Scenario
from .s5_access_violation import S5Scenario

SCENARIOS = {
    "S1": S1Scenario,
    "S2": S2Scenario,
    "S3": S3Scenario,
    "S4": S4Scenario,
    "S5": S5Scenario,
}
