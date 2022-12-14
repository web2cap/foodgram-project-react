# Generated by Django 4.1 on 2022-08-21 02:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ingredients", "0001_initial"),
        ("recipes", "0002_rename_ingredients_recipeingredients_ingredient"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipeingredients",
            name="ingredient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipe_ingredients",
                to="ingredients.ingerdient",
                verbose_name="Ingerdients",
            ),
        ),
        migrations.AlterField(
            model_name="recipeingredients",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipe_ingredients",
                to="recipes.recipe",
                verbose_name="Recipe",
            ),
        ),
    ]
