"""
InfraFlowX - Municipal Water Distribution Network & Hazen-Williams Head Loss Engine
Simulates hydraulic pipe network pressure drops, friction losses, and pump booster curves.
"""

from typing import Dict, List, Any
import math


class WaterDistributionHydraulicsEngine:
    """
    Hazen-Williams formula for head loss in pressurized water pipes:
    h_f = 10.67 * L * Q^1.852 / (C^1.852 * D^4.87)  (SI Units)
    """

    # Hazen-Williams C Roughness Coefficients
    C_FACTORS = {
        "DUCTILE_IRON_NEW": 140,
        "DUCTILE_IRON_AGED": 100,
        "PVC": 150,
        "HDPE": 150,
        "CONCRETE": 120,
        "CAST_IRON_UNLINED": 80,
    }

    @classmethod
    def calculate_pipe_head_loss(cls, length_m: float, flow_m3_s: float, internal_diameter_m: float, pipe_material: str = "DUCTILE_IRON_AGED") -> Dict[str, Any]:
        c = cls.C_FACTORS.get(pipe_material.upper(), 120)
        l = length_m
        q = max(0.0001, flow_m3_s)
        d = max(0.01, internal_diameter_m)
        
        # Head loss in meters of water
        h_f = (10.67 * l * (q ** 1.852)) / ((c ** 1.852) * (d ** 4.87))
        
        # Flow velocity V = Q / A
        area = math.pi * ((d / 2.0) ** 2)
        velocity = q / area
        
        # Pressure loss in kPa (1 m H2O = 9.80665 kPa)
        pressure_loss_kpa = h_f * 9.80665
        
        return {
            "head_loss_meters": round(h_f, 3),
            "pressure_drop_kpa": round(pressure_loss_kpa, 2),
            "flow_velocity_mps": round(velocity, 2),
            "velocity_acceptable": (0.6 <= velocity <= 2.5),
            "roughness_c_factor": c,
        }

    @classmethod
    def pump_system_operating_point(cls, static_head_m: float, pipe_loss_coeff_k: float, pump_shutoff_head_m: float, pump_curve_coeff_a: float) -> Dict[str, Any]:
        """
        Finds intersection of System Curve (H_sys = H_stat + K*Q^2) and Pump Curve (H_pump = H_0 - A*Q^2).
        Q_operating = sqrt((H_0 - H_stat) / (K + A))
        """
        if pump_shutoff_head_m <= static_head_m:
            return {"operating_flow_m3_s": 0.0, "operating_head_m": static_head_m, "status": "Pump head below static lift"}
        
        denom = pipe_loss_coeff_k + pump_curve_coeff_a
        q_op = math.sqrt((pump_shutoff_head_m - static_head_m) / denom)
        h_op = pump_shutoff_head_m - pump_curve_coeff_a * (q_op ** 2)
        
        # Hydraulic Power P_hyd = rho * g * Q * H / 1000 (kW)
        p_hydraulic_kw = (1000.0 * 9.81 * q_op * h_op) / 1000.0

        return {
            "operating_flow_m3_s": round(q_op, 4),
            "operating_flow_liters_per_sec": round(q_op * 1000.0, 2),
            "operating_head_m": round(h_op, 2),
            "hydraulic_power_kw": round(p_hydraulic_kw, 2),
            "status": "Stable operating point established",
        }
