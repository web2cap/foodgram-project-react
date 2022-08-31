# Generated by Django 4.1 on 2022-08-31 15:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0011_alter_recipeingredients_ingredient"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="pub_date",
            field=models.DateTimeField(
                default=datetime.datetime.now, verbose_name="Publish date"
            ),
        ),
    ]
