from django import forms
from .models import Incident, IncidentDispatchLog

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = [
            'incident_id', 'title', 'incident_type', 'severity', 'asset',
            'location', 'emergency_crew', 'description', 'estimated_damage_cost',
            'status', 'photo_evidence'
        ]
        widgets = {
            'incident_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'INC-2026-0811'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Water Main Rupture on 4th Avenue'}),
            'incident_type': forms.Select(attrs={'class': 'form-select'}),
            'severity': forms.Select(attrs={'class': 'form-select'}),
            'asset': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'emergency_crew': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estimated_damage_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'photo_evidence': forms.FileInput(attrs={'class': 'form-control'}),
        }


class IncidentDispatchForm(forms.ModelForm):
    class Meta:
        model = IncidentDispatchLog
        fields = ['responder_name', 'action_taken']
        widgets = {
            'responder_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fire Chief / Road Marshal Name'}),
            'action_taken': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Traffic diversion cones installed, isolation valve closed...'}),
        }


class IncidentResolveForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['root_cause_analysis', 'resolution_summary']
        widgets = {
            'root_cause_analysis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Material fatigue due to water hammer pressure spike...'}),
            'resolution_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Pipe segment replaced with ductile iron sleeve. System re-pressurized.'}),
        }
