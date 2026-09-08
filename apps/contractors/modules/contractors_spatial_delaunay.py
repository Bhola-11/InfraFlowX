"""
InfraFlowX Enterprise Platform - Contractors Spatial Delaunay & Mesh Geometry Engine
Generates triangular irregular networks (TIN) and topography mesh connectivity.
"""

from typing import Dict, List, Any, Tuple
import math


class ContractorsDelaunayMeshEngine:
    """
    Triangular spatial mesh and terrain surface generator for contractors.
    """

    @classmethod
    def calculate_triangle_circumcircle(cls, p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float]) -> Dict[str, Any]:
        """
        Computes center and radius of circumcircle for triangle (p1, p2, p3).
        """
        ax, ay = p1
        bx, by = p2
        cx, cy = p3

        d = 2.0 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        if abs(d) < 1e-9:
            return {"center": (0.0, 0.0), "radius": float("inf"), "is_degenerate": True}

        ux = ((ax**2 + ay**2)*(by - cy) + (bx**2 + by**2)*(cy - ay) + (cx**2 + cy**2)*(ay - by)) / d
        uy = ((ax**2 + ay**2)*(cx - bx) + (bx**2 + by**2)*(ax - cx) + (cx**2 + cy**2)*(bx - ax)) / d
        radius = math.sqrt((ax - ux)**2 + (ay - uy)**2)

        return {
            "app_module": "contractors",
            "center_x": round(ux, 6),
            "center_y": round(uy, 6),
            "circumradius": round(radius, 6),
            "is_degenerate": False,
        }
