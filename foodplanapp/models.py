from django.core.validators import MinValueValidator
from django.db import models


class RecipePeriod(models.Model):
    name = models.CharField("Время приема", max_length=200, db_index=True)

    class Meta:
        verbose_name = "Время приема"
        verbose_name_plural = "Время приемов"

    def __str__(self):
        return f"{self.name}"


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
    calories = models.PositiveIntegerField("Кол-во калорий", validators=[MinValueValidator(0)])
    image_file = models.ImageField("Изображение")
    recipe_type = models.ForeignKey(
        RecipeType, on_delete=models.CASCADE, verbose_name="Тип рецепта", related_name="recipe"
    )
    allergy = models.ForeignKey(
        Allergy, on_delete=models.CASCADE, verbose_name="Аллергия", related_name="recipe"
    )
    period = models.ForeignKey(
        RecipePeriod, on_delete=models.CASCADE, verbose_name="Время приема", related_name="recipe"
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return f"{self.name}"


class Subscription(models.Model):
    name = models.CharField("Название подписки", max_length=200, db_index=True)
    price = models.PositiveIntegerField("Цена подписки", validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.name}"
