from django.contrib import admin
from .models import DashboardMetricSnapshot, KPITarget, InfrastructureHealthIndex


@admin.register(DashboardMetricSnapshot)
class DashboardMetricSnapshotAdmin(admin.ModelAdmin):
    list_display = ('snapshot_date', 'total_assets_count', 'operational_assets_count', 'active_workorders_count', 'overall_health_index_avg')


@admin.register(KPITarget)
class KPITargetAdmin(admin.ModelAdmin):
    list_display = ('name', 'metric_key', 'target_value', 'unit', 'current_actual_value', 'is_higher_better')


@admin.register(InfrastructureHealthIndex)
class InfrastructureHealthIndexAdmin(admin.ModelAdmin):
    list_display = ('asset', 'pavement_condition_index', 'bridge_condition_index', 'structural_integrity_rating', 'calculated_at')
    search_fields = ('asset__name', 'asset__asset_code')
