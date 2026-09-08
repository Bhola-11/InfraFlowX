"""
InfraFlowX - HDM-4 Highway Deterioration and Pavement Life Engine
Simulates international roughness index (IRI), structural cracking, rutting progression, and ravelling.
"""

from typing import Dict, List, Any
import math


class HDM4PavementDeteriorationEngine:
    """
    World Bank HDM-4 (Highway Development and Management) Pavement Deterioration Mathematical Models.
    Computes time-series deterioration over multi-year lifecycle horizons.
    """

    def __init__(self, structural_number: float, initial_iri: float = 1.8, climate_factor: float = 1.0):
        self.sn = structural_number
        self.initial_iri = initial_iri
        self.m = climate_factor  # Environmental degradation parameter (0.015 - 0.040)

    def structural_cracking_initiation_time(self, annual_esal: float) -> float:
        """
        Calculates time to crack initiation in years:
        TY_CRACK = K_cia * 4.21 * exp(-0.14 * SN) * (ESAL / 10^6)^(-0.35)
        """
        million_esal = max(0.01, annual_esal / 1_000_000.0)
        ty = 4.21 * math.exp(-0.14 * self.sn) * (million_esal ** -0.35)
        return max(1.0, ty)

    def calculate_cracking_progression(self, age_years: float, annual_esal: float) -> float:
        """Returns total cracked area percentage (0 - 100%)."""
        t_init = self.structural_cracking_initiation_time(annual_esal)
        if age_years <= t_init:
            return 0.0
        delta_t = age_years - t_init
        cracking_pct = 100.0 / (1.0 + math.exp(4.0 - 0.65 * delta_t))
        return min(100.0, cracking_pct)

    def calculate_rut_depth_progression_mm(self, age_years: float, annual_esal: float) -> float:
        """
        Rut depth RD = K_rd * 0.166 * (ESAL_total / 10^6)^0.43 * (SN)^(-0.63)
        """
        total_esal_million = (annual_esal * age_years) / 1_000_000.0
        if total_esal_million <= 0:
            return 0.0
        rut_mm = 0.166 * (total_esal_million ** 0.43) * (self.sn ** -0.63) * 25.4
        return round(rut_mm, 2)

    def calculate_iri_progression(self, age_years: float, annual_esal: float) -> float:
        """
        HDM-4 Roughness Progression:
        IRI(t) = IRI_0 * exp(m * t) + Delta_IRI_structural + Delta_IRI_cracking + Delta_IRI_rutting
        """
        env_roughness = self.initial_iri * math.exp(0.025 * self.m * age_years)
        cracking_pct = self.calculate_cracking_progression(age_years, annual_esal)
        rut_mm = self.calculate_rut_depth_progression_mm(age_years, annual_esal)
        
        delta_structural = 0.0065 * ((annual_esal * age_years) / (1_000_000.0 * (1.0 + self.sn)**5))
        delta_cracking = 0.005 * cracking_pct
        delta_rutting = 0.025 * rut_mm
        
        total_iri = env_roughness + delta_structural + delta_cracking + delta_rutting
        return round(total_iri, 3)

    def run_lifecycle_simulation(self, horizon_years: int, annual_esal: float, esal_growth_rate: float = 0.02) -> List[Dict[str, Any]]:
        trajectory = []
        cum_esal = 0.0
        curr_annual_esal = annual_esal

        for yr in range(1, horizon_years + 1):
            cum_esal += curr_annual_esal
            iri = self.calculate_iri_progression(yr, curr_annual_esal)
            crack = self.calculate_cracking_progression(yr, curr_annual_esal)
            rut = self.calculate_rut_depth_progression_mm(yr, curr_annual_esal)
            
            # Maintenance Trigger Assessment
            if iri < 2.5 and crack < 10.0 and rut < 8.0:
                condition = "GOOD"
                recommended_action = "Routine Maintenance / Crack Sealing"
            elif iri < 3.8 and crack < 25.0 and rut < 15.0:
                condition = "FAIR"
                recommended_action = "Preventive Micro-surfacing / Thin Overlay"
            elif iri < 5.0 and crack < 50.0:
                condition = "POOR"
                recommended_action = "Mill and Structural Overlay (50-75mm)"
            else:
                condition = "FAILED"
                recommended_action = "Full Depth Pavement Reconstruction"

            trajectory.append({
                "year": yr,
                "annual_esal": round(curr_annual_esal, 0),
                "cumulative_esal": round(cum_esal, 0),
                "iri_m_per_km": iri,
                "cracked_area_pct": round(crack, 2),
                "rut_depth_mm": rut,
                "condition_grade": condition,
                "recommended_action": recommended_action,
            })
            curr_annual_esal *= (1.0 + esal_growth_rate)

        return trajectory
