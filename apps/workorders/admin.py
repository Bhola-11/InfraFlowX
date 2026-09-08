from django.contrib import admin
from .models import WorkOrder, WorkOrderTask

class WorkOrderTaskInline(admin.TabularInline):
    model = WorkOrderTask
    extra = 0

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    inlines = [WorkOrderTaskInline]
    list_display = ('workorder_id', 'title', 'asset', 'priority', 'status', 'due_date', 'estimated_cost', 'actual_cost')
    list_filter = ('priority', 'status', 'due_date')
    search_fields = ('workorder_id', 'title', 'asset__name')
