from django.shortcuts import get_object_or_404
from rest_framework import (
    status,
    mixins,
    viewsets,
    pagination,
    decorators,
    response,
)

from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    ShoppingCart,
)

from django_filters.rest_framework import DjangoFilterBackend

from .permissions import (
    IsAdminOrReadOnly,
    IsAuthorOrReadOnly,
    IsAuthenticated,
    SAFE_METHODS,
)

from .serializers import (
    TagSerializer,
    IngredientSerializer,
    BaseRecipeSerializer,
)

from .filters import (
    IngredientFilterSet,
    RecipeFilterSet,
)

from recipes.services import recipe_services


class TagViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = IngredientFilterSet
    filter_backends = (DjangoFilterBackend,)


class RecipeViewSet(viewsets.ModelViewSet):
    class RecipesPagination(pagination.PageNumberPagination):
        page_size_query_param = 'limit'

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly | IsAdminOrReadOnly,)
    pagination_class = RecipesPagination
    filterset_class = RecipeFilterSet
    filter_backends = (DjangoFilterBackend,)

    @decorators.action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, id_):
        if request.method == 'POST':
            # Добавление рецепта в список покупок.
            return recipe_services.add_recipe_service(
                model=ShoppingCart,
                request=request,
                id_=id_,
            )

        # Удаление рецепта из списка покупок.
        recipe_services.delete_recipe_service(
            model=ShoppingCart,
            request=request,
            id=id_,
        )

    # TODO: Add favorite viewset.
