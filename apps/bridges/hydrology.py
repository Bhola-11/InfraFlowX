"""
InfraFlowX - Bridge Hydraulic & Hydrodynamic Scour Engine
Compliant with FHWA HEC-18 (Evaluating Scour at Bridges) & USGS Regression Discharge.
"""

from typing import Dict, Any
import math


class BridgeHydrologyEngine:
    """
    Calculates bridge waterway constriction backwater profiles and pier/abutment scour depths.
    """

    @classmethod
    def calculate_pier_scour_hec18(cls, flow_velocity_mps: float, approach_depth_m: float, pier_width_m: float, pier_nose_shape: str = "ROUND", angle_of_attack_deg: float = 0.0, bed_condition: str = "CLEAR_WATER") -> Dict[str, Any]:
        """
        FHWA HEC-18 Pier Scour Equation:
        y_s / y_1 = 2.0 * K_1 * K_2 * K_3 * (a / y_1)^0.65 * Fr_1^0.43
        """
        y1 = max(0.1, approach_depth_m)
        a = pier_width_m
        v = flow_velocity_mps
        g = 9.81
        fr1 = v / math.sqrt(g * y1)

        # K1: Pier nose shape factor
        k1_map = {"SQUARE": 1.1, "ROUND": 1.0, "CIRCULAR": 1.0, "SHARP": 0.9}
        k1 = k1_map.get(pier_nose_shape.upper(), 1.0)

        # K2: Angle of attack factor K2 = (cos(theta) + (L/a)*sin(theta))^0.65
        # assuming pier length to width ratio L/a = 4.0
        theta_rad = math.radians(angle_of_attack_deg)
        k2 = (math.cos(theta_rad) + 4.0 * math.sin(theta_rad)) ** 0.65

        # K3: Bed condition factor
        k3 = 1.1 if bed_condition.upper() == "PLANE_BED" else (1.2 if bed_condition.upper() == "DUNES" else 1.1)

        # Scour depth calculation
        scour_ratio = 2.0 * k1 * k2 * k3 * ((a / y1) ** 0.65) * (fr1 ** 0.43)
        # HEC-18 maximum scour depth limit: 2.4 * a for Fr <= 0.8, 3.0 * a for Fr > 0.8
        max_scour_limit = 2.4 * a if fr1 <= 0.8 else 3.0 * a
        scour_depth_m = min(y1 * scour_ratio, max_scour_limit)

        return {
            "scour_depth_m": round(scour_depth_m, 3),
            "froude_number": round(fr1, 3),
            "shape_factor_k1": k1,
            "alignment_factor_k2": round(k2, 3),
            "bed_factor_k3": k3,
            "max_hec18_depth_limit_m": round(max_scour_limit, 3),
            "critical_risk_flag": scour_depth_m > (0.6 * y1),
        }

    @classmethod
    def calculate_contraction_scour(cls, channel_width_main_m: float, bridge_opening_width_m: float, upstream_depth_m: float, upstream_discharge_m3s: float, bridge_discharge_m3s: float, median_grain_size_d50_mm: float = 2.0) -> Dict[str, Any]:
        """
        Laursen's Clear-Water Contraction Scour:
        y2 / y1 = (Q_bridge / Q_main)^(6/7) * (W1 / W2)^(k1)
        """
        w1 = channel_width_main_m
        w2 = bridge_opening_width_m
        y1 = upstream_depth_m
        
        # Exponent k1 for mode of bed material transport (typically 0.64 for clear water)
        k1_exp = 0.64
        y2 = y1 * ((bridge_discharge_m3s / upstream_discharge_m3s) ** (6.0 / 7.0)) * ((w1 / w2) ** k1_exp)
        contraction_scour_m = max(0.0, y2 - y1)

        return {
            "contraction_scour_depth_m": round(contraction_scour_m, 3),
            "waterway_constriction_ratio": round(w2 / w1, 3),
            "post_scour_total_depth_m": round(y2, 3),
        }
