from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from ingredients.models import Ingerdient
from recipes.models import Recipe, RecipeIngredients, Tag
from rest_framework import serializers
from users.models import User

MESSAGES = getattr(settings, "MESSAGES", None)


class UserSerializer(serializers.ModelSerializer):
    """New user self registration serializer.
    Disabled 'me' username.
    Maked core password validation.
    """

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "is_subscribed",
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

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            if (
                request.user.is_authenticated
                and request.user.follower.filter(follow=obj).exists()
            ):
                return True
        return False


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

    author = UserSerializer()
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
    Shot infornation about recipe for Subscription list and favorites.
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
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "recipes",
            "recipes_count",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        return True

    def get_recipes_count(self, obj):
        return obj.recipes.count()
