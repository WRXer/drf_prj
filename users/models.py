from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}

# Create your models here.
class User(AbstractUser):
    username=None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, **NULLABLE)
    name = models.CharField(max_length=100, verbose_name="имя пользователя", **NULLABLE)
    city = models.CharField(max_length=100, **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='подтверждение почты')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []