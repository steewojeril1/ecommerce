from django.db import models
from django.contrib.auth.models import AbstractUser

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
