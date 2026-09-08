import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.organizations.models import Organization
from apps.contractors.models import Contractor

class Project(models.Model):
    """
    Capital infrastructure construction, widening, retrofit, and development project.
    """
    STATUS_CHOICES = [
        ('PLANNING', _('Planning & Feasibility')),
        ('APPROVED', _('Approved / Funding Allocated')),
        ('ACTIVE', _('Active Construction / Execution')),
        ('DELAYED', _('Delayed / Schedule Variance')),
        ('COMPLETED', _('Completed & Handed Over')),
        ('CANCELLED', _('Cancelled / De-scoped')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name=_('Project Reference ID')
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('Project Title')
    )
    description = models.TextField(
        verbose_name=_('Project Scope & Objectives')
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name=_('Owner Agency')
    )
    project_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_projects',
        verbose_name=_('Lead Project Manager')
    )
    contractor = models.ForeignKey(
        Contractor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects',
        verbose_name=_('Prime Contractor')
    )
    start_date = models.DateField(verbose_name=_('Commencement Date'))
    end_date = models.DateField(verbose_name=_('Target Completion Date'))
    budget = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Approved Project Budget ($)')
    )
    actual_spending = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Cumulative Spending ($)')
    )
    progress = models.IntegerField(
        default=0,
        verbose_name=_('Overall Progress Percentage (0–100%)')
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='PLANNING',
        db_index=True,
        verbose_name=_('Project Status')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = _('Project')
        verbose_name_plural = _('Capital Projects')
        indexes = [
            models.Index(fields=['project_id']),
            models.Index(fields=['status', '-start_date']),
        ]

    def __str__(self):
        return f"[{self.project_id}] {self.name} ({self.progress}% - {self.get_status_display()})"

    @property
    def budget_variance(self):
        return self.budget - self.actual_spending


class ProjectMilestone(models.Model):
    """
    Work Breakdown Structure (WBS) major milestones.
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='milestones',
        verbose_name=_('Parent Project')
    )
    milestone_title = models.CharField(max_length=255, verbose_name=_('Milestone Title'))
    due_date = models.DateField(verbose_name=_('Milestone Due Date'))
    is_completed = models.BooleanField(default=False, verbose_name=_('Milestone Achieved'))
    completed_date = models.DateField(null=True, blank=True, verbose_name=_('Actual Completion Date'))
    weight_percentage = models.IntegerField(default=20, verbose_name=_('Weight / Contribution (%)'))

    class Meta:
        ordering = ['due_date']
        verbose_name = _('Project Milestone')
        verbose_name_plural = _('Project Milestones')

    def __str__(self):
        return f"{self.project.project_id} - {self.milestone_title} ({'ACHIEVED' if self.is_completed else 'PENDING'})"
