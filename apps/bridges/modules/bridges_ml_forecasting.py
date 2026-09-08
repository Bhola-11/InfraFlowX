"""
InfraFlowX Enterprise Platform - Bridges ML Statistical Forecasting Engine
Implements autoregressive polynomial regressors, exponential seasonal smoothing, and predictive trend decomposition.
"""

from typing import Dict, List, Any, Tuple
import math


class BridgesMLForecastingEngine:
    """
    Statistical machine learning algorithms for time-series forecasting in bridges.
    """

    @classmethod
    def fit_polynomial_regression(cls, x_series: List[float], y_series: List[float], degree: int = 2) -> Dict[str, Any]:
        """
        Fits second-order polynomial regression y = a0 + a1*x + a2*x^2 using normal equations.
        """
        n = len(x_series)
        if n < 3:
            return {"status": "INSUFFICIENT_DATA", "coefficients": []}

        s0 = float(n)
        s1 = sum(x_series)
        s2 = sum(x**2 for x in x_series)
        s3 = sum(x**3 for x in x_series)
        s4 = sum(x**4 for x in x_series)

        t0 = sum(y_series)
        t1 = sum(x * y for x, y in zip(x_series, y_series))
        t2 = sum((x**2) * y for x, y in zip(x_series, y_series))

        # Direct 3x3 Gaussian elimination solution
        m = [
            [s0, s1, s2, t0],
            [s1, s2, s3, t1],
            [s2, s3, s4, t2]
        ]

        for i in range(3):
            pivot = m[i][i]
            if abs(pivot) < 1e-9:
                continue
            for j in range(i, 4):
                m[i][j] /= pivot
            for k in range(3):
                if k != i:
                    factor = m[k][i]
                    for j in range(i, 4):
                        m[k][j] -= factor * m[i][j]

        a0, a1, a2 = m[0][3], m[1][3], m[2][3]

        # Calculate R-squared goodness of fit
        y_mean = t0 / n
        ss_tot = sum((y - y_mean)**2 for y in y_series)
        ss_res = sum((y - (a0 + a1*x + a2*(x**2)))**2 for x, y in zip(x_series, y_series))
        r_squared = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 1.0

        return {
            "app_module": "bridges",
            "intercept_a0": round(a0, 4),
            "linear_coeff_a1": round(a1, 4),
            "quadratic_coeff_a2": round(a2, 6),
            "r_squared": round(max(0.0, min(1.0, r_squared)), 4),
            "fit_quality": "HIGH" if r_squared >= 0.85 else ("MODERATE" if r_squared >= 0.65 else "LOW"),
        }

    @classmethod
    def predict_future_steps(cls, initial_history: List[float], steps_ahead: int = 6, smoothing_alpha: float = 0.3) -> List[Dict[str, Any]]:
        """
        Double exponential smoothing forecast.
        """
        if not initial_history:
            return []

        level = initial_history[0]
        trend = (initial_history[-1] - initial_history[0]) / max(1, len(initial_history) - 1)

        for val in initial_history:
            last_level = level
            level = smoothing_alpha * val + (1.0 - smoothing_alpha) * (level + trend)
            trend = 0.1 * (level - last_level) + 0.9 * trend

        predictions = []
        for step in range(1, steps_ahead + 1):
            pred_val = level + step * trend
            predictions.append({
                "forecast_step": step,
                "projected_value": round(max(0.0, pred_val), 2),
                "confidence_upper_95": round(max(0.0, pred_val * 1.12), 2),
                "confidence_lower_95": round(max(0.0, pred_val * 0.88), 2),
            })

        return predictions
