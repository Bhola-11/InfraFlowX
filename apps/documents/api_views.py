"""
RESTful JSON API Views for Documents
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from apps.documents.models import Document
from apps.documents.serializers import DocumentSerializer


@require_GET
def api_documents_list(request):
    """
    JSON API endpoint returning list of Document records.
    """
    qs = Document.objects.all()[:100]
    data = []
    for item in qs:
        if hasattr(DocumentSerializer, 'to_dict'):
            data.append(DocumentSerializer.to_dict(item))
        elif hasattr(DocumentSerializer, 'spare_part_to_dict'):
            data.append(DocumentSerializer.spare_part_to_dict(item))
        elif hasattr(DocumentSerializer, 'kpi_to_dict'):
            data.append(DocumentSerializer.kpi_to_dict(item))
            
    return JsonResponse({'status': 'success', 'count': len(data), 'results': data})


@require_GET
def api_documents_detail(request, pk):
    """
    JSON API endpoint returning single Document record.
    """
    try:
        item = Document.objects.get(pk=pk)
        if hasattr(DocumentSerializer, 'to_dict'):
            d = DocumentSerializer.to_dict(item)
        elif hasattr(DocumentSerializer, 'spare_part_to_dict'):
            d = DocumentSerializer.spare_part_to_dict(item)
        elif hasattr(DocumentSerializer, 'kpi_to_dict'):
            d = DocumentSerializer.kpi_to_dict(item)
        return JsonResponse({'status': 'success', 'data': d})
    except Document.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Document not found'}, status=404)
