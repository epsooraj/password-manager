from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets

from .permissions import OwnerOnlySharePermission, OwnerOrUserInOrgPasswordPermission, OwnerOrUserInOrganizationPermission
from . import models
from . import serializers
from password import serializers as password_serializers


class OrganizationViewSet(viewsets.ModelViewSet):
    permission_classes = (OwnerOrUserInOrganizationPermission,)
    serializer_class = serializers.OrganizationSerializer

    def get_queryset(self):
        # Filtering user's organization
        # and organizations which user has access to
        return (models.Organization.objects.filter(user=self.request.user) | models.Organization.objects.filter(members__user=self.request.user)).distinct()


class OrgAccessUserViewSet(viewsets.ModelViewSet):
    permission_classes = (OwnerOnlySharePermission,)
    serializer_class = password_serializers.SharedUserSerializer

    def get_queryset(self):
        pid = self.kwargs.get('oid')
        return models.Organization.objects.get(id=pid).members.all()

    def perform_create(self, serializer):
        obj = serializer.save()

        try:
            oid = self.kwargs.get('oid')
            org_obj = models.Organization.objects.get(id=oid)
            org_obj.members.add(obj)
        except ObjectDoesNotExist:
            pass

        return obj


class OrgPasswordViewSet(viewsets.ModelViewSet):
    permission_classes = (OwnerOrUserInOrgPasswordPermission,)
    serializer_class = serializers.OrganizationPasswordSerializer

    def get_queryset(self):
        pid = self.kwargs.get('oid')
        return models.Organization.objects.get(id=pid).passwords.all()

    def perform_create(self, serializer):
        obj = serializer.save()

        try:
            oid = self.kwargs.get('oid')
            org_obj = models.Organization.objects.get(id=oid)
            org_obj.passwords.add(obj)
        except ObjectDoesNotExist:
            pass

        return obj
