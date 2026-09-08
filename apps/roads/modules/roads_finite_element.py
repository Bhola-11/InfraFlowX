"""
InfraFlowX Enterprise Platform - Roads Finite Element & Structural Mechanics Engine
Computes 1D/2D structural stress profiles, elastic modulus deflections, and safety factors.
"""

from typing import Dict, List, Any
import math


class RoadsStructuralMechanicsEngine:
    """
    Beam deflection and elastic deformation calculations for roads.
    """

    @classmethod
    def calculate_simply_supported_beam(cls, span_length_m: float, point_load_kn: float, elastic_modulus_gpa: float, moment_of_inertia_m4: float) -> Dict[str, Any]:
        """
        Euler-Bernoulli beam theory:
        Max Deflection delta_max = (P * L^3) / (48 * E * I)
        Max Bending Moment M_max = (P * L) / 4
        """
        l = span_length_m
        p = point_load_kn * 1000.0  # N
        e = elastic_modulus_gpa * 1e9  # Pa
        i_inertia = moment_of_inertia_m4

        max_moment_nm = (p * l) / 4.0
        max_deflection_m = (p * (l ** 3)) / (48.0 * e * i_inertia) if (e * i_inertia) > 0 else 0.0

        # Permissible deflection limit (L / 360)
        allowable_deflection_m = l / 360.0

        return {
            "app_module": "roads",
            "span_length_m": span_length_m,
            "max_bending_moment_kNm": round(max_moment_nm / 1000.0, 2),
            "max_deflection_mm": round(max_deflection_m * 1000.0, 3),
            "allowable_deflection_limit_mm": round(allowable_deflection_m * 1000.0, 3),
            "structural_adequacy_passed": max_deflection_m <= allowable_deflection_m,
        }
