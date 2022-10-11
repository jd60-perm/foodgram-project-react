from api.serializers import FollowSerializer
from dblogic.models import Follow
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class CustomUserViewSet(UserViewSet):
    permission_classes = IsAuthenticated,

    @action(detail=False, methods=['get', ])
    def subscriptions(self, request):
        following = Follow.objects.filter(follower=self.request.user)
        page = self.paginate_queryset(following)
        if page is not None:
            serializer = FollowSerializer(
                following, many=True, context={'request': request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = FollowSerializer(
            following, many=True, context={'request': request}
        )
        return Response(serializer.data)
