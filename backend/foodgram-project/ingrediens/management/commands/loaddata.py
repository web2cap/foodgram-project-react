import csv

import django.db.utils
from django.core.management.base import BaseCommand
from ingrediens.models import Ingerdient


class Command(BaseCommand):
    def handle(self, *args, **options):

        with open(
            "../../data/ingredients.csv", "r", encoding="utf-8"
        ) as csvfile:
            freader = csv.DictReader(
                csvfile, fieldnames=["name", "measurement_unit"]
            )
            for row in freader:
                try:
                    Ingerdient.objects.get_or_create(
                        name=row["name"],
                        measurement_unit=row["measurement_unit"],
                    )
                except django.db.utils.IntegrityError:
                    continue
