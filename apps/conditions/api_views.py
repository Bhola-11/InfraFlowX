"""
RESTful JSON API Views for Conditions
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from apps.conditions.models import ConditionLog
from apps.conditions.serializers import ConditionSerializer


@require_GET
def api_conditions_list(request):
    """
    JSON API endpoint returning list of ConditionLog records.
    """
    qs = ConditionLog.objects.all()[:100]
    data = []
    for item in qs:
        if hasattr(ConditionSerializer, 'to_dict'):
            data.append(ConditionSerializer.to_dict(item))
        elif hasattr(ConditionSerializer, 'spare_part_to_dict'):
            data.append(ConditionSerializer.spare_part_to_dict(item))
        elif hasattr(ConditionSerializer, 'kpi_to_dict'):
            data.append(ConditionSerializer.kpi_to_dict(item))
            
    return JsonResponse({'status': 'success', 'count': len(data), 'results': data})


@require_GET
def api_conditions_detail(request, pk):
    """
    JSON API endpoint returning single ConditionLog record.
    """
    try:
        item = ConditionLog.objects.get(pk=pk)
        if hasattr(ConditionSerializer, 'to_dict'):
            d = ConditionSerializer.to_dict(item)
        elif hasattr(ConditionSerializer, 'spare_part_to_dict'):
            d = ConditionSerializer.spare_part_to_dict(item)
        elif hasattr(ConditionSerializer, 'kpi_to_dict'):
            d = ConditionSerializer.kpi_to_dict(item)
        return JsonResponse({'status': 'success', 'data': d})
    except ConditionLog.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'ConditionLog not found'}, status=404)
