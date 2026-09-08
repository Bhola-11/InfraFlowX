"""
RESTful JSON API Views for Inventory
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from apps.inventory.models import SparePart
from apps.inventory.serializers import InventorySerializer


@require_GET
def api_inventory_list(request):
    """
    JSON API endpoint returning list of SparePart records.
    """
    qs = SparePart.objects.all()[:100]
    data = []
    for item in qs:
        if hasattr(InventorySerializer, 'to_dict'):
            data.append(InventorySerializer.to_dict(item))
        elif hasattr(InventorySerializer, 'spare_part_to_dict'):
            data.append(InventorySerializer.spare_part_to_dict(item))
        elif hasattr(InventorySerializer, 'kpi_to_dict'):
            data.append(InventorySerializer.kpi_to_dict(item))
            
    return JsonResponse({'status': 'success', 'count': len(data), 'results': data})


@require_GET
def api_inventory_detail(request, pk):
    """
    JSON API endpoint returning single SparePart record.
    """
    try:
        item = SparePart.objects.get(pk=pk)
        if hasattr(InventorySerializer, 'to_dict'):
            d = InventorySerializer.to_dict(item)
        elif hasattr(InventorySerializer, 'spare_part_to_dict'):
            d = InventorySerializer.spare_part_to_dict(item)
        elif hasattr(InventorySerializer, 'kpi_to_dict'):
            d = InventorySerializer.kpi_to_dict(item)
        return JsonResponse({'status': 'success', 'data': d})
    except SparePart.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'SparePart not found'}, status=404)
