from django import forms
from .models import Property, PropertyImage, PropertyInquiry


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'property_type', 'status', 'description',
            'address', 'city', 'state_province', 'country',
            'total_units', 'available_units', 'floor_area_sqm',
            'is_for_rent', 'is_for_sale', 'price_per_month', 'price_for_sale',
            'year_built', 'floors',
            'contact_name', 'contact_phone', 'contact_email',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Skyline Residences Tower A'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state_province': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State / Province'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'total_units': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'available_units': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'floor_area_sqm': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'sq. meters'}),
            'price_per_month': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'price_for_sale': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'year_built': forms.NumberInput(attrs={'class': 'form-control', 'min': 1900, 'max': 2030}),
            'floors': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'caption', 'is_primary']


PropertyImageFormSet = forms.inlineformset_factory(
    Property, PropertyImage,
    form=PropertyImageForm,
    extra=5,
    max_num=10,
)


class PropertyInquiryForm(forms.ModelForm):
    class Meta:
        model = PropertyInquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 000-0000'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell the owner about yourself and your needs...'}),
        }
