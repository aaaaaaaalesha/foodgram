from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TagViewSet,
    IngredientViewSet,
    RecipeFilterSet,
)

app_name = 'api'

router = DefaultRouter()

router.register(
    r'tags',
    TagViewSet,
    basename='tags',
)
router.register(
    r'ingredients',
    IngredientViewSet,
    basename='ingredients',
)
router.register(
    r'recipes',
    RecipeFilterSet,
    basename='recipes',
)

urlpatterns = [
    path('', include(router.urls)),
]
