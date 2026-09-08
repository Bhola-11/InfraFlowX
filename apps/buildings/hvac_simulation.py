"""
InfraFlowX - Building HVAC & Psychrometric Thermodynamics Simulation Engine
Calculates enthalpy, sensible/latent heat transfer, and VAV airflow sizing.
"""

from typing import Dict, Any
import math


class PsychrometricHVACEngine:
    """
    Thermodynamic moist air calculations and cooling coil sizing.
    """

    SPECIFIC_HEAT_AIR = 1.006  # kJ/kg-C
    LATENT_HEAT_VAPORIZATION = 2501.0  # kJ/kg

    @classmethod
    def saturation_vapor_pressure_kpa(cls, dry_bulb_temp_c: float) -> float:
        """Tetens formula for saturation vapor pressure."""
        t = dry_bulb_temp_c
        return 0.61078 * math.exp((17.27 * t) / (t + 237.3))

    @classmethod
    def calculate_humidity_ratio(cls, dry_bulb_c: float, relative_humidity_pct: float, atmospheric_pressure_kpa: float = 101.325) -> float:
        """Humidity ratio W in kg water / kg dry air."""
        rh = min(100.0, max(0.0, relative_humidity_pct)) / 100.0
        p_ws = cls.saturation_vapor_pressure_kpa(dry_bulb_c)
        p_w = rh * p_ws
        w = 0.62198 * p_w / (atmospheric_pressure_kpa - p_w)
        return max(0.0, w)

    @classmethod
    def calculate_specific_enthalpy(cls, dry_bulb_c: float, humidity_ratio: float) -> float:
        """Enthalpy h in kJ / kg dry air."""
        t = dry_bulb_c
        w = humidity_ratio
        h = 1.006 * t + w * (2501.0 + 1.86 * t)
        return round(h, 2)

    @classmethod
    def size_cooling_coil(cls, airflow_cfm: float, entering_db_c: float, entering_rh_pct: float, leaving_db_c: float = 12.8, leaving_rh_pct: float = 95.0) -> Dict[str, Any]:
        """
        Computes Total, Sensible, and Latent cooling capacity in Tons of Refrigeration.
        """
        # Convert CFM to kg/s (standard air density 1.2 kg/m^3)
        airflow_m3_s = airflow_cfm * 0.000471947
        mass_flow_kg_s = airflow_m3_s * 1.204
        
        w_in = cls.calculate_humidity_ratio(entering_db_c, entering_rh_pct)
        w_out = cls.calculate_humidity_ratio(leaving_db_c, leaving_rh_pct)
        
        h_in = cls.calculate_specific_enthalpy(entering_db_c, w_in)
        h_out = cls.calculate_specific_enthalpy(leaving_db_c, w_out)
        
        q_total_kw = mass_flow_kg_s * (h_in - h_out)
        q_sensible_kw = mass_flow_kg_s * cls.SPECIFIC_HEAT_AIR * (entering_db_c - leaving_db_c)
        q_latent_kw = max(0.0, q_total_kw - q_sensible_kw)
        
        tons_refrigeration = q_total_kw / 3.51685
        sensible_heat_ratio = q_sensible_kw / q_total_kw if q_total_kw > 0 else 1.0

        return {
            "total_cooling_capacity_kw": round(q_total_kw, 2),
            "sensible_cooling_kw": round(q_sensible_kw, 2),
            "latent_cooling_kw": round(q_latent_kw, 2),
            "cooling_capacity_tons": round(tons_refrigeration, 2),
            "sensible_heat_ratio_shr": round(sensible_heat_ratio, 3),
            "moisture_removed_liters_per_hr": round(mass_flow_kg_s * (w_in - w_out) * 3600.0, 2),
        }
