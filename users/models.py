from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    codeuser = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = None

    USERNAME_FIELD = 'codeuser'
    REQUIRED_FIELDS = []
