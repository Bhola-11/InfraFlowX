from django.contrib import admin
from .models import Inspection, InspectionChecklistItem

class InspectionChecklistItemInline(admin.TabularInline):
    model = InspectionChecklistItem
    extra = 0

@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    inlines = [InspectionChecklistItemInline]
    list_display = ('inspection_id', 'asset', 'inspector', 'inspection_type', 'inspection_date', 'condition_score', 'status')
    list_filter = ('inspection_type', 'status', 'inspection_date')
    search_fields = ('inspection_id', 'asset__name', 'inspector__username')
