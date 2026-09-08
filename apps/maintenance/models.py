import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.assets.models import Asset
from apps.organizations.models import Team
from apps.contractors.models import Contractor

class MaintenancePlan(models.Model):
    """
    Preventive, corrective, predictive, and emergency maintenance operations.
    """
    MAINTENANCE_TYPES = [
        ('PREVENTIVE', _('Preventive Cyclic Maintenance')),
        ('CORRECTIVE', _('Corrective / Defect Repair')),
        ('EMERGENCY', _('Emergency Breakdown Intervention')),
        ('PREDICTIVE', _('Condition-Based Predictive Overhaul')),
    ]

    STATUS_CHOICES = [
        ('PLANNED', _('Planned / Draft')),
        ('SCHEDULED', _('Scheduled Dispatch')),
        ('IN_PROGRESS', _('In Progress (Active Work)')),
        ('ON_HOLD', _('On Hold (Awaiting Spares/Weather)')),
        ('COMPLETED', _('Completed & Commissioned')),
        ('CANCELLED', _('Cancelled')),
    ]

    PRIORITY_CHOICES = [
        ('LOW', _('Low')),
        ('MEDIUM', _('Medium')),
        ('HIGH', _('High Priority')),
        ('CRITICAL', _('Critical Emergency')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    maintenance_code = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name=_('Maintenance Code ID')
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_('Maintenance Job Title')
    )
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='maintenance_records',
        verbose_name=_('Target Infrastructure Asset')
    )
    maintenance_type = models.CharField(
        max_length=50,
        choices=MAINTENANCE_TYPES,
        default='PREVENTIVE',
        verbose_name=_('Maintenance Type')
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='MEDIUM',
        verbose_name=_('Priority Level')
    )
    assigned_team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='maintenance_jobs',
        verbose_name=_('Internal Operations Crew / Team')
    )
    contractor = models.ForeignKey(
        Contractor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='maintenance_contracts',
        verbose_name=_('External Contractor Vendor')
    )
    start_date = models.DateField(verbose_name=_('Scheduled Start Date'))
    completion_date = models.DateField(null=True, blank=True, verbose_name=_('Actual Completion Date'))
    estimated_hours = models.DecimalField(max_digits=6, decimal_places=1, default=8.0, verbose_name=_('Est. Labor Hours'))
    cost = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, verbose_name=_('Total Maintenance Cost ($)'))
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PLANNED', db_index=True)
    trigger_condition = models.CharField(max_length=200, blank=True, verbose_name=_('Maintenance Trigger / Threshold'))
    procedure_notes = models.TextField(blank=True, verbose_name=_('Standard Operating Procedure Checklist'))
    notes = models.TextField(blank=True, verbose_name=_('Execution Notes & Findings'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date', '-created_at']
        verbose_name = _('Maintenance Plan')
        verbose_name_plural = _('Maintenance Plans & Jobs')
        indexes = [
            models.Index(fields=['maintenance_code']),
            models.Index(fields=['status', 'priority']),
        ]

    def __str__(self):
        return f"[{self.maintenance_code}] {self.title} ({self.get_maintenance_type_display()}) - {self.get_status_display()}"


class MaintenanceActionLog(models.Model):
    """
    Line-item log of maintenance tasks and step executions.
    """
    maintenance_plan = models.ForeignKey(
        MaintenancePlan,
        on_delete=models.CASCADE,
        related_name='action_logs',
        verbose_name=_('Maintenance Job')
    )
    step_description = models.CharField(max_length=255, verbose_name=_('Task Step Completed'))
    technician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Technician')
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    parts_replaced = models.CharField(max_length=255, blank=True, verbose_name=_('Parts / Spares Replaced'))
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _('Maintenance Action Log')
        verbose_name_plural = _('Maintenance Action Logs')

    def __str__(self):
        return f"{self.maintenance_plan.maintenance_code}: {self.step_description} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
