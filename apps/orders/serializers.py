from rest_framework import serializers
from django.core.validators import RegexValidator

from .models import Orders, Comment


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.surname', read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'author_name', 'author_id']


class OrdersSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.surname', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    manager_id = serializers.IntegerField(source="manager.id", read_only=True)
    age = serializers.IntegerField(min_value=0, max_value=120, required=False)
    sum = serializers.DecimalField(max_digits=10, decimal_places=0, min_value=0, required=False, allow_null=True)
    already_paid = serializers.DecimalField(max_digits=10, decimal_places=0, min_value=0, required=False,
                                            allow_null=True)
    name = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        max_length=25,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zА-Яа-яЁёІіЇїЄєҐґ]+$',
                message="Name must contain only letters without numbers or special characters."
            )
        ]
    )
    surname = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        max_length=25,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zА-Яа-яЁёІіЇїЄєҐґ]*$',
                message="Surname must contain only letters without numbers or special characters."
            )
        ]
    )

    class Meta:
        model = Orders
        fields = '__all__'


def to_representation(self, instance):
    data = super().to_representation(instance)
    request = self.context.get("request")

    if not request:
        return data

    user = request.user

    if user.role != "admin" and instance.manager != user:
        data.pop("comments", None)

    return data
