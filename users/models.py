from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


NULLABLE = {'blank': True, 'null': True}

# Create your models here.
class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Необходимо указать адрес электронной почты')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('У суперпользователя должен быть is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('У суперпользователя должен быть is_superuser=True')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, **NULLABLE)
    name = models.CharField(max_length=100, verbose_name="имя пользователя", **NULLABLE)
    city = models.CharField(max_length=100, **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='подтверждение почты')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()