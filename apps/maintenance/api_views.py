"""
RESTful JSON API Views for Maintenance
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from apps.maintenance.models import MaintenancePlan
from apps.maintenance.serializers import MaintenanceSerializer


@require_GET
def api_maintenance_list(request):
    """
    JSON API endpoint returning list of MaintenancePlan records.
    """
    qs = MaintenancePlan.objects.all()[:100]
    data = []
    for item in qs:
        if hasattr(MaintenanceSerializer, 'to_dict'):
            data.append(MaintenanceSerializer.to_dict(item))
        elif hasattr(MaintenanceSerializer, 'spare_part_to_dict'):
            data.append(MaintenanceSerializer.spare_part_to_dict(item))
        elif hasattr(MaintenanceSerializer, 'kpi_to_dict'):
            data.append(MaintenanceSerializer.kpi_to_dict(item))
            
    return JsonResponse({'status': 'success', 'count': len(data), 'results': data})


@require_GET
def api_maintenance_detail(request, pk):
    """
    JSON API endpoint returning single MaintenancePlan record.
    """
    try:
        item = MaintenancePlan.objects.get(pk=pk)
        if hasattr(MaintenanceSerializer, 'to_dict'):
            d = MaintenanceSerializer.to_dict(item)
        elif hasattr(MaintenanceSerializer, 'spare_part_to_dict'):
            d = MaintenanceSerializer.spare_part_to_dict(item)
        elif hasattr(MaintenanceSerializer, 'kpi_to_dict'):
            d = MaintenanceSerializer.kpi_to_dict(item)
        return JsonResponse({'status': 'success', 'data': d})
    except MaintenancePlan.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'MaintenancePlan not found'}, status=404)
