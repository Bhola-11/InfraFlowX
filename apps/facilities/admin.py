from django.contrib import admin
from .models import FacilityEquipment, FacilityServiceLog

class FacilityServiceLogInline(admin.TabularInline):
    model = FacilityServiceLog
    extra = 0

@admin.register(FacilityEquipment)
class FacilityEquipmentAdmin(admin.ModelAdmin):
    inlines = [FacilityServiceLogInline]
    list_display = ('equipment_code', 'equipment_name', 'equipment_type', 'manufacturer', 'operating_hours', 'last_service_date', 'next_service_due')
    list_filter = ('equipment_type', 'manufacturer')
    search_fields = ('equipment_code', 'equipment_name', 'model_number')
