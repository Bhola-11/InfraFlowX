from django.contrib import admin
from .models import AssetSchedule, ScheduledEventExecution


class ScheduledEventExecutionInline(admin.TabularInline):
    model = ScheduledEventExecution
    extra = 0


@admin.register(AssetSchedule)
class AssetScheduleAdmin(admin.ModelAdmin):
    list_display = ('schedule_code', 'title', 'schedule_type', 'asset', 'frequency', 'next_due_date', 'is_active')
    search_fields = ('schedule_code', 'title', 'asset__name')
    list_filter = ('schedule_type', 'frequency', 'is_active')
    inlines = [ScheduledEventExecutionInline]


@admin.register(ScheduledEventExecution)
class ScheduledEventExecutionAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'scheduled_date', 'status', 'assigned_to', 'created_at')
    list_filter = ('status', 'scheduled_date')
    search_fields = ('schedule__title', 'findings_summary')
