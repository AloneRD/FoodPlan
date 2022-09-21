from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
from django.urls import reverse


def login(request):
    """Вход или создание регистрация нового пользователя."""
    return render(request, 'auth.html')


def logout_view(request):
    """Выход пользователя."""
    return HttpResponseRedirect(reverse("index"))


def index(request):
    """Главная страница"""
    return render(request, 'index.html')
