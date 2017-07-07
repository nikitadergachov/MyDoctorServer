from django import forms
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.views.generic import FormView
from django.contrib.auth.forms import AuthenticationForm

from mydoctor.models import MyUser, Patient, Procedure, VisitDoctor, Analysis, Medicine


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Электронная почта', 'required': ''}))
    password = forms.CharField(
        widget=forms.PasswordInput({'class': 'form-control', 'placeholder': 'Пароль', 'required': '', 'minlength': 6}))

    def clean_email(self):
        form_email = self.cleaned_data['email']
        result = MyUser.objects.filter(email=form_email)
        if not result:
            raise ValidationError('Пользователя с таким email не существует')
        return form_email



class RegistrationForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ['name', 'email', 'phone_number', 'password']
        localized_fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'ФИО', 'required': '', 'minlength': 6}),
            'email': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Электронная почта', 'required': '', }),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                'Номер телефона', 'required': '', 'minlength': 12, 'maxlength': 12}),
            'password': forms.PasswordInput(
                attrs={'class': 'form-control', 'placeholder': 'Пароль', 'required': '', 'minlength': 6}),
        }


class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'phone_number', 'email', 'insurance_number', 'DOB', 'password']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'ФИО', 'minlength': 6}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                'Номер телефона', 'required': '', 'minlength': 12, 'maxlength': 12}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                'Электронная почта', 'required': '', 'type': 'email'}),
            'insurance_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Номер полиса', 'required': '', 'minlength': 4}),
            'DOB': forms.DateInput(attrs={'class': 'form-control datepicker',
                                          'placeholder': 'Дата рождения', 'type': 'date'}),
            'password': forms.PasswordInput(
                {'class': 'form-control', 'placeholder': 'Пароль', 'required': '', 'minlength': 6})

        }


class ProcedureForm(ModelForm):
    class Meta:
        model = Procedure
        fields = ['name', 'description', 'number']


class VisitDoctorForm(ModelForm):
    class Meta:
        model = VisitDoctor
        fields = ['name_doctor', 'description']


class AnalysisForm(ModelForm):
    class Meta:
        model = Analysis
        fields = ['name', 'description']


class MedicinesForm(ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'type', 'method_reception', 'dosage', 'number_of_receptions_per_day', 'number_medicines',
                  'description', 'after_meals', 'start_date', 'end_date']

        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'type': 'date'}),
        }
