"""
RESTful JSON API Views for Schedules
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from apps.schedules.models import AssetSchedule
from apps.schedules.serializers import ScheduleSerializer


@require_GET
def api_schedules_list(request):
    """
    JSON API endpoint returning list of AssetSchedule records.
    """
    qs = AssetSchedule.objects.all()[:100]
    data = []
    for item in qs:
        if hasattr(ScheduleSerializer, 'to_dict'):
            data.append(ScheduleSerializer.to_dict(item))
        elif hasattr(ScheduleSerializer, 'spare_part_to_dict'):
            data.append(ScheduleSerializer.spare_part_to_dict(item))
        elif hasattr(ScheduleSerializer, 'kpi_to_dict'):
            data.append(ScheduleSerializer.kpi_to_dict(item))
            
    return JsonResponse({'status': 'success', 'count': len(data), 'results': data})


@require_GET
def api_schedules_detail(request, pk):
    """
    JSON API endpoint returning single AssetSchedule record.
    """
    try:
        item = AssetSchedule.objects.get(pk=pk)
        if hasattr(ScheduleSerializer, 'to_dict'):
            d = ScheduleSerializer.to_dict(item)
        elif hasattr(ScheduleSerializer, 'spare_part_to_dict'):
            d = ScheduleSerializer.spare_part_to_dict(item)
        elif hasattr(ScheduleSerializer, 'kpi_to_dict'):
            d = ScheduleSerializer.kpi_to_dict(item)
        return JsonResponse({'status': 'success', 'data': d})
    except AssetSchedule.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'AssetSchedule not found'}, status=404)
