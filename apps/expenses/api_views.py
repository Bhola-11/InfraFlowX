"""
RESTful JSON API Views for Expenses
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from apps.expenses.models import Expense
from apps.expenses.serializers import ExpenseSerializer


@require_GET
def api_expenses_list(request):
    """
    JSON API endpoint returning list of Expense records.
    """
    qs = Expense.objects.all()[:100]
    data = []
    for item in qs:
        if hasattr(ExpenseSerializer, 'to_dict'):
            data.append(ExpenseSerializer.to_dict(item))
        elif hasattr(ExpenseSerializer, 'spare_part_to_dict'):
            data.append(ExpenseSerializer.spare_part_to_dict(item))
        elif hasattr(ExpenseSerializer, 'kpi_to_dict'):
            data.append(ExpenseSerializer.kpi_to_dict(item))
            
    return JsonResponse({'status': 'success', 'count': len(data), 'results': data})


@require_GET
def api_expenses_detail(request, pk):
    """
    JSON API endpoint returning single Expense record.
    """
    try:
        item = Expense.objects.get(pk=pk)
        if hasattr(ExpenseSerializer, 'to_dict'):
            d = ExpenseSerializer.to_dict(item)
        elif hasattr(ExpenseSerializer, 'spare_part_to_dict'):
            d = ExpenseSerializer.spare_part_to_dict(item)
        elif hasattr(ExpenseSerializer, 'kpi_to_dict'):
            d = ExpenseSerializer.kpi_to_dict(item)
        return JsonResponse({'status': 'success', 'data': d})
    except Expense.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Expense not found'}, status=404)
