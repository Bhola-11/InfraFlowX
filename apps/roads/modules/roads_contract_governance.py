"""
InfraFlowX Enterprise Platform - Roads Contract Governance & SLA Penalty Matrix
Calculates liquidated damages, contract performance multipliers, and warranty claim recovery.
"""

from typing import Dict, List, Any


class RoadsContractGovernanceEngine:
    """
    Contractual SLA verification and liquidated damages calculator for roads.
    """

    @classmethod
    def calculate_liquidated_damages(
        cls,
        contract_value: float,
        scheduled_completion_days: int,
        actual_completion_days: int,
        daily_liquidated_damages_rate: float = 1500.0,
        max_penalty_cap_percentage: float = 15.0,
    ) -> Dict[str, Any]:
        delay_days = max(0, actual_completion_days - scheduled_completion_days)
        raw_damages = delay_days * daily_liquidated_damages_rate
        max_cap = contract_value * (max_penalty_cap_percentage / 100.0)
        assessed_damages = min(raw_damages, max_cap)
        net_contract_payout = max(0.0, contract_value - assessed_damages)

        return {
            "app_module": "roads",
            "contract_value": round(contract_value, 2),
            "scheduled_days": scheduled_completion_days,
            "actual_days": actual_completion_days,
            "days_delayed": delay_days,
            "assessed_liquidated_damages": round(assessed_damages, 2),
            "penalty_cap_applied": raw_damages > max_cap,
            "net_contract_payout": round(net_contract_payout, 2),
        }
