from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from .models import Allergy


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


class OrderForm(forms.Form):
    limit = forms.ChoiceField(
        choices=[(3, 3), (12, 12)]
            )
    breakfast = forms.ChoiceField(
        choices=[(0, 0), (1, 1)]
    )
    lunch = forms.ChoiceField(
        choices=[(0, 0), (1, 1)]
    )
    dinner = forms.ChoiceField(
        choices=[(0, 0), (1, 1)]
    )
    desserts = forms.ChoiceField(
        choices=[(0, 0), (1, 1)]
    )
    new_year = forms.ChoiceField(
        choices=[(0, 0), (1, 1)]
    )
    persons = forms.ChoiceField(
        choices=[(1, 1), (2, 2), (3, 3)]
    )
    allergy = forms.ModelMultipleChoiceField(
        queryset=Allergy.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class':"form-check-input me-1"}),
        required=False
        )


class PayForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    month = forms.IntegerField(max_value=12, min_value=1)
    year = forms.IntegerField(max_value=99, min_value=1)
    cart_number = forms.CharField(max_length=16)
    cvs = forms.IntegerField(max_value=999, min_value=1)
