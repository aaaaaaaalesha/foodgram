from rest_framework import (
    mixins,
    viewsets,
    pagination,
)

from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
)

from django_filters.rest_framework import DjangoFilterBackend

from .permissions import (
    IsAdminOrReadOnly,
    IsAuthorOrReadOnly,
)

from .serializers import (
    TagSerializer,
    IngredientSerializer,
)

from .filters import (
    IngredientFilterSet,
    RecipeFilterSet,
)


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
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilterSet
