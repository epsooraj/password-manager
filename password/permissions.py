from rest_framework import permissions


class OwnerOrUserWithOwnerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if obj.user == request.user:
            return True

        # Check if user has access rights

        # Read
        if request.method in permissions.SAFE_METHODS:
            return len(obj.access_users.filter(user__in=[request.user])) > 0
        # Write
        return len(obj.access_users.filter(user__in=[request.user], permission='w')) > 0
