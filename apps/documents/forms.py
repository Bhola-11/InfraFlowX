from django import forms
from .models import DocumentCategory, Document, DocumentVersion, BlueprintMetadata


class DocumentCategoryForm(forms.ModelForm):
    class Meta:
        model = DocumentCategory
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['doc_number', 'title', 'category', 'asset', 'project', 'organization', 'file',
                  'current_version', 'is_blueprint', 'confidentiality', 'status', 'tags', 'description']
        widgets = {
            'doc_number': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'asset': forms.Select(attrs={'class': 'form-select'}),
            'project': forms.Select(attrs={'class': 'form-select'}),
            'organization': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'current_version': forms.TextInput(attrs={'class': 'form-control'}),
            'is_blueprint': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'confidentiality': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. structural, bridge, inspection'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DocumentVersionForm(forms.ModelForm):
    class Meta:
        model = DocumentVersion
        fields = ['version_number', 'file', 'change_log']
        widgets = {
            'version_number': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'change_log': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class BlueprintMetadataForm(forms.ModelForm):
    class Meta:
        model = BlueprintMetadata
        fields = ['drawing_number', 'scale_ratio', 'sheet_size', 'cad_software', 'engineer_signoff_name', 'approval_date']
        widgets = {
            'drawing_number': forms.TextInput(attrs={'class': 'form-control'}),
            'scale_ratio': forms.TextInput(attrs={'class': 'form-control'}),
            'sheet_size': forms.Select(attrs={'class': 'form-select'}),
            'cad_software': forms.TextInput(attrs={'class': 'form-control'}),
            'engineer_signoff_name': forms.TextInput(attrs={'class': 'form-control'}),
            'approval_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
