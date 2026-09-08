import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings
from apps.organizations.models import Organization, Department
from apps.locations.models import Location
from apps.workorders.models import WorkOrder


class Warehouse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='warehouses')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='warehouses')
    address = models.TextField(blank=True, null=True)
    capacity_sqm = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_warehouses')
    contact_phone = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def total_stock_items_count(self):
        return self.stock_items.count()

    @property
    def total_inventory_valuation(self):
        return sum(item.valuation for item in self.stock_items.all())


class InventoryCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Inventory Category'
        verbose_name_plural = 'Inventory Categories'

    def __str__(self):
        return f"{self.name} ({self.code})"


class SparePart(models.Model):
    UNIT_CHOICES = [
        ('PCS', 'Pieces'),
        ('BOX', 'Box'),
        ('KG', 'Kilogram'),
        ('MTR', 'Meters'),
        ('LTR', 'Liters'),
        ('SET', 'Set'),
        ('TON', 'Tons'),
        ('ROLL', 'Rolls'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    part_number = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(InventoryCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='spare_parts')
    description = models.TextField(blank=True, null=True)
    unit_of_measure = models.CharField(max_length=20, choices=UNIT_CHOICES, default='PCS')
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    minimum_reorder_level = models.PositiveIntegerField(default=10)
    maximum_stock_level = models.PositiveIntegerField(default=500)
    lead_time_days = models.PositiveIntegerField(default=7, help_text="Supplier turnaround time in days")
    manufacturer = models.CharField(max_length=200, blank=True, null=True)
    barcode = models.CharField(max_length=100, blank=True, null=True, unique=True)
    is_hazardous = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Spare Part / Material'
        verbose_name_plural = 'Spare Parts & Materials'

    def __str__(self):
        return f"{self.part_number} - {self.name}"

    @property
    def total_quantity_on_hand(self):
        return sum(item.quantity_on_hand for item in self.stock_entries.all())

    @property
    def is_low_stock(self):
        return self.total_quantity_on_hand <= self.minimum_reorder_level


class StockItem(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('RESERVED', 'Reserved'),
        ('OUT_OF_STOCK', 'Out of Stock'),
        ('EXPIRED_DAMAGED', 'Damaged / Expired'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_items')
    spare_part = models.ForeignKey(SparePart, on_delete=models.CASCADE, related_name='stock_entries')
    quantity_on_hand = models.PositiveIntegerField(default=0)
    quantity_reserved = models.PositiveIntegerField(default=0)
    aisle_bin_location = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. Aisle 3, Rack B, Bin 12")
    last_stocktake_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='AVAILABLE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('warehouse', 'spare_part')
        ordering = ['warehouse', 'spare_part']
        verbose_name = 'Stock Item'
        verbose_name_plural = 'Stock Items'

    def __str__(self):
        return f"{self.spare_part.name} @ {self.warehouse.name} ({self.quantity_on_hand} {self.spare_part.unit_of_measure})"

    @property
    def quantity_available(self):
        return max(0, self.quantity_on_hand - self.quantity_reserved)

    @property
    def valuation(self):
        return Decimal(self.quantity_on_hand) * self.spare_part.unit_cost


class StockMovementLedger(models.Model):
    MOVEMENT_TYPES = [
        ('INWARD', 'Goods Inward / Purchase Receipt'),
        ('OUTWARD', 'Goods Issue / Consumption'),
        ('TRANSFER', 'Inter-Warehouse Transfer'),
        ('ADJUSTMENT', 'Stock Adjustment / Audit Write-off'),
        ('RETURN', 'Return to Supplier / Return from Job'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movement_number = models.CharField(max_length=60, unique=True)
    movement_type = models.CharField(max_length=30, choices=MOVEMENT_TYPES)
    spare_part = models.ForeignKey(SparePart, on_delete=models.CASCADE, related_name='movements')
    source_warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True, related_name='outward_movements')
    destination_warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True, related_name='inward_movements')
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_cost = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    reference_workorder = models.ForeignKey(WorkOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='material_issues')
    reference_po = models.CharField(max_length=100, blank=True, null=True, help_text="Purchase Order or Dispatch Doc #")
    moved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='stock_movements')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Stock Movement Ledger'
        verbose_name_plural = 'Stock Movement Ledgers'

    def __str__(self):
        return f"{self.movement_number} - {self.get_movement_type_display()} ({self.quantity} {self.spare_part.unit_of_measure})"

    def save(self, *args, **kwargs):
        if not self.total_cost:
            self.total_cost = Decimal(self.quantity) * self.unit_price
        super().save(*args, **kwargs)


class PurchaseRequisition(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted for Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('ORDERED', 'PO Issued / Ordered'),
        ('RECEIVED', 'Goods Received & Closed'),
        ('CANCELLED', 'Cancelled'),
    ]
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('EMERGENCY', 'Emergency / Critical'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pr_number = models.CharField(max_length=60, unique=True)
    title = models.CharField(max_length=255)
    requesting_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='purchase_requisitions')
    warehouse_destination = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True, related_name='requisitions')
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submitted_prs')
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_prs')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='DRAFT')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    total_estimated_cost = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    justification = models.TextField(blank=True, null=True)
    delivery_due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Purchase Requisition'
        verbose_name_plural = 'Purchase Requisitions'

    def __str__(self):
        return f"{self.pr_number} - {self.title} [{self.get_status_display()}]"

    def recalculate_total(self):
        self.total_estimated_cost = sum(item.total_amount for item in self.items.all())
        self.save(update_fields=['total_estimated_cost'])


class PurchaseRequisitionItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requisition = models.ForeignKey(PurchaseRequisition, on_delete=models.CASCADE, related_name='items')
    spare_part = models.ForeignKey(SparePart, on_delete=models.CASCADE, related_name='pr_items')
    quantity = models.PositiveIntegerField(default=1)
    estimated_unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    fulfilled_quantity = models.PositiveIntegerField(default=0)
    remarks = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Requisition Item'
        verbose_name_plural = 'Requisition Items'

    def save(self, *args, **kwargs):
        self.total_amount = Decimal(self.quantity) * self.estimated_unit_cost
        super().save(*args, **kwargs)
        self.requisition.recalculate_total()
