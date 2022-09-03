# Generated by Django 4.1 on 2022-08-30 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ingredients", "0002_ingredient"),
        ("recipes", "0011_alter_recipeingredients_ingredient"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Ingerdient",
        ),
        migrations.AddConstraint(
            model_name="ingredient",
            constraint=models.UniqueConstraint(
                fields=("name", "measurement_unit"),
                name="unique_ingredient_in_unit",
            ),
        ),
    ]
