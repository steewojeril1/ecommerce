from django.db import models


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
