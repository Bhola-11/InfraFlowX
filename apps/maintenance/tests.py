from django.test import TestCase
from apps.maintenance.predictive_maintenance import PredictiveMaintenanceEngine
from apps.maintenance.crew_dispatch import MaintenanceCrewDispatchEngine


class MaintenanceEngineeringTestCase(TestCase):
    def test_predictive_rul(self):
        res = PredictiveMaintenanceEngine.calculate_remaining_useful_life_exponential(
            initial_health_index=100.0,
            current_health_index=75.0,
            operating_hours_elapsed=5000.0,
        )
        self.assertIn("estimated_rul_hours", res)
        self.assertGreater(res["estimated_rul_hours"], 0.0)

    def test_crew_dispatch(self):
        work_orders = [
            {"id": 1, "lat": 37.77, "lon": -122.41, "duration_hrs": 1.5},
            {"id": 2, "lat": 37.78, "lon": -122.42, "duration_hrs": 2.0},
        ]
        res = MaintenanceCrewDispatchEngine.optimize_dispatch_route(
            depot_coords=(37.76, -122.40),
            work_orders=work_orders,
        )
        self.assertEqual(res["assigned_work_orders_count"], 2)
