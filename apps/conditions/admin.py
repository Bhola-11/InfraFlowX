from django.contrib import admin
from .models import ConditionLog, DeteriorationModel

@admin.register(ConditionLog)
class ConditionLogAdmin(admin.ModelAdmin):
    list_display = ('asset', 'recorded_date', 'condition_score', 'condition_category', 'structural_index', 'assessor')
    list_filter = ('condition_category', 'recorded_date')
    search_fields = ('asset__name', 'asset__asset_id')

@admin.register(DeteriorationModel)
class DeteriorationModelAdmin(admin.ModelAdmin):
    list_display = ('asset_type', 'expected_lifecycle_years', 'annual_decay_rate_pct', 'heavy_load_multiplier', 'severe_climate_multiplier')
