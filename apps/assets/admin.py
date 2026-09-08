from django.contrib import admin
from .models import Asset, AssetCategory, AssetStatusHistory

class AssetStatusHistoryInline(admin.TabularInline):
    model = AssetStatusHistory
    extra = 0
    readonly_fields = ('previous_status', 'new_status', 'changed_by', 'reason', 'timestamp')

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    inlines = [AssetStatusHistoryInline]
    list_display = ('asset_id', 'name', 'asset_type', 'organization', 'condition', 'condition_score', 'status', 'current_value')
    list_filter = ('asset_type', 'status', 'condition', 'organization')
    search_fields = ('asset_id', 'name', 'serial_number', 'barcode')

@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
