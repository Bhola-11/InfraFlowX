from django import forms
from .models import Organization, Region, Zone, Department, Office, Team

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = [
            'name', 'code', 'org_type', 'tax_id', 'email', 
            'phone', 'website', 'address', 'logo', 'annual_budget', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. State Highway & Infrastructure Authority'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. SHIA-HQ'}),
            'org_type': forms.Select(attrs={'class': 'form-select'}),
            'tax_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tax ID / Registration Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contact@organization.gov'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 019-2834'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://infra.gov'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'annual_budget': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['organization', 'name', 'code', 'regional_head', 'description']
        widgets = {
            'organization': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Northern Metropolitan Region'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'REG-NORTH'}),
            'regional_head': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = ['region', 'name', 'code', 'description']
        widgets = {
            'region': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Metro Expressway Corridor Zone'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ZONE-MEC-01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['organization', 'name', 'code', 'head_of_department', 'budget_allocation', 'description']
        widgets = {
            'organization': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bridge & Structural Engineering Dept'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DEPT-BSE'}),
            'head_of_department': forms.Select(attrs={'class': 'form-select'}),
            'budget_allocation': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office
        fields = ['organization', 'region', 'name', 'office_type', 'address', 'phone', 'email']
        widgets = {
            'organization': forms.Select(attrs={'class': 'form-select'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Central Field Operations Depot'}),
            'office_type': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['department', 'office', 'name', 'code', 'team_lead', 'specialization']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-select'}),
            'office': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rapid Emergency Paving Crew A'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'TEAM-REP-A'}),
            'team_lead': forms.Select(attrs={'class': 'form-select'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hot Mix Asphalt & Crack Sealing'}),
        }
