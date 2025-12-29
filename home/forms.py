from django import forms
from marketing.models import Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["first_name", "last_name", "email", "phone", "source"]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'john@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 000-0000'}),
            'source': forms.HiddenInput(),
        }
