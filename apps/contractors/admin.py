from django.contrib import admin
from .models import Contractor, ContractAgreement, ContractorEvaluation

class ContractAgreementInline(admin.TabularInline):
    model = ContractAgreement
    extra = 0

class ContractorEvaluationInline(admin.TabularInline):
    model = ContractorEvaluation
    extra = 0

@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    inlines = [ContractAgreementInline, ContractorEvaluationInline]
    list_display = ('company_name', 'registration_number', 'specialization', 'rating', 'status', 'contact_person', 'phone')
    list_filter = ('specialization', 'status', 'organization')
    search_fields = ('company_name', 'registration_number', 'contact_person')
