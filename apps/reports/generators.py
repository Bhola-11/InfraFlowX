import csv
import io
from apps.assets.models import Asset
from apps.workorders.models import WorkOrder
from apps.inspections.models import Inspection
from apps.expenses.models import Expense


def generate_asset_registry_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Asset ID', 'Name', 'Type', 'Status', 'Condition Score', 'Criticality', 'Location', 'Initial Cost', 'Current Value', 'Installation Date'])

    assets = Asset.objects.select_related('location').all()
    for a in assets:
        writer.writerow([
            a.asset_id,
            a.name,
            a.get_asset_type_display() if hasattr(a, 'get_asset_type_display') else a.asset_type,
            a.get_status_display() if hasattr(a, 'get_status_display') else a.status,
            getattr(a, 'condition_score', 0),
            a.get_criticality_display() if hasattr(a, 'get_criticality_display') else getattr(a, 'criticality', ''),
            a.location.name if a.location else '',
            getattr(a, 'initial_cost', ''),
            getattr(a, 'current_value', ''),
            a.installation_date or ''
        ])
    return output.getvalue()


def generate_workorders_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['WorkOrder ID', 'Title', 'Asset', 'Type', 'Priority', 'Status', 'Assigned Employee', 'Estimated Cost', 'Actual Cost', 'Scheduled Start', 'Completed Date'])

    wos = WorkOrder.objects.select_related('asset', 'assigned_employee__user').all()
    for w in wos:
        assigned_name = ''
        if w.assigned_employee:
            if hasattr(w.assigned_employee, 'user') and w.assigned_employee.user:
                assigned_name = w.assigned_employee.user.get_full_name() or w.assigned_employee.user.username
            else:
                assigned_name = str(w.assigned_employee)

        writer.writerow([
            w.workorder_id,
            w.title,
            w.asset.name if w.asset else '',
            w.get_order_type_display() if hasattr(w, 'get_order_type_display') else getattr(w, 'order_type', ''),
            w.get_priority_display() if hasattr(w, 'get_priority_display') else getattr(w, 'priority', ''),
            w.get_status_display() if hasattr(w, 'get_status_display') else w.status,
            assigned_name,
            getattr(w, 'estimated_cost', 0),
            getattr(w, 'actual_cost', 0),
            getattr(w, 'scheduled_start_date', '') or '',
            getattr(w, 'completion_date', '') or ''
        ])
    return output.getvalue()


def generate_inspections_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Inspection ID', 'Asset', 'Type', 'Status', 'Inspector', 'Inspection Date', 'Condition Score', 'Findings'])

    inspections = Inspection.objects.select_related('asset', 'inspector').all()
    for i in inspections:
        inspector_name = i.inspector.get_full_name() or i.inspector.username if i.inspector else ''
        writer.writerow([
            i.inspection_id,
            i.asset.name if i.asset else '',
            i.get_inspection_type_display() if hasattr(i, 'get_inspection_type_display') else getattr(i, 'inspection_type', ''),
            i.get_status_display() if hasattr(i, 'get_status_display') else i.status,
            inspector_name,
            getattr(i, 'inspection_date', '') or '',
            getattr(i, 'condition_score', 0),
            getattr(i, 'findings', '') or ''
        ])
    return output.getvalue()


def generate_expenses_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Expense ID', 'Description', 'Category', 'Amount', 'Date', 'Invoice No', 'Status', 'Asset', 'Project', 'Contractor', 'Approved By'])

    expenses = Expense.objects.select_related('asset', 'project', 'contractor', 'approved_by').all()
    for e in expenses:
        approved_by_name = (e.approved_by.get_full_name() or e.approved_by.username) if e.approved_by else ''
        writer.writerow([
            e.expense_id,
            e.description,
            e.get_category_display() if hasattr(e, 'get_category_display') else e.category,
            e.amount,
            e.expense_date,
            e.invoice_number or '',
            e.get_approval_status_display() if hasattr(e, 'get_approval_status_display') else e.approval_status,
            e.asset.name if e.asset else '',
            e.project.name if e.project else '',
            e.contractor.company_name if e.contractor else '',
            approved_by_name
        ])
    return output.getvalue()
