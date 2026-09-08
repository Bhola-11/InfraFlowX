"""
InfraFlowX Enterprise Platform - Projects Spatial Voronoi & Service Area Partitioning
Computes nearest service depot assignment and territorial coverage polygons.
"""

from typing import Dict, List, Any, Tuple
import math


class ProjectsVoronoiEngine:
    """
    Nearest neighbor service boundary tessellation for projects.
    """

    @classmethod
    def find_nearest_service_facility(cls, query_lat: float, query_lon: float, facility_locations: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not facility_locations:
            return {"nearest_facility": None, "distance_km": -1.0}

        best_fac = None
        min_dist = float("inf")

        for fac in facility_locations:
            flat = fac.get("lat", 0.0)
            flon = fac.get("lon", 0.0)
            
            # Haversine distance in km
            dlat = math.radians(flat - query_lat)
            dlon = math.radians(flon - query_lon)
            a = math.sin(dlat/2.0)**2 + math.cos(math.radians(query_lat)) * math.cos(math.radians(flat)) * math.sin(dlon/2.0)**2
            c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
            dist_km = 6371.0 * c

            if dist_km < min_dist:
                min_dist = dist_km
                best_fac = fac

        return {
            "app_module": "projects",
            "query_coordinates": (query_lat, query_lon),
            "nearest_facility": best_fac,
            "distance_km": round(min_dist, 2),
            "estimated_drive_time_minutes": round((min_dist / 40.0) * 60.0, 1),
        }
