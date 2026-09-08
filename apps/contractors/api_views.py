"""
RESTful JSON API Views for Contractors
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from apps.contractors.models import Contractor
from apps.contractors.serializers import ContractorSerializer


@require_GET
def api_contractors_list(request):
    """
    JSON API endpoint returning list of Contractor records.
    """
    qs = Contractor.objects.all()[:100]
    data = []
    for item in qs:
        if hasattr(ContractorSerializer, 'to_dict'):
            data.append(ContractorSerializer.to_dict(item))
        elif hasattr(ContractorSerializer, 'spare_part_to_dict'):
            data.append(ContractorSerializer.spare_part_to_dict(item))
        elif hasattr(ContractorSerializer, 'kpi_to_dict'):
            data.append(ContractorSerializer.kpi_to_dict(item))
            
    return JsonResponse({'status': 'success', 'count': len(data), 'results': data})


@require_GET
def api_contractors_detail(request, pk):
    """
    JSON API endpoint returning single Contractor record.
    """
    try:
        item = Contractor.objects.get(pk=pk)
        if hasattr(ContractorSerializer, 'to_dict'):
            d = ContractorSerializer.to_dict(item)
        elif hasattr(ContractorSerializer, 'spare_part_to_dict'):
            d = ContractorSerializer.spare_part_to_dict(item)
        elif hasattr(ContractorSerializer, 'kpi_to_dict'):
            d = ContractorSerializer.kpi_to_dict(item)
        return JsonResponse({'status': 'success', 'data': d})
    except Contractor.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Contractor not found'}, status=404)
