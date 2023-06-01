from django.db import transaction
from rest_framework import status
from drf_extra_fields.fields import Base64ImageField
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    SerializerMethodField,
    PrimaryKeyRelatedField,
)

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
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IngredientInRecipeSerializer(ModelSerializer):
    id = PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id'
    )
    name = CharField(
        read_only=True,
        source='ingredient.name'
    )
    measurement_unit = CharField(
        read_only=True,
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
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


class RecipeReadSerializer(ModelSerializer):
    tags = TagSerializer(
        many=True,
        read_only=True,
    )
    author = BaseUserSerializer(
        read_only=True,
    )
    ingredients = IngredientInRecipeSerializer(
        source='ingredient_list',
        many=True,
    )
    image = Base64ImageField()
    is_favorited = SerializerMethodField(
        read_only=True,
    )
    is_in_shopping_cart = SerializerMethodField(
        read_only=True,
    )

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

    @staticmethod
    def validate_tags(value):
        if not value:
            raise ValidationError({
                'tags': 'Выберите хотя бы один тег'
            })

        return value

    @staticmethod
    def validate_ingredients(value):
        if not value:
            raise ValidationError({
                'ingredients': 'Выберите хотя бы один ингредиент'
            })

        ingredients = [
            ingredient_in_recipe['ingredient']['id']
            for ingredient_in_recipe in value
        ]
        if len(ingredients) != len(set(ingredients)):
            raise ValidationError({
                'ingredients': 'Ингредиенты не должны дублироваться'
            })

        return value

    @transaction.atomic
    def create_ingredients_amounts(self, ingredients, recipe):
        IngredientInRecipe.objects.bulk_create([
            IngredientInRecipe(
                ingredient=ingredient['ingredient']['id'],
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


class SubscribeSerializer(BaseUserSerializer):
    recipes_count = SerializerMethodField()
    recipes = SerializerMethodField()

    @staticmethod
    def get_recipes_count(obj):
        return obj.recipes.count()

    class Meta(BaseUserSerializer.Meta):
        fields = (
            *BaseUserSerializer.Meta.fields,
            'recipes_count',
            'recipes',
        )
        read_only_fields = USER_REQUIRED_FIELDS

    def save(self, **kwargs):
        user = self.context.get('request').user
        author = self.instance
        Subscription.objects.create(user=user, author=author)
        return super().save(**kwargs)

    def validate(self, data):
        author = self.instance
        user = self.context.get('request').user
        if Subscription.objects.filter(
                author=author,
                user=user,
        ).exists():
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
        return serializer.data
