from djoser.views import UserViewSet

from .serializers import CustomUserSerializer
from .models import User


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
