import time
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from .models import ReportTemplate, GeneratedReport
from .generators import generate_asset_registry_csv, generate_workorders_csv, generate_inspections_csv, generate_expenses_csv
from apps.audit.utils import log_audit_event


@login_required
def report_catalog_view(request):
    templates = ReportTemplate.objects.filter(is_active=True)
    recent_reports = GeneratedReport.objects.select_related('template', 'generated_by').all()[:10]
    return render(request, 'reports/report_catalog.html', {
        'templates': templates,
        'recent_reports': recent_reports,
    })


@login_required
def report_generate_view(request, code):
    template = get_object_or_404(ReportTemplate, code=code)
    start_time = time.time()

    content = ""
    filename = f"{template.code}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"

    if template.module == 'ASSETS':
        content = generate_asset_registry_csv()
    elif template.module == 'WORKORDERS':
        content = generate_workorders_csv()
    elif template.module == 'INSPECTIONS':
        content = generate_inspections_csv()
    elif template.module == 'FINANCIALS':
        content = generate_expenses_csv()
    else:
        content = generate_asset_registry_csv()

    exec_time = time.time() - start_time
    row_count = len(content.splitlines()) - 1 if content else 0
    size_kb = len(content.encode('utf-8')) / 1024.0

    # Log generated report record
    GeneratedReport.objects.create(
        template=template,
        report_name=filename,
        generated_by=request.user,
        file_format=template.default_format,
        row_count=max(0, row_count),
        file_size_kb=size_kb,
        execution_time_sec=exec_time,
        status='COMPLETED'
    )

    log_audit_event(request.user, 'EXPORT', 'Report', str(template.id), f"Generated report {template.title} ({filename})")

    response = HttpResponse(content, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
def generated_reports_history_view(request):
    reports = GeneratedReport.objects.select_related('template', 'generated_by').all()
    return render(request, 'reports/report_history.html', {'reports': reports})
