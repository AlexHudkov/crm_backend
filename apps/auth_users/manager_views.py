from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import Count, Q

from apps.auth_users.models import CustomUser
from apps.auth_users.serializers import ManagerSerializer
from core.permissions.is_admin_and_is_manager_permission import IsAdmin


class ManagerViewSet(ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all().annotate(
        total_orders=Count("orders"),
        in_work_orders=Count("orders", filter=Q(orders__status="In Work")),
        aggre_orders=Count("orders", filter=Q(orders__status="Aggre")),
        disaggre_orders=Count("orders", filter=Q(orders__status="Disaggre")),
        dubbing_orders=Count("orders", filter=Q(orders__status="Dubbing"))
    )
    serializer_class = ManagerSerializer
    permission_classes = [IsAdmin]
