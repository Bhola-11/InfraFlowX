from django import forms
from .models import Contractor, ContractAgreement, ContractorEvaluation

class ContractorForm(forms.ModelForm):
    class Meta:
        model = Contractor
        fields = [
            'organization', 'company_name', 'registration_number', 'contact_person',
            'email', 'phone', 'address', 'specialization', 'rating', 'status',
            'contract_start', 'contract_end', 'insurance_policy_number', 'insurance_expiry', 'notes'
        ]
        widgets = {
            'organization': forms.Select(attrs={'class': 'form-select'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apex Infrastructure Solutions LLC'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VEN-REG-99201'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Principal Engineer Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'specialization': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': 1.0, 'max': 5.0}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'contract_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'contract_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'insurance_policy_number': forms.TextInput(attrs={'class': 'form-control'}),
            'insurance_expiry': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ContractAgreementForm(forms.ModelForm):
    class Meta:
        model = ContractAgreement
        fields = ['contractor', 'organization', 'contract_title', 'contract_number', 'total_contract_value', 'start_date', 'end_date', 'scope_summary', 'is_active', 'document_file']
        widgets = {
            'contractor': forms.Select(attrs={'class': 'form-select'}),
            'organization': forms.Select(attrs={'class': 'form-select'}),
            'contract_title': forms.TextInput(attrs={'class': 'form-control'}),
            'contract_number': forms.TextInput(attrs={'class': 'form-control'}),
            'total_contract_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'scope_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'document_file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ContractorEvaluationForm(forms.ModelForm):
    class Meta:
        model = ContractorEvaluation
        fields = ['contractor', 'quality_score', 'safety_score', 'timeliness_score', 'comments']
        widgets = {
            'contractor': forms.Select(attrs={'class': 'form-select'}),
            'quality_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'safety_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'timeliness_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
