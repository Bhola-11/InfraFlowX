from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import AuditLog

@login_required
def audit_log_list(request):
    """
    Enterprise audit logs viewer with filtering by module, user, action, date range, and keyword search.
    """
    query = request.GET.get('q', '').strip()
    action_filter = request.GET.get('action', '')
    module_filter = request.GET.get('module', '')
    user_filter = request.GET.get('user', '')
    
    logs = AuditLog.objects.select_related('user').all()

    if query:
        logs = logs.filter(
            Q(object_repr__icontains=query) |
            Q(description__icontains=query) |
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        )
    if action_filter:
        logs = logs.filter(action=action_filter)
    if module_filter:
        logs = logs.filter(module__iexact=module_filter)
    if user_filter:
        logs = logs.filter(user_id=user_filter)

    # Distinct modules for filter dropdown
    modules = AuditLog.objects.values_list('module', flat=True).distinct()

    paginator = Paginator(logs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'action_filter': action_filter,
        'module_filter': module_filter,
        'action_choices': AuditLog.ACTION_CHOICES,
        'modules': sorted(list(set(modules))),
        'total_logs_count': logs.count(),
    }
    return render(request, 'audit/log_list.html', context)
