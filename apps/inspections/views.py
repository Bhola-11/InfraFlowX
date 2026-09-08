from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count

from .models import Inspection, InspectionChecklistItem
from .forms import InspectionForm, InspectionChecklistItemForm
from apps.assets.models import Asset
from apps.permissions.decorators import permission_required
from apps.audit.utils import log_audit_event

@login_required
def inspection_list_view(request):
    """
    Inspection operations listing with type, status, and condition filtering.
    """
    query = request.GET.get('q', '').strip()
    type_filter = request.GET.get('type', '')
    status_filter = request.GET.get('status', '')

    inspections_qs = Inspection.objects.select_related(
        'asset', 'inspector', 'asset__organization', 'asset__location'
    ).all()

    if query:
        inspections_qs = inspections_qs.filter(
            Q(inspection_id__icontains=query) |
            Q(asset__name__icontains=query) |
            Q(asset__asset_id__icontains=query) |
            Q(inspector__username__icontains=query) |
            Q(findings__icontains=query)
        )
    if type_filter:
        inspections_qs = inspections_qs.filter(inspection_type=type_filter)
    if status_filter:
        inspections_qs = inspections_qs.filter(status=status_filter)

    avg_score = inspections_qs.aggregate(avg=Avg('condition_score'))['avg'] or 0

    paginator = Paginator(inspections_qs, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'query': query,
        'type_filter': type_filter,
        'status_filter': status_filter,
        'inspection_types': Inspection.INSPECTION_TYPES,
        'statuses': Inspection.STATUS_CHOICES,
        'total_inspections': inspections_qs.count(),
        'avg_score': round(avg_score, 1),
        'pending_count': inspections_qs.filter(status='SCHEDULED').count(),
    }
    return render(request, 'inspections/inspection_list.html', context)


@login_required
def inspection_detail_view(request, pk):
    """
    Detailed inspection report scorecard, checklist evaluation and photos.
    """
    inspection = get_object_or_404(
        Inspection.objects.select_related('asset', 'inspector', 'asset__organization', 'asset__location'),
        pk=pk
    )
    checklist_items = inspection.checklist_items.all()

    context = {
        'inspection': inspection,
        'checklist_items': checklist_items,
    }
    return render(request, 'inspections/inspection_detail.html', context)


@login_required
@permission_required('inspections', 'create')
def inspection_create_view(request):
    """
    Create a new infrastructure inspection dispatch.
    """
    if request.method == 'POST':
        form = InspectionForm(request.POST, request.FILES)
        if form.is_valid():
            insp = form.save()
            # Update asset condition score if inspection is completed
            if insp.status == 'COMPLETED':
                asset = insp.asset
                asset.condition_score = insp.condition_score
                if insp.condition_score >= 90:
                    asset.condition = 'EXCELLENT'
                elif insp.condition_score >= 70:
                    asset.condition = 'GOOD'
                elif insp.condition_score >= 50:
                    asset.condition = 'FAIR'
                elif insp.condition_score >= 25:
                    asset.condition = 'POOR'
                else:
                    asset.condition = 'CRITICAL'
                asset.save(update_fields=['condition_score', 'condition'])

            log_audit_event(
                action='CREATE',
                module='inspections',
                object_id=insp.pk,
                object_repr=f"{insp.inspection_id} for {insp.asset.name}",
                description=f"Created {insp.get_inspection_type_display()} inspection report",
                request=request
            )
            messages.success(request, f"Inspection '{insp.inspection_id}' created successfully.")
            return redirect('inspections:detail', pk=insp.pk)
    else:
        form = InspectionForm()

    return render(request, 'inspections/inspection_form.html', {'form': form, 'title': 'Create Inspection Report'})


@login_required
@permission_required('inspections', 'edit')
def inspection_update_view(request, pk):
    inspection = get_object_or_404(Inspection, pk=pk)
    if request.method == 'POST':
        form = InspectionForm(request.POST, request.FILES, instance=inspection)
        if form.is_valid():
            insp = form.save()
            log_audit_event(
                action='UPDATE',
                module='inspections',
                object_id=insp.pk,
                object_repr=f"{insp.inspection_id}",
                description=f"Updated inspection findings for {insp.inspection_id}",
                request=request
            )
            messages.success(request, f"Inspection '{insp.inspection_id}' updated.")
            return redirect('inspections:detail', pk=insp.pk)
    else:
        form = InspectionForm(instance=inspection)
    return render(request, 'inspections/inspection_form.html', {'form': form, 'title': f'Edit Inspection: {inspection.inspection_id}', 'inspection': inspection})


@login_required
@permission_required('inspections', 'create')
def inspection_add_checklist_view(request, inspection_pk):
    inspection = get_object_or_404(Inspection, pk=inspection_pk)
    if request.method == 'POST':
        form = InspectionChecklistItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.inspection = inspection
            item.save()
            messages.success(request, f"Checklist item '{item.item_title}' recorded.")
            return redirect('inspections:detail', pk=inspection.pk)
    else:
        form = InspectionChecklistItemForm()
    return render(request, 'inspections/generic_form.html', {'form': form, 'title': f'Add Checklist Point for {inspection.inspection_id}'})


@login_required
@permission_required('inspections', 'approve')
def inspection_approve_view(request, pk):
    inspection = get_object_or_404(Inspection, pk=pk)
    inspection.status = 'REVIEWED'
    inspection.save(update_fields=['status'])
    log_audit_event(
        action='UPDATE',
        module='inspections',
        object_id=inspection.pk,
        object_repr=inspection.inspection_id,
        description=f"Approved and finalized inspection {inspection.inspection_id}",
        request=request
    )
    messages.success(request, f"Inspection '{inspection.inspection_id}' reviewed and approved.")
    return redirect('inspections:detail', pk=inspection.pk)
