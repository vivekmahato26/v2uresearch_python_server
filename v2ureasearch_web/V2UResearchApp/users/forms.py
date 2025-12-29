from django import forms
from django.forms import ModelForm, PasswordInput
from .models import User

class UserForm(ModelForm):
    password = forms.CharField(widget=PasswordInput())
    class Meta:
        model = User
        exclude = []