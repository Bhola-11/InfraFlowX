from django.contrib import admin
from .models import ReportTemplate, GeneratedReport


@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'module', 'default_format', 'is_active', 'created_at')
    list_filter = ('module', 'default_format', 'is_active')
    search_fields = ('title', 'code')


@admin.register(GeneratedReport)
class GeneratedReportAdmin(admin.ModelAdmin):
    list_display = ('report_name', 'template', 'generated_by', 'row_count', 'file_size_kb', 'execution_time_sec', 'created_at')
    list_filter = ('template__module', 'status', 'created_at')
    search_fields = ('report_name',)
