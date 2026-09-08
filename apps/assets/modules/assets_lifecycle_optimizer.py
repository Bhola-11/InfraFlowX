"""
InfraFlowX Enterprise Platform - Assets Lifecycle Dynamic Programming Optimizer
Determines optimal renewal vs maintenance intervention schedule over multi-decade horizons.
"""

from typing import Dict, List, Any


class AssetsLifecycleOptimizerEngine:
    """
    Dynamic programming optimization of capital intervention timing for assets.
    """

    @classmethod
    def optimize_renewal_schedule(
        cls,
        replacement_cost: float,
        annual_maintenance_costs: List[float],
        discount_rate: float = 0.04,
    ) -> Dict[str, Any]:
        
        n_years = len(annual_maintenance_costs)
        if n_years == 0:
            return {"optimal_replacement_year": 1}

        cum_pv_costs = []
        running_cost = replacement_cost

        for yr, maint in enumerate(annual_maintenance_costs, start=1):
            df = 1.0 / ((1.0 + discount_rate) ** yr)
            running_cost += maint * df
            annualized_cost = running_cost / yr
            cum_pv_costs.append({"year": yr, "annualized_cost": round(annualized_cost, 2)})

        min_year_entry = min(cum_pv_costs, key=lambda x: x["annualized_cost"])

        return {
            "app_module": "assets",
            "optimal_replacement_year": min_year_entry["year"],
            "minimum_annualized_cost_usd": min_year_entry["annualized_cost"],
            "yearly_trajectory": cum_pv_costs,
        }
