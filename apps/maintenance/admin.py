from django.contrib import admin
from .models import MaintenancePlan, MaintenanceActionLog

class MaintenanceActionLogInline(admin.TabularInline):
    model = MaintenanceActionLog
    extra = 0

@admin.register(MaintenancePlan)
class MaintenancePlanAdmin(admin.ModelAdmin):
    inlines = [MaintenanceActionLogInline]
    list_display = ('maintenance_code', 'title', 'asset', 'maintenance_type', 'priority', 'status', 'cost', 'start_date')
    list_filter = ('maintenance_type', 'priority', 'status', 'start_date')
    search_fields = ('maintenance_code', 'title', 'asset__name')
