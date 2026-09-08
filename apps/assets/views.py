from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum, Avg

from .models import Asset, AssetCategory, AssetStatusHistory
from .forms import AssetForm, AssetCategoryForm, AssetStatusChangeForm
from apps.organizations.models import Organization, Department
from apps.locations.models import Location
from apps.permissions.decorators import permission_required
from apps.audit.utils import log_audit_event

@login_required
def asset_list_view(request):
    """
    Central Asset Registry directory with multi-faceted filtering.
    """
    query = request.GET.get('q', '').strip()
    type_filter = request.GET.get('type', '')
    status_filter = request.GET.get('status', '')
    condition_filter = request.GET.get('condition', '')
    org_filter = request.GET.get('org', '')

    assets_qs = Asset.objects.select_related(
        'organization', 'location', 'department', 'owner', 'category'
    ).all()

    if query:
        assets_qs = assets_qs.filter(
            Q(asset_id__icontains=query) |
            Q(name__icontains=query) |
            Q(serial_number__icontains=query) |
            Q(barcode__icontains=query) |
            Q(location__name__icontains=query) |
            Q(location__city__icontains=query)
        )
    if type_filter:
        assets_qs = assets_qs.filter(asset_type=type_filter)
    if status_filter:
        assets_qs = assets_qs.filter(status=status_filter)
    if condition_filter:
        assets_qs = assets_qs.filter(condition=condition_filter)
    if org_filter:
        assets_qs = assets_qs.filter(organization_id=org_filter)

    # Aggregates for KPI ribbon
    total_count = assets_qs.count()
    total_val = assets_qs.aggregate(total=Sum('current_value'))['total'] or 0
    avg_score = assets_qs.aggregate(avg=Avg('condition_score'))['avg'] or 0
    critical_count = assets_qs.filter(condition='CRITICAL').count()

    paginator = Paginator(assets_qs, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'query': query,
        'type_filter': type_filter,
        'status_filter': status_filter,
        'condition_filter': condition_filter,
        'org_filter': org_filter,
        'asset_types': Asset.ASSET_TYPES,
        'statuses': Asset.STATUS_CHOICES,
        'conditions': Asset.CONDITION_CHOICES,
        'organizations': Organization.objects.filter(is_active=True),
        'total_count': total_count,
        'total_val': total_val,
        'avg_score': round(avg_score, 1),
        'critical_count': critical_count,
    }
    return render(request, 'assets/asset_list.html', context)


@login_required
def asset_detail_view(request, pk):
    """
    360-degree Central Asset Detail View.
    Integrates geospatial location, road/bridge/building/facility extensions,
    inspection logs, maintenance records, workorders, expenses, documents, and incidents.
    """
    asset = get_object_or_404(
        Asset.objects.select_related('organization', 'location', 'department', 'owner', 'category'),
        pk=pk
    )

    # Related operational entities via real ORM relations
    status_history = asset.status_history.select_related('changed_by').all()[:10]
    
    # Subtype-specific extension lookups if available
    road_extension = getattr(asset, 'road_extension', None) if hasattr(asset, 'road_extension') else None
    bridge_extension = getattr(asset, 'bridge_extension', None) if hasattr(asset, 'bridge_extension') else None
    building_extension = getattr(asset, 'building_extension', None) if hasattr(asset, 'building_extension') else None
    facility_extension = getattr(asset, 'facility_extension', None) if hasattr(asset, 'facility_extension') else None

    # Operational modules connected to this asset
    inspections = asset.inspections.select_related('inspector').all()[:10] if hasattr(asset, 'inspections') else []
    condition_logs = asset.condition_logs.all()[:10] if hasattr(asset, 'condition_logs') else []
    maintenance_records = asset.maintenance_records.all()[:10] if hasattr(asset, 'maintenance_records') else []
    work_orders = asset.work_orders.select_related('contractor', 'assigned_employee').all()[:10] if hasattr(asset, 'work_orders') else []
    expenses = asset.expenses.all()[:10] if hasattr(asset, 'expenses') else []
    incidents = asset.incidents.all()[:10] if hasattr(asset, 'incidents') else []
    documents = asset.documents.all()[:10] if hasattr(asset, 'documents') else []

    status_form = AssetStatusChangeForm(initial={'new_status': asset.status})

    context = {
        'asset': asset,
        'status_history': status_history,
        'road_extension': road_extension,
        'bridge_extension': bridge_extension,
        'building_extension': building_extension,
        'facility_extension': facility_extension,
        'inspections': inspections,
        'condition_logs': condition_logs,
        'maintenance_records': maintenance_records,
        'work_orders': work_orders,
        'expenses': expenses,
        'incidents': incidents,
        'documents': documents,
        'status_form': status_form,
    }
    return render(request, 'assets/asset_detail.html', context)


