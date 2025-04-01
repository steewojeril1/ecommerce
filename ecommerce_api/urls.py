from rest_framework.routers import DefaultRouter
from ecommerce_api import views
from django.urls import path, include

router = DefaultRouter()

router.register('admin/categories', views.CategoryView, basename='api-admin-categories') # no need of trailing slashes
router.register('admin/products', views.AdminProductView, basename='api-admin-products')
router.register('users', views.CustomUserViewSet, basename='api-user')


urlpatterns=[
    path('',include(router.urls))
]