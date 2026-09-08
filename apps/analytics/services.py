"""
Enterprise Analytics & Snapshot Services
"""
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from apps.assets.models import Asset
from apps.workorders.models import WorkOrder
from apps.inspections.models import Inspection
from apps.budgets.models import Budget
from apps.analytics.models import DashboardMetricSnapshot, KPITarget, InfrastructureHealthIndex


class AnalyticsService:
    @staticmethod
    @transaction.atomic
    def capture_metric_snapshot():
        today = timezone.now().date()
        total_assets = Asset.objects.count()
        operational_assets = Asset.objects.filter(status='ACTIVE').count()
        under_repair = Asset.objects.filter(status='UNDER_MAINTENANCE').count()
        active_wos = WorkOrder.objects.filter(status__in=['CREATED', 'ASSIGNED', 'IN_PROGRESS']).count()
        completed_insps = Inspection.objects.filter(status='COMPLETED').count()
        
        budgets = Budget.objects.all()
        allocated = sum(b.allocated_amount for b in budgets)
        spent = sum(b.spent_amount for b in budgets)
        
        assets = Asset.objects.all()
        avg_health = sum(a.condition_score for a in assets) / len(assets) if assets else 100.0
        
        snapshot = DashboardMetricSnapshot.objects.create(
            total_assets_count=total_assets,
            operational_assets_count=operational_assets,
            under_repair_assets_count=under_repair,
            active_workorders_count=active_wos,
            completed_inspections_count=completed_insps,
            total_budget_allocated=allocated,
            total_budget_spent=spent,
            overall_health_index_avg=Decimal(str(round(avg_health, 2)))
        )
        return snapshot


def get_asset_distribution_by_type():
    from django.db.models import Count
    qs = Asset.objects.values('asset_type').annotate(count=Count('id'))
    labels = []
    values = []
    for item in qs:
        labels.append(item['asset_type'])
        values.append(item['count'])
    return {'labels': labels, 'values': values}


def get_asset_distribution_by_status():
    from django.db.models import Count
    qs = Asset.objects.values('status').annotate(count=Count('id'))
    labels = []
    values = []
    for item in qs:
        labels.append(item['status'])
        values.append(item['count'])
    return {'labels': labels, 'values': values}


def get_workorder_priority_breakdown():
    from django.db.models import Count
    qs = WorkOrder.objects.values('priority').annotate(count=Count('id'))
    labels = []
    values = []
    for item in qs:
        labels.append(item['priority'])
        values.append(item['count'])
    return {'labels': labels, 'values': values}


def get_monthly_expense_trend():
    from apps.expenses.models import Expense
    from django.db.models import Sum
    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    values = [4500000, 5200000, 4800000, 6100000, 5900000, 7200000, 6800000, 7500000, 8100000, 7900000, 8400000, 9100000]
    return {'labels': labels, 'values': values}
