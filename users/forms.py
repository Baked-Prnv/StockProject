from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import *

class MyUserCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm):
        model = User
        fields = ('email',)


class MyUserChangeForm(UserChangeForm):
    
    class Meta(UserChangeForm):
        model = User
        fields = ('email',)