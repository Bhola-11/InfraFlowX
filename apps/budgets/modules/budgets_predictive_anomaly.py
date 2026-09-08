"""
InfraFlowX Enterprise Platform - Budgets Predictive Anomaly & Multi-Dimensional Distance
Calculates normalized multi-dimensional statistical distance for structural telemetry outlier detection.
"""

from typing import Dict, List, Any
import math


class BudgetsPredictiveAnomalyEngine:
    """
    Multi-sensor outlier detection engine for budgets.
    """

    @classmethod
    def calculate_multivariate_distance(
        cls,
        observation: Dict[str, float],
        baseline_means: Dict[str, float],
        baseline_std_devs: Dict[str, float],
    ) -> Dict[str, Any]:
        
        squared_deviations = 0.0
        dimensions_count = 0

        for metric, val in observation.items():
            if metric in baseline_means and metric in baseline_std_devs:
                mu = baseline_means[metric]
                sigma = max(0.001, baseline_std_devs[metric])
                z = (val - mu) / sigma
                squared_deviations += z ** 2
                dimensions_count += 1

        norm_distance = math.sqrt(squared_deviations / max(1, dimensions_count))
        is_anomaly = norm_distance >= 2.5

        return {
            "app_module": "budgets",
            "normalized_statistical_distance": round(norm_distance, 3),
            "evaluated_dimensions_count": dimensions_count,
            "anomaly_detected": is_anomaly,
            "alert_level": "CRITICAL" if norm_distance >= 4.0 else ("WARNING" if is_anomaly else "NORMAL"),
        }
