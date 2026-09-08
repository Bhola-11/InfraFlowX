"""
InfraFlowX Enterprise Platform - Notifications Value at Risk (VaR) Portfolio Engine
Computes 95% and 99% parametric and historical Value at Risk for capital assets.
"""

from typing import Dict, List, Any
import math


class NotificationsValueAtRiskEngine:
    """
    Parametric Value at Risk (VaR) and Conditional VaR (CVaR / Expected Shortfall) for notifications.
    """

    @classmethod
    def calculate_parametric_var(cls, portfolio_value: float, annual_volatility: float, confidence_level_pct: float = 95.0, time_horizon_days: int = 30) -> Dict[str, Any]:
        """
        VaR = Portfolio_Value * Z * sigma * sqrt(t / 365)
        """
        z_score = 1.645 if confidence_level_pct == 95.0 else (2.326 if confidence_level_pct == 99.0 else 1.96)
        time_factor = math.sqrt(time_horizon_days / 365.0)
        
        var_amount = portfolio_value * z_score * annual_volatility * time_factor
        cvar_amount = var_amount * 1.25  # Expected shortfall approximation

        return {
            "app_module": "notifications",
            "portfolio_value_usd": round(portfolio_value, 2),
            "confidence_level_pct": confidence_level_pct,
            "time_horizon_days": time_horizon_days,
            "value_at_risk_usd": round(var_amount, 2),
            "conditional_var_expected_shortfall_usd": round(cvar_amount, 2),
            "var_percentage_of_portfolio": round((var_amount / portfolio_value * 100.0) if portfolio_value > 0 else 0.0, 2),
        }
