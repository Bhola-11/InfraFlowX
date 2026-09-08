from django.test import TestCase
from apps.budgets.forecasting_engine import BudgetForecastingEngine
from apps.budgets.allocation_optimizer import BudgetAllocationOptimizer
from apps.budgets.variance_analyzer import BudgetVarianceEngine


class BudgetsEngineeringTestCase(TestCase):
    def test_budget_forecast(self):
        history = [100000.0, 110000.0, 120000.0, 130000.0]
        res = BudgetForecastingEngine.holt_linear_forecast(history, forecast_horizon_years=3)
        self.assertEqual(len(res), 3)

    def test_knapsack_allocation(self):
        candidates = [
            {"id": 1, "name": "P1", "cost": 50000.0, "benefit_score": 80.0},
            {"id": 2, "name": "P2", "cost": 60000.0, "benefit_score": 90.0},
            {"id": 3, "name": "P3", "cost": 30000.0, "benefit_score": 45.0},
        ]
        res = BudgetAllocationOptimizer.optimize_capital_allocation(available_budget=100000.0, candidate_projects=candidates)
        self.assertGreater(res["total_allocated_cost"], 0)

    def test_variance_analyzer(self):
        res = BudgetVarianceEngine.calculate_budget_variance(allocated_budget=500000.0, actual_expenditures=450000.0)
        self.assertEqual(res["variance_type"], "FAVORABLE")
