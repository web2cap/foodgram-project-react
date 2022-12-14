# Generated by Django 4.1 on 2022-09-04 18:08

from django.db import migrations, models

import recipes.validators


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0015_rename_colour_tag_color"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="recipeingredients",
            options={
                "verbose_name": "Recipe ingredients",
                "verbose_name_plural": "Recipe ingredients",
            },
        ),
        migrations.AlterField(
            model_name="recipe",
            name="cooking_time",
            field=models.PositiveIntegerField(
                validators=[recipes.validators.validator_not_zero],
                verbose_name="Cooking time",
            ),
        ),
        migrations.AddConstraint(
            model_name="recipeingredients",
            constraint=models.UniqueConstraint(
                fields=("ingredient", "recipe"),
                name="unique_recipe_ingredient",
            ),
        ),
    ]
