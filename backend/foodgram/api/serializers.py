from django.db.models import F
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    IntegerField,
    PrimaryKeyRelatedField,
)

from drf_extra_fields.fields import Base64ImageField

from recipes.models import (
    Tag,
    Recipe,
    Ingredient,
    IngredientInRecipe,
)
from users.models import Subscription
from users.serializers import (
    BaseUserSerializer,
    USER_REQUIRED_FIELDS,
)


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInRecipeSerializer(ModelSerializer):
    id = IntegerField(write_only=True)

    class Meta:
        model = IngredientInRecipe
        fields = (
            'id',
            'amount',
        )


class BaseRecipeSerializer(ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscribeSerializer(BaseUserSerializer):
    recipes_count = SerializerMethodField()
    recipes = SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        fields = (
            *BaseUserSerializer.Meta.fields,
            'recipes_count',
            'recipes',
        )
        read_only_fields = USER_REQUIRED_FIELDS

    def validate(self, data):
        author = self.instance
        user = self.context.get('request').user
        if Subscription.objects.filter(author=author, user=user).exists():
            raise ValidationError(
                detail=f'Вы уже подписаны на пользователя {author.first_name}',
                code=status.HTTP_400_BAD_REQUEST
            )
        if user == author:
            raise ValidationError(
                detail='Нельзя подписаться на себя',
                code=status.HTTP_400_BAD_REQUEST
            )
        return data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = (
            obj.recipes.all()[:int(limit)]
            if limit else obj.recipes.all()
        )
        serializer = BaseRecipeSerializer(
            recipes,
            many=True,
            read_only=True,
        )
        serializer.is_valid(raise_exception=True)
        return serializer.data


class RecipeReadSerializer(ModelSerializer):
    tags = TagSerializer(
        many=True,
        read_only=True,
    )
    author = BaseUserSerializer(
        read_only=True,
    )
    ingredients = SerializerMethodField()
    image = Base64ImageField()
    is_favorited = SerializerMethodField(
        read_only=True,
    )
    is_in_shopping_cart = SerializerMethodField(
        read_only=True,
    )

    def get_ingredients(self, obj):
        ingredients = obj.ingredients.all()
        return [
            {
                'id': ingredient.id,
                'name': ingredient.name,
                'measurement_unit': ingredient.measurement_unit,
                'amount': ingredient_in_recipe.amount,
            }
            for ingredient in ingredients
            for ingredient_in_recipe in obj.ingredient_list.filter(ingredient=ingredient)
        ]

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return (not user.is_anonymous
                and user.favorites.filter(
                    recipe=obj,
                ).exists())

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return (not user.is_anonymous
                and user.shopping_cart.filter(
                    recipe=obj,
                ).exists())

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'text',
            'tags',
            'author',
            'ingredients',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        )


class RecipeModifySerializer(ModelSerializer):
    author = BaseUserSerializer(read_only=True)
    tags = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    ingredients = IngredientInRecipeSerializer(many=True)
    image = Base64ImageField()

    def validate_tags(self, value):
        if not value:
            raise ValidationError({
                'tags': 'Выберите хотя бы один тег'
            })

        return value

    def validate_ingredients(self, value):
        if not value:
            raise ValidationError({
                'ingredients': 'Выберите хотя бы один ингредиент'
            })

        return value

    @transaction.atomic
    def create_ingredients_amounts(self, ingredients, recipe):
        IngredientInRecipe.objects.bulk_create([
            IngredientInRecipe(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount'],
            )
            for ingredient in ingredients
        ])

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients_amounts(
            recipe=recipe,
            ingredients=ingredients,
        )
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients_amounts(
            recipe=instance,
            ingredients=ingredients,
        )
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance,
            context={'request': self.context.get('request')},
        ).data

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )
