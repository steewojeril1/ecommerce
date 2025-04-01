from rest_framework import viewsets, permissions, status
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied




class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("You are not allowed to create other users.")

    def perform_update(self, serializer):
        user = self.request.user
        if user.is_staff or serializer.instance == user:
            serializer.save()
        else:
            raise PermissionDenied("You can only update your own profile.")

    def perform_destroy(self, instance):
        user = self.request.user
        if user.is_staff or instance == user:
            instance.delete()
        else:
            raise PermissionDenied("You can only delete your own profile.")
        
class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = [permissions.IsAdminUser]

class AdminProductView(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
