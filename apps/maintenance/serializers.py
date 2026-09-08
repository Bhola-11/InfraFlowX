"""
Maintenance Serializers
"""
from apps.maintenance.models import MaintenancePlan, MaintenanceActionLog


class MaintenanceSerializer:
    @staticmethod
    def to_dict(plan):
        return {
            'id': str(plan.id),
            'maintenance_code': plan.maintenance_code,
            'title': plan.title,
            'maintenance_type': plan.maintenance_type,
            'maintenance_type_display': plan.get_maintenance_type_display(),
            'priority': plan.priority,
            'priority_display': plan.get_priority_display(),
            'status': plan.status,
            'status_display': plan.get_status_display(),
            'asset_id': plan.asset.asset_id if plan.asset else None,
            'asset_name': plan.asset.name if plan.asset else None,
            'contractor': plan.contractor.company_name if plan.contractor else None,
            'assigned_team': plan.assigned_team.name if plan.assigned_team else None,
            'start_date': plan.start_date.isoformat() if plan.start_date else None,
            'completion_date': plan.completion_date.isoformat() if plan.completion_date else None,
            'estimated_hours': float(plan.estimated_hours),
            'cost': float(plan.cost),
            'action_logs_count': plan.action_logs.count(),
        }
