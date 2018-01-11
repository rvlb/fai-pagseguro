from django.db import models
from django.contrib.auth.models import AbstractUser

from products.models import OrderProduct

class User(AbstractUser):
    pass

class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct, blank=True)