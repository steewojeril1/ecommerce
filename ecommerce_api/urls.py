from rest_framework.routers import DefaultRouter
from ecommerce_api import views
from django.urls import path, include

router = DefaultRouter()

router.register('admin/categories', views.CategoryView, basename='admin-categories') # no need of trailing slashes
router.register('admin/products', views.AdminProductView, basename='admin-products')

urlpatterns=[
    path('',include(router.urls))
]