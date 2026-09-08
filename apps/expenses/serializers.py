"""
Expense Serializers
"""
from apps.expenses.models import Expense


class ExpenseSerializer:
    @staticmethod
    def to_dict(exp):
        return {
            'id': str(exp.id),
            'expense_id': exp.expense_id,
            'asset_id': exp.asset.asset_id if exp.asset else None,
            'project_id': exp.project.project_id if exp.project else None,
            'contractor': exp.contractor.company_name if exp.contractor else None,
            'category': exp.category,
            'category_display': exp.get_category_display(),
            'amount': float(exp.amount),
            'expense_date': exp.expense_date.isoformat() if exp.expense_date else None,
            'invoice_number': exp.invoice_number,
            'description': exp.description,
            'approval_status': exp.approval_status,
            'approval_status_display': exp.get_approval_status_display(),
            'approved_by': exp.approved_by.get_full_name() if exp.approved_by else None,
        }
