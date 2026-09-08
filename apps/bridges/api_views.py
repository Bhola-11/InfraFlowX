"""
RESTful JSON API Views for Bridges
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from apps.bridges.models import Bridge
from apps.bridges.serializers import BridgeSerializer


@require_GET
def api_bridges_list(request):
    """
    JSON API endpoint returning list of Bridge records.
    """
    qs = Bridge.objects.all()[:100]
    data = []
    for item in qs:
        if hasattr(BridgeSerializer, 'to_dict'):
            data.append(BridgeSerializer.to_dict(item))
        elif hasattr(BridgeSerializer, 'spare_part_to_dict'):
            data.append(BridgeSerializer.spare_part_to_dict(item))
        elif hasattr(BridgeSerializer, 'kpi_to_dict'):
            data.append(BridgeSerializer.kpi_to_dict(item))
            
    return JsonResponse({'status': 'success', 'count': len(data), 'results': data})


@require_GET
def api_bridges_detail(request, pk):
    """
    JSON API endpoint returning single Bridge record.
    """
    try:
        item = Bridge.objects.get(pk=pk)
        if hasattr(BridgeSerializer, 'to_dict'):
            d = BridgeSerializer.to_dict(item)
        elif hasattr(BridgeSerializer, 'spare_part_to_dict'):
            d = BridgeSerializer.spare_part_to_dict(item)
        elif hasattr(BridgeSerializer, 'kpi_to_dict'):
            d = BridgeSerializer.kpi_to_dict(item)
        return JsonResponse({'status': 'success', 'data': d})
    except Bridge.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Bridge not found'}, status=404)
