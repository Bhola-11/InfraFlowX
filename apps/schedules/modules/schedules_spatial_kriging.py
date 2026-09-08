"""
InfraFlowX Enterprise Platform - Schedules Spatial Variogram & Kriging Engine
Implements experimental semivariogram modeling (Spherical/Exponential) for geospatial prediction.
"""

from typing import Dict, List, Any, Tuple
import math


class SchedulesKrigingEngine:
    """
    Geostatistical semivariogram modeling for schedules.
    """

    @classmethod
    def spherical_semivariogram(cls, distance_h: float, nugget_c0: float, sill_c: float, range_a: float) -> float:
        """
        gamma(h) = c0 + c * (1.5*(h/a) - 0.5*(h/a)^3) for h <= a, else c0 + c
        """
        if distance_h <= 0:
            return 0.0
        if distance_h >= range_a:
            return nugget_c0 + sill_c

        hr = distance_h / range_a
        return nugget_c0 + sill_c * (1.5 * hr - 0.5 * (hr ** 3))

    @classmethod
    def fit_experimental_variogram(cls, sample_pairs: List[Tuple[float, float]], lag_bins: int = 5) -> List[Dict[str, Any]]:
        """
        Computes experimental variogram gamma(h) across discrete distance lag bins.
        sample_pairs: List of (distance_h, squared_difference_gamma)
        """
        if not sample_pairs:
            return []

        max_dist = max(p[0] for p in sample_pairs)
        lag_step = max_dist / lag_bins if lag_bins > 0 else 1.0

        binned_variograms = []
        for b in range(lag_bins):
            d_min = b * lag_step
            d_max = (b + 1) * lag_step
            pairs_in_bin = [p[1] for p in sample_pairs if d_min <= p[0] < d_max]
            
            mean_gamma = (sum(pairs_in_bin) / (2.0 * len(pairs_in_bin))) if pairs_in_bin else 0.0
            binned_variograms.append({
                "lag_bin": b + 1,
                "distance_range": f"{round(d_min, 1)}-{round(d_max, 1)}m",
                "semivariance_gamma": round(mean_gamma, 3),
                "pairs_count": len(pairs_in_bin),
            })

        return binned_variograms
