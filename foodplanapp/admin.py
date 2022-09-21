from django.contrib import admin

from foodplanapp.models import Recipe, RecipePeriod, Allergy, RecipeType, Subscription


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipePeriod)
class RecipePeriodAdmin(admin.ModelAdmin):
    pass


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipeType)
class RecipeTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass
