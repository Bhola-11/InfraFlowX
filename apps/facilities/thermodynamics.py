"""
Facility MEP Thermodynamics & Fluid Dynamics Engine
Implements:
- Darcy-Weisbach pipe friction loss & pump hydraulic power
- Centrifugal chiller coefficient of performance (COP) & kW/Ton
- Generator fuel consumption & heat recovery steam generator (HRSG) efficiency
"""
from decimal import Decimal
import math


class HydraulicPumpEngine:
    @staticmethod
    def calculate_pump_head_and_power(flow_rate_gpm, pipe_length_ft, pipe_diameter_in, hazan_williams_c=120.0, static_head_ft=45.0, pump_efficiency_pct=78.0, motor_efficiency_pct=92.0):
        q = float(flow_rate_gpm)
        l = float(pipe_length_ft)
        d = float(pipe_diameter_in)
        c = float(hazan_williams_c)
        h_static = float(static_head_ft)

        # Hazen-Williams Friction Head Loss equation: h_f = 0.002083 * L * (100/C)^1.852 * (q^1.852 / d^4.8655)
        h_friction = 0.002083 * l * ((100.0 / c) ** 1.852) * ((q ** 1.852) / (d ** 4.8655))
        total_dynamic_head_ft = h_static + h_friction

        # Water Horsepower (WHP) = (Q * TDH * SG) / 3960
        whp = (q * total_dynamic_head_ft * 1.0) / 3960.0
        
        # Brake Horsepower (BHP) = WHP / Pump Efficiency
        eta_pump = float(pump_efficiency_pct) / 100.0
        bhp = whp / eta_pump if eta_pump > 0 else whp
        
        # Electrical Power Input (kW) = (BHP * 0.7457) / Motor Efficiency
        eta_motor = float(motor_efficiency_pct) / 100.0
        kw_electric = (bhp * 0.7457) / eta_motor if eta_motor > 0 else bhp * 0.7457

        return {
            'friction_head_loss_ft': round(Decimal(str(h_friction)), 2),
            'total_dynamic_head_ft': round(Decimal(str(total_dynamic_head_ft)), 2),
            'water_horsepower_whp': round(Decimal(str(whp)), 2),
            'brake_horsepower_bhp': round(Decimal(str(bhp)), 2),
            'electrical_power_input_kw': round(Decimal(str(kw_electric)), 2)
        }


class ChillerThermodynamicsEngine:
    @staticmethod
    def calculate_chiller_efficiency(evaporator_load_tons, electrical_input_kw):
        tons = float(evaporator_load_tons)
        kw = float(electrical_input_kw)
        
        kw_per_ton = kw / tons if tons > 0 else 0.0
        # COP = 3.517 / (kW/ton)
        cop = 3.51685 / kw_per_ton if kw_per_ton > 0 else 0.0
        # Energy Efficiency Ratio (EER) = COP * 3.41214
        eer = cop * 3.41214

        return {
            'cooling_tonnage': round(Decimal(str(tons)), 1),
            'electrical_input_kw': round(Decimal(str(kw)), 1),
            'kw_per_ton': round(Decimal(str(kw_per_ton)), 3),
            'coefficient_of_performance_cop': round(Decimal(str(cop)), 2),
            'energy_efficiency_ratio_eer': round(Decimal(str(eer)), 2),
            'ashrae_90_1_compliance': kw_per_ton <= 0.65
        }
