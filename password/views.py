from rest_framework import viewsets

from . import serializers
from . import models
from . import permissions


class PasswordViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PasswordSerializer
    permission_classes = (permissions.OwnerOrUserWithOwnerPermission,)

    def get_queryset(self):

        if self.kwargs.get('pk'):
            return models.Password.objects.all()

        return models.Password.objects.filter(user=self.request.user)
