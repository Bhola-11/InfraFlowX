"""
InfraFlowX - UAV Drone Autonomous Flight & Photogrammetry Telemetry Engine
Calculates Ground Sampling Distance (GSD), camera overlap, and flight corridor geometry.
"""

from typing import Dict, List, Any
import math


class DronePhotogrammetryEngine:
    """
    UAV flight planning for aerial bridge, highway corridor, and roof infrastructure inspections.
    """

    @classmethod
    def calculate_ground_sampling_distance(
        cls,
        flight_altitude_m: float,
        focal_length_mm: float,
        sensor_width_mm: float,
        image_width_pixels: int,
    ) -> Dict[str, Any]:
        """
        GSD = (Altitude * Sensor_Width) / (Focal_Length * Image_Width) * 100 (cm/pixel)
        """
        gsd_cm = (flight_altitude_m * 100.0 * sensor_width_mm) / (focal_length_mm * image_width_pixels)
        ground_footprint_width_m = (gsd_cm * image_width_pixels) / 100.0

        return {
            "ground_sampling_distance_cm_per_pixel": round(gsd_cm, 3),
            "ground_footprint_width_m": round(ground_footprint_width_m, 2),
            "crack_detection_resolution_adequate": gsd_cm <= 0.5,  # Sub-half-centimeter resolution required for micro-cracks
        }

    @classmethod
    def calculate_flight_path_waypoints(
        cls,
        corridor_start_lat: float,
        corridor_start_lon: float,
        corridor_end_lat: float,
        corridor_end_lon: float,
        corridor_width_m: float,
        flight_altitude_m: float,
        forward_overlap_pct: float = 75.0,
        sidelap_pct: float = 60.0,
    ) -> Dict[str, Any]:
        """
        Generates autonomous UAV lawnmower flight path waypoints.
        """
        # Linear distance approximation
        dlat = (corridor_end_lat - corridor_start_lat) * 111_000.0
        dlon = (corridor_end_lon - corridor_start_lon) * 111_000.0 * math.cos(math.radians(corridor_start_lat))
        corridor_length_m = math.sqrt(dlat**2 + dlon**2)
        
        # Flight line spacing based on sidelap
        fov_width_m = flight_altitude_m * 0.8  # Typical 80 deg FOV
        line_spacing_m = fov_width_m * (1.0 - sidelap_pct / 100.0)
        num_flight_lines = max(1, math.ceil(corridor_width_m / max(5.0, line_spacing_m)))
        
        # Total flight distance
        total_flight_dist_m = (corridor_length_m * num_flight_lines) + (corridor_width_m)
        estimated_flight_time_minutes = (total_flight_dist_m / 8.0) / 60.0  # 8 m/s cruise speed

        return {
            "corridor_length_m": round(corridor_length_m, 1),
            "num_flight_lines": num_flight_lines,
            "flight_line_spacing_m": round(line_spacing_m, 2),
            "total_flight_distance_m": round(total_flight_dist_m, 1),
            "estimated_flight_time_min": round(estimated_flight_time_minutes, 1),
            "battery_swaps_estimated": math.ceil(estimated_flight_time_minutes / 22.0) - 1,
        }
