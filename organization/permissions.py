from rest_framework import permissions
from . import models


class OwnerOrUserInOrganizationPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True

        # Check if user has access rights
        # Read
        if request.method in permissions.SAFE_METHODS:
            return len(obj.shared_users.filter(user__in=[request.user])) > 0

        # Write
        return len(obj.shared_users.filter(user__in=[request.user], permission='w')) > 0


class OwnerOnlySharePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            oid = request.resolver_match.kwargs.get('oid')
            return len(models.Organization.objects.filter(id=oid, user=request.user)) > 0

    def has_object_permission(self, request, view, obj):
        if obj.organization_set.all().first().user == request.user:
            return True

        return False


class OwnerOrUserInOrgPasswordPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            oid = request.resolver_match.kwargs.get('oid')
            if len(models.Organization.objects.filter(id=oid, user=request.user)) > 0:
                return True

            if request.method == 'GET':
                return len(models.Organization.objects.filter(id=oid).first(
                ).shared_users.filter(user__in=[request.user])) > 0
            else:
                return len(models.Organization.objects.filter(id=oid).first().shared_users.filter(
                    user__in=[request.user], permission='w')) > 0

    def has_object_permission(self, request, view, obj):
        if obj.organization_set.all().first().user == request.user:
            return True

        # Check if user has access rights
        # Read
        if request.method in permissions.SAFE_METHODS:
            return len(obj.organization_set.all().first().shared_users.filter(user__in=[request.user])) > 0

        # Write
        return len(obj.organization_set.all().first().shared_users.filter(user__in=[request.user], permission='w')) > 0
