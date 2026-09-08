"""
InfraFlowX - Budget Variance & Monthly Burn Velocity Engine
Computes Favorable / Unfavorable variances and forecasts fiscal year-end budget surplus/deficit.
"""

from typing import Dict, List, Any


class BudgetVarianceEngine:
    """
    Analyzes actual expenditure versus allocated budget across departments.
    """

    @classmethod
    def calculate_budget_variance(cls, allocated_budget: float, actual_expenditures: float, committed_encumbrances: float = 0.0) -> Dict[str, Any]:
        total_obligated = actual_expenditures + committed_encumbrances
        variance = allocated_budget - total_obligated
        variance_pct = (variance / allocated_budget * 100.0) if allocated_budget > 0 else 0.0

        is_favorable = variance >= 0

        return {
            "allocated_budget": round(allocated_budget, 2),
            "actual_expenditures": round(actual_expenditures, 2),
            "committed_encumbrances": round(committed_encumbrances, 2),
            "total_obligated_funds": round(total_obligated, 2),
            "variance_amount": round(variance, 2),
            "variance_percentage": round(variance_pct, 2),
            "variance_type": "FAVORABLE" if is_favorable else "UNFAVORABLE_OVERRUN",
            "funds_available_remaining": round(max(0.0, variance), 2),
        }
