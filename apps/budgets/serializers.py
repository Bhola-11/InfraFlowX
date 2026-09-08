"""
Budget Serializers
"""
from apps.budgets.models import Budget, BudgetAllocation


class BudgetSerializer:
    @staticmethod
    def to_dict(b):
        return {
            'id': str(b.id),
            'budget_code': b.budget_code,
            'title': b.title,
            'budget_type': b.budget_type,
            'budget_type_display': b.get_budget_type_display(),
            'fiscal_year': b.fiscal_year,
            'organization': b.organization.name if b.organization else None,
            'department': b.department.name if b.department else None,
            'allocated_amount': float(b.allocated_amount),
            'spent_amount': float(b.spent_amount),
            'remaining_amount': float(b.remaining_amount),
            'utilization_percentage': b.utilization_percentage,
            'allocations_count': b.allocations.count(),
        }
