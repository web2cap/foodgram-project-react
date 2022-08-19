from django.db import models
from users.models import User


class Resipe(models.Model):
    name = models.CharField(
        verbose_name="Resipe name",
        max_length=200,
        null=False,
        blank=False,
    )
    image = models.ImageField(
        "Image",
        upload_to="recipes/images/",
        blank=False,
        null=False,
    )
    text = models.TextField(
        verbose_name="Recipe text",
        blank=False,
        null=False,
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name="Cooking time",
        blank=False,
        null=False,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Author",
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = "Resipe"
        verbose_name_plural = "Resipes"
        ordering = ["name"]

    def __str__(self):
        return self.name
