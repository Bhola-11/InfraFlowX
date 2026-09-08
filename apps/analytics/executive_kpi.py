"""
InfraFlowX - Executive KPI & Infrastructure Health Index (IHI) Engine
Synthesizes city-wide asset condition, maintenance backlog, and fiscal performance scores.
"""

from typing import Dict, Any


class ExecutiveKPIEngine:
    """
    Computes holistic municipal infrastructure health score (0-100).
    """

    @classmethod
    def calculate_infrastructure_health_index(
        cls,
        avg_asset_condition_pct: float,
        pm_compliance_pct: float,
        capital_backlog_ratio_fci: float,
        critical_incident_rate_per_100: float,
    ) -> Dict[str, Any]:
        """
        IHI = 0.40 * Condition + 0.30 * PM_Compliance + 0.20 * (1 - FCI)*100 - 0.10 * Incidents
        """
        cond_term = 0.40 * avg_asset_condition_pct
        pm_term = 0.30 * pm_compliance_pct
        fci_term = 0.20 * max(0.0, (1.0 - capital_backlog_ratio_fci) * 100.0)
        incident_penalty = min(20.0, critical_incident_rate_per_100 * 2.0)
        
        ihi = max(0.0, min(100.0, cond_term + pm_term + fci_term - incident_penalty))

        if ihi >= 85.0:
            rating = "STATE_OF_GOOD_REPAIR"
            tier = "OPTIMAL"
        elif ihi >= 70.0:
            rating = "ADEQUATE_OPERATING_CONDITION"
            tier = "SATISFACTORY"
        elif ihi >= 55.0:
            rating = "AT_RISK_DEGRADATION"
            tier = "ATTENTION_REQUIRED"
        else:
            rating = "CRITICAL_INFRASTRUCTURE_DEFICIT"
            tier = "EMERGENCY_INTERVENTION"

        return {
            "infrastructure_health_index_ihi": round(ihi, 1),
            "rating_description": rating,
            "operational_tier": tier,
            "component_breakdown": {
                "condition_weighted_score": round(cond_term, 1),
                "pm_compliance_weighted_score": round(pm_term, 1),
                "fci_weighted_score": round(fci_term, 1),
                "incident_penalty": round(incident_penalty, 1),
            },
        }
