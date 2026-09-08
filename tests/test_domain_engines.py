"""
InfraFlowX - Comprehensive Mathematical Verification of Domain Engines
"""

import pytest
from django.test import TestCase
from apps.projects.earned_value import EarnedValueManagementEngine
from apps.budgets.allocation_optimizer import BudgetAllocationOptimizer
from apps.contractors.bidding_engine import ContractorBiddingEngine
from apps.maintenance.predictive_maintenance import PredictiveMaintenanceEngine
from apps.audit.tamper_evident_log import MerkleAuditLogEngine


class MathematicalEnginesTestCase(TestCase):
    def test_earned_value_management(self):
        res = EarnedValueManagementEngine.calculate_evm_metrics(
            planned_value_pv=100000.0,
            earned_value_ev=95000.0,
            actual_cost_ac=90000.0,
            budget_at_completion_bac=500000.0,
        )
        self.assertGreater(res["cost_performance_index_cpi"], 1.0)
        self.assertEqual(res["cost_status"], "UNDER_BUDGET")

    def test_budget_knapsack_optimization(self):
        candidates = [
            {"id": 1, "cost": 40000.0, "benefit_score": 75.0},
            {"id": 2, "cost": 50000.0, "benefit_score": 90.0},
        ]
        res = BudgetAllocationOptimizer.optimize_capital_allocation(80000.0, candidates)
        self.assertGreater(res["total_allocated_cost"], 0)

    def test_contractor_bid_tab(self):
        bids = [
            {"contractor_id": 1, "bid_amount": 92000.0, "is_responsive": True, "is_responsible": True},
            {"contractor_id": 2, "bid_amount": 105000.0, "is_responsive": True, "is_responsible": True},
        ]
        res = ContractorBiddingEngine.evaluate_bid_tabulation(100000.0, bids)
        self.assertEqual(res["selected_awardee_contractor_id"], 1)

    def test_predictive_maintenance_rul(self):
        res = PredictiveMaintenanceEngine.calculate_remaining_useful_life_exponential(
            initial_health_index=100.0,
            current_health_index=80.0,
            operating_hours_elapsed=4000.0,
        )
        self.assertGreater(res["estimated_rul_hours"], 0.0)

    def test_merkle_audit_chain(self):
        h0 = "0" * 64
        h1 = MerkleAuditLogEngine.hash_record(h0, "Data1")
        h2 = MerkleAuditLogEngine.hash_record(h1, "Data2")
        chain = [
            {"prev_hash": h0, "event_data": "Data1", "hash": h1},
            {"prev_hash": h1, "event_data": "Data2", "hash": h2},
        ]
        self.assertTrue(MerkleAuditLogEngine.verify_hash_chain(chain)["chain_valid"])
