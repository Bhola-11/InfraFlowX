"""
Schedule & Preventive Maintenance Services
"""
from decimal import Decimal
from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from apps.schedules.models import AssetSchedule, ScheduledEventExecution
from apps.workorders.models import WorkOrder
from apps.audit.utils import log_audit_event


class ScheduleService:
    @staticmethod
    @transaction.atomic
    def trigger_scheduled_executions(user=None):
        today = timezone.now().date()
        due_schedules = AssetSchedule.objects.filter(is_active=True, next_due_date__lte=today + timedelta(days=3))
        triggered = []
        
        for sch in due_schedules:
            event, created = ScheduledEventExecution.objects.get_or_create(
                schedule=sch,
                scheduled_date=sch.next_due_date,
                defaults={'status': 'PENDING'}
            )
            if created:
                if sch.auto_generate_workorder:
                    wo = WorkOrder.objects.create(
                        workorder_id=f"WO-SCH-{sch.schedule_code[:10]}-{today.strftime('%m%d')}",
                        title=f"Scheduled PM: {sch.title}",
                        description=sch.description or f"Automated recurring maintenance execution according to schedule {sch.schedule_code}",
                        asset=sch.asset,
                        priority='MEDIUM',
                        status='CREATED',
                        due_date=sch.next_due_date
                    )
                    event.work_order = wo
                    event.save(update_fields=['work_order'])
                    
                # Advance next due date
                if sch.frequency == 'MONTHLY':
                    sch.next_due_date += timedelta(days=30)
                elif sch.frequency == 'QUARTERLY':
                    sch.next_due_date += timedelta(days=90)
                elif sch.frequency == 'ANNUAL':
                    sch.next_due_date += timedelta(days=365)
                else:
                    sch.next_due_date += timedelta(days=sch.custom_interval_days)
                    
                sch.last_performed_date = today
                sch.save(update_fields=['next_due_date', 'last_performed_date'])
                triggered.append(event)
                
        return triggered
