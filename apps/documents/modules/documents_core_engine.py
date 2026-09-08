"""
InfraFlowX Enterprise Platform - Documents Core Lifecycle & Computational Engine
Production module implementing deterministic domain state evaluation, validation rules,
and numerical modeling for municipal infrastructure management.
"""

from typing import Dict, List, Any, Optional, Tuple, Set
import math
from datetime import datetime, date, timedelta
from decimal import Decimal
import logging

logger = logging.getLogger("infraflowx.documents.core")


class DocumentsLifecycleManager:
    """
    Manages operational lifecycles, lifecycle state progression, integrity rules,
    and computational metrics for documents infrastructure records.
    """

    DEFAULT_PARAMETERS: Dict[str, Any] = {
        "inspection_interval_days": 180,
        "criticality_threshold": 75.0,
        "escalation_window_hours": 48.0,
        "depreciation_rate_annual": 0.05,
        "contingency_factor": 1.15,
        "max_retry_attempts": 3,
        "tolerance_limit": 0.02,
        "reliability_target": 0.985,
    }

    def __init__(self, tenant_id: int, config: Optional[Dict[str, Any]] = None):
        self.tenant_id = tenant_id
        self.config = {**self.DEFAULT_PARAMETERS, **(config or {})}
        self.audit_log: List[Dict[str, Any]] = []

    def calculate_health_index(self, performance_score: float, wear_factor: float, age_years: float, max_service_life: float) -> Dict[str, Any]:
        """
        Computes composite operational health index (0 to 100):
        H(t) = P * (1 - (age / max_life)^1.5) * (1 - wear_factor * 0.4)
        """
        p = max(0.0, min(100.0, performance_score))
        w = max(0.0, min(1.0, wear_factor))
        age_ratio = min(1.0, age_years / max(1.0, max_service_life))
        
        life_depreciation = (age_ratio ** 1.5)
        wear_penalty = w * 0.40
        
        composite_score = p * (1.0 - life_depreciation * 0.60) * (1.0 - wear_penalty)
        composite_score = max(0.0, min(100.0, composite_score))
        
        if composite_score >= 85.0:
            status = "EXCELLENT_OPTIMAL"
            urgency = "NONE"
        elif composite_score >= 70.0:
            status = "GOOD_SATISFACTORY"
            urgency = "MONITOR"
        elif composite_score >= 50.0:
            status = "FAIR_MODERATE_DEGRADATION"
            urgency = "SCHEDULED_MAINTENANCE"
        elif composite_score >= 30.0:
            status = "POOR_CRITICAL_INTERVENTION_NEEDED"
            urgency = "HIGH_PRIORITY"
        else:
            status = "FAILED_IMMEDIATE_SHUTDOWN"
            urgency = "EMERGENCY"

        result = {
            "app_module": "documents",
            "tenant_id": self.tenant_id,
            "calculated_at": datetime.now().isoformat(),
            "composite_health_index": round(composite_score, 2),
            "status_rating": status,
            "intervention_urgency": urgency,
            "factors": {
                "performance_score": p,
                "wear_factor": w,
                "life_consumption_pct": round(age_ratio * 100.0, 1),
            }
        }
        self.audit_log.append({"action": "CALCULATE_HEALTH", "timestamp": datetime.now().isoformat(), "score": composite_score})
        return result

    def project_lifecycle_costs(self, initial_capital_cost: float, annual_o_m_cost: float, inflation_rate: float, discount_rate: float, analysis_years: int = 20) -> Dict[str, Any]:
        """
        Net Present Value (NPV) lifecycle cost analysis over multi-year horizon.
        NPV = Initial_CapEx + Sum_{t=1}^N [ O&M_t * (1+i)^t / (1+d)^t ]
        """
        npv = initial_capital_cost
        yearly_projections = []
        cumulative_cost = initial_capital_cost

        for yr in range(1, analysis_years + 1):
            inflated_om = annual_o_m_cost * ((1.0 + inflation_rate) ** yr)
            discounted_om = inflated_om / ((1.0 + discount_rate) ** yr)
            npv += discounted_om
            cumulative_cost += inflated_om
            
            yearly_projections.append({
                "year": yr,
                "inflated_om_cost": round(inflated_om, 2),
                "discounted_present_value": round(discounted_om, 2),
                "cumulative_nominal_cost": round(cumulative_cost, 2),
            })

        return {
            "analysis_horizon_years": analysis_years,
            "initial_capex": round(initial_capital_cost, 2),
            "total_lifecycle_npv": round(npv, 2),
            "annualized_equivalent_cost": round(npv * (discount_rate / (1.0 - (1.0 + discount_rate) ** -analysis_years)), 2),
            "yearly_breakdown": yearly_projections,
        }

    def evaluate_compliance_matrix(self, criteria_scores: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluates regulatory and operational compliance matrix.
        criteria_scores: List of {"name": "...", "score": 0-100, "weight": 1.0, "is_mandatory": bool}
        """
        if not criteria_scores:
            return {"status": "NO_CRITERIA", "compliant": False}

        total_weighted = 0.0
        total_weight = 0.0
        mandatory_failures = []

        for item in criteria_scores:
            score = item.get("score", 0.0)
            weight = item.get("weight", 1.0)
            is_mand = item.get("is_mandatory", False)
            
            total_weighted += score * weight
            total_weight += weight

            if is_mand and score < 70.0:
                mandatory_failures.append(item.get("name", "Unknown Criterion"))

        weighted_avg = total_weighted / total_weight if total_weight > 0 else 0.0
        is_compliant = weighted_avg >= 75.0 and len(mandatory_failures) == 0

        return {
            "app_module": "documents",
            "overall_compliance_score": round(weighted_avg, 2),
            "is_compliant": is_compliant,
            "mandatory_deficiencies_count": len(mandatory_failures),
            "deficiencies": mandatory_failures,
            "evaluated_items_count": len(criteria_scores),
        }
