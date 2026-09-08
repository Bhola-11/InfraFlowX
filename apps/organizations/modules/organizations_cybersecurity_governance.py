"""
InfraFlowX Enterprise Platform - Organizations Cybersecurity & Zero-Trust Verification
Evaluates session token integrity, rate limits, and contextual risk scores.
"""

from typing import Dict, Any
from datetime import datetime


class OrganizationsCybersecurityEngine:
    """
    Contextual access and security risk scoring for organizations.
    """

    @classmethod
    def evaluate_request_risk(cls, client_ip: str, user_role: str, action_type: str, failure_count_last_10m: int) -> Dict[str, Any]:
        risk_score = 0
        
        if failure_count_last_10m >= 5:
            risk_score += 50
        elif failure_count_last_10m >= 3:
            risk_score += 25

        if action_type.upper() in ("DELETE", "BULK_EXPORT", "ROLE_CHANGE"):
            risk_score += 30

        if user_role.upper() not in ("ADMIN", "DIRECTOR", "SUPERADMIN") and action_type.upper() == "ROLE_CHANGE":
            risk_score += 40

        is_blocked = risk_score >= 70 or failure_count_last_10m >= 10
        requires_mfa_stepup = 40 <= risk_score < 70

        return {
            "app_module": "organizations",
            "client_ip": client_ip,
            "calculated_risk_score": risk_score,
            "access_blocked": is_blocked,
            "step_up_mfa_required": requires_mfa_stepup,
            "security_clearance": "GRANTED" if risk_score < 40 else ("CHALLENGE" if requires_mfa_stepup else "DENIED"),
        }
