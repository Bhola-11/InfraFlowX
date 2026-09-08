from django import forms
from .models import Inspection, InspectionChecklistItem

class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = [
            'inspection_id', 'asset', 'inspector', 'inspection_type',
            'inspection_date', 'condition_score', 'status', 'weather_conditions',
            'findings', 'recommendations', 'photo_primary', 'photo_secondary'
        ]
        widgets = {
            'inspection_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'INSP-2026-0881'}),
            'asset': forms.Select(attrs={'class': 'form-select'}),
            'inspector': forms.Select(attrs={'class': 'form-select'}),
            'inspection_type': forms.Select(attrs={'class': 'form-select'}),
            'inspection_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'condition_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'weather_conditions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Clear, 22°C, Dry Pavement'}),
            'findings': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'photo_primary': forms.FileInput(attrs={'class': 'form-control'}),
            'photo_secondary': forms.FileInput(attrs={'class': 'form-control'}),
        }


class InspectionChecklistItemForm(forms.ModelForm):
    class Meta:
        model = InspectionChecklistItem
        fields = ['item_title', 'is_satisfactory', 'score_1_to_10', 'comments']
        widgets = {
            'item_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Bearing pad elastomeric displacement check'}),
            'is_satisfactory': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'score_1_to_10': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
