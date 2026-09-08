"""
Maintenance Management Services
"""
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from apps.maintenance.models import MaintenancePlan, MaintenanceActionLog
from apps.maintenance.engineering import RCMEngine
from apps.audit.utils import log_audit_event
from apps.notifications.utils import send_notification


class MaintenanceService:
    @staticmethod
    @transaction.atomic
    def execute_maintenance_action(plan, step_description, technician=None, parts_replaced="", notes=""):
        log = MaintenanceActionLog.objects.create(
            maintenance_plan=plan,
            step_description=step_description,
            technician=technician,
            parts_replaced=parts_replaced,
            notes=notes
        )
        
        log_audit_event(
            action='MAINTENANCE_ACTION',
            module='maintenance',
            object_id=str(log.id),
            object_repr=str(log),
            description=f"Action '{step_description}' executed on Plan {plan.maintenance_code}",
            user=technician
        )
        return log

    @staticmethod
    @transaction.atomic
    def complete_maintenance_plan(plan_id, actual_completion_date=None, user=None):
        plan = MaintenancePlan.objects.get(id=plan_id)
        plan.status = 'COMPLETED'
        plan.completion_date = actual_completion_date or timezone.now().date()
        plan.save(update_fields=['status', 'completion_date'])
        
        # Reset asset status to ACTIVE if it was under maintenance
        if plan.asset and plan.asset.status == 'UNDER_MAINTENANCE':
            plan.asset.status = 'ACTIVE'
            plan.asset.save(update_fields=['status'])
            
        log_audit_event(
            action='UPDATE',
            module='maintenance',
            object_id=str(plan.id),
            object_repr=str(plan),
            description=f"Maintenance Plan {plan.maintenance_code} marked COMPLETED",
            user=user
        )
        
        if user:
            send_notification(
                recipient=user,
                title=f"Maintenance Completed: {plan.maintenance_code}",
                message=f"Job '{plan.title}' on asset '{plan.asset.name}' has been successfully completed.",
                notification_type='SYSTEM',
                priority='MEDIUM'
            )
        return plan
