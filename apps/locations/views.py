from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q, Count

from .models import Location
from .forms import LocationForm
from apps.permissions.decorators import permission_required
from apps.audit.utils import log_audit_event

@login_required
def location_list_view(request):
    """
    List of registered geospatial infrastructure locations.
    """
    query = request.GET.get('q', '').strip()
    city_filter = request.GET.get('city', '')
    
    locations_qs = Location.objects.select_related('organization').annotate(
        asset_count=Count('assets', distinct=True)
    )

    if query:
        locations_qs = locations_qs.filter(
            Q(name__icontains=query) |
            Q(code__icontains=query) |
            Q(city__icontains=query) |
            Q(address__icontains=query)
        )
    if city_filter:
        locations_qs = locations_qs.filter(city__iexact=city_filter)

    cities = Location.objects.values_list('city', flat=True).distinct()

    paginator = Paginator(locations_qs, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'query': query,
        'city_filter': city_filter,
        'cities': sorted(list(set(cities))),
        'total_locations': locations_qs.count(),
    }
    return render(request, 'locations/location_list.html', context)


@login_required
def location_detail_view(request, pk):
    """
    Location detailed view with GPS mapping, coordinates, and associated infrastructure assets.
    """
    location = get_object_or_404(Location.objects.select_related('organization'), pk=pk)
    assets = location.assets.select_related('organization').all()[:20]

    context = {
        'location': location,
        'assets': assets,
    }
    return render(request, 'locations/location_detail.html', context)


@login_required
def gis_map_view(request):
    """
    Interactive enterprise GIS-style Map visualization powered by Leaflet.js.
    Displays all geographic infrastructure assets, roads, bridges, and buildings with condition status markers.
    """
    locations = Location.objects.select_related('organization').prefetch_related('assets').all()
    context = {
        'locations_count': locations.count(),
    }
    return render(request, 'locations/gis_map.html', context)


@login_required
def geojson_api_view(request):
    """
    GeoJSON API endpoint streaming infrastructure coordinate points, asset types, and condition states for GIS mapping.
    """
    locations = Location.objects.select_related('organization').prefetch_related('assets').all()
    features = []

    for loc in locations:
        assets_list = []
        for a in loc.assets.all():
            assets_list.append({
                'id': str(a.id),
                'name': a.name,
                'asset_id': a.asset_id,
                'asset_type': a.get_asset_type_display(),
                'condition_score': a.condition_score,
                'status': a.get_status_display(),
            })

        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [float(loc.longitude), float(loc.latitude)]
            },
            'properties': {
                'id': str(loc.id),
                'name': loc.name,
                'code': loc.code,
                'city': loc.city,
                'state': loc.state,
                'address': loc.address,
                'assets_count': len(assets_list),
                'assets': assets_list,
                'url': f"/locations/{loc.id}/"
            }
        }
        features.append(feature)

    return JsonResponse({
        'type': 'FeatureCollection',
        'features': features
    })


@login_required
@permission_required('locations', 'create')
def location_create_view(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            loc = form.save()
            log_audit_event(
                action='CREATE',
                module='locations',
                object_id=loc.pk,
                object_repr=f"{loc.name} ({loc.code})",
                description=f"Created geospatial location site {loc.name}",
                request=request
            )
            messages.success(request, f"Location '{loc.name}' registered.")
            return redirect('locations:detail', pk=loc.pk)
    else:
        form = LocationForm()
    return render(request, 'locations/location_form.html', {'form': form, 'title': 'Register Geospatial Location'})


@login_required
@permission_required('locations', 'edit')
def location_update_view(request, pk):
    loc = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=loc)
        if form.is_valid():
            loc = form.save()
            log_audit_event(
                action='UPDATE',
                module='locations',
                object_id=loc.pk,
                object_repr=f"{loc.name} ({loc.code})",
                description=f"Updated geospatial coordinates for location {loc.name}",
                request=request
            )
            messages.success(request, f"Location '{loc.name}' updated.")
            return redirect('locations:detail', pk=loc.pk)
    else:
        form = LocationForm(instance=loc)
    return render(request, 'locations/location_form.html', {'form': form, 'title': f'Edit Location: {loc.name}', 'location': loc})
