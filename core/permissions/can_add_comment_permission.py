from rest_framework.permissions import BasePermission


class CanAddComment(BasePermission):
    """
    Дозволяє додавати коментарі тільки якщо:
    - У заявки немає менеджера.
    - Або менеджером є поточний користувач.
    """

    def has_object_permission(self, request, view, obj):
        return not obj.manager or obj.manager == request.user
