"""
InfraFlowX - 2D Spatial Grid Index & Geofence Query Engine
Fast spatial lookups, proximity indexing, and polygon point-in-polygon tests.
"""

from typing import Dict, List, Any, Tuple


class SpatialGridIndexEngine:
    """
    Spatial partitioning grid for high-speed coordinate queries.
    """

    @classmethod
    def point_in_polygon(cls, lat: float, lon: float, polygon_coords: List[Tuple[float, float]]) -> bool:
        """
        Ray-casting algorithm for Point-in-Polygon (PIP) testing.
        polygon_coords: List of (lat, lon) vertices.
        """
        n = len(polygon_coords)
        if n < 3:
            return False

        inside = False
        p1_lat, p1_lon = polygon_coords[0]
        for i in range(n + 1):
            p2_lat, p2_lon = polygon_coords[i % n]
            if lon > min(p1_lon, p2_lon):
                if lon <= max(p1_lon, p2_lon):
                    if lat <= max(p1_lat, p2_lat):
                        if p1_lon != p2_lon:
                            lat_inters = (lon - p1_lon) * (p2_lat - p1_lat) / (p2_lon - p1_lon) + p1_lat
                        if p1_lat == p2_lat or lat <= lat_inters:
                            inside = not inside
            p1_lat, p1_lon = p2_lat, p2_lon

        return inside