@login_required
@permission_required('assets', 'create')
def asset_create_view(request):
    """
    Register a new infrastructure asset in the central registry.
    """
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            asset = form.save()
            log_audit_event(
                action='CREATE',
                module='assets',
                object_id=asset.pk,
                object_repr=f"{asset.name} ({asset.asset_id})",
                description=f"Registered infrastructure asset {asset.name} [{asset.get_asset_type_display()}]",
                request=request
            )
            messages.success(request, f"Asset '{asset.name}' [{asset.asset_id}] created successfully.")
            return redirect('assets:detail', pk=asset.pk)
    else:
        form = AssetForm()

    return render(request, 'assets/asset_form.html', {'form': form, 'title': 'Register Infrastructure Asset'})


@login_required
@permission_required('assets', 'edit')
def asset_update_view(request, pk):
    """
    Update asset technical parameters, valuations, or specifications.
    """
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES, instance=asset)
        if form.is_valid():
            asset = form.save()
            log_audit_event(
                action='UPDATE',
                module='assets',
                object_id=asset.pk,
                object_repr=f"{asset.name} ({asset.asset_id})",
                description=f"Updated technical parameters for asset {asset.asset_id}",
                request=request
            )
            messages.success(request, f"Asset '{asset.name}' updated successfully.")
            return redirect('assets:detail', pk=asset.pk)
    else:
        form = AssetForm(instance=asset)

    return render(request, 'assets/asset_form.html', {'form': form, 'title': f'Edit Asset: {asset.name}', 'asset': asset})


@login_required
@permission_required('assets', 'edit')
def asset_status_change_view(request, pk):
    """
    Transition asset operational status with reason audit record.
    """
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        form = AssetStatusChangeForm(request.POST)
        if form.is_valid():
            prev = asset.status
            new_st = form.cleaned_data['new_status']
            reason = form.cleaned_data['reason']

            asset.status = new_st
            asset.save(update_fields=['status'])

            AssetStatusHistory.objects.create(
                asset=asset,
                previous_status=prev,
                new_status=new_st,
                changed_by=request.user,
                reason=reason
            )

            log_audit_event(
                action='ASSET_CHANGE',
                module='assets',
                object_id=asset.pk,
                object_repr=f"{asset.name} ({asset.asset_id})",
                description=f"Status transition from {prev} to {new_st}. Reason: {reason}",
                request=request
            )
            messages.success(request, f"Asset status updated to {asset.get_status_display()}.")
    return redirect('assets:detail', pk=asset.pk)


@login_required
def asset_category_list_view(request):
    categories = AssetCategory.objects.annotate(asset_count=Count('assets'))
    return render(request, 'assets/category_list.html', {'categories': categories})


@login_required
@permission_required('assets', 'create')
def asset_category_create_view(request):
    if request.method == 'POST':
        form = AssetCategoryForm(request.POST)
        if form.is_valid():
            cat = form.save()
            messages.success(request, f"Asset category '{cat.name}' created.")
            return redirect('assets:category_list')
    else:
        form = AssetCategoryForm()
    return render(request, 'assets/generic_form.html', {'form': form, 'title': 'Create Asset Category'})
