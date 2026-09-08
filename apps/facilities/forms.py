from django import forms
from .models import FacilityEquipment, FacilityServiceLog

class FacilityEquipmentForm(forms.ModelForm):
    class Meta:
        model = FacilityEquipment
        fields = [
            'asset', 'equipment_code', 'equipment_name', 'equipment_type',
            'manufacturer', 'model_number', 'power_rating_kw', 'operating_hours',
            'last_service_date', 'next_service_due', 'service_contract_vendor', 'notes'
        ]
        widgets = {
            'asset': forms.Select(attrs={'class': 'form-select'}),
            'equipment_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'EQP-GEN-01'}),
            'equipment_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '500kVA Cummins Diesel Backup Generator'}),
            'equipment_type': forms.Select(attrs={'class': 'form-select'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'model_number': forms.TextInput(attrs={'class': 'form-control'}),
            'power_rating_kw': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'operating_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'last_service_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'next_service_due': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'service_contract_vendor': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class FacilityServiceLogForm(forms.ModelForm):
    class Meta:
        model = FacilityServiceLog
        fields = ['equipment', 'service_date', 'service_type', 'technician_name', 'cost', 'operating_hours_at_service', 'notes']
        widgets = {
            'equipment': forms.Select(attrs={'class': 'form-select'}),
            'service_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'service_type': forms.Select(attrs={'class': 'form-select'}),
            'technician_name': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'operating_hours_at_service': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
