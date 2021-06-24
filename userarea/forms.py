from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm
from django import forms
from .models import *


class EditProfileForm(UserChangeForm):
    # email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password')
