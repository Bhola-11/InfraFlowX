import uuid
from django.db import models
from django.conf import settings
from apps.organizations.models import Organization, Department, Team
from apps.assets.models import Asset
from apps.contractors.models import Contractor
from apps.workorders.models import WorkOrder
from apps.inspections.models import Inspection


class AssetSchedule(models.Model):
    SCHEDULE_TYPES = [
        ('PREVENTIVE_MAINTENANCE', 'Preventive Maintenance'),
        ('ROUTINE_INSPECTION', 'Routine Inspection'),
        ('STATUTORY_AUDIT', 'Statutory / Regulatory Audit'),
        ('STRUCTURAL_TESTING', 'Structural Non-Destructive Testing'),
        ('SEASONAL_PREPARATION', 'Monsoon / Winter Preparedness'),
    ]

    FREQUENCY_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('BIWEEKLY', 'Bi-Weekly'),
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly (3 Months)'),
        ('BIANNUAL', 'Bi-Annual (6 Months)'),
        ('ANNUAL', 'Annual (1 Year)'),
        ('CUSTOM_DAYS', 'Custom Interval (Days)'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    schedule_code = models.CharField(max_length=60, unique=True)
    title = models.CharField(max_length=255)
    schedule_type = models.CharField(max_length=40, choices=SCHEDULE_TYPES, default='PREVENTIVE_MAINTENANCE')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='schedules')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='schedules')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='schedules')
    assigned_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='schedules')
    assigned_contractor = models.ForeignKey(Contractor, on_delete=models.SET_NULL, null=True, blank=True, related_name='schedules')
    frequency = models.CharField(max_length=30, choices=FREQUENCY_CHOICES, default='MONTHLY')
    custom_interval_days = models.PositiveIntegerField(default=30, help_text="Used if frequency is Custom")
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    next_due_date = models.DateField()
    last_performed_date = models.DateField(blank=True, null=True)
    auto_generate_workorder = models.BooleanField(default=True, help_text="Automatically create Work Order upon trigger")
    auto_generate_inspection = models.BooleanField(default=False, help_text="Automatically create Inspection upon trigger")
    lead_time_days = models.PositiveIntegerField(default=3, help_text="Days prior to due date to create pending execution ticket")
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['next_due_date', 'title']
        verbose_name = 'Asset Schedule'
        verbose_name_plural = 'Asset Schedules'

    def __str__(self):
        return f"{self.schedule_code} - {self.title} ({self.get_frequency_display()})"

    @property
    def is_overdue(self):
        from django.utils import timezone
        return self.next_due_date < timezone.now().date()


class ScheduledEventExecution(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending / Scheduled'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('OVERDUE', 'Overdue'),
        ('SKIPPED', 'Skipped / Postponed'),
        ('CANCELLED', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    schedule = models.ForeignKey(AssetSchedule, on_delete=models.CASCADE, related_name='executions')
    scheduled_date = models.DateField()
    actual_start_date = models.DateField(blank=True, null=True)
    actual_completion_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING')
    work_order = models.ForeignKey(WorkOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='schedule_events')
    inspection = models.ForeignKey(Inspection, on_delete=models.SET_NULL, null=True, blank=True, related_name='schedule_events')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_schedule_events')
    findings_summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_date']
        verbose_name = 'Scheduled Event Execution'
        verbose_name_plural = 'Scheduled Event Executions'

    def __str__(self):
        return f"Execution for {self.schedule.title} on {self.scheduled_date} [{self.get_status_display()}]"
