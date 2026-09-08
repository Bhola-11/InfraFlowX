"""
InfraFlowX Enterprise Platform - Contractors Competing Risks & Multi-Mode Hazard Engine
Evaluates combined reliability across independent failure mechanisms (Mechanical, Thermal, Electrical, Corrosion).
"""

from typing import Dict, List, Any
import math


class ContractorsCompetingRisksEngine:
    """
    Competing risk hazard modeling: R_sys(t) = Product( R_i(t) )
    """

    @classmethod
    def evaluate_combined_reliability(cls, failure_modes: List[Dict[str, float]], operating_time_years: float) -> Dict[str, Any]:
        """
        failure_modes: List of {"name": "Corrosion", "eta_characteristic_life": 25.0, "beta_shape": 2.2}
        """
        t = max(0.01, operating_time_years)
        sys_reliability = 1.0
        mode_reliabilities = []

        for mode in failure_modes:
            name = mode.get("name", "Unknown")
            eta = max(0.1, mode.get("eta_characteristic_life", 20.0))
            beta = max(0.1, mode.get("beta_shape", 1.5))

            # Cumulative failure F(t) = 1 - exp(-(t/eta)^beta)
            r_i = math.exp(-((t / eta) ** beta))
            sys_reliability *= r_i

            mode_reliabilities.append({
                "failure_mode": name,
                "reliability_r_i": round(r_i, 4),
                "failure_probability_f_i": round(1.0 - r_i, 4),
            })

        return {
            "app_module": "contractors",
            "operating_time_years": t,
            "system_overall_reliability": round(sys_reliability, 4),
            "system_failure_probability": round(1.0 - sys_reliability, 4),
            "mode_breakdown": mode_reliabilities,
            "dominant_failure_mode": min(mode_reliabilities, key=lambda x: x["reliability_r_i"])["failure_mode"] if mode_reliabilities else None,
        }
