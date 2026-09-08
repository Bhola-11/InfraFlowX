"""
InfraFlowX Enterprise Platform - Analytics Spatial Interpolation & Surface Estimation
Implements Inverse Distance Weighting (IDW) surface interpolation for sensor fields.
"""

from typing import Dict, List, Any, Tuple
import math


class AnalyticsSpatialInterpolationEngine:
    """
    Inverse Distance Weighting (IDW) interpolation for spatial measurements in analytics.
    """

    @classmethod
    def interpolate_idw(cls, sample_points: List[Dict[str, float]], target_lat: float, target_lon: float, power_p: float = 2.0) -> Dict[str, Any]:
        """
        z(x) = Sum(w_i * z_i) / Sum(w_i) where w_i = 1 / d(x, x_i)^p
        """
        if not sample_points:
            return {"interpolated_value": 0.0, "status": "NO_SAMPLES"}

        weights_sum = 0.0
        weighted_values_sum = 0.0

        for pt in sample_points:
            plat = pt.get("lat", 0.0)
            plon = pt.get("lon", 0.0)
            val = pt.get("value", 0.0)

            # Euclidean distance approximation for local grid
            d = math.sqrt((target_lat - plat)**2 + (target_lon - plon)**2)
            if d < 1e-6:
                return {"interpolated_value": val, "status": "EXACT_SAMPLE_LOCATION"}

            w = 1.0 / (d ** power_p)
            weights_sum += w
            weighted_values_sum += w * val

        interp_val = weighted_values_sum / weights_sum if weights_sum > 0 else 0.0

        return {
            "app_module": "analytics",
            "target_lat": target_lat,
            "target_lon": target_lon,
            "interpolated_value": round(interp_val, 3),
            "sample_points_used": len(sample_points),
            "power_exponent": power_p,
        }
