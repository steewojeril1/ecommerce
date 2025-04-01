from rest_framework import viewsets, permissions, status
from .serializers import *
from .models import *
from rest_framework.response import Response



class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    permission_classes = [permissions.IsAdminUser]

class AdminProductView(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
