"""
InfraFlowX - Predictive Maintenance & Remaining Useful Life (RUL) Engine
Estimates RUL based on exponential sensor degradation curves and vibration RMS metrics.
"""

from typing import Dict, List, Any
import math


class PredictiveMaintenanceEngine:
    """
    Calculates Remaining Useful Life (RUL) and ISO 10816 Vibration Severity.
    """

    @classmethod
    def evaluate_vibration_iso10816(cls, vibration_velocity_rms_mm_s: float, machine_class: str = "CLASS_II_MEDIUM_MACHINES") -> Dict[str, Any]:
        """
        ISO 10816-1 Vibration Severity Standard:
        Class II: Medium machines (15 kW - 75 kW).
        """
        v = vibration_velocity_rms_mm_s

        if v <= 1.12:
            zone = "ZONE_A_GOOD"
            action = "Normal operation; newly commissioned standard"
        elif v <= 2.80:
            zone = "ZONE_B_ACCEPTABLE"
            action = "Satisfactory for long-term unrestricted operation"
        elif v <= 7.10:
            zone = "ZONE_C_RESTRICTED"
            action = "Unsatisfactory for continuous operation; schedule maintenance"
        else:
            zone = "ZONE_D_UNACCEPTABLE_DANGER"
            action = "Vibration severity dangerous; immediate shutdown required"

        return {
            "vibration_rms_mm_s": v,
            "iso_zone": zone,
            "recommended_action": action,
            "alarm_triggered": v > 2.80,
            "trip_shutdown_mandated": v > 7.10,
        }

    @classmethod
    def calculate_remaining_useful_life_exponential(
        cls,
        initial_health_index: float,
        current_health_index: float,
        operating_hours_elapsed: float,
        critical_failure_threshold: float = 20.0,
    ) -> Dict[str, Any]:
        """
        Exponential Degradation Model: h(t) = h_0 * exp(-beta * t)
        beta = ln(h_0 / h_t) / t
        RUL = (ln(h_t / h_crit)) / beta
        """
        if current_health_index <= critical_failure_threshold:
            return {"rul_operating_hours": 0.0, "status": "FAILURE_THRESHOLD_REACHED"}

        h0 = max(initial_health_index, current_health_index + 0.1)
        ht = current_health_index
        
        beta = math.log(h0 / ht) / max(1.0, operating_hours_elapsed)
        if beta <= 0:
            beta = 1e-6

        rul_hours = math.log(ht / critical_failure_threshold) / beta

        return {
            "degradation_rate_beta": round(beta, 6),
            "estimated_rul_hours": round(rul_hours, 1),
            "estimated_rul_days_continuous": round(rul_hours / 24.0, 1),
            "health_loss_percentage": round((1.0 - ht / h0) * 100.0, 1),
        }
