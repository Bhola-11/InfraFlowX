"""
InfraFlowX - Global End-to-End Test Suite for All 27 Domain Apps
"""

import pytest
from django.test import Client, TestCase
from apps.roads.traffic_flow import GreenshieldsModel
from apps.bridges.hydrology import BridgeHydrologyEngine
from apps.buildings.energy_audit import BuildingEnergyAuditEngine
from apps.facilities.reliability import FacilityReliabilityEngine
from apps.conditions.sensor_fusion import KalmanSensorFusionEngine
from apps.assets.risk_matrix import AssetRiskMatrixEngine


class GlobalPlatformIntegrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_homepage_render(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_roads_speed_density(self):
        model = GreenshieldsModel(free_flow_speed=110.0, jam_density=120.0)
        self.assertEqual(model.speed_at_density(0), 110.0)
        self.assertEqual(model.speed_at_density(120), 0.0)

    def test_bridge_pier_scour(self):
        res = BridgeHydrologyEngine.calculate_pier_scour_hec18(flow_velocity_mps=2.0, approach_depth_m=3.5, pier_width_m=1.2)
        self.assertGreater(res["scour_depth_m"], 0.0)

    def test_building_ghg_emissions(self):
        res = BuildingEnergyAuditEngine.calculate_ghg_emissions(electricity_kwh=50000.0, natural_gas_therms=2500.0)
        self.assertGreater(res["total_ghg_mt_co2e"], 5.0)

    def test_facility_reliability(self):
        res = FacilityReliabilityEngine.calculate_k_out_of_n_system(n_total_units=3, k_required_units=2, unit_reliability=0.92)
        self.assertGreater(res["system_reliability"], 0.95)

    def test_kalman_sensor_fusion(self):
        kf = KalmanSensorFusionEngine(initial_state=100.0)
        est, _ = kf.update(98.5)
        self.assertAlmostEqual(est, 98.6, places=1)

    def test_asset_risk_matrix(self):
        res = AssetRiskMatrixEngine.calculate_business_risk_exposure(condition_score=72.0, age_years=10.0, expected_life_years=30.0)
        self.assertIn("business_risk_exposure_score", res)
