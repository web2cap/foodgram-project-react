import csv
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):

        self.csv2orm("data/tags.csv", Tag, ["name", "color", "slug"])
        self.csv2orm(
            "data/ingredients.csv",
            Ingredient,
            ["name", "measurement_unit"],
        )

        try:
            User.objects.create_superuser(
                os.getenv("ST_ADMIN_LOGIN", default=None),
                os.getenv("ST_ADMIN_EMAIL", default=None),
                os.getenv("ST_ADMIN_PASS", default=None),
            )
        except Exception:
            pass

    def csv2orm(self, file, model, head):
        with open(file, "r", encoding="utf-8") as csvfile:
            freader = csv.DictReader(csvfile, fieldnames=head)
            for row in freader:
                try:
                    data = {h: row[h] for h in head}
                    model.objects.get_or_create(**data)
                except Exception:
                    continue
