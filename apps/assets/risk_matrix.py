"""
InfraFlowX - ISO 55000 Business Risk Exposure (BRE) & Criticality Engine
Calculates Consequence of Failure (CoF) x Probability of Failure (PoF) Matrix.
"""

from typing import Dict, Any


class AssetRiskMatrixEngine:
    """
    Computes asset risk scores across Safety, Environmental, Financial, and Operational dimensions.
    BRE = CoF * PoF
    """

    @classmethod
    def calculate_probability_of_failure(cls, condition_score: float, age_years: float, expected_life_years: float, maintenance_backlog_flag: bool = False) -> Dict[str, Any]:
        """
        Condition-adjusted Probability of Failure (PoF 1 to 5 scale).
        """
        life_ratio = age_years / max(1.0, expected_life_years)
        
        # Base PoF on 0-100 condition score
        if condition_score >= 85:
            base_pof = 1.0
        elif condition_score >= 70:
            base_pof = 2.0
        elif condition_score >= 55:
            base_pof = 3.0
        elif condition_score >= 40:
            base_pof = 4.0
        else:
            base_pof = 5.0

        # Adjust for age over useful life
        if life_ratio > 1.2:
            base_pof = min(5.0, base_pof + 1.0)
        if maintenance_backlog_flag:
            base_pof = min(5.0, base_pof + 0.5)

        return {
            "pof_score": round(base_pof, 1),
            "pof_rating": "VERY_LOW" if base_pof <= 1.5 else ("LOW" if base_pof <= 2.5 else ("MEDIUM" if base_pof <= 3.5 else ("HIGH" if base_pof <= 4.5 else "CRITICAL"))),
        }

    @classmethod
    def calculate_consequence_of_failure(cls, safety_impact: int, environmental_impact: int, direct_financial_cost_tier: int, community_disruption_tier: int) -> Dict[str, Any]:
        """
        Weighted CoF (1 to 5 scale).
        Weights: Safety (35%), Environmental (25%), Direct Financial (20%), Community/Operational (20%).
        """
        w_safety = 0.35 * max(1, min(5, safety_impact))
        w_env = 0.25 * max(1, min(5, environmental_impact))
        w_fin = 0.20 * max(1, min(5, direct_financial_cost_tier))
        w_ops = 0.20 * max(1, min(5, community_disruption_tier))
        
        total_cof = w_safety + w_env + w_fin + w_ops

        return {
            "cof_score": round(total_cof, 2),
            "cof_rating": "NEGLIGIBLE" if total_cof <= 1.5 else ("MINOR" if total_cof <= 2.5 else ("MODERATE" if total_cof <= 3.5 else ("MAJOR" if total_cof <= 4.5 else "CATASTROPHIC"))),
        }

    @classmethod
    def calculate_business_risk_exposure(cls, condition_score: float, age_years: float, expected_life_years: float, safety_impact: int = 3, environmental_impact: int = 2, direct_cost_tier: int = 3, community_disruption: int = 3) -> Dict[str, Any]:
        pof_data = cls.calculate_probability_of_failure(condition_score, age_years, expected_life_years)
        cof_data = cls.calculate_consequence_of_failure(safety_impact, environmental_impact, direct_cost_tier, community_disruption)
        
        pof = pof_data["pof_score"]
        cof = cof_data["cof_score"]
        bre = pof * cof  # 1 to 25 scale

        if bre <= 5.0:
            risk_tier = "LOW"
            action = "Routine Monitor"
        elif bre <= 12.0:
            risk_tier = "MEDIUM"
            action = "Planned Condition-Based Maintenance"
        elif bre <= 18.0:
            risk_tier = "HIGH"
            action = "Immediate Capital Refurbishment Required"
        else:
            risk_tier = "EXTREME_CRITICAL"
            action = "Urgent Interventions / Risk Mitigation Mandated"

        return {
            "pof_score": pof,
            "pof_rating": pof_data["pof_rating"],
            "cof_score": cof,
            "cof_rating": cof_data["cof_rating"],
            "business_risk_exposure_score": round(bre, 2),
            "risk_tier": risk_tier,
            "action_recommendation": action,
        }
