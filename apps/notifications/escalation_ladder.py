"""
InfraFlowX - Alert Escalation Ladder & Acknowledgment Timeout State Machine
Escalates unacknowledged infrastructure alerts from Tier-1 Techs to Department Directors.
"""

from typing import Dict, Any


class EscalationLadderEngine:
    """
    Tiered escalation based on elapsed minutes without acknowledgment.
    """

    ESCALATION_TIERS = [
        {"tier": 1, "role": "FIELD_TECHNICIAN", "timeout_minutes": 15},
        {"tier": 2, "role": "OPERATIONS_SUPERVISOR", "timeout_minutes": 30},
        {"tier": 3, "role": "MAINTENANCE_DIRECTOR", "timeout_minutes": 60},
        {"tier": 4, "role": "MUNICIPAL_COMMISSIONER", "timeout_minutes": 120},
    ]

    @classmethod
    def determine_current_escalation_tier(cls, elapsed_unacknowledged_minutes: float) -> Dict[str, Any]:
        current_tier = cls.ESCALATION_TIERS[0]
        for t in cls.ESCALATION_TIERS:
            if elapsed_unacknowledged_minutes >= t["timeout_minutes"]:
                current_tier = t

        return {
            "elapsed_minutes": elapsed_unacknowledged_minutes,
            "active_tier_level": current_tier["tier"],
            "target_role": current_tier["role"],
            "escalated_to_executive": current_tier["tier"] >= 3,
        }
