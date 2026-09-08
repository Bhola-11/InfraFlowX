"""
Geospatial Location Services
"""
import math
from apps.locations.models import Location


class LocationService:
    @staticmethod
    def calculate_haversine_distance_km(lat1, lon1, lat2, lon2):
        """
        Calculates Great Circle Distance between two GPS points in kilometers.
        """
        r = 6371.0 # Earth radius in km
        dlat = math.radians(float(lat2) - float(lat1))
        dlon = math.radians(float(lon2) - float(lon1))
        a = math.sin(dlat / 2.0)**2 + math.cos(math.radians(float(lat1))) * math.cos(math.radians(float(lat2))) * math.sin(dlon / 2.0)**2
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return round(r * c, 3)
