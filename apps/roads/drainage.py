"""
InfraFlowX - Highway Hydraulic and Stormwater Drainage Engine
Calculates peak runoff using the Rational Method and open channel flow using Manning's Equation.
"""

from typing import Dict, Any
import math


class HighwayDrainageEngine:
    """
    Stormwater hydraulic modeling for culverts, roadside ditches, and curb inlets.
    """

    @classmethod
    def rational_method_peak_flow(cls, runoff_coefficient_c: float, rainfall_intensity_mm_hr: float, catchment_area_hectares: float) -> float:
        """
        Peak discharge Q = 0.00278 * C * I * A (m^3/s)
        """
        q = 0.00278 * runoff_coefficient_c * rainfall_intensity_mm_hr * catchment_area_hectares
        return round(q, 4)

    @classmethod
    def mannings_trapezoidal_channel_capacity(cls, bottom_width_m: float, side_slope_z: float, depth_m: float, longitudinal_slope: float, mannings_n: float = 0.035) -> Dict[str, Any]:
        """
        Manning's Equation: Q = (1/n) * A * R^(2/3) * S^(1/2)
        Trapezoidal channel with side slopes 1:z (vertical:horizontal)
        """
        b = bottom_width_m
        y = depth_m
        z = side_slope_z
        s = max(0.0001, longitudinal_slope)
        
        cross_sectional_area = (b + z * y) * y
        wetted_perimeter = b + 2.0 * y * math.sqrt(1.0 + z ** 2)
        hydraulic_radius = cross_sectional_area / wetted_perimeter if wetted_perimeter > 0 else 0.0
        
        velocity = (1.0 / mannings_n) * (hydraulic_radius ** (2.0 / 3.0)) * math.sqrt(s)
        discharge = cross_sectional_area * velocity
        froude_number = velocity / math.sqrt(9.81 * (cross_sectional_area / (b + 2.0 * z * y)))

        return {
            "flow_capacity_m3_per_sec": round(discharge, 4),
            "flow_velocity_m_per_sec": round(velocity, 3),
            "cross_sectional_area_m2": round(cross_sectional_area, 3),
            "hydraulic_radius_m": round(hydraulic_radius, 3),
            "froude_number": round(froude_number, 3),
            "flow_regime": "Supercritical" if froude_number > 1.0 else ("Critical" if abs(froude_number - 1.0) < 0.05 else "Subcritical"),
        }

    @classmethod
    def curb_inlet_efficiency(cls, gutter_flow_m3_s: float, longitudinal_slope: float, cross_slope: float, inlet_length_m: float) -> Dict[str, Any]:
        """
        FHWA HEC-22 curb inlet interception and bypass calculator.
        """
        # Equivalent length for 100% interception L_T = 0.6 * Q^0.42 * S^0.3 * (1 / (n * S_x))^0.6
        s_0 = max(0.001, longitudinal_slope)
        s_x = max(0.01, cross_slope)
        n = 0.016  # concrete gutter roughness
        
        l_total = 0.6 * (gutter_flow_m3_s ** 0.42) * (s_0 ** 0.3) * (1.0 / (n * s_x)) ** 0.6
        if inlet_length_m >= l_total:
            efficiency = 1.0
            intercepted = gutter_flow_m3_s
            bypass = 0.0
        else:
            efficiency = 1.0 - (1.0 - (inlet_length_m / l_total)) ** 1.8
            intercepted = gutter_flow_m3_s * efficiency
            bypass = gutter_flow_m3_s - intercepted

        return {
            "interception_efficiency_pct": round(efficiency * 100.0, 2),
            "intercepted_flow_m3_s": round(intercepted, 4),
            "bypass_flow_m3_s": round(bypass, 4),
            "full_interception_required_length_m": round(l_total, 2),
        }
