from rest_framework import serializers
from ecommerce_api.models import *
from django.contrib.auth import get_user_model

User = get_user_model() # this will return value in AUTH_USER_MODEL in settings

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'address')  # Customize based on your needs
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'
        

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

