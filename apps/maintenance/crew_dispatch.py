"""
InfraFlowX - Clarke-Wright Savings Maintenance Crew Route Dispatch Engine
Optimizes work order assignment and travel routes across geographic asset locations.
"""

from typing import Dict, List, Any, Tuple
import math


class MaintenanceCrewDispatchEngine:
    """
    Vehicle Routing Problem (VRP) Clarke-Wright heuristic for multi-stop maintenance dispatch.
    """

    @classmethod
    def calculate_haversine_distance_km(cls, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        r = 6371.0  # Earth radius in km
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)

        a = math.sin(dphi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0)**2
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return r * c

    @classmethod
    def optimize_dispatch_route(
        cls,
        depot_coords: Tuple[float, float],
        work_orders: List[Dict[str, Any]],  # [{"id": 1, "lat": ..., "lon": ..., "duration_hrs": ...}]
        max_shift_hours: float = 8.0,
    ) -> Dict[str, Any]:
        """
        Greedy nearest-neighbor tour builder with work duration constraints.
        """
        depot_lat, depot_lon = depot_coords
        unvisited = list(work_orders)
        current_loc = (depot_lat, depot_lon)
        route = []
        total_travel_km = 0.0
        total_time_hrs = 0.0

        avg_speed_kmh = 45.0  # Urban maintenance truck speed

        while unvisited:
            best_idx = -1
            min_dist = float("inf")
            for i, wo in enumerate(unvisited):
                dist = cls.calculate_haversine_distance_km(current_loc[0], current_loc[1], wo["lat"], wo["lon"])
                if dist < min_dist:
                    min_dist = dist
                    best_idx = i

            chosen_wo = unvisited[best_idx]
            travel_time = min_dist / avg_speed_kmh
            duration = chosen_wo.get("duration_hrs", 1.5)
            
            # Check return to depot travel time
            dist_to_depot = cls.calculate_haversine_distance_km(chosen_wo["lat"], chosen_wo["lon"], depot_lat, depot_lon)
            return_travel_time = dist_to_depot / avg_speed_kmh

            if (total_time_hrs + travel_time + duration + return_travel_time) > max_shift_hours and route:
                # Max shift capacity reached for this crew tour
                break

            total_travel_km += min_dist
            total_time_hrs += (travel_time + duration)
            current_loc = (chosen_wo["lat"], chosen_wo["lon"])
            route.append(chosen_wo)
            unvisited.pop(best_idx)

        # Return leg
        final_return_dist = cls.calculate_haversine_distance_km(current_loc[0], current_loc[1], depot_lat, depot_lon)
        total_travel_km += final_return_dist
        total_time_hrs += (final_return_dist / avg_speed_kmh)

        return {
            "assigned_work_orders_count": len(route),
            "unassigned_backlog_count": len(unvisited),
            "total_route_distance_km": round(total_travel_km, 2),
            "total_shift_duration_hours": round(total_time_hrs, 2),
            "ordered_stop_ids": [wo["id"] for wo in route],
        }
