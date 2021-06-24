from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm
from django import forms
from .models import *
from adminarea.models import Lead



class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)
    catid = forms.IntegerField()



class ContactForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = '__all__'
        widgets={
                   "name":forms.TextInput(attrs={'class': "form-control form-control-sm"}),
                   "phone":forms.TextInput(attrs={'class': "form-control form-control-sm"}),
                   "email":forms.TextInput(attrs={'class': "form-control form-control-sm"}),
                   "address":forms.TextInput(attrs={'class': "form-control form-control-sm"}),
                }
