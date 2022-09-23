from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    username_validator = UnicodeUsernameValidator()
    email = forms.EmailField()
    username = forms.CharField(validators=[username_validator])
    password1 = forms.CharField(required=False, validators=[password_validation.validate_password])
    password2 = forms.CharField(required=False, validators=[password_validation.validate_password])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)