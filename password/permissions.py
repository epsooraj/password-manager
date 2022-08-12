from rest_framework import permissions
from . import models


class OwnerOrUserWithOwnersPermission(permissions.BasePermission):

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
                return len(obj.access_users.filter(user__in=[request.user])) > 0

            # Write
            return len(obj.access_users.filter(user__in=[request.user], permission='w')) > 0
        except:
            return False


class ShareOwnerOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # If corresponding password object belong to the user
            pid = request.resolver_match.kwargs.get('pid')
            return len(models.Password.objects.filter(id=pid, user=request.user)) > 0

    def has_object_permission(self, request, view, obj):

        try:
            if obj.password_set.all().first().user == request.user:
                return True
        except:
            pass

        return False
