from django import forms
from .models import ReportTemplate, GeneratedReport


class ReportTemplateForm(forms.ModelForm):
    class Meta:
        model = ReportTemplate
        fields = ['title', 'code', 'module', 'default_format', 'description', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'module': forms.Select(attrs={'class': 'form-select'}),
            'default_format': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
