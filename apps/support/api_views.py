"""
RESTful JSON API Views for Support
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from apps.support.models import SupportTicket
from apps.support.serializers import SupportTicketSerializer


@require_GET
def api_support_list(request):
    """
    JSON API endpoint returning list of SupportTicket records.
    """
    qs = SupportTicket.objects.all()[:100]
    data = []
    for item in qs:
        if hasattr(SupportTicketSerializer, 'to_dict'):
            data.append(SupportTicketSerializer.to_dict(item))
        elif hasattr(SupportTicketSerializer, 'spare_part_to_dict'):
            data.append(SupportTicketSerializer.spare_part_to_dict(item))
        elif hasattr(SupportTicketSerializer, 'kpi_to_dict'):
            data.append(SupportTicketSerializer.kpi_to_dict(item))
            
    return JsonResponse({'status': 'success', 'count': len(data), 'results': data})


@require_GET
def api_support_detail(request, pk):
    """
    JSON API endpoint returning single SupportTicket record.
    """
    try:
        item = SupportTicket.objects.get(pk=pk)
        if hasattr(SupportTicketSerializer, 'to_dict'):
            d = SupportTicketSerializer.to_dict(item)
        elif hasattr(SupportTicketSerializer, 'spare_part_to_dict'):
            d = SupportTicketSerializer.spare_part_to_dict(item)
        elif hasattr(SupportTicketSerializer, 'kpi_to_dict'):
            d = SupportTicketSerializer.kpi_to_dict(item)
        return JsonResponse({'status': 'success', 'data': d})
    except SupportTicket.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'SupportTicket not found'}, status=404)
