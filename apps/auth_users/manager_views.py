from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAdminUser
from django.db.models import Count, Q

from apps.auth_users.models import CustomUser
from apps.auth_users.serializers import ManagerSerializer


class ManagerViewSet(ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all().annotate(
        total_orders=Count("orders"),
        in_work_orders=Count("orders", filter=Q(orders__status="In Work"))
    )
    serializer_class = ManagerSerializer
    permission_classes = [IsAdminUser]
