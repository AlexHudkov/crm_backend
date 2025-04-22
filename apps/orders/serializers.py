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

    class Meta:
        model = Orders
        fields = '__all__'

