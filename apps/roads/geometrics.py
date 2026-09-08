"""
InfraFlowX - Highway Geometric Design and Alignment Engine
Compliant with AASHTO Green Book: A Policy on Geometric Design of Highways and Streets.
"""

from typing import Dict, Any, Tuple
import math


class HighwayGeometricEngine:
    """
    Geometric Alignment Engine calculating curve radii, superelevation, stopping sight distances,
    and vertical curve crest/sag elevations.
    """

    GRAVITY = 9.81  # m/s^2

    @classmethod
    def minimum_horizontal_radius(cls, design_speed_kmh: float, max_superelevation_rate: float = 0.06, side_friction_factor: float = 0.14) -> float:
        """
        R_min = V^2 / (127 * (e_max + f_max))
        """
        v = design_speed_kmh
        r_min = (v ** 2) / (127.0 * (max_superelevation_rate + side_friction_factor))
        return round(r_min, 2)

    @classmethod
    def stopping_sight_distance(cls, design_speed_kmh: float, grade_pct: float = 0.0, reaction_time_sec: float = 2.5) -> float:
        """
        SSD = 0.278 * V * t + V^2 / (254 * (f_friction +/- G/100))
        """
        v = design_speed_kmh
        g_dec = grade_pct / 100.0
        f_friction = 0.35  # AASHTO baseline coefficient
        brake_dist = (v ** 2) / (254.0 * (f_friction + g_dec))
        perception_dist = 0.278 * v * reaction_time_sec
        return round(perception_dist + brake_dist, 2)

    @classmethod
    def crest_vertical_curve_length(cls, ssd_m: float, grade_in_pct: float, grade_out_pct: float, driver_eye_height_m: float = 1.08, object_height_m: float = 0.60) -> Dict[str, Any]:
        """
        Calculates minimum vertical curve length (L) for crest curves.
        A = |g2 - g1|
        """
        a = abs(grade_out_pct - grade_in_pct)
        if a < 0.01:
            return {"length_m": 0.0, "k_value": 0.0, "sight_condition": "Adequate without curve"}
        
        # S <= L case: L = A * S^2 / (100 * (sqrt(2*h1) + sqrt(2*h2))^2)
        denom = 100.0 * (math.sqrt(2.0 * driver_eye_height_m) + math.sqrt(2.0 * object_height_m)) ** 2
        l_crest = (a * (ssd_m ** 2)) / denom
        k_val = l_crest / a if a > 0 else 0.0

        return {
            "algebraic_grade_difference_pct": round(a, 2),
            "required_curve_length_m": round(max(l_crest, 60.0), 2),
            "design_k_value": round(k_val, 2),
            "stopping_sight_distance_m": ssd_m,
        }

    @classmethod
    def sag_vertical_curve_length(cls, ssd_m: float, grade_in_pct: float, grade_out_pct: float, headlight_height_m: float = 0.60, beam_angle_deg: float = 1.0) -> Dict[str, Any]:
        """
        Calculates sag vertical curve length based on headlight beam distance.
        """
        a = abs(grade_out_pct - grade_in_pct)
        if a < 0.01:
            return {"length_m": 0.0, "k_value": 0.0}
        
        beam_rad = math.radians(beam_angle_deg)
        denom = 200.0 * (headlight_height_m + ssd_m * math.tan(beam_rad))
        l_sag = (a * (ssd_m ** 2)) / denom
        k_val = l_sag / a if a > 0 else 0.0

        return {
            "algebraic_grade_difference_pct": round(a, 2),
            "required_curve_length_m": round(max(l_sag, 60.0), 2),
            "design_k_value": round(k_val, 2),
        }
