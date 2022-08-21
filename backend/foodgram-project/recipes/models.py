from django.db import models
from ingrediens.models import Ingerdient
from users.models import User

from .validators import validator_not_zero


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


class RecipeIngredients(models.Model):
    ingredients = models.ForeignKey(
        Ingerdient,
        related_name="recipe",
        verbose_name="Ingerdients",
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Resipe,
        related_name="ingredients",
        verbose_name="Recipe",
        on_delete=models.CASCADE,
    )

    amount = models.PositiveIntegerField(
        verbose_name="Amount",
        blank=False,
        null=False,
        validators=(validator_not_zero,),
    )
