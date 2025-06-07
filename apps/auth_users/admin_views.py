from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.auth_users.models import CustomUser
from apps.auth_users.serializers import ManagerSerializer
from core.permissions.is_admin_and_is_manager_permission import IsAdmin
from core.services.jwt_service import JWTService, ActivateToken, RecoveryToken


class CreateManagerView(CreateAPIView):
    permission_classes = [IsAdmin]
    queryset = CustomUser.objects.all()
    serializer_class = ManagerSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        user.set_unusable_password()
        user.save()


class AdminStatsView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        from apps.orders.models import Orders
        stats = Orders.objects.values("status").annotate(count=Count("id"))
        return Response(stats)


class ActivateManagerLinkView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        manager = get_object_or_404(CustomUser, id=request.data["manager_id"])
        token = JWTService.create_token(manager, ActivateToken)
        return Response({"token": token["access"]})


class RecoveryManagerLinkView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        manager = get_object_or_404(CustomUser, id=request.data["manager_id"])
        token = JWTService.create_token(manager, RecoveryToken)
        return Response({"token": token["access"]})


class BanManagerView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        manager = get_object_or_404(CustomUser, id=request.data["manager_id"])
        manager.is_active = False
        manager.save()
        return Response({'detail': 'Manager banned'})


class UnbanManagerView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        manager = get_object_or_404(CustomUser, id=request.data["manager_id"])
        manager.is_active = True
        manager.save()
        return Response({'detail': 'Manager unbanned'})


class DeleteManagerView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        manager = get_object_or_404(CustomUser, id=request.data["manager_id"])
        if manager.is_active:
            return Response({"error": "Manager must be banned first"}, status=400)
        manager.delete()
        return Response({"detail": "Manager deleted"})
