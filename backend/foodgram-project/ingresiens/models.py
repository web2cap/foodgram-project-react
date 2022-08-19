from django.db import models


class Ingerdient(models.Model):
    name = models.CharField(
        verbose_name="Ingerdient name",
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
        verbose_name = "Ingerdient"
        verbose_name_plural = "Ingerdients"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "measurement_unit"],
                name="unique_ingerdient_in_unit",
            )
        ]

    def __str__(self):
        return self.name
