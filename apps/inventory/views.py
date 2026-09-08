import uuid
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, F
from django.utils import timezone
from .models import Warehouse, InventoryCategory, SparePart, StockItem, StockMovementLedger, PurchaseRequisition, PurchaseRequisitionItem
from .forms import WarehouseForm, InventoryCategoryForm, SparePartForm, StockItemForm, StockMovementLedgerForm, PurchaseRequisitionForm, PurchaseRequisitionItemForm
from apps.audit.utils import log_audit_event


# ---------------- Warehouses ----------------
@login_required
def warehouse_list_view(request):
    warehouses = Warehouse.objects.select_related('organization', 'location', 'manager').all()
    q = request.GET.get('q', '').strip()
    if q:
        warehouses = warehouses.filter(Q(name__icontains=q) | Q(code__icontains=q) | Q(address__icontains=q))

    paginator = Paginator(warehouses, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'inventory/warehouse_list.html', {
        'page_obj': page_obj,
        'search_query': q,
        'total_warehouses': warehouses.count()
    })


@login_required
def warehouse_detail_view(request, pk):
    warehouse = get_object_or_404(Warehouse.objects.select_related('organization', 'location', 'manager'), pk=pk)
    stock_items = warehouse.stock_items.select_related('spare_part').all()
    recent_inward = warehouse.inward_movements.select_related('spare_part', 'moved_by')[:10]
    recent_outward = warehouse.outward_movements.select_related('spare_part', 'moved_by')[:10]

    return render(request, 'inventory/warehouse_detail.html', {
        'warehouse': warehouse,
        'stock_items': stock_items,
        'recent_inward': recent_inward,
        'recent_outward': recent_outward,
    })


@login_required
def warehouse_create_view(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            wh = form.save()
            log_audit_event(request.user, 'CREATE', 'Warehouse', str(wh.id), f"Created warehouse {wh.name}")
            messages.success(request, f"Warehouse '{wh.name}' created successfully.")
            return redirect('inventory:warehouse_detail', pk=wh.id)
    else:
        form = WarehouseForm()
    return render(request, 'inventory/warehouse_form.html', {'form': form, 'title': 'Create New Warehouse'})


@login_required
def warehouse_update_view(request, pk):
    wh = get_object_or_404(Warehouse, pk=pk)
    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=wh)
        if form.is_valid():
            wh = form.save()
            log_audit_event(request.user, 'UPDATE', 'Warehouse', str(wh.id), f"Updated warehouse {wh.name}")
            messages.success(request, f"Warehouse '{wh.name}' updated successfully.")
            return redirect('inventory:warehouse_detail', pk=wh.id)
    else:
        form = WarehouseForm(instance=wh)
    return render(request, 'inventory/warehouse_form.html', {'form': form, 'title': f'Update Warehouse - {wh.name}', 'warehouse': wh})


# ---------------- Spare Parts ----------------
@login_required
def sparepart_list_view(request):
    parts = SparePart.objects.select_related('category').prefetch_related('stock_entries').all()
    q = request.GET.get('q', '').strip()
    cat_id = request.GET.get('category', '').strip()
    low_stock = request.GET.get('low_stock', '').strip()

    if q:
        parts = parts.filter(Q(name__icontains=q) | Q(part_number__icontains=q) | Q(manufacturer__icontains=q))
    if cat_id:
        parts = parts.filter(category_id=cat_id)

    paginator = Paginator(parts, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    categories = InventoryCategory.objects.all()

    return render(request, 'inventory/sparepart_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': q,
        'selected_category': cat_id,
        'low_stock_filter': low_stock,
    })


@login_required
def sparepart_detail_view(request, pk):
    part = get_object_or_404(SparePart.objects.select_related('category'), pk=pk)
    stock_locations = part.stock_entries.select_related('warehouse').all()
    movements = part.movements.select_related('source_warehouse', 'destination_warehouse', 'moved_by', 'reference_workorder')[:20]

    return render(request, 'inventory/sparepart_detail.html', {
        'part': part,
        'stock_locations': stock_locations,
        'movements': movements,
    })


