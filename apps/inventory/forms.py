from django import forms
from .models import Warehouse, InventoryCategory, SparePart, StockItem, StockMovementLedger, PurchaseRequisition, PurchaseRequisitionItem


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'code', 'organization', 'location', 'address', 'capacity_sqm', 'manager', 'contact_phone', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'organization': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'capacity_sqm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'manager': forms.Select(attrs={'class': 'form-select'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class InventoryCategoryForm(forms.ModelForm):
    class Meta:
        model = InventoryCategory
        fields = ['name', 'code', 'description', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'parent': forms.Select(attrs={'class': 'form-select'}),
        }


class SparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = ['part_number', 'name', 'category', 'description', 'unit_of_measure', 'unit_cost',
                  'minimum_reorder_level', 'maximum_stock_level', 'lead_time_days', 'manufacturer', 'barcode', 'is_hazardous', 'is_active']
        widgets = {
            'part_number': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'unit_of_measure': forms.Select(attrs={'class': 'form-select'}),
            'unit_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'minimum_reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'maximum_stock_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'lead_time_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control'}),
            'is_hazardous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class StockItemForm(forms.ModelForm):
    class Meta:
        model = StockItem
        fields = ['warehouse', 'spare_part', 'quantity_on_hand', 'quantity_reserved', 'aisle_bin_location', 'last_stocktake_date', 'status']
        widgets = {
            'warehouse': forms.Select(attrs={'class': 'form-select'}),
            'spare_part': forms.Select(attrs={'class': 'form-select'}),
            'quantity_on_hand': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity_reserved': forms.NumberInput(attrs={'class': 'form-control'}),
            'aisle_bin_location': forms.TextInput(attrs={'class': 'form-control'}),
            'last_stocktake_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class StockMovementLedgerForm(forms.ModelForm):
    class Meta:
        model = StockMovementLedger
        fields = ['movement_number', 'movement_type', 'spare_part', 'source_warehouse', 'destination_warehouse',
                  'quantity', 'unit_price', 'total_cost', 'reference_workorder', 'reference_po', 'moved_by', 'notes']
        widgets = {
            'movement_number': forms.TextInput(attrs={'class': 'form-control'}),
            'movement_type': forms.Select(attrs={'class': 'form-select'}),
            'spare_part': forms.Select(attrs={'class': 'form-select'}),
            'source_warehouse': forms.Select(attrs={'class': 'form-select'}),
            'destination_warehouse': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'total_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'reference_workorder': forms.Select(attrs={'class': 'form-select'}),
            'reference_po': forms.TextInput(attrs={'class': 'form-control'}),
            'moved_by': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PurchaseRequisitionForm(forms.ModelForm):
    class Meta:
        model = PurchaseRequisition
        fields = ['pr_number', 'title', 'requesting_department', 'warehouse_destination', 'approver', 'status', 'priority', 'delivery_due_date', 'justification']
        widgets = {
            'pr_number': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'requesting_department': forms.Select(attrs={'class': 'form-select'}),
            'warehouse_destination': forms.Select(attrs={'class': 'form-select'}),
            'approver': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'delivery_due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'justification': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PurchaseRequisitionItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseRequisitionItem
        fields = ['spare_part', 'quantity', 'estimated_unit_cost', 'fulfilled_quantity', 'remarks']
        widgets = {
            'spare_part': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'estimated_unit_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fulfilled_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control'}),
        }
