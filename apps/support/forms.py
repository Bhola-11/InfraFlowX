from django import forms
from .models import SupportTicket, TicketComment, CitizenFeedback, SLAPolicy


class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = [
            'ticket_number', 'subject', 'category', 'priority', 'status',
            'asset', 'location', 'reporter_name', 'reporter_email', 'reporter_phone',
            'is_citizen_complaint', 'assigned_to', 'assigned_department',
            'description', 'resolution_notes'
        ]
        widgets = {
            'ticket_number': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'asset': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'reporter_name': forms.TextInput(attrs={'class': 'form-control'}),
            'reporter_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'reporter_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'is_citizen_complaint': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'assigned_department': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'resolution_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class TicketCommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ['comment', 'is_internal_note']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write an update or internal note...'}),
            'is_internal_note': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CitizenFeedbackForm(forms.ModelForm):
    class Meta:
        model = CitizenFeedback
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Your experience and comments...'}),
        }