@login_required
def sparepart_create_view(request):
    if request.method == 'POST':
        form = SparePartForm(request.POST)
        if form.is_valid():
            part = form.save()
            log_audit_event(request.user, 'CREATE', 'SparePart', str(part.id), f"Registered spare part {part.name} ({part.part_number})")
            messages.success(request, f"Spare part '{part.name}' created.")
            return redirect('inventory:sparepart_detail', pk=part.id)
    else:
        form = SparePartForm()
    return render(request, 'inventory/sparepart_form.html', {'form': form, 'title': 'Register New Spare Part / Material'})


@login_required
def sparepart_update_view(request, pk):
    part = get_object_or_404(SparePart, pk=pk)
    if request.method == 'POST':
        form = SparePartForm(request.POST, instance=part)
        if form.is_valid():
            part = form.save()
            log_audit_event(request.user, 'UPDATE', 'SparePart', str(part.id), f"Updated spare part {part.name}")
            messages.success(request, f"Spare part '{part.name}' updated.")
            return redirect('inventory:sparepart_detail', pk=part.id)
    else:
        form = SparePartForm(instance=part)
    return render(request, 'inventory/sparepart_form.html', {'form': form, 'title': f'Edit Spare Part - {part.name}', 'part': part})


# ---------------- Stock Movement Ledgers ----------------
@login_required
def stock_movement_list_view(request):
    movements = StockMovementLedger.objects.select_related('spare_part', 'source_warehouse', 'destination_warehouse', 'moved_by', 'reference_workorder').all()
    m_type = request.GET.get('movement_type', '').strip()
    if m_type:
        movements = movements.filter(movement_type=m_type)

    paginator = Paginator(movements, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'inventory/movement_list.html', {
        'page_obj': page_obj,
        'selected_type': m_type,
        'movement_types': StockMovementLedger.MOVEMENT_TYPES
    })


@login_required
def stock_movement_create_view(request):
    if request.method == 'POST':
        form = StockMovementLedgerForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            if not movement.moved_by:
                movement.moved_by = request.user
            if not movement.movement_number:
                movement.movement_number = f"MOV-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            movement.save()

            # Update stock balances
            if movement.movement_type == 'INWARD' and movement.destination_warehouse:
                stock, _ = StockItem.objects.get_or_create(warehouse=movement.destination_warehouse, spare_part=movement.spare_part)
                stock.quantity_on_hand += movement.quantity
                stock.save()
            elif movement.movement_type == 'OUTWARD' and movement.source_warehouse:
                stock = StockItem.objects.filter(warehouse=movement.source_warehouse, spare_part=movement.spare_part).first()
                if stock and stock.quantity_on_hand >= movement.quantity:
                    stock.quantity_on_hand -= movement.quantity
                    stock.save()
            elif movement.movement_type == 'TRANSFER' and movement.source_warehouse and movement.destination_warehouse:
                src_stock = StockItem.objects.filter(warehouse=movement.source_warehouse, spare_part=movement.spare_part).first()
                if src_stock and src_stock.quantity_on_hand >= movement.quantity:
                    src_stock.quantity_on_hand -= movement.quantity
                    src_stock.save()
                    dst_stock, _ = StockItem.objects.get_or_create(warehouse=movement.destination_warehouse, spare_part=movement.spare_part)
                    dst_stock.quantity_on_hand += movement.quantity
                    dst_stock.save()

            log_audit_event(request.user, 'CREATE', 'StockMovementLedger', str(movement.id), f"Recorded stock movement {movement.movement_number}")
            messages.success(request, f"Stock movement '{movement.movement_number}' recorded successfully.")
            return redirect('inventory:movement_list')
    else:
        init_num = f"MOV-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        form = StockMovementLedgerForm(initial={'movement_number': init_num, 'moved_by': request.user})
    return render(request, 'inventory/movement_form.html', {'form': form, 'title': 'Record Stock Movement / Transaction'})


