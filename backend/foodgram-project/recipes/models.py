from colorfield.fields import ColorField
from django.db import models

from ingredients.models import Ingredient
from users.models import User

from .validators import validator_not_zero


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Tag name",
        unique=True,
        blank=False,
        null=False,
    )
    color = ColorField(
        verbose_name="Color",
        unique=True,
        null=True,
    )
    slug = models.SlugField(
        verbose_name="Slug",
        max_length=200,
        null=True,
        blank=False,
        unique=True,
    )

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.name} [{self.color}]"


class Recipe(models.Model):
    name = models.CharField(
        verbose_name="Recipe name",
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
        validators=(validator_not_zero,),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Author",
        blank=False,
        null=False,
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name="Tags",
        related_name="recipes",
    )

    favorite = models.ManyToManyField(
        User,
        verbose_name="Favorites",
        related_name="favorite_recipes",
        blank=True,
    )

    shopping_card = models.ManyToManyField(
        User,
        verbose_name="In shopping card",
        related_name="shopping_recipes",
        blank=True,
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Publish date",
    )

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"
        ordering = ["-pub_date"]
        indexes = [
            models.Index(fields=["-pub_date"]),
        ]

    def __str__(self):
        return self.name

    @property
    def favorite_count(self):
        return self.favorite.count()


class RecipeIngredients(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        related_name="recipe_ingredients",
        verbose_name="Ingredients",
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="recipe_ingredients",
        verbose_name="Recipe",
        on_delete=models.CASCADE,
    )

    amount = models.PositiveIntegerField(
        verbose_name="Amount",
        blank=False,
        null=False,
        validators=(validator_not_zero,),
    )

    class Meta:
        verbose_name = "Recipe ingredients"
        verbose_name_plural = "Recipe ingredients"
        constraints = [
            models.UniqueConstraint(
                fields=["ingredient", "recipe"],
                name="unique_recipe_ingredient",
            )
        ]

    def __str__(self):
        return f"{self.ingredient} in {self.recipe}"
