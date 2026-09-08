"""
RESTful JSON API Views for Projects
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from apps.projects.models import Project
from apps.projects.serializers import ProjectSerializer


@require_GET
def api_projects_list(request):
    """
    JSON API endpoint returning list of Project records.
    """
    qs = Project.objects.all()[:100]
    data = []
    for item in qs:
        if hasattr(ProjectSerializer, 'to_dict'):
            data.append(ProjectSerializer.to_dict(item))
        elif hasattr(ProjectSerializer, 'spare_part_to_dict'):
            data.append(ProjectSerializer.spare_part_to_dict(item))
        elif hasattr(ProjectSerializer, 'kpi_to_dict'):
            data.append(ProjectSerializer.kpi_to_dict(item))
            
    return JsonResponse({'status': 'success', 'count': len(data), 'results': data})


@require_GET
def api_projects_detail(request, pk):
    """
    JSON API endpoint returning single Project record.
    """
    try:
        item = Project.objects.get(pk=pk)
        if hasattr(ProjectSerializer, 'to_dict'):
            d = ProjectSerializer.to_dict(item)
        elif hasattr(ProjectSerializer, 'spare_part_to_dict'):
            d = ProjectSerializer.spare_part_to_dict(item)
        elif hasattr(ProjectSerializer, 'kpi_to_dict'):
            d = ProjectSerializer.kpi_to_dict(item)
        return JsonResponse({'status': 'success', 'data': d})
    except Project.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Project not found'}, status=404)
