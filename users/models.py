from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='электронная почта')
    phone = models.CharField(max_length=50, verbose_name='номер телефона', **NULLABLE)
    city = models.CharField(max_length=150, verbose_name='город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', **NULLABLE)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []




