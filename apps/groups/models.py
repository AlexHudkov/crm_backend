from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=55, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'learning_groups'

    def __str__(self):
        return self.name
