from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "Email is required",
            "invalid": "Enter a valid email address",
        },
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={"required": "Password is required"},
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                username=email,
                password=password,
            )
            if not user:
                raise serializers.ValidationError(
                    _("Invalid email or password."),
                    code="authorization",
                )
        else:
            raise serializers.ValidationError(
                _("Both email and password are required."),
                code="authorization",
            )

        attrs["user"] = user
        return attrs
