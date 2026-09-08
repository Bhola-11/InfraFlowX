"""
InfraFlowX - Capital Improvement Plan (CIP) Multi-Year Budget Forecasting Engine
Implements Holt-Winters Double Exponential Smoothing for capital expenditure trends.
"""

from typing import Dict, List, Any


class BudgetForecastingEngine:
    """
    Forecasting capital replacement expenditure horizons and municipal fiscal requirements.
    """

    @classmethod
    def holt_linear_forecast(cls, historical_series: List[float], forecast_horizon_years: int = 5, alpha: float = 0.3, beta: float = 0.1) -> List[Dict[str, Any]]:
        """
        Holt's Two-Parameter Linear Exponential Smoothing:
        Level: l_t = alpha * y_t + (1 - alpha) * (l_{t-1} + b_{t-1})
        Trend: b_t = beta * (l_t - l_{t-1}) + (1 - beta) * b_{t-1}
        Forecast: y_{t+h} = l_t + h * b_t
        """
        if len(historical_series) < 2:
            return []

        # Initialization
        level = historical_series[0]
        trend = historical_series[1] - historical_series[0]

        for val in historical_series[1:]:
            last_level = level
            level = alpha * val + (1.0 - alpha) * (level + trend)
            trend = beta * (level - last_level) + (1.0 - beta) * trend

        # Generate future projections
        forecasts = []
        for h in range(1, forecast_horizon_years + 1):
            projected_value = level + h * trend
            forecasts.append({
                "horizon_year": h,
                "projected_expenditure": round(max(0.0, projected_value), 2),
                "trend_slope": round(trend, 2),
            })

        return forecasts
