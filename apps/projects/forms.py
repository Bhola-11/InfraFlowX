from django import forms
from .models import Project, ProjectMilestone

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'project_id', 'name', 'description', 'organization', 'project_manager',
            'contractor', 'start_date', 'end_date', 'budget', 'actual_spending',
            'progress', 'status'
        ]
        widgets = {
            'project_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PRJ-2026-CAP-08'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Highway 101 Expressway 6-Lane Widening'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'organization': forms.Select(attrs={'class': 'form-select'}),
            'project_manager': forms.Select(attrs={'class': 'form-select'}),
            'contractor': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'actual_spending': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'progress': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class ProjectMilestoneForm(forms.ModelForm):
    class Meta:
        model = ProjectMilestone
        fields = ['milestone_title', 'due_date', 'is_completed', 'completed_date', 'weight_percentage']
        widgets = {
            'milestone_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phase 1 Sub-base Earthwork Compaction'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'completed_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'weight_percentage': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100}),
        }
