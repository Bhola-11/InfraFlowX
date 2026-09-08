"""
InfraFlowX - Roads Application Test Suite
Tests Highway Capacity, HDM-4 Deterioration, Geometrics, Drainage, and Pavement Models.
"""

from django.test import TestCase
from apps.roads.engineering import PavementConditionEngine, AASHTODesignEngine
from apps.roads.mechanics import MultiLayerElasticEngine, RigidPavementEngine
from apps.roads.traffic_flow import GreenshieldsModel, LWRShockwaveEngine, HCMHighwayCapacityAnalyzer, TrafficStreamParameters
from apps.roads.pavement_life import HDM4PavementDeteriorationEngine
from apps.roads.geometrics import HighwayGeometricEngine
from apps.roads.drainage import HighwayDrainageEngine


class RoadsEngineeringTestCase(TestCase):
    def test_pci_calculation(self):
        defects = [
            {"defect_type": "POTHOLE", "severity": "HIGH", "area_sqm": 25.0},
            {"defect_type": "ALLIGATOR_CRACKING", "severity": "MEDIUM", "area_sqm": 40.0},
        ]
        pci = PavementConditionEngine.calculate_pci(road_length_km=1.0, road_width_m=7.0, defects=defects)
        self.assertTrue(0 <= pci <= 100)

    def test_greenshields_model(self):
        model = GreenshieldsModel(free_flow_speed=100.0, jam_density=120.0)
        self.assertEqual(model.speed_at_density(0), 100.0)
        self.assertEqual(model.speed_at_density(120.0), 0.0)
        self.assertEqual(model.speed_at_density(60.0), 50.0)
        self.assertEqual(model.flow_at_density(60.0), 3000.0)

    def test_lwr_shockwave(self):
        model = GreenshieldsModel(free_flow_speed=100.0, jam_density=120.0)
        engine = LWRShockwaveEngine(model)
        w = engine.compute_shockwave_speed(k_upstream=20.0, k_downstream=100.0)
        self.assertIsInstance(w, float)

    def test_hcm_capacity(self):
        params = TrafficStreamParameters(free_flow_speed=110.0, jam_density=125.0, capacity=2400.0, number_of_lanes=2)
        analyzer = HCMHighwayCapacityAnalyzer(params)
        res = analyzer.evaluate_level_of_service(hourly_volume=1800.0)
        self.assertIn("level_of_service", res)
        self.assertIn(res["level_of_service"], ["A", "B", "C", "D", "E", "F"])

    def test_hdm4_deterioration(self):
        engine = HDM4PavementDeteriorationEngine(structural_number=4.5, initial_iri=1.8)
        sim = engine.run_lifecycle_simulation(horizon_years=5, annual_esal=500_000.0)
        self.assertEqual(len(sim), 5)
        self.assertGreater(sim[-1]["iri_m_per_km"], sim[0]["iri_m_per_km"])

    def test_geometrics(self):
        r_min = HighwayGeometricEngine.minimum_horizontal_radius(design_speed_kmh=100.0)
        self.assertGreater(r_min, 100.0)
        ssd = HighwayGeometricEngine.stopping_sight_distance(design_speed_kmh=100.0)
        self.assertGreater(ssd, 50.0)

    def test_drainage(self):
        q = HighwayDrainageEngine.rational_method_peak_flow(runoff_coefficient_c=0.85, rainfall_intensity_mm_hr=75.0, catchment_area_hectares=10.0)
        self.assertGreater(q, 1.0)
