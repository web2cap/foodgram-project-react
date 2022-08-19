# Generated by Django 4.1 on 2022-08-19 22:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Resipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="Resipe name")),
                (
                    "image",
                    models.ImageField(
                        upload_to="recipes/images/", verbose_name="Image"
                    ),
                ),
                ("text", models.TextField(verbose_name="Recipe text")),
                (
                    "cooking_time",
                    models.PositiveIntegerField(verbose_name="Cooking time"),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recipes",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Author",
                    ),
                ),
            ],
            options={
                "verbose_name": "Resipe",
                "verbose_name_plural": "Resipes",
                "ordering": ["name"],
            },
        ),
    ]