"""
InfraFlowX Enterprise Platform - Organizations Reliability Centered Maintenance (RCM) & FMEA Engine
Computes Failure Modes and Effects Analysis (FMEA) Risk Priority Numbers (RPN = S * O * D).
"""

from typing import Dict, List, Any


class OrganizationsRCMEngine:
    """
    RCM and FMEA decision matrix for organizations.
    """

    @classmethod
    def calculate_rpn_score(cls, severity_1_to_10: int, occurrence_1_to_10: int, detection_1_to_10: int) -> Dict[str, Any]:
        s = max(1, min(10, severity_1_to_10))
        o = max(1, min(10, occurrence_1_to_10))
        d = max(1, min(10, detection_1_to_10))

        rpn = s * o * d  # 1 to 1000 scale

        if rpn <= 50:
            action = "ROUTINE_MONITOR"
            priority = "LOW"
        elif rpn <= 125:
            action = "SCHEDULED_INSPECTION"
            priority = "MEDIUM"
        elif rpn <= 250:
            action = "PREVENTIVE_MAINTENANCE_OVERHAUL"
            priority = "HIGH"
        else:
            action = "REDESIGN_OR_IMMEDIATE_REPAIR"
            priority = "CRITICAL"

        return {
            "app_module": "organizations",
            "severity": s,
            "occurrence": o,
            "detection": d,
            "rpn_score": rpn,
            "priority_tier": priority,
            "recommended_action": action,
            "immediate_corrective_action_required": rpn > 200 or s >= 9,
        }
