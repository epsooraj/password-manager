from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets

from . import serializers
from . import models
from . import permissions


class PasswordViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PasswordSerializer
    permission_classes = (permissions.OwnerOrUserWithOwnersPermission,)

    def get_queryset(self):

        if self.kwargs.get('pk'):
            return models.Password.objects.all()

        return models.Password.objects.filter(user=self.request.user)


class SharePermissionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SharedUserSerializer
    permission_classes = (permissions.ShareOwnerOnlyPermission,)

    def get_queryset(self):
        pid = self.kwargs.get('pid')
        return models.Password.objects.get(id=pid).access_users.all()
