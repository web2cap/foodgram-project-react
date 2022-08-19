from django.conf import settings
from rest_framework import filters, status, viewsets
from rest_framework.response import Response
from users.models import User

from .permissions import PostOrAutorised
from .serializers import UserSerializer, UserSignupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet API управления пользователями.
    Запросы к экземпляру осуществляются по username.
    При обращении на /me/ пользователь дополняет/получает свою запись."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (PostOrAutorised,)
    lookup_field = "username"

    def create(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )
