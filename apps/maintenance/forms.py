from django import forms
from .models import MaintenancePlan, MaintenanceActionLog

class MaintenancePlanForm(forms.ModelForm):
    class Meta:
        model = MaintenancePlan
        fields = [
            'maintenance_code', 'title', 'asset', 'maintenance_type', 'priority',
            'assigned_team', 'contractor', 'start_date', 'completion_date',
            'estimated_hours', 'cost', 'status', 'trigger_condition', 'procedure_notes', 'notes'
        ]
        widgets = {
            'maintenance_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MNT-2026-0412'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Expansion Joint Polymer Seal Replacement'}),
            'asset': forms.Select(attrs={'class': 'form-select'}),
            'maintenance_type': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'assigned_team': forms.Select(attrs={'class': 'form-select'}),
            'contractor': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'completion_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estimated_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'trigger_condition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PCI Score < 65 or 12-Month Cycle'}),
            'procedure_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class MaintenanceActionLogForm(forms.ModelForm):
    class Meta:
        model = MaintenanceActionLog
        fields = ['step_description', 'parts_replaced', 'notes']
        widgets = {
            'step_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. High-pressure hydrodemolition of spalled deck area'}),
            'parts_replaced': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Neoprene elastomeric bearing strip (Part #BS-440)'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
