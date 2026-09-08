from django.contrib import admin
from .models import Project, ProjectMilestone

class ProjectMilestoneInline(admin.TabularInline):
    model = ProjectMilestone
    extra = 0

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectMilestoneInline]
    list_display = ('project_id', 'name', 'organization', 'status', 'progress', 'budget', 'actual_spending', 'start_date', 'end_date')
    list_filter = ('status', 'organization', 'start_date')
    search_fields = ('project_id', 'name')
