from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Allergy(models.Model):
    name = models.CharField("Аллергия", max_length=200, db_index=True)

    class Meta:
        verbose_name = "Аллергия"
        verbose_name_plural = "Аллергии"

    def __str__(self):
        return f"{self.name}"


class RecipeType(models.Model):
    name = models.CharField("Категория рецепта", max_length=200, db_index=True)

    class Meta:
        verbose_name = "Категория рецепта"
        verbose_name_plural = "Категория рецепта"

    def __str__(self):
        return f"{self.name}"


class Recipe(models.Model):
    name = models.CharField("Название рецепта", max_length=200, db_index=True)
    description = models.TextField(
        "Описание",
        blank=True,
        null=True
    )
    cooking_steps = ingredients = models.TextField("Шаги приготовления", max_length=600)
    calories = models.PositiveIntegerField("Кол-во калорий", validators=[MinValueValidator(0)])
    image_file = models.ImageField("Изображение")
    recipe_type = models.ForeignKey(
        RecipeType, on_delete=models.CASCADE, verbose_name="Тип рецепта", related_name="recipe"
    )
    ingredients = models.TextField("Ингридиенты", max_length=300)
    new_year_flag = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    PAY_STATUS = [
        ("Оплачен", "Оплачен"),
        ("Не оплачен", "Не оплачен")
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="subscription"
    )
    start_date = models.DateField("Дата начала", auto_now_add=True, db_index=True)
    end_date = models.DateField("Дата окончания", db_index=True)
    breakfast = models.BooleanField("Завтрак", default=False)
    lunch = models.BooleanField("Обед", default=False)
    dinner = models.BooleanField("Ужин", default=False)
    desserts = models.BooleanField("Десерт", default=False)
    new_year = models.BooleanField("Новогоднее меню", default=False)
    persons = models.PositiveIntegerField(
        "Кол-во персон",
        default=1,
        validators=[MinValueValidator(0)]
    )
    allergy = models.ForeignKey(
        Allergy,
        on_delete=models.CASCADE,
        verbose_name="Аллергия",
        related_name="subscription",
        null=True,
        blank=True
    )
    price = models.PositiveIntegerField("Цена подписки", validators=[MinValueValidator(0)])
    pay_status = models.CharField(
        "Статус оплаты",
        max_length=50,
        choices=PAY_STATUS,
        default="Не оплачен"
        )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.id} Дата окончания - {self.end_date}"


class Rate(models.Model):
    recipe_type = recipe_type = models.ForeignKey(
        RecipeType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Тип рецепта",
        related_name="rate"
    )
    allergy = models.ForeignKey(
        Allergy,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Аллергия",
        related_name="rate"
    )
    price = models.FloatField(default=0.0, verbose_name="Стоимость")

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

    def __str__(self):
        return f"{self.recipe_type}{self.allergy} - {self.price}"
