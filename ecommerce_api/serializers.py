from rest_framework import serializers
from ecommerce_api.models import *
from django.contrib.auth import get_user_model

User = get_user_model() # this will return value in AUTH_USER_MODEL in settings

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'address')  # Customize based on your needs
        read_only_fields = ['id']

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # write only

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'phone', 'address']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)   # to hash the password use create_uer()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'
        

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    product = serializers.CharField(read_only=True)

    class Meta:
        model = Carts
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        product=self.context.get("product")
        return Carts.objects.create(user=user, product=product, **validated_data)

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)  # User is set automatically in the view
    product = serializers.CharField(read_only=True)  # Product is selected from the cart, no need for input

    class Meta:
        model = Orders
        fields = '__all__'

    def create(self, validated_data):
        cart_instances = self.context.get("cart_instances")
        user = self.context.get("user")
        address = self.context.get("address")
        expected_date = self.context.get("expected_date")
        
        created_orders = []

        # Loop through the cart instances and create an order for each cart item
        for item in cart_instances:
            order = Orders.objects.create(
                user=user,
                product=item.product,
                quantity=item.quantity,
                address=address,
                expected_date=expected_date,
            )
            created_orders.append(order)
            
            # Update the cart item status to "order_placed" after creating the order
            item.status = 'order_placed'
            item.save()

        return created_orders  # Return a list of the created orders