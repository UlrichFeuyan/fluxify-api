from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, codeuser, password=None, **extra_fields):
        if not codeuser:
            raise ValueError('The codeuser field must be set')
        email = self.normalize_email(extra_fields.get('email'))
        user = self.model(codeuser=codeuser, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, codeuser, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(codeuser, password, **extra_fields)


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

    objects = CustomUserManager()