# ---------------- Purchase Requisitions ----------------
@login_required
def purchase_requisition_list_view(request):
    prs = PurchaseRequisition.objects.select_related('requesting_department', 'warehouse_destination', 'requested_by', 'approver').all()
    status = request.GET.get('status', '').strip()
    if status:
        prs = prs.filter(status=status)

    paginator = Paginator(prs, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'inventory/pr_list.html', {
        'page_obj': page_obj,
        'status_choices': PurchaseRequisition.STATUS_CHOICES,
        'selected_status': status,
    })


@login_required
def purchase_requisition_detail_view(request, pk):
    pr = get_object_or_404(PurchaseRequisition.objects.select_related('requesting_department', 'warehouse_destination', 'requested_by', 'approver'), pk=pk)
    items = pr.items.select_related('spare_part').all()
    item_form = PurchaseRequisitionItemForm()

    return render(request, 'inventory/pr_detail.html', {
        'pr': pr,
        'items': items,
        'item_form': item_form,
    })


@login_required
def purchase_requisition_create_view(request):
    if request.method == 'POST':
        form = PurchaseRequisitionForm(request.POST)
        if form.is_valid():
            pr = form.save(commit=False)
            pr.requested_by = request.user
            if not pr.pr_number:
                pr.pr_number = f"PR-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            pr.save()
            log_audit_event(request.user, 'CREATE', 'PurchaseRequisition', str(pr.id), f"Created PR {pr.pr_number}")
            messages.success(request, f"Purchase Requisition '{pr.pr_number}' initiated.")
            return redirect('inventory:pr_detail', pk=pr.id)
    else:
        init_num = f"PR-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        form = PurchaseRequisitionForm(initial={'pr_number': init_num, 'requested_by': request.user})
    return render(request, 'inventory/pr_form.html', {'form': form, 'title': 'Create Purchase Requisition'})


@login_required
def purchase_requisition_update_view(request, pk):
    pr = get_object_or_404(PurchaseRequisition, pk=pk)
    if request.method == 'POST':
        form = PurchaseRequisitionForm(request.POST, instance=pr)
        if form.is_valid():
            pr = form.save()
            log_audit_event(request.user, 'UPDATE', 'PurchaseRequisition', str(pr.id), f"Updated PR {pr.pr_number}")
            messages.success(request, f"PR '{pr.pr_number}' updated.")
            return redirect('inventory:pr_detail', pk=pr.id)
    else:
        form = PurchaseRequisitionForm(instance=pr)
    return render(request, 'inventory/pr_form.html', {'form': form, 'title': f'Edit Purchase Requisition - {pr.pr_number}', 'pr': pr})


@login_required
def purchase_requisition_item_create_view(request, pk):
    pr = get_object_or_404(PurchaseRequisition, pk=pk)
    if request.method == 'POST':
        form = PurchaseRequisitionItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.requisition = pr
            item.save()
            messages.success(request, f"Added {item.spare_part.name} to PR.")
    return redirect('inventory:pr_detail', pk=pr.id)


# ---------------- Categories ----------------
@login_required
def inventory_category_list_view(request):
    cats = InventoryCategory.objects.select_related('parent').all()
    form = InventoryCategoryForm()
    if request.method == 'POST':
        form = InventoryCategoryForm(request.POST)
        if form.is_valid():
            cat = form.save()
            log_audit_event(request.user, 'CREATE', 'InventoryCategory', str(cat.id), f"Created category {cat.name}")
            messages.success(request, f"Category '{cat.name}' created.")
            return redirect('inventory:category_list')
    return render(request, 'inventory/category_list.html', {'categories': cats, 'form': form})
