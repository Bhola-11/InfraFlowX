"""
RESTful JSON API Views for Roads
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from apps.roads.models import Road
from apps.roads.serializers import RoadSerializer


@require_GET
def api_roads_list(request):
    """
    JSON API endpoint returning list of Road records.
    """
    qs = Road.objects.all()[:100]
    data = []
    for item in qs:
        if hasattr(RoadSerializer, 'to_dict'):
            data.append(RoadSerializer.to_dict(item))
        elif hasattr(RoadSerializer, 'spare_part_to_dict'):
            data.append(RoadSerializer.spare_part_to_dict(item))
        elif hasattr(RoadSerializer, 'kpi_to_dict'):
            data.append(RoadSerializer.kpi_to_dict(item))
            
    return JsonResponse({'status': 'success', 'count': len(data), 'results': data})


@require_GET
def api_roads_detail(request, pk):
    """
    JSON API endpoint returning single Road record.
    """
    try:
        item = Road.objects.get(pk=pk)
        if hasattr(RoadSerializer, 'to_dict'):
            d = RoadSerializer.to_dict(item)
        elif hasattr(RoadSerializer, 'spare_part_to_dict'):
            d = RoadSerializer.spare_part_to_dict(item)
        elif hasattr(RoadSerializer, 'kpi_to_dict'):
            d = RoadSerializer.kpi_to_dict(item)
        return JsonResponse({'status': 'success', 'data': d})
    except Road.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Road not found'}, status=404)
