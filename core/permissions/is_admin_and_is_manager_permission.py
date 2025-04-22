from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Дозвіл для адміністраторів.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsManager(BasePermission):
    """
    Дозвіл для менеджерів.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'manager'
