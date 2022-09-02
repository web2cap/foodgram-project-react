from django_filters import rest_framework as filters
from recipes.models import Recipe


class RecipesFilter(filters.FilterSet):
    """Recipes Filter ."""

    tags = filters.CharFilter(
        field_name="tags__slug",  # lookup_expr="icontains"
    )

    class Meta:
        model = Recipe
        fields = ["tags"]
