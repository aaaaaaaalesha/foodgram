from djoser.serializers import UserCreateSerializer, UserSerializer

from .models import User

USER_REQUIRED_FIELDS = (
    User.USERNAME_FIELD,
    'username',
    'first_name',
    'last_name',
)


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = USER_REQUIRED_FIELDS


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            *USER_REQUIRED_FIELDS,
            'password',
        )
