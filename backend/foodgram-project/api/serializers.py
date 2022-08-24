from dataclasses import fields

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from ingredients.models import Ingerdient
from recipes.models import Recipe, RecipeIngredients, Tag
from rest_framework import serializers
from users.models import Subscription, User

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
        )
        lookup_field = "username"


class UserInstanceSerializer(serializers.ModelSerializer):
    """User Instance Serializer."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
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


class UserSetPasswordSerializer(serializers.ModelSerializer):
    """Self change password serializer.
    Maked core password validation.
    """

    new_password = serializers.CharField(max_length=150, required=True)
    current_password = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ("password", "new_password", "current_password")
        extra_kwargs = {
            "password": {"write_only": True},
        }
        lookup_field = "username"

    def validate(self, data):
        """Maked passwords validation."""

        if not check_password(
            data["current_password"], self.instance.password
        ):
            raise serializers.ValidationError(
                {"current_password": MESSAGES["current_password_invalid"]}
            )

        try:
            validate_password(data["new_password"])
        except ValidationError as exc:
            raise serializers.ValidationError({"new_password": str(exc)})

        data["password"] = make_password(data["new_password"])
        return data


class IngerdientSerializer(serializers.ModelSerializer):
    """Ingredien Serializer."""

    class Meta:
        model = Ingerdient
        fields = ("id", "name", "measurement_unit")


class RecipeIngredientsSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipeIngredients
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


class TagSerializer(serializers.ModelSerializer):
    "Serializer for Tags."

    class Meta:
        model = Tag
        fields = ("id", "name", "colour", "slug")


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe."""

    author = UserInstanceSerializer()
    ingredients = RecipeIngredientsSerializer(
        source="recipe_ingredients", many=True
    )
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "text",
            "cooking_time",
            "author",
            "ingredients",
            "tags",
        )


class RecipeShotSerializer(serializers.ModelSerializer):
    """Serializer for Recipe.
    Shot infornation about recipe for Subscription list.
    """

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    """Subscription Serializer."""

    recipes = RecipeShotSerializer(many=True, read_only=True)
    # TODO: "is_subscribed"

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "recipes",
        )
