import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.assets.models import Asset

class Inspection(models.Model):
    """
    Field and engineering inspection record assessing asset physical integrity and safety.
    """
    INSPECTION_TYPES = [
        ('ROUTINE', _('Routine Cyclic Inspection')),
        ('SAFETY', _('Safety & Hazard Compliance Audit')),
        ('STRUCTURAL', _('Detailed Non-Destructive Structural Assessment')),
        ('PREVENTIVE', _('Pre-Maintenance Diagnostic Inspection')),
        ('EMERGENCY', _('Post-Disaster / Emergency Damage Assessment')),
    ]

    STATUS_CHOICES = [
        ('SCHEDULED', _('Scheduled / Pending Dispatch')),
        ('IN_PROGRESS', _('In Progress (Field Survey)')),
        ('COMPLETED', _('Completed & Submitted')),
        ('REVIEWED', _('Reviewed & Approved by Engineer')),
        ('REJECTED', _('Rejected / Re-Audit Required')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inspection_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name=_('Inspection Reference ID')
    )
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='inspections',
        verbose_name=_('Inspected Infrastructure Asset')
    )
    inspector = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conducted_inspections',
        verbose_name=_('Lead Inspector / Field Engineer')
    )
    inspection_type = models.CharField(
        max_length=50,
        choices=INSPECTION_TYPES,
        default='ROUTINE',
        verbose_name=_('Inspection Classification')
    )
    inspection_date = models.DateField(
        verbose_name=_('Inspection Date')
    )
    condition_score = models.IntegerField(
        default=80,
        verbose_name=_('Assessed Condition Score (0–100)')
    )
    findings = models.TextField(
        verbose_name=_('Observed Physical Findings & Defect Notes')
    )
    recommendations = models.TextField(
        blank=True,
        verbose_name=_('Engineering Recommendations / Remedial Actions')
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='SCHEDULED',
        db_index=True,
        verbose_name=_('Inspection Status')
    )
    weather_conditions = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_('Ambient Weather Conditions')
    )
    photo_primary = models.ImageField(
        upload_to='inspections/%Y/%m/',
        null=True,
        blank=True,
        verbose_name=_('Primary Photo Evidence')
    )
    photo_secondary = models.ImageField(
        upload_to='inspections/%Y/%m/',
        null=True,
        blank=True,
        verbose_name=_('Secondary Photo Evidence')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-inspection_date', '-created_at']
        verbose_name = _('Inspection')
        verbose_name_plural = _('Inspections')
        indexes = [
            models.Index(fields=['inspection_id']),
            models.Index(fields=['status', '-inspection_date']),
        ]

    def __str__(self):
        return f"[{self.inspection_id}] {self.asset.name} - {self.get_inspection_type_display()} ({self.condition_score}/100)"


class InspectionChecklistItem(models.Model):
    """
    Granular multi-point checklist questions for field inspectors.
    """
    inspection = models.ForeignKey(
        Inspection,
        on_delete=models.CASCADE,
        related_name='checklist_items',
        verbose_name=_('Inspection')
    )
    item_title = models.CharField(max_length=255, verbose_name=_('Inspection Check Item'))
    is_satisfactory = models.BooleanField(default=True, verbose_name=_('Satisfactory / Pass'))
    score_1_to_10 = models.IntegerField(default=8, verbose_name=_('Rating (1-10)'))
    comments = models.TextField(blank=True, verbose_name=_('Inspector Comments'))

    class Meta:
        ordering = ['item_title']
        verbose_name = _('Inspection Checklist Item')
        verbose_name_plural = _('Inspection Checklist Items')

    def __str__(self):
        return f"{self.item_title} - {'PASS' if self.is_satisfactory else 'FAIL'} ({self.score_1_to_10}/10)"
