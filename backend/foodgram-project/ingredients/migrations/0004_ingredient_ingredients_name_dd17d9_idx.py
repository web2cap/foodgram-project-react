# Generated by Django 4.1 on 2022-09-04 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ingredients", "0003_delete_ingerdient_and_more"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="ingredient",
            index=models.Index(
                fields=["name"],
                name="ingredients_name_dd17d9_idx"
            ),
        ),
    ]
