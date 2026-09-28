from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from common.models import BaseModel

from .choices import UserRole
from .managers import UserManager


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.
    """

    email = models.EmailField(
        unique=True,
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.PATIENT,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_verified = models.BooleanField(
        default=False,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    def __str__(self):
        return self.email
