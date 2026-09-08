from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q, Sum, Count

from .models import WorkOrder, WorkOrderTask
from .forms import WorkOrderForm, WorkOrderTaskForm
from apps.permissions.decorators import permission_required
from apps.audit.utils import log_audit_event

@login_required
def workorder_list_view(request):
    """
    Field work orders listing with priority, status, and contractor filtering.
    """
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')

    workorders_qs = WorkOrder.objects.select_related(
        'asset', 'location', 'assigned_employee__user', 'contractor'
    ).annotate(task_count=Count('tasks'))

    if query:
        workorders_qs = workorders_qs.filter(
            Q(workorder_id__icontains=query) |
            Q(title__icontains=query) |
            Q(asset__name__icontains=query) |
            Q(assigned_employee__user__first_name__icontains=query)
        )
    if status_filter:
        workorders_qs = workorders_qs.filter(status=status_filter)
    if priority_filter:
        workorders_qs = workorders_qs.filter(priority=priority_filter)

    total_est = workorders_qs.aggregate(total=Sum('estimated_cost'))['total'] or 0
    total_act = workorders_qs.aggregate(total=Sum('actual_cost'))['total'] or 0

    paginator = Paginator(workorders_qs, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'statuses': WorkOrder.STATUS_CHOICES,
        'priorities': WorkOrder.PRIORITY_CHOICES,
        'total_orders': workorders_qs.count(),
        'total_est': total_est,
        'total_act': total_act,
        'open_orders': workorders_qs.filter(status__in=['CREATED', 'ASSIGNED', 'SCHEDULED', 'IN_PROGRESS']).count(),
    }
    return render(request, 'workorders/workorder_list.html', context)


@login_required
def workorder_detail_view(request, pk):
    """
    Work order detail page with task checklist, actual cost tracking and sign-off.
    """
    work_order = get_object_or_404(
        WorkOrder.objects.select_related('asset', 'location', 'assigned_employee__user', 'contractor', 'asset__organization'),
        pk=pk
    )
    tasks = work_order.tasks.all()

    context = {
        'work_order': work_order,
        'tasks': tasks,
    }
    return render(request, 'workorders/workorder_detail.html', context)


@login_required
@permission_required('workorders', 'create')
def workorder_create_view(request):
    if request.method == 'POST':
        form = WorkOrderForm(request.POST)
        if form.is_valid():
            wo = form.save()
            log_audit_event(
                action='CREATE',
                module='workorders',
                object_id=wo.pk,
                object_repr=f"{wo.workorder_id} ({wo.title})",
                description=f"Created work order {wo.workorder_id} for {wo.asset.name}",
                request=request
            )
            messages.success(request, f"Work order '{wo.workorder_id}' created successfully.")
            return redirect('workorders:detail', pk=wo.pk)
    else:
        form = WorkOrderForm()
    return render(request, 'workorders/workorder_form.html', {'form': form, 'title': 'Create Work Order'})


@login_required
@permission_required('workorders', 'edit')
def workorder_update_view(request, pk):
    work_order = get_object_or_404(WorkOrder, pk=pk)
    if request.method == 'POST':
        form = WorkOrderForm(request.POST, instance=work_order)
        if form.is_valid():
            wo = form.save()
            log_audit_event(
                action='UPDATE',
                module='workorders',
                object_id=wo.pk,
                object_repr=wo.workorder_id,
                description=f"Updated work order {wo.workorder_id}",
                request=request
            )
            messages.success(request, f"Work order '{wo.workorder_id}' updated.")
            return redirect('workorders:detail', pk=wo.pk)
    else:
        form = WorkOrderForm(instance=work_order)
    return render(request, 'workorders/workorder_form.html', {'form': form, 'title': f'Edit Work Order: {work_order.workorder_id}', 'work_order': work_order})


@login_required
@permission_required('workorders', 'edit')
def workorder_status_update_view(request, pk, new_status):
    work_order = get_object_or_404(WorkOrder, pk=pk)
    work_order.status = new_status
    if new_status == 'COMPLETED':
        work_order.completion_date = timezone.now().date()
    work_order.save(update_fields=['status', 'completion_date'])

    log_audit_event(
        action='UPDATE',
        module='workorders',
        object_id=work_order.pk,
        object_repr=work_order.workorder_id,
        description=f"Transitioned work order {work_order.workorder_id} to {new_status}",
        request=request
    )
    messages.success(request, f"Work order status updated to {work_order.get_status_display()}.")
    return redirect('workorders:detail', pk=work_order.pk)


@login_required
@permission_required('workorders', 'create')
def workorder_add_task_view(request, wo_pk):
    work_order = get_object_or_404(WorkOrder, pk=wo_pk)
    if request.method == 'POST':
        form = WorkOrderTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.work_order = work_order
            task.save()
            messages.success(request, f"Task '{task.task_title}' added to work order.")
            return redirect('workorders:detail', pk=work_order.pk)
    else:
        form = WorkOrderTaskForm()
    return render(request, 'workorders/generic_form.html', {'form': form, 'title': f'Add Task to Work Order {work_order.workorder_id}'})
