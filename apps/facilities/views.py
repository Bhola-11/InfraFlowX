from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count

from .models import FacilityEquipment, FacilityServiceLog
from .forms import FacilityEquipmentForm, FacilityServiceLogForm
from apps.permissions.decorators import permission_required
from apps.audit.utils import log_audit_event

@login_required
def facility_list_view(request):
    """
    Facility MEP equipment directory with maintenance overdue alerts.
    """
    query = request.GET.get('q', '').strip()
    type_filter = request.GET.get('type', '')

    equipment_qs = FacilityEquipment.objects.select_related('asset', 'asset__organization', 'asset__location').annotate(
        service_count=Count('service_logs')
    )

    if query:
        equipment_qs = equipment_qs.filter(
            Q(equipment_code__icontains=query) |
            Q(equipment_name__icontains=query) |
            Q(manufacturer__icontains=query) |
            Q(model_number__icontains=query)
        )
    if type_filter:
        equipment_qs = equipment_qs.filter(equipment_type=type_filter)

    paginator = Paginator(equipment_qs, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'query': query,
        'type_filter': type_filter,
        'equipment_types': FacilityEquipment.EQUIPMENT_TYPES,
        'total_equipment': equipment_qs.count(),
    }
    return render(request, 'facilities/facility_list.html', context)


@login_required
def facility_detail_view(request, pk):
    """
    Facility plant equipment dossier with historical service logs and meter readings.
    """
    equipment = get_object_or_404(
        FacilityEquipment.objects.select_related('asset', 'asset__organization', 'asset__location'),
        pk=pk
    )
    service_logs = equipment.service_logs.all()[:15]

    context = {
        'equipment': equipment,
        'service_logs': service_logs,
    }
    return render(request, 'facilities/facility_detail.html', context)


@login_required
@permission_required('facilities', 'create')
def facility_create_view(request):
    if request.method == 'POST':
        form = FacilityEquipmentForm(request.POST)
        if form.is_valid():
            eqp = form.save()
            log_audit_event(
                action='CREATE',
                module='facilities',
                object_id=eqp.pk,
                object_repr=f"{eqp.equipment_code} ({eqp.equipment_name})",
                description=f"Registered facility equipment unit {eqp.equipment_name}",
                request=request
            )
            messages.success(request, f"Equipment '{eqp.equipment_name}' registered successfully.")
            return redirect('facilities:detail', pk=eqp.pk)
    else:
        form = FacilityEquipmentForm()
    return render(request, 'facilities/facility_form.html', {'form': form, 'title': 'Register Facility Equipment'})


@login_required
@permission_required('facilities', 'edit')
def facility_update_view(request, pk):
    eqp = get_object_or_404(FacilityEquipment, pk=pk)
    if request.method == 'POST':
        form = FacilityEquipmentForm(request.POST, instance=eqp)
        if form.is_valid():
            eqp = form.save()
            log_audit_event(
                action='UPDATE',
                module='facilities',
                object_id=eqp.pk,
                object_repr=f"{eqp.equipment_code}",
                description=f"Updated parameters for equipment {eqp.equipment_code}",
                request=request
            )
            messages.success(request, f"Equipment '{eqp.equipment_name}' updated successfully.")
            return redirect('facilities:detail', pk=eqp.pk)
    else:
        form = FacilityEquipmentForm(instance=eqp)
    return render(request, 'facilities/facility_form.html', {'form': form, 'title': f'Edit Equipment: {eqp.equipment_name}', 'equipment': eqp})


@login_required
@permission_required('facilities', 'create')
def service_log_create_view(request, equipment_pk):
    equipment = get_object_or_404(FacilityEquipment, pk=equipment_pk)
    if request.method == 'POST':
        form = FacilityServiceLogForm(request.POST)
        if form.is_valid():
            svc = form.save(commit=False)
            svc.equipment = equipment
            svc.save()
            # Update equipment last service date
            equipment.last_service_date = svc.service_date
            if svc.operating_hours_at_service > equipment.operating_hours:
                equipment.operating_hours = svc.operating_hours_at_service
            equipment.save(update_fields=['last_service_date', 'operating_hours'])
            messages.success(request, f"Service record logged for {equipment.equipment_name}.")
            return redirect('facilities:detail', pk=equipment.pk)
    else:
        form = FacilityServiceLogForm(initial={'equipment': equipment})
    return render(request, 'facilities/generic_form.html', {'form': form, 'title': f'Log Service for {equipment.equipment_name}'})
