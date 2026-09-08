"""
RESTful JSON API Views for Buildings
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from apps.buildings.models import Building
from apps.buildings.serializers import BuildingSerializer


@require_GET
def api_buildings_list(request):
    """
    JSON API endpoint returning list of Building records.
    """
    qs = Building.objects.all()[:100]
    data = []
    for item in qs:
        if hasattr(BuildingSerializer, 'to_dict'):
            data.append(BuildingSerializer.to_dict(item))
        elif hasattr(BuildingSerializer, 'spare_part_to_dict'):
            data.append(BuildingSerializer.spare_part_to_dict(item))
        elif hasattr(BuildingSerializer, 'kpi_to_dict'):
            data.append(BuildingSerializer.kpi_to_dict(item))
            
    return JsonResponse({'status': 'success', 'count': len(data), 'results': data})


@require_GET
def api_buildings_detail(request, pk):
    """
    JSON API endpoint returning single Building record.
    """
    try:
        item = Building.objects.get(pk=pk)
        if hasattr(BuildingSerializer, 'to_dict'):
            d = BuildingSerializer.to_dict(item)
        elif hasattr(BuildingSerializer, 'spare_part_to_dict'):
            d = BuildingSerializer.spare_part_to_dict(item)
        elif hasattr(BuildingSerializer, 'kpi_to_dict'):
            d = BuildingSerializer.kpi_to_dict(item)
        return JsonResponse({'status': 'success', 'data': d})
    except Building.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Building not found'}, status=404)
