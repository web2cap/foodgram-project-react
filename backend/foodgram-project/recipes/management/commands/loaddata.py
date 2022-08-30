import csv

import django.db.utils
from django.conf import settings
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from recipes.models import Ingredient, Recipe, Tag
from users.models import User

ST_ADMIN_PASS = getattr(settings, "ST_ADMIN_PASS", None)


class Command(BaseCommand):
    def handle(self, *args, **options):

        self.csv2orm("../../data/tags.csv", Tag, ["name", "colour", "slug"])
        self.csv2orm(
            "../../data/ingredients.csv",
            Ingredient,
            ["name", "measurement_unit"],
        )
        self.csv2orm("../../data/users.csv", User, ["username", "email"])

        with open("../../data/recipes.csv", "r", encoding="utf-8") as csvfile:
            freader = csv.DictReader(
                csvfile,
                fieldnames=[
                    "name",
                    "image",
                    "text",
                    "cooking_time",
                    "author",
                    "tags",
                    "ingredients",
                ],
            )
            for row in freader:
                try:
                    author = get_object_or_404(User, username=row["author"])
                    tags = list()
                    for i in row["tags"].split("/"):
                        tags.append(get_object_or_404(Tag, slug=i))
                    ingredients = list()
                    for ia in row["ingredients"].split("/"):
                        iname, amount = ia.split(":")
                        ingredients.append(
                            {
                                "ingredient": get_object_or_404(
                                    Ingredient, name=iname
                                ),
                                "amount": amount,
                            }
                        )

                    if author and len(tags) and len(ingredients):
                        Recipe.objects.get_or_create(
                            name=row["name"],
                            image=row["image"],
                            text=row["text"],
                            cooking_time=row["cooking_time"],
                            author=author,
                        )
                        recipe = get_object_or_404(Recipe, name=row["name"])
                        for tag in tags:
                            recipe.tags.add(tag)

                        for ingredient in ingredients:
                            recipe.recipe_ingredients.create(**ingredient)

                except:
                    continue

    def csv2orm(self, file, model, head):
        with open(file, "r", encoding="utf-8") as csvfile:
            freader = csv.DictReader(csvfile, fieldnames=head)
            for row in freader:
                try:
                    data = {h: row[h] for h in head}
                    model.objects.get_or_create(**data)
                except:
                    continue
