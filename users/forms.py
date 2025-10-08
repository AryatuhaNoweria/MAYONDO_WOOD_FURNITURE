from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Form for creating new users (with role)"""
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')
        error_messages ={
            "username":{"required":"please enter the username"},
            "email":{"required":"please enter the valid email"},
            'role':{"required":"please select the role "},
            'password1':{"required":"please the password"},
            'password2':{"required":"please confirm password"}
        }


class CustomUserChangeForm(UserChangeForm):
    """Form for updating user info"""
    class Meta:
        model = User
        fields = ('username', 'email', 'role')
        error_messages ={
            "username":{"required":"please enter the username"},
            "email":{"required":"please enter the valid email"},
         }

class Userloginform(AuthenticationForm):
    error_messages={
        "invalid_login":"please enter correct credentials"
    }