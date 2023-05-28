from rest_framework import (
    mixins,
    viewsets,
)

from recipes.models import (
    Tag,
)

from .permissions import (
    IsAdminOrReadOnly,
    IsAuthorOrReadOnly,
)

from .serializers import (
    TagSerializer,
)


class TagViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
