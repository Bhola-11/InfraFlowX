"""
InfraFlowX Enterprise Platform - Employees Economic Valuation & Asset Cost Analysis Engine
Computes Depreciated Replacement Cost (DRC), Salvage Value Discounting, and Municipal Asset Valuations.
"""

from typing import Dict, List, Any


class EmployeesEconomicValuationEngine:
    """
    Valuation modeling and asset accounting rules for employees.
    """

    @classmethod
    def calculate_depreciated_replacement_cost(
        cls,
        gross_replacement_cost: float,
        effective_age_years: float,
        total_economic_life_years: float,
        residual_salvage_percentage: float = 10.0,
    ) -> Dict[str, Any]:
        """
        DRC = GRC - (GRC - Salvage) * (Effective_Age / Economic_Life)
        """
        salvage_val = gross_replacement_cost * (residual_salvage_percentage / 100.0)
        depreciable_amount = gross_replacement_cost - salvage_val
        
        age_ratio = min(1.0, max(0.0, effective_age_years / max(1.0, total_economic_life_years)))
        accumulated_depreciation = depreciable_amount * age_ratio
        drc = gross_replacement_cost - accumulated_depreciation

        return {
            "app_module": "employees",
            "gross_replacement_cost": round(gross_replacement_cost, 2),
            "estimated_salvage_value": round(salvage_val, 2),
            "accumulated_depreciation": round(accumulated_depreciation, 2),
            "depreciated_replacement_cost_drc": round(drc, 2),
            "condition_consumption_pct": round(age_ratio * 100.0, 1),
            "remaining_economic_life_years": round(max(0.0, total_economic_life_years - effective_age_years), 1),
        }
