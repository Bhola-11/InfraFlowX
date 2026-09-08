"""
InfraFlowX - Multi-Channel Alert Routing & Duty Matrix Engine
Routes emergency alarms to Webhook, SMS, Email, and On-Call Engineers.
"""

from typing import Dict, List, Any


class AlertRouterEngine:
    """
    Channel selection and severity dispatch matrix.
    """

    SEVERITY_CHANNELS = {
        "CRITICAL": ["PAGER_SMS", "VOICE_CALL", "IN_APP", "SLACK_WEBHOOK", "EMAIL"],
        "HIGH": ["IN_APP", "SLACK_WEBHOOK", "EMAIL"],
        "MEDIUM": ["IN_APP", "EMAIL"],
        "LOW": ["IN_APP"],
    }

    @classmethod
    def route_alert(cls, alert_severity: str, module_name: str, message: str) -> Dict[str, Any]:
        sev = alert_severity.upper()
        channels = cls.SEVERITY_CHANNELS.get(sev, ["IN_APP"])

        return {
            "alert_severity": sev,
            "origin_module": module_name,
            "dispatched_channels": channels,
            "urgent_delivery": sev in ("CRITICAL", "HIGH"),
        }
