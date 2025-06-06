from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken, Token

from apps.tokens.models import UsedToken


class JWTService:
    @staticmethod
    def create_token(user, token_class=None):
        if token_class is None:
            refresh = RefreshToken.for_user(user)
            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

        token = token_class.for_user(user)
        return {
            "access": str(token)
        }

    @staticmethod
    def verify_token(token, token_class=None):
        try:
            decoded = token_class(token)

            if UsedToken.objects.filter(jti=decoded["jti"]).exists():
                raise ValueError("This token has already been used")

            return decoded
        except Exception as e:
            raise ValueError(f"Invalid token: {e}")


class ActionToken(Token):
    token_type = "action"
    lifetime = timedelta(minutes=30)


class ActivateToken(ActionToken):
    token_type = "activate"
    lifetime = timedelta(minutes=30)


class RecoveryToken(ActionToken):
    token_type = "recovery"
    lifetime = timedelta(minutes=30)


class SocketToken(ActionToken):
    token_type = "socket"
    lifetime = timedelta(minutes=30)
