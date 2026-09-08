import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.assets.models import Asset
from apps.locations.models import Location
from apps.employees.models import Employee
from apps.contractors.models import Contractor

class WorkOrder(models.Model):
    """
    Work order ticket governing field execution, job labor, parts, cost actuals, and sign-offs.
    """
    STATUS_CHOICES = [
        ('CREATED', _('Created / Ticket Opened')),
        ('ASSIGNED', _('Assigned to Crew / Vendor')),
        ('SCHEDULED', _('Scheduled in Field Calendar')),
        ('IN_PROGRESS', _('In Progress / Field Execution')),
        ('WAITING', _('Waiting for Parts / Permitting')),
        ('COMPLETED', _('Completed & Ready for Inspection')),
        ('CANCELLED', _('Cancelled / Aborted')),
    ]

    PRIORITY_CHOICES = [
        ('LOW', _('Low')),
        ('MEDIUM', _('Medium')),
        ('HIGH', _('High Priority')),
        ('CRITICAL', _('Critical Emergency Dispatch')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workorder_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name=_('Work Order ID')
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_('Work Order Title / Summary')
    )
    description = models.TextField(
        verbose_name=_('Scope of Work & Technical Instructions')
    )
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='work_orders',
        verbose_name=_('Target Asset')
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='work_orders',
        verbose_name=_('Field Site Location')
    )
    assigned_employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_work_orders',
        verbose_name=_('Assigned Field Engineer / Lead')
    )
    contractor = models.ForeignKey(
        Contractor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='work_orders',
        verbose_name=_('Contractor Vendor (If Out-sourced)')
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='MEDIUM',
        verbose_name=_('Priority')
    )
    estimated_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Estimated Cost ($)')
    )
    actual_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Actual Incurred Cost ($)')
    )
    due_date = models.DateField(
        verbose_name=_('Target Completion Date')
    )
    completion_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Actual Completion Date')
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='CREATED',
        db_index=True,
        verbose_name=_('Execution Status')
    )
    is_safety_briefed = models.BooleanField(
        default=True,
        verbose_name=_('Safety Tailgate Briefing Verified')
    )
    client_signoff = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_('Client / Inspector Sign-Off Name')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-due_date', '-created_at']
        verbose_name = _('Work Order')
        verbose_name_plural = _('Work Orders')
        indexes = [
            models.Index(fields=['workorder_id']),
            models.Index(fields=['status', 'priority']),
        ]

    def __str__(self):
        return f"[{self.workorder_id}] {self.title} ({self.get_priority_display()}) - {self.get_status_display()}"


class WorkOrderTask(models.Model):
    """
    Sub-tasks and step checklists executed under a work order.
    """
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='tasks')
    task_title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    hours_spent = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
    technician_name = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = _('Work Order Task')
        verbose_name_plural = _('Work Order Tasks')

    def __str__(self):
        return f"{self.work_order.workorder_id}: {self.task_title} ({'DONE' if self.is_completed else 'PENDING'})"
