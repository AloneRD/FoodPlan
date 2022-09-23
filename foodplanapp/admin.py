from django.contrib import admin

from foodplanapp.models import Recipe, Allergy, RecipeType, Order, Rate


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_filter = ['recipe_type']


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipeType)
class RecipeTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class SubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    pass
