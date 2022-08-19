# Generated by Django 4.1 on 2022-08-19 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Ingerdient",
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
                (
                    "name",
                    models.CharField(
                        max_length=200, unique=True, verbose_name="Ingerdient name"
                    ),
                ),
                (
                    "measurement_unit",
                    models.CharField(max_length=200, verbose_name="Measuring unit"),
                ),
            ],
            options={
                "verbose_name": "Ingerdient",
                "verbose_name_plural": "Ingerdients",
                "ordering": ["name"],
            },
        ),
    ]
