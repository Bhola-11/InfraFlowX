"""
Work Order Serializers
"""
from apps.workorders.models import WorkOrder, WorkOrderTask


class WorkOrderSerializer:
    @staticmethod
    def to_dict(wo):
        return {
            'id': str(wo.id),
            'workorder_id': wo.workorder_id,
            'title': wo.title,
            'description': wo.description,
            'asset_id': wo.asset.asset_id if wo.asset else None,
            'asset_name': wo.asset.name if wo.asset else None,
            'location': wo.location.name if wo.location else None,
            'assigned_employee': wo.assigned_employee.user.get_full_name() if wo.assigned_employee else None,
            'contractor': wo.contractor.company_name if wo.contractor else None,
            'priority': wo.priority,
            'priority_display': wo.get_priority_display(),
            'status': wo.status,
            'status_display': wo.get_status_display(),
            'estimated_cost': float(wo.estimated_cost),
            'actual_cost': float(wo.actual_cost),
            'due_date': wo.due_date.isoformat() if wo.due_date else None,
            'completion_date': wo.completion_date.isoformat() if wo.completion_date else None,
            'tasks_count': wo.tasks.count(),
            'completed_tasks_count': wo.tasks.filter(is_completed=True).count(),
        }
