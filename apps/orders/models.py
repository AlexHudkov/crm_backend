from django.db import models
from django.conf import settings

from apps.groups.models import Group
from apps.orders.choices import STATUS_CHOICES, COURSE_CHOICES, COURSE_FORMAT_CHOICES, COURSE_TYPE_CHOICES


class Orders(models.Model):
    name = models.CharField(max_length=25, null=True, blank=True)
    surname = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    course = models.CharField(max_length=10, choices=COURSE_CHOICES, null=True, blank=True)
    course_format = models.CharField(max_length=15, choices=COURSE_FORMAT_CHOICES, null=True, blank=True)
    course_type = models.CharField(max_length=100, choices=COURSE_TYPE_CHOICES, null=True, blank=True)
    sum = models.IntegerField(null=True, blank=True)
    already_paid = models.IntegerField(db_column='alreadyPaid', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    utm = models.CharField(max_length=100, null=True, blank=True)
    msg = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, null=True, blank=True, db_index=True)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='orders',
        default=None
    )
    group = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f"{self.name} {self.surname} - {self.course}"


class Comment(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author_id} on Order #{self.order.id}"
