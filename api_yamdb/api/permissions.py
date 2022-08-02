from rest_framework import permissions


class AuthorModerAdminOrReadOnly(permissions.BasePermission):
    """Разрешение только для админа, модератора или владельца."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
            or request.user.is_superuser
            or request.user == obj.author
        )


class IsOwnerOrAdmins(permissions.BasePermission):
    """Разрешение только для админа или владельца."""

    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.role == 'admin'


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """Разрешение только для админа или только на чтение."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.role == 'admin')
        )
