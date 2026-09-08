from django import forms
from .models import AssetSchedule, ScheduledEventExecution


class AssetScheduleForm(forms.ModelForm):
    class Meta:
        model = AssetSchedule
        fields = [
            'schedule_code', 'title', 'schedule_type', 'asset', 'organization', 'department',
            'assigned_team', 'assigned_contractor', 'frequency', 'custom_interval_days',
            'start_date', 'end_date', 'next_due_date', 'auto_generate_workorder',
            'auto_generate_inspection', 'lead_time_days', 'is_active', 'description'
        ]
        widgets = {
            'schedule_code': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'schedule_type': forms.Select(attrs={'class': 'form-select'}),
            'asset': forms.Select(attrs={'class': 'form-select'}),
            'organization': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'assigned_team': forms.Select(attrs={'class': 'form-select'}),
            'assigned_contractor': forms.Select(attrs={'class': 'form-select'}),
            'frequency': forms.Select(attrs={'class': 'form-select'}),
            'custom_interval_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'next_due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'auto_generate_workorder': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'auto_generate_inspection': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'lead_time_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ScheduledEventExecutionForm(forms.ModelForm):
    class Meta:
        model = ScheduledEventExecution
        fields = ['status', 'actual_start_date', 'actual_completion_date', 'assigned_to', 'findings_summary']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'actual_start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'actual_completion_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'findings_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
