# Generated by Django 3.2.15 on 2022-09-21 20:26

# Generated by Django 3.2.15 on 2022-09-21 20:23

from django.db import migrations
import os
import json

class Migration(migrations.Migration):

    def add_recipes(apps, schema_editor):
        Recipe = apps.get_model('foodplanapp', 'Recipe')
        RecipeType = apps.get_model('foodplanapp', 'RecipeType')

        base_directory = '../data/breakfasts'
        recipes = os.listdir(base_directory)
        for recipe in recipes:
            with open(os.path.join(base_directory, recipe), encoding='utf-8') as file:
                recipe_content = json.load(file)
                title,\
                discription,\
                calories,\
                ingredients,\
                steps = recipe_content.values()
                recipe_type = RecipeType.objects.get(name='Завтрак')
                Recipe.objects.get_or_create(
                    name=title,
                    description=discription,
                    cooking_steps=' '.join(steps),
                    calories=int(calories),
                    image_file=f'{title}.jpg',
                    recipe_type=recipe_type,
                    ingredients=' '.join(ingredients)
                )

    dependencies = [
        ('foodplanapp', '0002_auto_20220921_2215'),
    ]

    operations = [
        migrations.RunPython(add_recipes)
    ]