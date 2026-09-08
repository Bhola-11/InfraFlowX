from django import forms
from .models import Bridge, BridgeComponentInspection

class BridgeForm(forms.ModelForm):
    class Meta:
        model = Bridge
        fields = [
            'asset', 'bridge_id_code', 'bridge_name', 'feature_crossed',
            'bridge_type', 'length_meters', 'width_meters', 'span_count',
            'main_span_length', 'construction_year', 'load_capacity_tons',
            'vertical_clearance_meters', 'condition', 'inspection_frequency_months',
            'is_scour_critical', 'notes'
        ]
        widgets = {
            'asset': forms.Select(attrs={'class': 'form-select'}),
            'bridge_id_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. BRG-NBI-CA-0428'}),
            'bridge_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Golden Gateway Suspension Bridge'}),
            'feature_crossed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bay Strait Waterway'}),
            'bridge_type': forms.Select(attrs={'class': 'form-select'}),
            'length_meters': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'width_meters': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'span_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'main_span_length': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'construction_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'load_capacity_tons': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'vertical_clearance_meters': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'inspection_frequency_months': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_scour_critical': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class BridgeComponentInspectionForm(forms.ModelForm):
    class Meta:
        model = BridgeComponentInspection
        fields = ['bridge', 'component', 'rating_score_1_to_9', 'findings', 'photo', 'inspected_date']
        widgets = {
            'bridge': forms.Select(attrs={'class': 'form-select'}),
            'component': forms.Select(attrs={'class': 'form-select'}),
            'rating_score_1_to_9': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 9}),
            'findings': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'inspected_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
