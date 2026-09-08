from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q, Avg, Count

from .models import ConditionLog, DeteriorationModel
from .forms import ConditionLogForm, DeteriorationModelForm
from apps.assets.models import Asset
from apps.permissions.decorators import permission_required
from apps.audit.utils import log_audit_event

@login_required
def condition_list_view(request):
    """
    Overview of asset condition assessments, degradation alerts, and critical ratings.
    """
    query = request.GET.get('q', '').strip()
    cat_filter = request.GET.get('category', '')

    logs_qs = ConditionLog.objects.select_related('asset', 'assessor', 'asset__organization').all()

    if query:
        logs_qs = logs_qs.filter(
            Q(asset__name__icontains=query) |
            Q(asset__asset_id__icontains=query) |
            Q(notes__icontains=query)
        )
    if cat_filter:
        logs_qs = logs_qs.filter(condition_category=cat_filter)

    avg_score = logs_qs.aggregate(avg=Avg('condition_score'))['avg'] or 0

    paginator = Paginator(logs_qs, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'query': query,
        'cat_filter': cat_filter,
        'categories': ConditionLog.CATEGORY_CHOICES,
        'total_logs': logs_qs.count(),
        'avg_score': round(avg_score, 1),
        'critical_count': logs_qs.filter(condition_category='CRITICAL').count(),
    }
    return render(request, 'conditions/condition_list.html', context)


@login_required
@permission_required('conditions', 'create')
def condition_log_create_view(request):
    """
    Record a new physical condition assessment.
    """
    if request.method == 'POST':
        form = ConditionLogForm(request.POST)
        if form.is_valid():
            log = form.save()
            # Update parent asset condition and score
            asset = log.asset
            asset.condition_score = log.condition_score
            asset.condition = log.condition_category
            asset.save(update_fields=['condition_score', 'condition'])

            log_audit_event(
                action='UPDATE',
                module='conditions',
                object_id=log.pk,
                object_repr=f"{asset.name} ({log.condition_score}/100)",
                description=f"Logged condition score {log.condition_score} ({log.get_condition_category_display()}) for {asset.name}",
                request=request
            )
            messages.success(request, f"Condition score recorded for '{asset.name}'.")
            return redirect('conditions:list')
    else:
        form = ConditionLogForm()

    return render(request, 'conditions/condition_form.html', {'form': form, 'title': 'Record Condition Assessment'})


@login_required
def deterioration_curves_view(request):
    """
    Interactive degradation curves and predictive deterioration modeling based on asset design life.
    """
    models_list = DeteriorationModel.objects.all()
    return render(request, 'conditions/deterioration_curves.html', {'models_list': models_list})
