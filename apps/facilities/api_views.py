"""
RESTful JSON API Views for Facilities
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from apps.facilities.models import FacilityEquipment
from apps.facilities.serializers import FacilitySerializer


@require_GET
def api_facilities_list(request):
    """
    JSON API endpoint returning list of FacilityEquipment records.
    """
    qs = FacilityEquipment.objects.all()[:100]
    data = []
    for item in qs:
        if hasattr(FacilitySerializer, 'to_dict'):
            data.append(FacilitySerializer.to_dict(item))
        elif hasattr(FacilitySerializer, 'spare_part_to_dict'):
            data.append(FacilitySerializer.spare_part_to_dict(item))
        elif hasattr(FacilitySerializer, 'kpi_to_dict'):
            data.append(FacilitySerializer.kpi_to_dict(item))
            
    return JsonResponse({'status': 'success', 'count': len(data), 'results': data})


@require_GET
def api_facilities_detail(request, pk):
    """
    JSON API endpoint returning single FacilityEquipment record.
    """
    try:
        item = FacilityEquipment.objects.get(pk=pk)
        if hasattr(FacilitySerializer, 'to_dict'):
            d = FacilitySerializer.to_dict(item)
        elif hasattr(FacilitySerializer, 'spare_part_to_dict'):
            d = FacilitySerializer.spare_part_to_dict(item)
        elif hasattr(FacilitySerializer, 'kpi_to_dict'):
            d = FacilitySerializer.kpi_to_dict(item)
        return JsonResponse({'status': 'success', 'data': d})
    except FacilityEquipment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'FacilityEquipment not found'}, status=404)
