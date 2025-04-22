from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.auth_users.serializers import EmailSerializer, PasswordSerializer
from core.services.jwt_service import JWTService, RecoveryToken, ActivateToken
from django.contrib.auth import get_user_model
from rest_framework import status

UserModel = get_user_model()
User = get_user_model()


class CurrentUserView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({
            "id": user.id,
            "name": user.name,
            "surname": user.surname,
            "role": user.role,
        }, status=status.HTTP_200_OK)


class ActivateUserView(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, *args, **kwargs):
        token = kwargs['token']
        user = JWTService.verify_token(token, ActivateToken)
        user.is_active = True
        user.save()
        return Response({'detail': 'Activated'}, status.HTTP_200_OK)


class RecoveryPasswordRequestView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(UserModel, **serializer.validated_data)
        token = JWTService.create_token(user, RecoveryToken)
        return Response({"token": token["access"]})


class RecoverPasswordView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordSerializer

    def post(self, request, token):
        return self._set_password(request, token)

    def patch(self, request, token):
        return self._set_password(request, token)

    def _set_password(self, request, token):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            decoded = JWTService.verify_token(token, RecoveryToken)
        except Exception:
            decoded = JWTService.verify_token(token, ActivateToken)

        user = User.objects.get(id=decoded["user_id"])

        user.set_password(serializer.validated_data["password"])
        user.is_active = True
        user.save()

        return Response({"detail": "Password was set"}, status=status.HTTP_200_OK)


class SocketView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        token = JWTService.create_token(request.user)
        return Response({'token': token['access']})
