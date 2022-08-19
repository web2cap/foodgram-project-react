from rest_framework import permissions


class PostOrAutorised(permissions.BasePermission):
    """Method POST OR Autorised request"""

    def has_permission(self, request, view):
        return request.method == "POST" or request.user.is_authenticated
