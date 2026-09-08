from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Avg, Count

from .models import Road, RoadDefect, RoadRepairHistory
from .forms import RoadForm, RoadDefectForm
from apps.organizations.models import Region
from apps.permissions.decorators import permission_required
from apps.audit.utils import log_audit_event

@login_required
def road_list_view(request):
    """
    Road and Highway inventory directory with pavement condition scores and defect alerts.
    """
    query = request.GET.get('q', '').strip()
    surface_filter = request.GET.get('surface', '')
    traffic_filter = request.GET.get('traffic', '')
    region_filter = request.GET.get('region', '')

    roads_qs = Road.objects.select_related('asset', 'region').annotate(
        defect_count=Count('defects', filter=Q(defects__is_repaired=False))
    )

    if query:
        roads_qs = roads_qs.filter(
            Q(road_code__icontains=query) |
            Q(road_name__icontains=query) |
            Q(asset__name__icontains=query)
        )
    if surface_filter:
        roads_qs = roads_qs.filter(surface_type=surface_filter)
    if traffic_filter:
        roads_qs = roads_qs.filter(traffic_level=traffic_filter)
    if region_filter:
        roads_qs = roads_qs.filter(region_id=region_filter)

    total_km = roads_qs.aggregate(total=Sum('length_km'))['total'] or 0
    avg_pci = roads_qs.aggregate(avg=Avg('pci_score'))['avg'] or 0

    paginator = Paginator(roads_qs, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'query': query,
        'surface_filter': surface_filter,
        'traffic_filter': traffic_filter,
        'region_filter': region_filter,
        'surface_types': Road.SURFACE_TYPES,
        'traffic_levels': Road.TRAFFIC_LEVELS,
        'regions': Region.objects.all(),
        'total_roads': roads_qs.count(),
        'total_km': round(total_km, 2),
        'avg_pci': round(avg_pci, 1),
    }
    return render(request, 'roads/road_list.html', context)


@login_required
def road_detail_view(request, pk):
    """
    In-depth road engineering profile with defect log and pavement repair history.
    """
    road = get_object_or_404(Road.objects.select_related('asset', 'region', 'asset__location'), pk=pk)
    defects = road.defects.all()[:15]
    repairs = road.repairs.all()[:10]

    context = {
        'road': road,
        'defects': defects,
        'repairs': repairs,
    }
    return render(request, 'roads/road_detail.html', context)


@login_required
@permission_required('roads', 'create')
def road_create_view(request):
    if request.method == 'POST':
        form = RoadForm(request.POST)
        if form.is_valid():
            road = form.save()
            log_audit_event(
                action='CREATE',
                module='roads',
                object_id=road.pk,
                object_repr=f"{road.road_code} ({road.road_name})",
                description=f"Registered road segment {road.road_code}",
                request=request
            )
            messages.success(request, f"Road '{road.road_code}' registered successfully.")
            return redirect('roads:detail', pk=road.pk)
    else:
        form = RoadForm()
    return render(request, 'roads/road_form.html', {'form': form, 'title': 'Register Road Segment'})


@login_required
@permission_required('roads', 'edit')
def road_update_view(request, pk):
    road = get_object_or_404(Road, pk=pk)
    if request.method == 'POST':
        form = RoadForm(request.POST, instance=road)
        if form.is_valid():
            road = form.save()
            log_audit_event(
                action='UPDATE',
                module='roads',
                object_id=road.pk,
                object_repr=f"{road.road_code}",
                description=f"Updated road engineering specifications for {road.road_code}",
                request=request
            )
            messages.success(request, f"Road '{road.road_code}' updated successfully.")
            return redirect('roads:detail', pk=road.pk)
    else:
        form = RoadForm(instance=road)
    return render(request, 'roads/road_form.html', {'form': form, 'title': f'Edit Road: {road.road_code}', 'road': road})


@login_required
def road_defect_list_view(request):
    defects = RoadDefect.objects.select_related('road').filter(is_repaired=False)
    return render(request, 'roads/defect_list.html', {'defects': defects})


@login_required
@permission_required('roads', 'create')
def road_defect_create_view(request):
    if request.method == 'POST':
        form = RoadDefectForm(request.POST, request.FILES)
        if form.is_valid():
            defect = form.save()
            messages.success(request, f"Road defect recorded at KM {defect.chainage_km}.")
            return redirect('roads:detail', pk=defect.road.pk)
    else:
        form = RoadDefectForm()
    return render(request, 'roads/defect_form.html', {'form': form, 'title': 'Log Road Pavement Defect'})


@login_required
@permission_required('roads', 'edit')
def road_defect_resolve_view(request, pk):
    defect = get_object_or_404(RoadDefect, pk=pk)
    defect.is_repaired = True
    defect.save(update_fields=['is_repaired'])
    messages.success(request, "Road defect marked as repaired.")
    return redirect('roads:detail', pk=defect.road.pk)
