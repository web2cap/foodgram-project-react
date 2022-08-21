from django.conf import settings
from django.shortcuts import get_object_or_404
from ingrediens.models import Ingerdient
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User

from .permissions import OnlyGet, RegisterUserProfileOrAutorised
from .serializers import (
    IngerdientSerializer,
    UserInstanceSerializer,
    UserSerializer,
    UserSetPasswordSerializer,
    UserSignupSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet API for user managment.
    Requests to instance by username.
    When referring to /me/, the user completes/gets himself."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (RegisterUserProfileOrAutorised,)
    lookup_field = "username"

    def create(self, request, *args, **kwargs):
        """User self-registration.
        Uses UserSignupSerializer.
        """

        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )

    def retrieve(self, request, username=None):
        """Getting a user instance by username.
        When requested for /me/, returns the user himself."""

        if username == "me":
            username = request.user.username
        user = get_object_or_404(self.queryset, username=username)

        serializer = UserInstanceSerializer(user)
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


class IngredientViewSet(viewsets.ModelViewSet):
    """ViewSet for Ingredients.
    Support only GET, limited by permissoun.
    Support search bu name."""

    queryset = Ingerdient.objects.all()
    serializer_class = IngerdientSerializer
    permission_classes = (OnlyGet,)
