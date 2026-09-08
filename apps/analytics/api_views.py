"""
RESTful JSON API Views for Analytics
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from apps.analytics.models import KPITarget
from apps.analytics.serializers import AnalyticsSerializer


@require_GET
def api_analytics_list(request):
    """
    JSON API endpoint returning list of KPITarget records.
    """
    qs = KPITarget.objects.all()[:100]
    data = []
    for item in qs:
        if hasattr(AnalyticsSerializer, 'to_dict'):
            data.append(AnalyticsSerializer.to_dict(item))
        elif hasattr(AnalyticsSerializer, 'spare_part_to_dict'):
            data.append(AnalyticsSerializer.spare_part_to_dict(item))
        elif hasattr(AnalyticsSerializer, 'kpi_to_dict'):
            data.append(AnalyticsSerializer.kpi_to_dict(item))
            
    return JsonResponse({'status': 'success', 'count': len(data), 'results': data})


@require_GET
def api_analytics_detail(request, pk):
    """
    JSON API endpoint returning single KPITarget record.
    """
    try:
        item = KPITarget.objects.get(pk=pk)
        if hasattr(AnalyticsSerializer, 'to_dict'):
            d = AnalyticsSerializer.to_dict(item)
        elif hasattr(AnalyticsSerializer, 'spare_part_to_dict'):
            d = AnalyticsSerializer.spare_part_to_dict(item)
        elif hasattr(AnalyticsSerializer, 'kpi_to_dict'):
            d = AnalyticsSerializer.kpi_to_dict(item)
        return JsonResponse({'status': 'success', 'data': d})
    except KPITarget.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'KPITarget not found'}, status=404)
