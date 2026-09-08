"""
Inventory Services
"""
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from apps.inventory.models import Warehouse, SparePart, StockItem, StockMovementLedger, PurchaseRequisition
from apps.inventory.supply_chain import SupplyChainEngine
from apps.audit.utils import log_audit_event


class InventoryService:
    @staticmethod
    @transaction.atomic
    def issue_stock(warehouse_id, spare_part_id, quantity, work_order=None, user=None, notes=""):
        stock = StockItem.objects.select_for_update().get(warehouse_id=warehouse_id, spare_part_id=spare_part_id)
        if stock.quantity_on_hand < quantity:
            raise ValueError(f"Insufficient stock on hand ({stock.quantity_on_hand}) for requested quantity ({quantity})")
            
        stock.quantity_on_hand -= quantity
        stock.save(update_fields=['quantity_on_hand'])
        
        mov = StockMovementLedger.objects.create(
            movement_number=f"ISS-{timezone.now().strftime('%Y%m%d%H%M%S')}",
            movement_type='OUTWARD',
            spare_part_id=spare_part_id,
            source_warehouse_id=warehouse_id,
            quantity=quantity,
            unit_price=stock.spare_part.unit_cost,
            total_cost=Decimal(quantity) * stock.spare_part.unit_cost,
            reference_workorder=work_order,
            moved_by=user,
            notes=notes
        )
        
        log_audit_event(
            action='UPDATE',
            module='inventory',
            object_id=str(mov.id),
            object_repr=str(mov),
            description=f"Issued {quantity} {stock.spare_part.unit_of_measure} of {stock.spare_part.name}",
            user=user
        )
        return mov
