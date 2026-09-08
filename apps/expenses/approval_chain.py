"""
InfraFlowX - Delegation of Financial Authority (DOA) Approval Workflow Engine
Routes municipal infrastructure expenditures based on tiered financial limits.
"""

from typing import Dict, Any


class ExpenseApprovalChainEngine:
    """
    Determines required approval tier based on expenditure threshold.
    """

    THRESHOLDS = [
        {"tier": "TIER_1_SUPERVISOR", "max_amount": 1_000.0, "required_role": "SUPERVISOR"},
        {"tier": "TIER_2_DEPARTMENT_MANAGER", "max_amount": 10_000.0, "required_role": "MANAGER"},
        {"tier": "TIER_3_DIRECTOR_OF_PUBLIC_WORKS", "max_amount": 50_000.0, "required_role": "DIRECTOR"},
        {"tier": "TIER_4_CHIEF_FINANCIAL_OFFICER", "max_amount": 250_000.0, "required_role": "CFO"},
        {"tier": "TIER_5_CITY_COUNCIL_APPROVAL", "max_amount": float("inf"), "required_role": "CITY_COUNCIL"},
    ]

    @classmethod
    def determine_required_approval(cls, expense_amount: float) -> Dict[str, Any]:
        for rule in cls.THRESHOLDS:
            if expense_amount <= rule["max_amount"]:
                return {
                    "expense_amount": expense_amount,
                    "required_approval_tier": rule["tier"],
                    "approver_role_required": rule["required_role"],
                    "city_council_vote_needed": rule["tier"] == "TIER_5_CITY_COUNCIL_APPROVAL",
                }
        return {"required_approval_tier": "TIER_5_CITY_COUNCIL_APPROVAL", "approver_role_required": "CITY_COUNCIL"}
