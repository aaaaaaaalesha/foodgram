from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404
from rest_framework import (
    status,
    response,
    pagination,
    decorators,
    permissions,
)

from api.serializers import BaseUserSerializer, SubscribeSerializer
from .models import User, Subscription


class CustomUserViewSet(UserViewSet):
    class UserPagination(pagination.PageNumberPagination):
        page_size_query_param = 'limit'

    queryset = User.objects.all()
    serializer_class = BaseUserSerializer
    pagination_class = UserPagination

    @decorators.action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscriptions(self, request):
        pages = self.paginate_queryset(
            User.objects.filter(subscribing__user=request.user)
        )
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request},
        )
        return self.get_paginated_response(serializer.data)

    @decorators.action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)

        if request.method == 'POST':
            serializer = SubscribeSerializer(
                author,
                data=request.data,
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user, author=author)
            return response.Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        get_object_or_404(
            Subscription,
            user=user,
            author=author,
        ).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
