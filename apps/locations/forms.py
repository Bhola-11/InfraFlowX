from django import forms
from .models import Location

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = [
            'organization', 'name', 'code', 'country', 'state',
            'city', 'district', 'zone', 'area', 'address',
            'postal_code', 'latitude', 'longitude', 'elevation_meters'
        ]
        widgets = {
            'organization': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. North Metropolitan Expressway Overpass'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GIS-LOC-9021'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'California'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'San Francisco'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bay Area North'}),
            'zone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zone A'}),
            'area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Downtown Sector 4'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0000001', 'placeholder': '37.7749295'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0000001', 'placeholder': '-122.4194155'}),
            'elevation_meters': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
