"""
InfraFlowX - Bridges Application Test Suite
Tests Sufficiency Rating, Scour Analysis, Fatigue Life, and Load Rating.
"""

from django.test import TestCase
from unittest.mock import MagicMock
from apps.bridges.engineering import BridgeSufficiencyEngine
from apps.bridges.hydrology import BridgeHydrologyEngine
from apps.bridges.fatigue import BridgeFatigueEngine
from apps.bridges.load_rating import BridgeLoadRatingEngine
from apps.bridges.sensor_analytics import RainflowCycleCounter, DynamicVibrationAnalyzer


class BridgesEngineeringTestCase(TestCase):
    def test_sufficiency_rating(self):
        mock_bridge = MagicMock()
        mock_bridge.width_meters = 12.0
        mock_bridge.vertical_clearance_meters = 5.2
        mock_bridge.is_scour_critical = False

        sr = BridgeSufficiencyEngine.calculate_sufficiency_rating(
            bridge=mock_bridge,
            deck_rating=7,
            super_rating=7,
            sub_rating=6,
            detour_length_km=5.0,
            adt=15000,
        )
        self.assertTrue(0 <= float(sr) <= 100)

    def test_pier_scour_hec18(self):
        res = BridgeHydrologyEngine.calculate_pier_scour_hec18(
            flow_velocity_mps=2.5,
            approach_depth_m=4.0,
            pier_width_m=1.5,
        )
        self.assertIn("scour_depth_m", res)
        self.assertGreater(res["scour_depth_m"], 0.0)

    def test_fatigue_cycles(self):
        res = BridgeFatigueEngine.calculate_fatigue_life_cycles(detail_category="C", effective_stress_range_mpa=75.0)
        self.assertIn("permissible_cycles_to_failure", res)
        self.assertGreater(res["permissible_cycles_to_failure"], 1000)

    def test_load_rating_lrfr(self):
        res = BridgeLoadRatingEngine.calculate_rating_factor(
            nominal_capacity_kn_m=5000.0,
            dead_load_components_kn_m=1200.0,
            dead_load_wearing_surface_kn_m=300.0,
            live_load_plus_impact_kn_m=1500.0,
        )
        self.assertIn("rating_factor_rf", res)
        self.assertGreater(res["rating_factor_rf"], 0.5)

    def test_rainflow_cycle_counting(self):
        signal = [0.0, 10.0, -5.0, 15.0, 0.0, 20.0, -10.0, 0.0]
        cycles = RainflowCycleCounter.count_cycles(signal)
        self.assertIsInstance(cycles, list)
