import json
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import AssetSchedule, ScheduledEventExecution
from .forms import AssetScheduleForm, ScheduledEventExecutionForm
from apps.audit.utils import log_audit_event


@login_required
def schedule_list_view(request):
    schedules = AssetSchedule.objects.select_related('asset', 'organization', 'assigned_team', 'assigned_contractor').all()
    q = request.GET.get('q', '').strip()
    s_type = request.GET.get('type', '').strip()
    freq = request.GET.get('frequency', '').strip()

    if q:
        schedules = schedules.filter(Q(title__icontains=q) | Q(schedule_code__icontains=q) | Q(asset__name__icontains=q))
    if s_type:
        schedules = schedules.filter(schedule_type=s_type)
    if freq:
        schedules = schedules.filter(frequency=freq)

    paginator = Paginator(schedules, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'schedules/schedule_list.html', {
        'page_obj': page_obj,
        'types': AssetSchedule.SCHEDULE_TYPES,
        'frequencies': AssetSchedule.FREQUENCY_CHOICES,
        'search_query': q,
        'selected_type': s_type,
        'selected_freq': freq,
    })


@login_required
def schedule_detail_view(request, pk):
    schedule = get_object_or_404(AssetSchedule.objects.select_related('asset', 'organization', 'department', 'assigned_team', 'assigned_contractor'), pk=pk)
    executions = schedule.executions.select_related('assigned_to', 'work_order', 'inspection').all()[:20]

    return render(request, 'schedules/schedule_detail.html', {
        'schedule': schedule,
        'executions': executions,
    })


@login_required
def schedule_create_view(request):
    if request.method == 'POST':
        form = AssetScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save()
            log_audit_event(request.user, 'CREATE', 'AssetSchedule', str(schedule.id), f"Created schedule {schedule.title}")
            messages.success(request, f"Schedule '{schedule.title}' created.")
            return redirect('schedules:schedule_detail', pk=schedule.id)
    else:
        init_code = f"SCH-{timezone.now().strftime('%Y%m%d%H%M')}"
        form = AssetScheduleForm(initial={'schedule_code': init_code, 'next_due_date': timezone.now().date() + timedelta(days=30), 'start_date': timezone.now().date()})
    return render(request, 'schedules/schedule_form.html', {'form': form, 'title': 'Create Infrastructure Maintenance Schedule'})


@login_required
def schedule_update_view(request, pk):
    schedule = get_object_or_404(AssetSchedule, pk=pk)
    if request.method == 'POST':
        form = AssetScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            schedule = form.save()
            log_audit_event(request.user, 'UPDATE', 'AssetSchedule', str(schedule.id), f"Updated schedule {schedule.title}")
            messages.success(request, f"Schedule '{schedule.title}' updated.")
            return redirect('schedules:schedule_detail', pk=schedule.id)
    else:
        form = AssetScheduleForm(instance=schedule)
    return render(request, 'schedules/schedule_form.html', {'form': form, 'title': f'Edit Schedule - {schedule.title}', 'schedule': schedule})


@login_required
def schedule_calendar_view(request):
    schedules = AssetSchedule.objects.filter(is_active=True).select_related('asset')
    events = []
    for s in schedules:
        events.append({
            'title': f"[{s.get_schedule_type_display()}] {s.title} ({s.asset.name})",
            'start': s.next_due_date.strftime('%Y-%m-%d'),
            'url': f"/schedules/{s.id}/",
            'className': 'badge bg-primary' if not s.is_overdue else 'badge bg-danger',
        })
    return render(request, 'schedules/calendar.html', {
        'events_json': json.dumps(events),
        'schedules_count': schedules.count()
    })


@login_required
def execution_update_view(request, pk):
    execution = get_object_or_404(ScheduledEventExecution, pk=pk)
    if request.method == 'POST':
        form = ScheduledEventExecutionForm(request.POST, instance=execution)
        if form.is_valid():
            exec_obj = form.save()
            log_audit_event(request.user, 'UPDATE', 'ScheduledEventExecution', str(exec_obj.id), f"Updated execution status to {exec_obj.status}")
            messages.success(request, f"Execution record updated.")
            return redirect('schedules:schedule_detail', pk=exec_obj.schedule.id)
    else:
        form = ScheduledEventExecutionForm(instance=execution)
    return render(request, 'schedules/execution_form.html', {'form': form, 'execution': execution})
