from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.assets.models import Asset

class ConditionLog(models.Model):
    """
    Historical log of asset condition scores (0-100) and multi-factor engineering health indices.
    """
    CATEGORY_CHOICES = [
        ('EXCELLENT', _('Excellent (90-100)')),
        ('GOOD', _('Good (70-89)')),
        ('FAIR', _('Fair (50-69)')),
        ('POOR', _('Poor (25-49)')),
        ('CRITICAL', _('Critical (0-24)')),
    ]

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='condition_logs',
        verbose_name=_('Asset')
    )
    recorded_date = models.DateField(
        verbose_name=_('Assessment Date')
    )
    condition_score = models.IntegerField(
        verbose_name=_('Overall Health Score (0-100)')
    )
    condition_category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='GOOD'
    )
    structural_index = models.IntegerField(
        default=80,
        verbose_name=_('Structural Integrity Index (0-100)')
    )
    operational_index = models.IntegerField(
        default=85,
        verbose_name=_('Operational Reliability Index (0-100)')
    )
    safety_index = models.IntegerField(
        default=90,
        verbose_name=_('Public Safety Index (0-100)')
    )
    assessor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Lead Assessor')
    )
    notes = models.TextField(blank=True, verbose_name=_('Assessment Justification'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_date', '-created_at']
        verbose_name = _('Condition Log')
        verbose_name_plural = _('Condition Logs')
        indexes = [
            models.Index(fields=['asset', '-recorded_date']),
            models.Index(fields=['condition_category']),
        ]

    def __str__(self):
        return f"{self.asset.name} on {self.recorded_date}: Score {self.condition_score}/100 ({self.get_condition_category_display()})"


class DeteriorationModel(models.Model):
    """
    Predictive decay curves modeling asset deterioration over time by asset type and environmental exposure.
    """
    asset_type = models.CharField(
        max_length=50,
        choices=Asset.ASSET_TYPES,
        unique=True,
        verbose_name=_('Asset Classification')
    )
    expected_lifecycle_years = models.IntegerField(default=30)
    annual_decay_rate_pct = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=2.50,
        verbose_name=_('Baseline Annual Degradation Rate (%)')
    )
    heavy_load_multiplier = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=1.35,
        verbose_name=_('High Traffic / Heavy Load Factor')
    )
    severe_climate_multiplier = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=1.25,
        verbose_name=_('Harsh Climate / Freeze-Thaw Factor')
    )
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = _('Deterioration Model')
        verbose_name_plural = _('Deterioration Models')

    def __str__(self):
        return f"Deterioration Model: {self.get_asset_type_display()} ({self.annual_decay_rate_pct}%/yr)"
