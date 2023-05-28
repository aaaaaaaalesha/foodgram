from django_filters.rest_framework import FilterSet, filters

from recipes.models import (
    Ingredient,
    Recipe,
    Tag,
)


class IngredientFilterSet(FilterSet):
    name = filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilterSet(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited'
    )

    def filter_is_favorited(self, queryset, name, value):
        """Рецепты в списке избранного."""
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(favorites__user=user)

        return queryset

    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    def filter_is_in_shopping_cart(self, queryset, name, value):
        """Рецепты в списке покупок."""
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(shopping_cart__user=user)

        return queryset

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
        )
