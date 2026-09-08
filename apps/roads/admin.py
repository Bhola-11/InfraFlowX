from django.contrib import admin
from .models import Road, RoadDefect, RoadRepairHistory

class RoadDefectInline(admin.TabularInline):
    model = RoadDefect
    extra = 0

class RoadRepairHistoryInline(admin.TabularInline):
    model = RoadRepairHistory
    extra = 0

@admin.register(Road)
class RoadAdmin(admin.ModelAdmin):
    inlines = [RoadDefectInline, RoadRepairHistoryInline]
    list_display = ('road_code', 'road_name', 'surface_type', 'length_km', 'lanes_count', 'traffic_level', 'pci_score')
    list_filter = ('surface_type', 'traffic_level', 'region')
    search_fields = ('road_code', 'road_name')

@admin.register(RoadDefect)
class RoadDefectAdmin(admin.ModelAdmin):
    list_display = ('road', 'defect_type', 'severity', 'chainage_km', 'is_repaired', 'reported_date')
    list_filter = ('defect_type', 'severity', 'is_repaired')
