from django import forms
from .models import ConditionLog, DeteriorationModel

class ConditionLogForm(forms.ModelForm):
    class Meta:
        model = ConditionLog
        fields = ['asset', 'recorded_date', 'condition_score', 'condition_category', 'structural_index', 'operational_index', 'safety_index', 'assessor', 'notes']
        widgets = {
            'asset': forms.Select(attrs={'class': 'form-select'}),
            'recorded_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'condition_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'condition_category': forms.Select(attrs={'class': 'form-select'}),
            'structural_index': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'operational_index': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'safety_index': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'assessor': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DeteriorationModelForm(forms.ModelForm):
    class Meta:
        model = DeteriorationModel
        fields = ['asset_type', 'expected_lifecycle_years', 'annual_decay_rate_pct', 'heavy_load_multiplier', 'severe_climate_multiplier', 'description']
        widgets = {
            'asset_type': forms.Select(attrs={'class': 'form-select'}),
            'expected_lifecycle_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'annual_decay_rate_pct': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'heavy_load_multiplier': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'severe_climate_multiplier': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
