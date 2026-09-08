"""
Work Order Services
"""
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from apps.workorders.models import WorkOrder, WorkOrderTask
from apps.workorders.scheduler import WorkOrderSchedulingEngine
from apps.audit.utils import log_audit_event
from apps.notifications.utils import send_notification


class WorkOrderService:
    @staticmethod
    @transaction.atomic
    def dispatch_work_order(workorder_id, assigned_employee=None, contractor=None, due_date=None, user=None):
        wo = WorkOrder.objects.get(id=workorder_id)
        wo.status = 'IN_PROGRESS'
        if assigned_employee:
            wo.assigned_employee = assigned_employee
        if contractor:
            wo.contractor = contractor
        if due_date:
            wo.due_date = due_date
        wo.save(update_fields=['status', 'assigned_employee', 'contractor', 'due_date'])
        
        log_audit_event(
            action='UPDATE',
            module='workorders',
            object_id=str(wo.id),
            object_repr=str(wo),
            description=f"Work Order {wo.workorder_id} dispatched to field",
            user=user
        )
        return wo

    @staticmethod
    @transaction.atomic
    def complete_task(task_id, hours_spent, technician_name="", user=None):
        task = WorkOrderTask.objects.select_related('work_order').get(id=task_id)
        task.is_completed = True
        task.hours_spent = hours_spent
        if technician_name:
            task.technician_name = technician_name
        task.save(update_fields=['is_completed', 'hours_spent', 'technician_name'])
        
        wo = task.work_order
        # If all tasks completed, auto-complete work order
        if not wo.tasks.filter(is_completed=False).exists():
            wo.status = 'COMPLETED'
            wo.completion_date = timezone.now().date()
            wo.save(update_fields=['status', 'completion_date'])
            
        return task
