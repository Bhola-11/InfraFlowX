"""
InfraFlowX Enterprise Platform - Budgets Quantitative Analytics & Risk Engine
Implements statistical risk modeling, sensitivity distributions, and time-series anomaly filters.
"""

from typing import Dict, List, Any, Optional, Tuple
import math
from datetime import datetime


class BudgetsRiskAnalyticsEngine:
    """
    Statistical risk evaluation, probabilistic failure forecasting, and Monte Carlo sensitivity modeling.
    """

    @classmethod
    def calculate_probabilistic_risk(cls, failure_probability_base: float, exposure_index: float, consequence_severity: float, mitigation_efficiency: float = 0.0) -> Dict[str, Any]:
        """
        Risk R = PoF * CoF * Exposure * (1 - Mitigation)
        """
        pof = max(0.0, min(1.0, failure_probability_base))
        cof = max(1.0, min(10.0, consequence_severity))
        exp_idx = max(0.1, min(5.0, exposure_index))
        mit = max(0.0, min(0.95, mitigation_efficiency))

        raw_risk_score = pof * cof * exp_idx * 10.0
        residual_risk_score = raw_risk_score * (1.0 - mit)

        if residual_risk_score < 10.0:
            level = "LOW_NEGLIGIBLE"
            strategy = "ACCEPT_AND_MONITOR"
        elif residual_risk_score < 25.0:
            level = "MODERATE_CONTROLLED"
            strategy = "PREVENTIVE_MAINTENANCE"
        elif residual_risk_score < 50.0:
            level = "ELEVATED_SUBSTANTIAL"
            strategy = "ENGINEERING_CONTROLS_AND_RETROFIT"
        else:
            level = "CRITICAL_INTOLERABLE"
            strategy = "IMMEDIATE_CAPITAL_REPLACEMENT"

        return {
            "raw_risk_score": round(raw_risk_score, 2),
            "residual_risk_score": round(residual_risk_score, 2),
            "risk_tier": level,
            "recommended_strategy": strategy,
            "risk_reduction_pct": round(mit * 100.0, 1),
        }

    @classmethod
    def analyze_trend_series(cls, historical_data_points: List[float]) -> Dict[str, Any]:
        """
        Computes rolling statistics, linear slope direction, and variance volatility.
        """
        n = len(historical_data_points)
        if n < 2:
            return {"status": "INSUFFICIENT_DATA", "trend": "STABLE"}

        mean = sum(historical_data_points) / n
        variance = sum((x - mean) ** 2 for x in historical_data_points) / (n - 1) if n > 1 else 0.0
        std_dev = math.sqrt(variance)

        # Linear regression slope: b = Sum((x_i - mean_x)*(y_i - mean_y)) / Sum((x_i - mean_x)^2)
        x_mean = (n - 1) / 2.0
        numerator = sum((i - x_mean) * (y - mean) for i, y in enumerate(historical_data_points))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        slope = (numerator / denominator) if denominator > 0 else 0.0

        trend_direction = "INCREASING" if slope > 0.05 else ("DECREASING" if slope < -0.05 else "STABLE")

        return {
            "data_points_count": n,
            "mean_value": round(mean, 3),
            "std_deviation": round(std_dev, 3),
            "variance": round(variance, 3),
            "linear_slope": round(slope, 4),
            "trend_direction": trend_direction,
            "coefficient_of_variation": round((std_dev / mean) if mean != 0 else 0.0, 4),
        }

    @classmethod
    def simulate_failure_horizon(cls, failure_rate_lambda: float, simulation_years: int = 10, time_step_months: int = 1) -> List[Dict[str, Any]]:
        """
        Exponential reliability distribution: R(t) = exp(-lambda * t)
        """
        steps = []
        total_months = simulation_years * 12
        for m in range(0, total_months + 1, time_step_months):
            t_years = m / 12.0
            r_t = math.exp(-failure_rate_lambda * t_years)
            f_t = 1.0 - r_t
            steps.append({
                "month": m,
                "elapsed_years": round(t_years, 2),
                "survival_probability": round(r_t, 4),
                "cumulative_failure_probability": round(f_t, 4),
            })
        return steps
