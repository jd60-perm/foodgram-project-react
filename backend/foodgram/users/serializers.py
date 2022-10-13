from dblogic.models import Follow
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from djoser.conf import settings
from djoser.serializers import TokenCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import User


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'is_subscribed',
        )
        read_only_fields = (settings.LOGIN_FIELD,)

    def get_is_subscribed(self, obj):
        if not isinstance(self.context['request'].user, AnonymousUser):
            return Follow.objects.filter(
                follower=self.context['request'].user,
                following=obj
            ).exists()
        return False


class CustomTokenCreateSerializer(TokenCreateSerializer):

    def validate(self, attrs):
        password = attrs.get("password")
        params = {
            settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD).lower()
        }
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        if self.user and self.user.is_active:
            return attrs
        self.fail("invalid_credentials")
