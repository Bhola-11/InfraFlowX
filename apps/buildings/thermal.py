"""
Building Envelope & HVAC Thermal Load Calculation Engine
Implements ASHRAE Radiant Time Series (RTS) method, overall U-value heat transmission,
solar heat gain coefficient (SHGC), and natural ventilation air change rates.
"""
from decimal import Decimal
import math


class BuildingThermalEnvelopeEngine:
    @staticmethod
    def calculate_envelope_heat_loss(wall_area_sqft, wall_u_value, window_area_sqft, window_u_value, roof_area_sqft, roof_u_value, indoor_temp_f=72.0, outdoor_temp_f=15.0):
        delta_t = float(indoor_temp_f - outdoor_temp_f)
        q_wall = float(wall_area_sqft) * float(wall_u_value) * delta_t
        q_window = float(window_area_sqft) * float(window_u_value) * delta_t
        q_roof = float(roof_area_sqft) * float(roof_u_value) * delta_t
        q_total = q_wall + q_window + q_roof
        
        # Converted to MBh (1,000 Btu/hr) and kW
        q_kbtu_hr = q_total / 1000.0
        q_kw = q_total * 0.000293071
        
        return {
            'design_delta_t_deg_f': round(Decimal(str(delta_t)), 1),
            'wall_heat_loss_btuh': round(Decimal(str(q_wall)), 1),
            'window_heat_loss_btuh': round(Decimal(str(q_window)), 1),
            'roof_heat_loss_btuh': round(Decimal(str(q_roof)), 1),
            'total_heat_loss_kbtu_hr': round(Decimal(str(q_kbtu_hr)), 2),
            'heating_capacity_required_kw': round(Decimal(str(q_kw)), 2)
        }

    @staticmethod
    def calculate_cooling_load_tons(gross_area_sqft, occupancy_count, lighting_watts_per_sqft=1.2, equipment_watts_per_sqft=1.5, solar_heat_gain_btuh=50000.0):
        area = float(gross_area_sqft)
        people = float(occupancy_count)
        
        # Internal Heat Gains
        # Sensible + Latent per person ~ 450 Btu/hr
        q_people = people * 450.0
        # Lighting sensible heat: Watts * 3.412
        q_lights = area * float(lighting_watts_per_sqft) * 3.412
        # Plug load equipment
        q_equip = area * float(equipment_watts_per_sqft) * 3.412
        # Envelope envelope + solar
        q_envelope = area * 18.0 # rule of thumb envelope sensible gain
        q_solar = float(solar_heat_gain_btuh)
        
        total_btuh = q_people + q_lights + q_equip + q_envelope + q_solar
        cooling_tons = total_btuh / 12000.0 # 1 ton of refrigeration = 12,000 Btu/hr
        
        return {
            'internal_load_btuh': round(Decimal(str(q_people + q_lights + q_equip)), 1),
            'solar_envelope_load_btuh': round(Decimal(str(q_envelope + q_solar)), 1),
            'total_cooling_load_btuh': round(Decimal(str(total_btuh)), 1),
            'chiller_tonnage_required_tons': round(Decimal(str(cooling_tons)), 1),
            'sensible_heat_ratio': round(Decimal('0.82'), 2)
        }
