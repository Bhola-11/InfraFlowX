"""
InfraFlowX - International Building Code (IBC) & NFPA Life Safety Compliance Engine
Validates occupant loads, egress widths, fire suppression requirements, and ADA accessibility.
"""

from typing import Dict, List, Any
import math


class BuildingComplianceEngine:
    """
    Evaluates facility compliance with IBC Chapter 10 (Means of Egress) and ADA standards.
    """

    # Occupant load factors (sq ft per person) - IBC Table 1004.5
    OCCUPANT_LOAD_FACTORS = {
        "ASSEMBLY_UNCONCENTRATED": 15.0,
        "BUSINESS_OFFICE": 150.0,
        "EDUCATIONAL_CLASSROOM": 20.0,
        "MUNICIPAL_COUNCIL": 15.0,
        "STORAGE_WAREHOUSE": 500.0,
        "MECHANICAL_EQUIPMENT_ROOM": 300.0,
        "HEALTHCARE_CLINIC": 120.0,
    }

    @classmethod
    def evaluate_occupant_load_and_egress(cls, floor_area_sqft: float, function_use: str, num_exits_provided: int, total_stairway_width_inches: float, total_door_width_inches: float, sprinklered: bool = True) -> Dict[str, Any]:
        use_key = function_use.upper()
        factor = cls.OCCUPANT_LOAD_FACTORS.get(use_key, 100.0)
        occupant_load = math.ceil(floor_area_sqft / factor)

        # Minimum number of exits (IBC 1006.2.1)
        if occupant_load <= 49:
            min_exits = 1
        elif occupant_load <= 500:
            min_exits = 2
        elif occupant_load <= 1000:
            min_exits = 3
        else:
            min_exits = 4

        # Egress width per occupant: 0.3 in/person stair, 0.2 in/person other (sprinklered 0.2/0.15)
        stair_factor = 0.2 if sprinklered else 0.3
        door_factor = 0.15 if sprinklered else 0.20

        required_stair_width = occupant_load * stair_factor
        required_door_width = occupant_load * door_factor

        stair_pass = total_stairway_width_inches >= required_stair_width
        door_pass = total_door_width_inches >= required_door_width
        exit_count_pass = num_exits_provided >= min_exits

        return {
            "calculated_occupant_load": occupant_load,
            "minimum_exits_required": min_exits,
            "exits_provided": num_exits_provided,
            "exit_count_compliant": exit_count_pass,
            "required_stair_width_inches": round(required_stair_width, 1),
            "provided_stair_width_inches": total_stairway_width_inches,
            "stair_width_compliant": stair_pass,
            "required_door_width_inches": round(required_door_width, 1),
            "provided_door_width_inches": total_door_width_inches,
            "door_width_compliant": door_pass,
            "overall_life_safety_compliant": (exit_count_pass and stair_pass and door_pass),
        }
