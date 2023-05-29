from django.shortcuts import get_object_or_404

from rest_framework import status, response

from recipes.models import (
    Recipe,
    ShoppingCart,
)

from api.serializers import BaseRecipeSerializer


def add_recipe_service(model, request, id_) -> response.Response:
    found_recipe = model.objects.filter(
        user=request.user,
        recipe__id=id_,
    )
    if found_recipe.exists():
        return response.Response(
            {'errors': 'Рецепт уже присутствует'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    found_recipe = get_object_or_404(Recipe, id=id_)
    serializer = BaseRecipeSerializer(found_recipe)
    serializer.is_valid(raise_exception=True)

    model.objects.create(
        user=request.user,
        recipe=found_recipe,
    )
    return response.Response(
        serializer.data,
        status=status.HTTP_201_CREATED,
    )


def delete_recipe_service(model, request, id_):
    found_recipe = model.objects.filter(
        user=request.user,
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
