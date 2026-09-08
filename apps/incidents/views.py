from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q, Sum, Count

from .models import Incident, IncidentDispatchLog
from .forms import IncidentForm, IncidentDispatchForm, IncidentResolveForm
from apps.permissions.decorators import permission_required
from apps.audit.utils import log_audit_event
from apps.notifications.utils import broadcast_notification_to_role

@login_required
def incident_list_view(request):
    """
    Emergency incident response directory with severity and triage status filters.
    """
    query = request.GET.get('q', '').strip()
    sev_filter = request.GET.get('severity', '')
    status_filter = request.GET.get('status', '')

    incidents_qs = Incident.objects.select_related(
        'asset', 'location', 'reported_by', 'emergency_crew'
    ).all()

    if query:
        incidents_qs = incidents_qs.filter(
            Q(incident_id__icontains=query) |
            Q(title__icontains=query) |
            Q(asset__name__icontains=query) |
            Q(location__city__icontains=query)
        )
    if sev_filter:
        incidents_qs = incidents_qs.filter(severity=sev_filter)
    if status_filter:
        incidents_qs = incidents_qs.filter(status=status_filter)

    total_damage = incidents_qs.aggregate(total=Sum('estimated_damage_cost'))['total'] or 0

    paginator = Paginator(incidents_qs, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'query': query,
        'sev_filter': sev_filter,
        'status_filter': status_filter,
        'severities': Incident.SEVERITY_LEVELS,
        'statuses': Incident.STATUS_CHOICES,
        'total_incidents': incidents_qs.count(),
        'total_damage': total_damage,
        'active_emergencies': incidents_qs.filter(severity='CRITICAL', status__in=['REPORTED', 'DISPATCHED', 'UNDER_INVESTIGATION']).count(),
    }
    return render(request, 'incidents/incident_list.html', context)


@login_required
def incident_detail_view(request, pk):
    """
    Incident command dossier with timeline logs and Root Cause Analysis.
    """
    incident = get_object_or_404(
        Incident.objects.select_related('asset', 'location', 'reported_by', 'emergency_crew'),
        pk=pk
    )
    dispatch_logs = incident.dispatch_logs.all()

    context = {
        'incident': incident,
        'dispatch_logs': dispatch_logs,
    }
    return render(request, 'incidents/incident_detail.html', context)


@login_required
def incident_create_view(request):
    """
    Log an infrastructure emergency or safety incident ticket.
    """
    if request.method == 'POST':
        form = IncidentForm(request.POST, request.FILES)
        if form.is_valid():
            inc = form.save(commit=False)
            inc.reported_by = request.user
            inc.save()

            # If asset linked and critical, transition asset status to DAMAGED
            if inc.asset and inc.severity == 'CRITICAL':
                inc.asset.status = 'DAMAGED'
                inc.asset.save(update_fields=['status'])

            # Broadcast urgent notification to infrastructure managers
            broadcast_notification_to_role(
                role_name='infrastructure_manager',
                title=f"URGENT: {inc.get_severity_display()} - {inc.title}",
                message=f"Incident {inc.incident_id} reported for {inc.asset.name if inc.asset else 'Site'}. Immediate review required.",
                notification_type='INCIDENT',
                priority='CRITICAL' if inc.severity == 'CRITICAL' else 'HIGH',
                link=f"/incidents/{inc.id}/"
            )

            log_audit_event(
                action='CREATE',
                module='incidents',
                object_id=inc.pk,
                object_repr=f"{inc.incident_id} ({inc.title})",
                description=f"Logged emergency incident {inc.incident_id} with severity {inc.get_severity_display()}",
                request=request
            )
            messages.success(request, f"Incident ticket '{inc.incident_id}' registered and dispatched.")
            return redirect('incidents:detail', pk=inc.pk)
    else:
        form = IncidentForm()
    return render(request, 'incidents/incident_form.html', {'form': form, 'title': 'Report Infrastructure Incident'})


@login_required
@permission_required('incidents', 'edit')
def incident_update_view(request, pk):
    incident = get_object_or_404(Incident, pk=pk)
    if request.method == 'POST':
        form = IncidentForm(request.POST, request.FILES, instance=incident)
        if form.is_valid():
            inc = form.save()
            log_audit_event(
                action='UPDATE',
                module='incidents',
                object_id=inc.pk,
                object_repr=inc.incident_id,
                description=f"Updated incident parameters for {inc.incident_id}",
                request=request
            )
            messages.success(request, f"Incident '{inc.incident_id}' updated.")
            return redirect('incidents:detail', pk=inc.pk)
    else:
        form = IncidentForm(instance=incident)
    return render(request, 'incidents/incident_form.html', {'form': form, 'title': f'Edit Incident: {incident.incident_id}', 'incident': incident})


@login_required
def incident_dispatch_view(request, incident_pk):
    incident = get_object_or_404(Incident, pk=incident_pk)
    if request.method == 'POST':
        form = IncidentDispatchForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.incident = incident
            log.save()
            
            # Transition incident status to DISPATCHED if in REPORTED state
            if incident.status == 'REPORTED':
                incident.status = 'DISPATCHED'
                incident.save(update_fields=['status'])

            messages.success(request, f"Response log recorded for {incident.incident_id}.")
            return redirect('incidents:detail', pk=incident.pk)
    else:
        form = IncidentDispatchForm()
    return render(request, 'incidents/generic_form.html', {'form': form, 'title': f'Log Field Dispatch for {incident.incident_id}'})


@login_required
@permission_required('incidents', 'edit')
def incident_resolve_view(request, pk):
    incident = get_object_or_404(Incident, pk=pk)
    if request.method == 'POST':
        form = IncidentResolveForm(request.POST, instance=incident)
        if form.is_valid():
            inc = form.save(commit=False)
            inc.status = 'RESOLVED'
            inc.resolved_at = timezone.now()
            inc.save()

            if inc.asset and inc.asset.status == 'DAMAGED':
                inc.asset.status = 'ACTIVE'
                inc.asset.save(update_fields=['status'])

            log_audit_event(
                action='UPDATE',
                module='incidents',
                object_id=inc.pk,
                object_repr=inc.incident_id,
                description=f"Resolved incident {inc.incident_id} with root cause analysis",
                request=request
            )
            messages.success(request, f"Incident '{inc.incident_id}' successfully marked as RESOLVED.")
            return redirect('incidents:detail', pk=inc.pk)
    else:
        form = IncidentResolveForm(instance=incident)
    return render(request, 'incidents/generic_form.html', {'form': form, 'title': f'Complete RCA & Resolve {incident.incident_id}'})
