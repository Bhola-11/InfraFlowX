"""
RESTful JSON API Views for Incidents
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from apps.incidents.models import Incident
from apps.incidents.serializers import IncidentSerializer


@require_GET
def api_incidents_list(request):
    """
    JSON API endpoint returning list of Incident records.
    """
    qs = Incident.objects.all()[:100]
    data = []
    for item in qs:
        if hasattr(IncidentSerializer, 'to_dict'):
            data.append(IncidentSerializer.to_dict(item))
        elif hasattr(IncidentSerializer, 'spare_part_to_dict'):
            data.append(IncidentSerializer.spare_part_to_dict(item))
        elif hasattr(IncidentSerializer, 'kpi_to_dict'):
            data.append(IncidentSerializer.kpi_to_dict(item))
            
    return JsonResponse({'status': 'success', 'count': len(data), 'results': data})


@require_GET
def api_incidents_detail(request, pk):
    """
    JSON API endpoint returning single Incident record.
    """
    try:
        item = Incident.objects.get(pk=pk)
        if hasattr(IncidentSerializer, 'to_dict'):
            d = IncidentSerializer.to_dict(item)
        elif hasattr(IncidentSerializer, 'spare_part_to_dict'):
            d = IncidentSerializer.spare_part_to_dict(item)
        elif hasattr(IncidentSerializer, 'kpi_to_dict'):
            d = IncidentSerializer.kpi_to_dict(item)
        return JsonResponse({'status': 'success', 'data': d})
    except Incident.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Incident not found'}, status=404)
