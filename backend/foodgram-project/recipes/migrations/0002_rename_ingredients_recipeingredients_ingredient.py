# Generated by Django 4.1 on 2022-08-21 02:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="recipeingredients",
            old_name="ingredients",
            new_name="ingredient",
        ),
    ]
