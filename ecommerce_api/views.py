from rest_framework import viewsets, permissions, status
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action



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


# we're using ReadOnlyModelViewSet because you're not allowing full access to products like admins can.
# or we can use viewset but need to define list retrieve
# we only want read-only access (list, retrieve). we’re not exposing POST/PUT/DELETE through this view
class UserProductView(viewsets.ReadOnlyModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # url: api/ekart/products/<pid>/add_to_cart/
    @action(methods=["post"],detail=True)
    def add_to_cart(self, request, *args, **kwargs):
        product = self.get_object()  # shortcut: same as Products.objects.get(pk=kwargs['pk'])
        data = {
            "product": product.id,
            "quantity": request.data.get("quantity", 1),
            "status": "incart"
        }

        serializer = CartSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET /api/ekart/mycart/    x - POST, PUT, PATCH, DELETE
class CartView(viewsets.ReadOnlyModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user, status='incart').order_by('-created_date')
