"""
Budget Management Services
"""
from decimal import Decimal
from django.db import transaction
from apps.budgets.models import Budget, BudgetAllocation
from apps.audit.utils import log_audit_event


class BudgetService:
    @staticmethod
    @transaction.atomic
    def record_expenditure_against_allocation(allocation_id, amount, user=None):
        alloc = BudgetAllocation.objects.select_related('budget').get(id=allocation_id)
        alloc.spent_amount += Decimal(str(amount))
        alloc.save(update_fields=['spent_amount'])
        
        bud = alloc.budget
        bud.spent_amount += Decimal(str(amount))
        bud.save(update_fields=['spent_amount'])
        
        log_audit_event(
            action='BUDGET_ACTION',
            module='budgets',
            object_id=str(alloc.id),
            object_repr=str(alloc),
            description=f"Disbursement of ${amount:,} recorded on allocation '{alloc.category_name}'",
            user=user
        )
        return alloc
