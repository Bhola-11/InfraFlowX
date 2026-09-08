from django.test import TestCase
from datetime import datetime, timedelta
from apps.workorders.sla_engine import WorkOrderSLAEngine
from apps.workorders.cost_estimator import WorkOrderCostEstimator


class WorkOrdersEngineeringTestCase(TestCase):
    def test_sla_evaluation(self):
        now = datetime.now()
        created = now - timedelta(hours=2)
        res = WorkOrderSLAEngine.evaluate_sla_status(
            priority="HIGH",
            created_at=created,
            current_time=now,
        )
        self.assertIn("remaining_hours_to_breach", res)

    def test_cost_estimator(self):
        labor = [{"hours": 10.0, "hourly_rate": 50.0}]
        eq = [{"hours": 5.0, "rental_rate_hr": 100.0}]
        mat = [{"quantity": 2.0, "unit_cost": 200.0}]
        res = WorkOrderCostEstimator.estimate_work_order_cost(labor, eq, mat)
        self.assertGreater(res["grand_total_estimated_cost"], 1400.0)
