"""
InfraFlowX Enterprise Platform - Expenses Cost Allocation Ledger & GAAP Journal Engine
Generates balanced double-entry accounting transactions for municipal infrastructure expenses.
"""

from typing import Dict, List, Any


class ExpensesCostLedgerEngine:
    """
    Double-entry accounting journal generator for expenses.
    """

    @classmethod
    def generate_journal_entry(cls, transaction_id: str, debit_account: str, credit_account: str, amount: float, description: str) -> Dict[str, Any]:
        amt = round(amount, 2)
        debit_line = {"account": debit_account, "debit": amt, "credit": 0.0}
        credit_line = {"account": credit_account, "debit": 0.0, "credit": amt}

        return {
            "app_module": "expenses",
            "transaction_id": transaction_id,
            "description": description,
            "total_debit": amt,
            "total_credit": amt,
            "is_balanced": True,
            "lines": [debit_line, credit_line],
        }
