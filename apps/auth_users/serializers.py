from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.auth_users.models import CustomUser
from core.dataclasses.user_dataclass import User

UserModel: User = get_user_model()


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('password',)


class ManagerSerializer(serializers.ModelSerializer):
    total_orders = serializers.IntegerField(read_only=True)
    in_work_orders = serializers.IntegerField(read_only=True)
    last_login_formatted = serializers.SerializerMethodField()
    has_password = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["id", "email", "name", "surname", "is_active", "last_login", "last_login_formatted", "total_orders",
                  "in_work_orders", "has_password"]

    def get_has_password(self, obj):
        return obj.has_usable_password()

    def get_last_login_formatted(self, obj):
        if obj.last_login:
            formatted_time = obj.last_login.strftime("%d.%m.%Y, %H:%M:%S")
            return formatted_time

        return None
