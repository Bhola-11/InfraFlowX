from django.contrib import admin
from .models import Bridge, BridgeComponentInspection

class BridgeComponentInspectionInline(admin.TabularInline):
    model = BridgeComponentInspection
    extra = 0

@admin.register(Bridge)
class BridgeAdmin(admin.ModelAdmin):
    inlines = [BridgeComponentInspectionInline]
    list_display = ('bridge_id_code', 'bridge_name', 'bridge_type', 'length_meters', 'load_capacity_tons', 'condition', 'is_scour_critical')
    list_filter = ('bridge_type', 'condition', 'is_scour_critical')
    search_fields = ('bridge_id_code', 'bridge_name', 'feature_crossed')
