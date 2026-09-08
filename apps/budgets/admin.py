from django.contrib import admin
from .models import Budget, BudgetAllocation

class BudgetAllocationInline(admin.TabularInline):
    model = BudgetAllocation
    extra = 0

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    inlines = [BudgetAllocationInline]
    list_display = ('budget_code', 'title', 'budget_type', 'fiscal_year', 'allocated_amount', 'spent_amount', 'organization')
    list_filter = ('budget_type', 'fiscal_year', 'organization')
    search_fields = ('budget_code', 'title')
