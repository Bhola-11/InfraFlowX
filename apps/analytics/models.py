import uuid
from decimal import Decimal
from django.db import models
from apps.assets.models import Asset
from apps.organizations.models import Organization


class DashboardMetricSnapshot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True, related_name='metric_snapshots')
    snapshot_date = models.DateField(auto_now_add=True)
    total_assets_count = models.PositiveIntegerField(default=0)
    operational_assets_count = models.PositiveIntegerField(default=0)
    under_repair_assets_count = models.PositiveIntegerField(default=0)
    critical_defects_count = models.PositiveIntegerField(default=0)
    active_workorders_count = models.PositiveIntegerField(default=0)
    completed_inspections_count = models.PositiveIntegerField(default=0)
    total_budget_allocated = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal('0.00'))
    total_budget_spent = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal('0.00'))
    overall_health_index_avg = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('100.00'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-snapshot_date']
        verbose_name = 'Dashboard Metric Snapshot'
        verbose_name_plural = 'Dashboard Metric Snapshots'

    def __str__(self):
        return f"Snapshot {self.snapshot_date} - Assets: {self.total_assets_count}"


class KPITarget(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    metric_key = models.CharField(max_length=60, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    target_value = models.DecimalField(max_digits=12, decimal_places=2)
    warning_threshold = models.DecimalField(max_digits=12, decimal_places=2)
    critical_threshold = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(max_length=30, default='%')
    current_actual_value = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    is_higher_better = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'KPI Target'
        verbose_name_plural = 'KPI Targets'

    def __str__(self):
        return f"{self.name} (Target: {self.target_value}{self.unit})"

    @property
    def status(self):
        if self.is_higher_better:
            if self.current_actual_value >= self.target_value:
                return 'SUCCESS'
            elif self.current_actual_value >= self.warning_threshold:
                return 'WARNING'
            else:
                return 'DANGER'
        else:
            if self.current_actual_value <= self.target_value:
                return 'SUCCESS'
            elif self.current_actual_value <= self.warning_threshold:
                return 'WARNING'
            else:
                return 'DANGER'


class InfrastructureHealthIndex(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='health_indexes')
    pavement_condition_index = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="PCI score (0 - 100)")
    bridge_condition_index = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="BCI score (0 - 100)")
    structural_integrity_rating = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('100.00'))
    risk_priority_number = models.PositiveIntegerField(default=1, help_text="RPN = Severity x Occurrence x Detection (1-1000)")
    expected_remaining_service_life_years = models.DecimalField(max_digits=5, decimal_places=1, default=Decimal('20.0'))
    calculated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-calculated_at']
        verbose_name = 'Infrastructure Health Index'
        verbose_name_plural = 'Infrastructure Health Indexes'

    def __str__(self):
        return f"Health Index for {self.asset.name}: Structural Rating {self.structural_integrity_rating}%"
