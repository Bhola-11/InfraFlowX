"""
InfraFlowX - Non-Destructive Testing (NDT) Concrete & Structural Evaluation Engine
Compliant with ASTM C597 (Pulse Velocity) and ASTM C805 (Rebound Number).
"""

from typing import Dict, Any


class NonDestructiveTestingEngine:
    """
    NDT evaluations for structural concrete integrity, compressive strength, and void detection.
    """

    @classmethod
    def evaluate_ultrasonic_pulse_velocity(cls, path_length_mm: float, transit_time_microseconds: float) -> Dict[str, Any]:
        """
        UPV = Path Length / Transit Time (km/s or m/s)
        IS 13311 / ASTM C597 Concrete Quality Grading.
        """
        if transit_time_microseconds <= 0:
            return {"error": "Invalid transit time"}

        velocity_km_s = (path_length_mm / 1000.0) / (transit_time_microseconds / 1000.0)

        if velocity_km_s >= 4.5:
            quality = "EXCELLENT"
            desc = "Dense, defect-free high strength concrete"
        elif velocity_km_s >= 3.5:
            quality = "GOOD"
            desc = "Sound structural concrete, minimal micro-cracking"
        elif velocity_km_s >= 3.0:
            quality = "MEDIUM"
            desc = "Moderate porosity or slight internal cracking"
        else:
            quality = "POOR_DOUBTFUL"
            desc = "Honeycombing, severe cracking, or major internal voids"

        return {
            "pulse_velocity_km_per_sec": round(velocity_km_s, 2),
            "concrete_quality_grade": quality,
            "engineering_evaluation": desc,
        }

    @classmethod
    def schmidt_rebound_hammer_strength(cls, rebound_values: list, impact_angle: str = "HORIZONTAL") -> Dict[str, Any]:
        """
        ASTM C805 Rebound Number Compressive Strength Estimation (MPa).
        """
        if not rebound_values:
            return {"estimated_strength_mpa": 0.0}

        mean_r = sum(rebound_values) / len(rebound_values)

        # Angle correction factor
        angle_adjust = 0.0
        if impact_angle.upper() == "VERTICALLY_DOWNWARDS":
            angle_adjust = -2.0
        elif impact_angle.upper() == "VERTICALLY_UPWARDS":
            angle_adjust = +2.5

        adj_r = mean_r + angle_adjust

        # Empirical calibration curve: f_ck = 0.027 * R^2 + 0.38 * R
        estimated_fck_mpa = 0.027 * (adj_r ** 2) + 0.38 * adj_r

        return {
            "average_rebound_number": round(mean_r, 1),
            "adjusted_rebound_number": round(adj_r, 1),
            "estimated_compressive_strength_mpa": round(estimated_fck_mpa, 1),
            "estimated_compressive_strength_psi": round(estimated_fck_mpa * 145.038, 0),
        }
