from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q # (.filter(Q(...))) and also in model constraints (like UniqueConstraint) to add conditions.
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator



class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True) # blank - Field is allowed to be empty in forms # null - Field is allowed to store NULL in the database
    address = models.TextField(blank=True, null=True)


class Categories(models.Model):
    cat_name = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.cat_name

class Products(models.Model):
    pro_name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    description = models.CharField(max_length=250, null=True)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images', null=True, blank=True) # need pillow library

    def __str__(self) -> str:
        return self.pro_name

class Carts(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    created_date = models.DateTimeField(auto_now_add=True)
    options = (
        ('incart', 'In Cart'),
        ('order_placed', 'Order Placed'),
        ('cancelled', 'Cancelled')
    )
    status = models.CharField(max_length=120, choices=options, default='incart')

    class Meta:
            constraints = [
                models.UniqueConstraint(
                    fields=['user', 'product'],
                    condition=Q(status='incart'),
                    name='unique_active_cart_item'
                )
            ]    # Only one active (‘incart’) item is allowed per (user, product). But if it’s already ordered or cancelled, you can add it again.


class Orders(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    created_date = models.DateTimeField(auto_now_add=True)
    options = (
        ('order_placed', 'Order Placed'),
        ('dispatched', 'Dispatched'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    )
    status = models.CharField(max_length=120, choices=options, default='order_placed')
    address = models.CharField(max_length=200, null=True)
    expected_date = models.DateField(null=True)
    # no unique together('user','product')a user can order the same product multiple times. eg: (1,2) - this can be occur again
class Reviews(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comments = models.CharField(max_length=200)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    class Meta:
         constraints = [
              models.UniqueConstraint(
                   fields=['user','product'],
                   name='unique_review_per_product'
              )
         ]
