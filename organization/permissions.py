from re import L
from rest_framework import permissions
from . import models


class OwnerOrUserInOrganizationPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True

        try:
            # Check if user has access rights
            # Read
            if request.method in permissions.SAFE_METHODS:
                return len(obj.members.filter(user__in=[request.user])) > 0

            # Write
            return len(obj.members.filter(user__in=[request.user], permission='w')) > 0
        except:
            return False


class OwnerOnlySharePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                oid = request.resolver_match.kwargs.get('oid')
                return len(models.Organization.objects.filter(id=oid, user=request.user)) > 0
            except:
                pass

    def has_object_permission(self, request, view, obj):
        try:
            if obj.organization_set.all().first().user == request.user:
                return True
        except:
            pass

        return False


class OwnerOrUserInOrgPasswordPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            oid = request.resolver_match.kwargs.get('oid')
            if len(models.Organization.objects.filter(id=oid, user=request.user)) > 0:
                return True

            try:
                if request.method == 'GET':
                    return len(models.Organization.objects.filter(id=oid).first(
                    ).members.filter(user__in=[request.user])) > 0
                else:
                    return len(models.Organization.objects.filter(id=oid).first().members.filter(
                        user__in=[request.user], permission='w')) > 0
            except:
                return False

    def has_object_permission(self, request, view, obj):
        if obj.organization_set.all().first().user == request.user:
            return True

        try:
            # Check if user has access rights
            # Read
            if request.method in permissions.SAFE_METHODS:
                return len(obj.organization_set.all().first().members.filter(user__in=[request.user])) > 0

            # Write
            return len(obj.organization_set.all().first().members.filter(user__in=[request.user], permission='w')) > 0
        except:
            return False
