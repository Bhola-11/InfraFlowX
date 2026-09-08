"""
Comprehensive Unit Tests for Locations App
"""
from decimal import Decimal
from django.test import TestCase
from apps.organizations.models import Organization
from apps.locations.models import Location
from apps.locations.services import LocationService


class LocationsTestSuite(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='City Council', code='CC-01')
        self.loc1 = Location.objects.create(
            organization=self.org,
            name='Central Depot',
            code='LOC-DEL-01',
            latitude=Decimal('28.6139'),
            longitude=Decimal('77.2090')
        )
        self.loc2 = Location.objects.create(
            organization=self.org,
            name='Yamuna Crossing Site',
            code='LOC-DEL-02',
            latitude=Decimal('28.7041'),
            longitude=Decimal('77.1025')
        )

    def test_haversine_distance(self):
        dist_km = LocationService.calculate_haversine_distance_km(
            lat1=self.loc1.latitude,
            lon1=self.loc1.longitude,
            lat2=self.loc2.latitude,
            lon2=self.loc2.longitude
        )
        self.assertGreater(dist_km, 5.0)
        self.assertLess(dist_km, 30.0)
