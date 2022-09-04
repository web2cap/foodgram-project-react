from django.db import models


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name="Ingredient name",
        max_length=200,
        null=False,
        blank=False,
    )

    measurement_unit = models.CharField(
        verbose_name="Measuring unit",
        max_length=200,
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "measurement_unit"],
                name="unique_ingredient_in_unit",
            )
        ]
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return self.name
