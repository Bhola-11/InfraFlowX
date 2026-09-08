from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count

from .models import Building, BuildingFloor
from .forms import BuildingForm, BuildingFloorForm
from apps.permissions.decorators import permission_required
from apps.audit.utils import log_audit_event

@login_required
def building_list_view(request):
    """
    Municipal building and facilities registry list.
    """
    query = request.GET.get('q', '').strip()
    type_filter = request.GET.get('type', '')
    energy_filter = request.GET.get('energy', '')

    buildings_qs = Building.objects.select_related('asset', 'asset__organization', 'asset__location').annotate(
        floor_levels_count=Count('floors')
    )

    if query:
        buildings_qs = buildings_qs.filter(
            Q(building_id_code__icontains=query) |
            Q(building_name__icontains=query) |
            Q(address__icontains=query)
        )
    if type_filter:
        buildings_qs = buildings_qs.filter(building_type=type_filter)
    if energy_filter:
        buildings_qs = buildings_qs.filter(energy_rating=energy_filter)

    total_sqft = buildings_qs.aggregate(total=Sum('total_area_sqft'))['total'] or 0

    paginator = Paginator(buildings_qs, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'query': query,
        'type_filter': type_filter,
        'energy_filter': energy_filter,
        'building_types': Building.BUILDING_TYPES,
        'energy_ratings': Building.ENERGY_RATINGS,
        'total_buildings': buildings_qs.count(),
        'total_sqft': total_sqft,
    }
    return render(request, 'buildings/building_list.html', context)


@login_required
def building_detail_view(request, pk):
    """
    Building structural profile, floor plan breakdown, HVAC and energy metrics.
    """
    building = get_object_or_404(Building.objects.select_related('asset', 'asset__organization', 'asset__location'), pk=pk)
    floors = building.floors.all()

    context = {
        'building': building,
        'floors': floors,
    }
    return render(request, 'buildings/building_detail.html', context)


@login_required
@permission_required('buildings', 'create')
def building_create_view(request):
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            bld = form.save()
            log_audit_event(
                action='CREATE',
                module='buildings',
                object_id=bld.pk,
                object_repr=f"{bld.building_id_code} ({bld.building_name})",
                description=f"Registered municipal building {bld.building_name}",
                request=request
            )
            messages.success(request, f"Building '{bld.building_name}' registered successfully.")
            return redirect('buildings:detail', pk=bld.pk)
    else:
        form = BuildingForm()
    return render(request, 'buildings/building_form.html', {'form': form, 'title': 'Register Building Facility'})


@login_required
@permission_required('buildings', 'edit')
def building_update_view(request, pk):
    bld = get_object_or_404(Building, pk=pk)
    if request.method == 'POST':
        form = BuildingForm(request.POST, instance=bld)
        if form.is_valid():
            bld = form.save()
            log_audit_event(
                action='UPDATE',
                module='buildings',
                object_id=bld.pk,
                object_repr=f"{bld.building_id_code}",
                description=f"Updated parameters for building {bld.building_id_code}",
                request=request
            )
            messages.success(request, f"Building '{bld.building_name}' updated successfully.")
            return redirect('buildings:detail', pk=bld.pk)
    else:
        form = BuildingForm(instance=bld)
    return render(request, 'buildings/building_form.html', {'form': form, 'title': f'Edit Building: {bld.building_name}', 'building': bld})


@login_required
@permission_required('buildings', 'create')
def building_floor_create_view(request, building_pk):
    building = get_object_or_404(Building, pk=building_pk)
    if request.method == 'POST':
        form = BuildingFloorForm(request.POST)
        if form.is_valid():
            floor = form.save(commit=False)
            floor.building = building
            floor.save()
            messages.success(request, f"Floor level '{floor.floor_name}' added.")
            return redirect('buildings:detail', pk=building.pk)
    else:
        form = BuildingFloorForm(initial={'building': building})
    return render(request, 'buildings/generic_form.html', {'form': form, 'title': f'Add Floor Level for {building.building_name}'})
