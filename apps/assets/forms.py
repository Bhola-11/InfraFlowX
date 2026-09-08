from django import forms
from .models import Asset, AssetCategory, AssetStatusHistory

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            'asset_id', 'name', 'asset_type', 'category', 'organization',
            'location', 'department', 'owner', 'installation_date',
            'acquisition_cost', 'current_value', 'salvage_value',
            'useful_life_years', 'depreciation_method', 'condition',
            'condition_score', 'status', 'lifecycle_stage',
            'warranty_expiry', 'serial_number', 'barcode', 'photo', 'description'
        ]
        widgets = {
            'asset_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'AST-HWY-0091'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Interstate Highway I-95 North Segment 4'}),
            'asset_type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'organization': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'owner': forms.Select(attrs={'class': 'form-select'}),
            'installation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'acquisition_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'current_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'salvage_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'useful_life_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'depreciation_method': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'condition_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'lifecycle_stage': forms.Select(attrs={'class': 'form-select'}),
            'warranty_expiry': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AssetCategoryForm(forms.ModelForm):
    class Meta:
        model = AssetCategory
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AssetStatusChangeForm(forms.Form):
    new_status = forms.ChoiceField(choices=Asset.STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    reason = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'State justification for operational status transition'}))
