"""
InfraFlowX - Structural Receipt OCR & Financial Expense Parser Engine
Extracts vendor details, line items, sales tax, and verifies mathematical consistency.
"""

from typing import Dict, List, Any
import re


class ReceiptOCRParserEngine:
    """
    Parses structured expense receipts and validates subtotal + tax = total.
    """

    @classmethod
    def parse_and_validate_receipt(
        cls,
        vendor_name: str,
        line_items: List[Dict[str, float]],  # [{"description": "Asphalt Patch", "amount": 150.0}]
        tax_amount: float,
        stated_total: float,
    ) -> Dict[str, Any]:
        
        calculated_subtotal = sum(item.get("amount", 0.0) for item in line_items)
        calculated_total = calculated_subtotal + tax_amount
        discrepancy = abs(calculated_total - stated_total)

        is_balanced = discrepancy < 0.02

        return {
            "vendor_name": vendor_name.strip(),
            "line_items_count": len(line_items),
            "calculated_subtotal": round(calculated_subtotal, 2),
            "tax_amount": round(tax_amount, 2),
            "calculated_total": round(calculated_total, 2),
            "stated_total": round(stated_total, 2),
            "discrepancy_amount": round(discrepancy, 2),
            "reconciliation_passed": is_balanced,
        }
