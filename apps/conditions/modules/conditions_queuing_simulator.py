"""
InfraFlowX Enterprise Platform - Conditions M/M/c Municipal Queueing Engine
Computes average queue length, wait times, and server utilization for repair and service tickets.
"""

from typing import Dict, Any
import math


class ConditionsQueueingEngine:
    """
    Erlang-C / M/M/c multiserver queueing model for conditions.
    """

    @classmethod
    def evaluate_service_queue(cls, arrival_rate_lambda: float, service_rate_per_server_mu: float, num_servers_c: int = 3) -> Dict[str, Any]:
        l = arrival_rate_lambda
        mu = max(0.001, service_rate_per_server_mu)
        c = max(1, num_servers_c)

        utilization_rho = l / (c * mu)
        if utilization_rho >= 1.0:
            return {
                "utilization_rho": round(utilization_rho, 3),
                "is_stable": False,
                "status": "UNSTABLE_QUEUE_CAPACITY_EXCEEDED",
            }

        # P0 calculation
        sum_terms = sum(((l / mu) ** k) / math.factorial(k) for k in range(c))
        c_term = (((l / mu) ** c) / (math.factorial(c) * (1.0 - utilization_rho)))
        p0 = 1.0 / (sum_terms + c_term)

        # Average queue length Lq
        l_q = (p0 * ((l / mu) ** c) * utilization_rho) / (math.factorial(c) * ((1.0 - utilization_rho) ** 2))
        w_q_hours = l_q / l if l > 0 else 0.0
        w_total_hours = w_q_hours + (1.0 / mu)

        return {
            "app_module": "conditions",
            "servers_count": c,
            "utilization_rate_pct": round(utilization_rho * 100.0, 1),
            "average_queue_length_tickets": round(l_q, 2),
            "average_wait_time_in_queue_hours": round(w_q_hours, 2),
            "average_total_time_system_hours": round(w_total_hours, 2),
            "is_stable": True,
        }
