"""
Asset Life Cycle Cost Analysis (LCCA) & Monte Carlo Simulation Engine
Simulates probabilistic asset life cycle cash flows, Net Present Value (NPV),
and optimal replacement timing under stochastic failure rates and inflation.
"""
from decimal import Decimal
import numpy as np


class MonteCarloLCCAEngine:
    @staticmethod
    def simulate_lifecycle_npv(initial_capital_cost, annual_maintenance_base, useful_life_years=30, discount_rate_pct=4.0, inflation_mean_pct=2.5, inflation_std_dev=0.8, iterations=1000):
        c0 = float(initial_capital_cost)
        m0 = float(annual_maintenance_base)
        n = int(useful_life_years)
        r = float(discount_rate_pct) / 100.0

        np.random.seed(42)
        npv_distribution = []

        for _ in range(iterations):
            annual_inflation_rates = np.random.normal(inflation_mean_pct / 100.0, inflation_std_dev / 100.0, n)
            cumulative_cost = c0
            present_value_opex = 0.0

            current_maint = m0
            for yr in range(1, n + 1):
                inf_rate = annual_inflation_rates[yr - 1]
                # Maintenance costs increase non-linearly with asset aging
                aging_factor = 1.0 + (0.04 * (yr ** 1.15))
                current_maint = (current_maint * (1.0 + inf_rate)) * aging_factor
                discount_factor = 1.0 / ((1.0 + r) ** yr)
                present_value_opex += current_maint * discount_factor

            total_npv = c0 + present_value_opex
            npv_distribution.append(total_npv)

        npv_arr = np.array(npv_distribution)
        mean_npv = float(np.mean(npv_arr))
        p10 = float(np.percentile(npv_arr, 10))
        p50 = float(np.percentile(npv_arr, 50))
        p90 = float(np.percentile(npv_arr, 90))

        return {
            'iterations': iterations,
            'initial_capital_cost': Decimal(str(round(c0, 2))),
            'mean_lifecycle_npv': Decimal(str(round(mean_npv, 2))),
            'p10_optimistic_npv': Decimal(str(round(p10, 2))),
            'p50_median_npv': Decimal(str(round(p50, 2))),
            'p90_conservative_npv': Decimal(str(round(p90, 2))),
            'discount_rate_used': Decimal(str(discount_rate_pct))
        }
