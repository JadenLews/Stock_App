from django import forms
from django.conf import settings
from django.forms import ModelForm
# import pdb
#from django.utils.translation import ugettext_lazy as _
import logging
from .models import *
from django.contrib.auth.forms import *
from django.contrib.auth.models import User



class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=101)
    last_name = forms.CharField(max_length=101)
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


