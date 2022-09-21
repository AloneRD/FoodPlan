from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def login(request):
    """Вход в аккаунт пользователя"""
    return render(request, 'auth.html')


def register(request):
    """Регистрация пользователя"""
    return render(request, 'registration.html')


def logout_view(request):
    """Выход пользователя."""
    return HttpResponseRedirect(reverse("index"))


def index(request):
    """Главная страница"""
    return render(request, 'index.html')
