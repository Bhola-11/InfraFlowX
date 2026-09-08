"""
InfraFlowX - Facility Redundancy & Markov Reliability Engine
Computes k-out-of-n system reliability, parallel redundancy, and steady-state availability.
"""

from typing import Dict, List, Any
import math


class FacilityReliabilityEngine:
    """
    System reliability modeling for critical municipal utilities, pump stations, and backup generators.
    """

    @classmethod
    def calculate_series_reliability(cls, component_reliabilities: List[float]) -> float:
        """R_series = Product(R_i)"""
        r_total = 1.0
        for r in component_reliabilities:
            r_total *= max(0.0, min(1.0, r))
        return round(r_total, 5)

    @classmethod
    def calculate_parallel_reliability(cls, component_reliabilities: List[float]) -> float:
        """R_parallel = 1 - Product(1 - R_i)"""
        unavail = 1.0
        for r in component_reliabilities:
            unavail *= (1.0 - max(0.0, min(1.0, r)))
        return round(1.0 - unavail, 5)

    @classmethod
    def calculate_k_out_of_n_system(cls, n_total_units: int, k_required_units: int, unit_reliability: float) -> Dict[str, Any]:
        """
        Binomial k-out-of-n active redundancy reliability:
        R_k_n = Sum_{i=k}^n (n choose i) * R^i * (1-R)^(n-i)
        """
        r = max(0.0, min(1.0, unit_reliability))
        n = n_total_units
        k = k_required_units
        
        system_r = 0.0
        for i in range(k, n + 1):
            comb = math.comb(n, i)
            term = comb * (r ** i) * ((1.0 - r) ** (n - i))
            system_r += term

        return {
            "total_redundant_units": n,
            "required_operating_units": k,
            "single_unit_reliability": r,
            "system_reliability": round(system_r, 5),
            "system_unavailability": round(1.0 - system_r, 5),
        }

    @classmethod
    def markov_two_unit_standby_availability(cls, failure_rate_lambda: float, repair_rate_mu: float) -> Dict[str, Any]:
        """
        Steady-state availability of 1-operating, 1-cold-standby system with 1 repairman:
        A = (mu^2 + 2*lambda*mu) / (mu^2 + 2*lambda*mu + 2*lambda^2)
        """
        l = failure_rate_lambda
        m = repair_rate_mu
        
        denom = (m ** 2) + (2.0 * l * m) + (2.0 * (l ** 2))
        if denom <= 0:
            return {"steady_state_availability": 0.0}
        
        avail = ((m ** 2) + (2.0 * l * m)) / denom
        unavail = 1.0 - avail
        unplanned_downtime_hours_per_year = unavail * 8760.0

        return {
            "failure_rate_per_hour": l,
            "repair_rate_per_hour": m,
            "steady_state_availability": round(avail, 6),
            "unplanned_downtime_hours_per_year": round(unplanned_downtime_hours_per_year, 2),
            "system_uptime_percentage": round(avail * 100.0, 4),
        }
