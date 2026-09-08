from django.contrib import admin
from .models import SupportTicket, TicketComment, CitizenFeedback, SLAPolicy


@admin.register(SLAPolicy)
class SLAPolicyAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority', 'response_time_hours', 'resolution_time_hours', 'escalation_email')


class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    extra = 0


class CitizenFeedbackInline(admin.StackedInline):
    model = CitizenFeedback
    extra = 0


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'subject', 'category', 'priority', 'status', 'reporter_name', 'assigned_to', 'created_at')
    list_filter = ('category', 'priority', 'status', 'is_citizen_complaint')
    search_fields = ('ticket_number', 'subject', 'reporter_name', 'description')
    inlines = [TicketCommentInline, CitizenFeedbackInline]


@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'author', 'author_name', 'is_internal_note', 'created_at')


@admin.register(CitizenFeedback)
class CitizenFeedbackAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'rating', 'created_at')
