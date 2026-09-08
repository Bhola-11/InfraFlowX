from django.contrib import admin
from .models import Warehouse, InventoryCategory, SparePart, StockItem, StockMovementLedger, PurchaseRequisition, PurchaseRequisitionItem


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'organization', 'location', 'capacity_sqm', 'manager', 'is_active')
    search_fields = ('name', 'code', 'address')
    list_filter = ('organization', 'is_active')


@admin.register(InventoryCategory)
class InventoryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'parent', 'created_at')
    search_fields = ('name', 'code')


class StockItemInline(admin.TabularInline):
    model = StockItem
    extra = 0


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ('part_number', 'name', 'category', 'unit_of_measure', 'unit_cost', 'minimum_reorder_level', 'is_active')
    search_fields = ('part_number', 'name', 'manufacturer', 'barcode')
    list_filter = ('category', 'unit_of_measure', 'is_hazardous', 'is_active')
    inlines = [StockItemInline]


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ('spare_part', 'warehouse', 'quantity_on_hand', 'quantity_reserved', 'status', 'last_stocktake_date')
    search_fields = ('spare_part__name', 'spare_part__part_number', 'warehouse__name')
    list_filter = ('status', 'warehouse')


@admin.register(StockMovementLedger)
class StockMovementLedgerAdmin(admin.ModelAdmin):
    list_display = ('movement_number', 'movement_type', 'spare_part', 'source_warehouse', 'destination_warehouse', 'quantity', 'total_cost', 'created_at')
    search_fields = ('movement_number', 'spare_part__name', 'reference_po')
    list_filter = ('movement_type', 'created_at')


class PurchaseRequisitionItemInline(admin.TabularInline):
    model = PurchaseRequisitionItem
    extra = 1


@admin.register(PurchaseRequisition)
class PurchaseRequisitionAdmin(admin.ModelAdmin):
    list_display = ('pr_number', 'title', 'requesting_department', 'status', 'priority', 'total_estimated_cost', 'created_at')
    search_fields = ('pr_number', 'title', 'justification')
    list_filter = ('status', 'priority', 'requesting_department')
    inlines = [PurchaseRequisitionItemInline]
