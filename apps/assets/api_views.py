"""
RESTful JSON API Views for Assets
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from apps.assets.models import Asset
from apps.assets.serializers import AssetSerializer


@require_GET
def api_assets_list(request):
    """
    JSON API endpoint returning list of Asset records.
    """
    qs = Asset.objects.all()[:100]
    data = []
    for item in qs:
        if hasattr(AssetSerializer, 'to_dict'):
            data.append(AssetSerializer.to_dict(item))
        elif hasattr(AssetSerializer, 'spare_part_to_dict'):
            data.append(AssetSerializer.spare_part_to_dict(item))
        elif hasattr(AssetSerializer, 'kpi_to_dict'):
            data.append(AssetSerializer.kpi_to_dict(item))
            
    return JsonResponse({'status': 'success', 'count': len(data), 'results': data})


@require_GET
def api_assets_detail(request, pk):
    """
    JSON API endpoint returning single Asset record.
    """
    try:
        item = Asset.objects.get(pk=pk)
        if hasattr(AssetSerializer, 'to_dict'):
            d = AssetSerializer.to_dict(item)
        elif hasattr(AssetSerializer, 'spare_part_to_dict'):
            d = AssetSerializer.spare_part_to_dict(item)
        elif hasattr(AssetSerializer, 'kpi_to_dict'):
            d = AssetSerializer.kpi_to_dict(item)
        return JsonResponse({'status': 'success', 'data': d})
    except Asset.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Asset not found'}, status=404)
