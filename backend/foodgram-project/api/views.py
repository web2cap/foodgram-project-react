from multiprocessing import context

from django.conf import settings
from django.shortcuts import get_object_or_404
from ingredients.models import Ingerdient
from recipes.models import Recipe, Tag
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import Subscription, User

from .permissions import (
    OnlyGet,
    OnlyGetAutorised,
    RegisterUserProfileOrAutorised,
)
from .serializers import (
    IngerdientSerializer,
    RecipeSerializer,
    SubscriptionSerializer,
    TagSerializer,
    UserSerializer,
    UserSetPasswordSerializer,
)

MESSAGES = getattr(settings, "MESSAGES", None)


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

        # TODO: Check response fields
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
            serializer = SubscriptionSerializer(follow_user)
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

    queryset = Ingerdient.objects.all()
    serializer_class = IngerdientSerializer
    permission_classes = (OnlyGet,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("^name",)


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet for Recipes."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # TODO: permission
    # permission_classes = ()


class TagViewSet(viewsets.ModelViewSet):
    """ViewSet for Recipes."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (OnlyGet,)


class SubscriptionViewSet(viewsets.ModelViewSet):

    serializer_class = SubscriptionSerializer
    permission_classes = (OnlyGetAutorised,)

    def get_queryset(self):
        user = self.request.user
        followed_people = Subscription.objects.filter(follower=user).values(
            "follow"
        )
        subscription = User.objects.filter(id__in=followed_people)
        return subscription
