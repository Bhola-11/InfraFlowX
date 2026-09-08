from django import forms
from .models import Building, BuildingFloor

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = [
            'asset', 'building_id_code', 'building_name', 'building_type',
            'address', 'floor_count', 'total_area_sqft', 'construction_year',
            'occupancy_capacity', 'energy_rating', 'is_fire_safety_certified',
            'hvac_system_type', 'roof_type', 'notes'
        ]
        widgets = {
            'asset': forms.Select(attrs={'class': 'form-select'}),
            'building_id_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'BLD-HQ-01'}),
            'building_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Central Municipal Civic Center'}),
            'building_type': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'floor_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_area_sqft': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'construction_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'occupancy_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'energy_rating': forms.Select(attrs={'class': 'form-select'}),
            'is_fire_safety_certified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hvac_system_type': forms.TextInput(attrs={'class': 'form-control'}),
            'roof_type': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class BuildingFloorForm(forms.ModelForm):
    class Meta:
        model = BuildingFloor
        fields = ['building', 'floor_number', 'floor_name', 'area_sqft', 'usage_type']
        widgets = {
            'building': forms.Select(attrs={'class': 'form-select'}),
            'floor_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'floor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Executive Operations Floor'}),
            'area_sqft': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'usage_type': forms.TextInput(attrs={'class': 'form-control'}),
        }
