from django.urls import include, path
from rest_framework import routers

from .views import (
    IngredientViewSet,
    RecipeViewSet,
    SubscriptionViewSet,
    TagViewSet,
    UserViewSet,
)

app_name = "api"

router = routers.DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("ingredients", IngredientViewSet, basename="ingredients")
router.register("recipes", RecipeViewSet, basename="recipes")
router.register("tags", TagViewSet, basename="tags")
router.register("subscriptions", SubscriptionViewSet, basename="subscriptions")


urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
]
