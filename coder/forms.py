from django.contrib.auth.models import User
from .models import *
from django import forms
from django.forms.models import ModelForm
from django.forms.widgets import FileInput, TextInput, EmailInput, CheckboxInput


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'profile_image': FileInput(attrs={
                'class': "form-control",
                'style': 'max-width: 400px;',
            }),
            'username': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 400px;',
                'placeholder': 'Name'
            }),
            'first_name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 400px;',
                'placeholder': 'First Name'
            }),
            'last_name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 400px;',
                'placeholder': 'Last Name'
            }),
            'email': EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 400px;',
                'placeholder': 'Email'
            }),
            'phone': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 400px;',
                'placeholder': 'Phone Number'
            }),
            'desc': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 400px;',
                'placeholder': 'About Yourself'
            }),
        }