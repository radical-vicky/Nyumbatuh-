from django import forms
from .models import PartnershipRequest


class PartnershipRequestForm(forms.ModelForm):
    class Meta:
        model = PartnershipRequest
        fields = ['property_name', 'property_address', 'city', 'unit_count', 'contact_name', 'contact_phone', 'contact_email', 'notes']
        widgets = {
            'property_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Building or development name'}),
            'property_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full street address'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any additional details about your property...'}),
        }
