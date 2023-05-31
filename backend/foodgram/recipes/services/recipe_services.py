from typing import Union
from datetime import datetime

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import status, response

from recipes.models import (
    Recipe,
    ShoppingCart,
    Favourite,
    IngredientInRecipe,
)
from users.models import User

from api.serializers import BaseRecipeSerializer


def add_recipe_service(
        model: Union[ShoppingCart, Favourite],
        user: User,
        id_: int,
) -> response.Response:
    """
    Удаление рецепта по идентификатору из сущности переданной модели.
    Модель должна иметь внешние ключи на сущности User и Recipe.
    """
    found_recipe = model.objects.filter(
        user=user,
        recipe__id=id_,
    )
    if found_recipe.exists():
        return response.Response(
            {'errors': 'Рецепт уже присутствует'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    found_recipe = get_object_or_404(Recipe, id=id_)
    serializer = BaseRecipeSerializer(found_recipe)

    model.objects.create(
        user=user,
        recipe=found_recipe,
    )
    return response.Response(
        serializer.data,
        status=status.HTTP_201_CREATED,
    )


def delete_recipe_service(
        model: Union[ShoppingCart, Favourite],
        user: User,
        id_: int,
) -> response.Response:
    """
    Удаление рецепта по идентификатору из сущности переданной модели.
    Модель должна иметь внешние ключи на сущности User и Recipe.
    """
    found_recipe = model.objects.filter(
        user=user,
        recipe__id=id_,
    )

    if found_recipe.exists():
        found_recipe.delete()
        return response.Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    return response.Response(
        {'errors': 'Рецепта уже не существует'},
        status=status.HTTP_400_BAD_REQUEST,
    )


def collect_shopping_cart(user: User):
    """Формирование списка покупок для пользователя на основе добавленных рецептов."""
    if not user.shopping_cart.exists():
        return response.Response(
            status=status.HTTP_400_BAD_REQUEST,
        )

    ingredients = IngredientInRecipe.objects.filter(
        recipe__shopping_cart__user=user,
    ).values(
        'ingredient__name',
        'ingredient__measurement_unit',
    ).annotate(amount=Sum('amount'))

    ingredient_list = '\n'.join(
        f'• {ingredient["ingredient__name"]} '
        f'- {ingredient["amount"]} '
        f'({ingredient["ingredient__measurement_unit"]})'
        for ingredient in ingredients
    )
    resp = HttpResponse(
        (
            f'Список покупок пользователя {user.get_full_name()}\n\n'
            f'Дата: {datetime.today():%Y-%m-%d}\n\n{ingredient_list}'
        ),
        content_type='text/plain',
    )
    resp['Content-Disposition'] = (
        'attachment; '
        f'filename={user.username}_shopping_list.txt'
    )
    return resp
