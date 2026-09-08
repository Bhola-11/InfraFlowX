"""
InfraFlowX Enterprise Platform - Budgets Spatial Corridor Buffer & Zone Dilation
Computes right-of-way buffer corridors and geometric offsets for spatial assets.
"""

from typing import Dict, List, Any, Tuple
import math


class BudgetsSpatialBufferEngine:
    """
    Calculates right-of-way buffer zone offsets around spatial centerlines for budgets.
    """

    @classmethod
    def generate_corridor_buffer(cls, centerline_coords: List[Tuple[float, float]], buffer_width_meters: float = 30.0) -> Dict[str, Any]:
        """
        Generates left and right parallel offset polylines.
        """
        if len(centerline_coords) < 2:
            return {"status": "INSUFFICIENT_COORDINATES", "left_offset": [], "right_offset": []}

        offset_deg = buffer_width_meters / 111000.0  # Approx 111km per degree
        left_line = []
        right_line = []

        for i in range(len(centerline_coords) - 1):
            p1 = centerline_coords[i]
            p2 = centerline_coords[i + 1]

            dx = p2[1] - p1[1]
            dy = p2[0] - p1[0]
            length = math.sqrt(dx**2 + dy**2)
            if length < 1e-9:
                continue

            # Normal vector (-dy, dx)
            nx = -dy / length * offset_deg
            ny = dx / length * offset_deg

            left_line.append((round(p1[0] + ny, 6), round(p1[1] + nx, 6)))
            right_line.append((round(p1[0] - ny, 6), round(p1[1] - nx, 6)))

        return {
            "app_module": "budgets",
            "centerline_points_count": len(centerline_coords),
            "buffer_width_meters": buffer_width_meters,
            "left_offset_boundary": left_line,
            "right_offset_boundary": right_line,
            "corridor_area_sqm": round(buffer_width_meters * 2.0 * len(centerline_coords) * 100.0, 2),
        }
