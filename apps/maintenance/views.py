from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q, Sum, Count

from .models import MaintenancePlan, MaintenanceActionLog
from .forms import MaintenancePlanForm, MaintenanceActionLogForm
from apps.permissions.decorators import permission_required
from apps.audit.utils import log_audit_event

@login_required
def maintenance_list_view(request):
    """
    Maintenance plan operations directory with type, priority, and status filtering.
    """
    query = request.GET.get('q', '').strip()
    type_filter = request.GET.get('type', '')
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')

    plans_qs = MaintenancePlan.objects.select_related(
        'asset', 'assigned_team', 'contractor', 'asset__organization'
    ).all()

    if query:
        plans_qs = plans_qs.filter(
            Q(maintenance_code__icontains=query) |
            Q(title__icontains=query) |
            Q(asset__name__icontains=query) |
            Q(asset__asset_id__icontains=query)
        )
    if type_filter:
        plans_qs = plans_qs.filter(maintenance_type=type_filter)
    if status_filter:
        plans_qs = plans_qs.filter(status=status_filter)
    if priority_filter:
        plans_qs = plans_qs.filter(priority=priority_filter)

    total_cost = plans_qs.aggregate(total=Sum('cost'))['total'] or 0

    paginator = Paginator(plans_qs, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'query': query,
        'type_filter': type_filter,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'maintenance_types': MaintenancePlan.MAINTENANCE_TYPES,
        'statuses': MaintenancePlan.STATUS_CHOICES,
        'priorities': MaintenancePlan.PRIORITY_CHOICES,
        'total_jobs': plans_qs.count(),
        'total_cost': total_cost,
        'active_jobs': plans_qs.filter(status='IN_PROGRESS').count(),
    }
    return render(request, 'maintenance/plan_list.html', context)


@login_required
def maintenance_detail_view(request, pk):
    """
    Maintenance job detail dossier, SOP execution steps, and action logs.
    """
    plan = get_object_or_404(
        MaintenancePlan.objects.select_related('asset', 'assigned_team', 'contractor', 'asset__organization', 'asset__location'),
        pk=pk
    )
    action_logs = plan.action_logs.select_related('technician').all()

    context = {
        'plan': plan,
        'action_logs': action_logs,
    }
    return render(request, 'maintenance/plan_detail.html', context)


@login_required
@permission_required('maintenance', 'create')
def maintenance_create_view(request):
    if request.method == 'POST':
        form = MaintenancePlanForm(request.POST)
        if form.is_valid():
            plan = form.save()
            log_audit_event(
                action='CREATE',
                module='maintenance',
                object_id=plan.pk,
                object_repr=f"{plan.maintenance_code} ({plan.title})",
                description=f"Created {plan.get_maintenance_type_display()} plan for {plan.asset.name}",
                request=request
            )
            messages.success(request, f"Maintenance job '{plan.maintenance_code}' registered.")
            return redirect('maintenance:detail', pk=plan.pk)
    else:
        form = MaintenancePlanForm()
    return render(request, 'maintenance/plan_form.html', {'form': form, 'title': 'Create Maintenance Job'})


@login_required
@permission_required('maintenance', 'edit')
def maintenance_update_view(request, pk):
    plan = get_object_or_404(MaintenancePlan, pk=pk)
    if request.method == 'POST':
        form = MaintenancePlanForm(request.POST, instance=plan)
        if form.is_valid():
            plan = form.save()
            log_audit_event(
                action='UPDATE',
                module='maintenance',
                object_id=plan.pk,
                object_repr=plan.maintenance_code,
                description=f"Updated maintenance plan {plan.maintenance_code}",
                request=request
            )
            messages.success(request, f"Maintenance job '{plan.maintenance_code}' updated.")
            return redirect('maintenance:detail', pk=plan.pk)
    else:
        form = MaintenancePlanForm(instance=plan)
    return render(request, 'maintenance/plan_form.html', {'form': form, 'title': f'Edit Maintenance: {plan.maintenance_code}', 'plan': plan})


@login_required
@permission_required('maintenance', 'create')
def maintenance_action_log_add_view(request, plan_pk):
    plan = get_object_or_404(MaintenancePlan, pk=plan_pk)
    if request.method == 'POST':
        form = MaintenanceActionLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.maintenance_plan = plan
            log.technician = request.user
            log.save()
            messages.success(request, f"Action step '{log.step_description}' logged.")
            return redirect('maintenance:detail', pk=plan.pk)
    else:
        form = MaintenanceActionLogForm()
    return render(request, 'maintenance/action_form.html', {'form': form, 'title': f'Log Task Step for {plan.maintenance_code}'})


@login_required
@permission_required('maintenance', 'edit')
def maintenance_complete_view(request, pk):
    plan = get_object_or_404(MaintenancePlan, pk=pk)
    plan.status = 'COMPLETED'
    plan.completion_date = timezone.now().date()
    plan.save(update_fields=['status', 'completion_date'])
    
    # Restore asset operational status if under maintenance
    if plan.asset.status == 'UNDER_MAINTENANCE':
        plan.asset.status = 'ACTIVE'
        plan.asset.save(update_fields=['status'])

    log_audit_event(
        action='MAINTENANCE_ACTION',
        module='maintenance',
        object_id=plan.pk,
        object_repr=plan.maintenance_code,
        description=f"Completed and commissioned maintenance job {plan.maintenance_code}",
        request=request
    )
    messages.success(request, f"Maintenance job '{plan.maintenance_code}' marked as Completed.")
    return redirect('maintenance:detail', pk=plan.pk)
