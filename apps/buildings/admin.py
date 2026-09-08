from django.contrib import admin
from .models import Building, BuildingFloor

class BuildingFloorInline(admin.TabularInline):
    model = BuildingFloor
    extra = 0

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    inlines = [BuildingFloorInline]
    list_display = ('building_id_code', 'building_name', 'building_type', 'floor_count', 'total_area_sqft', 'energy_rating', 'is_fire_safety_certified')
    list_filter = ('building_type', 'energy_rating', 'is_fire_safety_certified')
    search_fields = ('building_id_code', 'building_name', 'address')
