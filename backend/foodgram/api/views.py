from rest_framework import (
    mixins,
    viewsets,
    pagination,
    decorators,
    permissions,
)
from django_filters.rest_framework import DjangoFilterBackend

from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    ShoppingCart,
    Favourite,
    IngredientInRecipe,
)
from .permissions import (
    IsAdminOrReadOnly,
    IsAuthorOrReadOnly,
    SAFE_METHODS,
)
from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeModifySerializer,
    RecipeReadSerializer,
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

    @staticmethod
    def __recipe_handler(model, request, pk):
        if request.method == 'POST':
            # Добавление рецепта в экземпляр модели.
            return recipe_services.add_recipe_service(
                model=model,
                user=request.user,
                id_=pk,
            )

        # Удаление рецепта из экземпляра модели.
        return recipe_services.delete_recipe_service(
            model=model,
            user=request.user,
            id_=pk,
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return RecipeModifySerializer

        return RecipeReadSerializer

    @decorators.action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        return self.__recipe_handler(ShoppingCart, request, pk)

    @decorators.action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request, pk):
        return self.__recipe_handler(Favourite, request, pk)

    @decorators.action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        return recipe_services.collect_shopping_cart(request.user)
