from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status

from ingredients.models import Ingredient
from recipes.models import Recipe, RecipeIngredients, Tag
from users.models import User

from .exceptions import CustomAPIException

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
            return (
                request.user.is_authenticated
                and request.user.follower.filter(follow=obj).exists()
            )
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


class IngredientSerializer(serializers.ModelSerializer):
    """Ingredien Serializer."""

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class RecipeIngredientsSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.IntegerField(source="ingredient.id")
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
        fields = ("id", "name", "color", "slug")


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe."""

    author = UserSerializer(required=False)
    ingredients = RecipeIngredientsSerializer(
        source="recipe_ingredients",
        many=True,
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_list = serializers.ListField(
        write_only=True, child=serializers.IntegerField(min_value=1)
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

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
            "tag_list",
            "is_favorited",
            "is_in_shopping_cart",
        )

    def add_ingredients_tags(self, instance, ingredients, tags):
        recipe_ingredients = list()
        for ingrow in ingredients:
            recipe_ingredients.append(
                RecipeIngredients(
                    ingredient=get_object_or_404(
                        Ingredient, id=ingrow["ingredient"]["id"]
                    ),
                    recipe=instance,
                    amount=ingrow["amount"],
                )
            )
        RecipeIngredients.objects.bulk_create(recipe_ingredients)

        instance.tags.set(tags)

    def check_ingredients(self, ingredients):
        if not len(ingredients):
            raise serializers.ValidationError(MESSAGES["ingredients_requared"])

    def create(self, validated_data):

        validated_data["author"] = self.context["request"].user
        recipe_ingredients = validated_data.pop("recipe_ingredients")
        self.check_ingredients(recipe_ingredients)
        tag_list = validated_data.pop("tag_list")
        instance = Recipe.objects.create(**validated_data)
        self.add_ingredients_tags(instance, recipe_ingredients, tag_list)
        return instance

    def update(self, instance, validated_data):

        if (
            instance.author != self.context["request"].user
            and not self.context["request"].user.is_superuser
        ):
            raise CustomAPIException(
                {"message": MESSAGES["patch_only_author"]},
                status_code=status.HTTP_403_FORBIDDEN,
            )

        recipe_ingredients = validated_data.pop("recipe_ingredients")
        tag_list = validated_data.pop("tag_list")
        self.check_ingredients(recipe_ingredients)
        instance.recipe_ingredients.all().delete()
        self.add_ingredients_tags(instance, recipe_ingredients, tag_list)
        return super().update(instance, validated_data)

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return (
                request.user.is_authenticated
                and obj.favorite.filter(id=request.user.id).exists()
            )
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return (
                request.user.is_authenticated
                and obj.shopping_card.filter(id=request.user.id).exists()
            )
        return False


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

        # Для Максима Любиева
        # не смог найти тебя в слаке, сообщил об этом куратору,

        # тут бы я всегда возвращал True как в прошлой версии,
        # т.к. это подписки пользователя и из этого списка
        # пользователь на всех подписан по логике. Но я переделал)

        # данный комент удалю ко второму этапу, сорри

        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return (
                request.user.is_authenticated
                and request.user.follower.filter(follow=obj).exists()
            )
        return False

    def get_recipes_count(self, obj):
        return obj.recipes_count
