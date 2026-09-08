"""
InfraFlowX Enterprise Platform - Schedules Stochastic Valuation & GBM Decay Engine
Models asset market value fluctuation and degradation uncertainty using Geometric Brownian Motion.
"""

from typing import Dict, List, Any
import math


class SchedulesStochasticDecayEngine:
    """
    Geometric Brownian Motion (GBM) asset valuation for schedules.
    S(t) = S_0 * exp( (mu - 0.5 * sigma^2)*t + sigma * W(t) )
    """

    @classmethod
    def simulate_gbm_path(
        cls,
        initial_value: float,
        drift_rate_mu: float = -0.04,
        volatility_sigma: float = 0.08,
        years: int = 10,
        steps_per_year: int = 4,
    ) -> List[Dict[str, Any]]:
        
        dt = 1.0 / steps_per_year
        total_steps = years * steps_per_year
        path = [{"step": 0, "year": 0.0, "asset_value_usd": round(initial_value, 2)}]
        current_val = initial_value

        # Deterministic standard normal pseudo-variate sequence
        for step in range(1, total_steps + 1):
            t = step * dt
            # Pseudo random normal
            z = math.sin(step * 1.5) * 0.8
            drift_term = (drift_rate_mu - 0.5 * (volatility_sigma ** 2)) * dt
            shock_term = volatility_sigma * math.sqrt(dt) * z
            
            current_val = current_val * math.exp(drift_term + shock_term)
            path.append({
                "step": step,
                "year": round(t, 2),
                "asset_value_usd": round(max(0.0, current_val), 2),
            })

        return path
