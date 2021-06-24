from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm
from django import forms
from .models import *


 


class Form(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets={
                   "product":forms.Select(attrs={'class': "form-control form-control-sm"}),
                   "customer":forms.Select(attrs={'class': "form-control form-control-sm"}),
                   "status":forms.Select(attrs={'class': "form-control form-control-sm"}),
                }  


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets={
                   "name":forms.TextInput(attrs={'class': "form-control form-control-sm"}),
                   "product":forms.TextInput(attrs={'class': "form-control form-control-sm"}),
                   "vendor":forms.TextInput(attrs={'class': "form-control form-control-sm"}),
                   "discount":forms.TextInput(attrs={'class': "form-control form-control-sm"}),
                   "cost":forms.TextInput(attrs={'class': "form-control form-control-sm"}),
                } 




class CreateLead(forms.ModelForm):
    class Meta:
        model = Lead
        fields = '__all__'
        widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
        'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        'business_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business name'}),
        'business_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business type'}),
        'url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full URL including https://'}),
        'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone +1 prefix'}),
        'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Notepad'}),
    }



class UpdateLead(forms.ModelForm):
    class Meta:
        model = Lead
        fields = '__all__'
        widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
        'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        'business_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business name'}),
        'business_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business type'}),
        'url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full URL including https://'}),
        'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone +1 prefix'}),
        'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Notepad'}),
    }



class UpdateReferral(forms.ModelForm):
    class Meta:
        model = Referral
        fields = '__all__'
        widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
        'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
        'call_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Call date'}),
        'monthly_revenue': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Monthly revenue'}),
    }

