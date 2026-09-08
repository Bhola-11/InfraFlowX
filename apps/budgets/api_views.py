"""
RESTful JSON API Views for Budgets
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from apps.budgets.models import Budget
from apps.budgets.serializers import BudgetSerializer


@require_GET
def api_budgets_list(request):
    """
    JSON API endpoint returning list of Budget records.
    """
    qs = Budget.objects.all()[:100]
    data = []
    for item in qs:
        if hasattr(BudgetSerializer, 'to_dict'):
            data.append(BudgetSerializer.to_dict(item))
        elif hasattr(BudgetSerializer, 'spare_part_to_dict'):
            data.append(BudgetSerializer.spare_part_to_dict(item))
        elif hasattr(BudgetSerializer, 'kpi_to_dict'):
            data.append(BudgetSerializer.kpi_to_dict(item))
            
    return JsonResponse({'status': 'success', 'count': len(data), 'results': data})


@require_GET
def api_budgets_detail(request, pk):
    """
    JSON API endpoint returning single Budget record.
    """
    try:
        item = Budget.objects.get(pk=pk)
        if hasattr(BudgetSerializer, 'to_dict'):
            d = BudgetSerializer.to_dict(item)
        elif hasattr(BudgetSerializer, 'spare_part_to_dict'):
            d = BudgetSerializer.spare_part_to_dict(item)
        elif hasattr(BudgetSerializer, 'kpi_to_dict'):
            d = BudgetSerializer.kpi_to_dict(item)
        return JsonResponse({'status': 'success', 'data': d})
    except Budget.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Budget not found'}, status=404)
