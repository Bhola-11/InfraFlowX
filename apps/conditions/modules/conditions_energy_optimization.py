"""
InfraFlowX Enterprise Platform - Conditions Energy Optimization & Carbon Accounting Engine
Models energy demand profiles, peak load shaving, and Scope 1/2 greenhouse gas emission savings.
"""

from typing import Dict, List, Any


class ConditionsEnergyOptimizationEngine:
    """
    Energy conservation and carbon accounting calculations for conditions.
    """

    @classmethod
    def calculate_energy_savings_payback(cls, retrofit_capital_cost: float, annual_kwh_baseline: float, annual_kwh_post_retrofit: float, electricity_rate_kwh: float = 0.14) -> Dict[str, Any]:
        kwh_saved = max(0.0, annual_kwh_baseline - annual_kwh_post_retrofit)
        annual_financial_savings = kwh_saved * electricity_rate_kwh
        simple_payback_years = (retrofit_capital_cost / annual_financial_savings) if annual_financial_savings > 0 else float("inf")
        
        # Carbon offset (0.385 kg CO2e / kWh)
        annual_co2_offset_metric_tons = (kwh_saved * 0.385) / 1000.0

        return {
            "app_module": "conditions",
            "annual_energy_saved_kwh": round(kwh_saved, 1),
            "annual_cost_savings_usd": round(annual_financial_savings, 2),
            "simple_payback_years": round(simple_payback_years, 2),
            "annual_co2e_reduction_metric_tons": round(annual_co2_offset_metric_tons, 2),
            "project_viable": simple_payback_years <= 7.0,
        }
