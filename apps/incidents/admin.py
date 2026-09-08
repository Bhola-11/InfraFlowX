from django.contrib import admin
from .models import Incident, IncidentDispatchLog


class IncidentDispatchLogInline(admin.TabularInline):
    model = IncidentDispatchLog
    extra = 0


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('incident_id', 'title', 'incident_type', 'severity', 'status', 'reported_at')
    list_filter = ('incident_type', 'severity', 'status', 'reported_at')
    search_fields = ('incident_id', 'title', 'description')
    inlines = [IncidentDispatchLogInline]


@admin.register(IncidentDispatchLog)
class IncidentDispatchLogAdmin(admin.ModelAdmin):
    list_display = ('incident', 'responder_name', 'action_taken', 'timestamp')
    list_filter = ('timestamp',)
