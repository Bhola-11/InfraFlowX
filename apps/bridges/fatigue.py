"""
InfraFlowX - Steel and Concrete Bridge Fatigue & Life Assessment Engine
Compliant with AASHTO LRFD Bridge Design Specifications & Palmgren-Miner Cumulative Damage Rule.
"""

from typing import Dict, List, Any
import math


class BridgeFatigueEngine:
    """
    Fatigue evaluation of structural steel girders, welded details, and prestressed strands.
    """

    # Detail Category Constant A (ksi^3 or MPa^3) - AASHTO Table 6.6.1.2.5-1
    DETAIL_THRESHOLDS_MPA = {
        "A": {"A_const": 3.93e11, "f_th": 165.0},
        "B": {"A_const": 1.19e11, "f_th": 110.0},
        "B_PRIME": {"A_const": 6.11e10, "f_th": 83.0},
        "C": {"A_const": 4.40e10, "f_th": 69.0},
        "C_PRIME": {"A_const": 4.40e10, "f_th": 83.0},
        "D": {"A_const": 2.18e10, "f_th": 48.0},
        "E": {"A_const": 1.10e10, "f_th": 31.0},
        "E_PRIME": {"A_const": 3.93e9, "f_th": 18.0},
    }

    @classmethod
    def calculate_fatigue_life_cycles(cls, detail_category: str, effective_stress_range_mpa: float) -> Dict[str, Any]:
        """
        N = A / (Delta_f)^3
        """
        cat = detail_category.upper()
        if cat not in cls.DETAIL_THRESHOLDS_MPA:
            cat = "C"
        params = cls.DETAIL_THRESHOLDS_MPA[cat]
        a_const = params["A_const"]
        f_th = params["f_th"]

        infinite_life = effective_stress_range_mpa <= (f_th / 2.0)
        
        if infinite_life:
            nominal_cycles = float("inf")
        else:
            nominal_cycles = a_const / (effective_stress_range_mpa ** 3)

        return {
            "detail_category": cat,
            "threshold_stress_mpa": f_th,
            "effective_stress_range_mpa": effective_stress_range_mpa,
            "infinite_life_eligible": infinite_life,
            "permissible_cycles_to_failure": nominal_cycles if not infinite_life else 1e12,
        }

    @classmethod
    def palmgren_miner_cumulative_damage(cls, detail_category: str, stress_spectrum: List[Dict[str, float]], current_operating_years: float) -> Dict[str, Any]:
        """
        Miner's Rule: D = Sum(n_i / N_i)
        stress_spectrum: List of {"stress_range_mpa": float, "annual_cycles": float}
        """
        total_damage = 0.0
        cat_info = cls.DETAIL_THRESHOLDS_MPA.get(detail_category.upper(), cls.DETAIL_THRESHOLDS_MPA["C"])
        
        for block in stress_spectrum:
            stress = block.get("stress_range_mpa", 30.0)
            annual_n = block.get("annual_cycles", 100000.0)
            applied_cycles = annual_n * current_operating_years
            
            if stress > (cat_info["f_th"] / 2.0):
                capacity_n = cat_info["A_const"] / (stress ** 3)
                damage_fraction = applied_cycles / capacity_n
            else:
                damage_fraction = 0.0
            
            total_damage += damage_fraction

        remaining_life_years = 0.0
        if total_damage < 1.0 and current_operating_years > 0:
            annual_damage_rate = total_damage / current_operating_years
            if annual_damage_rate > 0:
                remaining_life_years = (1.0 - total_damage) / annual_damage_rate

        return {
            "cumulative_damage_index_D": round(total_damage, 4),
            "fatigue_consumed_percentage": round(min(100.0, total_damage * 100.0), 2),
            "structural_failure_imminent": total_damage >= 1.0,
            "estimated_remaining_fatigue_life_years": round(max(0.0, remaining_life_years), 1),
        }
