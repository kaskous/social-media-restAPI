from rest_framework.permissions import BasePermission


class IsValidUser(BasePermission):
    """
    Allows access only to valid users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_valid
