from django.db import models


class UsedToken(models.Model):
    jti = models.CharField(max_length=255, unique=True)  # JWT ID
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.jti
