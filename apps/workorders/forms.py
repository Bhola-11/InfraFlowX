from django import forms
from .models import WorkOrder, WorkOrderTask

class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = [
            'workorder_id', 'title', 'description', 'asset', 'location',
            'assigned_employee', 'contractor', 'priority', 'estimated_cost',
            'actual_cost', 'due_date', 'completion_date', 'status',
            'is_safety_briefed', 'client_signoff'
        ]
        widgets = {
            'workorder_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WO-2026-9012'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bridge Deck Expansion Joint Sealing'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'asset': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'assigned_employee': forms.Select(attrs={'class': 'form-select'}),
            'contractor': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'estimated_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'actual_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'completion_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'is_safety_briefed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'client_signoff': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lead Engineer Full Name'}),
        }


class WorkOrderTaskForm(forms.ModelForm):
    class Meta:
        model = WorkOrderTask
        fields = ['task_title', 'is_completed', 'hours_spent', 'technician_name']
        widgets = {
            'task_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Concrete milling to 50mm depth'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hours_spent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'technician_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
