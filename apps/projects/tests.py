from django.test import TestCase
from apps.projects.earned_value import EarnedValueManagementEngine


class ProjectsEngineeringTestCase(TestCase):
    def test_evm_metrics(self):
        res = EarnedValueManagementEngine.calculate_evm_metrics(
            planned_value_pv=100_000.0,
            earned_value_ev=95_000.0,
            actual_cost_ac=90_000.0,
            budget_at_completion_bac=500_000.0,
        )
        self.assertGreater(res["cost_performance_index_cpi"], 1.0)
        self.assertEqual(res["cost_status"], "UNDER_BUDGET")
