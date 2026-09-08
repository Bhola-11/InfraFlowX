"""
InfraFlowX - AASHTO Manual for Bridge Evaluation (MBE) LRFR Load Rating Engine
Computes Inventory, Operating, and Permit Rating Factors (RF).
"""

from typing import Dict, Any


class BridgeLoadRatingEngine:
    """
    AASHTO LRFR Rating Factor Formula:
    RF = (C - gamma_DC * DC - gamma_DW * DW +/- gamma_P * P) / (gamma_LL * (LL + IM))
    """

    @classmethod
    def calculate_rating_factor(
        cls,
        nominal_capacity_kn_m: float,
        dead_load_components_kn_m: float,
        dead_load_wearing_surface_kn_m: float,
        live_load_plus_impact_kn_m: float,
        rating_level: str = "INVENTORY",
        condition_factor: float = 1.0,
        system_factor: float = 1.0,
        resistance_factor: float = 1.0,
    ) -> Dict[str, Any]:
        
        # Load factors based on AASHTO LRFR table 6A.4.2.2-1
        if rating_level.upper() == "INVENTORY":
            gamma_dc = 1.25
            gamma_dw = 1.50
            gamma_ll = 1.75
        elif rating_level.upper() == "OPERATING":
            gamma_dc = 1.25
            gamma_dw = 1.50
            gamma_ll = 1.35
        else:  # LEGAL / PERMIT
            gamma_dc = 1.25
            gamma_dw = 1.50
            gamma_ll = 1.40

        capacity = condition_factor * system_factor * resistance_factor * nominal_capacity_kn_m
        dead_load_effect = (gamma_dc * dead_load_components_kn_m) + (gamma_dw * dead_load_wearing_surface_kn_m)
        live_load_demand = gamma_ll * live_load_plus_impact_kn_m

        if live_load_demand <= 0:
            rf = 99.0
        else:
            rf = (capacity - dead_load_effect) / live_load_demand

        rf = max(0.0, rf)
        safe_posting_required = rf < 1.0

        return {
            "rating_level": rating_level.upper(),
            "rating_factor_rf": round(rf, 3),
            "factored_capacity_kn_m": round(capacity, 2),
            "factored_dead_load_kn_m": round(dead_load_effect, 2),
            "factored_live_load_kn_m": round(live_load_demand, 2),
            "safe_load_posting_required": safe_posting_required,
            "structural_adequacy_status": "ADEQUATE" if rf >= 1.0 else "SUBSTANDARD_RESTRICTION_MANDATORY",
            "posting_load_percentage": round(min(100.0, rf * 100.0), 1),
        }
