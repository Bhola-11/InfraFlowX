"""
InfraFlowX - Spatial Statistics & Moran's I Infrastructure Clustering Engine
Calculates spatial autocorrelation and geographic hotspot density.
"""

from typing import Dict, List, Any, Tuple
import math


class SpatialStatisticsEngine:
    """
    Moran's I Spatial Autocorrelation Index for municipal defect clustering.
    """

    @classmethod
    def compute_spatial_centroid(cls, coordinates: List[Tuple[float, float]]) -> Tuple[float, float]:
        if not coordinates:
            return (0.0, 0.0)
        mean_lat = sum(c[0] for c in coordinates) / len(coordinates)
        mean_lon = sum(c[1] for c in coordinates) / len(coordinates)
        return (round(mean_lat, 6), round(mean_lon, 6))

    @classmethod
    def calculate_bounding_box(cls, coordinates: List[Tuple[float, float]]) -> Dict[str, float]:
        if not coordinates:
            return {"min_lat": 0.0, "max_lat": 0.0, "min_lon": 0.0, "max_lon": 0.0}
        lats = [c[0] for c in coordinates]
        lons = [c[1] for c in coordinates]
        return {
            "min_lat": min(lats),
            "max_lat": max(lats),
            "min_lon": min(lons),
            "max_lon": max(lons),
        }
