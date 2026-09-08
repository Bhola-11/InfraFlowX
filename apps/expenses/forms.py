from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            'expense_id', 'asset', 'project', 'work_order', 'contractor',
            'category', 'amount', 'expense_date', 'invoice_number',
            'description', 'receipt_file', 'approval_status'
        ]
        widgets = {
            'expense_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'EXP-2026-9901'}),
            'asset': forms.Select(attrs={'class': 'form-select'}),
            'project': forms.Select(attrs={'class': 'form-select'}),
            'work_order': forms.Select(attrs={'class': 'form-select'}),
            'contractor': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'expense_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'invoice_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'INV-APEX-8823'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'receipt_file': forms.FileInput(attrs={'class': 'form-control'}),
            'approval_status': forms.Select(attrs={'class': 'form-select'}),
        }
