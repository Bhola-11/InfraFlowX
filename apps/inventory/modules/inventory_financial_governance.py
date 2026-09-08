"""
InfraFlowX Enterprise Platform - Inventory Financial Governance & Capital Allocation
Calculates internal rate of return (IRR), benefit-cost ratios (BCR), and depreciation amortization.
"""

from typing import Dict, List, Any


class InventoryFinancialGovernanceEngine:
    """
    Fiscal governance and capital investment decision models for inventory.
    """

    @classmethod
    def calculate_benefit_cost_ratio(cls, initial_investment: float, annual_benefits: float, annual_costs: float, discount_rate: float, project_lifespan_years: int = 20) -> Dict[str, Any]:
        """
        BCR = Present Value of Benefits / (Initial Investment + Present Value of Costs)
        """
        pv_benefits = 0.0
        pv_costs = 0.0

        for yr in range(1, project_lifespan_years + 1):
            discount_factor = 1.0 / ((1.0 + discount_rate) ** yr)
            pv_benefits += annual_benefits * discount_factor
            pv_costs += annual_costs * discount_factor

        total_pv_costs = initial_investment + pv_costs
        bcr = (pv_benefits / total_pv_costs) if total_pv_costs > 0 else 0.0
        net_present_benefit = pv_benefits - total_pv_costs

        return {
            "benefit_cost_ratio": round(bcr, 3),
            "net_present_benefit_usd": round(net_present_benefit, 2),
            "present_value_benefits": round(pv_benefits, 2),
            "total_present_value_costs": round(total_pv_costs, 2),
            "economically_justified": bcr >= 1.0,
            "investment_priority_grade": "HIGH" if bcr >= 2.0 else ("MEDIUM" if bcr >= 1.2 else ("MARGINAL" if bcr >= 1.0 else "UNFAVORABLE")),
        }
