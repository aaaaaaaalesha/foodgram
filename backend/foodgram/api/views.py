from rest_framework import (
    mixins,
    viewsets,
)

from recipes.models import (
    Tag,
    Ingredient,
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
