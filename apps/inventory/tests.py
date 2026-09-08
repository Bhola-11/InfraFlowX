from django.test import TestCase
from datetime import date
from apps.inventory.lotted_inventory import LottedInventoryValuationEngine, InventoryLot
from apps.inventory.rfid_barcode_tracker import BarcodeRFIDEngine
from apps.inventory.supplier_leadtime import SupplierLeadTimeEngine


class InventoryEngineeringTestCase(TestCase):
    def test_fifo_depletion(self):
        lots = [
            InventoryLot(lot_number="L1", quantity=10.0, unit_cost=50.0, received_date=date(2026, 1, 1)),
            InventoryLot(lot_number="L2", quantity=20.0, unit_cost=60.0, received_date=date(2026, 2, 1)),
        ]
        res = LottedInventoryValuationEngine.deplete_fifo(lots, units_demanded=15.0)
        self.assertEqual(res["units_fulfilled"], 15.0)
        self.assertEqual(res["total_cogs"], 10.0 * 50.0 + 5.0 * 60.0)

    def test_barcode_parsing(self):
        res = BarcodeRFIDEngine.parse_gs1_128("(01)12345678901234(10)LOT998")
        self.assertTrue(res["is_valid_gs1"])

    def test_supplier_leadtime(self):
        records = [
            {"promised_days": 10, "actual_days": 10, "on_time": True},
            {"promised_days": 10, "actual_days": 12, "on_time": False},
        ]
        res = SupplierLeadTimeEngine.analyze_supplier_performance(records)
        self.assertEqual(res["total_shipments_evaluated"], 2)
