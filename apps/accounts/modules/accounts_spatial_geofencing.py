"""
InfraFlowX Enterprise Platform - Accounts Spatial Geofencing & Corridor Engine
Manages polygonal geofence boundaries, corridor buffer zones, and coordinate containment.
"""

from typing import Dict, List, Any, Tuple


class AccountsGeofenceEngine:
    """
    Geofencing and spatial corridor proximity detection for accounts.
    """

    @classmethod
    def is_coordinate_within_geofence(cls, latitude: float, longitude: float, polygon_vertices: List[Tuple[float, float]]) -> bool:
        """
        Ray-casting algorithm for point-in-polygon containment test.
        """
        n = len(polygon_vertices)
        if n < 3:
            return False

        inside = False
        p1x, p1y = polygon_vertices[0]
        for i in range(n + 1):
            p2x, p2y = polygon_vertices[i % n]
            if longitude > min(p1y, p2y):
                if longitude <= max(p1y, p2y):
                    if latitude <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (longitude - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or latitude <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside
