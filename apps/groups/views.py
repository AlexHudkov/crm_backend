from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Group
from .serializers import GroupSerializer


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """Отримання списку груп"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """Створення нової групи, перевірка на унікальність"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            group_name = serializer.validated_data.get('name')
            if Group.objects.filter(name=group_name).exists():
                return Response(
                    {"error": "Group with this name already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
