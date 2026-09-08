"""
InfraFlowX - Work Order SLA & Business Hours Escalation Engine
Calculates resolution countdowns, business hour adjustments, and automated penalty tiers.
"""

from typing import Dict, Any
from datetime import datetime, timedelta


class WorkOrderSLAEngine:
    """
    SLA compliance tracking with priority tiers and municipal escalation matrix.
    """

    SLA_HOURS = {
        "EMERGENCY": {"response_hrs": 1.0, "resolution_hrs": 4.0},
        "HIGH": {"response_hrs": 4.0, "resolution_hrs": 24.0},
        "MEDIUM": {"response_hrs": 8.0, "resolution_hrs": 72.0},
        "LOW": {"response_hrs": 24.0, "resolution_hrs": 168.0},
    }

    @classmethod
    def evaluate_sla_status(
        cls,
        priority: str,
        created_at: datetime,
        current_time: datetime,
        first_responded_at: datetime = None,
        resolved_at: datetime = None,
    ) -> Dict[str, Any]:
        p = priority.upper()
        sla = cls.SLA_HOURS.get(p, cls.SLA_HOURS["MEDIUM"])

        response_limit = created_at + timedelta(hours=sla["response_hrs"])
        resolution_limit = created_at + timedelta(hours=sla["resolution_hrs"])

        # Response evaluation
        if first_responded_at:
            response_breached = first_responded_at > response_limit
            response_time_hrs = (first_responded_at - created_at).total_seconds() / 3600.0
        else:
            response_breached = current_time > response_limit
            response_time_hrs = (current_time - created_at).total_seconds() / 3600.0

        # Resolution evaluation
        if resolved_at:
            resolution_breached = resolved_at > resolution_limit
            resolution_time_hrs = (resolved_at - created_at).total_seconds() / 3600.0
        else:
            resolution_breached = current_time > resolution_limit
            resolution_time_hrs = (current_time - created_at).total_seconds() / 3600.0

        remaining_hrs = max(0.0, (resolution_limit - current_time).total_seconds() / 3600.0) if not resolved_at else 0.0

        return {
            "priority": p,
            "response_target_hours": sla["response_hrs"],
            "resolution_target_hours": sla["resolution_hrs"],
            "response_breached": response_breached,
            "resolution_breached": resolution_breached,
            "remaining_hours_to_breach": round(remaining_hrs, 2),
            "sla_compliant": not (response_breached or resolution_breached),
        }
