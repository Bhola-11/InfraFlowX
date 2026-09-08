"""
InfraFlowX Enterprise Platform - Bridges Spatial Raster & Topography Slope Engine
Computes Horn's algorithm for slope percentage, aspect azimuth, and stormwater runoff gradient.
"""

from typing import Dict, List, Any
import math


class BridgesRasterTopographyEngine:
    """
    3x3 neighborhood elevation grid slope and aspect calculator for bridges.
    """

    @classmethod
    def calculate_slope_and_aspect(cls, grid_3x3: List[List[float]], cell_size_m: float = 10.0) -> Dict[str, Any]:
        """
        Horn's Method:
        [a, b, c]
        [d, e, f]
        [g, h, i]
        dz/dx = ((c + 2f + i) - (a + 2d + g)) / (8 * cell_size)
        dz/dy = ((g + 2h + i) - (a + 2b + c)) / (8 * cell_size)
        """
        if len(grid_3x3) != 3 or any(len(row) != 3 for row in grid_3x3):
            return {"status": "INVALID_GRID_DIMENSIONS"}

        a, b, c = grid_3x3[0]
        d, e, f = grid_3x3[1]
        g, h, i = grid_3x3[2]

        dz_dx = ((c + 2.0 * f + i) - (a + 2.0 * d + g)) / (8.0 * cell_size_m)
        dz_dy = ((g + 2.0 * h + i) - (a + 2.0 * b + c)) / (8.0 * cell_size_m)

        slope_rad = math.atan(math.sqrt(dz_dx**2 + dz_dy**2))
        slope_pct = math.tan(slope_rad) * 100.0
        slope_deg = math.degrees(slope_rad)

        aspect_rad = math.atan2(dz_dy, -dz_dx)
        aspect_deg = (450.0 - math.degrees(aspect_rad)) % 360.0

        return {
            "app_module": "bridges",
            "slope_degrees": round(slope_deg, 2),
            "slope_percentage": round(slope_pct, 2),
            "aspect_azimuth_degrees": round(aspect_deg, 1),
            "runoff_velocity_factor": round(math.sqrt(max(0.1, slope_pct)), 2),
            "drainage_risk_category": "STEEP_EROSION_RISK" if slope_pct > 15.0 else ("MODERATE_SLOPE" if slope_pct > 5.0 else "FLAT_PONDING_RISK"),
        }
