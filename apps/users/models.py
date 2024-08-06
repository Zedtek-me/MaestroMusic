from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from .managers import UserManager
from interfaces.base_models import BaseModel


class User(AbstractBaseUser, BaseModel):
    '''user model'''
    USER_STATUSES = (
        ("ACTIVE", "ACTIVE"),
        ("DELETED", "DELETED"),
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=128, null=True)
    last_name = models.CharField(max_length=128, null=True)
    username = models.CharField(max_length=128, null=True)
    password = models.CharField(max_length=128, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    status = models.CharField(max_length=128, default="ACTIVE")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username", "password"]
    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return f"{self.email}"

