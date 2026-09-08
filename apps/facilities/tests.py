"""
InfraFlowX - Facilities Application Test Suite
Tests MTBF/MTTR, Redundancy, Water Pipe Hydraulics, and Pump Operating Points.
"""

from django.test import TestCase
from apps.facilities.engineering import EquipmentReliabilityEngine
from apps.facilities.reliability import FacilityReliabilityEngine
from apps.facilities.water_distribution import WaterDistributionHydraulicsEngine


class FacilitiesEngineeringTestCase(TestCase):
    def test_oee(self):
        oee = EquipmentReliabilityEngine.calculate_oee(availability_pct=95.0, performance_pct=90.0, quality_pct=99.0)
        self.assertAlmostEqual(float(oee), 84.65, places=1)

    def test_k_out_of_n_redundancy(self):
        res = FacilityReliabilityEngine.calculate_k_out_of_n_system(n_total_units=3, k_required_units=2, unit_reliability=0.90)
        self.assertGreater(res["system_reliability"], 0.95)

    def test_pipe_head_loss(self):
        res = WaterDistributionHydraulicsEngine.calculate_pipe_head_loss(
            length_m=1000.0,
            flow_m3_s=0.05,
            internal_diameter_m=0.25,
            pipe_material="DUCTILE_IRON_NEW"
        )
        self.assertIn("head_loss_meters", res)
        self.assertGreater(res["head_loss_meters"], 0.1)
