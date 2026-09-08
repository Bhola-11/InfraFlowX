"""
InfraFlowX - Building Energy Audit & Carbon Accounting Engine
Compliant with ASHRAE Standard 100 & GHG Protocol Scope 1 & 2 Emissions.
"""

from typing import Dict, List, Any
import math


class BuildingEnergyAuditEngine:
    """
    Computes Weather Normalized Energy Use Intensity (EUI), Heating/Cooling Degree Days (HDD/CDD),
    and Scope 1/2 Greenhouse Gas Emissions.
    """

    # EPA eGRID carbon emissions factors (kg CO2e / kWh) by region
    EMISSION_FACTORS = {
        "ELECTRICITY_GRID_AVG": 0.385,  # kg CO2e / kWh
        "NATURAL_GAS_THERM": 5.306,     # kg CO2e / therm
        "FUEL_OIL_GALLON": 10.21,      # kg CO2e / gallon
        "STEAM_KLB": 54.12,            # kg CO2e / 1000 lbs
    }

    @classmethod
    def calculate_degree_days(cls, daily_temperatures: List[Dict[str, float]], base_temp_c: float = 18.33) -> Dict[str, float]:
        """
        Calculates Heating Degree Days (HDD) and Cooling Degree Days (CDD).
        """
        hdd_total = 0.0
        cdd_total = 0.0

        for day in daily_temperatures:
            t_max = day.get("max_temp_c", 20.0)
            t_min = day.get("min_temp_c", 10.0)
            t_mean = (t_max + t_min) / 2.0
            
            if t_mean < base_temp_c:
                hdd_total += (base_temp_c - t_mean)
            elif t_mean > base_temp_c:
                cdd_total += (t_mean - base_temp_c)

        return {
            "heating_degree_days_cdd": round(hdd_total, 1),
            "cooling_degree_days_cdd": round(cdd_total, 1),
            "total_degree_days": round(hdd_total + cdd_total, 1),
        }

    @classmethod
    def calculate_ghg_emissions(cls, electricity_kwh: float, natural_gas_therms: float, fuel_oil_gallons: float = 0.0) -> Dict[str, Any]:
        """
        Computes metric tons of CO2 equivalent emissions.
        """
        scope2_elec = (electricity_kwh * cls.EMISSION_FACTORS["ELECTRICITY_GRID_AVG"]) / 1000.0
        scope1_gas = (natural_gas_therms * cls.EMISSION_FACTORS["NATURAL_GAS_THERM"]) / 1000.0
        scope1_oil = (fuel_oil_gallons * cls.EMISSION_FACTORS["FUEL_OIL_GALLON"]) / 1000.0
        
        total_scope1 = scope1_gas + scope1_oil
        total_ghg = total_scope1 + scope2_elec

        return {
            "scope_1_direct_mt_co2e": round(total_scope1, 2),
            "scope_2_indirect_mt_co2e": round(scope2_elec, 2),
            "total_ghg_mt_co2e": round(total_ghg, 2),
            "breakdown_percentage": {
                "electricity": round((scope2_elec / total_ghg * 100.0) if total_ghg > 0 else 0.0, 1),
                "natural_gas": round((scope1_gas / total_ghg * 100.0) if total_ghg > 0 else 0.0, 1),
                "fuel_oil": round((scope1_oil / total_ghg * 100.0) if total_ghg > 0 else 0.0, 1),
            },
        }

    @classmethod
    def energy_star_target_comparison(cls, actual_eui_kbtu_sqft: float, property_type: str = "OFFICE") -> Dict[str, Any]:
        # Median national EUIs by property type (CBECS)
        median_euis = {
            "OFFICE": 53.0,
            "HOSPITAL": 214.0,
            "SCHOOL": 48.5,
            "WAREHOUSE": 28.0,
            "MUNICIPAL_HQ": 62.0,
            "COMMUNITY_CENTER": 58.0,
        }
        median = median_euis.get(property_type.upper(), 55.0)
        pct_diff = ((actual_eui_kbtu_sqft - median) / median) * 100.0
        
        # Approximate 1-100 score
        if actual_eui_kbtu_sqft <= median * 0.5:
            score = 95
        elif actual_eui_kbtu_sqft <= median * 0.75:
            score = 80
        elif actual_eui_kbtu_sqft <= median:
            score = 55
        elif actual_eui_kbtu_sqft <= median * 1.3:
            score = 35
        else:
            score = 15

        return {
            "property_type": property_type.upper(),
            "actual_eui": actual_eui_kbtu_sqft,
            "national_median_eui": median,
            "variance_from_median_pct": round(pct_diff, 1),
            "estimated_energy_star_score": score,
            "certification_eligible": score >= 75,
        }
