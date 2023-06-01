from rest_framework.serializers import SerializerMethodField
from djoser.serializers import UserCreateSerializer, UserSerializer

from .models import User, Subscription

USER_REQUIRED_FIELDS = (
    'email',
    'username',
    'first_name',
    'last_name',
)


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'password',
            *USER_REQUIRED_FIELDS,
        )


class BaseUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return (not user.is_anonymous
                and Subscription.objects.filter(
                    user=user,
                    author=obj,
                ).exists())

    class Meta:
        model = User
        fields = (
            'id',
            'is_subscribed',
            *USER_REQUIRED_FIELDS,
        )
