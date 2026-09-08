from django import forms
from .models import Road, RoadDefect, RoadRepairHistory

class RoadForm(forms.ModelForm):
    class Meta:
        model = Road
        fields = [
            'asset', 'road_code', 'road_name', 'region', 'length_km',
            'width_meters', 'lanes_count', 'surface_type', 'construction_date',
            'last_resurfaced_date', 'traffic_level', 'speed_limit_mph',
            'pci_score', 'notes'
        ]
        widgets = {
            'asset': forms.Select(attrs={'class': 'form-select'}),
            'road_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. HWY-US-101-N'}),
            'road_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pacific Coast Highway Northern Corridor'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
            'length_km': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'width_meters': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'lanes_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'surface_type': forms.Select(attrs={'class': 'form-select'}),
            'construction_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'last_resurfaced_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'traffic_level': forms.Select(attrs={'class': 'form-select'}),
            'speed_limit_mph': forms.NumberInput(attrs={'class': 'form-control'}),
            'pci_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class RoadDefectForm(forms.ModelForm):
    class Meta:
        model = RoadDefect
        fields = ['road', 'defect_type', 'severity', 'chainage_km', 'description', 'photo', 'is_repaired']
        widgets = {
            'road': forms.Select(attrs={'class': 'form-select'}),
            'defect_type': forms.Select(attrs={'class': 'form-select'}),
            'severity': forms.Select(attrs={'class': 'form-select'}),
            'chainage_km': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'is_repaired': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
