import datetime

from django.conf import settings
from django.db.models import Count, OuterRef, Prefetch, Subquery, Sum
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ingredients.models import Ingredient
from recipes.models import Recipe, RecipeIngredients, Tag
from users.models import Subscription, User
from .filters import IngredientSearchFilter
from .permissions import (GetOrGPPDAutorized, OnlyGet, OnlyGetAutorised,
                          RegisterUserProfileOrAutorised)
from .serializers import (IngredientSerializer, RecipeSerializer,
                          RecipeShotSerializer, SubscriptionSerializer,
                          TagSerializer, UserSerializer,
                          UserSetPasswordSerializer)
from .utils import render_to_pdf

MESSAGES = getattr(settings, "MESSAGES", None)
PDF_PAGE_SIZE = getattr(settings, "PDF_PAGE_SIZE", "A4")


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet API for user managment.
    Requests to instance by username.
    When referring to /me/, the user completes/gets himself."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (RegisterUserProfileOrAutorised,)
    lookup_field = "id"

    def create(self, request):
        """User self-registration.
        Uses UserSignupSerializer.
        """

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )

    @action(detail=False, methods=["get"])
    def me(self, request):
        """Getting a user self user instance."""

        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def set_password(self, request):
        """Self change password.
        Endpoint /set_password/."""

        serializer = UserSetPasswordSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post", "delete"])
    def subscribe(self, request, id=None):
        """Subscribe for user if method POST.
        Disabled subscription to self and dowble subscription.
        Unsubscribe if method DELETE.
        Disabled unsubscription if no subscribed."""

        if int(id) == request.user.id:
            return Response(
                {"detail": MESSAGES["self_subscription"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow_user = get_object_or_404(User, id=id)
        me = get_object_or_404(User, id=request.user.id)

        if request._request.method == "POST":
            if me.follower.filter(follow=follow_user).exists():
                return Response(
                    {"detail": MESSAGES["double_subscription"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            me.follower.create(follow=follow_user)
            serializer = SubscriptionSerializer(
                follow_user,
                context={"request": request},
            )
            return Response(serializer.data)

        if not me.follower.filter(follow=follow_user).exists():
            return Response(
                {"detail": MESSAGES["no_subscribed"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        me.follower.filter(follow=follow_user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ModelViewSet):
    """ViewSet for Ingredients.
    Support only GET, limited by permissoun.
    Support search bu name."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (OnlyGet,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ("^name",)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet for Recipes."""

    serializer_class = RecipeSerializer
    permission_classes = (GetOrGPPDAutorized,)

    def get_queryset(self):
        queryset = Recipe.objects.all()

        tag_list = self.request.GET.getlist("tags")
        if tag_list:
            queryset = queryset.filter(tags__slug__in=tag_list).distinct()

        author = self.request.GET.get("author")
        if author:
            queryset = queryset.filter(author__id=author)

        if not self.request.user.is_authenticated:
            return queryset

        if self.request.GET.get("is_in_shopping_cart"):
            queryset = queryset.filter(shopping_card=self.request.user)

        if self.request.GET.get("is_favorited"):
            queryset = queryset.filter(favorite=self.request.user)

        return queryset

    def create(self, request, *args, **kwargs):
        request.data["tag_list"] = request.data.pop("tags")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.data["tag_list"] = request.data.pop("tags")
        return super().update(request, *args, **kwargs)

    def add_remove_m2m_relation(
        self, request, model_main, model_mgr, pk, serializer_class
    ):
        """Add many to many relation to user model if POST method.
        Disabled double records.
        Delete many to many relation if method DELETE.
        Disabled delete if relation doesn't exists.
        """

        main = get_object_or_404(model_main, pk=pk)
        manager = getattr(main, model_mgr)

        if request._request.method == "POST":
            if manager.filter(id=request.user.id).exists():
                return Response(
                    {"detail": MESSAGES["relation_already_exists"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            manager.add(request.user)
            serializer = serializer_class(main)
            return Response(serializer.data)

        if not manager.filter(id=request.user.id).exists():
            return Response(
                {"detail": MESSAGES["relation_not_exists"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        manager.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post", "delete"])
    def favorite(self, request, pk=None):
        """Add to favorite recipe if POST method.
        Delete recipe from favorite if method DELETE.
        """

        return self.add_remove_m2m_relation(
            request, Recipe, "favorite", pk, RecipeShotSerializer
        )

    @action(detail=True, methods=["post", "delete"])
    def shopping_cart(self, request, pk=None):
        """Add to user shopping card recipe if POST method.
        Delete recipe from shopping card if method DELETE.
        """

        return self.add_remove_m2m_relation(
            request, Recipe, "shopping_card", pk, RecipeShotSerializer
        )

    @action(detail=False, methods=["get"])
    def download_shopping_cart(self, request):

        card_recipes = Recipe.objects.filter(shopping_card=request.user)
        card_ingredients = (
            RecipeIngredients.objects.filter(recipe__in=card_recipes)
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(amount=Sum("amount"))
        )

        timenow = datetime.datetime.now()
        time_label = timenow.strftime("%b %d %Y %H:%M:%S")
        template_card = "download_shopping_cart.html"
        context = {
            "pagesize": PDF_PAGE_SIZE,
            "card_recipes": card_recipes,
            "card_ingredients": card_ingredients,
            "time_label": time_label,
            "about": MESSAGES["pdf_about"],
        }
        return render_to_pdf(template_card, context)


class TagViewSet(viewsets.ModelViewSet):
    """ViewSet for Recipes."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (OnlyGet,)
    pagination_class = None


class SubscriptionViewSet(viewsets.ModelViewSet):

    serializer_class = SubscriptionSerializer
    permission_classes = (OnlyGetAutorised,)

    def get_queryset(self):
        user = self.request.user
        followed_people = Subscription.objects.filter(follower=user).values(
            "follow"
        )
        subscription = User.objects.filter(id__in=followed_people).annotate(
            recipes_count=Count("recipes")
        )
        recipes_limit = int(self.request.GET.get("recipes_limit"))
        if not recipes_limit:
            return subscription

        subqry = Subquery(
            Recipe.objects.filter(author=OuterRef("author")).values_list(
                "id", flat=True
            )[:recipes_limit]
        )
        subscription = subscription.prefetch_related(
            Prefetch("recipes", queryset=Recipe.objects.filter(id__in=subqry))
        )
        return subscription
