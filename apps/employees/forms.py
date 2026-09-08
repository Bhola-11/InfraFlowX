from django import forms
from .models import Designation, Skill, Certification, Employee, EmployeeSkill, EmployeeCertification
from apps.accounts.models import User
from apps.organizations.models import Organization, Department, Office, Team

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'user', 'employee_id', 'organization', 'department', 'office', 
            'team', 'designation', 'supervisor', 'employment_type', 'status',
            'date_of_joining', 'salary', 'emergency_contact_name', 'emergency_contact_phone'
        ]
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'EMP-2026-0042'}),
            'organization': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'office': forms.Select(attrs={'class': 'form-select'}),
            'team': forms.Select(attrs={'class': 'form-select'}),
            'designation': forms.Select(attrs={'class': 'form-select'}),
            'supervisor': forms.Select(attrs={'class': 'form-select'}),
            'employment_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'date_of_joining': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Person Full Name'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 234-5678'}),
        }


class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['title', 'code', 'level', 'pay_grade', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Senior Structural Bridge Engineer'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DES-SSBE'}),
            'level': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'pay_grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GRADE-GS-13'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'category', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bridge Scour Depth Sonar Analysis'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'code', 'issuing_body', 'validity_years', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Certified Bridge Inspector (CBI)'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CERT-CBI-FHWA'}),
            'issuing_body': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Federal Highway Administration'}),
            'validity_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class EmployeeSkillForm(forms.ModelForm):
    class Meta:
        model = EmployeeSkill
        fields = ['skill', 'proficiency', 'years_experience']
        widgets = {
            'skill': forms.Select(attrs={'class': 'form-select'}),
            'proficiency': forms.Select(attrs={'class': 'form-select'}),
            'years_experience': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
        }


class EmployeeCertificationForm(forms.ModelForm):
    class Meta:
        model = EmployeeCertification
        fields = ['certification', 'certificate_number', 'issue_date', 'expiry_date', 'certificate_file', 'is_verified']
        widgets = {
            'certification': forms.Select(attrs={'class': 'form-select'}),
            'certificate_number': forms.TextInput(attrs={'class': 'form-control'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'certificate_file': forms.FileInput(attrs={'class': 'form-control'}),
            'is_verified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
