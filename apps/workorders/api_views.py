"""
RESTful JSON API Views for Workorders
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from apps.workorders.models import WorkOrder
from apps.workorders.serializers import WorkOrderSerializer


@require_GET
def api_workorders_list(request):
    """
    JSON API endpoint returning list of WorkOrder records.
    """
    qs = WorkOrder.objects.all()[:100]
    data = []
    for item in qs:
        if hasattr(WorkOrderSerializer, 'to_dict'):
            data.append(WorkOrderSerializer.to_dict(item))
        elif hasattr(WorkOrderSerializer, 'spare_part_to_dict'):
            data.append(WorkOrderSerializer.spare_part_to_dict(item))
        elif hasattr(WorkOrderSerializer, 'kpi_to_dict'):
            data.append(WorkOrderSerializer.kpi_to_dict(item))
            
    return JsonResponse({'status': 'success', 'count': len(data), 'results': data})


@require_GET
def api_workorders_detail(request, pk):
    """
    JSON API endpoint returning single WorkOrder record.
    """
    try:
        item = WorkOrder.objects.get(pk=pk)
        if hasattr(WorkOrderSerializer, 'to_dict'):
            d = WorkOrderSerializer.to_dict(item)
        elif hasattr(WorkOrderSerializer, 'spare_part_to_dict'):
            d = WorkOrderSerializer.spare_part_to_dict(item)
        elif hasattr(WorkOrderSerializer, 'kpi_to_dict'):
            d = WorkOrderSerializer.kpi_to_dict(item)
        return JsonResponse({'status': 'success', 'data': d})
    except WorkOrder.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'WorkOrder not found'}, status=404)
