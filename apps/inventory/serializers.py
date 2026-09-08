"""
Inventory Serializers
"""
from apps.inventory.models import Warehouse, SparePart, StockItem


class InventorySerializer:
    @staticmethod
    def spare_part_to_dict(part):
        return {
            'id': str(part.id),
            'part_number': part.part_number,
            'name': part.name,
            'category': part.category.name if part.category else None,
            'unit_of_measure': part.unit_of_measure,
            'unit_cost': float(part.unit_cost),
            'minimum_reorder_level': part.minimum_reorder_level,
            'maximum_stock_level': part.maximum_stock_level,
            'lead_time_days': part.lead_time_days,
            'manufacturer': part.manufacturer,
            'total_quantity_on_hand': part.total_quantity_on_hand,
            'is_low_stock': part.is_low_stock,
        }
