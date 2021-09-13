from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=100)
    point = models.IntegerField(default=0)
    grade = models.CharField(max_length=10,default="나무")