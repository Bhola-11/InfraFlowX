from django.test import TestCase
from datetime import date, timedelta
from apps.contractors.bidding_engine import ContractorBiddingEngine
from apps.contractors.compliance_verifier import ContractorComplianceEngine
from apps.contractors.retention_accounting import ContractorRetentionEngine


class ContractorsEngineeringTestCase(TestCase):
    def test_bidding_evaluation(self):
        bids = [
            {"contractor_id": 1, "bid_amount": 95000.0, "is_responsive": True, "is_responsible": True},
            {"contractor_id": 2, "bid_amount": 105000.0, "is_responsive": True, "is_responsible": True},
        ]
        res = ContractorBiddingEngine.evaluate_bid_tabulation(engineers_estimate=100000.0, bids=bids)
        self.assertEqual(res["selected_awardee_contractor_id"], 1)

    def test_compliance_trir(self):
        res = ContractorComplianceEngine.calculate_osha_trir(num_recordable_injuries=1, total_hours_worked=150000.0)
        self.assertTrue(res["qualification_passed"])

    def test_retention_accounting(self):
        res = ContractorRetentionEngine.calculate_progress_billing(
            work_completed_to_date=100000.0,
            stored_materials_value=20000.0,
            retention_rate_pct=10.0,
        )
        self.assertEqual(res["total_completed_and_stored"], 120000.0)
        self.assertEqual(res["total_retainage_withheld"], 12000.0)
