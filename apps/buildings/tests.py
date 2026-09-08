"""
InfraFlowX - Buildings Application Test Suite
Tests FCI, Psychrometrics, Carbon Accounting, and Life Safety Compliance.
"""

from django.test import TestCase
from apps.buildings.engineering import FacilityConditionIndexEngine
from apps.buildings.energy_audit import BuildingEnergyAuditEngine
from apps.buildings.hvac_simulation import PsychrometricHVACEngine
from apps.buildings.compliance import BuildingComplianceEngine


class BuildingsEngineeringTestCase(TestCase):
    def test_fci_calculation(self):
        fci = FacilityConditionIndexEngine.calculate_fci(total_repair_needs_cost=150_000.0, current_replacement_value=2_000_000.0)
        self.assertAlmostEqual(float(fci), 0.075, places=3)

    def test_ghg_emissions(self):
        res = BuildingEnergyAuditEngine.calculate_ghg_emissions(electricity_kwh=100_000.0, natural_gas_therms=5_000.0)
        self.assertIn("total_ghg_mt_co2e", res)
        self.assertGreater(res["total_ghg_mt_co2e"], 10.0)

    def test_cooling_coil_sizing(self):
        res = PsychrometricHVACEngine.size_cooling_coil(airflow_cfm=5000.0, entering_db_c=28.0, entering_rh_pct=60.0)
        self.assertIn("cooling_capacity_tons", res)
        self.assertGreater(res["cooling_capacity_tons"], 1.0)

    def test_life_safety_compliance(self):
        res = BuildingComplianceEngine.evaluate_occupant_load_and_egress(
            floor_area_sqft=15000.0,
            function_use="BUSINESS_OFFICE",
            num_exits_provided=2,
            total_stairway_width_inches=88.0,
            total_door_width_inches=72.0,
        )
        self.assertTrue(res["overall_life_safety_compliant"])
