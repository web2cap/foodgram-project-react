# Generated by Django 4.1 on 2022-08-30 17:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ingredients", "0002_ingredient"),
        ("recipes", "0010_alter_recipe_shopping_card"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipeingredients",
            name="ingredient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipe_ingredients",
                to="ingredients.ingredient",
                verbose_name="Ingredients",
            ),
        ),
    ]
