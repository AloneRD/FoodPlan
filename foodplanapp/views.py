import random

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Sum
from django.urls import reverse
from foodplanapp.forms import UserLoginForm,\
    UserRegisterForm,\
    UserUpdateForm,\
    OrderForm,\
    PayForm
from foodplanapp.models import Order, Rate, RecipeType,Recipe
import datetime


def get_portions(order):
    portions = 0
    if order.breakfast:
        portions += 1

    if order.lunch:
        portions += 1

    if order.dinner:
        portions += 1

    if order.desserts:
        portions += 1

    return portions


def get_recipe(recipe_type, allergy=None):
    recipes = Recipe.objects.filter(recipe_type__name=recipe_type)
    with_allergy_recipes = []
    for recipe in recipes:
        if allergy:
            if allergy.name.lower() not in recipe.ingredients.lower().split():
                with_allergy_recipes.append(recipe)
    if allergy:
        recipe = random.choice(with_allergy_recipes)
    else:
        recipe = random.choice(recipes)

    return recipe


def get_day_menu(order, allergy=None):
    day_menu = {}
    day_calories = 0
    if order.breakfast:
        breakfast = get_recipe('Завтрак', allergy)
        day_menu['breakfast'] = breakfast
        day_calories += breakfast.calories
    if order.lunch:
        lunch = get_recipe('Обед', allergy)
        day_menu['lunch'] = lunch
        day_calories += lunch.calories
    if order.dinner:
        dinner = get_recipe('Ужин', allergy)
        day_menu['dinner'] = dinner
        day_calories += lunch.calories
    if order.desserts:
        desserts = get_recipe('Десерт', allergy)
        day_menu['desserts'] = desserts
        day_calories += lunch.calories

    return day_menu, day_calories


@login_required
def lk(request):
    """Личный кабинет пользователя"""
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('lk')
    else:
        form = UserUpdateForm(instance=request.user)

    orders = Order.objects.filter(user=request.user).select_related('user')
    client_subscriptions = {}
    for order in orders:
        if order.allergy:
            day_menu, day_calories = get_day_menu(order, order.allergy)
            client_subscriptions[order] = {
                'subscription_name': 'Пользовательская',
                'allergy': order.allergy,
                'user_day_menu': day_menu,
                'day_calories': day_calories,
                'portions': get_portions(order),
            }
        else:
            client_subscriptions[order] = {
                'allergy': 'Нет',
            }

    return render(
        request,
        'lk.html',
        {
            'orders': client_subscriptions,
            'form': form,
        },
    )


@login_required
def subscription(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user
            limit,\
            breakfast,\
            lunch,\
            dinner,\
            desserts,\
            new_year,\
            person,\
            allergy = cd.values()
            end_date = datetime.datetime.now().date()\
                + datetime.timedelta(days=int(limit)*30)
            price = calculate_order_cost(cd)
            order = Order.objects.create(
                user=user,
                end_date=end_date,
                breakfast=bool(breakfast),
                lunch=bool(lunch),
                dinner=bool(dinner),
                desserts=bool(desserts),
                new_year=bool(new_year),
                persons=int(person),
                price=price,
            )
            order.allergy.set(allergy)
            return redirect('pay', order_id=order.id)

    else:
        form = OrderForm()
    return render(request, 'order.html', {'form': form})


def calculate_order_cost(order):
    meals = []
    for type_tariff, presence in order.items():
        if type_tariff == "breakfast" and bool(int(presence)):
            meals.append("Завтрак")
        elif type_tariff == "lunch" and bool(int(presence)):
            meals.append("Обед")
        elif type_tariff == "dinner" and bool(int(presence)):
            meals.append("Ужин")
        elif type_tariff == "desserts" and bool(int(presence)):
            meals.append("Десерт")
    tariff_sum = Rate.objects.filter(
        Q(recipe_type__in=RecipeType.objects.filter(name__in=meals)) |
        Q(allergy__in=order['allergy'])
        ).aggregate(Sum('price'))
    total_cost = tariff_sum['price__sum'] * int(order['limit']) * int(order['persons'])
    return float(total_cost)


@login_required
def pay(request, order_id=1):
    '''Оплата подписки'''
    order = get_object_or_404(Order, pk=order_id)
    if request.method == "POST":
        form = PayForm(request.POST)
        print(form)
        if form.is_valid():
            cd = form.cleaned_data
            # Тут должна быть интеграция с платежной системой.
            return redirect('lk')
    else:
        form = PayForm()
    return render(request, 'pay_with_robokassa.html', {"order":order})


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
