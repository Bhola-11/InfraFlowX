import csv
import io
from django.http import HttpResponse
from apps.assets.models import Asset
from apps.workorders.models import WorkOrder
from apps.inspections.models import Inspection
from apps.expenses.models import Expense
from apps.contractors.models import Contractor
from apps.incidents.models import Incident


def generate_asset_registry_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Asset Code', 'Name', 'Type', 'Status', 'Condition Score', 'Criticality', 'Location', 'Purchase Cost', 'Current Valuation', 'Installation Date'])

    assets = Asset.objects.select_related('location').all()
    for a in assets:
        writer.writerow([
            a.asset_code,
            a.name,
            a.get_asset_type_display(),
            a.get_status_display(),
            a.condition_score,
            a.get_criticality_level_display(),
            a.location.name if a.location else '',
            a.purchase_cost,
            a.current_valuation,
            a.installation_date or ''
        ])
    return output.getvalue()


def generate_workorders_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['WO Number', 'Title', 'Asset', 'Type', 'Priority', 'Status', 'Assigned To', 'Estimated Cost', 'Actual Cost', 'Scheduled Start', 'Completed Date'])

    wos = WorkOrder.objects.select_related('asset', 'assigned_to').all()
    for w in wos:
        writer.writerow([
            w.wo_number,
            w.title,
            w.asset.name if w.asset else '',
            w.get_work_type_display(),
            w.get_priority_display(),
            w.get_status_display(),
            w.assigned_to.get_full_name() if w.assigned_to else '',
            w.estimated_cost,
            w.actual_cost,
            w.scheduled_start_date or '',
            w.actual_end_date or ''
        ])
    return output.getvalue()


def generate_inspections_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Inspection Number', 'Title', 'Asset', 'Type', 'Status', 'Inspector', 'Scheduled Date', 'Condition Score', 'Remarks'])

    inspections = Inspection.objects.select_related('asset', 'inspector').all()
    for i in inspections:
        writer.writerow([
            i.inspection_number,
            i.title,
            i.asset.name if i.asset else '',
            i.get_inspection_type_display(),
            i.get_status_display(),
            i.inspector.get_full_name() if i.inspector else '',
            i.scheduled_date,
            i.overall_condition_score,
            i.summary_notes or ''
        ])
    return output.getvalue()


def generate_expenses_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Expense Number', 'Title', 'Category', 'Amount', 'Date', 'Status', 'Budget Item', 'Vendor', 'Logged By'])

    expenses = Expense.objects.select_related('budget_allocation', 'logged_by').all()
    for e in expenses:
        writer.writerow([
            e.expense_number,
            e.title,
            e.category,
            e.amount,
            e.expense_date,
            e.get_status_display(),
            e.budget_allocation.budget.title if e.budget_allocation else '',
            e.vendor_name or '',
            e.logged_by.get_full_name() if e.logged_by else ''
        ])
    return output.getvalue()
