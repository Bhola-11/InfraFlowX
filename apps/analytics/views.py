import json
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Avg, Count
from .models import DashboardMetricSnapshot, KPITarget, InfrastructureHealthIndex
from .services import get_asset_distribution_by_type, get_asset_distribution_by_status, get_workorder_priority_breakdown, get_monthly_expense_trend
from apps.assets.models import Asset
from apps.workorders.models import WorkOrder
from apps.inspections.models import Inspection
from apps.incidents.models import Incident
from apps.projects.models import Project
from apps.contractors.models import Contractor
from apps.documents.models import Document
from apps.budgets.models import Budget
from apps.expenses.models import Expense


@login_required
def dashboard_view(request):
    total_assets = Asset.objects.count()
    operational_assets = Asset.objects.filter(status='ACTIVE').count()
    active_workorders = WorkOrder.objects.filter(status__in=['CREATED', 'ASSIGNED', 'IN_PROGRESS', 'SCHEDULED']).count()
    critical_incidents = Incident.objects.filter(severity__in=['HIGH', 'CRITICAL'], status__in=['REPORTED', 'DISPATCHED', 'UNDER_INVESTIGATION']).count()
    pending_inspections = Inspection.objects.filter(status__in=['SCHEDULED', 'IN_PROGRESS']).count()

    total_budget = Budget.objects.aggregate(t=Sum('allocated_amount'))['t'] or Decimal('0.00')
    total_spent = Expense.objects.filter(approval_status='APPROVED').aggregate(t=Sum('amount'))['t'] or Decimal('0.00')
    budget_utilization_pct = (total_spent / total_budget * 100) if total_budget > 0 else Decimal('0.0')

    recent_workorders = WorkOrder.objects.select_related('asset', 'assigned_employee').order_by('-created_at')[:6]
    recent_incidents = Incident.objects.select_related('asset', 'location', 'reported_by').order_by('-reported_at')[:5]
    recent_inspections = Inspection.objects.select_related('asset', 'inspector').order_by('-inspection_date')[:5]

    # Chart datasets
    type_chart = get_asset_distribution_by_type()
    status_chart = get_asset_distribution_by_status()
    wo_priority_chart = get_workorder_priority_breakdown()
    expense_trend_chart = get_monthly_expense_trend()

    kpi_targets = KPITarget.objects.all()

    # GeoJSON / Map markers for top assets with coordinates
    map_assets = Asset.objects.filter(location__latitude__isnull=False, location__longitude__isnull=False).select_related('location')[:50]
    map_markers = []
    for a in map_assets:
        map_markers.append({
            'name': a.name,
            'code': a.asset_id,
            'type': a.get_asset_type_display(),
            'status': a.get_status_display(),
            'lat': float(a.location.latitude),
            'lng': float(a.location.longitude),
            'url': f"/assets/{a.id}/",
        })

    return render(request, 'analytics/dashboard.html', {
        'total_assets': total_assets,
        'operational_assets': operational_assets,
        'active_workorders': active_workorders,
        'critical_incidents': critical_incidents,
        'pending_inspections': pending_inspections,
        'total_budget': total_budget,
        'total_spent': total_spent,
        'budget_utilization_pct': budget_utilization_pct,
        'recent_workorders': recent_workorders,
        'recent_incidents': recent_incidents,
        'recent_inspections': recent_inspections,
        'type_chart_json': json.dumps(type_chart),
        'status_chart_json': json.dumps(status_chart),
        'wo_priority_json': json.dumps(wo_priority_chart),
        'expense_trend_json': json.dumps(expense_trend_chart),
        'kpi_targets': kpi_targets,
        'map_markers_json': json.dumps(map_markers),
    })


@login_required
def degradation_analytics_view(request):
    assets_with_health = InfrastructureHealthIndex.objects.select_related('asset').all()[:30]
    avg_pci = assets_with_health.aggregate(avg=Avg('pavement_condition_index'))['avg'] or 82.5
    avg_integrity = assets_with_health.aggregate(avg=Avg('structural_integrity_rating'))['avg'] or 88.0

    return render(request, 'analytics/degradation.html', {
        'assets_with_health': assets_with_health,
        'avg_pci': avg_pci,
        'avg_integrity': avg_integrity,
    })


@login_required
def global_search_view(request):
    q = request.GET.get('q', '').strip()
    assets = []
    workorders = []
    inspections = []
    incidents = []
    contractors = []
    documents = []

    if q:
        assets = Asset.objects.filter(Q(name__icontains=q) | Q(asset_id__icontains=q) | Q(description__icontains=q))[:10]
        workorders = WorkOrder.objects.filter(Q(workorder_id__icontains=q) | Q(title__icontains=q) | Q(description__icontains=q))[:10]
        inspections = Inspection.objects.filter(Q(inspection_id__icontains=q) | Q(findings__icontains=q))[:10]
        incidents = Incident.objects.filter(Q(incident_id__icontains=q) | Q(title__icontains=q) | Q(description__icontains=q))[:10]
        contractors = Contractor.objects.filter(Q(company_name__icontains=q) | Q(registration_number__icontains=q))[:10]
        documents = Document.objects.filter(Q(title__icontains=q) | Q(doc_number__icontains=q) | Q(tags__icontains=q))[:10]

    total_results = len(assets) + len(workorders) + len(inspections) + len(incidents) + len(contractors) + len(documents)

    return render(request, 'analytics/search.html', {
        'search_query': q,
        'total_results': total_results,
        'assets': assets,
        'workorders': workorders,
        'inspections': inspections,
        'incidents': incidents,
        'contractors': contractors,
        'documents': documents,
    })
