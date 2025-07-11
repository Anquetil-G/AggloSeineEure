from django import forms
from .models import CustomUser, Department, Contact, Commune
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number')

class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number')

class CustomUserCreationFormAdmin(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'rank', 'administrated_departments', 'administrated_communes', 'accessible_departments')
        widgets = {
            'administrated_departments': forms.SelectMultiple(attrs={
                'class': 'classic_input select2',
                'style': 'width: 100%;'
            }),
            'administrated_communes': forms.SelectMultiple(attrs={
                'class': 'classic_input select2',
                'style': 'width: 100%;'
            }),
            'accessible_departments': forms.SelectMultiple(attrs={
                'class': 'classic_input select2',
                'style': 'width: 100%;'
            }),
        }

class CustomUserChangeFormAdmin(UserChangeForm):
    password = None
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'rank', 'administrated_departments', 'administrated_communes', 'accessible_departments')
        widgets = {
            'administrated_departments': forms.SelectMultiple(attrs={
                'class': 'classic_input select2',
                'style': 'width: 100%;'
            }),
            'administrated_communes': forms.SelectMultiple(attrs={
                'class': 'classic_input select2',
                'style': 'width: 100%;'
            }),
            'accessible_departments': forms.SelectMultiple(attrs={
                'class': 'classic_input select2',
                'style': 'width: 100%;'
            }),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

class CommuneForm(forms.ModelForm):
    class Meta:
        model = Commune
        fields = ['name', 'department']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['commune', 'full_name', 'email', 'phone_number', 'observation', 'reminder', 'document']