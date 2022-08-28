# Generated by Django 4.1 on 2022-08-28 16:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0008_recipe_shopping_card"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="favorite",
            field=models.ManyToManyField(
                blank=True,
                related_name="favorite_recipes",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Favorites",
            ),
        ),
    ]
