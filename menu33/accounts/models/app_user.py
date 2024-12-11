from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin

from menu33.accounts.managers import AppUserManager


class AppUser(AbstractBaseUser, PermissionsMixin):
    use_in_migrations = True
    email = models.EmailField(
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )  # when creates a user it will be activ

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = "email"  # the first credential that we will be authenticate
    REQUIRED_FIELDS = []  # not so necessary
    objects = AppUserManager()


