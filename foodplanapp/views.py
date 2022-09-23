from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from foodplanapp.forms import UserLoginForm, UserRegisterForm
from foodplanapp.models import Order


@login_required
def lk(request):
    """Личный кабинет пользователя"""
    orders = Order.objects.filter(user=request.user).select_related('subscription__allergy')
    client_subscriptions = {}
    for order in orders:
        client_subscriptions[order] = {
            'subscription_name': order.subscription.name,
            'allergy': order.subscription.allergy.name,
            'user_day_menu': 'меню на день',  # написать функцию генерации меню на день
            'day_calories': order.subscription.day_calories,
            'portions': order.subscription.portions,
        }
    return render(request, 'lk.html', {'orders': client_subscriptions})


def authenticate_user(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user


def auth(request):
    """Вход в аккаунт пользователя"""
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate_user(email=cd['email'], password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('lk')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = UserLoginForm()
    return render(request, 'auth.html', {'form': form})


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    form = UserRegisterForm()
    return render(request, 'registration.html', {'form': form})


def logout_view(request):
    """Выход пользователя."""
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def index(request):
    """Главная страница"""
    return render(request, 'index.html')
