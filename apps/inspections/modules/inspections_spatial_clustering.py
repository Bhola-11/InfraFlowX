"""
InfraFlowX Enterprise Platform - Inspections Spatial Clustering & Zone Partitioning Engine
Implements density-based spatial clustering (DBSCAN style) and geographic hot-spot grouping.
"""

from typing import Dict, List, Any, Tuple
import math


class InspectionsSpatialClusteringEngine:
    """
    Groups spatial infrastructure points into clusters based on proximity and severity.
    """

    @classmethod
    def compute_distance_meters(cls, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        r = 6371000.0  # Earth radius in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)

        a = math.sin(dphi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0)**2
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return r * c

    @classmethod
    def cluster_points_by_radius(cls, points: List[Dict[str, Any]], radius_meters: float = 500.0, min_points_for_cluster: int = 2) -> Dict[str, Any]:
        """
        Greedy spatial proximity clustering.
        points: List of {"id": 1, "lat": 37.77, "lon": -122.41, "severity": 4}
        """
        visited = set()
        clusters = []
        noise = []

        for i, pt in enumerate(points):
            if i in visited:
                continue

            visited.add(i)
            neighbors = [i]
            for j, other in enumerate(points):
                if i != j:
                    d = cls.compute_distance_meters(pt["lat"], pt["lon"], other["lat"], other["lon"])
                    if d <= radius_meters:
                        neighbors.append(j)

            if len(neighbors) >= min_points_for_cluster:
                cluster_pts = []
                for idx in neighbors:
                    visited.add(idx)
                    cluster_pts.append(points[idx])

                # Centroid
                mean_lat = sum(p["lat"] for p in cluster_pts) / len(cluster_pts)
                mean_lon = sum(p["lon"] for p in cluster_pts) / len(cluster_pts)
                avg_severity = sum(p.get("severity", 1) for p in cluster_pts) / len(cluster_pts)

                clusters.append({
                    "cluster_id": len(clusters) + 1,
                    "centroid_lat": round(mean_lat, 6),
                    "centroid_lon": round(mean_lon, 6),
                    "points_count": len(cluster_pts),
                    "average_severity": round(avg_severity, 2),
                    "point_ids": [p.get("id") for p in cluster_pts],
                })
            else:
                noise.append(pt.get("id"))

        return {
            "app_module": "inspections",
            "total_points_evaluated": len(points),
            "clusters_discovered": len(clusters),
            "noise_points_count": len(noise),
            "clusters": clusters,
        }
