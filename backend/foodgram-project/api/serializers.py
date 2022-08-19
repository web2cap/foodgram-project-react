from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from users.models import User

MESSAGES = getattr(settings, "MESSAGES", None)


class UserSerializer(serializers.ModelSerializer):
    """UserSerializer."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
        )
        lookup_field = "username"


class UserSignupSerializer(serializers.ModelSerializer):
    """New user self registration serializer.
    Disabled 'me' username.
    Maked core password validation.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(MESSAGES["username_invalid"])
        return value

    def validate_password(self, value):

        try:
            validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return make_password(value)
