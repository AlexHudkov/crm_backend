from rest_framework import serializers
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
