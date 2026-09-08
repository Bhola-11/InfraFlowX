"""
InfraFlowX Enterprise Platform - Workorders Copula Joint Probability & Failure Dependence Engine
Models joint multi-asset degradation dependence using Archimedean (Clayton) copulas.
"""

from typing import Dict, Any
import math


class WorkordersCopulaEngine:
    """
    Clayton Archimedean Copula for joint tail dependency modeling in workorders.
    C(u, v) = [ u^(-theta) + v^(-theta) - 1 ]^(-1 / theta)
    """

    @classmethod
    def calculate_clayton_joint_probability(cls, u_marginal: float, v_marginal: float, theta_dependence: float = 2.0) -> Dict[str, Any]:
        u = max(0.001, min(0.999, u_marginal))
        v = max(0.001, min(0.999, v_marginal))
        th = max(0.1, theta_dependence)

        term = (u ** -th) + (v ** -th) - 1.0
        if term <= 0:
            joint_prob = 0.0
        else:
            joint_prob = term ** (-1.0 / th)

        joint_prob = max(0.0, min(1.0, joint_prob))
        tail_dependence_lambda = 2.0 ** (-1.0 / th)

        return {
            "app_module": "workorders",
            "marginal_u": u,
            "marginal_v": v,
            "joint_failure_probability": round(joint_prob, 4),
            "lower_tail_dependence_lambda": round(tail_dependence_lambda, 3),
            "correlation_tier": "STRONG_CORRELATION" if th >= 3.0 else ("MODERATE" if th >= 1.5 else "WEAK"),
        }
