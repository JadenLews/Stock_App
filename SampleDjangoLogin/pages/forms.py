from django import forms
from django.conf import settings
from django.forms import ModelForm
# import pdb
#from django.utils.translation import ugettext_lazy as _
import logging
from .models import *
from django.contrib.auth.forms import *
from django.contrib.auth.models import User


class NewProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewProjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Project
        fields = '__all__'

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=101)
    last_name = forms.CharField(max_length=101)
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class StudentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Student
        fields = '__all__'

