# Generated by Django 4.1 on 2022-08-21 01:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ingredients", "0001_initial"),
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipeingredients",
            name="ingredients",
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
