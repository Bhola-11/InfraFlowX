from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('expense_id', 'category', 'amount', 'expense_date', 'contractor', 'project', 'approval_status')
    list_filter = ('category', 'approval_status', 'expense_date')
    search_fields = ('expense_id', 'description', 'invoice_number')
