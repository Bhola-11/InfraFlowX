from django.test import TestCase
from apps.expenses.ocr_receipt_parser import ReceiptOCRParserEngine
from apps.expenses.approval_chain import ExpenseApprovalChainEngine
from apps.expenses.tax_depreciation import AssetTaxDepreciationEngine


class ExpensesEngineeringTestCase(TestCase):
    def test_receipt_ocr_parser(self):
        items = [{"description": "Asphalt", "amount": 100.0}]
        res = ReceiptOCRParserEngine.parse_and_validate_receipt("Vendor A", items, tax_amount=8.25, stated_total=108.25)
        self.assertTrue(res["reconciliation_passed"])

    def test_approval_chain(self):
        res = ExpenseApprovalChainEngine.determine_required_approval(25000.0)
        self.assertEqual(res["approver_role_required"], "DIRECTOR")

    def test_tax_depreciation_macrs(self):
        sched = AssetTaxDepreciationEngine.generate_macrs_schedule(100000.0, recovery_period_years=5)
        self.assertEqual(len(sched), 6)
