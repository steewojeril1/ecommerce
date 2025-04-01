from rest_framework import viewsets, permissions, status
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied




class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    # get/terieve
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)
    # post
    def perform_create(self, serializer):
        user = self.request.user
        if user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("You are not allowed to create other users.")
    # put/patch
    def perform_update(self, serializer):
        user = self.request.user
        if user.is_staff or serializer.instance == user:
            serializer.save()
        else:
            raise PermissionDenied("You can only update your own profile.")
    # delete
    def perform_destroy(self, instance):
        user = self.request.user
        if user.is_staff or instance == user:
            instance.delete()
        else:
            raise PermissionDenied("You can only delete your own profile.")


class SignupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can sign up

    # perform_create() -post   perform_update()-put/patch   perform_destroy()
    # calls during list() or retrieve().

    def get_queryset(self):
        # Prevent listing all users
        return User.objects.none()


class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = [permissions.IsAdminUser]

class AdminProductView(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
