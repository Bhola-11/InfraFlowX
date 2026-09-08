from django import forms
from .models import Budget, BudgetAllocation

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = [
            'budget_code', 'title', 'budget_type', 'fiscal_year',
            'organization', 'department', 'allocated_amount', 'spent_amount', 'notes'
        ]
        widgets = {
            'budget_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'BGT-FY26-HWY-01'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State Highway Preventive Maintenance Budget 2026'}),
            'budget_type': forms.Select(attrs={'class': 'form-select'}),
            'fiscal_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'organization': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'allocated_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'spent_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class BudgetAllocationForm(forms.ModelForm):
    class Meta:
        model = BudgetAllocation
        fields = ['category_name', 'allocated_amount', 'spent_amount', 'notes']
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asphalt Paving Materials & Bitumen Supply'}),
            'allocated_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'spent_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
