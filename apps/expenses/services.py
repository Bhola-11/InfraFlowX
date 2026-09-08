"""
Expense Management Services
"""
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from apps.expenses.models import Expense
from apps.audit.utils import log_audit_event


class ExpenseService:
    @staticmethod
    @transaction.atomic
    def approve_expense(expense_id, approved_by):
        exp = Expense.objects.get(id=expense_id)
        exp.approval_status = 'APPROVED'
        exp.approved_by = approved_by
        exp.approved_at = timezone.now()
        exp.save(update_fields=['approval_status', 'approved_by', 'approved_at'])
        
        log_audit_event(
            action='BUDGET_ACTION',
            module='expenses',
            object_id=str(exp.id),
            object_repr=str(exp),
            description=f"Expense voucher {exp.expense_id} approved for payment (${exp.amount:,})",
            user=approved_by
        )
        return exp
