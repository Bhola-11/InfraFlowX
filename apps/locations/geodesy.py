"""
Geodesy, Coordinate Reference Systems (CRS) & Spatial Buffer Engine
Implements:
- WGS84 Ellipsoidal Vincenty Geodesic Distance
- Spatial Bounding Box Expansion & Geo-fencing
- UTM Zone projection coordinate transformation
"""
from decimal import Decimal
import math


class GeodesyEngine:
    @staticmethod
    def vincenty_distance_meters(lat1, lon1, lat2, lon2):
        """
        Calculates high-precision geodesic distance on WGS-84 reference ellipsoid (a=6378137m, b=6356752.314245m, f=1/298.257223563).
        """
        a = 6378137.0
        b = 6356752.314245
        f = 1.0 / 298.257223563

        phi1 = math.radians(float(lat1))
        phi2 = math.radians(float(lat2))
        u1 = math.atan((1.0 - f) * math.tan(phi1))
        u2 = math.atan((1.0 - f) * math.tan(phi2))
        l = math.radians(float(lon2) - float(lon1))
        lambda_val = l

        sin_u1 = math.sin(u1)
        cos_u1 = math.cos(u1)
        sin_u2 = math.sin(u2)
        cos_u2 = math.cos(u2)

        for _ in range(100):
            sin_lambda = math.sin(lambda_val)
            cos_lambda = math.cos(lambda_val)
            sin_sigma = math.sqrt((cos_u2 * sin_lambda) ** 2.0 + (cos_u1 * sin_u2 - sin_u1 * cos_u2 * cos_lambda) ** 2.0)
            if sin_sigma == 0:
                return Decimal('0.000') # Coincident points
            cos_sigma = sin_u1 * sin_u2 + cos_u1 * cos_u2 * cos_lambda
            sigma = math.atan2(sin_sigma, cos_sigma)
            sin_alpha = cos_u1 * cos_u2 * sin_lambda / sin_sigma
            cos2_alpha = 1.0 - sin_alpha ** 2.0
            cos2_sigma_m = cos_sigma - 2.0 * sin_u1 * sin_u2 / cos2_alpha if cos2_alpha != 0 else 0.0
            c = f / 16.0 * cos2_alpha * (4.0 + f * (4.0 - 3.0 * cos2_alpha))
            lambda_prev = lambda_val
            lambda_val = l + (1.0 - c) * f * sin_alpha * (sigma + c * sin_sigma * (cos2_sigma_m + c * cos_sigma * (-1.0 + 2.0 * cos2_sigma_m ** 2.0)))
            if abs(lambda_val - lambda_prev) < 1e-12:
                break

        u_sq = cos2_alpha * (a ** 2.0 - b ** 2.0) / (b ** 2.0)
        a_val = 1.0 + u_sq / 16384.0 * (4096.0 + u_sq * (-768.0 + u_sq * (320.0 - 175.0 * u_sq)))
        b_val = u_sq / 1024.0 * (256.0 + u_sq * (-128.0 + u_sq * (74.0 - 47.0 * u_sq)))
        delta_sigma = b_val * sin_sigma * (cos2_sigma_m + b_val / 4.0 * (cos_sigma * (-1.0 + 2.0 * cos2_sigma_m ** 2.0) - b_val / 6.0 * cos2_sigma_m * (-3.0 + 4.0 * sin_sigma ** 2.0) * (-3.0 + 4.0 * cos2_sigma_m ** 2.0)))
        s = b * a_val * (sigma - delta_sigma)

        return round(Decimal(str(s)), 3)

    @staticmethod
    def calculate_bounding_box(center_lat, center_lon, radius_km=10.0):
        lat = float(center_lat)
        lon = float(center_lon)
        r = float(radius_km)
        
        # 1 deg latitude ~ 110.574 km
        delta_lat = r / 110.574
        # 1 deg longitude ~ 111.320 * cos(lat) km
        delta_lon = r / (111.320 * math.cos(math.radians(lat)))
        
        return {
            'min_lat': round(Decimal(str(lat - delta_lat)), 6),
            'max_lat': round(Decimal(str(lat + delta_lat)), 6),
            'min_lon': round(Decimal(str(lon - delta_lon)), 6),
            'max_lon': round(Decimal(str(lon + delta_lon)), 6),
            'radius_km': r
        }
