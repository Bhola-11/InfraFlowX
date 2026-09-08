from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg

from .models import Bridge, BridgeComponentInspection
from .forms import BridgeForm, BridgeComponentInspectionForm
from apps.permissions.decorators import permission_required
from apps.audit.utils import log_audit_event

@login_required
def bridge_list_view(request):
    """
    Bridge and structural engineering inventory list.
    """
    query = request.GET.get('q', '').strip()
    type_filter = request.GET.get('type', '')
    condition_filter = request.GET.get('condition', '')
    scour_filter = request.GET.get('scour', '')

    bridges_qs = Bridge.objects.select_related('asset', 'asset__organization', 'asset__location').annotate(
        component_count=Count('components')
    )

    if query:
        bridges_qs = bridges_qs.filter(
            Q(bridge_id_code__icontains=query) |
            Q(bridge_name__icontains=query) |
            Q(feature_crossed__icontains=query)
        )
    if type_filter:
        bridges_qs = bridges_qs.filter(bridge_type=type_filter)
    if condition_filter:
        bridges_qs = bridges_qs.filter(condition=condition_filter)
    if scour_filter == 'yes':
        bridges_qs = bridges_qs.filter(is_scour_critical=True)

    paginator = Paginator(bridges_qs, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'query': query,
        'type_filter': type_filter,
        'condition_filter': condition_filter,
        'scour_filter': scour_filter,
        'bridge_types': Bridge.BRIDGE_TYPES,
        'conditions': Bridge.CONDITION_CHOICES,
        'total_bridges': bridges_qs.count(),
        'critical_bridges': bridges_qs.filter(condition='CRITICAL').count(),
    }
    return render(request, 'bridges/bridge_list.html', context)


@login_required
def bridge_detail_view(request, pk):
    """
    Comprehensive structural dossier for bridge assets including component health grades.
    """
    bridge = get_object_or_404(Bridge.objects.select_related('asset', 'asset__organization', 'asset__location'), pk=pk)
    components = bridge.components.all()

    avg_component_rating = components.aggregate(avg=Avg('rating_score_1_to_9'))['avg'] or 0

    context = {
        'bridge': bridge,
        'components': components,
        'avg_component_rating': round(avg_component_rating, 1),
    }
    return render(request, 'bridges/bridge_detail.html', context)


@login_required
@permission_required('bridges', 'create')
def bridge_create_view(request):
    if request.method == 'POST':
        form = BridgeForm(request.POST)
        if form.is_valid():
            bridge = form.save()
            log_audit_event(
                action='CREATE',
                module='bridges',
                object_id=bridge.pk,
                object_repr=f"{bridge.bridge_id_code} ({bridge.bridge_name})",
                description=f"Registered bridge structure {bridge.bridge_id_code}",
                request=request
            )
            messages.success(request, f"Bridge '{bridge.bridge_name}' registered successfully.")
            return redirect('bridges:detail', pk=bridge.pk)
    else:
        form = BridgeForm()
    return render(request, 'bridges/bridge_form.html', {'form': form, 'title': 'Register Bridge Structure'})


@login_required
@permission_required('bridges', 'edit')
def bridge_update_view(request, pk):
    bridge = get_object_or_404(Bridge, pk=pk)
    if request.method == 'POST':
        form = BridgeForm(request.POST, instance=bridge)
        if form.is_valid():
            bridge = form.save()
            log_audit_event(
                action='UPDATE',
                module='bridges',
                object_id=bridge.pk,
                object_repr=f"{bridge.bridge_id_code}",
                description=f"Updated structural data for bridge {bridge.bridge_id_code}",
                request=request
            )
            messages.success(request, f"Bridge '{bridge.bridge_id_code}' updated successfully.")
            return redirect('bridges:detail', pk=bridge.pk)
    else:
        form = BridgeForm(instance=bridge)
    return render(request, 'bridges/bridge_form.html', {'form': form, 'title': f'Edit Bridge: {bridge.bridge_name}', 'bridge': bridge})


@login_required
@permission_required('bridges', 'create')
def bridge_component_add_view(request, bridge_pk):
    bridge = get_object_or_404(Bridge, pk=bridge_pk)
    if request.method == 'POST':
        form = BridgeComponentInspectionForm(request.POST, request.FILES)
        if form.is_valid():
            comp = form.save(commit=False)
            comp.bridge = bridge
            comp.save()
            messages.success(request, f"Component evaluation for '{comp.get_component_display()}' saved.")
            return redirect('bridges:detail', pk=bridge.pk)
    else:
        form = BridgeComponentInspectionForm(initial={'bridge': bridge})
    return render(request, 'bridges/component_form.html', {'form': form, 'bridge': bridge, 'title': f'Add Component Rating for {bridge.bridge_name}'})
